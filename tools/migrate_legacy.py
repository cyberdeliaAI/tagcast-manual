"""One-time, local migration of the reviewed legacy sources (never used by builds).

Only the content-construction section is executed, against recording helpers. No
legacy PDF rendering, image writes, font loading or absolute source paths run.
"""

import argparse
import ast
import hashlib
import html
import json
import re
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def markdown(text):
    text = re.sub(r'<link href="([^"]+)"[^>]*>(.*?)</link>', r'[\2](\1)', text)
    text = re.sub(r'<font name="Guide-Bold">(.*?)</font>', r'**\1**', text)
    text = text.replace('<b>', '**').replace('</b>', '**')
    text = text.replace('<i>', '*').replace('</i>', '*').replace('<br/>', '  \n')
    return html.unescape(text).replace('\\', '\\\\').replace('|', '\\|')


class RecordedTable(dict):
    def __init__(self, rows, colWidths=None, **kwargs):
        super().__init__(type='layout', rows=rows, widths=colWidths)

    def setStyle(self, style):
        self['style'] = style


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('app', type=Path)
    parser.add_argument('--overwrite-migrated-content', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if list((root / 'content/editions/1.7.0/en/chapters').glob('*.md')) and not args.overwrite_migrated_content:
        parser.error('Chapters exist; explicit --overwrite-migrated-content is required')
    legacy = root / 'legacy/1.7.0'
    source = (legacy / 'build_manual.py').read_text()
    pages = []
    figures = {}
    assets = {}
    counter = 0

    def p(text, kind='body'):
        return {'type': 'text', 'text': text, 'kind': kind}

    def page(group, title, lead, slug=None):
        blocks = []
        pages.append(dict(group=group, title=title, lead=lead, slug=slug, blocks=blocks))
        return blocks

    def paras(blocks, *texts):
        kind = 'small' if texts and texts[-1] == 'small' else 'body'
        if kind == 'small':
            texts = texts[:-1]
        blocks.extend(p(text, kind) for text in texts)

    def figure(rel, caption, maxh=285, crop=None, width=499.276):
        nonlocal counter
        rel, caption, crop = ns['resolve_figure'](rel, caption, crop)
        path = args.app / 'docs/screenshots' / rel
        sha = digest(path)
        asset_id = 'shot-' + sha[:16]
        assets[asset_id] = dict(path='assets/screenshots/' + rel, sha256=sha,
                               source_path='docs/screenshots/' + rel)
        counter += 1
        key = f'figure-{counter:03d}'
        figures[key] = dict(asset=asset_id, max_height=maxh, width=width, crop=crop)
        return [dict(type='figure', id=key, caption=caption)]

    ns = dict(Path=Path, TMP=Path('legacy-placeholder'), CW=499.276, p=p, page=page,
              pages=pages, paras=paras, Table=RecordedTable, TableStyle=lambda x: x,
              figure=figure, table=lambda rows, widths, headers=True:
              dict(type='table', rows=rows, widths=widths, headers=headers),
              h=lambda b, t: b.append(p(t, 'h2')),
              steps=lambda b, items: b.extend(p(f'<b>{n}.</b>  {t}') for n, t in enumerate(items, 1)),
              note=lambda title, text: [dict(type='callout', title=title, text=text)])
    ns['fig'] = lambda blocks, *a, **kw: blocks.extend(figure(*a, **kw))
    tree = ast.parse(source)
    setup = [node for node in tree.body if
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in
              {'CURRENT', 'INTERFACE', 'FINAL', 'FIGURES'} for t in node.targets)) or
             (isinstance(node, ast.FunctionDef) and node.name == 'resolve_figure')]
    exec(compile(ast.Module(body=setup, type_ignores=[]), '<legacy-resolution>', 'exec'), ns)
    start = source.index("b=page('GET STARTED'")
    end = source.index("exec((TMP/'current_topics.py')")
    exec(compile(source[start:end], '<legacy-content>', 'exec'), ns)
    exec(compile((legacy / 'current_topics.py').read_text(), '<legacy-revisions>', 'exec'), ns)

    # Discard images used only in chapters replaced by current_topics.py.
    used = {}

    def emit(blocks):
        out = []
        for block in blocks:
            kind = block['type']
            if kind == 'text':
                text = markdown(block['text'])
                if block['kind'] == 'h2':
                    out.append('## ' + text)
                elif block['kind'] == 'small':
                    out.append('::: small\n' + text + '\n:::')
                else:
                    out.append(text)
            elif kind == 'figure':
                key = block['id']
                used[key] = figures[key]
                out.append('::: figure ' + key + '\n' + markdown(block['caption']) + '\n:::')
            elif kind == 'callout':
                out.append('::: callout\n' + markdown(block['title']) + '\n\n' + markdown(block['text']) + '\n:::')
            elif kind == 'table':
                options = json.dumps(dict(widths=block['widths'], headers=block['headers']))
                rows = ['| ' + ' | '.join(markdown(str(c)) for c in row) + ' |' for row in block['rows']]
                rows.insert(1, '| ' + ' | '.join('---' for _ in block['widths']) + ' |')
                out.append('::: table ' + options + '\n' + '\n'.join(rows) + '\n:::')
            elif kind == 'layout':
                if len(block['rows']) == 1:
                    left, right = block['rows'][0]
                    out.append('::: columns\n' + emit(left) + '\n::: column\n' + emit(right) + '\n:::')
                else:
                    cells = [emit(cell) for row in block['rows'] for cell in row]
                    out.append('::: gallery\n' + '\n::: item\n'.join(cells) + '\n:::')
            else:
                raise ValueError(kind)
        return '\n\n'.join(out)

    chapters = []
    for index, pg in enumerate(pages):
        slug = re.sub(r'[^a-z0-9]+', '-', pg['title'].lower()).strip('-')
        name = f'{index + 1:02d}-{slug}.md'
        meta = dict(id=slug, group=pg['group'], title=pg['title'], lead=pg['lead'], wiki=pg['slug'])
        front = '\n'.join(f'{k} = {json.dumps(v, ensure_ascii=False)}' for k, v in meta.items())
        body = emit(pg['blocks'])
        (root / 'content/editions/1.7.0/en/chapters' / name).write_text('+++\n' + front + '\n+++\n\n' + body + '\n')
        chapters.append('chapters/' + name)
    assets = {v['asset']: assets[v['asset']] for v in used.values()}
    (root / 'manifests/figures.json').write_text(json.dumps(used, indent=2) + '\n')
    (root / 'manifests/screenshots.json').write_text(json.dumps(assets, indent=2) + '\n')
    (root / 'content/editions/1.7.0/en/chapters.json').write_text(json.dumps(chapters, indent=2) + '\n')
    print(f'Migrated {len(pages)} chapters, {len(used)} figures, {len(assets)} originals')


if __name__ == '__main__':
    main()
