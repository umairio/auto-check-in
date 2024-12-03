import requests, os, json
from logger import logger
from pprint import pprint
from discobot import send_discord_message



class CheckInAPI:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.login_url =  "https://linkedmatrix.resourceinn.com/api/v1/oauth/webLogin"
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
            "email" : self.username,
            "password": self.password
        }

        res = requests.post(self.login_url, headers=headers, data=data)
        logger.info(f"Login for {self.username}: {res.status_code}")
        if res.status_code != 200:
            raise Exception("Login failed")
        self.access_token = res.json().get("data").get("access_token")
        self.cookies = res.cookies.get_dict() #{'laravel_session': 'P1AqDqbULorKaKUzq54i1vkLYp4ba1tGJsPxZzl7'}
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
        logger.info(f"checkin for {username}: {res.status_code}")
        if res.status_code == 200 and 'data' in res.json():
            return "Success"
        else:
            return "Failed"


if __name__ == "__main__":
    result = dict()
    usernames = os.environ.get("USERNAMES", "").split(',')
    passwords = os.environ.get("PASSWORDS", "").split(',')
    leave_users = os.environ.get("LEAVE_USERS", "").split(',')
    user_ids = os.environ.get("DISCORD_USER_IDS", "").split(',')
    # emails = os.environ.get("EMAILS", "").split(',')
    if len(leave_users[0]):print(leave_users)
    if len(usernames) != len(passwords):
        logger.error("The number of emails does not match the number of passwords")
        raise Exception
    data = list(zip(usernames, passwords, user_ids))
    if not result:
        for username, password, user_id in data:
            if username not in leave_users:
                result[user_id] = CheckInAPI(username, password).checkin()
            else:
                result[user_id] = "Leave"

    # if failed result
    while "Failed" in result.values():
        logger.info("Retrying failed jobs")
        for username, password, user_id in data:
            if result[user_id] == "Failed":
                result[user_id] = CheckInAPI(username, password).checkin()
    
    send_discord_message(json.dumps(result, indent=4).replace('"', ''))

    logger.info(f"All jobs completed successfully {json.dumps(result, indent=4)}")    


# def time_waste():
#     false = False
#     true = True
#     null = None
#     identifier = f"{datetime.now().date().strftime('%Y%m%d')}-{self.employment_id}"
#     breaks = [{"id": 1, "name": "Default", "start": "Break Out", "end": "Break In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}, {"id": 2, "name": "Personal", "start": "Personal Out", "end": "Personal In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}, {"id": 3, "name": "Tea/Smoking", "start": "Tea/Smoking Out", "end": "Tea/Smoking In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}, {"id": 4, "name": "Official Work", "start": "Official Work Out", "end": "Official Work In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}, {"id": 5, "name": "Lunch", "start": "Lunch Out", "end": "Lunch In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}, {"id": 6, "name": "Prayer", "start": "Prayer Out", "end": "Prayer In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}, {"id": 7, "name": "Other", "start": "Other Out", "end": "Other In", "description": null, "created_at": "2020-06-09 12:52:50", "updated_at": "2020-06-09 12:52:50", "deleted_at": null, "icon": null, "start_color": null, "end_color": null}]
#     time_slot = {"id": 1, "code": "TS-00001", "day_changed": true, "start_buffer_minutes": 0, "end_buffer_minutes": 0, "punch_end_buffer_minutes": 59, "is_overtime_applicable": true, "is_active": true, "created_at": "2021-07-05 10:25:42", "updated_at": "2023-11-27 07:27:57", "deleted_at": null, "company_id": 1, "name": "General Timing ( Flexible Shift ) Short OT", "duration_minutes": 1320, "start": "2023-11-27 04:00:00", "end": "2023-11-28 02:00:00", "is_flexible": true, "flexible_minutes": 540, "bg_colour": "#008f35", "font_colour": "#000000", "is_full_overtime_slot": false, "is_night": false, "punch_start_buffer_minutes": 60, "flexible_hours": 9, "identifier": "TS-00001 - General Timing ( Flexible Shift ) Short OT (09:00 am - 07:00 am)", "status": "Active", "status_class": "bg-success"}
#     shift = {"id": 3562, "created_at": "2024-01-01 06:43:16", "updated_at": "2024-01-01 06:43:16", "deleted_at": null, "employment_id": self.employment_id, "company_id": 1, "time_slot_id": 1, "date": str(datetime.now().date()) +" 00:00:00", "bg_colour": "#008f35", "font_colour": "#000000", "over_time_hours": 0, "start_datetime":  str(datetime.now().date())+" 04:00:00", "end_datetime": str(datetime.now().date()+timedelta(days = 1))+" 02:00:00", "department_hierarchy_code": "", "is_default": false, "expected_minutes": 540, "is_full_overtime_shift": false, "geo_fence_ids": [], "identifier": identifier, "is_work_from_home": false, "is_optional": false, "shift_tags": [], "time_slot": time_slot}
#     payload = {"breaks": breaks, "is_checkin_time": false, "checkin_time": "", "checkin_address": "", "is_checkout_time": false, "checkout_time": "", "checkout_address": "", "break_id": null, "is_break": false, "break_time": "", "is_pic_required": false, "shift": shift, "geo_fences": [], "mark_checkin": true}
#     data = f"""------WebKitFormBoundaryLlz6sJ56J5TaAiKJ
# Content-Disposition: form-data; name="mark_attendance"

# {json.dumps(payload)}

# ------WebKitFormBoundaryLlz6sJ56J5TaAiKJ--
# """
