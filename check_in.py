from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    filename="checkin.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

def checkin_job(email, passwrd):
    logging.info("Check-in job started")

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        logging.info("Webdriver initiated")

        url = "https://linkedmatrix.resourceinn.com/#/core/login"
        driver.get(url)
        logging.info(f"Navigated to {url}")

        username_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "username"))
        )
        logging.info("Username field located")
        username_field.send_keys(email)

        password_field = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        logging.info("Password field located")

        logging.info(f"Attempting to log in with email: {email}")
        password_field.send_keys(passwrd)

        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        logging.info("Login button located and clicked and redirecting")

        RML = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="wrap"]/div/div/div[2]/div/section/div[2]/div/button',
                )
            )
        )
        RML.click()
        logging.info("RML button located and clicked and redirecting to dashboard")

        try:
            checkin = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="dashboard-here"]/div/div[3]/mark-attendance/section/div[2]/div/div/ng-transclude/div/div[3]/button[1]',
                    )
                )
            )
            checkin.click()
            logging.info("Check-in button located and clicked")
        except TimeoutException:
            logging.error("Check-in button not found or already checked-in")
            return

        logging.info("Job completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()
        logging.info("Webdriver closed")

def main():
    email_passwrd_pairs = [
        ('Muhammad Umair', 'aaaaaa'),
        ('Muhammad Iqran', 'lahore12345')
    ]

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(checkin_job, email, passwrd) for email, passwrd in email_passwrd_pairs]

    for future in futures:
        future.result()


if __name__ == "__main__":
    main()
