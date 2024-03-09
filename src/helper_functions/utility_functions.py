from datetime import datetime

def validate_datetime(datetime_str):
    try:
        datetime_format = "%Y-%m-%dT%H:%M:%S"
        datetime_obj = datetime.strptime(datetime_str, datetime_format)
        return True
    except ValueError:
        return False