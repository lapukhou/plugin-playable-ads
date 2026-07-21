# Playable Ads Plugin

A Claude Code plugin for creating production-ready HTML5 playable ads for mobile game user acquisition.

## What it does

Provides one skill, **playable-ads-creator**, which Claude activates automatically when you ask to build, create, or optimize playable ads, interactive ads, or HTML5 game ads. It covers the full workflow:

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
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── playable-ads-creator/
        ├── SKILL.md
        ├── references/      # Network specs, AppLovin compliance, game mechanics patterns
        ├── scripts/         # generate / optimize / integrate / validate (Python 3, stdlib only)
        └── assets/          # Reserved for custom per-project art
```

## Installation

Install from a marketplace that lists this plugin, or add it locally:

```
/plugin install playable-ads
```

## Usage

Just ask Claude, for example:

- "Create a match-3 playable ad for AppLovin, 30 seconds of gameplay"
- "Optimize this playable for AdMob's 2MB limit"
- "Add ironSource MRAID integration to my playable ad"

## Requirements

- Python 3 (scripts use only the standard library)
