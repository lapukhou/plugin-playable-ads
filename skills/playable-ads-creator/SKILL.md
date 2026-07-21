---
name: playable-ads-creator
description: Create production-ready HTML5 playable ads for mobile game user acquisition. Use when the user asks to build, create, or develop playable ads, interactive ads, HTML5 game ads, demo ads for app marketing, or needs to optimize ads for networks like Unity Ads, ironSource, Google AdMob, AppLovin, or Facebook Audience Network. Handles single-file HTML packages, MRAID integration, asset optimization, and network-specific requirements.
---

# Playable Ads Creator

Create production-ready HTML5 playable ads optimized for mobile game user acquisition across major ad networks.

## Workflow

### 1. Gather Requirements

Ask the user for:
- **Game type**: Match-3, bubble shooter, runner, puzzle, merge, idle, etc.
- **Core mechanic**: The primary interaction (swipe, tap, drag, tilt)
- **Duration target**: Typically 10-30 seconds of gameplay
- **Target network**: Unity Ads, ironSource, AdMob, AppLovin, Meta Audience Network
- **File size limit**: Usually 2-5MB depending on network
- **CTA approach**: Install button timing, win/lose scenarios

If not provided, use sensible defaults for the game type and ask only critical clarifications.

### 2. Create Initial Prototype

Build a working HTML5 prototype with:
- Single-file architecture (index.html with inline CSS/JS)
- Core game mechanics implemented
- Touch-optimized controls
- Clear visual feedback
- Basic tutorial/onboarding

Use `scripts/generate_playable_template.py` to initialize the base structure:

```bash
python3 scripts/generate_playable_template.py match3 --output ./build
```

Bundled templates: `match3`, `runner`, `bubble`. For other genres (puzzle, merge, idle), start from the closest template and adapt patterns from `references/game-mechanics-patterns.md`.

### 3. Implement Game Logic

Focus on:
- **Responsive gameplay**: 60 FPS target on mobile devices
- **Touch handling**: Support both touch and mouse for testing
- **Game states**: Loading → Tutorial → Playing → End → CTA
- **Satisfying feedback**: Visual effects, animations, sound
- **Win condition**: Clear, achievable goal within 15-20 seconds

Reference `references/game-mechanics-patterns.md` for common implementations.

### 4. Optimize for Production

Run `scripts/optimize_playable.py` to:
- Minify HTML, CSS, JavaScript
- Convert images to base64 or optimized inline SVG
- Inline audio as base64 data URIs (or remove if size constrained)
- Remove console logs and debug code
- Compress and validate file size

```bash
python3 scripts/optimize_playable.py build/match3_playable.html
```

### 5. Add Network-Specific Features

Use `scripts/add_network_integration.py` for:
- **MRAID support** (ironSource, AdMob require this)
- **Click tracking** with network-specific parameters
- **Package format** (Unity Ads requires specific .zip structure)
- **Orientation lock** or responsive handling
- **Store URL integration** for CTA button

```bash
python3 scripts/add_network_integration.py build/match3_playable_optimized.html applovin --store-url "https://apps.apple.com/app/id123456789"
```

Reference `references/network-requirements.md` for specifications.

**CRITICAL for AppLovin/AXON**:
- MUST use `mraid.open(url)` for click-throughs (NOT window.open)
- MUST support both landscape AND portrait orientations
- MUST wait for `mraid.ready` event before initialization
- Timer MUST start only after first user interaction
- Audio MUST be muted until first interaction
- See `references/applovin-compliance.md` for complete checklist

### 6. Testing Checklist

Before delivery, verify:
- Works offline (no external requests)
- File size under network limit
- Touch events properly bound
- No console errors
- CTA button clickable and prominent
- Loads in under 3 seconds
- Runs smoothly on mid-range devices (test in Chrome DevTools mobile simulation)
- Portrait and landscape support (if needed)

Use `scripts/validate_playable.py` for automated checks:

```bash
python3 scripts/validate_playable.py build/match3_playable_optimized_applovin.html
```

For on-device testing, serve the build directory with `python3 -m http.server 8000` and open it from a phone browser on the same network.

## Technical Guidelines

### File Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <style>/* Inline all CSS */</style>
</head>
<body>
    <canvas id="game"></canvas>
    <script>/* Inline all JavaScript */</script>
</body>
</html>
```

### Performance Patterns

- Use `requestAnimationFrame` for game loop
- Minimize DOM manipulations
- Use CSS transforms instead of position changes
- Implement object pooling for particles/effects
- Lazy-load non-critical assets

### Common Pitfalls to Avoid

- External dependencies (CDNs, fonts, libraries)
- Large uncompressed images
- Complex physics that lag on mobile
- Unclear tutorial or first interaction
- CTA appearing too early or too late
- Not handling touch events (only mouse)
- Portrait-only design when landscape needed

## Network-Specific Requirements

| Network | Size limit | Key requirements |
|---|---|---|
| Unity Ads | 5MB | HTML5 package as .zip, mraid.js reference, orientation preference in manifest |
| ironSource | 5MB | MRAID 2.0, handle viewableChange events, separate endcard recommended |
| Google AdMob | 2MB recommended, 5MB max | MRAID support, must load within 5 seconds |
| AppLovin | 5MB | mraid.open() click-throughs, both orientations, see `references/applovin-compliance.md` |
| Meta Audience Network | 5MB | Single HTML file, FbPlayableAd hooks, works in Facebook in-app browser |

Reference `references/network-requirements.md` for complete specifications and testing URLs.

## Bundled Resources

### Scripts

- **generate_playable_template.py**: Create initial project structure with game type templates (`match3`, `runner`, `bubble`)
- **optimize_playable.py**: Minify, inline assets, compress for production
- **add_network_integration.py**: Add network-specific MRAID and tracking code
- **validate_playable.py**: Run automated checks for common issues

### References

- **game-mechanics-patterns.md**: Code patterns for common game types (match-3, runner, bubble shooter, etc.)
- **network-requirements.md**: Complete specifications for each ad network
- **applovin-compliance.md**: AppLovin/AXON compliance checklist and critical requirements

### Assets

Game templates are generated inline by `generate_playable_template.py` — they are not stored as files. The `assets/` directory is reserved for custom per-project art and UI elements (keep them inline-friendly: SVG or small base64 images).
