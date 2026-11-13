"""Explicitly capture a reviewed original-layout and candidate visual baseline.

This is an editorial operation, not part of build/CI. Existing baselines are
never replaced unless --replace-reviewed-baseline is supplied explicitly.
"""

import argparse
import gzip
import json
from pathlib import Path

from tagcast_manual.provenance import sha256
from tagcast_manual.validate import pdf_snapshot, render_pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--replace-reviewed-baseline', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    directory = root / 'tests/reference/1.7.0'
    snapshot = directory / 'original-layout.json.gz'
    if snapshot.exists() and not args.replace_reviewed_baseline:
        parser.error('Baseline exists; review changes before explicitly replacing it')
    expected = '14cd59bcfa8249d1a20c6ff220525b1e412e61c67af35c03eefe47ff7be707fb'
    if sha256(args.original) != expected:
        parser.error('Original must be the published, unchanged 1.7.0 PDF')
    directory.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(gzip.compress(json.dumps(pdf_snapshot(args.original)).encode(), mtime=0))
    render_pages(args.candidate, directory / 'rendered')
    report = dict(original_pdf_sha256=expected, candidate_pdf_sha256=sha256(args.candidate),
                  render_dpi=96, font_substitution='Bundled Liberation Sans replaces system Arial',
                  layout_tolerance_pt=0.002,
                  policy='Exact text, links, screenshot bytes and placement; explicit font glyph substitution')
    (directory / 'reference.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
