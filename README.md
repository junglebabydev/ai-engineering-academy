# AI Engineering Academy — Jungle parent concierge edition

[Open the academy](https://junglebabydev.github.io/ai-engineering-academy/?edition=2) · [Start lesson 1](https://junglebabydev.github.io/ai-engineering-academy/?edition=2#lesson/1)

Learn the complete AI engineering curriculum by gradually building a parent-facing activity concierge. Designed for a learner familiar with ChatGPT, spreadsheets, website builders, Zapier or n8n, without assuming a programming background. The existing editorial design is retained.

## The same six curriculum areas

1. LLM and ML foundations.
2. RAG, search and retrieval.
3. Agents, tools, MCP, multimodal inputs, memory and harnesses.
4. Evaluation, observability and regression testing.
5. Production reliability, security, privacy and cost.
6. System design, capstone, business assessment and interview practice.

Each of the 36 lessons has a parent scenario, plain-language explanation, analogy, two defined terms, a worked comparison, a short activity with a self-check, a build card, two quiz questions with explanations, and a recall/explanation prompt. Linked reminders revisit earlier lessons. The original technical explanations and examples remain collapsed as optional depth. Six cumulative milestones build one concierge agent rather than six unrelated projects.

The Jungle connection is informed by a review of the user-provided marketplace and booking-system repositories, plus related agent/search/tool code. The public course uses original explanations and fictional records, not copied private source code, credentials or customer records. Code review is not a verification of production behaviour.

## Open offline

Open **index.html** in a modern browser with JavaScript enabled. All lesson explanations, exercises, quizzes, glossary, search, recall practice, the workshop, and the complete downloadable build pack are embedded. No account, CDN, font download, API key or server is needed for the academy itself.

The **Agent workshop** is an explicitly labelled deterministic simulation. It demonstrates clarification, strict filtering, supported recommendations, missing information, tool failure and denied actions. It does not call a model or access live Jungle data. The advanced labs cover rank fusion, bounded loops, cost/capacity and retrieval metrics.

## Build a real tool-using agent

Open Agent workshop and download the build pack. It contains:

- `BUILD-GUIDE.md`: a staged n8n build, tool-first tests, wiring checks and acceptance steps.
- `AGENT-BRIEF.md`: parent-concierge instructions and boundaries.
- `activities.csv` / `catalogue.json`: seven fictional activity records with sources and unknown availability.
- `search-activities.js`: ready-to-copy JavaScript for an n8n Code node in a callable search workflow.
- `get-activity-details.js`: a read-only ID lookup for a second callable workflow.
- `parent-tests.csv`: twelve parent scenarios and expected behaviours.

The learner creates the tool workflows and connects Chat Trigger, AI Agent, a supported chat model and Call n8n Workflow Tool nodes. A tool-call execution trace is required to demonstrate actual model-selected tool use. The pack is guidance and tested tool logic, not a preconfigured n8n workflow import. Live n8n/model wiring was not executed as part of website verification. Interfaces and credentials depend on the learner's installation.

Live model calls, n8n setup, optional packages, external readings and future production integration require internet and may incur service charges. The first agent is read-only. There are no connected booking, payment, messaging or private-data tools. A real Jungle integration requires separate access review, current API contracts, verified availability semantics and operational testing.

## Progress and edition migration

Completion, latest quiz attempts, activity worksheets, recall answers, notes and project checklists use localStorage. It is scoped to a browser profile and origin. File-URL persistence varies with browser, path and privacy settings. If saving fails, the page warns and the session remains usable.

Use **Progress & setup → Export progress JSON** regularly. Import validates the data and asks before replacing current progress. New exports include any archived earlier-edition progress. Notes can contain personal information; handle backups appropriately.

Edition 1 notes, completion and quiz records are preserved as a separate archive when loaded or imported. They are not counted as completion or mastery of rewritten content. The archive can be read and separately exported from Progress & setup. Old-tab storage events are handled to keep an earlier tab from replacing new worksheets while the new edition is open. Close old academy tabs and revisit online when upgrading; keep a JSON backup.

Lesson completion is self-attested. Quiz mastery means both latest submitted answers are correct. Written activities and recall answers are saved but are not automatically graded or a certificate.

## GitHub Pages and updates

This repository publishes **main / root** to GitHub Pages. Hash routes work under the repository subpath. There is no server runtime or deployment build command.

To edit the teaching content, modify `rewrite_curriculum.py`, then run:

```sh
python3 rewrite_curriculum.py
python3 build.py
```

The authoring script uses `technical-foundations.json` as its retained original reference. The generated `curriculum.json` is embedded along with `beginner.js`, `beginner.css`, and all files in `agent-build-pack/` into one `index.html`. `template.html` holds the common layout, navigation, storage and utilities. If editing only presentation or build-pack files, run `python3 build.py`.

Bump `CACHE_VERSION` in `sw.js` for a new published edition. Commit generated HTML with its sources. GitHub Pages publishes the revision. The single-file app allows a new worker to activate once its full page is cached; reload online to obtain a new edition. Save progress first.

For another host, publish `index.html` and `sw.js` together. Netlify can deploy that directory with no build command. Vercel can use the Other preset and root output directory. GitHub branch publishing includes `.nojekyll`.

Official deployment guides: [GitHub Pages](https://docs.github.com/en/pages/quickstart), [Netlify](https://docs.netlify.com/deploy/create-deploys/), [Vercel](https://vercel.com/docs/deployments).

## Hosted offline behaviour

On HTTPS or localhost, `sw.js` caches the complete page after an initial successful online visit. Check **Progress & setup** for “Hosted offline cache ready”, then disconnect and reload. First-ever offline visits cannot work; browsers may evict cached data. The standalone HTML is the durable portable copy. External reading pages are links, not bundled copies.

Optional local HTTP preview: `python3 -m http.server 8081`, then open `http://localhost:8081`.

## Verification

See `VERIFICATION.md`. `verify.py` covers the core site in direct-file and HTTP modes. `verify_beginner.py` covers migration, worksheet/recall persistence, workshop outcomes, offline build-pack integrity and supplied Code-node logic. They require Python Playwright and installed Chrome. Browser profiles are isolated and test data is fictional. Tests create ignored temporary downloads and screenshots.
