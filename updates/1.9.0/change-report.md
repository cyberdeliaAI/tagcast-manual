# Tagcast 1.7.0 to 1.9.0 manual change report

Status: proposal for editorial review. Prepared on 13 November 2026.

Update the existing illustrated manual incrementally. Carry forward the 1.7.0
content and design, add four focused topics, and revise the affected instructions,
references and illustrations. The largest changes are First setup, the compact
workspace, explicit MusicBrainz comparison/correction drafts, desktop updates and
the relocated Change history actions. These span both 1.8.0 and 1.9.0.

All 14 supplied screenshots match unchanged originals already present in the
released 1.9.0 source commit. They cover most general views. The clearest missing
illustrations are an open Details panel and the comparison/correction workflow.
The supplied update dialog is a usable interface example: the maintainer confirms
its version numbers are illustrative, so it does not need replacement on that account.

This proposal changes no manual text, captions, edition metadata, image selection,
renderer or visual baseline. The 1.7.0 reference edition remains fixed. No new PDF,
application operation, Wiki edit, commit, push or publication is part of this report.

## Fixed comparison sources

| Source | Revision |
|---|---|
| Previous documented application | [v1.7.0](https://github.com/cyberdeliaAI/tagcast/commit/a2493c85639780a9ca2b2a7121db85605b659c92) / `a2493c85639780a9ca2b2a7121db85605b659c92` |
| Existing manual checkout | `f67c8d061bd1f3b12a3e3512141159e623b2432e`; 50 topics on PDF pages 3-52 |
| Original manual documentation/images | `9b47dae9ba917da0bcdfc93b8d6fa52c0c23c900` |
| Original Wiki text baseline | `14d3e9839bf83cf8029ad8fc0084255ed251e2c8` |
| Intermediate published release | [v1.8.0](https://github.com/cyberdeliaAI/tagcast/releases/tag/v1.8.0) / `9c1615214ec11dc49dfaf23fc653d600f5e936a3` |
| Target published release | [v1.9.0](https://github.com/cyberdeliaAI/tagcast/releases/tag/v1.9.0) / `440199a359fd2df2fd615e3222fb36afbc13427c` |
| Wiki used for this proposal | `095b8c1f1189a4cb5237d3d3cd9089924a8caefa`; confirmed as the public Wiki HEAD |
| Supplied screenshots | 14 PNGs, all 2660 x 1780; filename dates 13 November 2026; timezone and captured build commit are not supplied |

[evidence.json](evidence.json) records source-file hashes, release observations,
the inspected code paths and the Wiki locator audit.
[chapter-impact.json](chapter-impact.json) maps every existing topic to its stable
ID and proposed action. [screenshots-inventory.json](screenshots-inventory.json)
records original filenames, SHA-256, visible states and proposed uses.

The 1.7.0 application commit and later documentation/image commit serve different
purposes. Screenshot additions and Wiki reorganisation are not new application
features. Functional claims below have code evidence as well as Wiki/release
context; existing tests were inspected, not rerun as new product validation.

## Changes supported by release source and Wiki

### D01 First setup

Introduced in 1.8.0. Add the guided Welcome, Playback, Lyrics, Workspace,
Optional services and Ready steps. Explain automatic opening for genuinely new
profiles and explicit opening from Settings > Interface > First setup for existing
profiles. It reuses sign-in and existing preferences. Save and continue applies a
step; Back, Set up later and Skip this step have different draft/progress effects.
Keep account capabilities, save failures, consent and opt-in defaults explicit.
The final English interface label is Ready; the Wiki describes its summary function.

Sources: [Wiki First setup](https://github.com/cyberdeliaAI/tagcast/wiki/First-setup),
[wizard and save handling](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/first-setup.js#L5),
[new-profile eligibility](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/client.py#L468),
[existing eligibility tests](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/tests/test_client.py#L67).

### D02 Navigation and playback details

Introduced in 1.8.0. Explain the independent navigation toggle and one right-hand
panel with Playlist and Details tabs. Playlist is the existing local queue,
separate from native Playlists. Devices is beside Play queue, including when the
queue is empty, and remains on the full Now playing page.

Details follows the current queued track and its original native album, even
while another album is being browsed. It uses known loaded metadata; it is not an
editor or provider lookup. Missing values stay unknown; complete-album totals
need complete values. Stored ReplayGain is display metadata, not a newly applied
audio effect. Include the restored-queue and empty-queue cases without promising
that every album detail has already been loaded.

Sources: [Wiki Workspace controls](https://github.com/cyberdeliaAI/tagcast/wiki/Workspace-controls),
[navigation/sort controls](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/workspace.js#L9),
[playback-following Details](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/workspace.js#L87),
[bounded restored metadata](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/collections.py#L601),
[queue restoration](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/queue-memory.js#L65).

### D03 Fixed sorting and Filters

Introduced in 1.8.0. Replace Filter and sort directions with the fixed sort row and
the Filters menu. Albums has Artist, Title, Year, Added, Rating and Random;
Album artists has Name, Rating and Random. Clicking an active direction reverses
it; Random reshuffles the matching shelf without playback. Added means the stored
upload date. The separate Albums Play random album shortcut was removed; random
playback within discovery groups remains. This also changes the duplicate-filter
entry path in chapter 36.

Sources: [Wiki fixed sort buttons](https://github.com/cyberdeliaAI/tagcast/wiki/Workspace-controls#fixed-sort-buttons),
[sort definitions](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/workspace.js#L25),
[Filters rendering](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/app.js#L338),
[remaining discovery random-play control](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/player.js#L329).

### D04 Compact album actions

Introduced in 1.8.0. Use the current Play label, the Shuffle album icon and its
accessible name, Queue, Edit and More album actions. Add to playlist moves into
More; Compare track list is another explicit menu choice. Keep existing album/set
membership and queue effects; this is an entry-point change, not a new playlist
mutation contract.

Sources: [Wiki Album pages](https://github.com/cyberdeliaAI/tagcast/wiki/Album-details),
[album actions](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/album.js),
[More menu](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/index.html#L298),
[guarded playlist handoff](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/collections.js#L122),
[exact English labels](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/i18n/en.json#L4).

### D05 Comparison and correction drafts

Introduced in 1.8.0. Add More > Compare track list, explicit Search MusicBrainz,
edition selection and positional observations. Opening makes no provider request;
search and selection are separate. Search is 20 editions per page and at most
200 per query; local/reference lists are bounded to 1,000 audio tracks. Known
duration differences greater than two seconds are observations, not audio identity.
Incomplete/unknown values and versions remain visible.

Use title and Use artist credits are explicit per-track choices. Choose another
reference track is manual pairing; Open corrections in editor transfers only
chosen changed title/artist fields into the ordinary review. It does not copy
numbers, years, duration, membership or album fields. Preserve existing credits,
roles, phrases and native IDs. Comparison does not save, reorder, merge or split.
The handoff suppresses automatic suggestions/initial lyrics expansion; ordinary
explicit track selection keeps its existing lazy lyrics behavior.

Sources: [Wiki comparison and corrections](https://github.com/cyberdeliaAI/tagcast/wiki/Comparing-track-lists),
[read-only endpoints and limits](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/track_comparison.py#L8),
[explicit opening and observations](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/track-comparison.js#L21),
[chosen-field editor handoff](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/track-comparison-drafts.js#L35),
[provider/ownership tests](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/tests/test_track_comparison.py#L43),
[existing correction regressions](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/tests/frontend.test.cjs#L6761).

### D06 History actions

Changed in 1.9.0. Locate Export changes and Clear change history below the heading,
above entries; the clear confirmation stays there. Export remains local JSON.
Clearing needs confirmation, waits for saves/read-back and removes local entries
and artwork Undo information without reverting iBroadcast. The supplied screenshot
contains both Saved and Checking entries: preserve that distinction.

Sources: [Wiki Change history](https://github.com/cyberdeliaAI/tagcast/wiki/Saving-and-history#overview-and-change-history),
[dialog structure](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/index.html#L222),
[export/clear guards](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/app.js#L1336).

### D07 Desktop update dialog

Introduced in 1.9.0. Describe bounded plain-text release notes and the explicit
Download update, Restart and install, Later and Skip this version actions.
Opening the dialog or manually checking for a release does not itself download
or install a package. A supported download can continue while audio plays.
The maintainer's S01 example is suitable for illustrating these controls, with
illustrative version numbers in its caption.

Sources: [Wiki Updating Tagcast](https://github.com/cyberdeliaAI/tagcast/wiki/Updating-Tagcast),
[bounded notes](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/updates.py#L39),
[escaped dialog and controls](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/updates.js#L128),
[explicit offer/download state](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/updates.cjs#L89).

### D08 Platform update routes

Install 1.9.0 manually once when coming from 1.7.0 or 1.8.0; those earlier clients
cannot perform the new installation flow. From 1.9.0, a later stable version can
be installed in-app only on supported installations. Keep this platform matrix:

| Installation | Route to document |
|---|---|
| Developer ID signed macOS app, Apple Silicon or Intel | Download, then confirm native replacement/restart |
| Homebrew-managed macOS | Homebrew update/upgrade commands |
| Installed Debian/Ubuntu package in /opt/Tagcast | Download, then approve the native installer privilege request |
| Current unsigned Windows NSIS installer or portable ZIP | Manual installation; the new per-user installer does not enable in-app Windows updating |
| Linux TAR.GZ or source/browser | Manual package/source route |
| Ad-hoc macOS app or window reusing another server | Manual route; the updater does not own that server |

Add the Windows `tagcast-1.9.0-windows-x64-setup.exe` alongside the portable ZIP in
installation guidance. Retain SHA-256 companions and signing limitations. An
installer's presence is not evidence of trusted Windows signing.

Sources: [Wiki platform routes](https://github.com/cyberdeliaAI/tagcast/wiki/Updating-Tagcast#platform-routes),
[installation detection](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/updates.cjs#L174),
[backend ownership gate](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/main.cjs#L217),
[empty trusted Windows publisher configuration](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/update-config.json),
[Windows installer packaging](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/tools/windows_installer.py).

### D09 Update preferences and privacy

Separate automatic release checking from the new, initially off automatic package
download preference. Download consent and skipped version belong to the local
desktop profile. An explicit check can still show a skipped version. Packages
come from the fixed project release location, with exact version/platform names
and SHA-512 digests. This is separate from music-download `.ibfetch.json` integrity.
No iBroadcast credentials, library/track data or persistent staged-rollout ID are
sent by the updater. Include the public MusicBrainz query boundary from D05 in
the network/storage chapter.

Sources: [Wiki update preferences](https://github.com/cyberdeliaAI/tagcast/wiki/Updating-Tagcast#download-and-install),
[local preferences and offer policy](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/updates.cjs#L44),
[fixed feed/package validation](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/updates.cjs#L19),
[network session and native defaults](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/native-updater.cjs#L4),
[release privacy policy](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/PRIVACY.md).

### D10 Confirmed installation and shutdown

Restart and install needs an additional native confirmation. Ordinary Quit never
installs. Unsaved drafts retain their prompts; accepted writes, verification and
required local storage finish before the owned backend exits and installation
can proceed. Keep Tagcast open cancels that attempt; uncertain writes postpone
installation. Preserve the no-forced-deadline/no-blind-retry guidance.

Supported routes are implemented; the first later updater-enabled two-version
upgrade chain still has explicit validation requirements. Do not turn package
smoke tests or these screenshots into a claim of universally validated signed
in-place upgrades.

Sources: [Wiki installation/recovery](https://github.com/cyberdeliaAI/tagcast/wiki/Updating-Tagcast#download-and-install),
[uncertainty and backend shutdown](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/main.cjs#L34),
[native confirmation](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/main.cjs#L229),
[approval and finish gates](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/updates.cjs#L146),
[existing shutdown/updater tests](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/electron/tests/updates.test.cjs#L75),
[next-chain validation requirement](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/desktop-updates.md#L90).

### D11 Current screenshot coverage

Use the candidates listed below selectively. Retain earlier examples where the
workflow is unchanged or no current equivalent exists. Match every proposed
caption to the visible state. All 14 supplied originals match their release-tree
copies, including S01's explicitly confirmed illustrative offer. Do not infer a
CSS viewport, signed binary provenance or hardware coverage from image dimensions.

Sources: [release screenshot inventory](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/README.md),
[Wiki gallery](https://github.com/cyberdeliaAI/tagcast/wiki/Screenshots), [hashed inventory](screenshots-inventory.json).

### D12 Canonical Wiki destinations

The Wiki now separates Workspace controls, First setup, Comparing track lists,
Updating Tagcast, Now playing and Overview and metadata health. Point the future
edition directly to those task owners. In particular, update chapters 7, 14, 15,
17 and 18 to their current owner; chapter 32 should distinguish individual lyrics
from the sidecar importer. The original 50 page/fragment locators are still
present locally. The playback/Overview aliases lead to navigation tables that
link onward, so their continued existence is not a reason to retain indirect links.
This was a source/locator audit, not a new GitHub-rendering test.

Sources: [Wiki Home](https://github.com/cyberdeliaAI/tagcast/wiki/Home),
[old playback aliases](https://github.com/cyberdeliaAI/tagcast/wiki/Playback-and-queue#now-playing-views),
[current Now playing](https://github.com/cyberdeliaAI/tagcast/wiki/Now-playing),
[current Overview](https://github.com/cyberdeliaAI/tagcast/wiki/Overview-and-metadata-health).

### D13 Amber Midnight

Add the downloadable Amber Midnight example using the existing JSON import,
preview and Save & use workflow. It is a portable custom theme shown under My
themes, not a seventh built-in palette. Keep appearance independent of palette
and preserve local-only effects. S07 illustrates the menu after a custom theme
has been saved; it does not replace an editor-preview illustration.

Sources: [Wiki custom theme](https://github.com/cyberdeliaAI/tagcast/wiki/Custom-themes#amber-midnight),
[portable JSON](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/themes/tagcast-amber-midnight.json),
[six built-in palettes and explicit theme import](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/themes.js#L12).

### D14 Edition metadata

Create a separate future 1.9.0 edition only after content approval. Record the app,
Wiki and asset revisions independently, choose its actual document revision/date,
and regenerate contents, bookmarks, page numbers and output hashes after layout.
The page numbers in this report locate the original 52-page edition; they are not
promises about the future pagination. Keep both historical published editions intact.

### E01 Existing palette wording correction

Chapter 44 currently assigns red/pink accents to the last palette in its list,
Amber. The current source and Wiki associate red/pink with Apple Music Classic;
Amber uses amber/gold accents. This is an existing editorial correction proposed
for the future copy, not a new 1.9.0 palette behavior and not a change to the
fixed reference edition.

Sources: [reference chapter 44](../../content/editions/1.7.0/en/chapters/44-themes-and-custom-colours.md),
[palette values](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/src/tagcast/static/themes.js#L8),
[Wiki Apple Music Classic and Amber](https://github.com/cyberdeliaAI/tagcast/wiki/Custom-themes#apple-music-classic).

## Existing chapter impact

Action counts: 22 update, 5 references only,
4 illustration review and 19 retain.
Illustration candidates are optional unless the proposed instruction would
otherwise show the wrong control. Historical examples may remain labelled.
All actions target a future copy; this report edits none of these files.

| Chapter and original page | Existing topic | Proposed action | Changes and image candidates |
|---|---|---|---|
| 01 / p03 | [Your first session](../../content/editions/1.7.0/en/chapters/01-your-first-session.md) | update: Mention First setup for genuinely new profiles and use the current Play label; keep explicit sign-in and reviewed saves. | D01, D04 |
| 02 / p04 | [Install and update](../../content/editions/1.7.0/en/chapters/02-install-and-update.md) | update: Add the Windows NSIS installer, the manual first upgrade to 1.9.0, supported later update routes and explicit installation confirmation. | D07, D08, D10; S01 |
| 03 / p05 | [Connect your account](../../content/editions/1.7.0/en/chapters/03-connect-your-account.md) | retain: Keep the existing device/custom-client sign-in explanation. First setup reuses this flow; it adds no second login. | No release-driven change |
| 04 / p06 | [Close and restart safely](../../content/editions/1.7.0/en/chapters/04-close-and-restart-safely.md) | update: Distinguish ordinary Quit from Restart and install; keep accepted writes/read-back, Keep Tagcast open and reused-server limits. | D10 |
| 05 / p07 | [Find your way around](../../content/editions/1.7.0/en/chapters/05-find-your-way-around.md) | update: Replace combined Filter and sort directions with Filters plus fixed sort buttons; explain sidebar/panel toggles and the removed Albums random-play shortcut. | D02, D03; S06, S09 |
| 06 / p08 | [Choose the right view](../../content/editions/1.7.0/en/chapters/06-choose-the-right-view.md) | retain: Keep browse-category semantics. Explain Playlist versus native Playlists in the new panel topic rather than adding a misleading browse category. | No release-driven change |
| 07 / p09 | [Overview and discovery](../../content/editions/1.7.0/en/chapters/07-overview-and-discovery.md) | references: Point directly to Overview and metadata health. Keep current service-status semantics; a new image is optional. | D12; S10 |
| 08 / p10 | [Read an album page](../../content/editions/1.7.0/en/chapters/08-read-an-album-page.md) | update: Use Play and the Shuffle album icon; place Add to playlist and Compare track list in More album actions. Preserve grouping/rating/tag rules. | D04, D05; S04, S08 |
| 09 / p11 | [Continuous scroll and Random order](../../content/editions/1.7.0/en/chapters/09-continuous-scroll-and-random-order.md) | update: Describe the fixed Random sort button and separate Filters control. Keep continuous browsing; restrict random-play guidance to discovery groups. | D03; S09 |
| 10 / p12 | [Use the cache and refresh deliberately](../../content/editions/1.7.0/en/chapters/10-use-the-cache-and-refresh-deliberately.md) | illustration: Keep cache/refresh behavior. Optionally refresh figure-028 after privacy review; the redacted historical image remains usable. | D11; S10 |
| 11 / p13 | [1001 Albums and local matching](../../content/editions/1.7.0/en/chapters/11-1001-albums-and-local-matching.md) | illustration: Keep explicit local analysis/linking. Choose current examples with captions matching In your library versus Not found; preserve attribution. | D11; S11, S12, S13 |
| 12 / p14 | [A narrow window](../../content/editions/1.7.0/en/chapters/12-a-narrow-window.md) | retain: Keep the stacked narrow-window explanation and labelled historical mobile image. All new captures are desktop frames, not mobile replacements. | No release-driven change |
| 13 / p15 | [Play music and manage the queue](../../content/editions/1.7.0/en/chapters/13-play-music-and-manage-the-queue.md) | update: Explain the Playlist panel as the existing local queue, Devices beside Play queue, and Details as a separate playback-following tab. | D02, D04; S03 |
| 14 / p16 | [Expanded Now playing and CD view](../../content/editions/1.7.0/en/chapters/14-expanded-now-playing-and-cd-view.md) | references: Point to Now playing#optional-cd-view. Keep the existing Cover/CD behavior and labelled example. | D12 |
| 15 / p17 | [Mini Player, sound and quality](../../content/editions/1.7.0/en/chapters/15-mini-player-sound-and-quality.md) | references: Point to Now playing#desktop-mini-player. Mini Player, AirPlay and stream-quality semantics are unchanged. | D12 |
| 16 / p18 | [Experimental Gapless playback](../../content/editions/1.7.0/en/chapters/16-experimental-gapless-playback.md) | retain: Keep experimental/off-by-default Gapless limits. First setup is an additional entry point; the capture does not establish new audio support. | No release-driven change; S05 |
| 17 / p19 | [Eight music visualizations](../../content/editions/1.7.0/en/chapters/17-eight-music-visualizations.md) | illustration: Optionally refresh the Ribbon example, keeping the other seven effects and their historical labels; point to Now playing. | D11, D12; S14 |
| 18 / p20 | [Visualization controls and rotation](../../content/editions/1.7.0/en/chapters/18-visualization-controls-and-rotation.md) | references: Point to Now playing#eight-optional-music-visualizations. Rotation, timing and reduced-motion semantics stay unchanged. | D12; S14 |
| 19 / p21 | [Recover from an audio interruption](../../content/editions/1.7.0/en/chapters/19-recover-from-an-audio-interruption.md) | retain: Keep the one controlled audio-recovery attempt and existing fallback limits; do not claim broader recovery support. | No release-driven change |
| 20 / p22 | [Tags, ratings and favourites](../../content/editions/1.7.0/en/chapters/20-tags-ratings-and-favourites.md) | retain: Keep native tags, ratings and local favourites unchanged; retain the explicitly labelled older tag-manager example. | No release-driven change |
| 21 / p23 | [Playlists and folders](../../content/editions/1.7.0/en/chapters/21-playlists-and-folders.md) | update: Change the album entry path to More album actions > Add to playlist. Keep playlist review, duplicate-position and queue distinctions. | D04 |
| 22 / p24 | [Import a playlist](../../content/editions/1.7.0/en/chapters/22-import-a-playlist.md) | retain: No CSV mapping/matching change identified in the release source range; preserve local/import review boundaries. | No release-driven change |
| 23 / p25 | [Keep import progress and review order](../../content/editions/1.7.0/en/chapters/23-keep-import-progress-and-review-order.md) | retain: Keep paused CSV import and reviewed order behavior. Existing captures remain useful historical examples. | No release-driven change |
| 24 / p26 | [Playlist positions and uncertain results](../../content/editions/1.7.0/en/chapters/24-playlist-positions-and-uncertain-results.md) | retain: Retain F2-02: append with intentional duplicate positions is still unverified. The new comparison does not change append semantics. | No release-driven change |
| 25 / p27 | [Favourites and native ratings](../../content/editions/1.7.0/en/chapters/25-favourites-and-native-ratings.md) | retain: Keep local hearts versus native ratings and account/profile storage distinctions. | No release-driven change |
| 26 / p28 | [Edit album information](../../content/editions/1.7.0/en/chapters/26-edit-album-information.md) | update: Link the explicit comparison-correction route to the existing editor/review; distinguish it from ordinary automatic source suggestions. | D05 |
| 27 / p29 | [Tracks, credits and compilations](../../content/editions/1.7.0/en/chapters/27-tracks-credits-and-compilations.md) | update: Explain chosen title/artist-credit adoption, preservation of existing native IDs/roles/phrases, and no number/year/duration import. | D05 |
| 28 / p30 | [Review, save and confirm](../../content/editions/1.7.0/en/chapters/28-review-save-and-confirm.md) | update: Keep save guards and result meanings. Describe History actions above entries and clearing only local history/Undo after checks finish. | D05, D06; S02 |
| 29 / p31 | [Compare artwork and artist images](../../content/editions/1.7.0/en/chapters/29-compare-artwork-and-artist-images.md) | retain: Keep separate artwork comparison/save and limited artwork Undo; track-list comparison is a different workflow. | No release-driven change |
| 30 / p32 | [Follow a checked save](../../content/editions/1.7.0/en/chapters/30-follow-a-checked-save.md) | update: Use the current History example for Checking/read-back and relocated actions. Retain the genuinely confirmed composer example. | D06; S02 |
| 31 / p33 | [Lyrics that follow the music](../../content/editions/1.7.0/en/chapters/31-lyrics-that-follow-the-music.md) | illustration: Optionally use the new LRCLIB Now playing example. Keep native-only default, source order, visibility and cache/save boundaries. | D11; S03 |
| 32 / p34 | [Find, edit or import saved lyrics](../../content/editions/1.7.0/en/chapters/32-find-edit-or-import-saved-lyrics.md) | references: Link individual native lyrics to Lyrics and keep Importing lyrics for the album sidecar workflow; no new lyrics save behavior. | D12 |
| 33 / p35 | [Review linked lyrics separately](../../content/editions/1.7.0/en/chapters/33-review-linked-lyrics-separately.md) | retain: Keep explicit linked-track review, serialization, freshness and uncertainty rules. Comparison handoff is not an album lyrics import change. | No release-driven change |
| 34 / p36 | [Review metadata cleanup](../../content/editions/1.7.0/en/chapters/34-review-metadata-cleanup.md) | retain: Keep reviewed cleanup behavior, batches, stop/resume and reports. No new cleanup category is introduced. | No release-driven change |
| 35 / p37 | [Reconcile album and track years](../../content/editions/1.7.0/en/chapters/35-reconcile-album-and-track-years.md) | retain: Keep explicit known-year choices and no automatic oldest/majority inference. | No release-driven change |
| 36 / p38 | [Duplicate copies and trash](../../content/editions/1.7.0/en/chapters/36-duplicate-copies-and-trash.md) | update: Change Albums > Filter and sort > Duplicate tracks to Albums > Filters > Duplicate tracks. Preserve all trash/review safeguards. | D03 |
| 37 / p39 | [Merge album fragments](../../content/editions/1.7.0/en/chapters/37-merge-album-fragments.md) | retain: Keep merge eligibility, selected destination, membership review and nontransactional outcomes. | No release-driven change |
| 38 / p40 | [Split an album deliberately](../../content/editions/1.7.0/en/chapters/38-split-an-album-deliberately.md) | retain: Keep album splitting, explicit subset review and nontransactional outcomes. Comparison does not split or move tracks. | No release-driven change |
| 39 / p41 | [Upload local music](../../content/editions/1.7.0/en/chapters/39-upload-local-music.md) | retain: Keep explicit Start uploads, permission and uncertain-upload rules. Software updates do not add music uploads. | No release-driven change |
| 40 / p42 | [Download album copies](../../content/editions/1.7.0/en/chapters/40-download-album-copies.md) | retain: Keep explicit Start downloads and audio-copy rules. Download update is a separate desktop-software operation. | No release-driven change |
| 41 / p43 | [Download sources and file integrity](../../content/editions/1.7.0/en/chapters/41-download-sources-and-file-integrity.md) | retain: Keep original/stream distinctions and .ibfetch.json integrity. Updater SHA-512 is not the audio-download contract. | No release-driven change |
| 42 / p44 | [Language and sidebar](../../content/editions/1.7.0/en/chapters/42-language-and-sidebar.md) | update: Add the independent sidebar collapse preference and the Interface > First setup entry; keep language and shortcut ordering rules. | D01, D02 |
| 43 / p45 | [Playback preferences](../../content/editions/1.7.0/en/chapters/43-playback-preferences.md) | update: Add the setup cross-reference and current Devices location. Preserve save timing, opt-ins and Free-account limits. | D01, D02; S05 |
| 44 / p46 | [Themes and custom colours](../../content/editions/1.7.0/en/chapters/44-themes-and-custom-colours.md) | update: Add portable Amber Midnight under My themes, not built-ins. Correct the legacy red/pink colour attribution in the future copy only. | D13, E01; S07 |
| 45 / p47 | [Settings reference](../../content/editions/1.7.0/en/chapters/45-settings-reference.md) | update: Add First setup and separate desktop-profile automatic download/skip preferences from the backend automatic release-check setting. | D01, D07, D09; S01, S05 |
| 46 / p48 | [Export metadata and keep records](../../content/editions/1.7.0/en/chapters/46-export-metadata-and-keep-records.md) | update: Locate History export above entries; keep metadata JSON/CSV distinct. Include saved setup progress and desktop update preferences in restart/storage guidance. | D01, D06, D09; S02 |
| 47 / p49 | [Storage, privacy and safe recovery](../../content/editions/1.7.0/en/chapters/47-storage-privacy-and-safe-recovery.md) | update: Add public MusicBrainz comparison queries, GitHub package downloads/cache and local setup/update preferences; retain credential and native-write boundaries. | D01, D05, D09 |
| 48 / p50 | [Troubleshooting](../../content/editions/1.7.0/en/chapters/48-troubleshooting.md) | update: Add platform-specific manual-update reasons, postponed installs, expected existing-profile setup behavior, playback-following Details and incomplete/provider comparison results. | D01, D02, D05, D08, D10 |
| 49 / p51 | [Keyboard, limits and terminology](../../content/editions/1.7.0/en/chapters/49-keyboard-limits-and-terminology.md) | update: Add Playlist/Details tab keys and separate comparison limits: 20 editions/page, 200/query, 1,000 audio tracks. Preserve existing limits. | D02, D05 |
| 50 / p52 | [About this edition](../../content/editions/1.7.0/en/chapters/50-about-this-edition.md) | update: Prepare future 1.9.0 edition metadata and pinned source/asset revisions, with a new document date chosen at approval; leave this 1.7.0 file intact. | D14 |

## Proposed additional topics

These four topics are a proposed editorial division, not an instruction to
rewrite all 50 existing topics or to force one page per topic.

| ID | Proposed topic and placement | Scope | Illustration |
|---|---|---|---|
| N01 | First setup, after the connection/first-session guidance | New versus existing profiles, six steps, explicit saving, pause/skip and capabilities (D01) | S05; other steps can initially be described in text |
| N02 | Playlist and Details, next to queue playback | Playback-following read-only details, panel tabs, Devices and empty/restored queues (D02) | G01 needed for a fully illustrated explanation; S03 shows Devices on the full page |
| N03 | Compare a track list and prepare corrections, before ordinary track editing | Explicit search/edition choice, positional limits, chosen fields and normal editor review (D05) | G02-G04; existing editor/review images can support the unchanged final save |
| N04 | Download and install desktop updates, beside installation/update guidance | First manual 1.9.0 upgrade, platform matrix, notes, consent, safe restart and recovery (D07-D10) | S01 is a suitable interface example; G05-G06 are optional additional states |

## Supplied screenshot decisions

IDs identify candidates, not approved renderer assets. Source links below point
to the unchanged release-tree originals. Exact supplied filenames and hashes are
in the companion inventory. All frames remain untouched.

| ID and release image | Visible state | Proposed use | Caption or review condition |
|---|---|---|---|
| [S01 update-dialog.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/update-dialog.png) | Illustrative release offer, plain-text notes, Download update, Skip this version and automatic download unchecked. | reuse; ch. 02, ch. 45; N04 | The maintainer explicitly confirms the version offer is an interface example. Caption the version numbers as illustrative; no replacement is requested for that reason. |
| [S02 change-history.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/change-history.png) | History export/clear above entries; a cover entry is Checking and earlier genre entries are Saved; clear is disabled. | use; ch. 28, ch. 30, ch. 46 | Do not present the Checking artwork entry as confirmed or the visible artwork Undo as general metadata Undo. |
| [S03 now-playing-lyrics.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/now-playing-lyrics.png) | Full Now playing page with queue, Devices, LRCLIB line lyrics and the spectrum. | use; ch. 13, ch. 31 | Retain LRCLIB timing attribution and the notice that online text is not stored in iBroadcast. This is not an open Details-tab capture. |
| [S04 album-details.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/album-details.png) | Album hero and track list with compact Play, shuffle icon, Queue, Edit and More; album background is collapsed. | use; ch. 08 | Useful replacement for the old hero; the closed More menu does not illustrate its entries. |
| [S05 first-setup-playback.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/first-setup-playback.png) | First setup Playback step with Premium Original selected, Gapless unchecked and explicit Save and continue. | use; ch. 16, ch. 43, ch. 45; N01 | Illustrates a Premium profile and unchanged optional Gapless. It does not establish a new default or show a Free-account quality picker. |
| [S06 album-artists.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/album-artists.png) | Album artists grid with Filters, fixed Name/Rating/Random controls and Continuous scroll. | use; ch. 05 | Random is browsing order. Do not caption this as starting random playback. |
| [S07 theme-menu.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/theme-menu.png) | Theme disclosure with Light/Dark/Auto, six built-in palettes and Amber Midnight under My themes. | use; ch. 44 | Shows a saved custom-theme choice, not the JSON import/editor preview or a seventh built-in palette. |
| [S08 album-background.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/album-background.png) | So (Remastered) album page with expanded attributed 1001 Albums background. | optional; ch. 08 | Keep Wikipedia contributor and CC BY-SA attribution. This is bundled 1001 Albums prose, not proof of a TheAudioDB lookup. |
| [S09 albums-list.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/albums-list.png) | Albums list with fixed sort controls, Year selected, Filters, Continuous scroll and compact row actions. | use; ch. 05, ch. 09 | Caption the actual selected order; no Random playback or additional downloads are shown. |
| [S10 overview-service-status.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/overview-service-status.png) | Overview with public operational service status, timestamps and visible account/collection information. | optional_privacy_review; ch. 07, ch. 10 | A capture-time service report does not establish account/track availability. Review account name and collection totals before choosing it over the earlier redacted image. |
| [S11 1001-albums.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/1001-albums.png) | 1001 Albums local results filtered to In your library, including Linked by you. | optional; ch. 11 | It is not a Not found capture. Change the proposed caption/state if used in place of figure-029. |
| [S12 1001-albums-link.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/1001-albums-link.png) | Choose an album dialog for a local 1001 Albums link, with an available candidate and Use this album. | use; ch. 11 | Shows a proposed local choice, not a completed iBroadcast mutation or complete-track verification. |
| [S13 album-1001-background.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/album-1001-background.png) | Logical Progression Level 1 album with attributed 1001 Albums background text. | optional; ch. 11 | Retain visible Wikipedia/CC BY-SA attribution. It is a background illustration rather than an additional new feature. |
| [S14 milkdrop-ribbon.png](https://github.com/cyberdeliaAI/tagcast/blob/440199a359fd2df2fd615e3222fb36afbc13427c/docs/screenshots/2026-11-13-1.9.0/milkdrop-ribbon.png) | Expanded Now playing with MilkDrop Ribbon selected and the shared transport/queue. | optional; ch. 17, ch. 18 | One effect example; it does not establish rotation, audio/hardware coverage, or replace the seven other effect examples. |

## Figure replacements and retained examples

The following decisions refer to IDs in the existing 1.7.0 figure manifest.
They are proposed changes for a future asset manifest, not edits to that manifest.

| Existing figure | Proposed treatment |
|---|---|
| figure-002, chapter 5 | Prefer S06 to introduce the current Album artists workspace; S09 also demonstrates Albums controls |
| figure-027, chapter 9 | Prefer S09 for fixed sorting plus Continuous scroll; caption Year selected accurately |
| figure-003, chapter 8 | Prefer S04 for the current compact hero; S08 is a separate optional expanded background example |
| figure-024, chapter 13 | Prefer S03 for current queue playback; add G01 in N02 for the panel-specific view |
| figure-028, chapter 10 | S10 is optional after privacy review; keeping the earlier redacted image avoids any need for fresh personal-data disclosure |
| figure-029/030, chapter 11 | S12 can replace the chooser example; S11 shows In your library, so retain the earlier Not found example or change the new caption explicitly. S13 is optional |
| figure-034, chapter 17 | S14 is an optional Ribbon replacement. Keep the other seven effects and useful historical examples |
| figure-026, chapter 31 | S03 can refresh the lyrics example, with attribution and display-only meaning retained |
| figure-040/041, chapter 30 | Keep the genuinely confirmed composer result in figure-040. Prefer S02 for the current Checking/history example; decide whether figure-041 remains after layout review |
| figure-023, chapter 44 | Keep the existing theme-editor example where useful and label its age. S07 supplements it with the current menu/custom-theme example |

Keep the existing CD/Mini Player, metadata/artwork review, CSV matching, lyrics
import, cleanup/year/trash, merge/split, upload/download review and narrow-window
examples unless a specific changed control makes one misleading. Never relabel
an older capture as 1.9.0. Keep Reviews, Ready, Saving, Checking and Confirmed
visibly distinct. No complete screenshot refresh is required.

## Remaining capture opportunities

The first four fill gaps for the proposed illustrated new topics. They are not
prerequisites for this change report, and a maintainer may approve text plus
existing labelled examples instead. No captures or account operations are started.

| ID | Priority and state | What it should explain |
|---|---|---|
| G01 | Main gap: right-hand Details tab open, with Album/Track sections and both tabs visible | Details follows the queued track while browsing another album; loaded/unknown values and read-only controls. A second empty/restored view is optional |
| G02 | Main gap: Compare track list after an explicit MusicBrainz search | Search fields, edition choices and identity clues; opening alone makes no provider request |
| G03 | Main gap: a chosen reference with selected title/artist choices and optional manual pairing | Positional differences, unknowns, repeated positions and the separate Open corrections in editor action |
| G04 | Main gap: comparison choices in the ordinary editable draft or Before/After review | Only chosen fields enter review; nothing has been sent. An existing review image can cover unchanged save mechanics |
| G05 | Optional: downloading and downloaded/verified update states | Progress versus Restart and install; playback may continue during download. Use a clearly labelled controlled example when no newer public release is available |
| G06 | Optional: native install confirmation or safe-finishing/postponed state | Additional consent, Keep Tagcast open and waiting for accepted writes; no need to perform a real installation |
| G07 | Optional: current narrow workspace and First setup Lyrics/Workspace step | Mobile layout and provider consent, without replacing useful historical mobile/Settings captures merely for the version badge |

Use approved disposable/demo data for any future capture. Do not create real
iBroadcast writes, downloads, uploads or software installations just to obtain
an illustration. Preserve attribution; review account names and collection totals
before choosing an unredacted view. Any later crop/redaction must be a documented
derivative with its own hash, leaving the original intact. S01 already serves its
maintainer-confirmed illustrative purpose and is not a missing screenshot.

## Editorial decisions before a future edition

1. Approve the change IDs, including whether N01-N04 become separate topics.
   Resolve E01 as a correction in the future copy only.
2. Choose the proposed figure replacements and whether G01-G04 will be captured
   or covered with text/retained examples. S10 needs a deliberate privacy choice.
3. Follow the current canonical Wiki task owners and exact released English labels.
   Do not convert Wiki restructuring or translated captions into new feature claims.
4. Keep known limits: unsigned Windows/manual Windows updates, experimental
   off-by-default Gapless, unverified duplicate-position playlist append, uncertain
   write handling and the first subsequent signed upgrade-chain validation gate.
5. After approval, create a separate 1.9.0 content/asset snapshot and validate its
   layout, links, provenance and reproducible outputs. The current renderer targets
   the fixed reference edition; version selection is separate future implementation
   work, not part of this report. Do not reset the 1.7.0 layout or visual baselines.
6. Publication would require a separately approved PDF/checksum/source-manifest
   bundle and Wiki page change. This report grants no publication permission.

The user-confirmed S01 purpose has been incorporated. No unresolved clarification
prevents reviewing the proposal; screenshot choices and future content remain
editorial decisions. No later PDF page count or document publication date is assumed.
