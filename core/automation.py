from playwright.async_api import async_playwright
import asyncio

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
            await page.locator(locator).wait_for(state="visible", timeout=500000)
            await page.locator(locator).click()
            break
        except Exception as e:
            print(f"Browser initialization error: {e}")
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
    await page.locator(mic_selector).wait_for(state="visible", timeout=500000)
    response_blocks = page.locator(response_selector)
    response_count = await response_blocks.count()
    print(f"Found {response_count} response blocks.")
    if response_count > 0:
        latest_response_block = response_blocks.nth(response_count - 1)
        latest_response_text = await latest_response_block.inner_text()
        print(f"Latest response text retrieved: {latest_response_text}")
        return latest_response_text