import logging
import os
from logging.handlers import SMTPHandler

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(filename)s %(lineno)d %(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S"
)
logger = logging.getLogger()

if __name__ == "__main__":
    logger.info("This is an info message")