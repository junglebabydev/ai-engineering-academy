# Edition 02 verification — 28 October 2026

The subject areas remain unchanged. The default teaching path is now beginner-oriented and centred on one Jungle parent concierge agent. Original technical content remains optional. No private Jungle source code or real customer records are included in the course or fixture pack.

## Core browser verification

`verify.py` exercises all 36 lesson routes and all 72 new quiz questions; wrong answers and retries; persistence of notes/completion/quiz state/checklists; search and safe text handling; four technical labs; JSON export/import rejection, reset and restore; standalone HTML download; phone/tablet/desktop layout and navigation; and visible storage-denial fallback.

Direct file mode checks that the app makes no HTTP requests. Local HTTP mode checks that the worker controls the page, the page reloads with networking disabled, and lesson 36 remains available offline. There are no JavaScript runtime errors in these checks. Reference links are optional online resources.

## Beginner-edition verification

`verify_beginner.py` checks:

- Earlier-edition progress is archived and new content does not inherit old completion/mastery.
- Earlier notes render as text and can be exported separately.
- Activity and recall writing survives reload and appears in recall practice.
- Worked checks and technical depth begin collapsed.
- Workshop results enforce age, budget, area and interest; missing age prompts clarification.
- Unknown prices are not treated as free; insufficient budgets produce no matches.
- Unavailable tools and prohibited requests yield bounded, explicit outcomes.
- The ZIP generated in the browser passes a ZIP integrity check and matches every supplied build-pack file byte-for-byte after text decoding.
- Catalogue CSV download, current-edition backup round-trip, legacy import, malformed writing-map rejection, and old-tab save protection.
- New views fit widths 390, 768 and 1440; no page-wide horizontal overflow.
- Supplied search/details scripts execute against a simulated n8n `$input` object and pass known-match, invalid/missing age, budget/no-match, unknown-price, unknown-area and invented-ID tests.

## Upgrade verification

`verify_upgrade.py` loads the published edition-1 HTML and worker from the pinned repository history, saves earlier notes, installs edition 2, and confirms that new content starts fresh while old notes remain archived. It also reloads the new edition offline with a saved worksheet. This check requires the Git repository history and a local HTTP preview. Summary: `verification-upgrade.json`.

## Concept-first revision checks

`verify_concepts.py` checks all 36 definitions and core explanations are project-independent, that all original technical topics remain, and that every rendered lesson puts definition, mechanism, everyday example and concept practice before a separate collapsed Jungle application. It also checks existing edition-2 progress and writing are retained, lesson navigation expands the project, responsive layout, and runtime errors. Summary: `verification-concepts.json`.

## Verification scope

The browser workshop is a scripted rehearsal, not an LLM. The supplied tool scripts are tested as pure Code-node logic. An actual n8n instance, credential setup, AI Agent wiring and model-chosen tool calls were not run in this environment. They are explicit learner build steps with acceptance checks in the guide. No production Jungle API, availability, reservation, payment or private data access was tested or connected.

Jungle code review informed the distinction between marketplace discovery, draft booking choices, session information and protected booking records. It does not establish the current behaviour of deployed services. Public examples are fictional and no live capacity/price promises are made.

The tests use Chrome. Other browsers and private modes can handle file storage differently. Caches can be evicted. Use JSON backups, close old academy tabs, and revisit online for a new edition. No public load capacity, real-world model quality, booking safety or job outcome is claimed by these website checks.

Raw summaries: `verification-file.json`, `verification-hosted.json`, and `verification-beginner.json`.
