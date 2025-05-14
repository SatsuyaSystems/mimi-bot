import logging
import discord
from discord.ext import commands
from core.handlers import message_queue
from lib.global_registry import g_data
# Global message queue
import asyncio
message_queue = g_data.get("message_queue")

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = g_data.get_or_create(
    "discord_bot", 
    commands.Bot,
    command_prefix="!",
    intents=intents,
)

target_channel = [int(bot_id) for bot_id in g_data.get("cfg").data['discord']['target_channel']]
allowed_bots = [int(bot_id) for bot_id in g_data.get("cfg").data['discord']['allowed_bots']]

def isTargetChannelId(id) -> bool:
    """Check if the channel ID is in the target list."""
    if id in target_channel:
        return True
    else:
        return False

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    """Handle incoming messages."""
    # check if bot is mentioned
    if bot.user not in message.mentions:
        if not isTargetChannelId(message.channel.id):
            return

    if message.author.bot and message.author.id not in allowed_bots:
        return


    logging.info(f"Discord message from {message.author.name}. Adding to queue.")
    data = {
        "content": message.content,
        "username": message.author.name,
        "channel": message.channel.id,
        "userid": message.author.id,
        "messageid": message.id,
        "host": "Discord",
    }
    async with message.channel.typing():
        # Check if the message is already in the queue
        queue_items = list(message_queue._queue)
        if any(item["messageid"] == message.id for item in queue_items):
            logging.info("Discord message is already in the queue. Skipping.")
            return
        await message_queue.put((data))
