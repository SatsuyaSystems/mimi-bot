from lib.global_registry import g_data
from config.configurationFile import ConfigurationFile
import logging, os, time
from colorama import Fore, init
from dc.rpc import start_rpc

# --- Moved Logging Configuration ---
os.makedirs('./logs', exist_ok=True) # Use makedirs and exist_ok=True

# Get log level string from config first
cfg_temp = ConfigurationFile("config\config.yml") # Load config temporarily just for log level
log_level_str = cfg_temp.data.get('bot', {}).get('log_level', 'INFO')
log_level = getattr(logging, str(log_level_str).upper(), logging.INFO) # Convert string to logging level

logging.basicConfig(
    level=log_level,  # Set level directly from converted config value
    format=(
        f'{Fore.MAGENTA}[%(asctime)s] '
        f'{Fore.YELLOW}{"[%(levelname)s]":<8} '
        f'{Fore.RED}[%(name)s] '
        f'{Fore.RESET}'
        f'%(message)s'
    ),
    handlers=[
        logging.FileHandler(f"./logs/{time.strftime('%Y-%m-%d_%H_%M_%S')}.log", 'w', 'utf-8'),
        logging.StreamHandler()
    ],
    force=True
)
logging.info(f"Logging configured with level {logging.getLevelName(log_level)}.") # Log confirmation
# --- End Logging Configuration ---

# Global message queue
import asyncio
message_queue = g_data.get_or_create(
    "message_queue",
    asyncio.Queue
)
cfg : ConfigurationFile = g_data.get_or_create("cfg", ConfigurationFile, "config\config.yml")

from dc.bot import bot
from core.automation import initialize_browser
from core.handlers import process_message_from_queue

async def main():
    # Discord rich presence
    asyncio.create_task(start_rpc())
    # Initialize Playwright browser
    await initialize_browser()
    logging.info("Browser initialized.")
     # Start the message processing queue worker
    asyncio.create_task(process_message_from_queue())
    logging.info("Message processing queue worker started.")
    # Start the Discord bot
    await bot.start(g_data.get("cfg").data['discord']['bot_token'])
    logging.info("Discord bot started.")

# Run both the browser and the bot concurrently
try:
    asyncio.run(main())
except Exception as e:
    logging.info(f"An error occurred: {e}. Restarting the script...")
    exit(1)
except KeyboardInterrupt:
    logging.info("Shutting down...")
finally:
    pass
