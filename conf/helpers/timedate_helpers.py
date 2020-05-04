import datetime as _datetime

# TIME COMPARISON HELPERS

def create_timestamp():
    """
    Create timestamp string to be used in cahce file comparison
    """
    now = _datetime.datetime.now()
    return now.strftime('%s')

def get_timestamp_diff(timestamp_1, timestamp_2):
    """
    Compare two timestamp strings (created using create_timestamp()) return
    the different in seconds. This will always return a positive number so
    it will not illustrate which timestamp was taken first, just the difference
    between the two times.
    """
    timestamp_diff = 0
    try:
        # compare the time difference and convert number to positive always
        timestamp_diff = abs(int(timestamp_1) - int(timestamp_2))
    except:
        pass
    return timestamp_diff

def is_timestamp_diff_greater_than(timestamp_1, timestamp_2, seconds=0, minutes=0, hours=0):
    """
    Compare two timestamp strings (created using create_timestamp()) and passing in
    the measure of the comparison e.g. 'seconds', 'minutes', 'hours' this method
    will return True/False for IF the difference is GREATER than the provided
    timeframe.
    """
    is_timestamp_diff_greater_than = False
    assert seconds or minutes or hours
    timestamp_diff_in_seconds = get_timestamp_diff(timestamp_1, timestamp_2)
    if minutes:
        seconds += (int(minutes) * 60)
    if hours:
        seconds += (int(hours) * 60 * 60)
    if timestamp_diff_in_seconds > seconds:
        is_timestamp_diff_greater_than = True
    return is_timestamp_diff_greater_than
