import os

import requests


def send_discord_message(content, image=None):
    """
    Sends a message to a Discord channel via webhook with an optional file attachment.

    :param content: str - The message content to send.
    :param image: str - Optional path to the local image file to attach.
    """
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("Webhook URL not set in environment variables.")
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
            print(f"Message sent successfully: {content}")
            os.remove(image)
        else:
            print(f"Failed to send message: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_discord_message("<@1027111068704714833> test message")