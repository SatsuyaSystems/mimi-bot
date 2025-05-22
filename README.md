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
- VisualStudio Buildtools
- Packages: See `requirements.txt`

- https://www.python.org/
- https://brave.com/de/
- https://git-scm.com/
- https://download.visualstudio.microsoft.com/download/pr/f50ab15d-99d5-43aa-b0b4-496b6cb1e574/0b8c50b67343e7b02749da84af6cdf02725ba43307fde4178274a274dcad0664/vs_BuildTools.exe


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
├── config/               # Configuration files
│   ├── __init__.py
│   ├── config.yml        # Main configuration
│   ├── configurationFile.py
│   └── example_config.yml # Example configuration
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── automation.py     # Task automation handlers
│   ├── callback.py       # Event callback system
│   ├── handlers.py       # Message processing logic
│   └── utils.py          # Utility functions
├── dc/                   # Discord integration
│   ├── __init__.py
│   ├── bot.py            # Discord client implementation
│   └── rpc.py            # Rich Presence code
├── lib/                  # Shared utilities
│   ├── __init__.py
│   └── global_registry.py # Service registry
├── logs/                 # Application logs
├── temp/                 # Temporary files
├── user_data/            # User-specific storage
├── validation/           # Security configurations / Validation files
│   ├── communication.txt
│   ├── persona.txt       # Persona configuration
│   └── uservalidation.txt
├── venv/                 # Virtual Python environment (typical)
├── .gitignore            # Files/folders ignored by Git
├── dev.bat               # Development batch script
├── full_install_linux.sh # Full installation script for Linux
├── full_install_win.bat  # Full installation script for Windows
├── LICENSE               # License file
├── main.py               # Program entry point
├── README.md             # Project description
├── requirements.txt      # Dependencies
├── setup.bat             # Setup script
├── setup.sh              # Setup script for Linux/macOS
├── start.bat             # Launch script
├── start.sh              # Launch script for Linux/macOS
├── unnamed.png           # Image file in main directory
├── update.bat            # Executes 'git pull -v'
└── update.sh             # Update script for Linux/macOS
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