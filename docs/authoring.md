# Authoring PDF editions

The Wiki remains the canonical explanation of Tagcast. Markdown here is a
versioned, PDF-specific editorial snapshot. Correct functional documentation in
the Wiki through its own review process before incorporating it in a later PDF.
Do not use a newer Wiki HEAD as the source for an older application release.

## Markdown contract

Each chapter begins with TOML front matter between `+++` lines. It records a
stable ID, display group, title, lead and canonical Wiki topic/fragment. Ordering
is explicit in `chapters.json`. IDs drive bookmarks and contents destinations;
renumbering a file does not change its identity.

Supported inline content includes text, strong/emphasis, links, inline code
(retaining the original body typeface) and Markdown hard line breaks. Level-two
headings appear within a chapter. The migrated numbered steps retain their
original bold number paragraphs and spacing. Raw HTML is displayed literally.
Unsupported block types fail instead of disappearing.

The following block directives close with a line containing `:::`:

- `::: small`: supporting prose.
- `::: callout`: title, a blank line, then explanatory prose.
- `::: figure figure-NNN`: caption; image identity and geometry come from manifests.
- `::: table {"widths":[0.4,0.6],"headers":true}`: a Markdown pipe table.
  Widths are relative column proportions, not absolute page coordinates.
- `::: columns`: two cells separated by `::: column`, for the narrow-window example.
- `::: gallery`: four cells separated by `::: item`, for visualization examples.

Nested figures in columns/galleries retain ordinary figure IDs and captions.
Unknown directives, malformed front matter, invalid proportions, missing assets
and changed original hashes stop the build.

## Images and source records

Keep image originals unchanged. `screenshots.json` records the original app
repository path, exact commit, public source URL and SHA-256. Where available it
also points to a verbatim inventory under `assets/attribution/`; the inventory
records capture dates, original filenames, dimensions, visible states and credits.
Unknown provenance is not inferred from a screenshot's contents.

`figures.json` records crop coordinates, source asset ID and bounded layout sizes.
Captions live with the chapter. Crops and JPEG conversion happen only in memory;
no original is overwritten. Historical/version labels and draft/review/running/
confirmed distinctions are editorial content and must remain accurate.

## Versioning

`edition.json` distinguishes the application version, document revision and
historical edition date. It pins the released app commit separately from the
later documentation/image commit and Wiki text baseline. Start a later edition
from an approved snapshot and keep the earlier one intact.

The renderer selects an edition explicitly with `--edition VERSION`; omitted
means the fixed 1.7.0 reference. Supply a separate output directory for each later
edition so its manifest/reports do not replace earlier build records:

```sh
uv run --frozen tagcast-manual build --edition 1.9.0 --output output/pdf/1.9.0
uv run --frozen tagcast-manual validate --edition 1.9.0 \
  output/pdf/1.9.0/Tagcast-1.9.0-User-Manual.pdf --output output/pdf/1.9.0
uv run --frozen tagcast-manual verify --edition 1.9.0 --output output/pdf/1.9.0
```

Later editions use `manifests/VERSION/screenshots.json` and `figures.json`, with
the shared, unchanged font/legacy manifests. Keep copied originals byte for byte,
record the released source commit separately from the unknown capture runtime,
and label example versions and running/checking states accurately.

Validation checks source text, navigation, images, bounds and orphaned pages.
After inspecting every rendered page, capture the initial edition baseline with
`tools/capture_edition_reference.py`. It refuses to replace an existing baseline
and cannot select 1.7.0. Geometry/image and pixel regressions then fail validation.
A candidate baseline records the inspected layout, not maintainer publication
approval. Content changes require editorial review and an explicit baseline
review; builds and CI never rewrite content or refresh visual references.
