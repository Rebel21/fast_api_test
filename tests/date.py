import datetime


def get_date_x_days_earlier_than_today(days_ago=None, format_string="%Y-%m-%d"):
    later_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime(format_string)
    return later_date
