from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Slack client with bot token from environment variable
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def post_to_slack(channel, message):
    """
    Post a message to a Slack channel.
    
    Args:
        channel (str): The Slack channel ID or name to post to.
        message (str): The message to post.
    
    Returns:
        dict: The response from the Slack API.
    
    Raises:
        SlackApiError: If there's an error posting the message to Slack.
    """
    try:
        response = slack_client.chat_postMessage(channel=channel, text=message)
        return response
    except SlackApiError as e:
        logger.error(f"Error posting message to Slack: {e}")
        raise