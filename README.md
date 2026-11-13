# Tagcast Manual

Reproducible illustrated PDF editions of the [canonical Tagcast Wiki](https://github.com/cyberdeliaAI/tagcast/wiki).

This repository owns PDF editorial snapshots, templates, asset provenance and
build validation. It has no dependency on the Tagcast application checkout,
application runtime, account credentials, packaging or release gates. Builds
never publish to the Wiki or create a GitHub release.

The first reference edition preserves the existing **Tagcast 1.7.0** manual:
52 A4 pages, 50 topics, 51 bookmarks, 100 internal links, 110 external links and
44 figure placements from 43 original screenshots, plus the cover placement.

## Build

Install [uv](https://docs.astral.sh/uv/), clone this repository, then run from its root:

```sh
uv sync --frozen --python 3.12.14
uv run --frozen tagcast-manual build
uv run --frozen tagcast-manual validate output/pdf/Tagcast-1.7.0-User-Manual.pdf
```

Dependency installation needs internet access. PDF rendering and validation use
only local inputs. No application checkout, system fonts or external images are
needed. The Python patch version, dependency lock, fonts, image originals and
template are recorded in the repository.

`output/pdf/` contains the PDF, SHA-256 companion and deterministic source
manifest. Generated files are not committed. The historical published PDF stays
in the Wiki; it is not duplicated as another download here.

## Verify reproducibility

```sh
uv run --frozen python -m unittest discover -s tests -v
uv run --frozen ruff check src tools tests
uv run --frozen tagcast-manual verify
```

`verify` copies the required inputs into two independent temporary checkouts,
builds in fresh Python processes with different working directories, hash seeds,
timezones and ambient timestamps, and blocks Python socket operations. Both PDF
bytes and deterministic source manifests must match. It then checks the
historical text/layout and every page against the reviewed visual baseline.
Reports, rendered pages and any visual differences are saved under `output/pdf/`.

CI runs these checks independently on Ubuntu and macOS. Exact bytes are required
within each locked environment. Cross-platform byte equality is reported only
when observed; the lock does not pretend to freeze the host operating system or
its compression libraries. The checked-in visual baseline must pass on each
supported CI environment.

## Content and design

- `content/editions/1.7.0/en/`: the effective, reviewed English text in Markdown,
  chapter order, edition metadata and cover copy.
- `templates/tagcast/`: typography, colours and layout values.
- `assets/`: selected unchanged screenshots, bundled fonts and attribution.
- `manifests/`: original hashes, source revisions, figure crops and sizing.
- `legacy/1.7.0/`: the recovered original sources and publication records,
  preserved byte for byte and never executed by normal builds.
- `tests/reference/1.7.0/`: original text/geometry/image reference and reviewed
  new-renderer PNGs. Updating them is an explicit editorial action.

See [authoring](docs/authoring.md), [migration evidence](docs/reference-edition.md)
and [publishing boundaries](docs/publishing.md).

## Typography and preservation

The original used macOS Arial. This edition bundles unmodified **Liberation Sans**
under its SIL Open Font License. It retains the original sizes, line spacing,
colours and positions. A measured advance-width adjustment for the bold middle
dot retains three original lines without altering the font file. Glyph outlines
can differ; no claim of pixel identity with Arial is made.

All extracted page text, links, screenshots and positions are checked against the
published original. Screenshot stream bytes, crops and placements must match;
character coordinates have a 0.002 pt numerical tolerance. The PDF's metadata
identifies the new renderer and English language. Its timestamps are fixed to
the edition date at midnight UTC, so its checksum differs from the old PDF.

## Licences

The publishing code and original project documentation are MIT-licensed; see
[LICENSE](LICENSE). Fonts retain [SIL OFL 1.1](assets/fonts/OFL.txt). Artwork,
photographs, displayed lyrics and provider excerpts retain their existing rights
and attribution; they are not relicensed as MIT. See
[asset attribution](assets/attribution/README.md).
