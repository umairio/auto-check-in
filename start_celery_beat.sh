#!/bin/sh

SCHEDULE_FILE="celerybeat-schedule"

if [ -f "$SCHEDULE_FILE" ]; then
    echo "Deleting existing celerybeat-schedule file..."
    rm "$SCHEDULE_FILE"
else
    echo "No celerybeat-schedule file found, starting celery-beat..."
fi
rm -rf logs.log
exec celery -A celeryconfig beat -l info
