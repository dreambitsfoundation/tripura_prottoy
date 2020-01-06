import pytz
from django.conf.global_settings import TIME_ZONE
from django.db.models import DateTimeField


def generate_readable_date_time(date_time: DateTimeField):
    tz = pytz.timezone(TIME_ZONE)
    return date_time.astimezone(tz=tz).strftime('%a, %d %B %Y %I:%M:%S %p')