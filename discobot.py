import os

import discord
import requests
from dotenv import load_dotenv

from logger import logger

load_dotenv()


def send_discord_message(content, image=None):
    """
    Sends a message to a Discord channel via webhook with an optional file attachment.

    :param content: str - The message content to send.
    :param image: str - Optional path to the local image file to attach.
    """
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        logger.error("Webhook URL not set in environment variables.")
        return

    data = {
        "content": content
    }

    try:
        if image and os.path.isfile(image):
            with open(image, 'rb') as f:
                response = requests.post(
                    webhook_url,
                    data={"content": content},
                    files={"file": f}
                )
        else:
            response = requests.post(webhook_url, json=data)

        if response.status_code in [200, 204]:
            logger.info("Discord message sent successfully")
            os.remove(image) if image else None
        else:
            logger.error(f"Failed to send message: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


async def read_channel(server_name, channel_name, token=os.environ.get("DISCORD_BOT_TOKEN"), limit=100):
    if not token:
        logger.error("Discord bot token not set in environment variables.")
        return
    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True  # Required to read message content
    client = discord.Client(intents=intents)

    result = []

    @client.event
    async def on_ready():
        logger.info(f"Logged in as {client.user}")

        # Get the guild and channel
        guild = discord.utils.get(client.guilds, name=server_name)
        channel = discord.utils.get(guild.text_channels, name=channel_name)

        logger.info(f"Fetching messages from channel: {channel.name}")

        async for message in channel.history(limit=limit):
            result.append((message.author, message.content))

        logger.info(f"Fetched {len(result)} messages.")
        await client.close()  # Stop the bot after fetching messages

    await client.start(token)
    if not client.is_closed():
        await client.close()
    return result
