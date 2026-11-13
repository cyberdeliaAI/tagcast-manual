"""Local builds only: no publication or account credentials."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .provenance import input_inventory, read_json, sha256
from .render import build
from .validate import validate


def verify(root, output):
    output.mkdir(parents=True, exist_ok=True)
    inventory = input_inventory(root)
    results = []
    with tempfile.TemporaryDirectory(prefix='tagcast-manual-verify-') as temporary:
        for index in range(2):
            checkout = Path(temporary) / f'independent-checkout-{index}'
            checkout.mkdir()
            for name in inventory:
                target = checkout / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / name, target)
            environment = dict(os.environ, PYTHONPATH=str(checkout / 'src'),
                               PYTHONHASHSEED=str(index + 1),
                               TZ='Pacific/Honolulu' if index else 'Europe/Amsterdam',
                               SOURCE_DATE_EPOCH=str(12345 + index))
            # An attempted network request is a build failure, including in dependencies.
            code = ('import sys\n'
                    'def deny_network(event, args):\n'
                    '    if event.startswith("socket."):\n'
                    '        raise RuntimeError("Network forbidden during build")\n'
                    'sys.addaudithook(deny_network)\n'
                    'from tagcast_manual.cli import main\nmain()\n')
            process = subprocess.run([sys.executable, '-c', code, '--root', str(checkout),
                                      'build', '--output', str(checkout / 'result')], cwd=checkout,
                                     env=environment, capture_output=True, text=True)
            if process.returncode:
                raise ValueError(f'Clean build failed:\n{process.stderr}')
            manifest = read_json(checkout / 'result/source-manifest.json')
            results.append(dict(pdf=manifest['pdf']['sha256'],
                                manifest=sha256(checkout / 'result/source-manifest.json')))
            if index == 0:
                for path in (checkout / 'result').iterdir():
                    shutil.copyfile(path, output / path.name)
    if results[0] != results[1]:
        raise ValueError(f'Clean builds differ: {results}')
    edition = read_json(root / 'content/editions/1.7.0/en/edition.json')
    report = validate(root, output / edition['filename'], output)
    result = dict(independent_builds=results, network_disabled=True,
                  changed_environment=['working directory', 'PYTHONHASHSEED', 'TZ', 'SOURCE_DATE_EPOCH'],
                  validation=report)
    (output / 'reproducibility.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd(), help='Manual repository checkout')
    subparsers = parser.add_subparsers(dest='command', required=True)
    for command in ['build', 'validate', 'verify']:
        sub = subparsers.add_parser(command)
        sub.add_argument('--output', type=Path, default=Path('output/pdf'))
        if command == 'validate':
            sub.add_argument('pdf', type=Path)
    args = parser.parse_args()
    root, output = args.root.resolve(), args.output.resolve()
    try:
        if args.command == 'build':
            pdf, manifest = build(root, output)
            result = dict(pdf=str(pdf), pages=manifest['pages'], sha256=manifest['pdf']['sha256'])
        elif args.command == 'validate':
            result = validate(root, args.pdf.resolve(), output)
        else:
            result = verify(root, output)
    except (ValueError, KeyError, FileNotFoundError) as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps(result, indent=2))
