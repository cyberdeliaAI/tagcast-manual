+++
id = "split-an-album-deliberately"
group = "CLEAN UP"
title = "Split an album deliberately"
lead = "Move a reviewed subset into a new album without rewriting its track metadata."
wiki = "Split-albums"
+++

::: figure figure-043
Earlier 1.6.5 capture: inspect selected and retained tracks before splitting. Current text describes 1.9.0.
:::

**1.**  Choose **More > Split album** on one native disc with 2-500 active tracks. Combine sets must be off; unsupported additional album credits block the operation.

**2.**  Select a proper subset, check destination metadata and review the complete source/destination membership. Proposals never select tracks automatically.

**3.**  Confirm the reviewed split once. Creation and movement are separate remote steps; both albums are read back. Track metadata and numbers are preserved unless the reviewed operation explicitly says otherwise.

::: callout
A split is not transactional

An empty or partial destination can remain after an uncertain creation/movement. Do not repeat blindly. Inspect both albums and the retained report; there is no metadata Undo for this operation.
:::
