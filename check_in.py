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
    format="[%(asctime)s] %(message)s",
)


def send_success_email(email):
    try:
        # Create the email
        message = MIMEMultipart()
        message["From"] = os.environ.get("MAIL_USERNAME")
        message["To"] = email
        message["Subject"] = "Check-In Successful"

        # HTML content
        html_content = """
        <html dir="ltr" xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">
          <head>
            <meta charset="UTF-8">
            <meta content="width=device-width, initial-scale=1" name="viewport">
            <meta name="x-apple-disable-message-reformatting">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta content="telephone=no" name="format-detection">
            <title></title>
            <!--[if (mso 16)]>
            <style type="text/css">
            a {text-decoration: none;}
            </style>
            <![endif]-->
            <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]-->
            <!--[if gte mso 9]>
        <xml>
            <o:OfficeDocumentSettings>
            <o:AllowPNG></o:AllowPNG>
            <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
            <!--[if mso]>
        <style type="text/css">
          ul {
          margin: 0 !important;
        }
        ol {
          margin: 0 !important;
        }
        li {
          margin-left: 47px !important;
        }

        </style><![endif]
        -->
          </head>
          <body class="body">
            <div dir="ltr" class="es-wrapper-color">
              <!--[if gte mso 9]>
              <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                <v:fill type="tile" color="#fafafa"></v:fill>
              </v:background>
            <![endif]-->
              <table width="100%" cellspacing="0" cellpadding="0" class="es-wrapper">
                <tbody>
                  <tr>
                    <td valign="top" class="esd-email-paddings">
                      <table cellpadding="0" cellspacing="0" align="center" class="es-content esd-header-popover">
                        <tbody>
                          <tr>
                            <td align="center" class="esd-stripe">
                              <table align="center" cellpadding="0" cellspacing="0" width="600" bgcolor="rgba(0, 0, 0, 0)" class="es-content-body" style="background-color:transparent">
                                <tbody>
                                  <tr>
                                    <td align="left" class="esd-structure es-p20">
                                      <table cellpadding="0" cellspacing="0" width="100%">
                                        <tbody>
                                          <tr>
                                            <td align="center" valign="top" width="560" class="esd-container-frame">
                                              <table cellpadding="0" cellspacing="0" width="100%">
                                                <tbody>
                                                  <tr>
                                                    <td align="center" class="esd-block-image es-infoblock" style="font-size:0">
                                                      <a target="_blank">
                                                        <img src="https://gxowkk.stripocdn.email/content/guids/CABINET_69e84f3e7d4b41063cd667eb41c0244b0c5b1986d6ea3382963a2c955c972425/images/download.png" alt="" width="560" class="adapt-img" style="border-radius:0">
                                                      </a>
                                                    </td>
                                                  </tr>
                                                </tbody>
                                              </table>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      <table cellpadding="0" align="center" cellspacing="0" class="es-content">
                        <tbody>
                          <tr>
                            <td align="center" bgcolor="transparent" class="esd-stripe">
                              <table align="center" width="600" cellpadding="0" cellspacing="0" bgcolor="#ffffff" class="es-content-body">
                                <tbody>
                                  <tr>
                                    <td align="left" class="esd-structure es-p20r es-p20l">
                                      <table cellpadding="0" cellspacing="0" align="right" class="es-right">
                                        <tbody>
                                          <tr>
                                            <td width="560" align="left" class="esd-container-frame">
                                              <table cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                                <tbody>
                                                  <tr>
                                                    <td align="center" class="esd-block-text es-text-6752 es-p5t">
                                                      <h2 class="es-text-mobile-size-36" style="font-size: 36px; color: #444343; font-family: &#39;comic sans ms&#39;,&#39;marker felt-thin&#39;,arial,sans-serif">
                                                        <b>
                                                          <em>
                                                            Attendance Confirmation
                                                          </em>
                                                        </b>
                                                      </h2>
                                                    </td>
                                                  </tr>
                                                </tbody>
                                              </table>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      <table cellpadding="0" cellspacing="0" align="center" class="es-content">
                        <tbody>
                          <tr>
                            <td align="center" class="esd-stripe">
                              <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" width="600" class="es-content-body">
                                <tbody>
                                  <tr>
                                    <td align="left" class="esd-structure es-p30t es-p20b es-p20r es-p20l">
                                      <table cellpadding="0" cellspacing="0" width="100%">
                                        <tbody>
                                          <tr>
                                            <td width="560" align="center" valign="top" class="esd-container-frame">
                                              <table cellpadding="0" cellspacing="0" width="100%">
                                                <tbody>
                                                  <tr>
                                                    <td align="left" class="esd-block-text es-p5t es-p5b es-text-6509">
                                                      <p class="es-text-mobile-size-18" style="font-size: 18px; line-height: 150%; color: #444444">
                                                        I hope this email finds you well.
                                                      </p>
                                                      <p class="es-text-mobile-size-18" style="font-size: 18px; line-height: 150%; color: #444444">
                                                        This is to confirm that your check-in/attendance has been successfully recorded for today. If you have any questions or notice any discrepancies, please feel free to reach out.
                                                      </p>
                                                    </td>
                                                  </tr>
                                                  <tr>
                                                    <td align="center" class="esd-block-spacer es-p20" style="font-size: 0">
                                                      <table border="0" width="100%" height="100%" cellpadding="0" cellspacing="0" class="es-spacer">
                                                        <tbody>
                                                          <tr>
                                                            <td style="border-bottom: 1px solid #cccccc; background: none; height: 1px; width: 100%; margin: 0px 0px 0px 0px"></td>
                                                          </tr>
                                                        </tbody>
                                                      </table>
                                                    </td>
                                                  </tr>
                                                  <tr>
                                                    <td align="left" class="esd-block-text es-p5t es-p5b">
                                                      <p>
                                                        Best regards,
                                                        <br>
                                                        Muhammad Umair
                                                      </p>
                                                    </td>
                                                  </tr>
                                                  <tr>
                                                    <td align="center" class="esd-block-image es-p10t es-p10b" style="font-size:0px">
                                                      <a target="_blank">
                                                        <img src="https://gxowkk.stripocdn.email/content/guids/CABINET_1232eee4cab038122cd07270cd3bb85f/images/70451618316407074.png" alt="" width="260" class="adapt-img" style="display:block">
                                                      </a>
                                                    </td>
                                                  </tr>
                                                </tbody>
                                              </table>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </body>
        </html>
        """

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


def checkin_job(username, passwrd, email):
    logging.info("Check-in job started")

    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

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
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="wrap"]/div/div/div[2]/div/section/div[2]/div/button',
                )
            )
        )
        RML.click()
        logging.info("'Remind me later' button located and clicked and redirecting to dashboard")

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
    usernames = os.environ.get("USERNAMES", "")
    passwords = os.environ.get("PASSWORDS", "")
    emails = os.environ.get("EMAILS", "")

    if not usernames or not passwords:
        logging.error("No emails or passwords found in environment variables")
        return

    username_list = usernames.split(',')
    password_list = passwords.split(',')
    email_list = emails.split(',')

    if len(username_list) != len(password_list):
        logging.error("The number of emails does not match the number of passwords")
        return

    email_passwrd_pairs = list(zip(username_list, password_list, email_list))

    n = len(username_list)

    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(checkin_job, username, password, email) for username, password, email in email_passwrd_pairs]

    for future in futures:
        future.result()


if __name__ == "__main__":
    main()
