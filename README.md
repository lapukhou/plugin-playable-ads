# Playable Ads Plugin

A Codex and Claude Code plugin for creating production-ready HTML5 playable ads for mobile game user acquisition.

## What it does

Provides one skill, **playable-ads-creator**, which activates automatically when you ask to build, create, or optimize playable ads, interactive ads, or HTML5 game ads. It covers the full workflow:

1. **Generate** a single-file HTML5 game prototype (`match3`, `runner`, or `bubble` templates)
2. **Implement** game logic with touch-optimized, 60 FPS patterns
3. **Optimize** for production — minify, inline assets as base64, strip debug code
4. **Integrate** network-specific MRAID and click-tracking code
5. **Validate** against network requirements before delivery

## Supported ad networks

| Network | Size limit | Notes |
|---|---|---|
| Unity Ads | 5MB | .zip package, mraid.js reference |
| ironSource | 5MB | MRAID 2.0, viewableChange events |
| Google AdMob | 2MB rec. / 5MB max | MRAID, 5s load budget |
| AppLovin | 5MB | mraid.open() clicks, both orientations, interaction-gated timers |
| Meta Audience Network | 5MB | Single file, FbPlayableAd hooks |

## Structure

```
plugin-playable-ads/
├── .agents/plugins/marketplace.json       # Codex marketplace manifest
├── .claude-plugin/
│   ├── marketplace.json                    # Claude Code marketplace manifest
│   └── plugin.json                         # Claude Code plugin manifest
├── .codex-plugin/plugin.json               # Codex plugin manifest
├── commands/set-store-url.md               # /set-store-url slash command (Claude Code + Codex)
└── skills/playable-ads-creator/            # Shared skill and resources
```

## Installation

### Codex

Add this repository's marketplace, then install the plugin:

```bash
codex plugin marketplace add /path/to/plugin-playable-ads
codex plugin add playable-ads@plugin-playable-ads
```

### Claude Code

This repository is also a Claude Code marketplace (`plugin-playable-ads`). Add it and install the plugin:

```
/plugin marketplace add lapukhou/plugin-playable-ads
/plugin install playable-ads@plugin-playable-ads
```

For local development, point the marketplace at the checkout instead:

```
/plugin marketplace add /path/to/plugin-playable-ads
```

## Usage

Just ask, for example:

- "Create a match-3 playable ad for AppLovin, 30 seconds of gameplay"
- "Optimize this playable for AdMob's 2MB limit"
- "Add ironSource MRAID integration to my playable ad"

### Commands (Claude Code and Codex)

- `/set-store-url [store-url] [path/to/playable.html]` — set or replace the app store URL in a playable ad. Both arguments are optional: with no URL it uses the default ([Clever: Brain Training Games](https://apps.apple.com/us/app/clever-brain-training-games/id1599756543)); with no path it finds the playable HTML automatically.

## Requirements

- Python 3 (scripts use only the standard library)
