from discobot import send_discord_message, read_channel
from dateparser import parse
from datetime import datetime
import asyncio
import os, json
from logger import logger
from api import CheckInAPI


async def main(result):
    required_env_vars = ["DISCORD_BOT_TOKEN", "USERNAMES", "PASSWORDS", "DISCORD_USER_IDS"]
    for var in required_env_vars:
        if not os.environ.get(var):
            logger.error(f"Missing required environment variable: {var}")
            return 1

    usernames = os.environ.get("USERNAMES", "").split(',')
    passwords = os.environ.get("PASSWORDS", "").split(',')
    leave_user_ids = os.environ.get("LEAVE_USERS", "").split(',')
    user_ids = os.environ.get("DISCORD_USER_IDS", "").split(',')

    if len(usernames) != len(passwords):
        logger.error("The number of emails does not match the number of passwords")
        return 1

    data = list(zip(usernames, passwords, user_ids))

    messages = await read_channel("Apna Server", "leave-request")

    for author, content in messages:
        try:
            if "-" in content:
                # Split the content into two parts
                start_date, end_date = map(str.strip, content.split("-", 1))
                
                start_date = parse(start_date.strip(), settings={'FUZZY': True}).date()
                end_date = parse(end_date.strip(), settings={'FUZZY': True}).date()

                if start_date <= datetime.now().date() <= end_date:
                    logger.info("Leave for", author.name, content)
                    leave_user_ids.append(f"<@{author.id}>")

            else:
                message_date = parse(content.strip(), settings={'FUZZY': True}).date()

                if datetime.now().date() == message_date:
                    logger.info("Leave for", author.name, content)
                    leave_user_ids.append(f"<@{author.id}>")
        except ValueError:
            logger.info(f"Skipping message from {author.name}: Unable to parse {content} as a date or range.")

    if not result:
        for username, password, user_id in data:
            if user_id in leave_user_ids:
                result[user_id] = "Leave"
            else:
                result[user_id] = CheckInAPI(username, password).checkin()

    MAX_RETRIES = 3
    retries = 0
    while "Failed" in result.values() and retries < MAX_RETRIES:
        logger.info(f"Retrying failed jobs (Attempt {retries + 1}/{MAX_RETRIES})")
        for username, password, user_id in data:
            if result[user_id] == "Failed":
                result[user_id] = CheckInAPI(username, password).checkin()
        retries += 1

    if "Failed" in result.values():
        logger.error("Some jobs failed after maximum retries.")

    send_discord_message(json.dumps(result, indent=4).replace('"', ''))
    logger.info(f"All jobs completed successfully {json.dumps(result, indent=4)}")

if __name__ == "__main__":
    asyncio.run(main(dict()))
