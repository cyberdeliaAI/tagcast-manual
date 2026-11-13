+++
id = "keep-import-progress-and-review-order"
group = "ORGANISE"
title = "Keep import progress and review order"
lead = "An unfinished import is a draft, not a playlist or a download."
wiki = "Importing-playlists#pause-and-resume-csv-imports"
+++

::: figure figure-009
1.7.0: compare recording/edition differences before a manual match.
:::

Unresolved does not necessarily mean the song is missing: another edition, a different album, ambiguous duplicates or duration data can prevent an automatic match. Mapping fewer optional fields can be appropriate, but check the actual recording/version.

You may create a playlist from the matched subset. The final review states which unresolved records will be omitted. **Export unresolved records as CSV** preserves the remaining rows for later work. CSV order is retained; a rank/date column is not used to sort.

## Pause explicitly before closing

**Pause import** saves a checkpoint for the current account on this computer. **Paused imports > Refresh library & resume** checks current library matches while keeping valid manual choices. Review again before creating a playlist. Ordinary unpaused drafts are temporary and expire after one hour.

Up to ten paused imports per account can be stored. A failed or uncertain playlist creation is not automatically repeated: inspect Playlists first. Removing a paused checkpoint affects only that saved local draft.
