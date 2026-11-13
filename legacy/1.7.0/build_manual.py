from pathlib import Path
from html import escape
import re, json, hashlib
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Image, Table, TableStyle, PageBreak, KeepTogether, Flowable)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT=Path('/Users/cyberdelia/Documents/GitHub/tagcast/.worktrees/manual-1.7.0')
WORKSPACE=ROOT.parents[1]
TMP=WORKSPACE/'tmp/pdfs/manual-1.7.0'
OUT=WORKSPACE/'output/pdf/Tagcast-1.7.0-User-Manual.pdf'
SHOTS=ROOT/'docs/screenshots'
W,H=595.276,841.89
M=48; CW=W-2*M
INK=colors.HexColor('#17313e'); MUTED=colors.HexColor('#526a77')
TEAL=colors.HexColor('#276b7d'); PALE=colors.HexColor('#eaf3f6')
LINE=colors.HexColor('#cfdee4'); AMBER=colors.HexColor('#a86a20')
FONTROOT=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Guide','Arial.ttf'),('Guide-Bold','Arial Bold.ttf'),('Guide-Italic','Arial Italic.ttf'),('Guide-BoldItalic','Arial Bold Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTROOT/file)))
pdfmetrics.registerFontFamily('Guide',normal='Guide',bold='Guide-Bold',italic='Guide-Italic',boldItalic='Guide-BoldItalic')
styles={
 'body':ParagraphStyle('body',fontName='Guide',fontSize=11,leading=15.8,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Guide',fontSize=9.7,leading=13.7,textColor=MUTED,spaceAfter=7),
 'caption':ParagraphStyle('caption',fontName='Guide-Italic',fontSize=8.7,leading=11.8,textColor=MUTED,spaceBefore=6,spaceAfter=12),
 'title':ParagraphStyle('title',fontName='Guide-Bold',fontSize=26,leading=30,textColor=INK,spaceAfter=9),
 'lead':ParagraphStyle('lead',fontName='Guide',fontSize=11.8,leading=16.7,textColor=MUTED,spaceAfter=15),
 'h2':ParagraphStyle('h2',fontName='Guide-Bold',fontSize=12.5,leading=17,textColor=TEAL,spaceBefore=9,spaceAfter=6,keepWithNext=True),
 'kicker':ParagraphStyle('kicker',fontName='Guide-Bold',fontSize=8.2,leading=12,textColor=TEAL,spaceAfter=10,charSpace=1.1),
 'cell':ParagraphStyle('cell',fontName='Guide',fontSize=9.7,leading=13.8,textColor=INK),
 'cellhead':ParagraphStyle('cellhead',fontName='Guide-Bold',fontSize=9.7,leading=13.8,textColor=INK),
 'note':ParagraphStyle('note',fontName='Guide',fontSize=9.4,leading=13.5,textColor=INK),
 'toc':ParagraphStyle('toc',fontName='Guide',fontSize=9.5,leading=12.6,textColor=INK),
}

def normalise(t):
    return t.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ').replace('\u00a0',' ')
def p(t,kind='body'):
    return Paragraph(normalise(t),styles[kind])
def link(slug,label=None):
    return f'<link href="https://github.com/cyberdeliaAI/tagcast/wiki/{slug}" color="#276b7d">{escape(label or "Online guide")}</link>'
def table(rows,widths,headers=True):
    data=[[p(str(v),'cellhead' if headers and i==0 else 'cell') for v in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=[CW*w for w in widths],hAlign='LEFT')
    rules=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,-1),.45,LINE)]
    if headers:rules += [('BACKGROUND',(0,0),(-1,0),PALE)]
    t.setStyle(TableStyle(rules));return t
def note(title,text):
    t=Table([[p(f'<b>{title}</b><br/>{text}','note')]],colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PALE),('BOX',(0,0),(-1,-1),.4,LINE),('LINEBEFORE',(0,0),(0,-1),3,TEAL),('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    return [Spacer(1,5),t,Spacer(1,10)]

CURRENT="2026-11-11-guide/"
INTERFACE="2026-11-11-interface/"
FINAL="2026-11-11-manual/"
FIGURES={
 "connect-ibroadcast.png":(FINAL+"connect-ibroadcast.png","1.7.0: Tagcast connection dialog; sign-in starts only after the explicit button."),
 "2026-11-02-readme/album-storm-front.png":(INTERFACE+"album-full-house.png","1.7.0: album actions, native tags and attributed album information."),
 "2026-11-03-cd-view/cd-view.png":(INTERFACE+"fullscreen-cd-lyrics.png","1.7.0: upright sleeve, printed disc and LRCLIB lyrics; attribution stays visible."),
 "2026-10-26-mini-player/mini-player.png":(CURRENT+"mini-player.png","1.7.0: native Mini Player; Pin and return to the main window stay separate."),
 "tag-manager.png":(FINAL+"tag-manager.png","1.7.0: tag assignments with Keep as is; no changes are selected in this capture."),
 "2026-10-22/playlist-details.png":(CURRENT+"playlist-details.png","1.7.0: playlist detail with playback, edit and reorder actions."),
 "2026-10-22/deezer-import-columns.png":(CURRENT+"playlist-import-columns.png","1.7.0: CSV column mapping; these are local records, not a fetched URL result."),
 "2026-10-22/deezer-import-choose-track.png":(CURRENT+"playlist-import-choose.png","1.7.0: compare recording/edition differences before a manual match."),
 "2026-10-23/editor-album.jpg":(INTERFACE+"editor-album.png","1.7.0: album draft with online suggestions and additional artist credits."),
 "2026-10-23/editor-tracks.jpg":(CURRENT+"editor-tracks.png","1.7.0: selected track fields remain part of the album's shared metadata review."),
 "metadata-review.png":(FINAL+"composer-review.png","1.7.0: proposed composer change on 37 tracks; no save is confirmed by this review."),
 "artwork-compare.png":(CURRENT+"album-cover-review.png","1.7.0: current/proposed album covers. The explicit Save control is further down the dialog."),
 "2026-11-03-cd-view/cd-view-lyrics.png":(INTERFACE+"fullscreen-cover-lyrics.png","1.7.0: expanded cover with LRCLIB line timing; online display does not save lyrics."),
 "2026-10-23/lyrics-import.jpg":(CURRENT+"lyrics-import-matching.png","1.7.0: match LRC/TXT files to album tracks; this is preparation, not saving."),
 "2026-10-31-uploads/upload-progress.png":(CURRENT+"upload-review.png","1.7.0: reviewed files are Ready to upload; no transfer has started in this image."),
}
def resolve_figure(rel,caption,crop):
    key=str(rel)
    if key in FIGURES:
        source,caption=FIGURES[key];return source,caption,None
    basename=Path(key).name
    for prefix,target,description in [
      ("browse-",INTERFACE+"albums-continuous-random.png","1.7.0: Albums with Continuous scroll and Random order."),
      ("language-",CURRENT+"settings-interface.png","1.7.0: Interface settings; language and library-banner preferences."),
      ("playback-",CURRENT+"settings-playback.png","1.7.0: lower Playback settings for streaming/history and device queues; the Gapless switch is above this view."),
      ("appearance-",CURRENT+"settings-appearance.png","1.7.0: custom theme editor; draft preview is separate from the applied theme.")]:
        if basename.startswith(prefix):return target,description,None
    if crop:caption+=" Cropped detail from the original screenshot."
    return rel,caption,crop

used_images=[]
def figure(rel,caption,maxh=285,crop=None,width=CW):
    rel,caption,crop=resolve_figure(rel,caption,crop)
    source=Path(rel) if Path(rel).is_absolute() else SHOTS/rel
    im=PILImage.open(source).convert('RGB')
    if crop:
        # Crop only the documented UI region; the source screenshot stays untouched.
        iw,ih=im.size;im=im.crop(tuple(round(v*(iw if i%2==0 else ih)) for i,v in enumerate(crop)))
    im.thumbnail((2400,2100),PILImage.Resampling.LANCZOS)
    target=TMP/(hashlib.sha256((str(source)+str(crop)).encode()).hexdigest()[:14]+'.jpg')
    im.save(target,quality=91,subsampling=0)
    iw,ih=im.size;scale=min(width/iw,(maxh*1.13)/ih)
    item=Image(str(target),width=iw*scale,height=ih*scale,hAlign='LEFT')
    used_images.append({'source':str(source.relative_to(ROOT)),'crop':crop,'caption':caption,'rendered':str(target),'original_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    item.manual_figure_info=used_images[-1]
    return [Spacer(1,3),item,p(caption,'caption')]

pages=[]
def page(group,title,lead,slug=None):
    blocks=[];pages.append({'group':group,'title':title,'lead':lead,'slug':slug,'blocks':blocks});return blocks
def paras(b,*ts):
    kind='body'
    if ts and ts[-1] in styles:
        kind=ts[-1];ts=ts[:-1]
    b.extend(p(t,kind) for t in ts)
def h(b,t):b.append(p(t,'h2'))
def steps(b,items):
    for n,t in enumerate(items,1):
        b.append(p(f'<b>{n}.</b>  {t}'))
def fig(b,*args,**kwargs):b.extend(figure(*args,**kwargs))

b=page('GET STARTED','Your first session','A short route from opening Tagcast to making one carefully reviewed change.','Getting-started')
paras(b,'Tagcast is a local metadata editor and music player for your own iBroadcast library. Use it to browse, listen, organise and correct metadata. It runs as a desktop app, or as a local Python server with the same interface in a browser.')
steps(b,[
 'Install the package for your computer, extract it completely and open Tagcast. The sample library is a preview; it is normal to see it before signing in.',
 'Choose <b>Connect iBroadcast</b>. Approve access on the official iBroadcast website, then leave Tagcast open while it loads your library.',
 'Open <b>Album artists</b> or <b>Albums</b>. Search, open an album and choose <b>Play album</b> to listen.',
 'For your first edit, choose <b>Edit</b>, change one field, open <b>Review draft</b> and inspect the before/after values. Only the final Save sends metadata.',
 'Wait for confirmation. <b>Checking</b> means verification is still running; a large library can take time. Continue browsing or listening while ordinary checks finish.'
])
b.extend(note('Before album edits','In iBroadcast, turn <b>Combine Multi-Disc Album Sets</b> off, then reload Tagcast. Tagcast groups compatible discs itself and needs their original records to save album changes.'))
paras(b,'Your original music files are not retagged. Explicit downloads create separate copies; explicit uploads read the existing embedded tags in your chosen files. Neither happens merely by browsing.')

b=page('GET STARTED','Install and update','Use a standalone download for everyday desktop use; Python is bundled.','Getting-started')
b.append(table([
 ['Computer','Download suffix','Open after extraction'],
 ['macOS Apple Silicon','macos-arm64.zip','Move Tagcast.app to Applications.'],
 ['macOS Intel','macos-x64.zip','Move Tagcast.app to Applications.'],
 ['Windows x64','windows-x64.zip','Run Tagcast.exe; keep its folder complete.'],
 ['Debian / Ubuntu','linux-amd64.deb','Install with sudo apt install ./package.deb.'],
 ['Linux x64','linux-x64.tar.gz','Run ./Tagcast in a graphical session.'],
],[.25,.27,.48]))
paras(b,'The complete package name starts with <b>tagcast-1.7.0-</b>. macOS requires 13 Ventura or newer; Linux requires glibc 2.35 or newer. Use the <link href="https://github.com/cyberdeliaAI/tagcast/releases" color="#276b7d">official Releases page</link>, rather than GitHub\'s source-code archive, for a standalone app.')
h(b,'Updating')
paras(b,'Quit the older app, extract the new download and replace the application while preserving your user settings. Tagcast checks for stable updates when enabled, but does not install them automatically. <b>Settings &gt; About &amp; updates</b> offers a manual check and the release link.')
h(b,'Homebrew and source use')
paras(b,'On macOS: <font name="Guide-Bold">brew install --cask cyberdeliaAI/apps/tagcast</font>. Later run <b>brew update</b>, then <b>brew upgrade --cask cyberdeliaAI/apps/tagcast</b>. The cask also provides <b>tagcast-cli --open</b>.',
 'For source use, Python 3.11+ is required. From the repository, <b>uv run --frozen tagcast --open</b> starts the browser interface. The supplied platform start scripts are another option.')
b.extend(note('Verify the download','Compare its SHA-256 with the accompanying checksum file. On macOS use <b>shasum -a 256 filename.zip</b>; on Linux use <b>sha256sum filename.tar.gz</b>; in PowerShell use <b>Get-FileHash .\\filename.zip -Algorithm SHA256</b>.'))
paras(b,'Official macOS distributions use Developer ID signing and Apple notarization. Check the selected release\'s notes and available assets; Windows signing is not yet active. Tagcast 1.7.0 is published. Windows code signing remains deferred; physical Wayland and every hardware/audio combination are not fully validated.','small')

b=page('GET STARTED','Connect your account','Your password stays on iBroadcast. No client ID, client secret or app registration is needed.','Connecting-to-iBroadcast')
steps(b,[
 'Choose <b>Connect iBroadcast</b> near the bottom of the sidebar, or <b>Demo · Connect</b> in the header.',
 'Choose <b>Sign in with iBroadcast</b>. The desktop app opens a dedicated authorization window; browser use opens the official website in your browser.',
 'Sign in, or use <b>Continue as</b>, and approve the requested permissions. Return to Tagcast and keep it open while approval is detected.',
 'Wait for <b>Loading library</b> to finish. Your own albums replace the demo and the connection indicator changes to <b>Live</b>.'
])
fig(b,'connect-ibroadcast.png','Earlier-interface detail: code sign-in. In 1.7.0, Sign in with iBroadcast is offered first; the browser link/code remains a fallback.',maxh=205,crop=(.27,.28,.73,.62))
paras(b,'If the authorization window cannot open, follow the displayed browser link and code. A successful authorization page still needs Tagcast to retrieve the result and load the library.',
 'Use <b>Reload library</b> for later changes made elsewhere. <b>Download everything again</b> in the connected dialog requests a fresh copy when the cache appears stale. A temporary connection failure does not by itself mean your authorization is lost.')
b.extend(note('Extra permissions are optional','Uploads and queue synchronisation request additional permission only when you enable them. Authorizing an upload permission never starts an upload. Existing custom client registrations remain supported.'))

b=page('BROWSE','Find your way around','The sidebar chooses a view; the header shows your location, Help, language and appearance.','Browsing-and-discovery')
fig(b,str(TMP/'browse-1.4.png'),'Tagcast 1.7.0, local demo, Ocean Light. Search, Filter and sort, page size and card/list controls work together.',maxh=310)
paras(b,'Tagcast starts on <b>Album artists</b>. Select an artist to see their albums, or open <b>Albums</b> for the whole collection. Search there by album title, artist or genre. Use <b>Tracks</b> when you know a song title, performer, album or composer.',
 '<b>Filter and sort</b> keeps its Show filter separate from its sorting choice. Grid/list and page size are independent. <b>Random album order</b> only rearranges browsing; <b>Play random album</b> chooses a complete matching album and starts it in ordinary track order.',
 'Back and Forward restore your previous browse view, including searches and pages. Album breadcrumbs return to the artist, genre, tag or other origin. On narrow windows, use the navigation menu. Row actions appear on hover or keyboard focus and remain available on touch.')

b=page('BROWSE','Choose the right view','These views organise the loaded library; they do not rename your metadata.','Browsing-and-discovery')
b.append(table([
 ['View','Use it for'],
 ['Album artists','Albums credited to a primary or additional album artist.'],
 ['Track artists / Composers','Albums containing at least one track by that performer or composer.'],
 ['Genres / Tags','Main and additional genre labels, or native iBroadcast tags. Tags are independent of genres.'],
 ['Release year / Decades','Track year, falling back to album year. Unknown years stay unknown. Decades offer a random album selection and Surprise me again.'],
 ['Tracks','Library-wide song search, including accent-insensitive matches. Results are capped at 1,000; this is not a complete export.'],
 ['Favourites','Separate Tracks, Albums and Album artists tabs. Storage rules differ; see the ratings page.'],
 ['Upload folders / Date uploaded','Optional views of original upload-path labels and stored upload days. Enable their sidebar shortcuts under Interface.'],
 ['Recently played','iBroadcast\'s recent-track list when play reporting is enabled; not a complete listening event log.'],
],[.34,.66]))
h(b,'Upload groups show albums')
paras(b,'Opening an upload folder or day shows matching <b>album cards</b>. One matching active track is enough to include an album. The card and Play action refer to the complete album/set, even if only some tracks were uploaded on that day or path.',
 'Upload paths are historical labels stored by iBroadcast. They do not open a local folder on this computer. They are also different from playlist folders. Date uploaded is independent of release year.')

b=page('BROWSE','Overview and discovery','Use library health as a starting point, then choose a specific reviewed action.','Browsing-and-discovery#overview-and-metadata-health')
h(b,'Overview')
paras(b,'Overview shows collection totals, formats, playing time, account information and existing iBroadcast settings. <b>Metadata health</b> links to missing metadata/artwork and <b>Clean up metadata</b>. Opening Overview does not start cleanup or change your library.',
 'The album totals can differ: Overview uses iBroadcast\'s native totals; sidebar and browser cards count Tagcast\'s displayed disc groups. Separate discs may count individually in iBroadcast.')
h(b,'Public service health')
paras(b,'<b>iBroadcast Service Status</b> covers Streaming, API Server, Play Queue, Artwork and Library Generation. Readable states accompany the indicators: <b>Operational</b>, <b>Degraded performance</b>, <b>Service disruption</b> and <b>Unknown / unavailable</b>. Open the details for any issue text.',
 'The panel checks about every five minutes while Overview is visible. Last successful retrieval, provider report time and stale/unavailable notices help you judge freshness. Stale information is not presented as confirmed current Operational status. A failed status-feed request does not prove iBroadcast is down.')
b.extend(note('Global status is not your account connection','An operational API can coexist with a disconnected Tagcast session. A global streaming report cannot establish whether one particular track will play. The official status-page link shows iBroadcast\'s own report.'))
h(b,'Optional discovery')
paras(b,'Enable <b>1001 Albums</b> in Settings &gt; Discovery, then explicitly choose <b>Analyse my library</b>. It compares your loaded metadata with a bundled reference; it does not buy or download music. Review uncertain matches manually.',
 'Artist biographies and album background information are separate opt-in TheAudioDB features for visited pages. Available bundled album text takes priority. Source attribution remains visible. Some text is available only in English.')

b=page('BROWSE','Read an album page','The album header combines identity, organisation and playback actions.','Album-details')
fig(b,'2026-11-02-readme/album-storm-front.png','Album-page example, captured 2 November 2026 in Apple Music Classic Dark (1.3.0). The main controls remain in 1.7.0.',maxh=302,crop=(.18,.045,1,.92))
paras(b,'The cover, album title, album artists, year and track totals describe the displayed album or disc set. Genre chips and native tags are distinct; <b>+ Tag</b> opens the tag manager. Stars and the heart have separate meanings.',
 '<b>Play album</b> replaces the queue with the album in disc/track order. <b>Shuffle album</b> replaces it with a mixed order. <b>Queue</b> offers append or Play next. <b>Add to playlist</b>, <b>Edit</b> and <b>More</b> open their own choices.',
 'Tagcast groups discs conservatively: matching title, album artists, year and upload-day set, with distinct disc numbers. Different editions, upload dates or repeated disc numbers may remain separate. An ampersand in a title is not itself a grouping barrier. Avoid merging merely because covers look alike.')

b=page('LISTEN','Play music and manage the queue','One player continues while you browse, organise or edit metadata.','Playback-and-queue')
b.append(table([
 ['Control','Result'],
 ['Play album / Play on a track','Replaces the queue; a chosen track starts that album from that point. Clicking the current track toggles pause/play.'],
 ['Shuffle album / Shuffle playlist','Starts a mixed queue without changing the stored album or playlist.'],
 ['Add to queue','Appends music. Adding to an empty queue starts playback.'],
 ['Play next','Adds to Up next in click order. These entries play before returning to the regular queue.'],
 ['Repeat','Cycles Off, Queue and Track. Track repeat applies on a natural ending.'],
 ['Cover / queue button','Opens the Now playing side panel. Select a position to jump to it.'],
 ['Save as playlist','Reviews saving the track list; it does not preserve the current playback position.'],
 ['Clear queue & stop','Stops playback and removes the complete temporary queue.'],
],[.35,.65]))
paras(b,'In the queue panel, hover/focus a row for its remove cross; touch devices show it directly. Removing a different position keeps current audio intact. Removing the current position moves to a retained neighbour. This changes queue positions, not library music or saved playlists.')
b.extend(note('The ordinary queue is temporary','Reloading the page or restarting clears the queue and position. Save its track list as a playlist before closing if you want to keep it. Queue synchronisation is a separate optional mode.'))

b=page('LISTEN','Expanded Now playing and CD view','Choose a focused cover view or the optional spinning disc, using the same playback controls.','Playback-and-queue#optional-cd-view')
fig(b,'2026-11-03-cd-view/cd-view.png','1.7.0 CD-view feature, captured in the maintainer\'s local test build on 3 November. Regular rectangular artwork remains the default.',maxh=312)
steps(b,[
 'Under <b>Settings &gt; Playback &gt; Now playing view</b>, choose <b>Fullscreen</b> or <b>In app window</b>. The choice applies the next time you open the expanded view.',
 'Use the expanded-view icon in the compact player. Escape or the close button returns to the library.',
 'Choose <b>CD view</b> beside Lyrics to switch artwork presentation, or use <b>Now playing artwork &gt; Spinning CD</b> in Settings. Select Album cover to return.'
])
paras(b,'The disc turns during playback, stops while paused or buffering and resumes from its angle. System reduced-motion preferences keep it still. The choice is remembered locally, independently of Fullscreen/In app window. <b>Lyrics</b> opens timed or plain lyrics beside either artwork style. The optional artwork-derived background is shared with the listening view.')

b=page('LISTEN','Mini Player, sound and quality','Keep compact playback visible, and choose the output and stream that suit your setup.','Playback-and-queue#desktop-mini-player')
fig(b,'2026-10-26-mini-player/mini-player.png','Desktop Mini Player with fictional sample track information, captured 26 October. Pin and Open Tagcast are the two upper-right controls.',maxh=184,width=465)
paras(b,'Open it from <b>View &gt; Open Mini Player</b>, <b>Cmd/Ctrl+Shift+M</b>, or expanded Now playing. It hides the main window. <b>Open Tagcast</b>, closing the Mini Player or returning to the main window restores the full interface. Playback uses the same engine. Pin keeps it above other windows where supported; Linux/Wayland does not offer Pin. Window size and Pin are remembered.')
h(b,'Output and volume')
paras(b,'Open <b>Sound</b> from the output/speaker-cabinet button for player volume, mute and available outputs. If a browser cannot change volume or select a device, use your system controls. This is not direct Sonos or Chromecast control.',
 'For AirPlay in the macOS Electron app, leave Tagcast on <b>System default</b> and choose the AirPlay device in <b>macOS Control Centre &gt; Sound</b>. This routes system audio, including other apps. Safari may offer its own route picker.')
h(b,'File format is not stream quality')
paras(b,'<b>Settings &gt; Playback &gt; Streaming quality</b> applies on the next track after Save. Free accounts use MP3 128 kbps. Premium adds other offered bitrates and Original. A FLAC upload may still be playing as MP3; read the File and Stream labels. If Original cannot play, Tagcast can try MP3 128 kbps once and labels the fallback.')

b=page('LISTEN','Experimental Gapless playback','For compatible consecutive album tracks, not a promise about every file or output.','Gapless-playback')
steps(b,[
 'Choose <b>Original file (Premium)</b> under Streaming quality and <b>Save changes</b>.',
 'Enable <b>Gapless playback for albums in order</b> in Settings &gt; Playback. It is off by default.',
 'Start a fresh ordered album with <b>Play album</b>. The time bar remains relative to the current track.'
])
h(b,'Supported path')
paras(b,'Original FLAC is the primary validated path. Compatible consecutive tracks share a continuous buffer without crossfading or removing silence. Sample rate, channels, bit depth and decoder block-size compatibility matter; large or unusual files may exceed the preparation limits.',
 'Starting can take longer because music is prepared first. Seeking close to the end can wait for the next track. Intentional recorded silence remains. Explicit Next/Previous are available but are not promised seamless transitions.')
b.extend(note('When ordinary playback is expected','Shuffle album, Random Album, playlists and active queue synchronisation use standard playback. Unsupported files/transitions, preparation limits or decoder failures fall back to ordinary playback. The player identifies the fallback; a pause at that boundary is possible.'))
h(b,'Keep expectations precise')
paras(b,'MP3 has a separate experimental path that depends on acceptable delay/padding metadata; real iBroadcast MP3 alignment is not universally established. Prefer Original FLAC when checking supported Gapless behaviour.',
 'Deterministic audio tests establish exact continuity for their measured inputs. They do not prove universal sample accuracy on every platform, physical output or album. Sleep/wake and output-device changes depend on the system. If an album has a reproducible problem, compare Gapless off and record the exact format, action and boundary.')

b=page('ORGANISE','Tags, ratings and favourites','Choose a tag for organisation, stars for native ratings, or local hearts for albums and artists.','Tags')
fig(b,'tag-manager.png','Earlier-interface detail: the tag manager shows assignment counts. Keep as is preserves partial membership; selection alone sends nothing.',maxh=218,crop=(.277,.22,.712,.817))
paras(b,'On an album, choose <b>+ Tag</b>; for a single track use its tag action. Choose <b>Add to all tracks</b>, <b>Remove from all tracks</b> or <b>Keep as is</b>, then <b>Review tag changes</b>. Confirm the exact labels and affected track count.',
 'For several albums, tick their cards and choose <b>Tag</b>. The review includes complete selected sets, including selections outside the current page/filter. Fully confirmed multi-album assignments deselect the reviewed albums; cancellation or uncertainty retains selection. New tag creates an empty native label. Renaming/deleting a tag has global scope; deleting its label keeps the music.')
b.append(table([
 ['Choice','Where it is saved'],
 ['Track heart / thumbs-down','Native iBroadcast rating: heart 5, dislike 1, clear 0. These are alternatives for the same rating.'],
 ['Album / artist stars','Native iBroadcast ratings; wait for confirmation.'],
 ['Album / album-artist heart','Local, account-specific Tagcast favourites on this computer. Independent of stars.'],
],[.37,.63]))
paras(b,'Favourites has separate Tracks, Albums and Album artists tabs. Local hearts survive restarts but do not sync to another computer. Archived tags cannot be added here; manage archiving in iBroadcast.','small')

b=page('ORGANISE','Playlists and folders','Play a saved list, change its contents, or organise references without removing music.','Playlists')
fig(b,'2026-10-22/playlist-details.png','Earlier development interface, 22 October. A playlist has its own Play, Shuffle, Edit and Reorder actions.',maxh=225,crop=(.18,.08,1,.9))
paras(b,'<b>Add to playlist</b> on an album includes its discs. A track\'s action adds just that track; <b>Save as playlist</b> in Now playing reviews the queue. Choose a new private playlist or an existing destination and confirm the review. Repeated selected track IDs are retained once in their first position for create/append operations.')
b.append(table([
 ['Goal','Use'],
 ['Rename or describe','Edit playlist; leave every track checked to save text only.'],
 ['Remove one occurrence','Row cross, then review. The library track remains.'],
 ['Remove several','Untick tracks in Edit playlist, then review the retained list.'],
 ['Reorder','Reorder tracks: drag a handle, use Up/Down or Move to position, then Save order.'],
 ['Organise folders','Create/rename a folder or add/remove references. Removing a reference keeps its playlist.'],
],[.3,.7]))
paras(b,'Search works across playlist pages. Reordering preserves repeated and unavailable positions and does not reorder the playing queue. Deleting a playlist removes its definition, not music. System lists are protected. Above 10,000 positions, browsing/playback is page-based and some full-list edits are unavailable.','small')

b=page('ORGANISE','Import a playlist','Match a CSV or public playlist to music already in your iBroadcast library.','Importing-playlists')
fig(b,'2026-10-22/deezer-import-columns.png','Earlier development interface: check title, performing artist, duration and optional album columns before matching.',maxh=270,crop=(.055,.085,.935,.96))
steps(b,[
 'Choose <b>Playlists &gt; Import CSV</b>, check encoding/separator/header and preview. Map <b>Track title</b> and <b>Performing artist</b>; album, duration, year and number are optional. Set duration units correctly.',
 'Choose <b>Match tracks</b>. Unique full-title/performer matches can be automatic; versions, ambiguous copies and conflicting mapped fields need a decision. Album mapping makes matching stricter.',
 'Use <b>Find / choose a track</b> or <b>Change match</b> to compare copies. Keep the default manual choice for ambiguity, or deliberately choose a matching-copy preference such as Prefer FLAC. Skip unwanted records.',
 'Name the playlist, review its ordered matches and any unresolved omissions, then <b>Create private playlist in iBroadcast</b>. Wait for confirmation before repeating an import.'
])
paras(b,'<b>Playlist URL</b> accepts public Deezer lists; enable Deezer under Sources &amp; keys. ListenBrainz is an experimental test source and can be blocked. Spotify, Apple Music and TIDAL URLs are not supported. Fetching retrieves metadata, never audio.','small')

b=page('ORGANISE','Keep import progress and review order','An unfinished import is a draft, not a playlist or a download.','Importing-playlists#pause-and-resume-csv-imports')
fig(b,'2026-10-22/deezer-import-choose-track.png','Earlier development interface: manually compare the full title, performer, album and duration before choosing a library copy.',maxh=268,crop=(.07,.05,.94,.94))
paras(b,'Unresolved does not necessarily mean the song is missing: another edition, a different album, ambiguous duplicates or duration data can prevent an automatic match. Mapping fewer optional fields can be appropriate, but check the actual recording/version.',
 'You may create a playlist from the matched subset. The final review states which unresolved records will be omitted. <b>Export unresolved records as CSV</b> preserves the remaining rows for later work. CSV order is retained; a rank/date column is not used to sort.')
h(b,'Pause explicitly before closing')
paras(b,'<b>Pause import</b> saves a checkpoint for the current account on this computer. <b>Paused imports &gt; Refresh library &amp; resume</b> checks current library matches while keeping valid manual choices. Review again before creating a playlist. Ordinary unpaused drafts are temporary and expire after one hour.',
 'Up to ten paused imports per account can be stored. A failed or uncertain playlist creation is not automatically repeated: inspect Playlists first. Removing a paused checkpoint affects only that saved local draft.')

b=page('EDIT METADATA','Edit album information','Online suggestions fill a draft. Only your reviewed Save changes iBroadcast.','Editing-metadata')
fig(b,'2026-10-23/editor-album.jpg','0.80.0 sample library: Edit album on the left, online suggestions on the right. The scrollable form continues below this view.',maxh=315,crop=(.084,.05,.916,.95))
steps(b,[
 'Open an album and choose <b>Edit</b>. In <b>Edit album</b>, adjust title, album artist, release year, disc number and shared genre/composer choices as needed.',
 'Type a name or select an existing artist, genre or composer suggestion. A genre is one complete label until you explicitly Split it. Check spelling to avoid near-duplicate artist identities.',
 'Use online results only after comparing the artist, title and edition. Fill selected fields or Use all where offered. Search/suggestions alone never save.',
 'Choose <b>Review draft</b>, inspect every changed record and confirm Save. Wait for the read-back result.'
])
paras(b,'For several albums by <b>one album artist</b>, select their cards and enable only the shared fields you intend to change. Ordinary bulk metadata editing is not a general cross-artist edit. Changing album year leaves track years alone unless you choose the track-year option.','small')

b=page('EDIT METADATA','Tracks, credits and compilations','Album artists identify the release; track artists identify the performers on each song.','Artists-and-credits')
fig(b,'2026-10-23/editor-tracks.jpg','0.80.0 sample library: select a track in Edit tracks, then change its own fields and credits. Tabs retain the same metadata draft.',maxh=255,crop=(.084,.05,.916,.95))
paras(b,'<b>Edit tracks</b> contains a track list and the selected track\'s fields. Track title, artist, year, number, genres and credits can differ from the album. Individual track changes take precedence over album-wide changes. Review includes metadata from both tabs; lyrics keep a separate save.',
 'Additional credits retain their role and optional phrase. Composers are composer credits, not a second primary performer. Do not split a collaboration name on an ampersand, comma or slash unless it genuinely represents separate stored credits.')
h(b,'Various Artists')
paras(b,'For a compilation, select <b>Various Artists</b> below Album artist. It uses iBroadcast\'s native compilation identity and clears additional <b>album</b> artists in the review. Each track\'s performer and track credits remain unchanged. Check the before/after list across every disc. For a bulk selection, first enable Change Album artist.')
b.extend(note('Years are separate fields','New years must be 1800-2050; blank or 0 removes a year. The Interface preference <b>Apply the album release year to tracks by default</b> only preselects a checkbox in new drafts. It never repairs previous differences or changes an existing draft.'))

b=page('EDIT METADATA','Review, save and confirm','A sent request and a confirmed saved result are different states.','Saving-and-history')
fig(b,'metadata-review.png','Earlier-interface detail: the normal metadata review compares Before and After. The final Save is a separate decision.',maxh=191,crop=(.23,.28,.77,.69))
paras(b,'Before writing, Tagcast checks fresh library state against the review. Conflicting or replaced data blocks the save. Only changed supported fields are sent. After acceptance, a fresh library read-back checks the result. <b>Do not close and repeat an action because verification is slow.</b>')
b.append(table([
 ['Result','What to do'],
 ['Saved / confirmed','The checked values match. Other entries in the same job may have different results.'],
 ['Checking / sent, checking','Wait for read-back. Large-library verification can take longer than the write.'],
 ['Unconfirmed / not confirmed','Inspect iBroadcast and reload before any fresh review. An absent response does not prove failure.'],
 ['Failed / blocked / not sent','Read the reason. Earlier writes may already have succeeded; later requests can remain unsent.'],
],[.34,.66]))
paras(b,'Mutating requests are sent once rather than blindly retried after an ambiguous reply. Saves are not transactional and have no general metadata Undo. <b>Change history</b> keeps the newest 300 entries in this browser/profile and local address. Export it before clearing site data. Artwork has limited separate Undo; ratings, tags, lyrics, playlists, merging and trash do not gain Undo from History.','small')

b=page('EDIT METADATA','Compare artwork and artist images','Image changes have their own Now/New comparison and explicit Save.','Artwork-and-artist-images')
fig(b,'artwork-compare.png','Earlier-interface detail: compare the current and proposed cover. Save is further down the dialog and remains separate from metadata.',maxh=267,crop=(.195,.084,.792,.82))
steps(b,[
 'For an album cover, choose <b>Edit</b>, then its cover or a cover suggestion. For an artist, hover/focus its photo for <b>Change image</b>; for a playlist, use <b>Change cover</b>. Choose a suggestion, your own image or an allowed image URL.',
 'Compare <b>Now</b> and <b>New</b>. Check edition, artist identity and image quality. JPEG, PNG, WebP and GIF are supported up to 15 MB.',
 'Choose <b>Save to iBroadcast</b> and wait for verification. A displayed multi-disc album is processed disc by disc.'
])
paras(b,'An artist photo changes that artist\'s image throughout the library. A playlist cover changes only that playlist\'s cover. Original local image/audio files stay untouched.',
 'Album/artist artwork Undo is available only where previous artwork exists. Tracks without an earlier cover keep the new one; no prior artist image means it cannot be removed through this Undo. Playlist cover changes have no artwork Undo. An uncertain upload/assignment should be checked before another attempt.','small')

b=page('LYRICS','Lyrics that follow the music','Online display is optional and separate from storing lyrics in iBroadcast.','Lyrics#now-playing-lyrics')
fig(b,'2026-11-03-cd-view/cd-view-lyrics.png','1.7.0 CD-view test capture with LRCLIB line timing. The highlighted line follows playback; provider credit and Temporary display remain visible.',maxh=313)
paras(b,'Open expanded <b>Now playing &gt; Lyrics</b>. Under <b>Settings &gt; Playback &gt; Now playing lyrics</b>, choose native-only, <b>iBroadcast first with Unison &gt; LRCLIB fallback</b>, or <b>Unison &gt; LRCLIB first with iBroadcast fallback</b>. Native-only is the default.',
 'Public lookup runs while this expanded Lyrics view is open and an online mode is enabled. Unison is tried first for usable text; LRCLIB follows when needed and enabled under Sources &amp; keys. Line timing highlights a line; supported word/segment timing adds a moving underline. Plain text can still display without timing.',
 'Seeking and pause/resume follow the existing playback clock. Manual scrolling stops following; choose <b>Follow lyrics</b> to rejoin. Results may be missing or mistimed: contributed timing is not a guarantee. Online lyrics stay temporarily in memory and are not saved automatically.')
paras(b,'The selected provider receives track title, performer, album and known duration, not audio or your iBroadcast credentials. Closing the lyrics view stops new lookups. Source attribution remains visible.','small')

b=page('LYRICS','Find, edit or import saved lyrics','Native text is ordinary lyrics. Saving it requires its own reviewed action and Premium access.','Importing-lyrics')
fig(b,'2026-10-23/lyrics-import.jpg','0.80.0 sample album: link local LRC/TXT files to tracks, preview the plain text, then review. Timing is removed for native saves.',maxh=302,crop=(.084,.055,.916,.945))
paras(b,'For one track, use <b>Edit &gt; Edit tracks &gt; Track lyrics in iBroadcast</b>. <b>Find lyrics on LRCLIB</b> explicitly searches; <b>Use these lyrics</b> fills the separate draft. Then choose <b>Review lyrics</b> and <b>Save lyrics to iBroadcast</b>. A blank reviewed After removes only lyrics. Other native userdata is preserved.',
 'For an album, choose <b>More &gt; Import lyrics</b>. Select LRC/TXT files, inspect automatic number/full-title links and resolve ambiguity manually. <b>Review linked lyrics</b> reads current native text. Existing lyrics are kept unless you explicitly choose replacement for that track. Save runs one track at a time and stops on conflicts or uncertain results.',
 'File import supports up to 100 tracks/files, 5 MB total and 500 KB per file. Files and links are temporary until reviewed/saved; closing an unsaved import asks before discarding it.')
paras(b,'To read existing album lyrics without playback, choose <b>More &gt; Check album lyrics</b> (up to 100 tracks). It reads iBroadcast, not public providers. Known text gets a Lyrics label beside the title; no label may simply mean unchecked. Free accounts can read/search lyrics but cannot save them.','small')

b=page('CLEAN UP','Review metadata cleanup','Analyse first, inspect every proposed change, then approve bounded processing.','Metadata-cleanup')
fig(b,'2026-10-22/cleanup-genre-labels.png','Earlier development interface: choose one exact genre label and proposed replacements. Preparing this review changes nothing.',maxh=273,crop=(.11,.06,.91,.95))
steps(b,[
 'Open <b>Overview &gt; Metadata health &gt; Clean up metadata</b>. Choose combined genres, album artists, track artists, composers or <b>Review genre labels</b>.',
 'Prepare the preview. Semicolon cleanup splits only semicolons. Slashes, commas and ampersands are preserved rather than guessed as separators.',
 'For an exact genre replacement, choose the existing label and replacements. Removing a label requires the explicit removal option. Review/exclude albums before approving.',
 'Start only the reviewed selection. Tagcast checks and reads back each batch before continuing. Stop prevents later requests; already accepted writes may complete.'
])
paras(b,'Cleanup reports belong to the current account and persist on this computer. Export a report for your records. Resume explicitly and check outstanding work first; uncertain writes are not resent automatically. Album-artist cleanup requires Combine Multi-Disc Album Sets off. There is no automatic batch Undo.')

b=page('CLEAN UP','Reconcile album and track years','A difference can be intentional. Choose which known year to apply and where.','Album-and-track-years')
fig(b,'2026-10-28-year-review/year-comparison.png','Development example with fictional metadata, captured before 1.1.0. The year choice is explicit; it does not automatically use the oldest or majority value.',maxh=271,crop=(.10,.05,.89,.955))
paras(b,'In Cleanup, select <b>Album and track years &gt; Analyse years</b>. It compares the already-loaded library without audio or provider searches. Filter/search differing, mixed, missing or invalid years.')
b.append(table([
 ['Action','Scope'],
 ['Album year to track years','Apply the known album year to every track; keep the album year.'],
 ['Track year to album year','Apply the chosen known track year to the album only.'],
 ['Track year to album + all tracks','Use the chosen known track year for both; matching tracks need no write.'],
],[.43,.57]))
paras(b,'For album 2013 with tracks at 2007 and 2013, choose 2007 and the album-plus-tracks action if all should become 2007. Mixed track years require a choice. The normal review/save opens; after confirmed read-back the comparison refreshes in the same window. Checking may take time because it verifies against the full library.','small')

b=page('CLEAN UP','Duplicate copies and trash','Metadata identifies candidates; it cannot prove identical recordings or sound quality.','Trash-and-duplicates')
paras(b,'Use <b>Albums &gt; Filter and sort &gt; Duplicate tracks</b>, open an album and choose <b>More &gt; Move to trash</b>. Repeated positive numbers on one disc are flagged even when titles differ. The same title at different positions or on another disc is not automatically a duplicate.')
fig(b,'duplicate-tracks-upload-suggestions.png','Earlier-interface example: upload-day/format groups help compare copies. Suggestions are selected only when you choose them; still inspect the review.',maxh=264,crop=(.17,.19,.98,.93))
paras(b,'<b>Select extra copies</b> uses the stricter matching-title/number rule and keeps the first. <b>Select suggested copies</b> can prefer FLAC over MP3 and a newer upload within one format, while leaving ties or incomplete comparisons manual. Different titles, artists or durations deserve careful listening. Nothing is selected merely by opening the dialog.',
 'For whole albums, tick cards and review <b>Move selected albums to trash</b>. In paginated mode, selection applies to the page; Continuous scroll selects loaded results, not every matching album. Hidden selections still count. Library-wide duplicate analysis has a separate reviewed report and explicit approval/resume.')
b.extend(note('Trash is not permanent deletion','Tagcast moves reviewed tracks to <b>iBroadcast\'s trash</b>. Restore through iBroadcast itself. Tagcast cannot restore them or offer automatic Undo. Local music files stay untouched. Check uncertain results before another selection.'))

b=page('CLEAN UP','Merge album fragments','Move existing tracks into one selected destination album after checking every fragment.','Merge-albums')
fig(b,'2026-10-27-album-merge/destination-album.png','Local test, 27 October: four fragments of The 8bits of Christmas, with the existing Various Artists entry chosen as destination.',maxh=272)
steps(b,[
 'Search <b>Albums</b> for the fragments. Tick them, or <b>Select all on this page</b>, and inspect any notice about selected albums outside the results.',
 'Choose <b>Merge albums</b>, select the existing <b>Destination album</b> to keep and choose <b>Review merge</b>.',
 'Check all source albums, resulting tracks and warnings, then confirm the merge once. Wait for <b>All tracks confirmed in the destination album</b> before opening the result.'
])
paras(b,'Use 2-20 complete single-disc entries with the same disc number, up to 500 active tracks. This action is not for combining CD 1 and CD 2 or partial multi-disc sets. Combine Multi-Disc Album Sets must be off.',
 'The destination supplies title, album artists, album year, disc number and album rating. Tracks keep their IDs, titles, performers, credits, track years, genres, artwork and numbers. Merging does not infer Various Artists, renumber or deduplicate. Overlapping numbers require explicit acknowledgement. Source ratings/local favourites are not transferred. There is no automatic Undo.','small')

b=page('TRANSFER MUSIC','Upload local music','Choose, prepare, review, then explicitly Start. The feature is off by default.','Music-uploads')
fig(b,'2026-10-31-uploads/upload-progress.png','1.2.0 example, Amber Original: files upload serially and remain grouped by source folder. Pause and Stop stay beside progress.',maxh=289,crop=(.2,.27,.98,.93))
steps(b,[
 'Enable <b>Settings &gt; Data &amp; exports &gt; Music uploads</b>, Save, then approve the extra upload permission if asked. Open Uploads.',
 'In the desktop app, choose files/folders. Browser use accepts paths on the <b>server computer</b>. Prepare &amp; review checks access, formats and identical file hashes; it sends no audio.',
 'Inspect ready, skipped and unreadable files, then <b>Start uploads</b>. Only the reviewed new files are sent. Pause takes effect between files; Stop interrupts where possible.'
])
paras(b,'Uploaded means acknowledgement/hash confirmation. <b>Needs checking</b> is genuinely uncertain: inspect iBroadcast before preparing those files again. Hash matching finds byte-identical files, not the same song with different tags. Selection supports 1,000 discovered files, 1.5 GB each.','small')
paras(b,'iBroadcast processes the files and reads their embedded tags. Reload after processing to see new albums. Tagcast does not watch folders, retag originals or sync deletions. Successful selections clear; uncertain/incomplete jobs remain for inspection. Selections/results are not restored after closing.','small')

b=page('TRANSFER MUSIC','Download album copies','A reviewed download creates separate files; it does not adopt or retag existing music.','Downloads')
steps(b,[
 'Open <b>More &gt; Download album</b>, or select album cards and choose Download. A displayed set includes every disc.',
 'On Downloads, check the albums, destination folder and options. The destination is on the computer running Tagcast, even when the interface is in another browser.',
 'Choose <b>Review download</b> to inspect counts and example paths. No audio is fetched yet.',
 'Choose <b>Start downloads</b>. Read completed, skipped and fallback notes. Stop keeps completed files and eligible partials; reopening never resumes automatically.'
])
h(b,'Choose the source deliberately')
paras(b,'Premium defaults to <b>Original via the iBroadcast download service</b>. For current embedded tags, enable <b>Download Updated Metadata</b> in iBroadcast. That service decides which fields it embeds; Tagcast does not rewrite them locally.',
 '<b>Original upload via streaming</b> retrieves uploaded bytes/tags instead. A download-service fallback is labelled because later iBroadcast tag edits may be absent. Converted MP3 uses streaming. Free accounts use 128 kbps MP3. Changing source does not replace completed files.')
b.extend(note('Protect existing files','Unverified or locally modified destination files are preserved, not overwritten or silently trusted. Keep the hidden <b>.ibfetch.json</b> integrity manifest beside downloaded music. Recheck checksums explicitly when needed.'))
paras(b,'Default naming is artist / album (year) / disc-track title, with safe filenames and collision handling. One worker is the default; more workers compete with playback for network/disk capacity. Options persist, but selections and progress are session-local. Reselect/review after restart to reuse verified completed files or eligible streaming partials.',
 'For individual tracks, playlists, advanced filters or CLI downloads, use <link href="https://github.com/cyberdeliaAI/ibfetch" color="#276b7d">ibfetch</link>, linked from Downloads. Metadata JSON/CSV export is a different feature.')

b=page('PERSONALISE','Language and sidebar','Six interface languages share the same music metadata and saved library.','Settings-and-help#interface-language')
fig(b,str(TMP/'language-1.4.png'),'Tagcast 1.7.0 local demo: the header language menu and Settings > Interface use the same language choice.',maxh=286,crop=(.18,0,1,.77))
paras(b,'Use the small globe/language control in the header or <b>Settings &gt; Interface &gt; Language</b>. Choose English, Dutch, German, French, Spanish or Japanese. <b>Automatic · follow system</b> uses a supported system/browser language and otherwise English. A manual choice takes precedence.',
 'Language changes interface text and local date/number formatting, not artist names, album titles, genres, tags, filenames, lyrics or reports. Open dialogs with unsaved drafts retain their current language and values until reopened. Some server/provider messages remain English; the Wiki and this manual use English.')
h(b,'Make the sidebar your own')
paras(b,'Under Interface, show/hide optional shortcuts and move them up/down. Settings and essential navigation remain available. Hidden shortcuts do not disable a feature; Recently played and 1001 Albums have their own switches. Restore default sidebar resets the arrangement and hides the optional upload-folder/date shortcuts.',
 'Long labels wrap; the sidebar scrolls vertically. Pointer hover or keyboard focus reveals scrollbars, with a bottom fade when more items remain. System accessibility settings may keep scrollbars visible.')

b=page('PERSONALISE','Playback preferences','Local presentation choices apply immediately; server preferences use Save changes.','Settings-and-help#playback')
fig(b,str(TMP/'playback-1.4.png'),'Tagcast 1.7.0 local demo: display choices, fullscreen mode and optional spinning artwork. This screenshot shows preferences, not an active audio session.',maxh=265,crop=(.34,.30,.98,.99))
paras(b,'Compact-player format/quality and track-artist labels can be hidden without altering playback. Fullscreen/In app window controls how expanded Now playing opens. Album cover/Spinning CD controls artwork independently. Online lyrics, cover background and the optional live spectrum are presentation choices.',
 '<b>Streaming quality</b>, <b>Record played tracks in iBroadcast</b> and device/queue preferences need Save changes. Play reporting starts off; when enabled it reports after more than ten seconds of actual listening and enables Recently played. That page reflects iBroadcast\'s native list, including other devices, rather than a complete Tagcast log.')
b.extend(note('Experimental remote queues','Queue synchronisation is off by default and needs extra authorization. Use Devices to connect this app\'s queue or control a device. A controller pauses local audio. Compatibility with a particular iBroadcast player still needs a practical check; keep it off for ordinary local listening.'))

b=page('PERSONALISE','Themes and custom colours','Appearance controls brightness; Colour chooses the palette. They are independent.','Custom-themes')
fig(b,str(TMP/'appearance-1.4.png'),'Tagcast 1.7.0 local demo, Appearance editor. Preview colours are isolated until Save & use; the surrounding interface retains the current palette.',maxh=292,crop=(.35,.38,.98,1))
paras(b,'Open <b>Theme</b> in the header for Auto, Light or Dark, then choose Forest, Ocean, Warm, iBroadcast inspired, Apple Music Classic or Amber. The latter uses red/pink accents and sidebar icons. Changing appearance does not restart audio.')
steps(b,[
 'Choose <b>Settings &gt; Appearance</b> or <b>Theme &gt; Edit themes</b>. Start from a palette/saved theme, or use Import JSON.',
 'Name the draft and edit Light/Dark variants beside the component preview. Variant editing does not switch the app\'s Light/Dark/Auto preference. Inherited colours follow the base palette.',
 'Use <b>Save theme</b> to store it, or <b>Save &amp; use</b> to apply it. <b>Export JSON</b> exports the valid current draft, including both variants, for another profile.'
])
paras(b,'Saved themes are local. Import creates an unsaved preview rather than replacing an existing theme. Contrast guidance helps, but inspect the real screens too. Native audio/output controls can retain system styling. More ready-to-import palettes and their attribution are available at <link href="https://tagcast.app/themes.html" color="#276b7d">tagcast.app/themes.html</link>.','small')

b=page('PERSONALISE','Settings reference','Use the timing label beside each control rather than assuming every setting needs Save.','Settings-and-help')
b.append(table([
 ['Category','Main choices','When they apply'],
 ['Interface','Language, banner, sidebar, default track-year checkbox','Immediate local choices; language also persists through the server when available.'],
 ['Appearance','Custom themes and portable JSON','Draft preview until Save theme / Save & use.'],
 ['Playback','Labels, expanded view, CD, lyrics, Gapless; quality, play reporting, queues','Display choices immediate/next opening; Gapless next track; server settings require Save.'],
 ['Discovery','1001 Albums, artist biographies, album background','Save; analyses remain explicit. Visited-page lookups depend on their switches.'],
 ['Sources & keys','Providers, keys, automatic editor lookup','Save; key removal submits the current server settings form.'],
 ['Data & exports','Metadata/history exports, music uploads','Exports explicit; upload enable requires Save and authorization before Start.'],
 ['About & updates','Community, manual check, automatic stable-release checks','Links/checks explicit; automatic-check switch requires Save.'],
],[.20,.39,.41]))
paras(b,'<b>Discard changes</b> only discards unsaved server preferences. It does not undo immediate browser choices. Disabling a provider keeps its saved key; Remove deletes the saved key, so check other pending settings first. Environment-supplied keys must be managed outside Tagcast.',
 'The desktop app remembers resized main and Mini Player windows in its own profile. This is independent of the expanded Now playing mode. Browser and desktop profiles, or another local port, can have different appearance/history preferences.')

b=page('YOUR DATA','Export metadata and keep records','A metadata snapshot, Change history and audio downloads serve different purposes.','Exporting-library-metadata')
steps(b,[
 'Reload the library first if you want a snapshot of recent iBroadcast changes.',
 'Open <b>Settings &gt; Data &amp; exports &gt; Export library metadata</b>. Choose optional tags, playlists and local favourites where available.',
 'Choose <b>Prepare JSON export</b> or <b>Prepare CSV ZIP</b>. When ready, use its separate <b>Download</b> button. Prepared downloads expire after 15 minutes.',
 'Use <b>Export changes</b> separately to keep this browser\'s Change history. Save cleanup/duplicate reports from their own workflows.'
])
paras(b,'The metadata export covers the complete <b>loaded library</b>, not current search results or unsaved drafts. Native IDs preserve relationships between artists, albums/discs, tracks and credits. CSV ZIP contains linked tables, with optional playlists/folders, tags and local favourites when available. Read its manifest for missing optional data.')
b.extend(note('This is not a restorable music backup','The export excludes audio, image binaries, credentials and provider prose. It has no restore function. Audio downloads create separate music copies; Change history records only a bounded local set of actions. Keep your original music independently.'))
h(b,'What survives restart?')
b.append(table([
 ['Survives locally','Usually temporary'],
 ['Sign-in/configuration, library caches, saved themes/preferences, account-local hearts, remembered queue order, explicitly paused playlist imports and saved cleanup reports.','Elapsed playback time, unpaused editor/import drafts, online Now playing lyrics, upload/download selections and job progress. The bounded local queue itself is restored without starting audio.'],
],[.5,.5]))
paras(b,'Downloaded files and their integrity manifest remain on disk. Restarting a transfer requires a new reviewed selection; reopening never automatically sends or downloads music.','small')

b=page('YOUR DATA','Storage, privacy and safe recovery','Know which actions affect iBroadcast and which remain on this computer.','Whats-saved-where')
b.append(table([
 ['Stored in iBroadcast','Local to Tagcast'],
 ['Reviewed metadata/credits, saved native lyrics, artwork, native stars/track ratings, tags and private playlists; reviewed trash/merges affect the account library.','Tokens/settings/caches, album/artist hearts and reports in the settings folder; appearance and bounded History in the browser/app profile.'],
],[.5,.5]))
paras(b,'The default settings directory is <b>~/.tagcast/</b>, or .tagcast in your Windows user folder. TAGCAST_HOME can select another folder. Browser-local data belongs to its profile and local address/port. Changing ports or clearing site data can hide local history/preferences without changing iBroadcast.',
 'Disconnect forgets local sign-in/library cache and attempts token revocation. It does not undo saved account changes or erase every separate report/favourite. Tokens and source keys remain on the local server, not in the frontend.')
h(b,'When network requests happen')
paras(b,'iBroadcast is contacted for sign-in, library, playback and your chosen operations. Public update checks contact GitHub when enabled. Overview checks the public service feed. Selected editor providers can run automatically when the editor opens if that preference is enabled.',
 'Opt-in biographies/background text run for visited pages. Online Now playing lyrics require an online mode and an open listening-page or expanded lyrics view. Explicit Find lyrics and public-playlist fetches have their own actions. Uploads send chosen audio only after Start; downloads fetch audio only after Start downloads.')
b.extend(note('An uncertain write needs inspection','Keep the result/report, inspect the actual iBroadcast values and reload. Do not immediately repeat a merge, import, upload or save with an uncertain result. A timeout can mean the server already applied it. There is no global rollback.'))
paras(b,'Read the <link href="https://github.com/cyberdeliaAI/tagcast/blob/main/PRIVACY.md" color="#276b7d">Privacy policy</link> for current network and data-handling details.','small')

b=page('REFERENCE','Troubleshooting','Start with the visible state and exact message; avoid deleting settings as a first response.','Troubleshooting')
b.append(table([
 ['Symptom','Try this'],
 ['Still seeing the demo','Finish official approval and keep Tagcast open. Check the connection dialog; wait if Loading library is active. Reload when connected.'],
 ['Library looks old','Reload library. If necessary, Download everything again in the connected dialog. Preserve unsaved drafts before reloading.'],
 ['Saving seems slow','Checking verifies against iBroadcast and may download a large library. Wait; do not start a duplicate write.'],
 ['Album fields blocked','Turn off Combine Multi-Disc Album Sets in iBroadcast and reload before a new review. Supported track edits may have succeeded already.'],
 ['No lyrics / wrong timing','Check source mode, enabled LRCLIB and whether expanded Lyrics is open. Retry temporary failures where offered. A provider may lack this exact version.'],
 ['Gap or buffering','Compare normal playback and Original quality; check service/network health. Unsupported Gapless boundaries use ordinary playback.'],
 ['Missing local hearts/history/theme','Check the account, desktop/browser profile, settings directory and local port. Metadata changes in iBroadcast are separate.'],
 ['Upload stopped / needs checking','Inspect iBroadcast before preparing again. Stop can wait for an active network read; accepted files may still arrive.'],
 ['Old-looking interface after update','Quit the older app and reopen the intended extracted package. Check the footer version before discarding drafts or resetting data.'],
],[.31,.69]))
paras(b,'For a bug report, include Tagcast version, operating system, desktop/browser mode, exact steps/message and whether it is reproducible. Crop private account details, paths and tokens from screenshots/logs. <link href="https://github.com/cyberdeliaAI/tagcast/issues" color="#276b7d">GitHub Issues</link> is best for reproducible problems; <link href="https://www.reddit.com/r/Tagcast/" color="#276b7d">r/Tagcast</link> is available for discussion.','small')

b=page('REFERENCE','Keyboard, limits and terminology','A compact desk reference for the controls and distinctions used in this guide.','Settings-and-help#keyboard-and-dialog-controls')
b.append(table([
 ['Action','Keyboard'],
 ['Move through controls','Tab / Shift+Tab; the focus outline shows the target.'],
 ['Choose a button/menu option','Enter or Space; arrows/Home/End in supported menus and tabs.'],
 ['Dismiss a menu/dialog','Escape where supported; unsaved workflows may ask first.'],
 ['Open desktop Mini Player','Cmd/Ctrl+Shift+M.'],
 ['Reorder playlist positions','Focused handle: Up/Down; Move to position is also available.'],
 ['Scroll a narrow Tracks table','Tab to Track search results, then Left/Right.'],
 ['Contextual help','Choose ? in the header or supported dialog; closing restores focus.'],
],[.44,.56]))
h(b,'Common terms')
paras(b,'<b>Album artist / track artist:</b> release-level credit versus performer on a song. <b>Disc set:</b> a displayed group of original disc records, not necessarily a single native album ID.',
 '<b>Genre / tag:</b> genre fields versus a separate native label assignment. <b>Favourite / rating:</b> local album/artist hearts are independent; track hearts are native ratings.',
 '<b>Draft / review / confirmed:</b> proposed inputs; the explicit before/after decision; the checked result after sending. <b>Unconfirmed:</b> the result is uncertain, not proof of failure.')
h(b,'Useful boundaries')
paras(b,'Album merge: 2-20 single-disc entries / 500 tracks. Multi-album tags: 20 displayed albums / 500 tracks per review. Lyrics file import: 100 tracks/files. CSV playlist import: 10,000 records. Upload preparation: 1,000 discovered files. These limits describe Tagcast workflows; they are not claims about iBroadcast account storage.')

b=page('REFERENCE','About this edition','An illustrated user guide to Tagcast 1.7.0.','Home')
paras(b,'Prepared on <b>11 November 2026</b> from the Tagcast 1.7.0 source snapshot <b>d960633</b>, the project\'s user documentation and the curated screenshot collection. It describes everyday operation rather than developer APIs, internal protocols or an exhaustive test report.',
 'Screenshots are examples, not additional test evidence or a promise of provider coverage. The fresh language, browsing and Settings captures use the 1.7.0 local demo. Older workflow images and local CD-view test captures are identified in their captions. Their displayed metadata, counts and earlier version badges belong to those examples.',
 'The UI can vary with language, window width, theme, operating system, account capabilities and enabled options. English control names are used throughout this guide. The optional CD view is new in 1.7.0; an older test-build badge does not make it part of an earlier public download.')
h(b,'Online companion')
paras(b,'<link href="https://tagcast.app/" color="#276b7d">tagcast.app</link> - product overview, download links and theme collection.<br/>'
 '<link href="https://github.com/cyberdeliaAI/tagcast/wiki" color="#276b7d">Tagcast Wiki</link> - detailed feature walkthroughs and later corrections.<br/>'
 '<link href="https://github.com/cyberdeliaAI/tagcast/releases" color="#276b7d">GitHub Releases</link> - actual published versions, platform files and checksums.<br/>'
 '<link href="https://help.ibroadcast.com/" color="#276b7d">iBroadcast Help</link> - account settings and service behaviour.<br/>'
 '<link href="https://status.ibroadcast.com/" color="#276b7d">iBroadcast Status</link> - official global service reports.')
h(b,'Credits and scope')
paras(b,'Tagcast is an independent open-source project. iBroadcast and other service/product names belong to their respective owners; references do not imply endorsement. Screenshots reproduce the project\'s existing illustrations and maintainer-supplied captures. Album artwork and displayed lyrics remain the property of their respective rights holders.',
 'Online lyrics screenshots retain provider credits, including LRCLIB. Unison/Better Lyrics provides the other optional public display source. Custom theme adaptations and their source/licence credits are documented in the project\'s theme collection.',
 'The PDF has clickable contents, section bookmarks and per-topic Wiki links. It makes no account changes and contains no credentials or library export. Check the release page for availability; this document alone does not establish publication or platform certification.')

exec((TMP/'current_topics.py').read_text())

class GuideDoc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=69,bottomMargin=49,
            title='Tagcast 1.7.0 - Illustrated User Manual',author='Tagcast',subject='Browsing, playback, metadata, lyrics and library organisation',pageCompression=1,allowSplitting=1)
        self.addPageTemplates(PageTemplate(id='guide',frames=[Frame(M,49,CW,H-118,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=self.chrome))
        self.current_title='';self.seen={}
    def chrome(self,c,doc):
        if doc.page==1:return
        c.saveState();c.setStrokeColor(LINE);c.setLineWidth(.5);c.line(M,H-46,W-M,H-46)
        c.setFillColor(TEAL);c.setFont('Guide-Bold',8);c.drawString(M,H-34,'TAGCAST  /  USER MANUAL')
        c.setFillColor(MUTED);c.setFont('Guide',8);c.drawRightString(W-M,H-34,'VERSION 1.7.0')
        c.setStrokeColor(LINE);c.line(M,40,W-M,40);c.setFillColor(MUTED);c.setFont('Guide',8)
        c.drawString(M,26,'tagcast.app');c.drawRightString(W-M,26,f'{doc.page:02d}')
        c.restoreState()
    def afterFlowable(self,f):
        if getattr(f,'bookmark_key',None):
            key=f.bookmark_key;self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0,False);self.seen[key]=self.page

class Cover(Flowable):
    def __init__(self):super().__init__();self.width=CW;self.height=H-119
    def draw(self):
        c=self.canv;x=-M;y=-49;top=self.height
        c.setFillColor(INK);c.rect(x,y,W,H,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#8bd4df'));c.setFont('Guide-Bold',10);c.drawString(0,top-35,'YOUR COLLECTION. YOUR CHOICES.')
        c.setFillColor(colors.white);c.setFont('Guide-Bold',57);c.drawString(-2,top-109,'Tagcast.')
        c.setFont('Guide',27);c.drawString(0,top-153,'The illustrated user manual')
        c.setFillColor(colors.HexColor('#b7d0d9'));c.setFont('Guide',12);c.drawString(0,top-183,'Version 1.7.0  /  English edition')
        img=SHOTS/'2026-11-11-interface/now-playing-lyrics-queue.png'
        c.drawImage(str(img),-12,top-535,width=CW+24,height=(CW+24)*1828/2836,mask='auto')
        c.setFillColor(colors.HexColor('#b7d0d9'));c.setFont('Guide',9);c.drawString(0,top-558,'Now playing with lyrics, queue and the same shared playback controls.')
        c.setStrokeColor(colors.HexColor('#42606c'));c.line(0,110,CW,110)
        c.setFillColor(colors.white);c.setFont('Guide-Bold',11);c.drawString(0,84,'Browse · Listen · Organise · Edit')
        c.setFillColor(colors.HexColor('#b7d0d9'));c.setFont('Guide',10);c.drawString(0,63,'Practical instructions, screenshots and safe saving workflows.')
        c.setFont('Guide',9);c.drawString(0,15,'tagcast.app');c.drawRightString(CW,15,'Documentation snapshot  /  11 November 2026')

def build():
    story=[Cover(),PageBreak()]
    title=p('Contents','title');title.bookmark_key='contents';story.append(title)
    story.append(p('Start with the first session, or jump directly to a task. Every entry below is clickable.','lead'))
    # Two columns keep all topics on one readable contents page.
    half=(len(pages)+1)//2
    cols=[]
    for lo,hi in [(0,half),(half,len(pages))]:
        rows=[];last=None
        for i in range(lo,hi):
            pg=pages[i]
            if pg['group']!=last:
                rows.append([p(pg['group'],'kicker'),'']);last=pg['group']
            rows.append([p(f'<link href="#topic-{i}">{escape(pg["title"])}</link>','toc'),p(f'<link href="#topic-{i}">{i+3:02d}</link>','toc')])
        t=Table(rows,colWidths=[CW/2-35,22]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),1.5),('BOTTOMPADDING',(0,0),(-1,-1),2)]));cols.append(t)
    spread=Table([[cols[0],cols[1]]],colWidths=[CW/2,CW/2]);spread.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8)]));story.append(spread)
    story.append(Spacer(1,12));story.extend(note('Read screenshots as examples','Current text describes version 1.7.0. Captions identify older interface examples. Counts and metadata belong to the pictured library; no account changes were made to create this manual.'))
    for i,pg in enumerate(pages):
        story.append(PageBreak());story.append(p(pg['group'],'kicker'))
        title=p(pg['title'],'title');title.bookmark_key=f'topic-{i}';story.append(title);story.append(p(pg['lead'],'lead'))
        story.extend(pg['blocks'])
        if pg['slug']:story.append(p(link(pg['slug'],'More in the Wiki')+'  /  '+link('Home','Documentation home'),'small'))
    def gather(item):
        found=[]
        if hasattr(item,'manual_figure_info'):found.append(item.manual_figure_info)
        if isinstance(item,Table):
            for row in item._cellvalues:
                for cell in row:found.extend(gather(cell))
        elif isinstance(item,(list,tuple)):
            for child in item:found.extend(gather(child))
        return found
    actual_images=gather([pg['blocks'] for pg in pages])
    doc=GuideDoc(OUT);doc.build(story)
    expected={f'topic-{i}':i+3 for i in range(len(pages))}
    wrong={k:[expected[k],doc.seen.get(k)] for k in expected if doc.seen.get(k)!=expected[k]}
    (TMP/'manifest.json').write_text(json.dumps({'version':'1.7.0','source_commit':'9b47dae9ba917da0bcdfc93b8d6fa52c0c23c900','wiki_source_commit':'14d3e9839bf83cf8029ad8fc0084255ed251e2c8','release_commit':'a2493c85639780a9ca2b2a7121db85605b659c92','pages':doc.page,'topics':len(pages),'bookmarks':doc.seen,'image_uses':actual_images,'pagination_mismatches':wrong},indent=2))
    print(json.dumps({'pdf':str(OUT),'pages':doc.page,'topics':len(pages),'images':len(actual_images),'pagination_mismatches':wrong}))
    if wrong:raise RuntimeError('Fix overflow pages before delivery')

if __name__=='__main__':build()
