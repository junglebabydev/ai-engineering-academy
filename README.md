# AI Engineering Academy

A self-contained six-week study site for a TypeScript / Next.js / Supabase developer.

## Open offline

Double-click **index.html** and open it in a modern browser with JavaScript enabled. All 36 lessons, 72 interactive questions, 40 glossary definitions, six project briefs and four experiments are embedded. No installation, account, CDN, API key or network request is needed in file mode.

The academy is a learning site. Its project briefs guide you through building a support copilot; the download is not a prebuilt support-copilot application. Code snippets are teaching examples. TypeScript/SQL examples run in your own development environment; explicitly labeled adapters and pseudocode need your implementations. External readings and live model/database integrations require internet access. Offline fixture work and browser experiments do not.

## Save progress

Completion, latest quiz answers, lesson notes and project checklists use localStorage. This is specific to your browser profile and origin. File URL storage can vary between browsers, paths and private browsing sessions. The page displays a warning if saving fails; you can still use the current session and export a backup.

Open **Progress & setup → Export progress JSON** regularly. Import validates the schema before asking to replace current progress. Invalid backups preserve existing state. Export before importing if you need to retain both records. Notes are personal data: protect the backup accordingly. Hosted and local editions have separate storage; move progress between them using JSON.

Lesson completion is self-attested. Quiz mastery means both latest submitted answers in a lesson are correct. Neither is a certificate or a substitute for doing the project acceptance checks.

## Deploy

Publish the folder containing `index.html` and `sw.js`. There is no build command and no server runtime.

- **Netlify:** use a manual deploy and drag in the extracted folder; or connect a repository, leave the build command empty, and use `.` as the publish directory.
- **Vercel:** import a repository, set the site folder as the project root, choose **Other**, leave the build command empty, and serve the root output directory (`.`). Confirm `index.html` is at the published root.
- **GitHub Pages:** commit `index.html`, `sw.js` and `.nojekyll` at the repository root. In Settings → Pages, select deployment from the branch and root folder. Hash routes work at repository subpaths without rewrites.

Official guides: [Netlify](https://docs.netlify.com/deploy/create-deploys/), [Vercel](https://vercel.com/docs/deployments), [GitHub Pages](https://docs.github.com/en/pages/quickstart).

For a local HTTP preview, run `python3 -m http.server 8080` in this folder and open `http://localhost:8080`. This command is optional; the standalone HTML opens directly.

## Hosted offline behavior

On HTTPS or localhost, `sw.js` caches the complete HTML after the first successful online visit. Check **Progress & setup** for “Hosted offline cache ready.” Then disconnect and reload to verify your browser's cache. A first-ever visit without a connection cannot work. Browsers may evict cached files, so save the standalone HTML as the durable offline copy.

For an update, replace `index.html` and increment `CACHE_VERSION` in `sw.js`. A new worker waits until old site tabs close. Close all tabs for the site and reopen online. Existing progress remains on the same origin and storage key. No background sync, analytics or cross-device service is included.

## Study rhythm

Plan around 6–10 hours/week, including six lesson sessions and project work. Each week contributes a milestone to the support-copilot capstone:

1. LLM/ML foundations and a typed answer contract.
2. Versioned ingestion, permission-aware RAG and hybrid retrieval.
3. Tools, bounded agent loops, MCP, multimodal evidence and harnesses.
4. Datasets, grading, trace analysis and regression gates.
5. Reliability, security, privacy, cost and operational readiness.
6. Architecture, capstone integration, design review and interview practice.

Official and original-research references were checked on 27 October 2026. The site avoids hard-coded current model names or real provider prices. Pricing defaults in the cost lab are hypothetical. Recheck live API schemas, protocol revisions and hosting settings before a production integration.

## Files

- `index.html`: the complete portable academy, including CSS, JavaScript and curriculum.
- `sw.js`: optional service worker for hosted offline reloads.
- `.nojekyll`: plain static publishing on GitHub Pages.
- `README.md`: opening, hosting and backup instructions.
- `VERIFICATION.md`: checks and their scope.

The companion source archive includes `template.html`, `curriculum.json`, `build.py` and `verify.py`. To regenerate after editing content or presentation, run `python3 build.py`. There are no Python dependencies for generation. Browser verification uses Playwright.
