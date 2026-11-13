+++
id = "troubleshooting"
group = "REFERENCE"
title = "Troubleshooting"
lead = "Start with the visible state and exact message; avoid deleting settings as a first response."
wiki = "Troubleshooting"
+++

::: table {"widths": [0.31, 0.69], "headers": true}
| Symptom | Try this |
| --- | --- |
| Still seeing the demo | Finish official approval and keep Tagcast open. Check the connection dialog; wait if Loading library is active. Reload when connected. |
| Library looks old | Reload library. If necessary, Download everything again in the connected dialog. Preserve unsaved drafts before reloading. |
| Saving seems slow | Checking verifies against iBroadcast and may download a large library. Wait; do not start a duplicate write. |
| Album fields blocked | Turn off Combine Multi-Disc Album Sets in iBroadcast and reload before a new review. Supported track edits may have succeeded already. |
| No lyrics / wrong timing | Check source mode, enabled LRCLIB and whether expanded Lyrics is open. Retry temporary failures where offered. A provider may lack this exact version. |
| Gap or buffering | Compare normal playback and Original quality; check service/network health. Unsupported Gapless boundaries use ordinary playback. |
| Missing local hearts/history/theme | Check the account, desktop/browser profile, settings directory and local port. Metadata changes in iBroadcast are separate. |
| Upload stopped / needs checking | Inspect iBroadcast before preparing again. Stop can wait for an active network read; accepted files may still arrive. |
| Old-looking interface after update | Quit the older app and reopen the intended extracted package. Check the footer version before discarding drafts or resetting data. |
:::

::: small
For a bug report, include Tagcast version, operating system, desktop/browser mode, exact steps/message and whether it is reproducible. Crop private account details, paths and tokens from screenshots/logs. [GitHub Issues](https://github.com/cyberdeliaAI/tagcast/issues) is best for reproducible problems; [r/Tagcast](https://www.reddit.com/r/Tagcast/) is available for discussion.
:::
