"""ReportLab rendering, retaining the recovered 1.7.0 design."""

import functools
import io
import json
import os
from datetime import datetime, timezone
from html import escape

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from .content import load_chapter
from .provenance import (
    input_inventory,
    local_path,
    read_json,
    runtime_metadata,
    sha256,
    verify_assets,
)


class DeterministicCanvas(Canvas):
    def __init__(self, *args, source_epoch, **kwargs):
        # ReportLab's invariant mode still honours an ambient SOURCE_DATE_EPOCH.
        # This renderer is a single-process CLI; bind it to the edition, then restore.
        previous = os.environ.get('SOURCE_DATE_EPOCH')
        os.environ['SOURCE_DATE_EPOCH'] = str(source_epoch)
        try:
            super().__init__(*args, **kwargs)
        finally:
            if previous is None:
                os.environ.pop('SOURCE_DATE_EPOCH', None)
            else:
                os.environ['SOURCE_DATE_EPOCH'] = previous


class Design:
    def __init__(self, root, output):
        self.root, self.output = root, output
        self.edition = read_json(root / 'content/editions/1.7.0/en/edition.json')
        self.theme = read_json(root / 'templates/tagcast/theme.json')
        self.screenshots, fonts, self.figures = verify_assets(root)
        for variant, alias in [('Regular', 'Guide'), ('Bold', 'Guide-Bold'),
                               ('Italic', 'Guide-Italic'), ('BoldItalic', 'Guide-BoldItalic')]:
            font = TTFont(alias, str(local_path(root, fonts[variant]['path'])))
            # The original Arial bold middle dot has a wider advance. Keep that
            # measured design metric without modifying the bundled font file.
            for codepoint, width in self.theme['font_width_overrides'].get(variant, {}).items():
                font.face.charWidths[int(codepoint)] = width
            pdfmetrics.registerFont(font)
        pdfmetrics.registerFontFamily('Guide', normal='Guide', bold='Guide-Bold',
                                      italic='Guide-Italic', boldItalic='Guide-BoldItalic')
        self.palette = {k: colors.HexColor(v) for k, v in self.theme['colors'].items()}
        self.width, self.height = self.theme['page_size']
        self.margin = self.theme['margin']
        self.cw = self.width - 2 * self.margin
        self.styles = {}
        for name, values in self.theme['styles'].items():
            values = dict(values)
            values['textColor'] = self.palette[values['textColor']]
            self.styles[name] = ParagraphStyle(name, **values)
        base = root / 'content/editions/1.7.0/en'
        self.chapters = [load_chapter(local_path(root, (base / name).relative_to(root)))
                         for name in read_json(base / 'chapters.json')]
        ids = [chapter['id'] for chapter in self.chapters]
        if len(ids) != len(set(ids)):
            raise ValueError('Chapter IDs must be unique')
        self.image_uses = []

    def paragraph(self, text, kind='body'):
        text = text.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', ' - ').replace('\u00a0', ' ')
        return Paragraph(text, self.styles[kind])

    def data_table(self, block):
        data = [[self.paragraph(value, 'cellhead' if block['headers'] and i == 0 else 'cell')
                 for value in row] for i, row in enumerate(block['rows'])]
        table = Table(data, colWidths=[self.cw * w for w in block['widths']], hAlign='LEFT')
        rules = [('VALIGN', (0, 0), (-1, -1), 'TOP'),
                 ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
                 ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                 ('LINEBELOW', (0, 0), (-1, -1), .45, self.palette['LINE'])]
        if block['headers']:
            rules.append(('BACKGROUND', (0, 0), (-1, 0), self.palette['PALE']))
        table.setStyle(TableStyle(rules))
        return table

    def callout(self, title, text):
        table = Table([[self.paragraph(f'<b>{title}</b><br/>{text}', 'note')]], colWidths=[self.cw])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.palette['PALE']),
            ('BOX', (0, 0), (-1, -1), .4, self.palette['LINE']),
            ('LINEBEFORE', (0, 0), (0, -1), 3, self.palette['TEAL']),
            ('LEFTPADDING', (0, 0), (-1, -1), 13), ('RIGHTPADDING', (0, 0), (-1, -1), 13),
            ('TOPPADDING', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]))
        return [Spacer(1, 5), table, Spacer(1, 10)]

    def figure(self, block):
        spec = self.figures[block['id']]
        asset = self.screenshots[spec['asset']]
        source = local_path(self.root, asset['path'])
        with PILImage.open(source) as original:
            image = original.convert('RGB')
        if spec['crop']:
            iw, ih = image.size
            image = image.crop(tuple(round(v * (iw if i % 2 == 0 else ih))
                                     for i, v in enumerate(spec['crop'])))
        image.thumbnail((2400, 2100), PILImage.Resampling.LANCZOS)
        stream = io.BytesIO()
        image.save(stream, format='JPEG', quality=91, subsampling=0)
        stream.seek(0)
        iw, ih = image.size
        scale = min(spec['width'] / iw, spec['max_height'] * 1.13 / ih)
        self.image_uses.append(dict(id=block['id'], asset=spec['asset'], crop=spec['crop'],
                                    original_sha256=asset['sha256']))
        return [Spacer(1, 3), Image(stream, width=iw * scale, height=ih * scale, hAlign='LEFT'),
                self.paragraph(block['caption'], 'caption')]

    def blocks(self, blocks):
        result = []
        for block in blocks:
            kind = block['type']
            if kind == 'text':
                result.append(self.paragraph(block['text'], block['kind']))
            elif kind == 'figure':
                result.extend(self.figure(block))
            elif kind == 'callout':
                result.extend(self.callout(block['title'], block['text']))
            elif kind == 'table':
                result.append(self.data_table(block))
            elif kind == 'columns':
                cells = [self.blocks(cell) for cell in block['cells']]
                table = Table([cells], colWidths=[236, self.cw - 236], hAlign='LEFT')
                table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (0, 0), 14), ('RIGHTPADDING', (1, 0), (1, 0), 0)]))
                result.append(table)
            elif kind == 'gallery':
                cells = [self.blocks(cell) for cell in block['cells']]
                table = Table([cells[:2], cells[2:]], colWidths=[self.cw / 2] * 2)
                table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12), ('TOPPADDING', (0, 0), (-1, -1), 0),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
                result.append(table)
            else:
                raise ValueError(f'Unknown content block: {kind}')
        return result

    def story(self, destinations):
        self.image_uses = []
        story = [Cover(self), PageBreak()]
        title = self.paragraph('Contents', 'title')
        title.bookmark_key = 'contents'
        story.extend([title, self.paragraph(self.edition['contents_lead'], 'lead')])
        half = (len(self.chapters) + 1) // 2
        columns = []
        for lo, hi in [(0, half), (half, len(self.chapters))]:
            rows, last = [], None
            for chapter in self.chapters[lo:hi]:
                if chapter['group'] != last:
                    rows.append([self.paragraph(chapter['group'], 'kicker'), ''])
                    last = chapter['group']
                key = chapter['id']
                label = escape(chapter['title'])
                page = destinations.get(key, 0)
                rows.append([self.paragraph(f'<link href="#{key}">{label}</link>', 'toc'),
                             self.paragraph(f'<link href="#{key}">{page:02d}</link>', 'toc')])
            table = Table(rows, colWidths=[self.cw / 2 - 35, 22])
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5), ('TOPPADDING', (0, 0), (-1, -1), 1.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
            columns.append(table)
        spread = Table([columns], colWidths=[self.cw / 2] * 2)
        spread.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)]))
        story.extend([spread, Spacer(1, 12)])
        story.extend(self.callout(**self.edition['contents_note']))
        for chapter in self.chapters:
            title = self.paragraph(escape(chapter['title']), 'title')
            title.bookmark_key = chapter['id']
            story.extend([PageBreak(), self.paragraph(chapter['group'], 'kicker'), title,
                          self.paragraph(escape(chapter['lead']), 'lead')])
            story.extend(self.blocks(chapter['blocks']))
            if chapter['wiki']:
                base = 'https://github.com/cyberdeliaAI/tagcast/wiki/'
                story.append(self.paragraph(
                    f'<link href="{base}{escape(chapter["wiki"], quote=True)}" color="#276b7d">More in the Wiki</link>'
                    f'  /  <link href="{base}Home" color="#276b7d">Documentation home</link>', 'small'))
        return story


class GuideDoc(BaseDocTemplate):
    def __init__(self, stream, design):
        self.design, self.seen = design, {}
        super().__init__(stream, pagesize=(design.width, design.height),
                         leftMargin=design.margin, rightMargin=design.margin,
                         topMargin=69, bottomMargin=49, title=design.edition['title'],
                         author='Tagcast', subject=design.edition['subject'],
                         creator='Tagcast Manual 0.1.0', pageCompression=1, allowSplitting=1,
                         invariant=1, lang=design.edition['language'])
        self.addPageTemplates(PageTemplate(id='guide', frames=[Frame(
            design.margin, 49, design.cw, design.height - 118, id='normal',
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=self.chrome))

    def chrome(self, canvas, doc):
        if doc.page == 1:
            return
        d = self.design
        canvas.saveState()
        canvas.setStrokeColor(d.palette['LINE'])
        canvas.setLineWidth(.5)
        canvas.line(d.margin, d.height - 46, d.width - d.margin, d.height - 46)
        canvas.setFillColor(d.palette['TEAL'])
        canvas.setFont('Guide-Bold', 8)
        canvas.drawString(d.margin, d.height - 34, 'TAGCAST  /  USER MANUAL')
        canvas.setFillColor(d.palette['MUTED'])
        canvas.setFont('Guide', 8)
        canvas.drawRightString(d.width - d.margin, d.height - 34, 'VERSION ' + d.edition['app_version'])
        canvas.line(d.margin, 40, d.width - d.margin, 40)
        canvas.drawString(d.margin, 26, 'tagcast.app')
        canvas.drawRightString(d.width - d.margin, 26, f'{doc.page:02d}')
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if key := getattr(flowable, 'bookmark_key', None):
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, 0, False)
            self.seen[key] = self.page


class Cover(Flowable):
    def __init__(self, design):
        super().__init__()
        self.design = design
        self.width, self.height = design.cw, design.height - 119

    def draw(self):
        d, c, top = self.design, self.canv, self.height
        cover = d.edition['cover']
        c.setFillColor(d.palette['INK'])
        c.rect(-d.margin, -49, d.width, d.height, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#8bd4df'))
        c.setFont('Guide-Bold', 10)
        c.drawString(0, top - 35, cover['kicker'])
        c.setFillColor(colors.white)
        for font, size, x, y, text in [('Guide-Bold', 57, -2, top - 109, 'Tagcast.'),
                                      ('Guide', 27, 0, top - 153, cover['title'])]:
            c.setFont(font, size)
            c.drawString(x, y, text)
        c.setFillColor(colors.HexColor('#b7d0d9'))
        c.setFont('Guide', 12)
        c.drawString(0, top - 183, cover['edition'])
        image = local_path(d.root, d.screenshots[cover['asset']]['path'])
        # ImageReader makes ReportLab name this XObject by its bytes rather than
        # the absolute checkout path (which would break reproducible builds).
        c.drawImage(ImageReader(str(image)), -12, top - 535, width=d.cw + 24,
                    height=(d.cw + 24) * 1828 / 2836, mask='auto')
        c.setFont('Guide', 9)
        c.drawString(0, top - 558, cover['caption'])
        c.setStrokeColor(colors.HexColor('#42606c'))
        c.line(0, 110, d.cw, 110)
        c.setFillColor(colors.white)
        c.setFont('Guide-Bold', 11)
        c.drawString(0, 84, cover['strapline'])
        c.setFillColor(colors.HexColor('#b7d0d9'))
        c.setFont('Guide', 10)
        c.drawString(0, 63, cover['description'])
        c.setFont('Guide', 9)
        c.drawString(0, 15, 'tagcast.app')
        c.drawRightString(d.cw, 15, cover['date'])


def build(root, output):
    output.mkdir(parents=True, exist_ok=True)
    runtime = runtime_metadata(root)
    design = Design(root, output)
    destinations = {}
    for _ in range(5):
        stream = io.BytesIO()
        doc = GuideDoc(stream, design)
        source_epoch = int(datetime.fromisoformat(design.edition['document_date'])
                           .replace(tzinfo=timezone.utc).timestamp())
        doc.build(design.story(destinations), canvasmaker=functools.partial(
            DeterministicCanvas, source_epoch=source_epoch, invariant=1,
            pdfVersion=(1, 4), lang='en'))
        if doc.seen == destinations:
            break
        destinations = doc.seen
    else:
        raise ValueError('Contents pagination did not converge')
    name = design.edition['filename']
    pdf = output / name
    pdf.write_bytes(stream.getvalue())
    manifest = dict(edition=design.edition, pages=doc.page, bookmarks=doc.seen,
                    image_uses=design.image_uses, inputs=input_inventory(root),
                    runtime=runtime,
                    pdf=dict(file=name, bytes=pdf.stat().st_size, sha256=sha256(pdf)))
    (output / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    (output / (name + '.sha256')).write_text(f'{sha256(pdf)}  {name}\n')
    return pdf, manifest
