---
description: Set or replace the app store URL in a playable ad HTML file
argument-hint: [store-url] [path/to/playable.html]
---

Set the store URL in a playable ad to the requested value.

Arguments (both optional, in any order): $ARGUMENTS

- **Store URL** — the first argument that looks like an `http(s)://` URL.
  If none is given, use the default:
  `https://apps.apple.com/us/app/clever-brain-training-games/id1599756543`
- **Target file** — the first argument that looks like a file path.
  If none is given, find playable HTML files (`*.html` in the current directory and `build/`).
  If exactly one candidate exists, use it. If several exist, list them and ask which one to update.

## Steps

1. Read the target HTML file.
2. Replace every occurrence of the store URL, wherever it appears:
   - the `YOUR_STORE_URL` placeholder
   - URL literals inside `mraid.open('...')` and `window.open('...', ...)` calls
   - URL literals assigned to store-URL variables (e.g. `var storeUrl = '...'`, `var url = '...'` inside install/CTA handlers)
   Only replace app-store links (apps.apple.com, play.google.com) and the placeholder — do not touch unrelated URLs.
3. Do NOT change function names, MRAID logic, or anything else — this command only swaps the URL value.
4. Report how many occurrences were replaced and in which contexts.
5. If the plugin's validation script is available, run it on the updated file:
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/playable-ads-creator/scripts/validate_playable.py <file>`
   and summarize the result.

If the file contains no placeholder and no recognizable store URL, say so and show where the CTA click handler is, instead of guessing.
