from core.automation import send_to_website, wait_for_response
from core.utils import get_german_time
from core.callback import search_callback
from lib.global_registry import g_data
import logging

message_queue = g_data.get("message_queue")
# Use a logger specific to this module
logger = logging.getLogger(__name__)


async def process_message_from_queue():
    """Processes messages from the queue using core automation"""
    while True:
        message = await message_queue.get()
        
        try:
            logger.info("Starting website interaction...") 
            # Format and send message to website via core
            formatted_content = f"[{message['host']}] From {message['username']} with id ({message['userid']}) in ({message['channel']}) at {get_german_time()}: {message['content']}"
            await send_to_website(formatted_content)
            
            # Wait for and process response
            response, image, code = await wait_for_response()
            logger.info("Response received from website.")
            
            callback_object = {
                "host": message['host'],
                "responce": response,
                "image": image,
                "code": code,
                "messageid": message['messageid'],
                "channel": message['channel'],
                "userid": message['userid'],
            }
            logger.info("Processing callback...")
            await search_callback(callback_object)

        except Exception as e:
            logger.info(f"Error processing message: {e}")
        finally:
            message_queue.task_done()
