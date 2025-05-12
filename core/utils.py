import pytz
import datetime

def get_german_time():
    """Returns the current German time in hh:mm format."""
    german_timezone = pytz.timezone("Europe/Berlin")
    german_time = datetime.datetime.now(german_timezone)
    return german_time.strftime("%H:%M")
