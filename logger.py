import logging
from logging.handlers import SMTPHandler
import os

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(filename)s %(lineno)d %(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S"
)
mail_handler = SMTPHandler(
    mailhost=("smtp.gmail.com", 587),
    fromaddr=os.environ.get("MAIL_USERNAME"),
    toaddrs="umairmateen55@gmail.com",
    subject="Check-In Failed",
    credentials=(os.environ.get("MAIL_USERNAME"), os.environ.get("MAIL_PASSWORD")),
    secure=(),
)
mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))
logger = logging.getLogger()
logger.addHandler(mail_handler)

if __name__ == "__main__":
    logger.info("This is an info message")