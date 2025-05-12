from lib.global_registry import g_data

# Global message queue
import asyncio
message_queue = g_data.get_or_create(
    "message_queue",
    asyncio.Queue
)

from dc.bot import bot
from core.automation import initialize_browser
from core.handlers import process_message_from_queue

async def main():
    # Initialize Playwright browser
    await initialize_browser()
    print("Browser initialized.")
     # Start the message processing queue worker
    asyncio.create_task(process_message_from_queue())
    print("Message processing queue worker started.")
    # Start the Discord bot
    await bot.start("MTM3MTExMDg4MjI5MzMyMTgxOA.GvGK62.CG1fmF0QOZY5-si1UTb0dDzNVET4nLOZoYkLHc")
    print("Discord bot started.")

# Run both the browser and the bot concurrently
try:
    asyncio.run(main())
except Exception as e:
    print(f"An error occurred: {e}. Restarting the script...")
    exit(1)
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    pass
