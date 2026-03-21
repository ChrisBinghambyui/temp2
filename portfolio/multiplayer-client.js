// ==================== MULTIPLAYER CLIENT ====================
// Include this in loaded_bones.html after socket.io client script

class MultiplayerManager {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.currentRoom = null;
    this.playerId = null;
    this.isHost = false;
    this.mode = 'single'; // 'single' or 'multiplayer'
    this.opponentId = null;
    this.listeners = {};
  }

  connect(serverUrl = 'http://localhost:3000') {
    if (typeof io === 'undefined') {
      console.error('Socket.IO client not loaded. Add: <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>');
      return;
    }

    this.socket = io(serverUrl, {
      transports: ['websocket', 'polling']
    });

    this.socket.on('connect', () => {
      console.log('Connected to multiplayer server');
      this.isConnected = true;
      this.playerId = this.socket.id;
      this.emit('connected');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from multiplayer server');
      this.isConnected = false;
      this.emit('disconnected');
    });

    // Game events
    this.socket.on('playerJoined', (data) => this.emit('playerJoined', data));
    this.socket.on('bothPlayersReady', (data) => this.emit('bothPlayersReady', data));
    this.socket.on('gameStarted', (gameState) => this.emit('gameStarted', gameState));
    this.socket.on('diceRolled', (data) => this.emit('diceRolled', data));
    this.socket.on('cardPlayed', (data) => this.emit('cardPlayed', data));
    this.socket.on('turnEnded', (data) => this.emit('turnEnded', data));
    this.socket.on('damageApplied', (data) => this.emit('damageApplied', data));
    this.socket.on('gameOver', (data) => this.emit('gameOver', data));
    this.socket.on('playerLeft', (data) => this.emit('playerLeft', data));
    this.socket.on('playerDisconnected', (data) => this.emit('playerDisconnected', data));
    this.socket.on('combatAction', (data) => this.emit('combatAction', data));
    
    // Deck builder events
    this.socket.on('deckBuilderStarted', (data) => this.emit('deckBuilderStarted', data));
    this.socket.on('opponentDeckReady', (data) => this.emit('opponentDeckReady', data));
    this.socket.on('bothPlayersDecksReady', (data) => this.emit('bothPlayersDecksReady', data));
  }

  // ==================== ROOM MANAGEMENT ====================

  createRoom(playerData, callback) {
    if (!this.isConnected) {
      callback({ success: false, error: 'Not connected to server' });
      return;
    }

    const isObj = playerData && typeof playerData === 'object';
    const rawName = isObj ? playerData?.name : playerData;
    const playerName = (typeof rawName === 'string' && rawName.trim() && rawName.trim() !== '[object Object]')
      ? rawName.trim()
      : 'Host';
    const profile = isObj ? playerData.profile : null;

    this.socket.emit('createRoom', playerName, (response) => {
      if (response.success) {
        this.currentRoom = response.roomCode;
        this.playerId = this.socket.id;
        this.isHost = true;
        this.mode = 'multiplayer';
      }
      callback(response);

      // Profile sync is best-effort and must never block room creation UI.
      if (response.success && profile && typeof profile === 'object') {
        this.updateProfile(profile, () => {});
      }
    });
  }

  joinRoom(roomCode, playerData, callback) {
    if (!this.isConnected) {
      callback({ success: false, error: 'Not connected to server' });
      return;
    }

    const isObj = playerData && typeof playerData === 'object';
    const rawName = isObj ? playerData?.name : playerData;
    const playerName = (typeof rawName === 'string' && rawName.trim() && rawName.trim() !== '[object Object]')
      ? rawName.trim()
      : 'Guest';
    const profile = isObj ? playerData.profile : null;

    this.socket.emit('joinRoom', roomCode, playerName, (response) => {
      if (response.success) {
        this.currentRoom = roomCode;
        this.playerId = this.socket.id;
        this.isHost = false;
        this.mode = 'multiplayer';
      }
      callback(response);

      // Profile sync is best-effort and must never block room join UI.
      if (response.success && profile && typeof profile === 'object') {
        this.updateProfile(profile, () => {});
      }
    });
  }

  updateProfile(profile, callback = () => {}) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('updateProfile', profile, (response) => {
      callback(response);
    });
  }

  getRoomCode() {
    return this.currentRoom;
  }

  // ==================== CHARACTER SELECTION ====================

  selectCharacter(character, callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('selectCharacter', character, (response) => {
      callback(response);
    });
  }

  // ==================== GAME ACTIONS ====================

  startGame(gameData, callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('startGame', gameData, (response) => {
      callback(response);
    });
  }

  // ==================== DECK BUILDER ====================

  enterDeckBuilder(callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('enterDeckBuilder', (response) => {
      callback(response);
    });
  }

  submitDeck(deckCards, callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('submitDeck', deckCards, (response) => {
      callback(response);
    });
  }

  // ==================== GAME ACTIONS ====================

  rollDice(diceCount, callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('rollDice', diceCount, (response) => {
      callback(response);
    });
  }
  playCard(cardIndex, targetPlayerId, callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('playCard', cardIndex, targetPlayerId, (response) => {
      callback(response);
    });
  }

  endTurn(callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('endTurn', (response) => {
      callback(response);
    });
  }

  takeDamage(damage, targetSocketId, callback) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('takeDamage', damage, targetSocketId, (response) => {
      callback(response);
    });
  }

  sendCombatAction(action, callback = () => {}) {
    if (!this.isConnected || !this.currentRoom) {
      callback({ success: false, error: 'Not in a room' });
      return;
    }

    this.socket.emit('combatAction', action, (response) => {
      callback(response);
    });
  }

  leaveRoom() {
    if (this.isConnected && this.currentRoom) {
      this.socket.emit('leaveRoom');
      this.currentRoom = null;
      this.mode = 'single';
    }
  }

  // ==================== EVENT LISTENING ====================

  on(event, handler) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(handler);
  }

  off(event, handler) {
    if (!this.listeners[event]) return;
    this.listeners[event] = this.listeners[event].filter(h => h !== handler);
  }

  emit(event, data) {
    if (!this.listeners[event]) return;
    this.listeners[event].forEach(handler => handler(data));
  }

  // ==================== UTILITY ====================

  isInMultiplayer() {
    return this.mode === 'multiplayer' && this.isConnected && this.currentRoom;
  }

  getOpponents(allPlayers) {
    return allPlayers.filter(p => p.socketId !== this.playerId);
  }
}

// Create global instance
const multiplayer = new MultiplayerManager();
