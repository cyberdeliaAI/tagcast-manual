"""Strict Markdown and a small set of edition layout directives."""

import json
import re
import tomllib
from html import escape
from urllib.parse import urlsplit

from markdown_it import MarkdownIt

MD = MarkdownIt('commonmark', {'html': False}).enable('table')
DIRECTIVES = {'small', 'figure', 'callout', 'table', 'columns', 'gallery'}


def inline(text):
    result = []
    for token in MD.parseInline(text)[0].children or []:
        kind = token.type
        if kind in {'text', 'code_inline'}:
            result.append(escape(token.content))
        elif kind in {'strong_open', 'strong_close', 'em_open', 'em_close'}:
            tag = 'b' if kind.startswith('strong') else 'i'
            result.append(f'<{"/" if kind.endswith("close") else ""}{tag}>')
        elif kind == 'link_open':
            href = token.attrGet('href')
            if urlsplit(href).scheme not in {'https', ''} or href.startswith('//'):
                raise ValueError(f'Unsupported link: {href}')
            result.append(f'<link href="{escape(href, quote=True)}" color="#276b7d">')
        elif kind == 'link_close':
            result.append('</link>')
        elif kind == 'hardbreak':
            result.append('<br/>')
        elif kind == 'softbreak':
            result.append(' ')
        else:
            raise ValueError(f'Unsupported inline Markdown: {kind}')
    return ''.join(result)


def paragraphs(text, style='body'):
    tokens = MD.parse(text)
    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type not in {'paragraph_open', 'heading_open'}:
            raise ValueError(f'Unsupported Markdown block: {token.type}')
        kind = 'h2' if token.type == 'heading_open' else style
        if token.type == 'heading_open' and token.tag != 'h2':
            raise ValueError('Use level-two headings within chapters')
        if i + 2 >= len(tokens) or tokens[i + 1].type != 'inline':
            raise ValueError('Invalid Markdown paragraph')
        result.append(dict(type='text', text=inline(tokens[i + 1].content), kind=kind))
        i += 3
    return result


def table_rows(text):
    tokens = MD.parse(text)
    if not tokens or tokens[0].type != 'table_open' or tokens[-1].type != 'table_close':
        raise ValueError('Expected one Markdown table')
    rows = []
    for token in tokens:
        if token.type == 'tr_open':
            rows.append([])
        elif token.type == 'inline':
            rows[-1].append(inline(token.content))
        elif token.type not in {'table_open', 'table_close', 'thead_open', 'thead_close',
                                'tbody_open', 'tbody_close', 'tr_open', 'tr_close',
                                'th_open', 'th_close', 'td_open', 'td_close'}:
            raise ValueError(f'Unsupported table token: {token.type}')
    if not rows or len({len(row) for row in rows}) != 1:
        raise ValueError('Table rows must have equal widths')
    return rows


def parse_blocks(text):
    lines = text.splitlines()

    def read(index, nested=False):
        blocks = []
        while index < len(lines):
            line = lines[index]
            if line == ':::' or line in {'::: column', '::: item'}:
                if not nested:
                    raise ValueError(f'Unexpected directive boundary: {line}')
                return blocks, index, line
            if not line.startswith(':::'):
                start = index
                while index < len(lines) and not lines[index].startswith(':::'):
                    index += 1
                blocks.extend(paragraphs('\n'.join(lines[start:index])))
                continue
            match = re.fullmatch(r'::: ([a-z]+)(?: (.*))?', line)
            if not match or match[1] not in DIRECTIVES:
                raise ValueError(f'Unknown directive: {line}')
            kind, argument = match[1], match[2]
            index += 1
            if kind in {'columns', 'gallery'}:
                cells = []
                while True:
                    cell, index, boundary = read(index, nested=True)
                    cells.append(cell)
                    index += 1
                    if boundary == ':::':
                        break
                    if boundary != ('::: column' if kind == 'columns' else '::: item'):
                        raise ValueError('Incorrect layout separator')
                if len(cells) != (2 if kind == 'columns' else 4):
                    raise ValueError(f'{kind} has an incorrect number of cells')
                blocks.append(dict(type=kind, cells=cells))
                continue
            start = index
            while index < len(lines) and lines[index] != ':::':
                if lines[index].startswith(':::'):
                    raise ValueError('Nested directive in a leaf block')
                index += 1
            if index == len(lines):
                raise ValueError(f'Unclosed directive: {kind}')
            body = '\n'.join(lines[start:index]).strip()
            index += 1
            if kind == 'small':
                blocks.extend(paragraphs(body, 'small'))
            elif kind == 'figure':
                if not argument or not re.fullmatch(r'figure-\d{3}', argument):
                    raise ValueError('Figure requires a manifest ID')
                blocks.append(dict(type='figure', id=argument, caption=inline(body)))
            elif kind == 'callout':
                title, separator, prose = body.partition('\n\n')
                if not separator:
                    raise ValueError('Callout requires a title and paragraph')
                blocks.append(dict(type='callout', title=inline(title), text=inline(prose)))
            elif kind == 'table':
                options = json.loads(argument or '{}')
                if set(options) != {'widths', 'headers'} or not isinstance(options['headers'], bool):
                    raise ValueError('Table requires widths and a boolean headers option')
                widths = options.get('widths', [])
                rows = table_rows(body)
                if (len(widths) != len(rows[0]) or any(w <= 0 for w in widths)
                        or abs(sum(widths) - 1) > 0.00001):
                    raise ValueError('Table column proportions must be positive and total one')
                blocks.append(dict(type='table', rows=rows, **options))
        if nested:
            raise ValueError('Unclosed layout directive')
        return blocks, index, None

    return read(0)[0]


def load_chapter(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('+++\n'):
        raise ValueError(f'Missing TOML front matter: {path.name}')
    header, separator, body = text[4:].partition('\n+++\n')
    if not separator:
        raise ValueError('Unclosed chapter front matter')
    meta = tomllib.loads(header)
    if set(meta) != {'id', 'group', 'title', 'lead', 'wiki'}:
        raise ValueError('Unexpected chapter metadata')
    if not all(isinstance(value, str) for value in meta.values()):
        raise ValueError('Chapter metadata must contain strings')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['id']):
        raise ValueError('Chapter ID must be a stable lowercase slug')
    return dict(**meta, blocks=parse_blocks(body))
