"""Current 1.7.0 chapter additions to the illustrated-manual layout."""

def revise(title, lead=None):
    pg=next(pg for pg in pages if pg['title']==title)
    pg['blocks']=[]
    if lead:pg['lead']=lead
    return pg['blocks']

def extra(group,title,lead,slug):
    return page(group,title,lead,slug)

b=revise('Play music and manage the queue')
fig(b,INTERFACE+'now-playing-lyrics-queue.png','1.7.0: listening page, lyrics, queue and compact controls share one player.',maxh=252)
paras(b,'<b>Play album</b> and a chosen track replace the queue. <b>Shuffle album</b> and <b>Shuffle playlist</b> randomise playback without changing stored order. <b>Add to queue</b> appends; <b>Play next</b> fills Up next before the regular queue. Adding to an empty queue can start playback.')
paras(b,'Click the selected queue position to jump there. Remove one position with its row control; removing another position keeps current audio intact. Repeat cycles Off, Queue and Track. <b>Clear queue &amp; stop</b> removes the remembered local queue. <b>Save as playlist</b> reviews a native track list rather than saving an elapsed playback position.')
b.extend(note('The local queue is remembered','Since 1.5.5, account-specific queue order, repeated occurrences, Up next, current selection, Repeat and Shuffle are restored in the same browser/desktop profile and local address. Restoration never starts audio and does not restore elapsed time. Missing tracks are omitted; browser storage and the 10,000-entry limit apply. Clearing site data removes this recovery.'))
paras(b,'Queue synchronisation has its own opt-in ownership and takes priority while active. Local recovery is not a guarantee that a queue exists on another device.','small')

b=revise('Expanded Now playing and CD view')
fig(b,INTERFACE+'fullscreen-cd-lyrics.png','1.7.0: Cover / CD switches the presentation; playback and the queue remain shared.',maxh=290)
steps(b,['Choose Fullscreen or In app window under <b>Settings &gt; Playback &gt; Now playing view</b>. The choice applies when the expanded view next opens.',
         'Open the expanded-view icon from the compact player. Escape or its exit control returns to browsing.',
         'Choose <b>CD</b> in <b>Cover / CD</b>. The sleeve stays upright while the printed disc turns partly outside it. Choose <b>Cover</b> to return; the remembered choice is independent of fullscreen mode.'])
paras(b,'Lyrics works beside either presentation. The disc stops on pause/buffering and resumes from its angle; reduced motion keeps it still. Artwork-derived backgrounds respect Light/Dark appearance. Switching the view does not restart audio.')

b=revise('Lyrics that follow the music')
fig(b,INTERFACE+'fullscreen-cover-lyrics.png','1.7.0: LRCLIB line-synchronised display with provider attribution; no native save is performed.',maxh=277)
paras(b,'Open <b>Now playing</b> or expanded <b>Lyrics</b>. Choose native-only, iBroadcast-first with Unison/LRCLIB fallback, or Unison/LRCLIB-first with native fallback in <b>Settings &gt; Playback &gt; Now playing lyrics</b>. Native-only remains the default.')
paras(b,'Public lookup runs only while a listening-page/expanded lyrics view is visible and an online mode is enabled. Unison has priority for usable text, with LRCLIB fallback when enabled. Ordinary line timing highlights a line; supported word/segment timing adds a moving underline. Provider coverage and timing are imperfect.')
paras(b,'Manual scrolling stops following; use <b>Follow</b> to rejoin. Seeking, pause and compatible Gapless use the same player clock. Online results remain temporary and are not automatically saved. The provider receives identifying music metadata, not audio or iBroadcast credentials. Closing/hiding the view stops new lookups.','small')

b=revise('About this edition','An illustrated guide to the published Tagcast 1.7.0 release.')
paras(b,'Prepared on <b>11 November 2026</b> for the published <b>v1.7.0</b> release (release commit <b>a2493c8</b>). It combines the current user guide with the maintainer\'s November captures and selected older illustrations where no replacement is needed. Source revisions and image provenance are recorded with this edition.')
paras(b,'Current text describes 1.7.0. Captions identify earlier-interface and development examples; their counts and metadata belong to the pictured library. A draft, reviewed choice, running operation and confirmed result are different states. Images are illustrations, not additional test evidence or promises of universal provider/hardware compatibility.')
h(b,'Online companion')
paras(b,'<link href="https://tagcast.app/" color="#276b7d">tagcast.app</link> - product overview, current downloads and themes.<br/>'
        '<link href="https://github.com/cyberdeliaAI/tagcast/wiki" color="#276b7d">Tagcast Wiki</link> - task-by-task detail and later corrections.<br/>'
        '<link href="https://github.com/cyberdeliaAI/tagcast/releases/tag/v1.7.0" color="#276b7d">Tagcast 1.7.0 release</link> - actual platform packages and checksums.<br/>'
        '<link href="https://help.ibroadcast.com/" color="#276b7d">iBroadcast Help</link> - service/account behaviour.<br/>'
        '<link href="https://status.ibroadcast.com/" color="#276b7d">iBroadcast Status</link> - global service reports.')
h(b,'Credits and limitations')
paras(b,'Tagcast is an independent open-source project. iBroadcast, provider names, artwork and displayed lyrics belong to their respective owners. LRCLIB/TheAudioDB and other source credits remain visible. The Ellington background excerpt is adapted from Wikipedia contributors under CC BY-SA 4.0; that text licence is separate from Tagcast\'s MIT code. Theme attribution stays in the theme collection.','small')
paras(b,'Known release limits: playlist append with existing duplicate positions remains unverified (F2-02); physical Linux Wayland testing and Windows code signing remain incomplete; every audio/hardware combination cannot be certified. This manual makes no account writes and changes no release tags.','small')

b=extra('GET STARTED','Close and restart safely','Keep accepted changes visible until their checks finish.','Getting-started#closing-and-restarting-safely')
steps(b,['Quit or close the desktop app normally. Since 1.7.0, playback pauses and interruptible work stops while accepted changes, read-back and required local storage finish.',
         'If this takes time, the <b>Finishing Tagcast</b> window remains visible. A second launch brings that window forward; it does not create another backend or resend a save.',
         'If offered, <b>Keep Tagcast open</b> returns to the same session and drafts. Accepted checks continue, but playback, transfers and Cleanup remain stopped until you explicitly act.',
         'Wait for the owned backend to finish before replacing the app. Source/CLI users stop their server with Ctrl+C and wait. A desktop window leaves a compatible server it only reused running.'])
b.extend(note('Do not force a critical save to finish','There is no blanket deadline that kills an accepted remote mutation. Files already sent may still arrive. If progress genuinely stalls, retain the exact phase/message and inspect the result before trying a new mutation.'))
paras(b,'Closing a browser tab does not stop its Python server. The same no-blind-retry rule applies after an interrupted or uncertain operation. An ordinary restart can restore the bounded local queue but never automatically resumes audio or transfers.')

b=extra('BROWSE','Continuous scroll and Random order','Explore a large shelf without extra page-by-page refreshes.','Browsing-and-discovery#continuous-scroll')
fig(b,INTERFACE+'albums-continuous-random.png','1.7.0: browsing order, continuous loading and playback are separate controls.',maxh=270)
paras(b,'Choose <b>Continuous scroll</b> in the page-size selector for supported album and artist shelves. More results appear near the bottom; <b>Show more</b> is the keyboard alternative. Tagcast renders nearby chunks while retaining the space of distant chunks. The main document scrolls normally.')
paras(b,'Search, filters and ordering reset revealed results. Back/Forward restores revealed scope and scroll position after visiting an album. Choosing a numeric page size returns to pagination. Tracks, favourite artists/tracks, Recently played and the bounded Decades sample retain their own pagination.')
paras(b,'<b>Random order</b> reshuffles the complete matching album shelf, across pages, without starting music or changing the queue. Click again for a new order. It preserves the search/filter, returns to the beginning and works with continuous scroll. <b>Play random album</b> starts an album; <b>Shuffle album</b> changes its playback order.','small')
b.extend(note('Selection is the loaded scope','Select loaded albums does not select every matching album. Newly loaded cards are not automatically selected. Every tag, trash or metadata operation still requires its own review.'))

b=extra('BROWSE','Use the cache and refresh deliberately','Read-only browsing remains useful during a temporary library-service outage.','Browsing-and-discovery#cached-browsing-and-library-refresh')
paras(b,'Since 1.7.0, ordinary category/page requests, favourites, tags and history restoration use the valid, already loaded account library. They do not ask iBroadcast for status on every browse action. Switching or disconnecting accounts invalidates inappropriate cached state.')
paras(b,'Use <b>Reload library</b> for changes made elsewhere. Explicit refresh, fresh checks before remote writes and read-back after successful or uncertain writes are retained. A cached view is not proof that an outstanding mutation succeeded.')
fig(b,CURRENT+'overview-redacted.png','1.7.0: Overview with the maintainer\'s supplied account redaction retained. Global service status is separate from this account\'s connection.',maxh=275)
b.extend(note('An outage has boundaries','A loaded snapshot can keep browsing working, but cannot make streaming, provider lookups or remote saves work offline. Pending checks are not confirmations; failed read-back leaves the outcome unconfirmed.'))

b=extra('BROWSE','1001 Albums and local matching','Discovery compares the loaded metadata, never your audio.','1001-Albums')
fig(b,FINAL+'1001-not-found.png','1.7.0: Not found reference entries. The header\'s Checking saves indicator is a separate operation.',maxh=205)
fig(b,FINAL+'1001-manual-match.png','1.7.0: candidate editions before a local link is selected; this does not edit music metadata.',maxh=205)
paras(b,'Enable 1001 Albums in Discovery, then start <b>Analyse my library</b> explicitly. Filter found, possible or missing entries and use decade/year controls. A manual <b>Choose album</b> / <b>Use this album</b> saves only a local link. Check identity and edition; the result does not prove every track is present. Background excerpts retain their source and licence links.','small')

b=extra('BROWSE','A narrow window','The same interface adapts to a smaller workspace.','Album-details')
mobile=figure(FINAL+'album-mobile.png','1.7.0 maintainer capture: narrow Light album layout; complete original frame.',maxh=460,width=222)
right=[p('Cover and controls stay readable','h2'),p('The mobile-width album page stacks its cover above the title, artist, metadata and actions. The cover fills the available width. The navigation menu replaces the full desktop sidebar.'),p('Use the breadcrumb or Back to restore your browse context. Dialogs keep their own close/review controls; Back does not close an editor.'),p('On a narrow Tracks table, focus Track search results and use Left/Right to scroll. Touch devices keep row actions available.'),p('Light/Dark/Auto, palette and language remain independent choices. Native window borders and output controls can differ by platform.','small')]
t=Table([[mobile,right]],colWidths=[236,CW-236],hAlign='LEFT');t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),14),('RIGHTPADDING',(1,0),(1,0),0)]));b.append(t)

def visual_grid(names):
    cells=[]
    for stem,label in names:
        blocks=[p(label,'h2')]
        blocks.extend(figure('2026-11-11-visualizations/'+stem+'.png','1.7.0 - full-frame example.',maxh=152,width=(CW-18)/2))
        cells.append(blocks)
    t=Table([cells[:2],cells[2:]],colWidths=[CW/2,CW/2]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),3)]));return t

b=extra('LISTEN','Eight music visualizations','Optional local effects; no provider or account mutation is needed.','Playback-and-queue#eight-optional-music-visualizations')
paras(b,'Visualizations are <b>off by default</b>. Choose one in expanded Now playing, or select <b>Random - changes every 30 seconds</b>. These are eight distinct effects, rather than repeated screenshots of different tracks.')
b.append(visual_grid([('milkdrop-aurora','MilkDrop - Aurora'),('milkdrop-orbit','MilkDrop - Orbit'),('milkdrop-ribbons','MilkDrop - Ribbons'),('led-spectrum','Retro - LED spectrum')]))
paras(b,'The same player and queue continue. Cover/CD remains available when the visualizations are off. Still images illustrate appearance; they do not prove real-time rotation or hardware performance.','small')

b=extra('LISTEN','Visualization controls and rotation','Keep a fixed effect or use a shuffled cycle through all eight.','Playback-and-queue#eight-optional-music-visualizations')
b.append(visual_grid([('oscilloscope','Retro - Oscilloscope'),('neon-ring','Spectrum - Neon ring'),('starfield','Space - Starfield'),('waterfall','Spectrum - Waterfall')]))
paras(b,'Random changes after 30 seconds of visible playback and gives every effect a turn before repeating. Hidden or paused playback does not spend the visible-playback interval. Choose a fixed effect to leave the cycle. Lyrics can remain beside a visualization.')
paras(b,'Effects depend on the browser/desktop audio-analysis and graphics support. MilkDrop-style effects use the bundled local renderer; unsupported environments can have limits. Appearance choices do not change stream quality or save music metadata. Respect reduced-motion settings and use Off when a visual effect is not wanted.','small')

b=extra('LISTEN','Recover from an audio interruption','Recovery follows the same queue occurrence and your latest playback intent.','Playback-and-queue#playback-error-recovery')
paras(b,'In 1.7.0, a recoverable temporary network failure permits one automatic source reload for the same track occurrence and streaming quality. Track position, queue and listening-history watch are retained. A later Pause or seek is respected; Mini Player and system controls use the same player.')
b.append(table([['State','What it means'],['Temporary network interruption','One controlled source reload can recover; it is not an endless retry loop.'],['Recovery failed','Playback stops visibly. Inspect the message and press Play explicitly when ready.'],['Permission, certificate, unavailable track or decode error','Not treated as a transient network problem. Fix the stated cause.'],['Unsupported Original format','The existing labelled MP3 128 kbps fallback can apply; a network/sign-in error does not silently lower quality.']],[.36,.64]))
paras(b,'Gapless owns its own fallback; the ordinary player does not start a competing recovery. Stopping, changing track/account/library or beginning shutdown cancels stale recovery. Buffering is not counted as listening, and uncertain play-reporting writes are not resent. Keep Tagcast open during shutdown does not restart interrupted audio.')

b=extra('EDIT METADATA','Follow a checked save','A completed metadata save and an artwork save in progress are different examples.','Saving-and-history')
fig(b,FINAL+'composer-confirmed.png','1.7.0: track composer labels and the toast report 37 saved records.',maxh=232)
fig(b,FINAL+'artwork-saving.png','1.7.0: a separate artwork job is still saving disc 2 of 2. This frame is not final confirmation.',maxh=190)
paras(b,'Watch the explicit result and Change history. Read-back can continue after the request was accepted. Do not repeat an action merely because a progress indicator remains. A lost response is neither confirmed failure nor success; accepted writes are checked rather than retried.','small')

b=extra('LYRICS','Review linked lyrics separately','Native lyrics have their own review, save and uncertainty rules.','Importing-lyrics')
fig(b,CURRENT+'lyrics-import-review.png','1.7.0: linked tracks are Ready for the separate lyrics decision; no completed save is shown.',maxh=270)
paras(b,'Review only linked tracks. Before/After shows the current native text and proposed ordinary text. Existing lyrics stay unless you explicitly choose replacement for that track. Timing markers are removed for native saves; the online timed display is separate.')
paras(b,'Save reviewed lyrics proceeds one track at a time, preserves unrelated native userdata and reads back each accepted write. Stop, conflicts, errors or unconfirmed outcomes leave later tracks unsent. No automatic retry is performed. Source/account/library changes invalidate stale work.')
b.extend(note('Premium and cache boundaries','Free accounts can read known/native text and explicitly search supported public lyrics, but cannot save. A cached text is not permission to overwrite newer native lyrics; review/save still use fresh guards. The 1.7.0 review optimization avoids redundant reads without removing those checks.'))

b=extra('CLEAN UP','Split an album deliberately','Move a reviewed subset into a new album without rewriting its track metadata.','Split-albums')
fig(b,'2026-11-07-album-split/split-selection.png','Earlier 1.6.5 capture: inspect selected and retained tracks before splitting. Current text describes 1.7.0.',maxh=270)
steps(b,['Choose <b>More &gt; Split album</b> on one native disc with 2-500 active tracks. Combine sets must be off; unsupported additional album credits block the operation.',
         'Select a proper subset, check destination metadata and review the complete source/destination membership. Proposals never select tracks automatically.',
         'Confirm the reviewed split once. Creation and movement are separate remote steps; both albums are read back. Track metadata and numbers are preserved unless the reviewed operation explicitly says otherwise.'])
b.extend(note('A split is not transactional','An empty or partial destination can remain after an uncertain creation/movement. Do not repeat blindly. Inspect both albums and the retained report; there is no metadata Undo for this operation.'))

b=extra('ORGANISE','Playlist positions and uncertain results','Appending and exact-position editing have different contracts.','Playlists#appending-and-duplicate-positions')
fig(b,CURRENT+'playlist-order.png','1.7.0: original positions with zero changes; Save order is disabled until a change is made.',maxh=258)
paras(b,'Use Reorder tracks for an exact-position change. Drag a handle, use Up/Down or Move to position, inspect the complete resulting order and save once. Search and pagination must not hide which occurrence you selected. This workflow retains repeated and unavailable positions; changing playlist order does not change the current play queue.')
b.extend(note('Append and existing duplicates - known limit','The exact iBroadcast append behaviour for a destination containing intentional repeated positions remains unverified (F2-02). Do not assume append preserves them. Create/append reduce the selected incoming IDs to their first occurrence; this is separate from exact-position reorder/replacement.'))
paras(b,'An uncertain creation or append is checked rather than automatically retried. Inspect the actual list before preparing another mutation. A matching playlist name alone does not prove that a particular creation succeeded. A failed read-back leaves an unknown outcome, not proof of failure.','small')

b=revise('Download album copies','Review the source, destination and selection before creating separate local files.')
fig(b,CURRENT+'download-review.png','1.7.0: reviewed album/source/destination; the page says nothing has been downloaded yet.',maxh=277)
steps(b,['Choose More > Download album, or select album cards and Download. A displayed set includes every disc.',
         'Check albums, destination folder and options. The folder is on the computer running Tagcast, even when the interface is in another browser.',
         'Choose Review download to inspect counts and example paths. No audio is fetched yet.',
         'Choose Start downloads explicitly. Read completed, skipped and fallback notes. Stop keeps completed files and eligible partials; reopening never resumes automatically.'])

b=extra('TRANSFER MUSIC','Download sources and file integrity','Choose which bytes you want, and keep the verification record.','Downloads#quality-and-embedded-metadata')
b.append(table([['Source','What is downloaded'],['Original via download service','Premium default. For current embedded tags, enable Download Updated Metadata in iBroadcast. The service decides which fields it embeds.'],['Original upload via streaming','Uploaded bytes/tags; later library metadata edits may be absent. This fallback is labelled.'],['Converted streaming MP3','The selected offered quality; Free accounts use 128 kbps MP3.']],[.35,.65]))
paras(b,'Tagcast creates separate files. It does not retag, adopt or overwrite existing unverified music. Changing source does not replace completed files. Default naming uses artist/album/year and disc-track title, with safe filenames and collision handling.')
b.extend(note('Keep the hidden integrity manifest','Preserve .ibfetch.json beside downloaded music. Unverified or locally modified files are not silently trusted. Explicit checksum checks and eligible streaming partial-resume use this record. Completed files remain after stopping.'))
paras(b,'One worker is the default. Extra workers compete with playback for network/disk capacity. Options persist, but transfer selection/progress is session-local. Reselect and review after restart to reuse verified completed files or eligible partials. For individual tracks, playlists and advanced CLI filters, use the linked ibfetch tool. Metadata JSON/CSV export is separate.','small')

b=extra('ORGANISE','Favourites and native ratings','Album/artist hearts and native track ratings are stored in different places.','Ratings-and-favourites')
fig(b,CURRENT+'favourites-light.png','1.7.0: Favourites in Light appearance; the tabs distinguish track, album and artist collections.',maxh=270)
b.append(table([['Control','Storage / effect'],['Album or artist heart','Local account-specific Tagcast favourite; separate from native stars.'],['Album/artist stars','Native iBroadcast rating, subject to its account/features.'],['Track heart / thumbs-down','Native track rating; independent of playlist membership.']],[.37,.63]))
paras(b,'Use Favourites to browse the appropriate tab, search and open or play results. Changing a heart or rating does not remove music or alter playlist order. Check the visible state after an uncertain operation rather than repeatedly clicking. Local favourites belong to the active account and settings/profile storage.','small')

# Add current integrity and compatibility notes to otherwise unchanged chapters.
pg=next(pg for pg in pages if pg['title']=='Settings reference')
pg['blocks'].append(p('Since 1.7.0, a settings submission is validated before changes are applied. Invalid values or a persistence failure leave the existing configuration intact; sign-in scope and runtime services must remain consistent. Read the error and correct the form before retrying.','small'))
pg=next(pg for pg in pages if pg['title']=='Storage, privacy and safe recovery')
pg['blocks'].append(p('The standalone browser interface now sends a Content Security Policy, matching the desktop security intent without allowing arbitrary inline/evaluated JavaScript. Keep the existing local-server protections; an unsupported browser feature is not a reason to disable security headers.','small'))

# Keep groups together; place the reference/edition chapter last.
groups=['GET STARTED','BROWSE','LISTEN','ORGANISE','EDIT METADATA','LYRICS','CLEAN UP','TRANSFER MUSIC','PERSONALISE','YOUR DATA','REFERENCE']
pages.sort(key=lambda pg:(groups.index(pg['group']),pg['title']=='About this edition'))
