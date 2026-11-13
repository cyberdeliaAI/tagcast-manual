+++
id = "recover-from-an-audio-interruption"
group = "LISTEN"
title = "Recover from an audio interruption"
lead = "Recovery follows the same queue occurrence and your latest playback intent."
wiki = "Playback-and-queue#playback-error-recovery"
+++

In 1.7.0, a recoverable temporary network failure permits one automatic source reload for the same track occurrence and streaming quality. Track position, queue and listening-history watch are retained. A later Pause or seek is respected; Mini Player and system controls use the same player.

::: table {"widths": [0.36, 0.64], "headers": true}
| State | What it means |
| --- | --- |
| Temporary network interruption | One controlled source reload can recover; it is not an endless retry loop. |
| Recovery failed | Playback stops visibly. Inspect the message and press Play explicitly when ready. |
| Permission, certificate, unavailable track or decode error | Not treated as a transient network problem. Fix the stated cause. |
| Unsupported Original format | The existing labelled MP3 128 kbps fallback can apply; a network/sign-in error does not silently lower quality. |
:::

Gapless owns its own fallback; the ordinary player does not start a competing recovery. Stopping, changing track/account/library or beginning shutdown cancels stale recovery. Buffering is not counted as listening, and uncertain play-reporting writes are not resent. Keep Tagcast open during shutdown does not restart interrupted audio.
