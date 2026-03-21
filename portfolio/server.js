import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: "*", methods: ["GET", "POST"] }
});

app.use(cors());
app.use(express.static('public'));
app.use(express.json());

// ==================== GAME STATE ====================
const rooms = new Map(); // roomCode -> { players, gameState, turn }
const players = new Map(); // socketId -> { name, roomCode, character }

function normalizePlayerPayload(input) {
  if (typeof input === 'string') {
    const safe = input.trim();
    return { name: safe && safe !== '[object Object]' ? safe : '', profile: null };
  }

  const name = typeof input?.name === 'string'
    ? input.name.trim()
    : '';
  const rawProfile = input?.profile && typeof input.profile === 'object' ? input.profile : null;

  if (!rawProfile) {
    return { name: name !== '[object Object]' ? name : '', profile: null };
  }

  const profile = {
    level: Math.max(1, Number(rawProfile.level) || 1),
    maxHp: Math.max(1, Number(rawProfile.maxHp) || 1),
    hp: Math.max(1, Number(rawProfile.hp) || 1),
    classId: typeof rawProfile.classId === 'string' ? rawProfile.classId : null,
    className: typeof rawProfile.className === 'string' ? rawProfile.className : null,
    handLimit: Number(rawProfile.handLimit) || null,
    diceLimit: Number(rawProfile.diceLimit) || null,
    deck: Array.isArray(rawProfile.deck) ? rawProfile.deck : []
  };

  profile.hp = Math.min(profile.hp, profile.maxHp);
  return { name: name !== '[object Object]' ? name : '', profile };
}

function generateRoomCode() {
  const alphabet = 'ABCDEFGHIJKLMNPQRSTUVWXYZ123456789';
  let code = '';
  for (let i = 0; i < 6; i++) {
    const idx = Math.floor(Math.random() * alphabet.length);
    code += alphabet[idx];
  }
  return code;
}

function createRoom() {
  let code = generateRoomCode();
  while (rooms.has(code)) {
    code = generateRoomCode();
  }
  rooms.set(code, {
    players: [],
    gameState: null,
    turn: 0,
    status: 'waiting' // waiting, ready, inProgress, finished
  });
  return code;
}

function getRoom(roomCode) {
  return rooms.get(roomCode);
}

function deleteRoom(roomCode) {
  rooms.delete(roomCode);
}

// ==================== SOCKET EVENTS ====================

io.on('connection', (socket) => {
  console.log(`Player connected: ${socket.id}`);

  // Create a new game room
  socket.on('createRoom', (playerPayload, callback) => {
    const { name: parsedName, profile } = normalizePlayerPayload(playerPayload);
    const playerName = parsedName || 'Host';
    const roomCode = createRoom();
    const room = getRoom(roomCode);
    
    socket.join(roomCode);
    players.set(socket.id, {
      name: playerName,
      roomCode: roomCode,
      character: null,
      isHost: true,
      profile
    });
    room.players.push({ socketId: socket.id, name: playerName, isHost: true, profile });
    
    console.log(`Room created: ${roomCode} by ${playerName}`);
    callback({ success: true, roomCode });
  });

  // Join an existing game room
  socket.on('joinRoom', (roomCode, playerPayload, callback) => {
    const { name: parsedName, profile } = normalizePlayerPayload(playerPayload);
    const playerName = parsedName || 'Guest';
    const room = getRoom(roomCode);
    
    if (!room) {
      callback({ success: false, error: 'Room not found' });
      return;
    }
    
    if (room.players.length >= 2) {
      callback({ success: false, error: 'Room is full' });
      return;
    }
    
    if (room.status !== 'waiting') {
      callback({ success: false, error: 'Game already in progress' });
      return;
    }
    
    socket.join(roomCode);
    players.set(socket.id, {
      name: playerName,
      roomCode: roomCode,
      character: null,
      isHost: false,
      profile
    });
    room.players.push({ socketId: socket.id, name: playerName, isHost: false, profile });
    
    console.log(`${playerName} joined room: ${roomCode}`);
    
    // Notify both players
    io.to(roomCode).emit('playerJoined', {
      players: room.players,
      status: room.status
    });
    
    callback({ success: true, roomCode });
  });

  socket.on('updateProfile', (profilePayload, callback) => {
    const player = players.get(socket.id);
    if (!player) {
      if (callback) callback({ success: false, error: 'Player not found' });
      return;
    }

    const room = getRoom(player.roomCode);
    if (!room) {
      if (callback) callback({ success: false, error: 'Room not found' });
      return;
    }

    const normalized = normalizePlayerPayload({
      name: player.name,
      profile: profilePayload
    }).profile;

    player.profile = normalized;

    const roomPlayer = room.players.find(p => p.socketId === socket.id);
    if (roomPlayer) {
      roomPlayer.profile = normalized;
    }

    if (callback) callback({ success: true });
  });

  // Select character and start game
  socket.on('selectCharacter', (character, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    player.character = character;
    
    // Update player in room
    const roomPlayer = room.players.find(p => p.socketId === socket.id);
    if (roomPlayer) {
      roomPlayer.character = character;
    }
    
    // Check if both players have selected characters
    if (room.players.length === 2 && room.players.every(p => p.character)) {
      room.status = 'ready';
      io.to(player.roomCode).emit('bothPlayersReady', {
        players: room.players
      });
    }
    
    callback({ success: true });
  });

  // Enter deck building phase
  socket.on('enterDeckBuilder', (callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    if (!room.deckSubmissions) {
      room.deckSubmissions = {};
    }
    
    room.status = 'deckBuilding';
    
    io.to(player.roomCode).emit('deckBuilderStarted', {
      status: 'deckBuilding'
    });
    
    callback({ success: true });
  });

  // Submit deck for the match
  socket.on('submitDeck', (deckCards, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    if (!room.deckSubmissions) {
      room.deckSubmissions = {};
    }
    
    // Store the deck for this player
    room.deckSubmissions[socket.id] = {
      deck: Array.isArray(deckCards) ? deckCards : [],
      ready: true
    };
    
    // Notify opponent that this player is ready
    io.to(player.roomCode).emit('opponentDeckReady', {
      playerName: player.name
    });
    
    // Check if both players have submitted decks
    const submittedCount = Object.keys(room.deckSubmissions).filter(id => room.deckSubmissions[id]?.ready).length;
    
    if (submittedCount === 2 && room.players.length === 2) {
      // Both players are ready to start the game
      const response = {
        success: true,
        bothReady: true,
        gameState: {
          players: room.players,
          decks: room.deckSubmissions,
          status: 'ready_to_start'
        }
      };
      
      io.to(player.roomCode).emit('bothPlayersDecksReady', response);
      callback(response);
    } else {
      callback({
        success: true,
        bothReady: false,
        message: 'Deck submitted. Waiting for opponent.'
      });
    }
  });

  // Start the game
  socket.on('startGame', (gameData, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;

    // Idempotent start: if already running, send current state so late callers can recover.
    if (room.status === 'inProgress' && room.gameState) {
      if (callback) callback({ success: true, alreadyStarted: true, gameState: room.gameState });
      return;
    }

    const readyDeckCount = Object.keys(room.deckSubmissions || {}).filter(id => room.deckSubmissions[id]?.ready).length;
    if (room.players.length !== 2 || readyDeckCount !== 2) {
      if (callback) callback({ success: false, error: 'Both players must submit decks before starting.' });
      return;
    }
    
    room.status = 'inProgress';
    room.gameState = {
      players: room.players.map(p => {
        // Get the submitted deck for this player, or use empty array as fallback
        const submittedDeck = room.deckSubmissions?.[p.socketId]?.deck || [];
        const profile = p.profile || {};
        const profileDeck = Array.isArray(profile.deck) ? profile.deck : [];
        const deck = submittedDeck.length > 0 ? submittedDeck : profileDeck;
        const classKey = p.character;
        const fallbackClassHp = gameData.hpByClass[classKey] || 20;
        const maxHp = Math.max(1, Number(profile.maxHp) || fallbackClassHp);
        const hp = Math.max(1, Math.min(maxHp, Number(profile.hp) || maxHp));
        
        const safeName = typeof p.name === 'string'
          ? (p.name.trim() && p.name.trim() !== '[object Object]' ? p.name.trim() : 'Player')
          : String(p?.name?.name || p.name || '').trim() || 'Player';

        return {
          socketId: p.socketId,
          name: safeName,
          character: p.character,
          level: Math.max(1, Number(profile.level) || 1),
          handLimit: Number(profile.handLimit) || null,
          diceLimit: Number(profile.diceLimit) || null,
          hp,
          maxHp,
          deck,
          dicePool: [],
          hand: [],
          shield: 0,
          statuses: []
        };
      }),
      turn: 0,
      round: 1,
      activePlayerIndex: 0
    };
    
    io.to(player.roomCode).emit('gameStarted', room.gameState);
    callback({ success: true, gameState: room.gameState });
  });

  // Player rolls dice
  socket.on('rollDice', (diceCount, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    const gameState = room.gameState;
    const currentPlayer = gameState.players.find(p => p.socketId === socket.id);
    
    if (!currentPlayer) return;
    
    // Generate random dice values
    const rolls = Array.from({ length: diceCount }, () => Math.floor(Math.random() * 6) + 1);
    currentPlayer.dicePool = rolls;
    
    io.to(player.roomCode).emit('diceRolled', {
      playerName: currentPlayer.name,
      rolls: rolls
    });
    
    callback({ success: true, rolls });
  });

  // Player plays card
  socket.on('playCard', (cardIndex, targetPlayerId, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    const gameState = room.gameState;
    const currentPlayer = gameState.players.find(p => p.socketId === socket.id);
    const targetPlayer = gameState.players.find(p => p.socketId === targetPlayerId);
    
    if (!currentPlayer || !targetPlayer) return;
    
    // Card is played - you'd validate this based on your game rules
    io.to(player.roomCode).emit('cardPlayed', {
      playerName: currentPlayer.name,
      cardIndex: cardIndex,
      targetPlayer: targetPlayer.name,
      gameState: gameState
    });
    
    callback({ success: true });
  });

  // End turn
  socket.on('endTurn', (callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    const gameState = room.gameState;
    
    // Switch to next player
    gameState.activePlayerIndex = gameState.activePlayerIndex === 0 ? 1 : 0;
    gameState.turn++;
    
    if (gameState.activePlayerIndex === 0) {
      gameState.round++;
    }
    
    io.to(player.roomCode).emit('turnEnded', {
      gameState: gameState
    });
    
    callback({ success: true });
  });

  // Generic real-time combat relay for client-authoritative PvP visuals/state
  socket.on('combatAction', (payload, callback) => {
    const player = players.get(socket.id);
    if (!player) {
      if (callback) callback({ success: false, error: 'Player not found' });
      return;
    }

    const room = getRoom(player.roomCode);
    if (!room) {
      if (callback) callback({ success: false, error: 'Room not found' });
      return;
    }

    io.to(player.roomCode).emit('combatAction', {
      ...payload,
      actorId: socket.id,
      actorName: player.name,
      roomCode: player.roomCode,
      ts: Date.now()
    });

    if (callback) callback({ success: true });
  });

  // Player takes damage
  socket.on('takeDamage', (damage, targetSocketId, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    const targetPlayer = room.gameState.players.find(p => p.socketId === targetSocketId);
    if (!targetPlayer) return;
    
    // Apply shield first
    const shieldDamage = Math.min(damage, targetPlayer.shield);
    targetPlayer.shield -= shieldDamage;
    const remainingDamage = damage - shieldDamage;
    
    targetPlayer.hp -= remainingDamage;
    targetPlayer.hp = Math.max(0, targetPlayer.hp);
    
    io.to(player.roomCode).emit('damageApplied', {
      targetPlayer: targetPlayer.name,
      damage: damage,
      shieldDamage: shieldDamage,
      hpRemaining: targetPlayer.hp,
      gameState: room.gameState
    });
    
    // Check for game over
    if (targetPlayer.hp <= 0) {
      const winner = room.gameState.players.find(p => p.socketId !== targetSocketId);
      io.to(player.roomCode).emit('gameOver', {
        winner: winner.name,
        loser: targetPlayer.name
      });
      room.status = 'finished';
    }
    
    callback({ success: true });
  });

  // Leave room
  socket.on('leaveRoom', () => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (room) {
      room.players = room.players.filter(p => p.socketId !== socket.id);
      
      if (room.players.length === 0) {
        deleteRoom(player.roomCode);
      } else {
        io.to(player.roomCode).emit('playerLeft', {
          players: room.players
        });
      }
    }
    
    players.delete(socket.id);
    socket.leave(player.roomCode);
  });

  socket.on('disconnect', () => {
    console.log(`Player disconnected: ${socket.id}`);
    const player = players.get(socket.id);
    if (player) {
      const room = getRoom(player.roomCode);
      if (room) {
        room.players = room.players.filter(p => p.socketId !== socket.id);
        
        if (room.players.length === 0) {
          deleteRoom(player.roomCode);
        } else {
          io.to(player.roomCode).emit('playerDisconnected', {
            players: room.players
          });
        }
      }
      players.delete(socket.id);
    }
  });
});

const PORT = process.env.PORT || 3000;
httpServer.listen(PORT, () => {
  console.log(`🎲 LOADED BONES multiplayer server running on port ${PORT}`);
});
