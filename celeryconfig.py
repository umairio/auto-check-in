from celery import Celery
from celery.schedules import crontab
from check_in import main



app = Celery("check_in", broker="redis://redis:6379/0")

app.conf.beat_schedule = {
    'daily-checki-in': {
        'task': 'celeryconfig.do_checkin',
        'schedule': crontab(day_of_week="1-5", hour='9-12', minute='20-40'),
    },
}
app.conf.timezone = 'Asia/Karachi'

@app.task
def do_checkin():
    main()