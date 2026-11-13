+++
id = "settings-reference"
group = "PERSONALISE"
title = "Settings reference"
lead = "Use the timing label beside each control rather than assuming every setting needs Save."
wiki = "Settings-and-help"
+++

::: table {"widths": [0.2, 0.39, 0.41], "headers": true}
| Category | Main choices | When they apply |
| --- | --- | --- |
| Interface | Language, banner, sidebar, First setup, default track-year checkbox | Immediate local choices; language also persists through the server when available. |
| Appearance | Custom themes and portable JSON | Draft preview until Save theme / Save & use. |
| Playback | Labels, expanded view, CD, lyrics, Gapless; quality, play reporting, queues | Display choices immediate/next opening; Gapless next track; server settings require Save. |
| Discovery | 1001 Albums, artist biographies, album background | Save; analyses remain explicit. Visited-page lookups depend on their switches. |
| Sources & keys | Providers, keys, automatic editor lookup | Save; key removal submits the current server settings form. |
| Data & exports | Metadata/history exports, music uploads | Exports explicit; upload enable requires Save and authorization before Start. |
| About & updates | Community, manual/automatic stable-release checks; desktop package choices | Automatic checks require Save; package download is a separate desktop preference. Install requires explicit confirmation. |
:::

**Discard changes** only discards unsaved server preferences. It does not undo immediate browser choices. Disabling a provider keeps its saved key; Remove deletes the saved key, so check other pending settings first. Environment-supplied keys must be managed outside Tagcast.

The desktop app remembers resized main and Mini Player windows in its own profile. This is independent of the expanded Now playing mode. Browser and desktop profiles, or another local port, can have different appearance/history preferences.

::: small
Since 1.7.0, a settings submission is validated before changes are applied. Invalid values or a persistence failure leave the existing configuration intact; sign-in scope and runtime services must remain consistent. Read the error and correct the form before retrying.
:::
