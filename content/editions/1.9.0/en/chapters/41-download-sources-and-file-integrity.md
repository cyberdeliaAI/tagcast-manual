+++
id = "download-sources-and-file-integrity"
group = "TRANSFER MUSIC"
title = "Download sources and file integrity"
lead = "Choose which bytes you want, and keep the verification record."
wiki = "Downloads#quality-and-embedded-metadata"
+++

::: table {"widths": [0.35, 0.65], "headers": true}
| Source | What is downloaded |
| --- | --- |
| Original via download service | Premium default. For current embedded tags, enable Download Updated Metadata in iBroadcast. The service decides which fields it embeds. |
| Original upload via streaming | Uploaded bytes/tags; later library metadata edits may be absent. This fallback is labelled. |
| Converted streaming MP3 | The selected offered quality; Free accounts use 128 kbps MP3. |
:::

Tagcast creates separate files. It does not retag, adopt or overwrite existing unverified music. Changing source does not replace completed files. Default naming uses artist/album/year and disc-track title, with safe filenames and collision handling.

::: callout
Keep the hidden integrity manifest

Preserve .ibfetch.json beside downloaded music. Unverified or locally modified files are not silently trusted. Explicit checksum checks and eligible streaming partial-resume use this record. Completed files remain after stopping.
:::

::: small
One worker is the default. Extra workers compete with playback for network/disk capacity. Options persist, but transfer selection/progress is session-local. Reselect and review after restart to reuse verified completed files or eligible partials. For individual tracks, playlists and advanced CLI filters, use the linked ibfetch tool. Metadata JSON/CSV export is separate.
:::
