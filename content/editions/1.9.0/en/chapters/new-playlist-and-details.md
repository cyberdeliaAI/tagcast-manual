+++
id = "playlist-and-details"
group = "LISTEN"
title = "Playlist and Details"
lead = "Keep the queue or current track information beside your browsing view."
wiki = "Workspace-controls"
+++

Open the right playback panel and choose **Playlist** or **Details**. The panel and the left **Navigation** toggle work independently; opening one does not automatically close the other.

::: table {"widths": [0.28, 0.72], "headers": true}
| Tab | What it shows |
| --- | --- |
| Playlist | The local playback queue, its current position and Up next. It is not the saved Playlists library. |
| Details | Known information about the current queued track and its original native album, even while another album is open. |
:::

Details follows the player selection, not the album you happen to browse. It uses already loaded information. Opening it does not fetch provider data, read audio or change metadata. An empty queue shows a hint rather than inventing a selected track.

Where known, Details can show track/album identity, technical information and stored ReplayGain. Album totals for duration or size appear only when the required values are complete. Missing information stays missing; stored ReplayGain is display information, not a new playback setting.

Use the ordinary album **Edit** action to change metadata. Playback continues through browsing, tab changes and opening Details. Remote queue synchronisation keeps its separate consent and controller rules.
