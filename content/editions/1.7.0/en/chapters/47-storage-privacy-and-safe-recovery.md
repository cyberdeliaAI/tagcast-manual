+++
id = "storage-privacy-and-safe-recovery"
group = "YOUR DATA"
title = "Storage, privacy and safe recovery"
lead = "Know which actions affect iBroadcast and which remain on this computer."
wiki = "Whats-saved-where"
+++

::: table {"widths": [0.5, 0.5], "headers": true}
| Stored in iBroadcast | Local to Tagcast |
| --- | --- |
| Reviewed metadata/credits, saved native lyrics, artwork, native stars/track ratings, tags and private playlists; reviewed trash/merges affect the account library. | Tokens/settings/caches, album/artist hearts and reports in the settings folder; appearance and bounded History in the browser/app profile. |
:::

The default settings directory is **~/.tagcast/**, or .tagcast in your Windows user folder. TAGCAST_HOME can select another folder. Browser-local data belongs to its profile and local address/port. Changing ports or clearing site data can hide local history/preferences without changing iBroadcast.

Disconnect forgets local sign-in/library cache and attempts token revocation. It does not undo saved account changes or erase every separate report/favourite. Tokens and source keys remain on the local server, not in the frontend.

## When network requests happen

iBroadcast is contacted for sign-in, library, playback and your chosen operations. Public update checks contact GitHub when enabled. Overview checks the public service feed. Selected editor providers can run automatically when the editor opens if that preference is enabled.

Opt-in biographies/background text run for visited pages. Online Now playing lyrics require an online mode and an open listening-page or expanded lyrics view. Explicit Find lyrics and public-playlist fetches have their own actions. Uploads send chosen audio only after Start; downloads fetch audio only after Start downloads.

::: callout
An uncertain write needs inspection

Keep the result/report, inspect the actual iBroadcast values and reload. Do not immediately repeat a merge, import, upload or save with an uncertain result. A timeout can mean the server already applied it. There is no global rollback.
:::

::: small
Read the [Privacy policy](https://github.com/cyberdeliaAI/tagcast/blob/main/PRIVACY.md) for current network and data-handling details.
:::

::: small
The standalone browser interface now sends a Content Security Policy, matching the desktop security intent without allowing arbitrary inline/evaluated JavaScript. Keep the existing local-server protections; an unsupported browser feature is not a reason to disable security headers.
:::
