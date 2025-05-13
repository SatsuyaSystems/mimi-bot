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

target_channel_id = [1370940507127283913, 1371601242417135698]

def isTargetChannelId(channel_id : int) -> bool:
    """Check if the channel ID is in the target list."""
    return channel_id in target_channel_id

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot and message.author.id != 590851927621894157:
        return
    
    if not isTargetChannelId(message.channel.id):
        return

    print(f"Received message: {message.content} from {message.author.name}. Adding to queue.")
    data = {
        "content": message.content,
        "username": message.author.name,
        "channel": message.channel.id,
        "userid": message.author.id,
        "messageid": message.id,
        "host": "Discord",
    }
    async with message.channel.typing():
        await message_queue.put((data))
