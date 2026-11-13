+++
id = "review-linked-lyrics-separately"
group = "LYRICS"
title = "Review linked lyrics separately"
lead = "Native lyrics have their own review, save and uncertainty rules."
wiki = "Importing-lyrics"
+++

::: figure figure-042
1.7.0: linked tracks are Ready for the separate lyrics decision; no completed save is shown.
:::

Review only linked tracks. Before/After shows the current native text and proposed ordinary text. Existing lyrics stay unless you explicitly choose replacement for that track. Timing markers are removed for native saves; the online timed display is separate.

Save reviewed lyrics proceeds one track at a time, preserves unrelated native userdata and reads back each accepted write. Stop, conflicts, errors or unconfirmed outcomes leave later tracks unsent. No automatic retry is performed. Source/account/library changes invalidate stale work.

::: callout
Premium and cache boundaries

Free accounts can read known/native text and explicitly search supported public lyrics, but cannot save. A cached text is not permission to overwrite newer native lyrics; review/save still use fresh guards. The 1.7.0 review optimization avoids redundant reads without removing those checks.
:::
