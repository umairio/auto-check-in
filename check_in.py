import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from logging.handlers import SMTPHandler
import time


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
    mailhost=("smtp.gmail.com", 465),
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


def send_email(email, image=None):
    """
    :param image: str
    :param email: str
    :return: None
    """
    try:
        message = MIMEMultipart()
        message["From"] = os.environ.get("MAIL_USERNAME")
        message["To"] = email
        message["Subject"] = "Check-In Successful"

        # HTML content
        with open("email.html", "r") as file:
            template = file.read()
        if image:
            with open(image, "rb") as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header("Content-ID", "<image1>")
                message.attach(mime_img)
            template = template.replace(
                "https://gxowkk.stripocdn.email/content/guids/CABINET_1232eee4cab038122cd07270cd3bb85f/images/70451618316407074.png",
                "cid:image1"
            )
        message.attach(MIMEText(template, "html"))
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.starttls()
        mail.login(os.environ.get("MAIL_USERNAME"), os.environ.get("MAIL_PASSWORD"))
        mail.sendmail(os.environ.get("MAIL_USERNAME"), email, message.as_string())
        mail.quit()
        logger.info(f"Success email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")


def initiate_driver():
    """
    :return: webdriver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        options=options,
        service=Service(path)
    )


def checkin_job(username, passwrd, email):
    """
    :param username: str
    :param passwrd: str
    :param email: str
    :return: None 

    """
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

        logger.info(f"Attempting to log in with email: {username}")
        password_field.send_keys(passwrd)

        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        logger.info("Login button located and clicked and redirecting")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="wrap"]/div/div/div[2]/div/section/div[2]/div/button',
            ))
        )
        driver.get('https://linkedmatrix.resourceinn.com/#/app/dashboard')
        logger.info("Redirecting to dashboard")

        try:
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
        except TimeoutException:
            try:
                checkout = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        '//*[@id="dashboard-here"]/div/div[3]/mark-attendance/section/div[2]/div/div/ng-transclude/div/div[3]/button[2]',
                    ))
                )
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
        ss = driver.save_screenshot("checkin.png")
        try:
            if email and ss:
                logger.info(f"Screenshot captured for {username}")             
                send_email(email, image='checkin.png')
            elif email:
                send_email(email)
        except Exception as e:
            logger.error(f"An error occurred while sending email: {e}")
        logger.info("Job completed successfully")
    except Exception as e:
        result = "Failed"
        logger.error(f"An error occurred for {username}: {e}")
    finally:
        driver.quit()
        logger.info("Webdriver closed")
        return result


def main():
    usernames = os.environ.get("USERNAMES", "").split(',')
    passwords = os.environ.get("PASSWORDS", "").split(',')
    emails = os.environ.get("EMAILS", "").split(',')

    if len(usernames) != len(passwords):
        logger.error("The number of emails does not match the number of passwords")
        return
    result = dict()
    for username, password, email in list(zip(usernames, passwords, emails)):
        done = checkin_job(username, password, email)
        result[username] = done
    
    logger.info(f"All jobs completed successfully {result}")
    print(result)

if __name__ == "__main__":
    main()
