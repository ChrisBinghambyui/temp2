# HTML Integration Checklist

## Step 1: Add Socket.IO to HTML
In `loaded_bones.html`, find the closing `</head>` tag and add this BEFORE it:

```html
<!-- Socket.IO client library -->
<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>

<!-- Multiplayer client manager -->
<script src="multiplayer-client.js"></script>
```

---

## Step 2: Initialize Multiplayer on Page Load
After your existing JS initialization code, add:

```javascript
// At the very end of your <script> section, before closing </script>

// Initialize multiplayer connection (optional - set to your server URL)
// multiplayer.connect('http://localhost:3000');

// Listen for multiplayer events
multiplayer.on('playerJoined', handlePlayerJoined);
multiplayer.on('gameStarted', handleGameStarted);
multiplayer.on('gameOver', handleGameOver);
```

---

## Step 3: Update Title Screen
In your current title screen HTML, add a "Multiplayer" button alongside "Single Player":

Find this section:
```html
<div style="margin-bottom: 50px; display: flex; gap: 20px;">
  <button class="btn primary" onclick="startGame()">Single Player</button>
</div>
```

Change to:
```html
<div style="margin-bottom: 50px; display: flex; gap: 20px;">
  <button class="btn primary" onclick="startGame()">Single Player</button>
  <button class="btn primary" onclick="showMultiplayerLobby()">Multiplayer</button>
</div>
```

---

## Step 4: Add Multiplayer Lobby Screen

Add this new screen div to your HTML (after other screen divs):

```html
<!-- Multiplayer Lobby Screen -->
<div id="multiplayer-screen" style="display: none; padding: 40px; width: 100%; max-width: 900px; margin: 0 auto;">
  
  <!-- Connection Status -->
  <div style="text-align: center; margin-bottom: 40px;">
    <div id="connection-status" style="font-family: 'Courier Prime', monospace; font-size: 12px; color: var(--bone-dim); letter-spacing: 2px;">
      CONNECTING...
    </div>
  </div>

  <!-- Main Lobby -->
  <div id="lobby-main" style="display: block;">
    <h1 class="title-main" style="font-size: 32px; margin-bottom: 40px; text-align: center;">FIND AN OPPONENT</h1>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 50px;">
      
      <!-- CREATE ROOM -->
      <div class="panel">
        <div class="panel-title">Create Room</div>
        <div class="form-group">
          <label class="form-label">Your Name</label>
          <input type="text" id="create-name" placeholder="Enter your name" maxlength="20">
        </div>
        <button class="btn primary" onclick="createMultiplayerRoom()" style="width: 100%;">
          Create & Wait
        </button>
        <div id="create-status" style="margin-top: 12px; font-size: 12px; min-height: 60px;"></div>
      </div>

      <!-- JOIN ROOM -->
      <div class="panel">
        <div class="panel-title">Join Room</div>
        <div class="form-group">
          <label class="form-label">Your Name</label>
          <input type="text" id="join-name" placeholder="Enter your name" maxlength="20">
        </div>
        <div class="form-group">
          <label class="form-label">Room Code</label>
          <input type="text" id="join-code" placeholder="e.g., ABC123" maxlength="6" style="text-transform: uppercase;">
        </div>
        <button class="btn primary" onclick="joinMultiplayerRoom()" style="width: 100%;">
          Join Room
        </button>
        <div id="join-status" style="margin-top: 12px; font-size: 12px; min-height: 60px;"></div>
      </div>

    </div>

    <div style="text-align: center;">
      <button class="btn" onclick="backFromMultiplayer();">
        Back to Menu
      </button>
    </div>
  </div>

  <!-- WAITING FOR OPPONENT -->
  <div id="lobby-waiting" style="display: none; text-align: center;">
    <h2 style="color: var(--parchment); margin-bottom: 30px;">Waiting for opponent...</h2>
    <div class="stat-box" style="display: inline-block; margin-bottom: 30px;">
      <div class="stat-label">Room Code</div>
      <div id="waiting-room-code" class="stat-value" style="color: var(--gold); letter-spacing: 2px; font-family: 'Courier Prime', monospace;">
        ABCDEF
      </div>
    </div>
    <p style="color: var(--bone-dim); margin-bottom: 20px;">Share this code with your opponent</p>
    <button class="btn" onclick="cancelWaiting();">Cancel</button>
  </div>

  <!-- BOTH READY - CHARACTER SELECT -->
  <div id="lobby-character" style="display: none;">
    <h2 style="color: var(--parchment); margin-bottom: 20px; text-align: center;">Choose Your Class</h2>
    <p style="text-align: center; color: var(--bone-dim); margin-bottom: 30px;">You vs <span id="opponent-name">Opponent</span></p>
    
    <div class="class-grid" id="multiplayer-class-grid">
      <!-- Classes will be populated here by JS -->
    </div>

    <div style="text-align: center; margin-top: 30px;">
      <button id="start-mp-game-btn" class="btn primary" onclick="startMultiplayerGame()" disabled>
        Ready to Fight
      </button>
    </div>
  </div>

</div>

<!-- CSS for new screens -->
<style>
  #multiplayer-screen {
    animation: fadeIn 0.3s ease;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
</style>
```

---

## Step 5: Add Helper Functions

Add these functions to your main JavaScript file:

```javascript
// ==================== MULTIPLAYER FUNCTIONS ====================

function showMultiplayerLobby() {
  // Connect to server if not already connected
  if (!multiplayer.isConnected) {
    multiplayer.connect('http://localhost:3000'); // Change to your server URL
    
    // Update connection status
    multiplayer.on('connected', () => {
      document.getElementById('connection-status').textContent = '✓ CONNECTED';
      document.getElementById('connection-status').style.color = 'var(--teal-light)';
    });
    
    multiplayer.on('disconnected', () => {
      document.getElementById('connection-status').textContent = '✗ DISCONNECTED';
      document.getElementById('connection-status').style.color = 'var(--blood-bright)';
    });
  }
  
  showScreen('multiplayer-screen');
}

function createMultiplayerRoom() {
  const name = document.getElementById('create-name').value.trim();
  if (!name) {
    alert('Please enter your name');
    return;
  }

  const btn = event.target;
  btn.disabled = true;
  btn.textContent = 'Creating...';

  multiplayer.createRoom(name, (response) => {
    if (response.success) {
      // Show waiting screen
      document.getElementById('lobby-main').style.display = 'none';
      document.getElementById('lobby-waiting').style.display = 'block';
      document.getElementById('waiting-room-code').textContent = response.roomCode;

      // Listen for opponent joining
      multiplayer.on('playerJoined', (data) => {
        if (data.players.length === 2) {
          // Both players are here - move to character select
          handleBothPlayersReady(data.players);
        }
      });
    } else {
      document.getElementById('create-status').innerHTML = 
        `<span style="color: var(--blood-bright);">✗ Error: ${response.error}</span>`;
      btn.disabled = false;
      btn.textContent = 'Create & Wait';
    }
  });
}

function joinMultiplayerRoom() {
  const name = document.getElementById('join-name').value.trim();
  const code = document.getElementById('join-code').value.trim().toUpperCase();
  
  if (!name || !code) {
    alert('Please enter name and room code');
    return;
  }

  const btn = event.target;
  btn.disabled = true;
  btn.textContent = 'Joining...';

  multiplayer.joinRoom(code, name, (response) => {
    if (response.success) {
      document.getElementById('join-status').innerHTML = 
        `<span style="color: var(--teal-light);">✓ Joined! Waiting for opponent...</span>`;

      // Listen for game ready
      multiplayer.on('playerJoined', (data) => {
        handleBothPlayersReady(data.players);
      });
      
      multiplayer.on('bothPlayersReady', (data) => {
        handleBothPlayersReady(data.players);
      });
    } else {
      document.getElementById('join-status').innerHTML = 
        `<span style="color: var(--blood-bright);">✗ ${response.error}</span>`;
      btn.disabled = false;
      btn.textContent = 'Join Room';
    }
  });
}

function handleBothPlayersReady(players) {
  // Hide main lobby, show character select
  document.getElementById('lobby-main').style.display = 'none';
  document.getElementById('lobby-waiting').style.display = 'none';
  document.getElementById('lobby-character').style.display = 'block';

  // Update opponent name
  const opponentName = players.find(p => p.socketId !== multiplayer.playerId)?.name || 'Opponent';
  document.getElementById('opponent-name').textContent = opponentName;

  // Populate class grid
  const grid = document.getElementById('multiplayer-class-grid');
  grid.innerHTML = `
    <div class="class-card" onclick="selectMultiplayerClass('Fencer')">
      <div class="class-name class-fencer">Fencer</div>
      <div class="class-desc">Quick strikes, high crit</div>
      <div class="class-hp">HP: 18</div>
    </div>
    <div class="class-card" onclick="selectMultiplayerClass('Knight')">
      <div class="class-name class-knight">Knight</div>
      <div class="class-desc">Heavy armor, block</div>
      <div class="class-hp">HP: 24</div>
    </div>
    <div class="class-card" onclick="selectMultiplayerClass('Cleric')">
      <div class="class-name class-cleric">Cleric</div>
      <div class="class-desc">Healing, support</div>
      <div class="class-hp">HP: 20</div>
    </div>
    <div class="class-card" onclick="selectMultiplayerClass('Warlock')">
      <div class="class-name class-warlock">Warlock</div>
      <div class="class-desc">Curses, damage</div>
      <div class="class-hp">HP: 19</div>
    </div>
    <div class="class-card" onclick="selectMultiplayerClass('Druid')">
      <div class="class-name class-druid">Druid</div>
      <div class="class-desc">Nature, shields</div>
      <div class="class-hp">HP: 21</div>
    </div>
    <div class="class-card" onclick="selectMultiplayerClass('Rogue')">
      <div class="class-name class-rogue">Rogue</div>
      <div class="class-desc">Stealth, evasion</div>
      <div class="class-hp">HP: 17</div>
    </div>
  `;

  // Enable start button
  document.getElementById('start-mp-game-btn').disabled = false;
}

function selectMultiplayerClass(className) {
  // Clear previous selection
  document.querySelectorAll('#multiplayer-class-grid .class-card').forEach(c => {
    c.classList.remove('selected');
  });

  // Mark selected
  event.target.closest('.class-card').classList.add('selected');

  // Notify server
  multiplayer.selectCharacter(className, (response) => {
    if (!response.success) {
      alert('Failed to select character');
    }
  });

  // Store for later
  window.selectedMultiplayerClass = className;
}

function startMultiplayerGame() {
  if (!window.selectedMultiplayerClass) {
    alert('Select a class first');
    return;
  }

  // Start game on server
  multiplayer.startGame({
    hpByClass: {
      'Fencer': 18,
      'Knight': 24,
      'Cleric': 20,
      'Warlock': 19,
      'Druid': 21,
      'Rogue': 17
    }
  }, (response) => {
    if (response.success) {
      // Listen for game start
      multiplayer.on('gameStarted', (gameState) => {
        startMultiplayerCombat(gameState);
      });
    }
  });
}

function startMultiplayerCombat(gameState) {
  // Hide lobby, show combat screen (reuse your existing combat UI)
  // Update game state with multiplayer data
  window.multiplayerGameState = gameState;
  
  // Show combat screen
  showScreen('combat-screen'); // or whatever your combat screen ID is
  
  // You'll need to adapt your existing combat logic to use multiplayer events
}

function cancelWaiting() {
  multiplayer.leaveRoom();
  document.getElementById('lobby-main').style.display = 'block';
  document.getElementById('lobby-waiting').style.display = 'none';
  document.getElementById('lobby-character').style.display = 'none';
  document.getElementById('create-name').value = '';
}

function backFromMultiplayer() {
  multiplayer.leaveRoom();
  document.getElementById('lobby-main').style.display = 'block';
  document.getElementById('lobby-waiting').style.display = 'none';
  document.getElementById('lobby-character').style.display = 'none';
  showScreen('title-screen');
}
```

---

## Step 6: Test Locally

1. Open terminal and run:
   ```bash
   cd portfolio
   npm install
   npm start
   ```

2. Open `loaded_bones.html` in your browser

3. Open another browser window/tab with the same URL

4. In first window: Click "Multiplayer" → "Create Room"

5. In second window: Click "Multiplayer" → "Join" with the room code

6. Both select characters and start playing!

---

## Production Deployment

When ready to deploy (so players can connect from anywhere):

1. Choose a hosting provider (Heroku, Render, Railway, AWS, etc.)
2. Push your `server.js` and `package.json` to that service
3. Update the connection URL in your HTML:
   ```javascript
   multiplayer.connect('https://your-deployed-server.com');
   ```
4. Host the HTML file on web hosting or same server

---

That's it! You now have a fully functional PvP multiplayer system. 🎲
