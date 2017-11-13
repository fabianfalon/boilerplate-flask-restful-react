import base64
import calendar


def make_basic(user, passw):
    return base64.b64encode(user + ':' + passw)


def get_month_day_range(date):
    """For a date 'date' returns the start and end date for the month
       of 'date'"""
    first_day = date.replace(day=1)
    last_day = date.replace(
        day=calendar.monthrange(date.year, date.month)[1])
    return first_day, last_day
