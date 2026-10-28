# Verification

Verified on 27 October 2026 using installed Google Chrome with Playwright in a fresh, isolated browser profile. No live model or database credentials were used. No public hosting deployment was performed.

## Passed: standalone HTML

23 checks covered:

- 36 substantive lessons, 72 questions, 40 glossary entries and valid internal reference keys.
- All 36 lesson routes and every correct quiz submission.
- Wrong-answer explanations, retries and updated quiz mastery.
- Completion, quiz answers, notes and project checklists persisting through reload.
- Global search, no-match states and escaped untrusted search content.
- Deterministic rank-fusion, bounded-agent, cost/concurrency and retrieval-metric calculations.
- Invalid lab input handling.
- JSON export, invalid format and invalid quiz-value rejection, reset and valid restore.
- A downloaded standalone HTML copy opening independently.
- No page-wide horizontal overflow across eight views at widths 390, 768 and 1440 pixels; mobile menu open/close.
- Zero HTTP requests in direct file mode.
- Zero JavaScript runtime errors.
- A visible warning and usable lessons when localStorage access is blocked.

## Passed: local HTTP hosted edition

The same functional checks passed under a local HTTP server (23 checks). The mode-specific check confirmed that the service worker installs, controls the page, reloads while browser networking is disabled, and allows navigation to lesson 36 offline.

## Supplemental checks

- JavaScript and service-worker syntax checked with Node.
- Content-hashing snippet preserves literal regex/newline escapes.
- Canceling a valid progress import preserves the current state.
- Import file chooser is exposed through a keyboard-focusable button.
- Mobile navigation is fully offscreen when closed.
- An explicit `/index.html` URL also reloads offline through the worker.
- Desktop and mobile layouts were visually inspected; the lesson reader, code blocks, quizzes and notes are legible and arranged vertically on phones.

## Scope and limits

The tests validate the academy website and its deterministic demonstrations. The educational TypeScript/SQL snippets are examples, and some explicitly require user-provided adapters; they are not a complete live capstone application. Real model quality, database permissions, third-party API behavior, load capacity and user-built projects were not tested. Browser code blocks may scroll horizontally inside their own containers on small screens.

Verification used Chrome. File-storage persistence can differ in Safari, Firefox and private browsing. Use JSON backups. Service-worker caches can be evicted and require an initial online visit. External references require the internet; their content is not bundled. Live hosting vendor dashboards and account settings may change.

Raw check summaries are included in the editable source archive as `verification-file.json` and `verification-hosted.json`. `verify.py` runs functional checks against a file URL by default or an HTTP URL supplied as its first argument; it needs Python Playwright and installed Chrome. It creates temporary test backups and screenshots in its own directory.
