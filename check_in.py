import logging
import os
import time
from logging.handlers import SMTPHandler
from pprint import pprint

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import (StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from discobot import send_discord_message

load_dotenv()

path = (
    ChromeDriverManager().install()
    .replace('chromedriver-linux64/THIRD_PARTY_NOTICES.chromedriver', 'chromedriver-linux64/chromedriver')
    .replace('chromedriver-win32/THIRD_PARTY_NOTICES.chromedriver', r'chromedriver-win32\chromedriver.exe')
)
if "linux" in path:
    os.chmod(path, 0o755)

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
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




def initiate_driver():
    """
    :return: webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options, service=Service(path))
    driver.execute_script("document.body.style.zoom='70%'")
    return driver


def checkin_job(username, passwrd):
    """
    :param username: str
    :param passwrd: str
    :return: None 

    """
    def checkin(driver):
        driver.execute_script("document.body.style.zoom='70%'")
        checkin = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="dashboard-here"]/div/div[3]/mark-attendance/section/div[2]/div/div/ng-transclude/div/div[3]/button[1]',
            ))
        )
        action = ActionChains(driver)
        time.sleep(1)
        action.move_to_element(checkin).perform()
        time.sleep(1)
        checkin.click()
        time.sleep(2)
        result = "Success"
        logger.info(f"{username} checked-in successfully")
        return result, driver
    
    logger.info(f"Check-in job started for: {username}")
    result = str

    try:
        driver = initiate_driver()

        logger.info("Webdriver initiated")

        url = "https://linkedmatrix.resourceinn.com/#/core/login"
        driver.get(url)
        logger.info(f"Navigated to {url}")

        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        logger.info("Username field located")
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        logger.info("Password field located")

        logger.info(f"Attempting to log in for: {username}")
        password_field.send_keys(passwrd)

        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        logger.info("Login button located and clicked and redirecting")
        rml = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                '//*[@id="wrap"]/div/div/div[2]/div/section/div[2]/div/button',))
        )
        rml.click()
        # driver.get("https://linkedmatrix.resourceinn.com/#/app/dashboard")
        # logger.info("Redirecting to dashboard")
        try:
            result, driver = checkin(driver)
        except TimeoutException:
            try:
                checkout = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                    '//*[@id="dashboard-here"]/div/div[3]/mark-attendance/section/div[2]/div/div/ng-transclude/div/div[3]/button[2]',
                )))
                if checkout:
                    action = ActionChains(driver)
                    time.sleep(1)
                    action.move_to_element(checkout).perform()
                    time.sleep(1)
                    result = "skip"
                    logger.info(f"Already checked-in for {username}")
            except Exception as e:
                logger.info(e)
                result = "Failed"
                return result
        except StaleElementReferenceException:
            logger.info("stale element reference, Refreshing the page")
            driver.get("https://linkedmatrix.resourceinn.com/#/app/dashboard")
            result, driver = checkin(driver)
        driver.execute_script("document.body.style.zoom='70%'")
        ss = driver.save_screenshot("checkin.png")

        #send discord messages
        try:
            if ss:
                content = "<@1027111068704714833> Checked-in successfully" if username == "Muhammad Umair" else username + " Checked-in successfully"
                logger.info(f"Screenshot captured for {username}")             
                send_discord_message(content, image='checkin.png')
            else:
                send_discord_message(content)
        except Exception as e:
            logger.error(f"An error occurred while sending message: {e}")

        logger.info("Job completed successfully")
    except Exception as e:
        result = "Failed"
        logger.error(f"An error occurred for {username}: {e}")
    finally:
        driver.quit()
        logger.info("Webdriver closed")
        return result


def main(result = None):
    usernames = os.environ.get("USERNAMES", "").split(',')
    passwords = os.environ.get("PASSWORDS", "").split(',')
    # emails = os.environ.get("EMAILS", "").split(',')
    leave_users = os.environ.get("LEAVE_USERS", "").split(',')
    if len(usernames) != len(passwords):
        logger.error("The number of emails does not match the number of passwords")
        return
    data = list(zip(usernames, passwords))
    if not result:
        for username, password in data:
            result[username] = checkin_job(username, password) if username not in leave_users else "leave"
        pprint(result)

    # if failed retry
    if "Failed" in result.values():
        logger.info("Retrying failed jobs")
        for username, password in data:
            if result[username] == "Failed":
                result[username] = checkin_job(username, password)
        pprint(result)

    logger.info(f"All jobs completed successfully {result}")

if __name__ == "__main__":
    main(result = dict())
