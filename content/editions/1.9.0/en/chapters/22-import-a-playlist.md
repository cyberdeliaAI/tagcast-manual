+++
id = "import-a-playlist"
group = "ORGANISE"
title = "Import a playlist"
lead = "Match a CSV or public playlist to music already in your iBroadcast library."
wiki = "Importing-playlists"
+++

::: figure figure-008
1.7.0: CSV column mapping; these are local records, not a fetched URL result.
:::

**1.**  Choose **Playlists > Import CSV**, check encoding/separator/header and preview. Map **Track title** and **Performing artist**; album, duration, year and number are optional. Set duration units correctly.

**2.**  Choose **Match tracks**. Unique full-title/performer matches can be automatic; versions, ambiguous copies and conflicting mapped fields need a decision. Album mapping makes matching stricter.

**3.**  Use **Find / choose a track** or **Change match** to compare copies. Keep the default manual choice for ambiguity, or deliberately choose a matching-copy preference such as Prefer FLAC. Skip unwanted records.

**4.**  Name the playlist, review its ordered matches and any unresolved omissions, then **Create private playlist in iBroadcast**. Wait for confirmation before repeating an import.

::: small
**Playlist URL** accepts public Deezer lists; enable Deezer under Sources & keys. ListenBrainz is an experimental test source and can be blocked. Spotify, Apple Music and TIDAL URLs are not supported. Fetching retrieves metadata, never audio.
:::
