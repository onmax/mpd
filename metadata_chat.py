import re
import datetime

# Given the string `13/10/17`,for example. It returns the date


def get_date(date_str):
    return datetime.datetime.strptime(date_str, "%d/%m/%y")

# Returns the number of days from the first message to the last message


def get_ndays(first_date, last_date):
    return (get_date(last_date) - get_date(first_date)).days + 1


def main(content):
    regex_date = '\d{1,2}\/\d{1,2}\/\d{1,2}'

    first_day_date = (re.findall(regex_date, content[0]))[0]
    last_day_date = (re.findall(regex_date, content[-1]))[0]

    first_day_str = get_date(first_day_date).strftime("%A %d. %B %Y")
    last_day_str = get_date(last_day_date).strftime("%A %d. %B %Y")
    metadata = {
        'first_day_date': first_day_date,
        'last_day_date': last_day_date,
        'first_day_str': first_day_str,
        'last_day_str': last_day_str,
        'days': get_ndays(first_day_date, last_day_date),
        'nmessages': len(content)
    }
    print(metadata)
