+++
id = "close-and-restart-safely"
group = "GET STARTED"
title = "Close and restart safely"
lead = "Keep accepted changes visible until their checks finish."
wiki = "Getting-started#closing-and-restarting-safely"
+++

**1.**  Quit or close the desktop app normally. Since 1.7.0, playback pauses and interruptible work stops while accepted changes, read-back and required local storage finish.

**2.**  If this takes time, the **Finishing Tagcast** window remains visible. A second launch brings that window forward; it does not create another backend or resend a save.

**3.**  If offered, **Keep Tagcast open** returns to the same session and drafts. Accepted checks continue, but playback, transfers and Cleanup remain stopped until you explicitly act.

**4.**  Wait for the owned backend to finish before replacing the app. Source/CLI users stop their server with Ctrl+C and wait. A desktop window leaves a compatible server it only reused running.

::: callout
Do not force a critical save to finish

There is no blanket deadline that kills an accepted remote mutation. Files already sent may still arrive. If progress genuinely stalls, retain the exact phase/message and inspect the result before trying a new mutation.
:::

Closing a browser tab does not stop its Python server. The same no-blind-retry rule applies after an interrupted or uncertain operation. An ordinary restart can restore the bounded local queue but never automatically resumes audio or transfers.
