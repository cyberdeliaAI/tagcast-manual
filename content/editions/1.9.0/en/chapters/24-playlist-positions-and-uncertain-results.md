+++
id = "playlist-positions-and-uncertain-results"
group = "ORGANISE"
title = "Playlist positions and uncertain results"
lead = "Appending and exact-position editing have different contracts."
wiki = "Playlists#appending-and-duplicate-positions"
+++

::: figure figure-044
1.7.0: original positions with zero changes; Save order is disabled until a change is made.
:::

Use Reorder tracks for an exact-position change. Drag a handle, use Up/Down or Move to position, inspect the complete resulting order and save once. Search and pagination must not hide which occurrence you selected. This workflow retains repeated and unavailable positions; changing playlist order does not change the current play queue.

::: callout
Append and existing duplicates - known limit

The exact iBroadcast append behaviour for a destination containing intentional repeated positions remains unverified (F2-02). Do not assume append preserves them. Create/append reduce the selected incoming IDs to their first occurrence; this is separate from exact-position reorder/replacement.
:::

::: small
An uncertain creation or append is checked rather than automatically retried. Inspect the actual list before preparing another mutation. A matching playlist name alone does not prove that a particular creation succeeded. A failed read-back leaves an unknown outcome, not proof of failure.
:::
