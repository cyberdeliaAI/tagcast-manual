+++
id = "use-the-cache-and-refresh-deliberately"
group = "BROWSE"
title = "Use the cache and refresh deliberately"
lead = "Read-only browsing remains useful during a temporary library-service outage."
wiki = "Browsing-and-discovery#cached-browsing-and-library-refresh"
+++

Since 1.7.0, ordinary category/page requests, favourites, tags and history restoration use the valid, already loaded account library. They do not ask iBroadcast for status on every browse action. Switching or disconnecting accounts invalidates inappropriate cached state.

Use **Reload library** for changes made elsewhere. Explicit refresh, fresh checks before remote writes and read-back after successful or uncertain writes are retained. A cached view is not proof that an outstanding mutation succeeded.

::: figure figure-028
1.7.0: Overview with the maintainer's supplied account redaction retained. Global service status is separate from this account's connection.
:::

::: callout
An outage has boundaries

A loaded snapshot can keep browsing working, but cannot make streaming, provider lookups or remote saves work offline. Pending checks are not confirmations; failed read-back leaves the outcome unconfirmed.
:::
