import datetime
from dateutil.parser import parse

def is_date(string):
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False

def generate_output_filename():
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    return f"result-{current_date}.csv"
