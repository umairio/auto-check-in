import logging
import os
import smtplib
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

logging.basicConfig(
    filename="checkin.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
)


def send_success_email(email):
    try:
        # Create the email
        message = MIMEMultipart()
        message["From"] = os.environ.get("MAIL_USERNAME")
        message["To"] = email
        message["Subject"] = "Check-In Successful"

        # HTML content
        with open("email.html", "r") as file:
            html_content = file.read()


        # Attach the HTML content to the email
        message.attach(MIMEText(html_content, "html"))

        # Send the email
        mail = smtplib.SMTP("smtp.gmail.com", 587)
        mail.starttls()
        mail.login(os.environ.get("MAIL_USERNAME"), os.environ.get("MAIL_PASSWORD"))
        mail.sendmail(os.environ.get("MAIL_USERNAME"), email, message.as_string())
        mail.quit()
        logging.info(f"Success email sent to {email}")
    except Exception as e:
        logging.error(f"Failed to send email to {email}: {e}")


def initiate_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def checkin_job(username, passwrd, email):
    logging.info("Check-in job started")

    try:
        driver = initiate_driver()

        logging.info("Webdriver initiated")

        url = "https://linkedmatrix.resourceinn.com/#/core/login"
        driver.get(url)
        logging.info(f"Navigated to {url}")

        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        logging.info("Username field located")
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        logging.info("Password field located")

        logging.info(f"Attempting to log in with email: {username}")
        password_field.send_keys(passwrd)

        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        logging.info("Login button located and clicked and redirecting")

        RML = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((
                By.XPATH,
                '//*[@id="wrap"]/div/div/div[2]/div/section/div[2]/div/button',
            ))
        )
        RML.click()
        logging.info("'Remind me later' button located and clicked and redirecting to dashboard")

        try:
            checkin = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[@id="dashboard-here"]/div/div[3]/mark-attendance/section/div[2]/div/div/ng-transclude/div/div[3]/button[1]',
                ))
            )
            checkin.click()
            if email:
                send_success_email(email)
            logging.info(f"{username} checked-in successfully")
        except TimeoutException:
            logging.error(f"Check-in button not found or already checked-in for {username}")
            return

        logging.info("Job completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()
        logging.info("Webdriver closed")


def main():
    usernames = os.environ.get("USERNAMES", "").split(',')
    passwords = os.environ.get("PASSWORDS", "").split(',')
    emails = os.environ.get("EMAILS", "").split(',')

    if len(usernames) != len(passwords):
        logging.error("The number of emails does not match the number of passwords")
        return

    for username, password, email in list(zip(usernames, passwords, emails)):
        checkin_job(username, password, email)
    
    logging.info("All jobs completed successfully")
if __name__ == "__main__":
    main()
