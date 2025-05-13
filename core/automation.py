from playwright.async_api import async_playwright
import asyncio
import logging
import os

# Global browser context and page
context = None
page = None

async def initialize_browser():
    """Initialize and maintain browser connection"""
    global context, page
    p = await async_playwright().start()
    brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

    if not context or context.is_closed():
        context = await p.chromium.launch_persistent_context(
            user_data_dir="user_data",
            headless=False,
            executable_path=brave_path,
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await context.new_page()

    # Browser initialization logic
    while True:
        try:
            for existing_page in context.pages:
                if len(context.pages) > 1:
                    await existing_page.close()
            await page.goto("https://gemini.google.com/")
            locator = 'xpath=//*[@id="conversations-list-0"]/div[1]/div[1]'
            await page.locator(locator).wait_for(state="visible", timeout=5000000)
            await page.locator(locator).click()
            break
        except Exception as e:
            logging.info(f"Browser initialization error: {e}")
            await asyncio.sleep(5)

async def send_to_website(content: str):
    """Core function to send content to website"""
    chat_input_selector = '//div[contains(@class, "textarea new-input-ui")]'
    chat_input = page.locator(chat_input_selector)
    await chat_input.fill(content)
    send_button_selector = '//button[contains(@class, "send-button")]'
    await page.locator(send_button_selector).click()

async def wait_for_response():
    """Wait for and return website response"""
    response_selector = '//message-content'
    mic_selector = 'xpath=//*[@id="app-root"]/main/side-navigation-v2/bard-sidenav-container/bard-sidenav-content/div[2]/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[3]/div/div[1]/speech-dictation-mic-button/button/div/mat-icon'

    try:
        await page.locator(mic_selector).wait_for(state="visible", timeout=500000)
    except Exception as e:
        logging.error(f"Timeout or error waiting for mic button: {e}")
        # Attempt to refresh or re-navigate if stuck
        try:
            logging.info("Attempting to refresh page due to mic button timeout...")
            await page.reload(wait_until="domcontentloaded")
            await page.locator(mic_selector).wait_for(state="visible", timeout=60000) # Shorter timeout after refresh
        except Exception as refresh_e:
            logging.error(f"Failed to find mic button even after refresh: {refresh_e}")
            return "Error: Could not find the response indicator.", None

    response_blocks = page.locator(response_selector)
    response_count = await response_blocks.count()
    logging.info(f"Found {response_count} response blocks.")
    image_path = None
    latest_response_text = None

    if response_count > 0:
        latest_response_block = response_blocks.nth(response_count - 1)
        latest_response_text = await latest_response_block.inner_text()
        
        # Check if the latest response contains an image and take a screenshot of it
        # Using a more specific selector for images within the response block
        image_element_locator = latest_response_block.locator('img').first # Get the first img if multiple
        
        try:
            if await image_element_locator.is_visible(timeout=5000): # Check if image is visible
                os.makedirs("temp", exist_ok=True)
                temp_image_path = os.path.join("temp", "latest_image_screenshot.png")
                await image_element_locator.screenshot(path=temp_image_path)
                image_path = temp_image_path
                logging.info(f"Screenshot of image element saved to {image_path}")
            else:
                logging.info("No visible image element found in the latest response block for screenshot.")
        except Exception as e:
            # This can happen if the locator doesn't find an image or times out
            logging.info(f"Could not find or screenshot image element: {e}")
            image_path = None # Ensure image_path is None if screenshot fails
            
    else:
        logging.warning("No response blocks found.")
        latest_response_text = "No response content found."

    return latest_response_text, image_path