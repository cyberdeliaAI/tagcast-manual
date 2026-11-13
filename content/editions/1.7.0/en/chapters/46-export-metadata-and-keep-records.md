+++
id = "export-metadata-and-keep-records"
group = "YOUR DATA"
title = "Export metadata and keep records"
lead = "A metadata snapshot, Change history and audio downloads serve different purposes."
wiki = "Exporting-library-metadata"
+++

**1.**  Reload the library first if you want a snapshot of recent iBroadcast changes.

**2.**  Open **Settings > Data & exports > Export library metadata**. Choose optional tags, playlists and local favourites where available.

**3.**  Choose **Prepare JSON export** or **Prepare CSV ZIP**. When ready, use its separate **Download** button. Prepared downloads expire after 15 minutes.

**4.**  Use **Export changes** separately to keep this browser's Change history. Save cleanup/duplicate reports from their own workflows.

The metadata export covers the complete **loaded library**, not current search results or unsaved drafts. Native IDs preserve relationships between artists, albums/discs, tracks and credits. CSV ZIP contains linked tables, with optional playlists/folders, tags and local favourites when available. Read its manifest for missing optional data.

::: callout
This is not a restorable music backup

The export excludes audio, image binaries, credentials and provider prose. It has no restore function. Audio downloads create separate music copies; Change history records only a bounded local set of actions. Keep your original music independently.
:::

## What survives restart?

::: table {"widths": [0.5, 0.5], "headers": true}
| Survives locally | Usually temporary |
| --- | --- |
| Sign-in/configuration, library caches, saved themes/preferences, account-local hearts, remembered queue order, explicitly paused playlist imports and saved cleanup reports. | Elapsed playback time, unpaused editor/import drafts, online Now playing lyrics, upload/download selections and job progress. The bounded local queue itself is restored without starting audio. |
:::

::: small
Downloaded files and their integrity manifest remain on disk. Restarting a transfer requires a new reviewed selection; reopening never automatically sends or downloads music.
:::
