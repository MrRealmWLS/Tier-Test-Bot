# Tier Test Bot

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-5865F2?style=flat&logo=discord)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

A powerful and fully configurable Discord bot for managing tier test results, player rankings, and automated role assignments across multiple competitive gamemodes.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Commands](#commands)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)
- [License](#license)

## ✨ Features

- 🎯 **Fully Configurable** - All settings (emojis, gamemodes, tiers) centralized in `config.json`
- 🎮 **Multiple Gamemodes** - Support for various PvP gamemodes (customizable)
- 🏆 **Tier Management** - Track player tiers and organize dynamic leaderboards
- 🎭 **Auto Role Assignment** - Automatically assigns tier-based Discord roles to players
- 💾 **SQLite Database** - Lightweight, persistent data storage for all tier records
- ⚙️ **Hot Reload Config** - Update settings without restarting via `/reloadconfig`
- 📊 **Clean Embeds** - Beautiful, organized embed displays with custom emojis
- 🔐 **Admin Only** - Protected commands with permission checks

## 📦 Requirements

- Python 3.8+
- discord.py 2.0+
- aiosqlite

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/tier-test-bot.git
cd tier-test-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install discord.py aiosqlite
```

### 3. Configure the Bot

Create and edit `config.json`:

```json
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "database": "tiers.db",
  "bot_status": "Aurora Tier Test",
  "emojis": {
    "test_passed": "<:TestPassed:1408141272644063252>",
    "leaderboard": "<:Leaderboard:1408141275601043548>",
    "tier_entry": "<:FullStop1:1408141269946994869>"
  },
  "gamemodes": [
    {"name": "Bedfight", "value": "bedfight"},
    {"name": "Sumo", "value": "sumo"},
    {"name": "Boxing", "value": "boxing"}
  ],
  "tiers": ["S+", "S", "A+", "A", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "D-", "F+", "F", "F-"],
  "colors": {
    "embed": "0xFF1B00"
  }
}
```

**Required Fields:**
| Field | Description |
|-------|-------------|
| `token` | Your Discord bot token |
| `database` | SQLite database filename |
| `bot_status` | Status message shown in Discord |
| `emojis` | Custom emojis for embeds |
| `gamemodes` | Available gamemodes with name/value pairs |
| `tiers` | Tier ranking order |
| `colors` | Embed colors in hex format |

### 4. Create Discord Roles

Create roles in your Discord server with the naming format:
```
{Gamemode} {Tier}
```

**Examples:**
- `Bedfight S+`
- `Boxing A`
- `Sumo B-`

> The bot will automatically assign these roles when players complete tier tests.

### 5. Run the Bot

```bash
python bot.py
```

## ⚙️ Configuration Guide

### Custom Emojis

Update emoji IDs in `config.json`. To get emoji IDs:
1. Enable Developer Mode in Discord
2. Right-click an emoji
3. Select "Copy Text"

```json
"emojis": {
  "test_passed": "<:YourEmoji:123456789>",
  "leaderboard": "<:YourEmoji:123456789>",
  "tier_entry": "<:YourEmoji:123456789>"
}
```

### Custom Gamemodes

Add or remove gamemodes dynamically:

```json
"gamemodes": [
  {"name": "Bedfight", "value": "bedfight"},
  {"name": "Your Gamemode", "value": "your_gamemode"}
]
```

### Custom Tiers

Modify tier order (respects order in config):

```json
"tiers": ["S+", "S", "A+", "A", "B+", "B", "B-", ...]
```

### Embed Colors

Use hex color codes:

```json
"colors": {
  "embed": "0xFF1B00"
}
```

## 📝 Commands

### `/tiertest` (Admin Only)

Submit a tier test result to the database.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `ign` | String | Player's in-game name |
| `gamemode` | Choice | Selected gamemode |
| `score` | String | Final score (e.g., "3-0") |
| `tier` | Choice | Tier achieved |
| `comments` | String | Optional tester comments |

**Example:**
```
/tiertest ign:PlayerName gamemode:Bedfight score:3-0 tier:S+ comments:Excellent performance
```

### `/tierlist`

Display the tier leaderboard for a gamemode and assign roles.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `gamemode` | Choice | Gamemode to view leaderboard for |

**Output:**
- Organized leaderboard by tier
- Automatic role assignment to players
- Beautiful embed display

### `/reloadconfig` (Admin Only)

Reload configuration without restarting the bot.

**Usage:**
```
/reloadconfig
```

> Perfect for updating emojis, gamemodes, or tiers on the fly.

## 🔄 Updating Emojis (No Restart)

1. Edit `config.json` with new emoji IDs
2. Run `/reloadconfig` in Discord
3. Changes apply instantly

No bot restart needed!

## 💾 Database

The bot uses SQLite with a `tiertests` table. 

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key (auto-increment) |
| `ign` | TEXT | In-game name |
| `user_id` | INTEGER | Discord user ID |
| `gamemode` | TEXT | Gamemode tested |
| `score` | TEXT | Final score |
| `tier` | TEXT | Tier achieved |
| `comments` | TEXT | Tester comments |
| `tester_id` | INTEGER | Admin ID who submitted test |

Database file location is configurable in `config.json`.

## 🆘 Troubleshooting

### Bot Won't Start
- ✅ Verify `config.json` exists and is valid JSON
- ✅ Check bot token is correct
- ✅ Ensure all required fields are present

**Error: `Missing required config key`**
- Add missing keys to `config.json`

### Roles Not Assigned
- ✅ Verify roles exist in Discord with exact format: `{Gamemode} {Tier}`
- ✅ Bot must have "Manage Roles" permission
- ✅ Bot's highest role must be above the tier roles

**Error: `Forbidden: 403`**
- Check bot permissions in Discord server settings

### Emojis Not Showing
- ✅ Verify emoji IDs are correct
- ✅ Emojis must be in a server the bot can see
- ✅ Use `/reloadconfig` after updating

**Error: `Invalid emoji`**
- Check emoji ID syntax: `<:name:id>`

### Leaderboard Empty
- Verify records exist for that gamemode
- Check database with SQLite browser

## 📁 File Structure

```
tier-test-bot/
├── bot.py                 # Main bot file
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
└── tiers.db              # SQLite database (auto-created)
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs via [Issues](https://github.com/yourusername/tier-test-bot/issues)
- Submit improvements via [Pull Requests](https://github.com/yourusername/tier-test-bot/pulls)
- Suggest features in Discussions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [aiosqlite](https://github.com/omnilib/aiosqlite) - Async SQLite

## 📧 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/yourusername/tier-test-bot/issues)
- Check [Troubleshooting](#troubleshooting) section
- Review [Configuration Guide](#-configuration-guide)

---

**Made with ❤️ for competitive gaming communities**