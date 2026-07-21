# Game Mechanics Patterns

Common implementation patterns for popular playable ad game types.

## Match-3 Games

### Core Mechanics
- Grid-based gem/tile matching
- Swap adjacent pieces
- Match 3+ in a row/column
- Cascade and refill

### Implementation Pattern
```javascript
// Grid structure
const GRID_SIZE = 6;
let grid = [];

// Initialize grid with random gems
function initGrid() {
    for (let y = 0; y < GRID_SIZE; y++) {
        grid[y] = [];
        for (let x = 0; x < GRID_SIZE; x++) {
            grid[y][x] = {
                type: Math.floor(Math.random() * 5),
                x: x,
                y: y
            };
        }
    }
}

// Handle gem selection and swapping
let selectedGem = null;

function handleClick(x, y) {
    if (!selectedGem) {
        selectedGem = {x, y};
    } else {
        // Check if adjacent
        if (isAdjacent(selectedGem, {x, y})) {
            swapGems(selectedGem, {x, y});
            checkMatches();
        }
        selectedGem = null;
    }
}

// Check for matches
function checkMatches() {
    const matches = [];
    
    // Horizontal matches
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE - 2; x++) {
            if (grid[y][x].type === grid[y][x+1].type && 
                grid[y][x].type === grid[y][x+2].type) {
                matches.push([{x, y}, {x: x+1, y}, {x: x+2, y}]);
            }
        }
    }
    
    // Vertical matches
    for (let x = 0; x < GRID_SIZE; x++) {
        for (let y = 0; y < GRID_SIZE - 2; y++) {
            if (grid[y][x].type === grid[y+1][x].type && 
                grid[y][x].type === grid[y+2][x].type) {
                matches.push([{x, y}, {x, y: y+1}, {x, y: y+2}]);
            }
        }
    }
    
    return matches;
}
```

### Best Practices
- Visual feedback on selection (highlight, glow)
- Satisfying match animation (particles, scale)
- Clear swap animation (smooth transition)
- Cascading matches for engagement
- Score multipliers for consecutive matches

---

## Runner/Endless Runner

### Core Mechanics
- Character runs automatically
- Tap/click to jump
- Avoid obstacles
- Collect coins/items

### Implementation Pattern
```javascript
// Player state
const player = {
    x: 100,
    y: 300,
    width: 40,
    height: 40,
    velocityY: 0,
    isJumping: false
};

const GRAVITY = 0.8;
const JUMP_POWER = -15;
const GROUND_Y = 300;

// Game update loop
function update() {
    // Apply gravity
    player.velocityY += GRAVITY;
    player.y += player.velocityY;
    
    // Ground collision
    if (player.y >= GROUND_Y) {
        player.y = GROUND_Y;
        player.velocityY = 0;
        player.isJumping = false;
    }
    
    // Move obstacles toward player
    obstacles.forEach(obs => {
        obs.x -= gameSpeed;
    });
    
    // Check collisions
    obstacles.forEach(obs => {
        if (checkCollision(player, obs)) {
            gameOver();
        }
    });
    
    // Spawn new obstacles
    if (shouldSpawnObstacle()) {
        spawnObstacle();
    }
    
    // Increase difficulty
    gameSpeed += 0.001;
}

// Jump handler
function jump() {
    if (!player.isJumping) {
        player.velocityY = JUMP_POWER;
        player.isJumping = true;
    }
}
```

### Best Practices
- Responsive jump controls (immediate feedback)
- Clear obstacle visibility (contrast, size)
- Progressive difficulty (speed increase)
- Visual cues for timing (shadows, distance markers)
- Collectibles for engagement (coins, power-ups)

---

## Bubble Shooter

### Core Mechanics
- Aim and shoot bubbles
- Match 3+ colors
- Bubbles pop and fall
- Clear the board

### Implementation Pattern
```javascript
// Shooter state
const shooter = {
    x: canvas.width / 2,
    y: canvas.height - 50,
    angle: 0,
    currentBubble: null
};

// Aiming
canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    shooter.angle = Math.atan2(
        mouseY - shooter.y,
        mouseX - shooter.x
    );
});

// Shooting
function shoot() {
    if (!shooter.currentBubble || shooter.currentBubble.active) return;
    
    shooter.currentBubble.vx = Math.cos(shooter.angle) * 8;
    shooter.currentBubble.vy = Math.sin(shooter.angle) * 8;
    shooter.currentBubble.active = true;
}

// Update bubble position
function updateBubble(bubble) {
    bubble.x += bubble.vx;
    bubble.y += bubble.vy;
    
    // Wall bounce
    if (bubble.x < RADIUS || bubble.x > width - RADIUS) {
        bubble.vx *= -1;
    }
    
    // Check collision with grid bubbles
    gridBubbles.forEach(gridBubble => {
        const dist = distance(bubble, gridBubble);
        if (dist < RADIUS * 2) {
            // Attach bubble
            attachBubble(bubble, gridBubble);
            checkMatches(bubble.color);
        }
    });
}

// Match detection
function checkMatches(color) {
    const matches = findConnectedBubbles(color);
    if (matches.length >= 3) {
        matches.forEach(bubble => removeBubble(bubble));
        updateScore(matches.length * 10);
    }
}
```

### Best Practices
- Visual aim line (trajectory preview)
- Next bubble preview
- Color accessibility (distinct colors)
- Satisfying pop animation
- Chain reaction bonuses

---

## Puzzle/Physics Games

### Core Mechanics
- Interact with objects
- Physics-based movement
- Solve simple puzzles
- Clear objective

### Implementation Pattern
```javascript
// Simple physics
class PhysicsObject {
    constructor(x, y, mass) {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.mass = mass;
    }
    
    applyForce(fx, fy) {
        this.vx += fx / this.mass;
        this.vy += fy / this.mass;
    }
    
    update() {
        // Apply gravity
        this.applyForce(0, this.mass * 0.5);
        
        // Update position
        this.x += this.vx;
        this.y += this.vy;
        
        // Damping
        this.vx *= 0.98;
        this.vy *= 0.98;
        
        // Ground collision
        if (this.y > groundY) {
            this.y = groundY;
            this.vy *= -0.6; // Bounce
        }
    }
}

// Drag interaction
let draggedObject = null;
let dragOffset = {x: 0, y: 0};

canvas.addEventListener('mousedown', (e) => {
    objects.forEach(obj => {
        if (isPointInObject(e.x, e.y, obj)) {
            draggedObject = obj;
            dragOffset = {
                x: e.x - obj.x,
                y: e.y - obj.y
            };
        }
    });
});

canvas.addEventListener('mousemove', (e) => {
    if (draggedObject) {
        draggedObject.x = e.x - dragOffset.x;
        draggedObject.y = e.y - dragOffset.y;
        draggedObject.vx = 0;
        draggedObject.vy = 0;
    }
});

canvas.addEventListener('mouseup', () => {
    draggedObject = null;
});
```

### Best Practices
- Clear goal indication (target, arrows)
- Intuitive physics (not too realistic)
- Visual feedback on interaction (highlight, drag trail)
- Undo capability (for user error)
- Multiple solution paths

---

## Merge Games

### Core Mechanics
- Drag and drop items
- Merge same items to upgrade
- Unlock new items
- Build/progress

### Implementation Pattern
```javascript
// Item grid
const items = [];

class MergeItem {
    constructor(x, y, level) {
        this.x = x;
        this.y = y;
        this.level = level;
        this.gridX = Math.floor(x / CELL_SIZE);
        this.gridY = Math.floor(y / CELL_SIZE);
    }
    
    snapToGrid() {
        this.gridX = Math.floor(this.x / CELL_SIZE);
        this.gridY = Math.floor(this.y / CELL_SIZE);
        this.x = this.gridX * CELL_SIZE;
        this.y = this.gridY * CELL_SIZE;
    }
}

// Drag and merge logic
let draggedItem = null;

function onDrop(item) {
    item.snapToGrid();
    
    // Check for merge
    const targetItem = items.find(i => 
        i !== item &&
        i.gridX === item.gridX &&
        i.gridY === item.gridY &&
        i.level === item.level
    );
    
    if (targetItem) {
        // Merge items
        items.splice(items.indexOf(targetItem), 1);
        items.splice(items.indexOf(item), 1);
        
        const merged = new MergeItem(
            item.x,
            item.y,
            item.level + 1
        );
        items.push(merged);
        
        // Particle effect
        showMergeEffect(merged.x, merged.y);
        updateScore(item.level * 10);
    }
}
```

### Best Practices
- Clear grid indication
- Smooth drag and drop
- Satisfying merge animation (scale, glow)
- Item progression visual clarity
- Limited grid space (creates strategy)

---

## Hyper-Casual Mechanics

### Common Patterns

**Tap Timing**
```javascript
let isPressed = false;
let power = 0;

function onTapStart() {
    isPressed = true;
    power = 0;
}

function update() {
    if (isPressed) {
        power = Math.min(power + 0.1, 1.0);
    }
}

function onTapEnd() {
    isPressed = false;
    // Use power for action (jump height, shoot distance, etc.)
    performAction(power);
}
```

**Swipe Direction**
```javascript
let touchStart = null;

function onTouchStart(e) {
    touchStart = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY
    };
}

function onTouchEnd(e) {
    if (!touchStart) return;
    
    const dx = e.changedTouches[0].clientX - touchStart.x;
    const dy = e.changedTouches[0].clientY - touchStart.y;
    
    // Determine direction
    if (Math.abs(dx) > Math.abs(dy)) {
        handleSwipe(dx > 0 ? 'right' : 'left');
    } else {
        handleSwipe(dy > 0 ? 'down' : 'up');
    }
    
    touchStart = null;
}
```

---

## Performance Optimization Patterns

### Object Pooling
```javascript
class ObjectPool {
    constructor(createFn, size = 50) {
        this.pool = [];
        this.createFn = createFn;
        
        for (let i = 0; i < size; i++) {
            this.pool.push(createFn());
        }
    }
    
    get() {
        return this.pool.pop() || this.createFn();
    }
    
    release(obj) {
        this.pool.push(obj);
    }
}

// Usage for particles
const particlePool = new ObjectPool(() => ({
    x: 0, y: 0, vx: 0, vy: 0, life: 0
}));
```

### Efficient Rendering
```javascript
// Dirty rectangle optimization
let dirtyRegions = [];

function markDirty(x, y, width, height) {
    dirtyRegions.push({x, y, width, height});
}

function render() {
    // Only redraw dirty regions
    dirtyRegions.forEach(region => {
        ctx.clearRect(region.x, region.y, region.width, region.height);
        drawObjectsInRegion(region);
    });
    
    dirtyRegions = [];
}
```

### Request Animation Frame Pattern
```javascript
let lastTime = 0;
const TARGET_FPS = 60;
const FRAME_TIME = 1000 / TARGET_FPS;

function gameLoop(currentTime) {
    requestAnimationFrame(gameLoop);
    
    const deltaTime = currentTime - lastTime;
    
    if (deltaTime >= FRAME_TIME) {
        lastTime = currentTime - (deltaTime % FRAME_TIME);
        
        update(deltaTime);
        render();
    }
}

requestAnimationFrame(gameLoop);
```
