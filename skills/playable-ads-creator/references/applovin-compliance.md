# AppLovin / AXON Compliance Checklist

Complete validation checklist based on official AppLovin/AXON specifications.

## Pre-Upload Checklist

### File Structure ✓
- [ ] Single HTML file only
- [ ] All resources embedded (base64 or base122)
- [ ] File size ≤ 5MB (STRICT limit)
- [ ] No external resources or network calls
- [ ] Valid HTML5 structure

### MRAID Implementation ✓
- [ ] MRAID v2.0 support included
- [ ] Wait for `mraid.ready` event before initialization
- [ ] Check `mraid.getState() !== 'loading'` before API calls
- [ ] Use `mraid.open(url)` for ALL click-throughs (NOT window.open)
- [ ] Handle MRAID not available (fallback for testing)

### Orientation Support ✓
- [ ] Works in landscape mode
- [ ] Works in portrait mode
- [ ] Smooth transition between orientations
- [ ] UI elements remain visible in both modes
- [ ] No layout breaks when rotating

### User Interaction ✓
- [ ] No redirect on first tap/click
- [ ] Ad timer starts ONLY after first interaction
- [ ] Playable and interactive (not just a video)
- [ ] CTA button clearly visible
- [ ] No auto-click to app store
- [ ] No auto-redirect without user action

### Audio Compliance ✓
- [ ] Audio muted by default
- [ ] Audio starts only after first user interaction
- [ ] Audio stops when ad closes
- [ ] Audio mutes when ad becomes hidden
- [ ] No background audio after ad exit

### Performance ✓
- [ ] Loads and becomes interactive in reasonable time (<5 seconds)
- [ ] 60 FPS target maintained
- [ ] No memory leaks in game loop
- [ ] Smooth animations
- [ ] Responsive to user input

### WebGL (if applicable) ✓
- [ ] UI fallback if WebGL initialization fails
- [ ] UI fallback if context is lost
- [ ] Graceful degradation to 2D canvas

### Testing ✓
- [ ] Tested on [AppLovin Playable Preview](https://p.applov.in/playablePreview?create=1)
- [ ] Verified click tracking works with mraid.open()
- [ ] Tested in landscape orientation
- [ ] Tested in portrait orientation
- [ ] Verified no console errors
- [ ] Verified no external network requests
- [ ] Audio behavior validated
- [ ] Timer starts only after interaction

## Common Violations & Fixes

### CRITICAL: Click-Through Failures
**Problem**: Using `window.open()` instead of `mraid.open()`
```javascript
// ❌ WRONG - Will fail on AppLovin
function handleClick() {
    window.open(storeUrl, '_blank');
}

// ✅ CORRECT - Use mraid.open()
function handleClick() {
    if (typeof mraid !== 'undefined') {
        mraid.open(storeUrl); // MUST use this
    } else {
        window.open(storeUrl, '_blank'); // Fallback for testing only
    }
}
```

### External Resources
**Problem**: Loading external images, scripts, or stylesheets
```html
<!-- ❌ WRONG - External resources -->
<script src="https://cdn.example.com/lib.js"></script>
<img src="https://example.com/image.png">

<!-- ✅ CORRECT - Inline everything -->
<script>/* Inline JavaScript */</script>
<img src="data:image/png;base64,iVBORw0KG...">
```

### Auto-Play Audio
**Problem**: Audio plays automatically
```javascript
// ❌ WRONG - Auto-play
audio.play();

// ✅ CORRECT - Wait for user interaction
canvas.addEventListener('click', function() {
    if (!audioStarted) {
        audio.play();
        audioStarted = true;
    }
}, {once: true});
```

### MRAID Not Ready
**Problem**: Using MRAID before it's ready
```javascript
// ❌ WRONG - May fail if MRAID not ready
if (typeof mraid !== 'undefined') {
    mraid.open(url); // Might not be ready yet
}

// ✅ CORRECT - Wait for ready event
if (typeof mraid !== 'undefined') {
    if (mraid.getState() === 'loading') {
        mraid.addEventListener('ready', onMraidReady);
    } else {
        onMraidReady();
    }
}
```

### Timer Starting Too Early
**Problem**: Timer starts immediately on load
```javascript
// ❌ WRONG - Timer starts on load
let gameTime = 0;
setInterval(() => gameTime++, 1000);

// ✅ CORRECT - Timer starts after first interaction
let gameTime = 0;
let timerStarted = false;

canvas.addEventListener('click', function startTimer() {
    if (!timerStarted) {
        timerStarted = true;
        setInterval(() => gameTime++, 1000);
    }
});
```

### Portrait-Only Design
**Problem**: Ad only works in one orientation
```css
/* ❌ WRONG - Fixed to portrait */
body {
    width: 375px;
    height: 667px;
}

/* ✅ CORRECT - Responsive to orientation */
body {
    width: 100vw;
    height: 100vh;
}

canvas {
    max-width: 100%;
    max-height: 100%;
}
```

## Validation Script Usage

Run the validation script with AppLovin-specific checks:

```bash
python scripts/validate_playable.py your_playable.html
```

Additional manual checks:
1. Upload to [AppLovin Playable Preview](https://p.applov.in/playablePreview?create=1)
2. Test click-through in preview
3. Rotate device to test both orientations
4. Verify audio muting behavior
5. Check timer starts only after interaction

## Policy Compliance

### Account Protection
- Follow [AppLovin Policies for Demand Partners](https://legal.applovin.com/policies-demand-partners/)
- Single violation → Asset blocked
- Repeated violations → Account ban

### Content Guidelines
- No misleading gameplay
- Accurate representation of app
- Age-appropriate content
- No prohibited content (gambling, adult, etc.)
- Respect intellectual property

## File Size Optimization for 5MB Limit

### If exceeding 5MB:
1. **Compress images more aggressively**
   - Use WebP format instead of PNG
   - Reduce image dimensions
   - Lower JPEG quality (70-80%)

2. **Minify code**
   - Remove all comments
   - Remove console.logs
   - Minify variable names
   - Remove whitespace

3. **Simplify graphics**
   - Use CSS gradients instead of images
   - Use inline SVG for icons
   - Reduce number of animation frames

4. **Remove audio** (if necessary)
   - Audio files are large
   - Consider silent version
   - Or use very short, compressed audio clips

5. **Use simpler game mechanics**
   - Reduce particle effects
   - Simplify physics calculations
   - Fewer game assets

## Testing Workflow

1. **Local testing**
   - Test in Chrome DevTools mobile view
   - Check console for errors
   - Verify file size < 5MB

2. **Validation script**
   ```bash
   python scripts/validate_playable.py ad.html
   ```

3. **AppLovin preview tool**
   - Upload to https://p.applov.in/playablePreview?create=1
   - Test in both orientations
   - Click CTA button multiple times
   - Verify click tracking works

4. **Real device testing**
   - Test on iOS device
   - Test on Android device
   - Rotate device during gameplay
   - Verify audio behavior

## Success Criteria

Your playable is ready when:
- ✅ File size ≤ 5MB
- ✅ Works in AppLovin preview tool
- ✅ Click-through works (using mraid.open)
- ✅ Functions in both orientations
- ✅ No console errors
- ✅ Audio properly muted/controlled
- ✅ Timer starts after interaction
- ✅ No external requests
- ✅ Passes all checklist items

## Resources

- **Official Preview Tool**: https://p.applov.in/playablePreview?create=1
- **Demand Partner Policies**: https://legal.applovin.com/policies-demand-partners/
- **AXON Support**: https://support.axon.ai/en/growth/promoting-your-apps/creatives/best-practices-and-guidelines
