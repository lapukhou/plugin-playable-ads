#!/usr/bin/env python3
"""
Add network-specific integrations to playable ads.
Supports Unity Ads, ironSource, AdMob, AppLovin, and Meta.
"""

import argparse
import re
import sys
from pathlib import Path

MRAID_SNIPPET = '''
<!-- MRAID Bridge -->
<script src="mraid.js"></script>
<script>
if (typeof mraid !== 'undefined') {
    mraid.addEventListener('ready', function() {
        console.log('MRAID ready');
    });
} else {
    console.log('MRAID not available - testing mode');
}

function handleInstallClick() {
    if (typeof mraid !== 'undefined' && mraid.isViewable()) {
        mraid.open('STORE_URL');
    } else {
        window.open('STORE_URL', '_blank');
    }
}
</script>
'''

UNITY_ADS_INTEGRATION = '''
<!-- Unity Ads Integration -->
<script>
// Unity Ads click handler
function unityAdsClick() {
    if (typeof mraid !== 'undefined') {
        mraid.open('STORE_URL');
    } else {
        window.open('STORE_URL', '_blank');
    }
}

// Track viewability
if (typeof mraid !== 'undefined') {
    mraid.addEventListener('viewableChange', function(viewable) {
        if (viewable) {
            console.log('Ad is viewable');
            // Start game logic here
        }
    });
}
</script>
'''

IRONSOURCE_INTEGRATION = '''
<!-- ironSource Integration -->
<script>
// ironSource MRAID 2.0 support
if (typeof mraid !== 'undefined') {
    mraid.addEventListener('ready', function() {
        // Set expand properties if needed
        if (mraid.getState() === 'default') {
            mraid.addEventListener('stateChange', function(state) {
                if (state === 'expanded') {
                    console.log('Ad expanded');
                }
            });
        }
    });
    
    mraid.addEventListener('viewableChange', function(viewable) {
        if (viewable) {
            console.log('ironSource: Ad viewable');
        }
    });
}

function ironSourceClick() {
    if (typeof mraid !== 'undefined') {
        mraid.open('STORE_URL');
    } else {
        window.open('STORE_URL', '_blank');
    }
}
</script>
'''

ADMOB_INTEGRATION = '''
<!-- Google AdMob Integration -->
<script>
// AdMob MRAID support
if (typeof mraid !== 'undefined') {
    if (mraid.getState() === 'loading') {
        mraid.addEventListener('ready', function() {
            console.log('AdMob: MRAID ready');
        });
    }
    
    mraid.addEventListener('viewableChange', function(viewable) {
        if (viewable) {
            console.log('AdMob: Ad viewable');
        }
    });
}

function adMobClick() {
    if (typeof mraid !== 'undefined') {
        mraid.open('STORE_URL');
    } else {
        window.open('STORE_URL', '_blank');
    }
}
</script>
'''

APPLOVIN_INTEGRATION = '''
<!-- AppLovin/AXON Integration - CRITICAL REQUIREMENTS -->
<script>
// AppLovin MRAID v2.0 - MUST wait for ready event
var appLovinReady = false;
var storeUrl = 'STORE_URL';

function initAppLovin() {
    if (typeof mraid !== 'undefined') {
        // Check if MRAID is already ready
        if (mraid.getState() === 'loading') {
            mraid.addEventListener('ready', function() {
                console.log('AppLovin: MRAID ready');
                appLovinReady = true;
                // Safe to initialize game now
            });
        } else {
            console.log('AppLovin: MRAID already ready');
            appLovinReady = true;
        }
        
        // Handle viewability changes
        mraid.addEventListener('viewableChange', function(viewable) {
            if (viewable) {
                console.log('AppLovin: Ad viewable');
            } else {
                console.log('AppLovin: Ad hidden - pause/mute');
                // REQUIRED: Pause game and mute audio when hidden
                handleAdHidden();
            }
        });
    } else {
        console.log('MRAID not available - testing mode');
        appLovinReady = true;
    }
}

// CRITICAL: Use mraid.open() for click-through
// Using window.open() will cause click tracking failures!
function appLovinClick() {
    if (typeof mraid !== 'undefined' && appLovinReady) {
        // MUST use mraid.open() - NOT window.open()
        mraid.open(storeUrl);
    } else {
        // Fallback for testing only
        window.open(storeUrl, '_blank');
    }
}

// Handle audio requirements
var audioStarted = false;
var audioMuted = true;

function handleFirstInteraction() {
    if (!audioStarted) {
        // Audio can start after first interaction
        audioStarted = true;
        // Unmute audio if available
        if (typeof gameAudio !== 'undefined') {
            gameAudio.muted = false;
            audioMuted = false;
        }
    }
}

function handleAdHidden() {
    // REQUIRED: Mute audio when ad becomes hidden
    if (typeof gameAudio !== 'undefined' && !audioMuted) {
        gameAudio.muted = true;
        audioMuted = true;
    }
    // Pause game logic
    if (typeof pauseGame === 'function') {
        pauseGame();
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAppLovin);
} else {
    initAppLovin();
}

// Orientation support - AppLovin requires both portrait AND landscape
window.addEventListener('orientationchange', function() {
    console.log('Orientation changed');
    // Adjust layout if needed
    if (typeof handleOrientationChange === 'function') {
        handleOrientationChange();
    }
});

// Timer must start only after first user interaction (AppLovin requirement)
var timerStarted = false;
var gameTimer = 0;

function startGameTimer() {
    if (!timerStarted) {
        timerStarted = true;
        console.log('Game timer started');
        setInterval(function() {
            gameTimer++;
            if (typeof updateTimer === 'function') {
                updateTimer(gameTimer);
            }
        }, 1000);
    }
}

// Wire the gating handlers: the first touch or click anywhere in the ad
// unmutes audio and starts the game timer (AppLovin requirement)
function onFirstInteraction() {
    handleFirstInteraction();
    startGameTimer();
}
document.addEventListener('touchstart', onFirstInteraction, {once: true, passive: true});
document.addEventListener('mousedown', onFirstInteraction, {once: true});
</script>
'''

META_INTEGRATION = '''
<!-- Meta Audience Network Integration -->
<script>
// Meta-specific click handling
function metaClick() {
    // Facebook in-app browser compatibility
    const storeUrl = 'STORE_URL';
    
    if (typeof mraid !== 'undefined') {
        mraid.open(storeUrl);
    } else if (typeof FbPlayableAd !== 'undefined') {
        FbPlayableAd.onCTAClick();
    } else {
        window.open(storeUrl, '_blank');
    }
}

// Signal playable is ready
if (typeof FbPlayableAd !== 'undefined') {
    FbPlayableAd.onReady();
}
</script>
'''

NETWORKS = {
    'unity': UNITY_ADS_INTEGRATION,
    'ironsource': IRONSOURCE_INTEGRATION,
    'admob': ADMOB_INTEGRATION,
    'applovin': APPLOVIN_INTEGRATION,
    'meta': META_INTEGRATION
}

def add_network_integration(input_file, network, store_url, output_file=None):
    """Add network-specific integration code to a playable ad."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: File not found: {input_file}")
        return False
    
    if network not in NETWORKS:
        print(f"Error: Unknown network '{network}'")
        print(f"Available networks: {', '.join(NETWORKS.keys())}")
        return False
    
    print(f"Adding {network} integration to {input_file}")
    
    # Read input
    html = input_path.read_text(encoding='utf-8')
    
    # Add MRAID snippet if not present. Skip for Meta: the Facebook in-app
    # environment does not serve mraid.js, so referencing it would 404.
    if 'mraid.js' not in html and network != 'meta':
        integration_code = MRAID_SNIPPET + NETWORKS[network]
    else:
        integration_code = NETWORKS[network]
    
    # Replace store URL placeholder
    integration_code = integration_code.replace('STORE_URL', store_url)
    
    # Insert before closing head tag
    if '</head>' in html:
        html = html.replace('</head>', integration_code + '\n</head>')
    else:
        # If no head tag, insert at start of body
        html = html.replace('<body>', '<body>\n' + integration_code)
    
    # Update onclick handlers to use network-specific function
    function_name = {
        'unity': 'unityAdsClick',
        'ironsource': 'ironSourceClick',
        'admob': 'adMobClick',
        'applovin': 'appLovinClick',
        'meta': 'metaClick'
    }[network]
    
    # Rename the template's placeholder handler DEFINITION first, so its
    # hoisted declaration cannot override the injected network handler,
    # then point the remaining call sites at the network-specific function.
    html = re.sub(r'function\s+handleInstall\s*\(', 'function handleInstall_replaced(', html)
    html = html.replace('handleInstall()', f'{function_name}()')

    # Fill in any store URL placeholders left over from the base template
    html = html.replace('YOUR_STORE_URL', store_url)
    
    # Write output
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_{network}.html"
    else:
        output_file = Path(output_file)
    
    output_file.write_text(html, encoding='utf-8')
    print(f"✓ Added {network} integration")
    print(f"✓ Saved to: {output_file}")
    print("\nManual follow-ups:")
    print(f"  - Verify the CTA button's onclick now calls {function_name}()")
    print("  - Test the click-through in the network's preview tool before submission")
    if network == 'applovin':
        print("  - Confirm gameplay/timers only progress after the first user interaction")

    return True

def main():
    parser = argparse.ArgumentParser(description='Add network integrations to playable ads')
    parser.add_argument('input', help='Input HTML file')
    parser.add_argument('network', choices=list(NETWORKS.keys()),
                       help='Target ad network')
    parser.add_argument('--store-url', required=True,
                       help='App store URL for install button')
    parser.add_argument('--output', '-o',
                       help='Output file (default: input_network.html)')
    
    args = parser.parse_args()
    
    if not add_network_integration(args.input, args.network, args.store_url, args.output):
        sys.exit(1)

if __name__ == '__main__':
    main()
