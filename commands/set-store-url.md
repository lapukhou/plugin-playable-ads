---
description: Set or replace the app store URL in a playable ad HTML file. Defaults to the Clever Brain Training Games App Store URL when no URL is given.
argument-hint: [store-url] [path/to/playable.html]
---

# /set-store-url

Set the store URL in a playable ad to the requested value. This command only
swaps the URL value — it never changes function names, MRAID logic, or
anything else in the file.

## Arguments

Both arguments are optional and may be given in any order: $ARGUMENTS

- `store-url`: the first argument that looks like an `http(s)://` URL.
  Default when omitted:
  `https://apps.apple.com/us/app/clever-brain-training-games/id1599756543`
- `path/to/playable.html`: the first argument that looks like a file path.
  When omitted, find playable HTML files (`*.html` in the current directory
  and `build/`). If exactly one candidate exists, use it; if several exist,
  list them and ask which one to update.

## Workflow

1. Read the target HTML file.
2. Replace every occurrence of the store URL, wherever it appears:
   - the `YOUR_STORE_URL` placeholder
   - URL literals inside `mraid.open('...')` and `window.open('...', ...)` calls
   - URL literals assigned to store-URL variables (e.g. `var storeUrl = '...'`,
     `var url = '...'` inside install/CTA handlers)
3. Report how many occurrences were replaced and in which contexts.
4. If the plugin's validation script is available, run it on the updated file
   (`skills/playable-ads-creator/scripts/validate_playable.py` relative to the
   plugin root, or `${CLAUDE_PLUGIN_ROOT}/skills/playable-ads-creator/scripts/validate_playable.py`
   in Claude Code) and summarize the result.

## Guardrails

- Only replace app-store links (apps.apple.com, play.google.com) and the
  `YOUR_STORE_URL` placeholder — do not touch unrelated URLs.
- If the file contains no placeholder and no recognizable store URL, say so
  and show where the CTA click handler is, instead of guessing.
- Do not reformat or minify the file as a side effect.
