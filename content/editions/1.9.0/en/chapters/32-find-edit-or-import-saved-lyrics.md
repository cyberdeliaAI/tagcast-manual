+++
id = "find-edit-or-import-saved-lyrics"
group = "LYRICS"
title = "Find, edit or import saved lyrics"
lead = "Native text is ordinary lyrics. Saving it requires its own reviewed action and Premium access."
wiki = "Lyrics"
+++

::: figure figure-015
1.7.0: match LRC/TXT files to album tracks; this is preparation, not saving.
:::

For one track, use **Edit > Edit tracks > Track lyrics in iBroadcast**. **Find lyrics on LRCLIB** explicitly searches; **Use these lyrics** fills the separate draft. Then choose **Review lyrics** and **Save lyrics to iBroadcast**. A blank reviewed After removes only lyrics. Other native userdata is preserved.

For an album, choose **More > Import lyrics**. Select LRC/TXT files, inspect automatic number/full-title links and resolve ambiguity manually. **Review linked lyrics** reads current native text. Existing lyrics are kept unless you explicitly choose replacement for that track. Save runs one track at a time and stops on conflicts or uncertain results.

File import supports up to 100 tracks/files, 5 MB total and 500 KB per file. Files and links are temporary until reviewed/saved; closing an unsaved import asks before discarding it.

::: small
To read existing album lyrics without playback, choose **More > Check album lyrics** (up to 100 tracks). It reads iBroadcast, not public providers. Known text gets a Lyrics label beside the title; no label may simply mean unchecked. Free accounts can read/search lyrics but cannot save them.
:::

For album-local sidecar files, see [Importing lyrics in the Wiki](https://github.com/cyberdeliaAI/tagcast/wiki/Importing-lyrics). Those files still use the separate lyrics review and save.
