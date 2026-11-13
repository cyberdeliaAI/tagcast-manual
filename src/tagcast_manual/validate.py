"""PDF integrity, historical layout comparison and visual regression checks."""

import gzip
import hashlib
import json
import re

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageChops
from pypdf import PdfReader

from .provenance import load_edition, read_json, sha256


def pdf_snapshot(pdf):
    reader = PdfReader(pdf, strict=True)
    pages = []
    with pdfplumber.open(pdf) as document:
        for page in document.pages:
            pages.append(dict(
                text=page.extract_text(),
                chars=[[c['text'], *[round(c[k], 4) for k in ('x0', 'top', 'x1', 'bottom')]]
                       for c in page.chars],
                images=[dict(bounds=[round(im[k], 4) for k in ('x0', 'top', 'x1', 'bottom')],
                             size=list(im['srcsize']),
                             sha256=hashlib.sha256(im['stream'].get_data()).hexdigest())
                        for im in page.images]))
    outlines = [dict(title=d.title, page=reader.get_destination_page_number(d) + 1)
                for d in reader.outline]
    links = []
    for index, page in enumerate(reader.pages, 1):
        for ref in page.get('/Annots', []):
            annotation = ref.get_object()
            if annotation.get('/Subtype') != '/Link':
                continue
            if '/Dest' in annotation:
                destination = annotation['/Dest']
                number = reader._get_page_number_by_indirect(destination[0])
                if number is None:
                    raise ValueError('Invalid internal link destination')
                links.append(dict(source=index, destination=number + 1))
            else:
                action = annotation.get('/A', {})
                if action.get('/S') != '/URI':
                    raise ValueError('Unexpected PDF link action')
                links.append(dict(source=index, uri=str(action['/URI'])))
    return dict(pages=pages, outlines=outlines, links=links)


def render_pages(pdf, output):
    output.mkdir(parents=True, exist_ok=True)
    for previous in output.glob('page-*.png'):
        previous.unlink()
    document = pdfium.PdfDocument(str(pdf))
    try:
        for index in range(len(document)):
            page = document[index]
            bitmap = page.render(scale=96 / 72)
            try:
                image = bitmap.to_pil().convert('RGB')
                image.save(output / f'page-{index + 1:02d}.png', optimize=False)
            finally:
                bitmap.close()
                page.close()
    finally:
        document.close()


def visual_compare(actual, expected, diff_dir):
    failures = []
    for baseline in sorted(expected.glob('page-*.png')):
        path = actual / baseline.name
        if not path.is_file():
            failures.append(baseline.name)
            continue
        with Image.open(path) as im, Image.open(baseline) as ref:
            if im.size != ref.size:
                failures.append(baseline.name)
                continue
            delta = ImageChops.difference(im.convert('RGB'), ref.convert('RGB'))
            if delta.getbbox():
                diff_dir.mkdir(parents=True, exist_ok=True)
                delta.save(diff_dir / baseline.name)
                failures.append(baseline.name)
    extra = {p.name for p in actual.glob('page-*.png')} - {p.name for p in expected.glob('page-*.png')}
    return failures + sorted(extra)


def validate(root, pdf, output, visual=True, edition='1.7.0'):
    if edition != '1.7.0':
        return validate_edition(root, pdf, output, visual, edition)
    reference_dir = root / 'tests/reference/1.7.0'
    reference = json.loads(gzip.decompress((reference_dir / 'original-layout.json.gz').read_bytes()))
    snapshot = pdf_snapshot(pdf)
    errors = []
    if len(snapshot['pages']) != 52:
        errors.append('The 1.7.0 edition must have 52 pages')
    if snapshot['outlines'] != reference['outlines']:
        errors.append('Chapter titles or bookmark destinations changed')
    if snapshot['links'] != reference['links']:
        errors.append('Internal or external link targets changed')
    max_delta = 0
    for index, (actual, expected) in enumerate(zip(snapshot['pages'], reference['pages']), 1):
        if actual['text'] != expected['text']:
            errors.append(f'Page {index}: extracted text changed')
        if len(actual['chars']) != len(expected['chars']):
            errors.append(f'Page {index}: character count changed')
        else:
            for a, e in zip(actual['chars'], expected['chars']):
                if a[0] != e[0]:
                    errors.append(f'Page {index}: drawing text changed')
                    break
                delta = max(abs(x - y) for x, y in zip(a[1:], e[1:]))
                max_delta = max(max_delta, delta)
                if delta > .002:
                    errors.append(f'Page {index}: text moved by {delta:.4f} pt')
                    break
        if actual['images'] != expected['images']:
            errors.append(f'Page {index}: screenshot bytes, crops or positions changed')
        for c in actual['chars']:
            if c[1] < -.5 or c[2] < -.5 or c[3] > 595.776 or c[4] > 842.39:
                errors.append(f'Page {index}: text outside page bounds')
                break
        if '\ufffd' in actual['text'] or '\x00' in actual['text']:
            errors.append(f'Page {index}: invalid text encoding')
    reader = PdfReader(pdf, strict=True)
    edition = read_json(root / 'content/editions/1.7.0/en/edition.json')
    if reader.metadata.title != edition['title'] or reader.metadata.author != 'Tagcast':
        errors.append('PDF title or author metadata changed')
    if reader.is_encrypted or '/OpenAction' in reader.trailer['/Root']:
        errors.append('Unexpected encryption or automatic action')
    if reader.trailer['/Root'].get('/Lang') != 'en':
        errors.append('PDF language is missing')
    if visual:
        actual_dir = output / 'rendered'
        render_pages(pdf, actual_dir)
        failures = visual_compare(actual_dir, reference_dir / 'rendered', output / 'visual-diffs')
        errors.extend(f'Visual regression: {name}' for name in failures)
    report = dict(pages=len(snapshot['pages']), bookmarks=len(snapshot['outlines']),
                  internal_links=sum('destination' in link for link in snapshot['links']),
                  external_links=sum('uri' in link for link in snapshot['links']),
                  max_text_position_delta_pt=round(max_delta, 4),
                  pdf_sha256=sha256(pdf), visual_checked=visual, errors=errors)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    if errors:
        raise ValueError('\n'.join(errors))
    return report


def validate_edition(root, pdf, output, visual, edition):
    """Check a new edition against its own sources, never against the old manual."""
    from reportlab.platypus import Paragraph, Table

    from .render import Design

    metadata = load_edition(root, edition)
    design = Design(root, output, edition)
    snapshot = pdf_snapshot(pdf)
    reader = PdfReader(pdf, strict=True)
    errors = []
    def normalise(text):
        return re.sub(r'\s+', '', text)
    drawn = normalise(''.join(c[0] for page in snapshot['pages'] for c in page['chars']))

    def check_flowables(items):
        for item in items:
            if isinstance(item, Paragraph):
                if normalise(item.getPlainText()) not in drawn:
                    errors.append(f'Source paragraph missing: {item.getPlainText()[:100]}')
            elif isinstance(item, Table):
                for row in item._cellvalues:
                    for cell in row:
                        check_flowables(cell if isinstance(cell, (list, tuple)) else [cell])

    expected_titles = ['Contents', *[chapter['title'] for chapter in design.chapters]]
    if [entry['title'] for entry in snapshot['outlines']] != expected_titles:
        errors.append('Chapter bookmarks differ from the edition order')
    pages = [entry['page'] for entry in snapshot['outlines']]
    if pages != sorted(set(pages)) or any(p < 2 or p > len(reader.pages) for p in pages):
        errors.append('Invalid or repeated chapter destination')
    internal = [link for link in snapshot['links'] if 'destination' in link]
    expected_destinations = sorted(p for page in pages[1:] for p in (page, page))
    if sorted(link['destination'] for link in internal) != expected_destinations:
        errors.append('Contents links do not cover every chapter twice')
    for chapter in design.chapters:
        check_flowables([design.paragraph(chapter['title'], 'title'),
                         design.paragraph(chapter['lead'], 'lead'),
                         *design.blocks(chapter['blocks'])])
        if chapter['wiki']:
            uri = 'https://github.com/cyberdeliaAI/tagcast/wiki/' + chapter['wiki']
            if not any(link.get('uri') == uri for link in snapshot['links']):
                errors.append(f'Missing canonical Wiki link: {uri}')
    expected_images = len(design.image_uses) + 1
    actual_images = sum(len(page['images']) for page in snapshot['pages'])
    if actual_images != expected_images:
        errors.append(f'Expected {expected_images} images, found {actual_images}')
    for index, (page, raw) in enumerate(zip(snapshot['pages'], reader.pages), 1):
        if abs(float(raw.mediabox.width) - design.width) > .01 or abs(
                float(raw.mediabox.height) - design.height) > .01:
            errors.append(f'Page {index}: unexpected page size')
        if not page['text'] or len(page['chars']) < 40:
            errors.append(f'Page {index}: empty or near-empty page')
        body = ''.join(c[0] for c in page['chars'] if 69 <= c[2] < design.height - 49)
        if index > 1 and not page['images'] and len(normalise(body)) < 100:
            errors.append(f'Page {index}: orphaned content or Wiki footer')
        if '\ufffd' in page['text'] or '\x00' in page['text']:
            errors.append(f'Page {index}: invalid text encoding')
        for char in page['chars']:
            if char[1] < -.5 or char[2] < -.5 or char[3] > design.width + .5 or char[4] > design.height + .5:
                errors.append(f'Page {index}: text outside page bounds')
                break
        for image in page['images']:
            x0, top, x1, bottom = image['bounds']
            if x0 < -.5 or top < -.5 or x1 > design.width + .5 or bottom > design.height + .5:
                errors.append(f'Page {index}: image outside page bounds')
        if index > 1 and ('VERSION ' + edition not in page['text'] or
                          not page['text'].rstrip().endswith(f'{index:02d}')):
            errors.append(f'Page {index}: version header or page number missing')
    if reader.metadata.title != metadata['title'] or reader.metadata.author != 'Tagcast':
        errors.append('Incorrect edition metadata')
    if reader.is_encrypted or '/OpenAction' in reader.trailer['/Root']:
        errors.append('Unexpected encryption or automatic action')
    if reader.trailer['/Root'].get('/Lang') != metadata['language']:
        errors.append('Incorrect PDF language')
    reference_dir = root / 'tests/reference' / edition
    baseline = reference_dir / 'layout.json.gz'
    if baseline.is_file():
        reference = json.loads(gzip.decompress(baseline.read_bytes()))
        if snapshot['outlines'] != reference['outlines'] or snapshot['links'] != reference['links']:
            errors.append('Edition navigation regression')
        if len(snapshot['pages']) != len(reference['pages']):
            errors.append('Edition page-count regression')
        for index, (actual, expected) in enumerate(zip(snapshot['pages'], reference['pages']), 1):
            if actual['text'] != expected['text'] or actual['images'] != expected['images']:
                errors.append(f'Page {index}: edition text/image regression')
            if len(actual['chars']) != len(expected['chars']) or any(
                    a[0] != e[0] or max(abs(x-y) for x, y in zip(a[1:], e[1:])) > .002
                    for a, e in zip(actual['chars'], expected['chars'])):
                errors.append(f'Page {index}: edition layout regression')
    if visual:
        render_pages(pdf, output / 'rendered')
        if baseline.is_file():
            failures = visual_compare(output / 'rendered', reference_dir / 'rendered',
                                      output / 'visual-diffs')
            errors.extend(f'Visual regression: {name}' for name in failures)
    report = dict(edition=edition, pages=len(reader.pages), bookmarks=len(pages),
                  internal_links=len(internal), external_links=len(snapshot['links']) - len(internal),
                  image_placements=actual_images, source_content_checked=True,
                  pdf_sha256=sha256(pdf), pages_rendered=visual,
                  visual_baseline=str(baseline.relative_to(root)) if baseline.is_file()
                  else 'not yet captured', errors=errors)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    if errors:
        raise ValueError('\n'.join(errors))
    return report
