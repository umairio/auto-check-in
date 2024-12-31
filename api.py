import requests

from logger import logger


class CheckInAPI:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.login_url = "https://linkedmatrix.resourceinn.com/api/v1/oauth/webLogin"
        self.checkin_url = "https://linkedmatrix.resourceinn.com/api/v1/directives/markAttendance"
        self.access_token = str()
        self.employment_id = str()
        self.cookies = dict()
        self.id = int()

    def login(self):
        headers = {
            "sec-ch-ua-platform": '"Linux"',
            "Referer": "https://linkedmatrix.resourceinn.com/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "Version-Code": "417",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Version-No": "4.1.7"
        }

        data = {
            "email": self.username,
            "password": self.password
        }

        res = requests.post(self.login_url, headers=headers, data=data)
        logger.info(f"Login for {self.username}: {res.status_code}")
        if res.status_code != 200:
            raise Exception("Login failed")
        self.access_token = res.json().get("data").get("access_token")
        self.cookies = res.cookies.get_dict()  # {'laravel_session': 'P1AqDqbULorKaKUzq54i1vkLYp4ba1tGJsPxZzl7'}
        # self.employment_id = res.json().getx("data").get("user").get("employment_id")
        # <RequestsCookieJar[Cookie(version=0, name='laravel_session', value='P1AqDqbULorKaKUzq54i1vkLYp4ba1tGJsPxZzl7', port=None, port_specified=False, domain='linkedmatrix.resourceinn.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=1731418480, discard=False, comment=None, comment_url=None, rest={'httponly': None}, rfc2109=False)]>

    def checkin(self):
        self.login()
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.access_token,
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryLlz6sJ56J5TaAiKJ",
            "cookie": f"laravel_session={self.cookies.get('laravel_session')}",
            "origin": "https://linkedmatrix.resourceinn.com",
            "priority": "u=1, i",
            "referer": "https://linkedmatrix.resourceinn.com/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "version-code": "417",
            "version-no": "4.1.7",
        }

        data = """------WebKitFormBoundaryLlz6sJ56J5TaAiKJ
Content-Disposition: form-data; name="mark_attendance"

{"mark_checkin": true}

------WebKitFormBoundaryLlz6sJ56J5TaAiKJ--
"""

        res = requests.post(self.checkin_url, headers=headers, data=data)
        logger.info(f"checkin for {self.username}: {res.status_code}")
        if res.status_code == 200 and 'data' in res.json():
            return "Success"
        else:
            return "Failed"
