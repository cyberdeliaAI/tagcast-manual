"""Capture a new edition's visually inspected candidate, without replacing references."""

import argparse
import gzip
import json
from pathlib import Path

from tagcast_manual.provenance import edition_directory, sha256
from tagcast_manual.validate import pdf_snapshot, render_pages, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--edition', required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--visually-reviewed', action='store_true', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    edition_directory(root, args.edition)
    if args.edition == '1.7.0':
        parser.error('The historical reference cannot be changed by this command')
    directory = root / 'tests/reference' / args.edition
    if directory.exists():
        parser.error('Baseline exists; this command never replaces reviewed files')
    validate(root, args.candidate, root / 'output/reference-review' / args.edition,
             visual=False, edition=args.edition)
    directory.mkdir(parents=True)
    snapshot = json.dumps(pdf_snapshot(args.candidate), ensure_ascii=False).encode()
    (directory / 'layout.json.gz').write_bytes(gzip.compress(snapshot, mtime=0))
    render_pages(args.candidate, directory / 'rendered')
    report = dict(edition=args.edition, candidate_pdf_sha256=sha256(args.candidate),
                  render_dpi=96, layout_tolerance_pt=.002,
                  review='All pages visually inspected; candidate layout, not publication approval')
    (directory / 'reference.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
