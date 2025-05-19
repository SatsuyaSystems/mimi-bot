# discord_rpc.py
import asyncio
import logging
import time
from pypresence import AioPresence

# !!! REPLACE THIS WITH YOUR ACTUAL CLIENT ID !!!
# You get this from the Discord Developer Portal -> Your Application -> General Information -> Application ID
CLIENT_ID = "1371110882293321818" 

# RPC Update Interval (in seconds) - Discord expects updates every ~15 seconds
RPC_UPDATE_INTERVAL = 15

# logging configuration should ideally be done in the main app,
# but you can add a basic one here as fallback or for testing this file directly
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def start_rpc():
    """
    Connects to Discord RPC and updates presence with buttons.
    Runs indefinitely until cancelled.
    """
    # Use a logger specific to this module
    logger = logging.getLogger(__name__)
    logger.info("Starting Discord RPC task...")

    rpc = AioPresence(CLIENT_ID)

    try:
        await rpc.connect()
        logger.info("Connected to Discord RPC!")

        # --- Set your Rich Presence details here ---
        await rpc.update(
            state="Running Mimi-Bot",  # Smaller text under details
            details="AI Discord Assistant", # Larger text
            start=int(time.time()),              # Optional: Unix timestamp for start time
             large_image="bot", # Optional: Name of the image uploaded in Developer Portal
            # large_text="Tooltip for large image",# Optional: Tooltip text for large image
            # small_image="your_small_image_name", # Optional: Name of the image uploaded in Developer Portal
            # small_text="Tooltip for small image",# Optional: Tooltip text for small image
            buttons=[
                {"label": "Discord", "url": "https://discord.gg/MVjcXuS6pP"}, # Button 1
                {"label": "GitHub", "url": "https://github.com/SatsuyaSystems/mimi-bot"} # Button 2
            ]
        )

        logger.info("RPC presence updated. Running...")

        # Keep the connection alive and update periodically
        while True:
            # This loop keeps the async task alive.
            # asyncio.sleep allows the event loop to run other tasks.
            # You could add logic here to update the RPC state dynamically.
            await asyncio.sleep(RPC_UPDATE_INTERVAL)

    except asyncio.CancelledError:
        # This exception is raised when the task is cancelled (e.g., during shutdown)
        logger.info("RPC task was cancelled.")
    except Exception as e:
        logger.error(f"An error occurred with Discord RPC: {e}")
        logger.error("Please ensure Discord is running and you are logged in.")

    finally:
        # This block runs when the async function finishes (normally or due to cancellation/error)
        logger.info("RPC task stopping. Closing connection.")
        try:
            # Attempt to close the RPC connection gracefully
            await rpc.close()
            logger.info("RPC connection closed.")
        except Exception:
            # Ignore errors during closing if it was never connected properly
            pass

# Note: No if __name__ == "__main__": block here.
# This file is designed to be imported.