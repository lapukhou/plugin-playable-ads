#!/usr/bin/env python3
"""
Generate HTML5 playable ad templates for different game types.
"""

import argparse
import sys
from pathlib import Path

TEMPLATES = {
    "match3": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Match-3 Playable Ad</title>
    <!--
    AppLovin/AXON Compliance Notes:
    - handleInstall() prefers mraid.open() with a window.open fallback for local testing
    - Replace YOUR_STORE_URL, or run scripts/add_network_integration.py --store-url
    - Ensure timer starts only after first user interaction
    - Add orientation change handling for landscape/portrait
    - Keep audio muted until first interaction
    - Use mraid.open() for CTA click (NOT window.open)
    - All resources must be inline (no external requests)
    - File size must be ≤ 5MB
    -->
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            overflow: hidden; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            touch-action: none;
        }
        #game-container { 
            width: 100vw; 
            height: 100vh; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        #game-canvas { 
            max-width: 100%; 
            max-height: 80vh;
            image-rendering: crisp-edges;
        }
        #cta-button {
            display: none;
            margin-top: 20px;
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        #score {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="score">Score: 0</div>
        <canvas id="game-canvas"></canvas>
        <button id="cta-button" onclick="handleInstall()">Install Now!</button>
    </div>
    <script>
        // Game Configuration
        const GRID_SIZE = 6;
        const GEM_TYPES = 5;
        const CELL_SIZE = 60;
        
        // Game State
        let canvas, ctx;
        let grid = [];
        let score = 0;
        let selectedGem = null;
        let isAnimating = false;
        
        // Initialize
        window.addEventListener('load', init);
        
        function init() {
            canvas = document.getElementById('game-canvas');
            ctx = canvas.getContext('2d');
            
            // Set canvas size
            const size = GRID_SIZE * CELL_SIZE;
            canvas.width = size;
            canvas.height = size;
            
            // Initialize grid
            initGrid();
            
            // Event listeners
            canvas.addEventListener('click', handleClick);
            canvas.addEventListener('touchstart', handleTouch, {passive: false});
            
            // Start game loop
            gameLoop();
        }
        
        function initGrid() {
            for (let y = 0; y < GRID_SIZE; y++) {
                grid[y] = [];
                for (let x = 0; x < GRID_SIZE; x++) {
                    grid[y][x] = Math.floor(Math.random() * GEM_TYPES);
                }
            }
        }
        
        function gameLoop() {
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Draw grid
            for (let y = 0; y < GRID_SIZE; y++) {
                for (let x = 0; x < GRID_SIZE; x++) {
                    drawGem(x, y, grid[y][x]);
                }
            }
            
            // Draw selection
            if (selectedGem) {
                ctx.strokeStyle = 'yellow';
                ctx.lineWidth = 3;
                ctx.strokeRect(
                    selectedGem.x * CELL_SIZE,
                    selectedGem.y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                );
            }
        }
        
        function drawGem(x, y, type) {
            const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
            ctx.fillStyle = colors[type];
            ctx.fillRect(
                x * CELL_SIZE + 2,
                y * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            );
        }
        
        function handleClick(e) {
            if (isAnimating) return;
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor((e.clientX - rect.left) / CELL_SIZE);
            const y = Math.floor((e.clientY - rect.top) / CELL_SIZE);
            handleGemSelection(x, y);
        }
        
        function handleTouch(e) {
            e.preventDefault();
            if (isAnimating) return;
            const touch = e.touches[0];
            const rect = canvas.getBoundingClientRect();
            const x = Math.floor((touch.clientX - rect.left) / CELL_SIZE);
            const y = Math.floor((touch.clientY - rect.top) / CELL_SIZE);
            handleGemSelection(x, y);
        }
        
        function handleGemSelection(x, y) {
            if (x < 0 || x >= GRID_SIZE || y < 0 || y >= GRID_SIZE) return;
            
            if (!selectedGem) {
                selectedGem = {x, y};
            } else {
                // Check if adjacent
                const dx = Math.abs(selectedGem.x - x);
                const dy = Math.abs(selectedGem.y - y);
                
                if ((dx === 1 && dy === 0) || (dx === 0 && dy === 1)) {
                    swapGems(selectedGem.x, selectedGem.y, x, y);
                }
                selectedGem = null;
            }
        }
        
        function swapGems(x1, y1, x2, y2) {
            const temp = grid[y1][x1];
            grid[y1][x1] = grid[y2][x2];
            grid[y2][x2] = temp;
            
            setTimeout(() => {
                checkMatches();
            }, 100);
        }
        
        function checkMatches() {
            let matches = [];
            
            // Check horizontal matches
            for (let y = 0; y < GRID_SIZE; y++) {
                for (let x = 0; x < GRID_SIZE - 2; x++) {
                    if (grid[y][x] === grid[y][x+1] && grid[y][x] === grid[y][x+2]) {
                        matches.push({x, y}, {x: x+1, y}, {x: x+2, y});
                    }
                }
            }
            
            // Check vertical matches
            for (let x = 0; x < GRID_SIZE; x++) {
                for (let y = 0; y < GRID_SIZE - 2; y++) {
                    if (grid[y][x] === grid[y+1][x] && grid[y][x] === grid[y+2][x]) {
                        matches.push({x, y}, {x, y: y+1}, {x, y: y+2});
                    }
                }
            }
            
            if (matches.length > 0) {
                updateScore(matches.length * 10);
                clearMatches(matches);
            }
        }
        
        function clearMatches(matches) {
            matches.forEach(({x, y}) => {
                grid[y][x] = Math.floor(Math.random() * GEM_TYPES);
            });
            
            setTimeout(() => checkMatches(), 300);
        }
        
        function updateScore(points) {
            score += points;
            document.getElementById('score').textContent = 'Score: ' + score;
            
            // Show CTA after certain score
            if (score >= 50) {
                document.getElementById('cta-button').style.display = 'block';
            }
        }
        
        function handleInstall() {
            var url = 'YOUR_STORE_URL';
            if (typeof mraid !== 'undefined') {
                mraid.open(url);
            } else {
                window.open(url, '_blank');
            }
        }
    </script>
</body>
</html>""",

    "runner": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Runner Playable Ad</title>
    <!--
    AppLovin/AXON Compliance Notes:
    - handleInstall() prefers mraid.open() with a window.open fallback for local testing
    - Gameplay starts only after the first user interaction (tap to start)
    - Keep audio muted until first interaction
    - All resources must be inline (no external requests); file size ≤ 5MB
    -->
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            overflow: hidden; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(180deg, #87CEEB 0%, #98D8C8 100%);
            touch-action: none;
        }
        #game-container { 
            width: 100vw; 
            height: 100vh; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        #game-canvas { 
            max-width: 100%; 
            max-height: 80vh;
            border: 2px solid #333;
        }
        #cta-button {
            display: none;
            margin-top: 20px;
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: linear-gradient(45deg, #FF6B6B 0%, #4ECDC4 100%);
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        #distance {
            position: absolute;
            top: 20px;
            left: 20px;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="distance">Distance: 0m</div>
        <canvas id="game-canvas"></canvas>
        <button id="cta-button" onclick="handleInstall()">Play Full Game!</button>
    </div>
    <script>
        // Game setup
        let canvas, ctx;
        let player = {x: 100, y: 280, width: 40, height: 40, velocityY: 0, isJumping: false};
        let obstacles = [];
        let distance = 0;
        let gameSpeed = 5;
        let gravity = 0.8;
        let jumpPower = -15;
        let gameOver = false;
        let started = false;
        
        window.addEventListener('load', init);
        
        function init() {
            canvas = document.getElementById('game-canvas');
            ctx = canvas.getContext('2d');
            canvas.width = 800;
            canvas.height = 400;
            
            // Input handlers
            canvas.addEventListener('click', jump);
            canvas.addEventListener('touchstart', (e) => {
                e.preventDefault();
                jump();
            }, {passive: false});
            
            // Start game
            spawnObstacle();
            gameLoop();
        }
        
        function gameLoop() {
            if (!gameOver) {
                update();
                draw();
                requestAnimationFrame(gameLoop);
            } else {
                showCTA();
            }
        }
        
        function update() {
            // AppLovin: gameplay may only progress after a user interaction
            if (!started) return;

            // Update player
            player.velocityY += gravity;
            player.y += player.velocityY;
            
            // Ground collision
            if (player.y > 280) {
                player.y = 280;
                player.velocityY = 0;
                player.isJumping = false;
            }
            
            // Update obstacles
            obstacles.forEach(obs => obs.x -= gameSpeed);
            
            // Remove off-screen obstacles
            obstacles = obstacles.filter(obs => obs.x > -obs.width);
            
            // Spawn new obstacles
            if (obstacles.length === 0 || obstacles[obstacles.length - 1].x < 400) {
                spawnObstacle();
            }
            
            // Check collisions
            obstacles.forEach(obs => {
                if (checkCollision(player, obs)) {
                    gameOver = true;
                }
            });
            
            // Update distance
            distance += gameSpeed * 0.1;
            document.getElementById('distance').textContent = 'Distance: ' + Math.floor(distance) + 'm';
            
            // Gradually increase speed
            gameSpeed += 0.001;
        }
        
        function draw() {
            // Clear canvas
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw ground
            ctx.fillStyle = '#8B7355';
            ctx.fillRect(0, 320, canvas.width, 80);
            
            // Draw player
            ctx.fillStyle = '#FF6B6B';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            
            // Draw obstacles
            ctx.fillStyle = '#333';
            obstacles.forEach(obs => {
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
            });

            if (!started) {
                ctx.fillStyle = 'white';
                ctx.font = 'bold 32px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Tap to Start!', canvas.width / 2, 150);
                ctx.textAlign = 'left';
            }
        }
        
        function jump() {
            if (!started) {
                started = true;
                return;
            }
            if (!player.isJumping && !gameOver) {
                player.velocityY = jumpPower;
                player.isJumping = true;
            }
        }
        
        function spawnObstacle() {
            obstacles.push({
                x: canvas.width,
                y: 280,
                width: 30,
                height: 40
            });
        }
        
        function checkCollision(rect1, rect2) {
            return rect1.x < rect2.x + rect2.width &&
                   rect1.x + rect1.width > rect2.x &&
                   rect1.y < rect2.y + rect2.height &&
                   rect1.y + rect1.height > rect2.y;
        }
        
        function showCTA() {
            document.getElementById('cta-button').style.display = 'block';
        }
        
        function handleInstall() {
            var url = 'YOUR_STORE_URL';
            if (typeof mraid !== 'undefined') {
                mraid.open(url);
            } else {
                window.open(url, '_blank');
            }
        }
    </script>
</body>
</html>""",

    "bubble": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Bubble Shooter Playable Ad</title>
    <!--
    AppLovin/AXON Compliance Notes:
    - handleInstall() prefers mraid.open() with a window.open fallback for local testing
    - Gameplay is user-driven; nothing progresses before the first interaction
    - Keep audio muted until first interaction
    - All resources must be inline (no external requests); file size ≤ 5MB
    -->
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            overflow: hidden; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            touch-action: none;
        }
        #game-container { 
            width: 100vw; 
            height: 100vh; 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        #game-canvas { 
            max-width: 100%; 
            max-height: 80vh;
            cursor: crosshair;
        }
        #cta-button {
            display: none;
            margin-top: 20px;
            padding: 15px 40px;
            font-size: 20px;
            font-weight: bold;
            color: white;
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            border: none;
            border-radius: 50px;
            cursor: pointer;
        }
        #score {
            position: absolute;
            top: 20px;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="game-container">
        <div id="score">Score: 0</div>
        <canvas id="game-canvas"></canvas>
        <button id="cta-button" onclick="handleInstall()">Download Now!</button>
    </div>
    <script>
        // Game config
        const BUBBLE_RADIUS = 20;
        const COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
        
        let canvas, ctx;
        let bubbles = [];
        let shooter = {x: 0, y: 0, angle: 0};
        let currentBubble = null;
        let score = 0;
        
        window.addEventListener('load', init);
        
        function init() {
            canvas = document.getElementById('game-canvas');
            ctx = canvas.getContext('2d');
            canvas.width = 400;
            canvas.height = 600;
            
            shooter.x = canvas.width / 2;
            shooter.y = canvas.height - 50;
            
            initBubbles();
            spawnBubble();
            
            canvas.addEventListener('click', shoot);
            canvas.addEventListener('touchstart', (e) => {
                e.preventDefault();
                const touch = e.touches[0];
                const rect = canvas.getBoundingClientRect();
                const x = touch.clientX - rect.left;
                const y = touch.clientY - rect.top;
                aimAt(x, y);
                shoot();
            }, {passive: false});
            
            canvas.addEventListener('mousemove', (e) => {
                const rect = canvas.getBoundingClientRect();
                aimAt(e.clientX - rect.left, e.clientY - rect.top);
            });
            
            gameLoop();
        }
        
        function initBubbles() {
            for (let row = 0; row < 5; row++) {
                for (let col = 0; col < 8; col++) {
                    bubbles.push({
                        x: col * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS + (row % 2) * BUBBLE_RADIUS,
                        y: row * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS,
                        color: COLORS[Math.floor(Math.random() * COLORS.length)],
                        active: true
                    });
                }
            }
        }
        
        function spawnBubble() {
            currentBubble = {
                x: shooter.x,
                y: shooter.y,
                color: COLORS[Math.floor(Math.random() * COLORS.length)],
                vx: 0,
                vy: 0,
                active: false
            };
        }
        
        function aimAt(x, y) {
            const dx = x - shooter.x;
            const dy = y - shooter.y;
            shooter.angle = Math.atan2(dy, dx);
        }
        
        function shoot() {
            if (currentBubble && !currentBubble.active) {
                currentBubble.vx = Math.cos(shooter.angle) * 8;
                currentBubble.vy = Math.sin(shooter.angle) * 8;
                currentBubble.active = true;
            }
        }
        
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        function update() {
            if (currentBubble && currentBubble.active) {
                currentBubble.x += currentBubble.vx;
                currentBubble.y += currentBubble.vy;
                
                // Wall collision
                if (currentBubble.x < BUBBLE_RADIUS || currentBubble.x > canvas.width - BUBBLE_RADIUS) {
                    currentBubble.vx *= -1;
                }
                
                // Check bubble collision
                bubbles.forEach(bubble => {
                    if (!bubble.active) return;
                    const dx = bubble.x - currentBubble.x;
                    const dy = bubble.y - currentBubble.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    if (dist < BUBBLE_RADIUS * 2) {
                        currentBubble.active = false;
                        checkMatches(bubble.color);
                        spawnBubble();
                    }
                });
                
                // Top collision
                if (currentBubble.y < BUBBLE_RADIUS) {
                    currentBubble.active = false;
                    spawnBubble();
                }
            }
        }
        
        function checkMatches(color) {
            const matched = bubbles.filter(b => b.active && b.color === color);
            if (matched.length >= 3) {
                matched.forEach(b => b.active = false);
                score += matched.length * 10;
                document.getElementById('score').textContent = 'Score: ' + score;
                
                if (score >= 50) {
                    document.getElementById('cta-button').style.display = 'block';
                }
            }
        }
        
        function draw() {
            ctx.fillStyle = '#1a1a2e';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw bubbles
            bubbles.forEach(bubble => {
                if (bubble.active) {
                    ctx.fillStyle = bubble.color;
                    ctx.beginPath();
                    ctx.arc(bubble.x, bubble.y, BUBBLE_RADIUS, 0, Math.PI * 2);
                    ctx.fill();
                }
            });
            
            // Draw current bubble
            if (currentBubble) {
                ctx.fillStyle = currentBubble.color;
                ctx.beginPath();
                ctx.arc(currentBubble.x, currentBubble.y, BUBBLE_RADIUS, 0, Math.PI * 2);
                ctx.fill();
            }
            
            // Draw shooter
            ctx.strokeStyle = 'white';
            ctx.beginPath();
            ctx.moveTo(shooter.x, shooter.y);
            ctx.lineTo(
                shooter.x + Math.cos(shooter.angle) * 50,
                shooter.y + Math.sin(shooter.angle) * 50
            );
            ctx.stroke();
        }
        
        function handleInstall() {
            var url = 'YOUR_STORE_URL';
            if (typeof mraid !== 'undefined') {
                mraid.open(url);
            } else {
                window.open(url, '_blank');
            }
        }
    </script>
</body>
</html>"""
}

def generate_template(game_type, output_path):
    """Generate a playable ad template for the specified game type."""
    if game_type not in TEMPLATES:
        print(f"Error: Unknown game type '{game_type}'")
        print(f"Available types: {', '.join(TEMPLATES.keys())}")
        return False
    
    output_file = Path(output_path) / f"{game_type}_playable.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    output_file.write_text(TEMPLATES[game_type])
    print(f"✓ Created {game_type} template: {output_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate playable ad templates')
    parser.add_argument('game_type', choices=list(TEMPLATES.keys()), 
                       help='Type of game template to generate')
    parser.add_argument('--output', '-o', default='.',
                       help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    if not generate_template(args.game_type, args.output):
        sys.exit(1)

if __name__ == '__main__':
    main()
