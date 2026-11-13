# The 1.7.0 reference migration

## Recovered inputs

- Published original: `Tagcast-1.7.0-User-Manual.pdf`, 20,986,722 bytes.
- Original SHA-256: `14cd59bcfa8249d1a20c6ff220525b1e412e61c67af35c03eefe47ff7be707fb`.
- Published app: `a2493c85639780a9ca2b2a7121db85605b659c92` (`v1.7.0`).
- Documentation/images: `9b47dae9ba917da0bcdfc93b8d6fa52c0c23c900`.
- Wiki text baseline: `14d3e9839bf83cf8029ad8fc0084255ed251e2c8`.
- Wiki publication commit: `29fead0d9f9316f8e817f1e64623464c22e03828`.

The original ReportLab sources were recovered from the maintainer's local
`tmp/pdfs/manual-1.7.0/` directory, not from the released application package.
Their original byte hashes and publication manifests are preserved under
`legacy/` and `manifests/legacy.json`. Absolute paths inside these archival files
are historical evidence; normal builds never resolve or execute them.

## Effective content, not obsolete intermediate copy

The original `current_topics.py` replaces several earlier chapters, adds topics
and sorts the final collection. The one-time migration records that effective
collection. For example, the obsolete base paragraph saying the queue is
temporary is replaced by the final text describing remembered local queues.

`tools/migrate_legacy.py` is an explicit local migration utility. It evaluates
only the reviewed content-construction sections against recording helpers;
legacy PDF rendering, image conversion and font registration are not run. It
requires a historical application asset checkout. It is not used by CI or
normal rendering and refuses to overwrite existing chapters without an option.

## Preservation checks

The compressed original-layout reference was extracted from the checksum-verified
published PDF. It contains text, character coordinates, image stream hashes and
positions, external link targets and bookmark destinations for all 52 pages.
The original PDF is not committed a second time.

The new renderer keeps the recovered ReportLab layout and uses the effective
Markdown content. Contents use an iterative layout pass and actual recorded
destinations, so an overflowing topic cannot silently shift later page numbers.
A regression test deliberately forces an overflow and checks the destinations.

The following are intentional differences from the historical PDF:

- Bundled Liberation Sans glyph outlines replace system Arial. Font files are
  unchanged; the original bold middle-dot advance is recorded in the template.
- Creator and English-language metadata identify this publishing engine.
- Creation/modification times use the fixed edition date in UTC.
- Internal destination/object names use stable IDs and image bytes rather than
  positional topic IDs or absolute local paths.

These differences do not change the extracted text, chapter/page order, image
bytes or link destinations. The old published PDF remains untouched.

## Baseline review

`tools/capture_reference.py` requires the exact historical original hash and a
candidate PDF. Its output is not automatically accepted by CI. The checked-in
candidate renders were reviewed during this migration, including comparison with
the original. To replace an existing baseline, explicitly pass
`--replace-reviewed-baseline` after reviewing the PDF, geometry and difference
images. Do not loosen tolerances to make an unexplained regression pass.

Build reproducibility reports describe the environment actually tested. They
prove equality between fresh builds, not reproduction of the historical Arial
PDF's checksum or universal equality across arbitrary runtimes.
