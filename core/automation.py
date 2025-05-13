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
    chat_input_selector = '#app-root > main > side-navigation-v2 > bard-sidenav-container > bard-sidenav-content > div.content-wrapper > div > div.content-container > chat-window > div > input-container > div > input-area-v2 > div > div > div.text-input-field_textarea-wrapper.ng-tns-c1933791834-3 > div > div > rich-textarea'
                
    await page.type(selector=chat_input_selector ,delay=0, text=content)
    await page.press(selector=chat_input_selector, delay=0, key="Enter")

async def wait_for_response():
    """Wait for and return website response"""
    response_selector = '//message-content[contains(@class, "model-response-text")]'
    mic_selector = '#app-root > main > side-navigation-v2 > bard-sidenav-container > bard-sidenav-content > div.content-wrapper > div > div.content-container > chat-window > div > input-container > div > input-area-v2 > div > div > div.trailing-actions-wrapper.ng-tns-c1933791834-3 > div > div.mic-button-container.ng-tns-c1933791834-3.ng-trigger.ng-trigger-slide.ng-star-inserted > speech-dictation-mic-button > button > div > mat-icon'
    
    await page.locator(mic_selector).wait_for(state="visible", timeout=500000)
    response_blocks = page.locator(response_selector)
    response_count = await response_blocks.count()
    print(f"Found {response_count} response blocks.")
    if response_count > 0:
        latest_response_block = response_blocks.nth(response_count - 1)
        latest_response_text = await latest_response_block.inner_text()
        print(f"Latest response text retrieved: {latest_response_text}")
        return latest_response_text