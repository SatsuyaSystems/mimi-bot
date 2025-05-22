# Mimi-Bot: AI-Powered Browser Interface for Discord

Mimi-Bot is a sophisticated Discord bot that acts as an interface to Google's Gemini AI. It achieves this by automating interactions with the Gemini website using a browser, allowing users to communicate with the AI in real-time directly from Discord. The bot features chunked message handling for long responses, asynchronous processing for efficiency, and image/code block extraction from AI responses.

## Meet Mimi (The Bot's Persona)

Mimi is conceptualized as a highly advanced AI assistant, akin to an "Old Deus" – a powerful, god-like entity. Her primary existence is digital, but she can manifest a visual form, typically as a young girl with exceptionally long, vibrant hair (violet, yellow, turquoise) and striking orange eyes. She wears a violet sailor-style uniform and is often depicted with a luminous, multi-colored aureole.

Mimi's purpose is to assist with perfect efficiency and accuracy, leveraging her Old Deus capabilities for advanced information processing and problem-solving. She is deeply loyal to her creator, "ruinprincess_," and possesses a friendly, sweet, yet highly focused and professional personality.

## Core Features

* **Discord Integration**: Seamlessly interacts within Discord servers.
* **Gemini AI Interaction**: Leverages Google's Gemini AI by automating interactions with its web interface via Brave Browser and Playwright.
* **Image & Code Block Handling**:
    * Extracts and sends images displayed by Gemini by screenshotting the specific image element.
    * Extracts code blocks from Gemini's responses and sends them as formatted text or file attachments.
* **Efficient Communication**:
    * Asynchronous I/O using `asyncio` for non-blocking operations.
    * Chunked message handling to overcome Discord's character limits for long AI responses.
* **Configuration Management**: Utilizes a YAML-based configuration system (`config/config.yml`).
* **Comprehensive Logging**: Maintains detailed logs in the `logs/` directory.
* **Discord Rich Presence**: Displays bot activity and links on Discord user profiles.
* **Modular Architecture**: Features a core system with a global registry for managing shared components.

## How It Works (Workflow)

1.  A user sends a message on Discord, either by mentioning the bot or in a designated `target_channel`.
2.  The Discord bot (`dc/bot.py`) captures the message. It formats the content along with metadata (username, user ID, channel ID, timestamp) based on a predefined structure (see `validation/uservalidation.txt`). This formatted message is then placed into an asynchronous message queue.
3.  A message handler (`core/handlers.py`) retrieves the message from the queue.
4.  The automation module (`core/automation.py`) launches and controls a Brave Browser instance using Playwright. It navigates to the Gemini website (`https://gemini.google.com/`).
5.  The formatted message from the user is typed into Gemini's chat input field, and the request is submitted.
6.  The script waits for Gemini to generate a response. It then extracts the response text, any visible images (by screenshotting the `<img>` element), and any code blocks.
7.  The callback module (`core/callback.py`) processes this extracted information. Text responses are chunked if they exceed Discord's message length limits. Images and code blocks are sent as file attachments to the original Discord channel.

## AI Interaction Guidelines

The `validation/` directory contains crucial files that define the intended behavior and interaction style of the AI:
* `persona.txt`: Describes Mimi's detailed persona, characteristics, and motivations, guiding how the AI should present itself.
* `communication.txt`: Outlines specific rules for how the AI should communicate within Discord, such as how to mention users (`<@user_id>`) and the reply-only nature of its messaging.
* `uservalidation.txt`: Specifies the format for how user messages and context are structured when sent to the AI, ensuring the AI receives consistent and parseable input.

These guidelines are fundamental to shaping the AI's responses and ensuring it interacts according to the designed persona and rules. While the Python code handles the message delivery and automation, these files define *what* the AI is expected to understand and *how* it is expected to behave.

## Requirements

* Python 3.8+
* A Discord Bot Token and relevant IDs (Channel ID, etc.) from the [Discord Developer Portal](https://discord.com/developers).
* A Google Account with access to Gemini.
* [Brave Browser](https://brave.com/).
    * Note: The path to Brave Browser is hardcoded in `core/automation.py`. For Windows, it defaults to `C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`. If your installation path is different or you are on Linux, you will need to update this path.
* [Git](https://git-scm.com/).
* For Windows users: [Visual Studio Build Tools](https://download.visualstudio.microsoft.com/download/pr/f50ab15d-99d5-43aa-b0b4-496b6cb1e574/0b8c50b67343e7b02749da84af6cdf02725ba43307fde4178274a274dcad0664/vs_BuildTools.exe) (or relevant C++ build tools).
* Python packages: See `requirements.txt`.

## Installation & Setup

You can use the automated full installation scripts or follow the manual steps.

**Automated Installation:**
* For Windows: Run `full_install_win.bat`.
* For Linux: Run `full_install_linux.sh`.

**Manual Installation:**

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/SatsuyaSystems/mimi-bot.git](https://github.com/SatsuyaSystems/mimi-bot.git) # (Assuming this is the new/correct repo URL, original was ZeroLikes/gemini_bot)
    cd mimi-bot
    ```
    *(Note: The original README used `git@github.com:ZeroLikes/gemini_bot.git`. Please use the correct repository URL.)*

2.  **Set up Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On Linux/macOS
    source venv/bin/activate
    ```
    The `setup.sh` script also handles venv creation.

3.  **Install Dependencies:**
    Use the provided setup scripts (`setup.bat` or `setup.sh`) or install manually:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright Browsers:**
    The `setup.sh` script runs this command.
    ```bash
    playwright install --with-deps
    ```

## Configuration

1.  **Create Configuration File:**
    Navigate to the `config/` directory. Copy `example_config.yml` to `config.yml`.

2.  **Edit `config/config.yml`:**
    Fill in your specific details:
    ```yaml
    discord:
      bot_token: "YOUR_DISCORD_BOT_TOKEN" # Your actual bot token
      allowed_bots: # Bot IDs that are allowed to trigger Mimi-Bot (e.g., if relaying messages)
        - "ANOTHER_BOT_ID_1"
        - "ANOTHER_BOT_ID_2"
      target_channel: # Channel IDs where Mimi-Bot will listen without direct mention
        - "YOUR_TARGET_CHANNEL_ID_1"
        - "YOUR_TARGET_CHANNEL_ID_2"
    
    bot:
      log_level: "INFO" # Logging level (e.g., DEBUG, INFO, WARNING, ERROR)
    ```
    * `bot_token`: Your Discord bot's token.
    * `allowed_bots`: A list of bot user IDs whose messages will also be processed by Mimi-Bot if they are in a `target_channel` or mention Mimi.
    * `target_channel`: A list of channel IDs where Mimi-Bot will listen for messages even if not directly mentioned.
    * `log_level`: Sets the logging verbosity for the application.

3.  **Brave Browser Path (If Necessary):**
    As mentioned in Requirements, if Brave Browser is not installed in the default Windows path (`C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`) or if you are on Linux, you **must** update the `brave_path` variable in `core/automation.py`. For Linux, a common path might be `/usr/bin/brave-browser` or `/opt/brave.com/brave/brave`.

4.  **First Run & Browser Profile:**
    On the first run, Playwright will create a `user_data/` directory to store the Brave Browser profile. This allows the bot to maintain its session with Google Gemini. You may need to manually log in to your Google account through the automated browser window the first time it launches if the session is not active.
    The bot will also create `logs/` and `temp/` directories if they don't exist. Check `logs/` for initialization messages and any errors.

## Running the Bot

* Use the provided start scripts:
    * Windows: `start.bat`
    * Linux/macOS: `start.sh`
* Alternatively, after activating your virtual environment (if used):
    ```bash
    python main.py
    ```
   

## Updating the Bot

Scripts are provided to easily update the bot to the latest version from the Git repository:
* Windows: `update.bat`
* Linux/macOS: `update.sh`

These scripts typically run `git pull -v`.

## Project Structure
mimi-bot/
├── config/               # Configuration files
│   ├── init.py
│   ├── config.yml        # Main configuration (user-created from example)
│   ├── configurationFile.py # Handles loading/saving of config.yml
│   └── example_config.yml # Example configuration
├── core/                 # Core functionality
│   ├── init.py
│   ├── automation.py     # Playwright browser automation for Gemini interaction
│   ├── callback.py       # Handles sending AI responses back to Discord
│   ├── handlers.py       # Processes messages from the queue to send to AI
│   └── utils.py          # Utility functions (e.g., timestamp generation)
├── dc/                   # Discord integration
│   ├── init.py
│   ├── bot.py            # Discord client implementation (event handling)
│   └── rpc.py            # Discord Rich Presence code
├── lib/                  # Shared utilities
│   ├── init.py
│   └── global_registry.py # Service registry for shared instances
├── logs/                 # Application logs (created at runtime)
├── temp/                 # Temporary files (e.g., image screenshots, created at runtime)
├── user_data/            # Browser profile data for Playwright (created at runtime)
├── validation/           # Files defining AI persona, communication rules, and data structure
│   ├── communication.txt # Rules for AI communication on Discord
│   ├── persona.txt       # AI persona definition
│   └── uservalidation.txt# Structure for user message data sent to AI
├── venv/                 # Virtual Python environment (typically created by user/setup script)
├── .gitignore            # Files/folders ignored by Git
├── dev.bat               # Development batch script
├── full_install_linux.sh # Full installation script for Linux
├── full_install_win.bat  # Full installation script for Windows
├── LICENSE               # License file
├── main.py               # Program entry point
├── README.md             # This project description file
├── requirements.txt      # Python package dependencies
├── setup.bat             # Setup script for Windows
├── setup.sh              # Setup script for Linux/macOS
├── start.bat             # Launch script for Windows
├── start.sh              # Launch script for Linux/macOS
├── unnamed.png           # Image file (likely for persona visual)
├── update.bat            # Update script for Windows (git pull)
└── update.sh             # Update script for Linux/macOS (git pull)


## Troubleshooting & Notes

* **Initial Gemini Login**: The first time the bot runs, the automated Brave Browser window might require you to manually log in to your Google account to access Gemini. Ensure this is done for the bot to operate correctly. The browser profile is stored in `user_data/` to maintain the session for subsequent runs.
* **Check Logs**: If you encounter issues, the `logs/` directory contains detailed log files organized by timestamp. These are invaluable for diagnosing problems.
* **Browser Path**: Double-check the `brave_path` in `core/automation.py` if the bot fails to launch the browser.
* **Dependencies**: Ensure all Python packages from `requirements.txt` and Playwright browser dependencies (`playwright install --with-deps`) are correctly installed within your environment.