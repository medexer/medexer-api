from time import time
from datetime import datetime


def CustomResponse(message, status, statusCode, data):
    _time = time()
    dateTime = datetime.fromtimestamp(_time)
    # str_time = dateTime.strftime("%A, %d %B, %Y, %I:%M %P")

    return {
        "timeStamp": datetime.now(),
        "message": message,
        "status": status,
        "statusCode": statusCode,
        "data": data,
    }


def CurrentTimeStamp():
    _time = time()
    dateTime = datetime.fromtimestamp(_time)
    str_time = dateTime.strftime("%A, %d %B, %Y")
    
    return str_time