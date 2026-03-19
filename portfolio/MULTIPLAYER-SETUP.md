# LOADED BONES - Multiplayer Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd portfolio
npm install
```

### 2. Start the Server
```bash
npm start
# or for development with auto-reload:
npm run dev
```

The server will run on `http://localhost:3000`

### 3. Update HTML File
In `loaded_bones.html`, add these lines in the `<head>` section (before closing `</head>`):

```html
<!-- Socket.IO client -->
<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<!-- Multiplayer manager -->
<script src="multiplayer-client.js"></script>
```

### 4. Update Server URL (if needed)
If your server is not on `localhost:3000`, call:
```javascript
multiplayer.connect('http://your-server-url:PORT');
```

---

## Game Flow

### Creating a Game
```javascript
multiplayer.createRoom('PlayerName', (response) => {
  if (response.success) {
    const roomCode = response.roomCode;
    console.log(`Share this code: ${roomCode}`);
  }
});
```

### Joining a Game
```javascript
multiplayer.joinRoom('ROOM_CODE', 'PlayerName', (response) => {
  if (response.success) {
    console.log('Joined room!');
  }
});
```

### Game Events
Listen for events with:
```javascript
multiplayer.on('playerJoined', (data) => {
  console.log('Opponent joined!', data.players);
});

multiplayer.on('gameStarted', (gameState) => {
  console.log('Game started!', gameState);
});

multiplayer.on('gameOver', (data) => {
  console.log(`${data.winner} wins!`);
});
```

---

## Available Events

| Event | Data | Purpose |
|-------|------|---------|
| `connected` | - | Connected to server |
| `disconnected` | - | Disconnected from server |
| `playerJoined` | `{players, status}` | Opponent joined |
| `bothPlayersReady` | `{players}` | Both have selected characters |
| `gameStarted` | `gameState` | Match begins |
| `diceRolled` | `{playerName, rolls}` | Player rolled dice |
| `cardPlayed` | `{playerName, cardIndex, targetPlayer, gameState}` | Card used |
| `turnEnded` | `{gameState}` | Turn switched |
| `damageApplied` | `{targetPlayer, damage, shieldDamage, hpRemaining, gameState}` | Damage dealt |
| `gameOver` | `{winner, loser}` | Match ended |
| `playerLeft` | `{players}` | Opponent left room |
| `playerDisconnected` | `{players}` | Opponent disconnected |

---

## Key Functions

### Room Management
- `multiplayer.createRoom(name, callback)` - Create new game
- `multiplayer.joinRoom(code, name, callback)` - Join existing game
- `multiplayer.leaveRoom()` - Leave current room
- `multiplayer.getRoomCode()` - Get current room code

### Game Actions
- `multiplayer.selectCharacter(character, callback)` - Pick class
- `multiplayer.startGame(gameData, callback)` - Begin match
- `multiplayer.rollDice(count, callback)` - Roll dice pool
- `multiplayer.playCard(cardIndex, targetSocketId, callback)` - Use spellcard
- `multiplayer.endTurn(callback)` - Next turn
- `multiplayer.takeDamage(damage, targetSocketId, callback)` - Apply damage

### Utilities
- `multiplayer.isInMultiplayer()` - Check if in multiplayer
- `multiplayer.getOpponents(allPlayers)` - Get opponent list
- `multiplayer.on(event, handler)` - Listen for event
- `multiplayer.off(event, handler)` - Stop listening

---

## Lobby Screen HTML Integration

Add this to the main game screen selection to enable multiplayer:

```html
<div id="multiplayer-lobby" style="display: none; padding: 24px; width: 100%;">
  <div style="max-width: 700px; margin: 0 auto;">
    <h1 class="title-main" style="font-size: 36px; margin-bottom: 40px;">MULTIPLAYER</h1>
    
    <div style="display: flex; gap: 30px; flex-wrap: wrap; margin-bottom: 50px;">
      <!-- Create Room -->
      <div class="panel" style="flex: 1; min-width: 250px;">
        <div class="panel-title">Create Game</div>
        <input type="text" id="create-player-name" placeholder="Your name" style="margin-bottom: 12px;">
        <button class="btn primary" onclick="startCreateRoom()" style="width: 100%;">
          Create Room
        </button>
        <div id="create-result" style="margin-top: 12px; font-size: 12px;"></div>
      </div>

      <!-- Join Room -->
      <div class="panel" style="flex: 1; min-width: 250px;">
        <div class="panel-title">Join Game</div>
        <input type="text" id="join-room-code" placeholder="Room code" style="margin-bottom: 12px;">
        <input type="text" id="join-player-name" placeholder="Your name" style="margin-bottom: 12px;">
        <button class="btn primary" onclick="startJoinRoom()" style="width: 100%;">
          Join Room
        </button>
        <div id="join-result" style="margin-top: 12px; font-size: 12px;"></div>
      </div>
    </div>

    <button class="btn" onclick="backToMainMenu()" style="width: 100%; max-width: 200px;">
      Back to Menu
    </button>
  </div>
</div>
```

Add these functions to your main JavaScript:

```javascript
function startCreateRoom() {
  const name = document.getElementById('create-player-name').value.trim();
  if (!name) {
    alert('Please enter a name');
    return;
  }

  multiplayer.createRoom(name, (response) => {
    const resultDiv = document.getElementById('create-result');
    if (response.success) {
      resultDiv.innerHTML = `
        <span style="color: var(--teal-light);">✓ Room created!</span>
        <div style="margin-top: 8px;">
          <strong>Room Code:</strong> <span style="color: var(--gold);">${response.roomCode}</span>
        </div>
        <div style="margin-top: 8px; font-size: 11px; color: var(--bone-dim);">
          Share this code with your opponent to join.
        </div>
      `;
      // Disable inputs and show waiting message
      document.getElementById('create-player-name').disabled = true;
      document.querySelector('[onclick="startCreateRoom()"]').disabled = true;
    } else {
      resultDiv.innerHTML = `<span style="color: var(--blood-bright);">✗ ${response.error}</span>`;
    }
  });
}

function startJoinRoom() {
  const code = document.getElementById('join-room-code').value.trim().toUpperCase();
  const name = document.getElementById('join-player-name').value.trim();
  
  if (!code || !name) {
    alert('Please enter room code and name');
    return;
  }

  multiplayer.joinRoom(code, name, (response) => {
    const resultDiv = document.getElementById('join-result');
    if (response.success) {
      resultDiv.innerHTML = `<span style="color: var(--teal-light);">✓ Joined room!</span>`;
    } else {
      resultDiv.innerHTML = `<span style="color: var(--blood-bright);">✗ ${response.error}</span>`;
    }
  });
}

function backToMainMenu() {
  multiplayer.leaveRoom();
  // Return to title screen
  showScreen('title-screen');
}
```

---

## Deploying to Production

### Using Heroku
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Using render.com (Free tier)
1. Push code to GitHub
2. Connect to render.com
3. Create Web Service
4. Build: `npm install`
5. Start: `npm start`

### Using Railway.app
Similar to render.com - connect GitHub, it auto-deploys.

---

## Troubleshooting

**Cannot connect to server**
- Check server is running: `npm start`
- Check port 3000 is not blocked by firewall
- Verify correct URL in `multiplayer.connect()`

**Room code not working**
- Room codes are case-sensitive
- Check both players are on the same server URL
- Refresh page and try again

**Players not syncing**
- Check browser console for errors
- Verify both clients loaded `multiplayer-client.js`
- Check network tab - should see WebSocket connection

**Server won't start**
- Run `npm install` first
- Check Node.js version (v14+)
- Check port 3000 is free: `netstat -ano | findstr :3000`

---

## Architecture Overview

```
loaded_bones.html (Client)
    ↓
multiplayer-client.js (WebSocket Manager)
    ↓
Socket.IO ↔ http://localhost:3000 (server.js)
    ↓
Game Room Management + State Sync
```

Each room maintains:
- Player info (name, character, host status)
- Game state (HP, dice, cards, turn)
- Real-time event broadcasting

---

## Next Steps

1. Run `npm install` and `npm start`
2. Add Socket.IO script and multiplayer-client.js to HTML
3. Integrate lobby UI into your game
4. Test with two browser windows
5. Deploy server to production

Good luck crushing your opponents! 🎲
