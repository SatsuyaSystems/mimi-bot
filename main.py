from lib.global_registry import g_data
from config.configurationFile import ConfigurationFile
import logging, os, time
from colorama import Fore, init
from dc.rpc import start_rpc
import asyncio

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
message_queue = g_data.get_or_create(
    "message_queue",
    asyncio.Queue
)
cfg : ConfigurationFile = g_data.get_or_create("cfg", ConfigurationFile, "config\config.yml")

from dc.bot import bot
from core.automation import initialize_browser
from core.handlers import process_message_from_queue

async def main():
    rpc_task = None
    message_processor_task = None
    # Add other tasks here if you have more (e.g., browser monitoring)

    try:
        # Discord rich presence
        rpc_task = asyncio.create_task(start_rpc())
        
        # Initialize Playwright browser
        await initialize_browser()
        logging.info("Browser initialized.")
        
        # Start the message processing queue worker
        message_processor_task = asyncio.create_task(process_message_from_queue())
        logging.info("Message processing queue worker started.")
        
        # Start the Discord bot - this is a blocking call
        logging.info("Starting Discord bot...")
        await bot.start(g_data.get("cfg").data['discord']['bot_token'])
        # This line is reached when the bot stops (e.g., disconnects or is stopped)
        logging.info("Discord bot has stopped.")

    except Exception as e:
        logging.error(f"An error occurred in main execution: {e}", exc_info=True)
    finally:
        logging.info("Main function is finishing. Cleaning up background tasks...")

        if message_processor_task and not message_processor_task.done():
            logging.info("Cancelling message processor task...")
            message_processor_task.cancel()
            try:
                await message_processor_task
            except asyncio.CancelledError:
                logging.info("Message processor task successfully cancelled.")
            except Exception as e:
                logging.error(f"Error during message processor task cleanup: {e}", exc_info=True)

        if rpc_task and not rpc_task.done():
            logging.info("Cancelling RPC task...")
            rpc_task.cancel()
            try:
                await rpc_task  # Wait for the RPC task to finish its cleanup
            except asyncio.CancelledError:
                # This is expected when cancelling a task that handles cancellation.
                logging.info("RPC task successfully cancelled.")
            except Exception as e:
                logging.error(f"Error during RPC task cleanup: {e}", exc_info=True)
        
        # Add cleanup for other tasks or resources here if needed
        # For example, if initialize_browser() returns a playwright instance `p` that needs p.stop()
        # or if global browser/context objects need closing.

        logging.info("Main function cleanup complete.")

if __name__ == "__main__":
    # Configure logging (ensure it's set up before any logging calls)
    # Example: logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Application shut down by KeyboardInterrupt.")
    except Exception as e:
        # This catches exceptions that might occur during asyncio.run() itself,
        # though most should be caught within main().
        logging.critical(f"Unhandled exception at top level: {e}", exc_info=True)
    finally:
        logging.info("Application has exited.")
