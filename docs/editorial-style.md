# Editorial style

Use this guide for new prose and explicitly approved revisions in later editions
and supporting documentation. Use a clear, professional tone with direct,
practical instructions. Keep repository documentation and the English manual in
English; communicate with the maintainer in Dutch.

The 1.7.0 reference edition is fixed. Do not rewrite its chapters, captions or
cover copy, replace its images, or refresh its layout and visual references to
apply these style preferences. Keep its historical labels and provenance intact.

## Write for the task

- Start with the reader's action or the information needed to make a decision.
  Prefer familiar words and concrete verbs to promotional or abstract wording.
- Remove filler, repetitive summaries, rhetorical hooks and conversational
  leftovers such as "Great question" or "I hope this helps".
- Prefer active voice when the actor is known. Keep the actual actor accurate:
  Tagcast, iBroadcast and the user can perform different parts of an operation.
  Do not introduce an actor or capability just to make a sentence active.
- Split sentences that combine several actions or conditions. Vary sentence
  length and openings, and keep related explanations together. Word counts are
  prompts for review, not mechanical limits.
- Edit only what improves understanding. Leave clear sentences alone. Preserve
  useful headings, steps, lists and links instead of restructuring for variety.
- English contractions are acceptable when unambiguous. Keep full forms where
  they make a prohibition, requirement or warning clearer. Avoid slang and
  artificial conversational touches. In Dutch, keep the form of address
  consistent and use sentence case for headings.

## Preserve technical meaning

- Preserve facts, numbers, limits, defaults, version availability, scope and the
  original level of certainty. Never turn "may" into "will", a proposal into an
  available feature, or an unverified result into a confirmed one.
- Retain exact product names, technical terms, visible button labels, Settings
  paths, source attribution and licence notices. Preserve quoted text, code,
  commands, identifiers, URLs, filenames and data-table values unless their
  change is explicitly part of the approved work.
- Keep draft, review, saving, checking, confirmed, failed and unconfirmed states
  distinct. Preserve the difference between local changes and iBroadcast writes,
  and between metadata edits, playback and file transfers.
- Keep prerequisites, consent, explicit Start/Save actions, stop conditions,
  uncertainty guidance and recovery limits. Concision must not remove safeguards
  or imply automatic retries, automatic publication or broader compatibility.
- Use accurate technical contrasts when they explain a choice or boundary.
  Treat suggested words and sentence patterns as review prompts, not bans.
  Punctuation, semicolons and serial commas may stay when they prevent ambiguity.
  Preserve punctuation within technical content and quotations.
- Keep emphasis purposeful, especially for control labels and decisions. Avoid
  decorative emoji and scattered bold text that distract from the instructions.

## Review before accepting changes

1. Inspect the wording diff against the approved scope. Check for lost conditions,
   changed actors, stronger claims and altered instructions.
2. Keep the Wiki canonical. Functional corrections follow its own review process
   before entering a later PDF snapshot. Check claims against the relevant
   released source and evidence; release notes alone do not establish behavior.
3. Check exact labels, links, values, attribution and historical screenshot states.
   Do not imply that a review or running operation shows a completed save.
4. Apply the [authoring contract](authoring.md) and validate the affected edition's
   rendering after approved content changes. Investigate layout differences;
   never loosen checks or overwrite the 1.7.0 baseline to accommodate a rewrite.
5. Follow the separate [publishing boundaries](publishing.md). Editorial approval
   does not authorize publication. Builds and CI do not rewrite prose.

Selected principles are adapted from the maintainer-supplied *Humanize Text*,
version 1.2, by Wilfred Helmig. The professional tone and technical-preservation
rules above govern their use in Tagcast documentation.
