import os
import sys
import discord
from discord.ext import commands
from playwright.async_api import async_playwright  # Changed from sync_playwright
import asyncio

# Global message queue
message_queue = asyncio.Queue()

# Discord bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
target_channel_id : int = 1371205265654943957  # Replace with your actual channel ID

# Global variables for Playwright
context = None
page = None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def process_message_from_queue():
    """Processes messages from the queue one by one."""
    global page  # Ensure 'page' is accessible if not passed explicitlyab
    while True:
        message, user_response = await message_queue.get()
        message : discord.Message
        user_response : discord.Message
        
        print(f"Processing queued message from {message.author.name}: {message.content}")
        try:
            if not page:
                await user_response.edit(content=f"{message.author.mention} Playwright page is not initialized. Cannot process request.")
                print("Error: Playwright page is not initialized in worker.")
                message_queue.task_done()
                continue

            chat_input_selector = '#app-root > main > side-navigation-v2 > bard-sidenav-container > bard-sidenav-content > div.content-wrapper > div > div.content-container > chat-window > div > input-container > div > input-area-v2 > div > div > div.text-input-field_textarea-wrapper.ng-tns-c3280767446-3 > div > div > rich-textarea > div.ql-editor.ql-blank.textarea.new-input-ui'
            send_button_selector = '#app-root > main > side-navigation-v2 > bard-sidenav-container > bard-sidenav-content > div.content-wrapper > div > div.content-container > chat-window > div > input-container > div > input-area-v2 > div > div > div.trailing-actions-wrapper.ng-tns-c3280767446-3 > div > div.mat-mdc-tooltip-trigger.send-button-container.ng-tns-c3280767446-3.inner.ng-star-inserted.visible > button'
            print(f"Attempting to locate chat input with selector: {chat_input_selector}")
            chat_button = page.locator(chat_input_selector)
            send_button = page.locator(send_button_selector)
            
            print("Chat input located. Clicking...")
            await chat_button.click()
            print(f"Filling with: Person:{message.author.name} ID:<@{message.author.id}> Message:{message.content}")
            await chat_button.fill(f"{message.author.name}: {message.content}")
            print("Pressing Enter...")
            await send_button.click()
            print("Waiting for response...")
            response_blocks_selector = '//message-content[contains(@class, "model-response-text")]'
            print(f"Locating response blocks with selector: {response_blocks_selector}")
            response_blocks = page.locator(response_blocks_selector)
            print("Waiting for response blocks to appear...")
            mic_button_selector = '#app-root > main > side-navigation-v2 > bard-sidenav-container > bard-sidenav-content > div.content-wrapper > div > div.content-container > chat-window > div > input-container > div > input-area-v2 > div > div > div.trailing-actions-wrapper.ng-tns-c3280767446-3 > div > div.mic-button-container.ng-tns-c3280767446-3.ng-trigger.ng-trigger-slide.ng-star-inserted > speech-dictation-mic-button > button'
            mic = page.locator(mic_button_selector)

            await asyncio.sleep(1)
            print("Checking if mic button is visible...")
            try:
                await mic.first.wait_for(state="visible", timeout=100000)
                print("Mic button is visible.")
            except Exception as e:
                print(f"Timeout or error waiting for response indicator (mic button): {e}")
                await user_response.edit(content=f"{message.author.mention} Timed out waiting for a response from Gemini.")
                message_queue.task_done()
                continue

            response_count = await response_blocks.count()
            print(f"Found {response_count} response blocks.")

            if response_count > 0:
                latest_response_block = response_blocks.nth(response_count - 1)
                latest_response_text = await latest_response_block.inner_text()
                print(f"Latest response text retrieved: {latest_response_text}")

                # Check for image elements in the response block
                image_elements = latest_response_block.locator("img")
                image_count = await image_elements.count()
                print(f"Found {image_count} image(s) in the response block.")

                image_urls = []
                for i in range(image_count):
                    image_url = await image_elements.nth(i).get_attribute("src")
                    if image_url:
                        image_urls.append(image_url+"=s512")
                        print(f"Image URL found: {image_url}")

                # Prepare the full response text
                max_length = 1900
                full_response_text = f"{latest_response_text}"
                print(f"Full response text length: {len(full_response_text)}")

                # Include image URLs in the response
                if image_urls:
                    full_response_text += "\n\nImages:\n" + "\n".join(image_urls)

                if len(full_response_text) <= 2000:
                    print("Response fits within Discord message limit. Sending full response.")
                    if user_response is not None:
                        await user_response.edit(content=full_response_text)
                    else:
                        await message.channel.send(full_response_text)
                else:
                    print("Response exceeds Discord message limit. Splitting into chunks.")
                    first_chunk = full_response_text[:max_length]
                    if '\n' in first_chunk:
                        first_chunk = first_chunk.rsplit('\n', 1)[0]
                        print(f"First chunk split at newline. Length: {len(first_chunk)}")
                    
                    if user_response is not None:
                        await user_response.edit(content=first_chunk)
                    else:
                        user_response = await message.channel.send(first_chunk)
                    
                    print("First chunk sent.")

                    remaining_text = full_response_text[len(first_chunk):].strip()
                    print(f"Remaining text length: {len(remaining_text)}")

                    while remaining_text:
                        chunk_to_send = remaining_text[:max_length]
                        if '\n' in chunk_to_send and len(remaining_text) > max_length:
                            split_pos = chunk_to_send.rfind('\n')
                            if split_pos > 0:
                                chunk_to_send = chunk_to_send[:split_pos]
                                print(f"Chunk split at newline. Length: {len(chunk_to_send)}")
                        
                        if not chunk_to_send.strip():
                            print("No more text to send. Breaking loop.")
                            break
                        print(f"Sending chunk of length: {len(chunk_to_send)}")
                        await user_response.reply(chunk_to_send)
                        remaining_text = remaining_text[len(chunk_to_send):].strip()
                        print(f"Remaining text length after sending chunk: {len(remaining_text)}")
            else:
                print("No response blocks found after interaction.")
                await user_response.edit(content=f"{message.author.mention} No response found.")

        except Exception as e:
            print(f"An error occurred processing queued message: {e}")
            try:
                await user_response.edit(content=f"{message.author.mention} An error occurred: {e}")
            except Exception as discord_e:
                print(f"Failed to send error to Discord: {discord_e}")
        finally:
            message_queue.task_done()

@bot.event
async def on_message_edit(before : discord.Message, message : discord.Message):
    if message.author == bot.user or not message.author.bot:
        return
    
    if message.author.id != 520307592212381699: #nami
        return
    
    if message.channel.id != 1370940507127283913:
        return

    if len(message.content) < 30:
        return

    if not page:
        await message.reply(content=f"{message.author.mention} Playwright page is not initialized. Cannot queue request.")
        print("Error: Playwright page is not initialized in on_message.")
        return
        
    await message_queue.put((message, None))



@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    
    if message.channel.id != target_channel_id:
        return

    print(f"Received message: {message.content} from {message.author.name}. Adding to queue.")
    # Send an initial response that will be edited later by the worker
    user_response = await message.reply(f"{message.author.mention} Your request has been queued and will be processed shortly...")

    if not page:  # Basic check before queueing
        await user_response.edit(content=f"{message.author.mention} Playwright page is not initialized. Cannot queue request.")
        print("Error: Playwright page is not initialized in on_message.")
        return
        
    await message_queue.put((message, user_response))

async def main():
    global page, context 
    async with async_playwright() as p:
        brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

        context = await p.chromium.launch_persistent_context(
            user_data_dir="user_data",
            headless=True,
            executable_path=brave_path,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await context.new_page() 

        print("Navigating to Gemini...")
        # Close all existing pages in the context before navigating
        for existing_page in context.pages:
            if len(context.pages) > 1:
                await existing_page.close()
        await page.goto("https://gemini.google.com/") 
        print("Navigation complete. Waiting for page to settle...")

        # Load memory and model
        locator = 'xpath=//*[@id="conversations-list-0"]/div[1]/div[1]'  # Tars

        try:
            await page.locator(locator).wait_for(state="visible", timeout=500000)  # Wait for the element to be visible
            print("Memory and model found. Start initializing...")
        except TimeoutError:
            print("Timeout waiting for element to be visible.")
        except Exception as e:
            print(f"Error waiting for element: {e}")
        await page.locator(locator).click()
        print("Memory and model loaded.")

        # Start the message processing worker task
        asyncio.create_task(process_message_from_queue())
        print("Message processing queue worker started.")

        print("Starting Discord bot...")
        await bot.start("MTM3MTExMDg4MjI5MzMyMTgxOA.GvGK62.CG1fmF0QOZY5-si1UTb0dDzNVET4nLOZoYkLHc")  # Replace with your bot token

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
