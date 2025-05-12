# Mimi-Bot: AI-Powered Browser Interface

Mimi-Bot is a Discord bot interface for interacting with Google's Gemini AI, designed for seamless real-time communication with chunked responses and asynchronous processing.

## Features

- **Multi-Platform Integration**: Discord interface with extensible adapter architecture
- **AI-Powered Processing**: Leverages Google's Gemini for intelligent responses
- **Efficient Communication**:
  - Chunked message handling for Discord limits
  - Asynchronous I/O with asyncio
  - Rate limiting and error handling
- **Modular Architecture**: Core system with plugin-ready structure

## Requirements

- Python 3.8+
- Discord bot token
- Google account credentials
- Packages: `requirements.txt`

## Installation & Setup

```bash
git clone git@github.com:ZeroLikes/gemini_bot.git
cd gemini_bot

# Install dependencies
setup.bat

# Launch App
start.bat
```

## Project Structure

```
mimi-bot/
├── core/              # Core functionality
│   ├── automation.py  # Task automation handlers
│   ├── callback.py    # Event callback system
│   └── handlers.py    # Message processing logic
├── dc/                # Discord integration
│   └── bot.py         # Discord client implementation
├── lib/               # Shared utilities
│   └── global_registry.py  # Service registry
├── user_data/         # User-specific storage
├── validation/        # Security configurations
│   ├── communication.txt
│   └── uservalidation.txt
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── *.bat              # Windows management scripts
```

## Configuration

1. **Discord Setup**:
   - Create bot at https://discord.com/developers
   - Add token to main.py:

2. **Gemini Setup**:
   - Hold your credentials ready
   - start the application and login. Then restart.


## Usage

```bash
# Start normally
start.bat
```