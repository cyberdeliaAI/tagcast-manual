"""Local-only source verification and deterministic input inventories."""

import hashlib
import json
import platform
import re
import tomllib
from importlib.metadata import version
from pathlib import Path


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def local_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise ValueError(f'Path escapes the repository: {relative}')
    if not path.is_file():
        raise ValueError(f'Missing input: {relative}')
    return path


def edition_directory(root, edition='1.7.0'):
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', edition):
        raise ValueError('Choose an edition using a stable version, such as 1.9.0')
    relative = f'content/editions/{edition}/en/edition.json'
    return local_path(root, relative).parent


def load_edition(root, edition='1.7.0'):
    data = read_json(edition_directory(root, edition) / 'edition.json')
    if data['app_version'] != edition:
        raise ValueError('Edition identity does not match its directory')
    filename = data['filename']
    if Path(filename).name != filename or not filename.endswith('.pdf'):
        raise ValueError('Edition output must be a PDF filename without a directory')
    return data


def verify_assets(root, edition='1.7.0'):
    if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', edition):
        raise ValueError('Invalid edition version')
    manifests = root / 'manifests' if edition == '1.7.0' else root / 'manifests' / edition
    screenshots = read_json(manifests / 'screenshots.json')
    fonts = read_json(root / 'manifests/fonts.json')['fonts']
    legacy = read_json(root / 'manifests/legacy.json')
    for item in [*screenshots.values(), *fonts.values(), *legacy]:
        path = local_path(root, item['path'])
        if sha256(path) != item['sha256']:
            raise ValueError(f'Input hash mismatch: {item["path"]}')
    figures = read_json(manifests / 'figures.json')
    for key, figure in figures.items():
        if figure['asset'] not in screenshots:
            raise ValueError(f'Unknown screenshot in {key}')
        if figure['width'] <= 0 or figure['max_height'] <= 0:
            raise ValueError(f'Invalid figure size in {key}')
        crop = figure['crop']
        if crop is not None and (len(crop) != 4 or not 0 <= crop[0] < crop[2] <= 1
                                 or not 0 <= crop[1] < crop[3] <= 1):
            raise ValueError(f'Invalid crop in {key}')
    return screenshots, fonts, figures


def input_inventory(root):
    names = ['pyproject.toml', 'uv.lock', '.python-version', 'LICENSE']
    for directory in ['src', 'templates', 'content', 'manifests', 'assets', 'legacy']:
        names.extend(p.relative_to(root).as_posix() for p in (root / directory).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    return {name: sha256(local_path(root, name)) for name in sorted(names)}


def runtime_metadata(root):
    project = tomllib.loads((root / 'pyproject.toml').read_text())
    packages = {}
    for requirement in project['project']['dependencies']:
        name, expected = requirement.split('==')
        installed = version(name)
        if installed != expected:
            raise ValueError(f'Use the locked runtime: {name} requires {expected}, found {installed}')
        packages[name] = installed
    expected_python = (root / '.python-version').read_text().strip()
    if platform.python_version() != expected_python:
        raise ValueError(f'Use Python {expected_python}, found {platform.python_version()}')
    return dict(python=expected_python, packages=packages)
