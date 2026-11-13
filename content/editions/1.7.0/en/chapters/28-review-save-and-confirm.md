+++
id = "review-save-and-confirm"
group = "EDIT METADATA"
title = "Review, save and confirm"
lead = "A sent request and a confirmed saved result are different states."
wiki = "Saving-and-history"
+++

::: figure figure-012
1.7.0: proposed composer change on 37 tracks; no save is confirmed by this review.
:::

Before writing, Tagcast checks fresh library state against the review. Conflicting or replaced data blocks the save. Only changed supported fields are sent. After acceptance, a fresh library read-back checks the result. **Do not close and repeat an action because verification is slow.**

::: table {"widths": [0.34, 0.66], "headers": true}
| Result | What to do |
| --- | --- |
| Saved / confirmed | The checked values match. Other entries in the same job may have different results. |
| Checking / sent, checking | Wait for read-back. Large-library verification can take longer than the write. |
| Unconfirmed / not confirmed | Inspect iBroadcast and reload before any fresh review. An absent response does not prove failure. |
| Failed / blocked / not sent | Read the reason. Earlier writes may already have succeeded; later requests can remain unsent. |
:::

::: small
Mutating requests are sent once rather than blindly retried after an ambiguous reply. Saves are not transactional and have no general metadata Undo. **Change history** keeps the newest 300 entries in this browser/profile and local address. Export it before clearing site data. Artwork has limited separate Undo; ratings, tags, lyrics, playlists, merging and trash do not gain Undo from History.
:::
