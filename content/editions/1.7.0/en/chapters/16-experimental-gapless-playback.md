+++
id = "experimental-gapless-playback"
group = "LISTEN"
title = "Experimental Gapless playback"
lead = "For compatible consecutive album tracks, not a promise about every file or output."
wiki = "Gapless-playback"
+++

**1.**  Choose **Original file (Premium)** under Streaming quality and **Save changes**.

**2.**  Enable **Gapless playback for albums in order** in Settings > Playback. It is off by default.

**3.**  Start a fresh ordered album with **Play album**. The time bar remains relative to the current track.

## Supported path

Original FLAC is the primary validated path. Compatible consecutive tracks share a continuous buffer without crossfading or removing silence. Sample rate, channels, bit depth and decoder block-size compatibility matter; large or unusual files may exceed the preparation limits.

Starting can take longer because music is prepared first. Seeking close to the end can wait for the next track. Intentional recorded silence remains. Explicit Next/Previous are available but are not promised seamless transitions.

::: callout
When ordinary playback is expected

Shuffle album, Random Album, playlists and active queue synchronisation use standard playback. Unsupported files/transitions, preparation limits or decoder failures fall back to ordinary playback. The player identifies the fallback; a pause at that boundary is possible.
:::

## Keep expectations precise

MP3 has a separate experimental path that depends on acceptable delay/padding metadata; real iBroadcast MP3 alignment is not universally established. Prefer Original FLAC when checking supported Gapless behaviour.

Deterministic audio tests establish exact continuity for their measured inputs. They do not prove universal sample accuracy on every platform, physical output or album. Sleep/wake and output-device changes depend on the system. If an album has a reproducible problem, compare Gapless off and record the exact format, action and boundary.
