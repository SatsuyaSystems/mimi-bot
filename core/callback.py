"""
Here are invidiual callbacks for each of my connectors.
The callbacks are used to handle the data to be returned to the connectors

"""
import discord
import logging
import os
from lib.global_registry import g_data
import io

# Use a logger specific to this module
logger = logging.getLogger(__name__)

async def mimi_callback(callback_object):
    """
    Callback function for Mimi connector.
    This function is called when the Mimi connector is triggered.
    It processes the data and sends the result in chunks if necessary.
    """
    logger.info("Mimi callback triggered.")
    messageId = callback_object['messageid']
    channelId = callback_object['channel']
    content = callback_object['responce']
    image_path = callback_object.get('image')  # Get the image path if it exists
    code = callback_object.get('code')  # Get the code if it exists

    # replace for codeblocks
    #content = content.replace(";;;", "```")  # Add a newline after code blocks

    # Get the bot instance and channel/message references
    bot = g_data.get("discord_bot")
    src_channel: discord.TextChannel = bot.get_channel(channelId)
    src_message: discord.Message = src_channel.get_partial_message(messageId)

    # Define the maximum chunk length
    max_length = 1900

    # Split the content into chunks
    if len(content) <= 2000:
        # If the content fits within a single message, send it directly
        await src_message.reply(content)
    else:
        # Split the content into chunks
        first_chunk = content[:max_length]
        if '\n' in first_chunk:
            first_chunk = first_chunk.rsplit('\n', 1)[0]  # Split at the last newline
        await src_message.reply(first_chunk)  # Send the first chunk

        # Process the remaining text
        remaining_text = content[len(first_chunk):].strip()
        while remaining_text:
            chunk_to_send = remaining_text[:max_length]
            if '\n' in chunk_to_send and len(remaining_text) > max_length:
                split_pos = chunk_to_send.rfind('\n')
                if split_pos > 0:
                    chunk_to_send = chunk_to_send[:split_pos]  # Split at the last newline

            if not chunk_to_send.strip():
                break  # Stop if there's no more text to send

            await src_message.reply(chunk_to_send)  # Send the chunk
            remaining_text = remaining_text[len(chunk_to_send):].strip()  # Update remaining text

    # Check if there is an image to upload
    if image_path:
        if os.path.exists(image_path):
            logger.info(f"Uploading image: {image_path} to channel {channelId}")
            try:
                await src_channel.send(file=discord.File(image_path))
                logger.info("Image uploaded successfully.")
                os.remove(image_path)  # Remove the image after sending
                logger.info(f"Image {image_path} removed after upload.")
            except Exception as e:
                logger.error(f"Failed to upload image: {e}")
        else:
            logger.warning(f"Image path does not exist: {image_path}")

    # Check if there is a code block to upload
    if code:
        logger.info("Uploading code block to channel.")
        try:
            await src_channel.send(file=discord.File(fp=io.BytesIO(code.encode('utf-8')), filename="message.txt"))
            logger.info("Code block uploaded successfully.")
        except Exception as e:
            logger.error(f"Failed to upload code block: {e}")

    logger.info("Mimi callback processing completed.")

async def search_callback(callback_object):
    """
    Callback function for search connector.
    This function is called when the search connector is triggered.
    It processes the data and returns the result.
    """
    if callback_object['host'] == "Discord":
        # Process data for Mimi connector
        data = await mimi_callback(callback_object)
    
    return data