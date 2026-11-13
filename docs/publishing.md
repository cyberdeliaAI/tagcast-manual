# Publishing boundaries

No command or workflow in this repository pushes to the Wiki, uploads a release,
modifies Tagcast, contacts iBroadcast or uses account credentials. CI has only
read access to repository contents and retains candidate review artifacts for
14 days. CI success is validation, not publication approval.

The existing Wiki owns the published manual downloads under `manuals/` and the
`PDF-manual` page. The application README and product website continue to point
there. Never replace the historical 1.4.0 or 1.7.0 files as a side effect of a
build, and never attach manual validation to application release gates.

For an explicitly approved future publication, prepare the candidate PDF,
SHA-256, deterministic source manifest, validation/reproducibility reports and a
reviewable Wiki page change. Record the exact manual Git commit and input
manifest hashes in the publication record. Get approval for that concrete bundle
before writing to the Wiki. Editorial approval and publication approval are
separate decisions.

The initial milestone delivers the independently reproducible 1.7.0 reference
edition only. Release-difference analysis, proposed chapter/screenshot updates
and approval-bound content updates remain the next milestone. Release notes
must never be the sole evidence for a functionality claim.
