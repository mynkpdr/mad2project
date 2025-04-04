from datetime import datetime
import pytz

def IndiaNow():
    """
    Returns the current time in India (Asia/Kolkata)
    """
    IST = pytz.timezone('Asia/Kolkata')
    return datetime.now(IST)

def IndiaTimeStampNow():
    """
    Returns the current timestamp in India (Asia/Kolkata)
    """
    IST = pytz.timezone('Asia/Kolkata')
    return int(datetime.now(IST).timestamp())