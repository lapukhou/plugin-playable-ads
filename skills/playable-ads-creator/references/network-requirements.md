# Ad Network Requirements Reference

Complete specifications for major mobile ad networks supporting HTML5 playable ads.

## Unity Ads

### File Specifications
- **Max file size**: 5MB
- **Format**: .zip package containing index.html
- **Orientation**: Specified in manifest or responsive

### Technical Requirements
- Must include MRAID support
- Single HTML file or packaged structure
- All assets must be inline or packaged
- No external CDN dependencies

### Package Structure
```
playable_ad.zip
├── index.html (entry point)
├── mraid.js (optional, provided by SDK)
└── Any additional assets (inline recommended)
```

### MRAID Integration
- Include `<script src="mraid.js"></script>` in head
- Listen for `mraid.ready` event
- Use `mraid.open(url)` for CTA clicks
- Handle `viewableChange` for game start

### Testing
- Unity Ads provides testing tools in dashboard
- Test on iOS and Android devices
- Verify click tracking works
- Check orientation handling

### Best Practices
- Start game only when ad is viewable
- Clear win/install CTA after 10-15 seconds
- Optimize for 3-5 second load time
- Test on mid-range devices (iPhone 11, Samsung Galaxy S10)

---

## ironSource

### File Specifications
- **Max file size**: 5MB
- **Format**: Single HTML file or .zip
- **MRAID version**: 2.0+ required
- **Orientation**: Portrait or landscape, responsive recommended

### Technical Requirements
- MRAID 2.0 support mandatory
- Must handle all MRAID events properly
- Separate endcard HTML recommended
- No external requests allowed

### MRAID Implementation
```javascript
if (typeof mraid !== 'undefined') {
    mraid.addEventListener('ready', function() {
        // Initialize game
    });
    
    mraid.addEventListener('viewableChange', function(viewable) {
        if (viewable) {
            // Start gameplay
        } else {
            // Pause game
        }
    });
    
    // For CTA
    mraid.open(storeUrl);
}
```

### Key Features
- Supports expandable ads
- Requires state management (default, expanded, hidden)
- Must handle orientation changes
- Video end card support

### Testing
- ironSource provides Luna preview tool
- Test on actual devices mandatory
- Verify MRAID events fire correctly
- Check click-through rate tracking

### Best Practices
- Implement clear tutorial (hand pointer, arrows)
- Show CTA after satisfying win moment
- Use object pooling for particles
- Optimize for 60 FPS on older devices

---

## Google AdMob

### File Specifications
- **Recommended size**: 2MB
- **Max size**: 5MB (but 2MB preferred for performance)
- **Format**: Single HTML file
- **Load time**: Must load within 5 seconds

### Technical Requirements
- MRAID support required
- Follow AMPHTML guidelines
- Must work on Chrome mobile browser
- No external dependencies

### MRAID Usage
```javascript
if (mraid.getState() === 'loading') {
    mraid.addEventListener('ready', onReady);
} else {
    onReady();
}

function onReady() {
    // Ad is ready, initialize game
}

mraid.addEventListener('viewableChange', function(viewable) {
    // Handle visibility changes
});
```

### Performance Requirements
- First meaningful paint < 2 seconds
- Time to interactive < 5 seconds
- 60 FPS target on mid-range devices
- Minimal JavaScript execution time

### Testing
- Test in AdMob test environment
- Use Chrome DevTools mobile emulation
- Test on slow 3G networks
- Verify metrics in AdMob dashboard

### Best Practices
- Prioritize quick load time (compress aggressively)
- Use CSS animations over JavaScript when possible
- Minimize reflows and repaints
- Lazy load non-critical assets

---

## AppLovin / AXON

### File Specifications
- **Max file size**: 5MB per HTML file (STRICT)
- **Format**: Single HTML file only
- **Orientation**: Must support BOTH landscape and portrait
- **File type**: HTML with all resources embedded (base64 or base122)

### CRITICAL Technical Requirements

#### Behavioral Requirements (MUST COMPLY)
1. **Single file architecture**: All resources embedded in base64/base122 - NO external resources
2. **Orientation handling**: Must work properly in both landscape AND portrait
3. **Timer initialization**: Ad timer starts ONLY after first user interaction
4. **Interactivity**: Must be playable - NO redirect to store on first tap/click
5. **Load time**: Must fully load and become interactive in reasonable time
6. **Audio control**:
   - Audio MUST be muted until first user interaction
   - Audio MUST stop/mute when ad closes or becomes hidden
7. **No auto-click**: NO auto-redirect to app stores without user interaction
8. **No external requests**: External network calls PROHIBITED

#### MRAID Requirements (CRITICAL)
- **MRAID v2.0 support REQUIRED**
- **MUST wait for ready event** before calling MRAID APIs:
```javascript
// CORRECT - Wait for MRAID ready
if (typeof mraid !== 'undefined') {
    if (mraid.getState() === 'loading') {
        mraid.addEventListener('ready', function() {
            // Safe to use MRAID now
            initializeAd();
        });
    } else {
        // Already ready
        initializeAd();
    }
}

// CRITICAL: Use mraid.open() for click-through
function handleCTAClick() {
    if (typeof mraid !== 'undefined') {
        mraid.open(storeUrl); // MUST use this, not window.open
    } else {
        // Fallback for testing
        window.open(storeUrl, '_blank');
    }
}
```

**WARNING**: Not using `mraid.open()` will cause click-through failures and campaign performance issues.

#### WebGL Support
- If using WebGL, MUST provide UI fallback if initialization fails or context is lost

### Testing & Preview
- **Official preview tool**: [AppLovin Playable Preview](https://p.applov.in/playablePreview?create=1)
- Test in both orientations
- Verify MRAID ready event handling
- Test click tracking with mraid.open()
- Verify no external requests
- Check audio muting behavior

### Video & Image Specifications

#### Video Specs
- **Supported formats**: MP4, MOV
- **MIME types**: `video/mp4`, `video/quicktime`, `video/x-m4v`
- **Aspect ratio**: 9:16 (Portrait)
- **Max file size**: 1 GB
- **Max duration**: 60 seconds
- Note: AppLovin reprocesses videos for mobile optimization

#### Image Specs
- **Supported formats**: GIF, JPEG, PNG
- **MIME types**: `image/gif`, `image/jpeg`, `image/png`
- **Max file size**: 10 MB
- **Max GIF duration**: 60 seconds

| Asset Type | Aspect Ratio | Min Width | Min Height | Additional Allowed |
|-----------|--------------|-----------|------------|--------------------|
| Banner | 32:5 | 320px | 50px | - |
| Endcard | 9:16 | 270px | 480px | 320×480, 320×512, 640×1138, 768×1024 |
| MREC | 6:5 | 300px | 250px | 320×250 |
| Icon | 1:1 | 50px | 50px | - |

### Compliance & Policy
- **Violations** lead to asset blocking
- **Serious/repeated violations** can result in account ban
- Review [AppLovin Policies for Demand Partners](https://legal.applovin.com/policies-demand-partners/)

### Best Practices
- Clear value proposition in first 3 seconds
- Timer starts only after user interaction
- Support rotation between portrait/landscape seamlessly
- Test extensively with official preview tool
- Ensure mraid.open() is used for ALL click-throughs
- Provide WebGL fallback UI
- Keep audio muted by default

---

## Meta Audience Network (Facebook)

### File Specifications
- **Max file size**: 5MB
- **Format**: Single HTML file preferred
- **Browser compatibility**: Must work in Facebook in-app browser

### Technical Requirements
- Facebook in-app browser compatibility critical
- Special handling for CTA clicks
- Must work without MRAID (but MRAID supported)
- No pop-ups allowed

### Facebook-Specific Integration
```javascript
// Check for Facebook Playable SDK
if (typeof FbPlayableAd !== 'undefined') {
    // Signal ad is ready
    FbPlayableAd.onReady();
    
    // Handle CTA click
    function handleCTAClick() {
        FbPlayableAd.onCTAClick();
    }
} else if (typeof mraid !== 'undefined') {
    // Fallback to MRAID
    mraid.open(storeUrl);
} else {
    // Standard fallback
    window.open(storeUrl, '_blank');
}
```

### Unique Considerations
- In-app browser has specific JavaScript limitations
- Must handle Facebook SDK initialization
- Different click handling than other networks
- Supports both MRAID and Facebook SDK

### Testing
- Test in Facebook app on iOS and Android
- Use Meta preview tool in Ads Manager
- Verify CTA click works in-app
- Check performance on older devices

### Best Practices
- Keep gameplay extremely simple (tap or swipe only)
- Show clear value proposition immediately
- Minimal text, maximum visual communication
- Test extensively in Facebook app environment

---

## Common Requirements Across All Networks

### Universal Best Practices
1. **Offline functionality**: Must work without internet
2. **No external requests**: All assets inline
3. **Touch optimization**: Support touch events, not just mouse
4. **Performance**: 60 FPS target, < 3 second load
5. **Clear CTA**: Install button visible and clickable
6. **Mobile-first**: Design for small screens first

### File Size Optimization
- Minify all HTML, CSS, JavaScript
- Use SVG for vector graphics when possible
- Compress images (consider WebP format)
- Inline small assets as base64
- Remove console logs and debug code

### Mobile Performance Checklist
- Use `requestAnimationFrame` for animations
- Minimize DOM manipulations
- Use CSS transforms for movement
- Implement object pooling for repeated elements
- Avoid memory leaks in game loop
- Test on devices with 2GB RAM or less

### Testing Checklist
- [ ] Works on iOS Safari
- [ ] Works on Android Chrome
- [ ] Touch events properly handled
- [ ] Portrait and landscape work (if applicable)
- [ ] Loads in under 5 seconds on 3G
- [ ] No console errors
- [ ] CTA button clickable and prominent
- [ ] File size under network limit
- [ ] Works completely offline
- [ ] Smooth 60 FPS gameplay

### Common Pitfalls to Avoid
- External CDN dependencies (jQuery, Google Fonts, etc.)
- Large image files not optimized
- Complex physics engines causing lag
- Unclear tutorial or first action
- CTA appearing too early (before engagement)
- Mouse-only events (not touch-compatible)
- Not testing on actual mobile devices
- Ignoring low-end device performance
