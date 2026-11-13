+++
id = "review-metadata-cleanup"
group = "CLEAN UP"
title = "Review metadata cleanup"
lead = "Analyse first, inspect every proposed change, then approve bounded processing."
wiki = "Metadata-cleanup"
+++

::: figure figure-016
Earlier development interface: choose one exact genre label and proposed replacements. Preparing this review changes nothing. Cropped detail from the original screenshot.
:::

**1.**  Open **Overview > Metadata health > Clean up metadata**. Choose combined genres, album artists, track artists, composers or **Review genre labels**.

**2.**  Prepare the preview. Semicolon cleanup splits only semicolons. Slashes, commas and ampersands are preserved rather than guessed as separators.

**3.**  For an exact genre replacement, choose the existing label and replacements. Removing a label requires the explicit removal option. Review/exclude albums before approving.

**4.**  Start only the reviewed selection. Tagcast checks and reads back each batch before continuing. Stop prevents later requests; already accepted writes may complete.

Cleanup reports belong to the current account and persist on this computer. Export a report for your records. Resume explicitly and check outstanding work first; uncertain writes are not resent automatically. Album-artist cleanup requires Combine Multi-Disc Album Sets off. There is no automatic batch Undo.
