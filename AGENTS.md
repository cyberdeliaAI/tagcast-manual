# Tagcast Manual

- Communicate with the maintainer in Dutch; keep source and documentation in English.
- The Tagcast Wiki is canonical. This repository owns PDF editions and publishing tools.
- Never modify the application repository or publish to the Wiki as part of a build.
- Preserve the 1.7.0 reference text, chapter order, captions and historical screenshot labels.
- Do not execute legacy generators in normal builds. They are archival migration evidence.
- Runtime builds must use only checked-in, hash-verified inputs and no network.
- Treat font changes, visual baseline changes and editorial changes as reviewable changes.
- Run `uv run --frozen python -m unittest discover -s tests -v` and `uv run --frozen ruff check src tools tests`.
- Run `uv run --frozen tagcast-manual verify` before accepting renderer changes.
- Publication is a separate explicitly approved operation. There is no automatic Wiki push.
