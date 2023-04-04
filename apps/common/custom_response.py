from time import time
from datetime import datetime


def customResponse(message, status, statusCode, data):
    _time = time()
    dateTime = datetime.fromtimestamp(_time)
    str_time = dateTime.strftime("%A, %d %B, %Y, %I:%M %P")

    return {
        "timeStamp": str_time,
        "message": message,
        "status": status,
        "statusCode": statusCode,
        "data": data,
    }
