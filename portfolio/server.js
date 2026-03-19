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

function generateRoomCode() {
  return Math.random().toString(36).substring(2, 8).toUpperCase();
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
  socket.on('createRoom', (playerName, callback) => {
    const roomCode = createRoom();
    const room = getRoom(roomCode);
    
    socket.join(roomCode);
    players.set(socket.id, {
      name: playerName,
      roomCode: roomCode,
      character: null,
      isHost: true
    });
    room.players.push({ socketId: socket.id, name: playerName, isHost: true });
    
    console.log(`Room created: ${roomCode} by ${playerName}`);
    callback({ success: true, roomCode });
  });

  // Join an existing game room
  socket.on('joinRoom', (roomCode, playerName, callback) => {
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
      isHost: false
    });
    room.players.push({ socketId: socket.id, name: playerName, isHost: false });
    
    console.log(`${playerName} joined room: ${roomCode}`);
    
    // Notify both players
    io.to(roomCode).emit('playerJoined', {
      players: room.players,
      status: room.status
    });
    
    callback({ success: true, roomCode });
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

  // Start the game
  socket.on('startGame', (gameData, callback) => {
    const player = players.get(socket.id);
    if (!player) return;
    
    const room = getRoom(player.roomCode);
    if (!room) return;
    
    room.status = 'inProgress';
    room.gameState = {
      players: room.players.map(p => ({
        socketId: p.socketId,
        name: p.name,
        character: p.character,
        hp: gameData.hpByClass[p.character] || 20,
        maxHp: gameData.hpByClass[p.character] || 20,
        dicePool: [],
        hand: [],
        shield: 0,
        statuses: []
      })),
      turn: 0,
      round: 1,
      activePlayerIndex: 0
    };
    
    io.to(player.roomCode).emit('gameStarted', room.gameState);
    callback({ success: true });
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
