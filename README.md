# Mimi-Bot: AI-Powered Browser Interface

Mimi-Bot is a Discord bot interface for interacting with Google's Gemini AI, designed for seamless real-time communication with chunked responses and asynchronous processing.

## Features

- **Multi-Platform Integration**: Discord interface with extensible adapter architecture
- **AI-Powered Processing**: Leverages Google's Gemini for intelligent responses
- **Image Generation**: Leverages Google's Gemini for image generation
- **Efficient Communication**:
  - Chunked message handling for Discord limits
  - Asynchronous I/O with asyncio
  - Rate limiting and error handling
- **Modular Architecture**: Core system with plugin-ready structure
- **Configuration Management**: YAML-based config system
- **Logging**: Comprehensive logging system in logs/ directory

## Requirements

- Python 3.8+
- Discord bot token
- Google account credentials
- Brave Browser (if on linux change path in core/automation.py)
- Packages: See `requirements.txt`

## Installation & Setup

```bash
git clone git@github.com:ZeroLikes/gemini_bot.git
cd gemini_bot

# Install dependencies
setup.bat or setup.sh on linux

# Configure your settings (see Configuration section below)
# Then launch the app
start.bat or start.sh on linux
```

## Project Structure

```
mimi-bot/
├── config/            # Configuration files
│   ├── __init__.py
│   ├── config.yml     # Main configuration
│   └── configurationFile.py
├── core/              # Core functionality
│   ├── __init__.py
│   ├── automation.py  # Task automation handlers
│   ├── callback.py    # Event callback system
│   ├── handlers.py    # Message processing logic
│   └── utils.py       # Utility functions
├── dc/                # Discord integration
│   ├── __init__.py
│   └── bot.py         # Discord client implementation
├── lib/               # Shared utilities
│   ├── __init__.py
│   └── global_registry.py  # Service registry
├── logs/              # Application logs
├── user_data/         # User-specific storage
├── validation/        # Security configurations
│   ├── communication.txt
│   └── uservalidation.txt
├── main.py            # Entry point
├── requirements.txt   # Dependencies
├── setup.bat          # Setup script
├── start.bat          # Launch script
└── update.bat          # Executes git pull -v
```

## Configuration

1. **Discord Setup**:
   - Create bot at https://discord.com/developers
   - Get your bot token and other ids
   - Edit config/config.yml:
```yaml
discord:
  bot_token: ""
  allowed_bots:
    - ""
    - ""
  target_channel:
    - "1370940507127283913"
    - "1371601242417135698"
    - "1371815158149812244"

```


3. **First Run**:
   - The bot will create necessary directories and files
   - Check logs/ for initialization messages

## Usage

### Basic Commands
```bash
# Start the bot normally
start.bat or start.sh on linux
```