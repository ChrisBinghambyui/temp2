# Multiplayer Server Setup & Launch Guide

## Quick Start

**Once you have everything installed (see Setup below), just run:**
```
start-multiplayer.bat
```

This will automatically:
1. Start ngrok tunnel (creates public URL)
2. Start your Node.js server
3. Display your public URL for friends to use

---

## Setup (One-Time Only)

### 1. Install ngrok
- Download from: https://ngrok.com/download
- Extract to a folder (e.g., `C:\ngrok`)
- Add ngrok to your system PATH:
  - Right-click "This PC" → Properties
  - Advanced system settings → Environment Variables
  - New User Variable: `Path` = `C:\ngrok` (or your ngrok folder)
  - Restart your computer

**Test:** Open PowerShell and run `ngrok --version` — should show version number.

### 2. Install Node.js (if not already done)
- Download from: https://nodejs.org (LTS recommended)
- Run installer, accept defaults
- Restart your computer

**Test:** Open PowerShell and run `node --version` and `npm --version` — should show version numbers.

### 3. Install project dependencies
```powershell
cd "c:\Users\chris\Downloads\chris hw\temp2\portfolio"
npm install
```

---

## Running the Server

### Every Time You Restart:

**Option A: Automatic (Recommended)**
- Double-click `start-multiplayer.bat` in your portfolio folder
- Wait ~3 seconds, two windows will open:
  - NGrok window (shows your public URL)
  - Server window (shows connection logs)

**Option B: Manual**
1. Open PowerShell in portfolio folder
2. Run: `ngrok http 3000` (copy the HTTPS URL)
3. Open another PowerShell window in portfolio folder
4. Run: `npm.cmd start`
5. Share the ngrok HTTPS URL with friends

---

## Sharing with Friends

1. When the server is running, look at the **ngrok window**
2. Find the line: `Forwarding    https://abc123def456.ngrok.io -> http://localhost:3000`
3. Copy that **HTTPS URL** (e.g., `https://abc123def456.ngrok.io`)
4. Update `loaded_bones.html` line ~4548:
   ```javascript
   const MULTIPLAYER_SERVER_URL = 'https://abc123def456.ngrok.io';
   ```
5. Commit and push to GitHub
6. Send friends your GitHub Pages link
7. They can now create/join rooms and fight!

---

## Important Notes

- **ngrok URL changes each restart.** Update the URL in the game code every time.
- **Your computer must stay on.** If you shut down, friends can't connect.
- **ngrok free tier is fine** for testing with friends. If you want a fixed URL, upgrade ngrok account.
- **Firewall:** If friends can't connect, check Windows Firewall (allow Node.js through).

---

## Troubleshooting

**ngrok command not found:**
- Make sure ngrok is installed and in PATH
- Restart PowerShell/computer after installing

**npm.cmd not found:**
- Install Node.js from nodejs.org

**Friends say "connection refused":**
- Check that ngrok window shows "Forwarding" line
- Verify you updated the URL in loaded_bones.html
- Make sure your server window isn't showing errors

**Port 3000 already in use:**
- Close any other Node processes (see conversation history)
- Or change port in server.js (advanced)
