import requests


class CheckInAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url =  "https://linkedmatrix.resourceinn.com/api/v1/oauth/webLogin"
        self.checkin_url = "https://linkedmatrix.resourceinn.com/api/v1/directives/markAttendance"
        self.access_token = str()
        self.employee_id = str()
        self.cookies = dict()
    def login(self):
        headers = {
            "sec-ch-ua-platform": "\"Linux\"",
            "Referer": "https://linkedmatrix.resourceinn.com/",
            "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "Version-Code": "417",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Version-No": "4.1.7"
        }

        data = {
            "email" : self.username,
            "password": self.password
        }

        res = requests.post(self.login_url, headers=headers, data=data)
        if res.status_code != 200:
            raise Exception("Login failed")
        breakpoint()
        self.access_token = res.json().get("data").get("access_token")
        self.cookies = res.cookies.get_dict() #{'laravel_session': 'P1AqDqbULorKaKUzq54i1vkLYp4ba1tGJsPxZzl7'}
        # <RequestsCookieJar[Cookie(version=0, name='laravel_session', value='P1AqDqbULorKaKUzq54i1vkLYp4ba1tGJsPxZzl7', port=None, port_specified=False, domain='linkedmatrix.resourceinn.com', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=1731418480, discard=False, comment=None, comment_url=None, rest={'httponly': None}, rfc2109=False)]>


    def checkin(self):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.access_token,
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryLlz6sJ56J5TaAiKJ",
            "cookie": "_ga=GA1.1.1127918565.1731309533; laravel_session=uoPPixE9jc366lkEmtWXXKvebgcGGRd6UxhHu3DC; _ga_YXXBVRH8F5=GS1.1.1731309532.1.1.1731309542.0.0.0; cf_clearance=8JOO7o_SuH13f16E1Q.E1ndkEHn.DYpeYYXCZD8qvT4-1731309542-1.2.1.1-C9kTGjWcWHKzRLOnJ3HstlkSPIWK68Qq1CC01ibLVWzp9AOYZedORHWrLNqcHIM96sSz66vdwEPvW2ryhOOB17jB2elyEjMQROb0zkC6uB_JkArgsjNESQunF351R4J3iAAMFvACnyjye_5OIFqwJVrXwgd6nGrr7GsajgN4D_MjnFvjFEUkjFY6_ngaASR.U3cZjLHgt9G6IUKDoz27QHrq3SZ3J6ZiixBkZ7pL8teecoSzqAg1y5.wRC_9lAmY8H_bbK5agltpRa7nDw2cUYKArGY_Ke9oWXM88njHvIF2dOaftznYWRnRlVSl.dTzqd.CVe5iLqdgM92qmJ6Ol_WBlEB1ODhnPwgGdteJNHHKHX4C2YzP8webkXXoVWt9",
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
if __name__ == "__main__":
    check_in_api = CheckInAPI("Ahmad Hassan", "123456")
    check_in_api.login()