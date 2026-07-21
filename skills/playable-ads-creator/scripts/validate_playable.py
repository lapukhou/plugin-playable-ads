#!/usr/bin/env python3
"""
Validate playable ads for production readiness.
Checks for common issues and best practices.
"""

import argparse
import re
import sys
from pathlib import Path

def validate_playable(file_path, max_size_mb=5):
    """Run validation checks on a playable ad."""
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    print(f"Validating: {file_path}\n")
    
    html = file_path.read_text(encoding='utf-8')
    issues = []
    warnings = []
    passes = []
    
    # Check file size
    file_size = len(html.encode('utf-8'))
    size_mb = file_size / (1024 * 1024)
    if size_mb > max_size_mb:
        issues.append(f"File size ({size_mb:.2f}MB) exceeds {max_size_mb}MB limit")
    else:
        passes.append(f"File size OK: {size_mb:.2f}MB / {max_size_mb}MB")
    
    # Check for external dependencies
    external_resources = []
    
    # Check for external scripts
    ext_scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html)
    for script in ext_scripts:
        if not script.startswith('data:') and script != 'mraid.js':
            external_resources.append(f"External script: {script}")
    
    # Check for external stylesheets
    ext_css = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', html)
    for css in ext_css:
        if not css.startswith('data:'):
            external_resources.append(f"External stylesheet: {css}")
    
    # Check for external images
    ext_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    for img in ext_imgs:
        if not img.startswith('data:'):
            external_resources.append(f"External image: {img}")
    
    if external_resources:
        issues.extend(external_resources)
        issues.append("Playable ads must work offline - all assets should be inlined")
    else:
        passes.append("No external dependencies (works offline)")
    
    # Check viewport meta tag
    if 'viewport' not in html:
        warnings.append("Missing viewport meta tag")
    else:
        passes.append("Viewport meta tag present")
    
    # Check for touch event handling
    if 'touchstart' in html or 'touchend' in html or 'touchmove' in html:
        passes.append("Touch events handled")
    else:
        warnings.append("No touch event handlers detected - may not work on mobile")
    
    # Check for CTA button: an actual clickable element, not just the word
    # "play" (which matches every "Playable Ad" title)
    cta_found = re.search(
        r'<(?:button|a|div)\b[^>]*(?:onclick=|id=["\'][^"\']*(?:cta|install|download))',
        html, re.IGNORECASE)
    if cta_found:
        passes.append("CTA button present")
    else:
        warnings.append("No clear CTA button detected (expected a button/link with onclick or a cta/install/download id)")

    # Check for unreplaced store URL placeholder
    if 'YOUR_STORE_URL' in html:
        issues.append("Store URL placeholder 'YOUR_STORE_URL' has not been replaced - CTA will not open the store")
    
    # Check for console.log (debug code)
    console_logs = re.findall(r'console\.(log|debug|info|warn|error)', html)
    if console_logs:
        warnings.append(f"Found {len(console_logs)} console statements - should be removed for production")
    else:
        passes.append("No debug console statements")
    
    # Check for canvas element
    if '<canvas' in html:
        passes.append("Canvas element found")
    else:
        warnings.append("No canvas element - consider using canvas for better performance")
    
    # Check for requestAnimationFrame
    if 'requestAnimationFrame' in html:
        passes.append("Uses requestAnimationFrame for smooth animation")
    elif 'setInterval' in html or 'setTimeout' in html:
        warnings.append("Using setInterval/setTimeout instead of requestAnimationFrame")
    
    # Check for user-scalable=no
    if 'user-scalable=no' in html:
        passes.append("Prevents pinch-zoom (good for games)")
    else:
        warnings.append("Consider adding user-scalable=no to viewport for game-like experience")
    
    # Check minification
    if re.search(r'\s{4,}', html):
        warnings.append("HTML appears unminified - consider running optimization")
    else:
        passes.append("Code appears minified")
    
    # AppLovin/AXON specific checks
    # Check for MRAID implementation
    if 'mraid' in html:
        passes.append("MRAID support included")
        
        # Check for proper MRAID ready handling
        if 'mraid.getState()' in html or "mraid.addEventListener('ready'" in html:
            passes.append("MRAID ready event handling present")
        else:
            warnings.append("MRAID included but no ready event handling detected")
        
        # CRITICAL: Check for mraid.open usage
        if 'mraid.open' in html:
            passes.append("CRITICAL: Uses mraid.open() for click-through (AppLovin compliant)")
        else:
            issues.append("CRITICAL: Missing mraid.open() - AppLovin click tracking will fail!")
    else:
        warnings.append("No MRAID support - required for ironSource, AdMob, AppLovin")
    
    # Check orientation support
    orientation_keywords = ['orientationchange', 'landscape', 'portrait', '@media']
    if any(keyword in html for keyword in orientation_keywords):
        passes.append("Orientation handling detected")
    else:
        warnings.append("No orientation handling - AppLovin requires both landscape and portrait support")
    
    # Check audio muting (AppLovin requirement)
    if 'audio' in html.lower() or 'Audio(' in html:
        if 'muted' in html or '.mute' in html.lower():
            passes.append("Audio muting controls present (AppLovin compliant)")
        else:
            issues.append("Audio present but no muting - AppLovin requires audio muted until first interaction")
    
    # Print results
    print("=" * 60)
    print("VALIDATION RESULTS")
    print("=" * 60)
    
    if passes:
        print(f"\n✓ PASSED ({len(passes)}):")
        for p in passes:
            print(f"  ✓ {p}")
    
    if warnings:
        print(f"\n⚠ WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")
    
    if issues:
        print(f"\n✗ ISSUES ({len(issues)}):")
        for i in issues:
            print(f"  ✗ {i}")
    
    print("\n" + "=" * 60)
    
    if issues:
        print("RESULT: FAILED - Fix issues before deploying")
        return False
    elif warnings:
        print("RESULT: PASSED WITH WARNINGS - Review warnings")
        return True
    else:
        print("RESULT: PASSED - Ready for production")
        return True

def main():
    parser = argparse.ArgumentParser(description='Validate playable ads')
    parser.add_argument('file', help='HTML file to validate')
    parser.add_argument('--max-size', type=float, default=5.0,
                       help='Maximum file size in MB (default: 5.0)')
    
    args = parser.parse_args()
    
    success = validate_playable(args.file, args.max_size)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
