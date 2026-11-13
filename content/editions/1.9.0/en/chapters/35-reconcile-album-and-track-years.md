+++
id = "reconcile-album-and-track-years"
group = "CLEAN UP"
title = "Reconcile album and track years"
lead = "A difference can be intentional. Choose which known year to apply and where."
wiki = "Album-and-track-years"
+++

::: figure figure-017
Development example with fictional metadata, captured before 1.1.0. The year choice is explicit; it does not automatically use the oldest or majority value. Cropped detail from the original screenshot.
:::

In Cleanup, select **Album and track years > Analyse years**. It compares the already-loaded library without audio or provider searches. Filter/search differing, mixed, missing or invalid years.

::: table {"widths": [0.43, 0.57], "headers": true}
| Action | Scope |
| --- | --- |
| Album year to track years | Apply the known album year to every track; keep the album year. |
| Track year to album year | Apply the chosen known track year to the album only. |
| Track year to album + all tracks | Use the chosen known track year for both; matching tracks need no write. |
:::

::: small
For album 2013 with tracks at 2007 and 2013, choose 2007 and the album-plus-tracks action if all should become 2007. Mixed track years require a choice. The normal review/save opens; after confirmed read-back the comparison refreshes in the same window. Checking may take time because it verifies against the full library.
:::
