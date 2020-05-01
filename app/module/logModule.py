import logging
import datetime

logging.basicConfig(filename = "logs/test.log", level = logging.DEBUG)

def log(request, message):
    log_date = get_log_date()
    log_message = "{0}/{1}/{2}".format(log_date, str(request), message)
    logging.info(log_message)

def get_log_date():
    dt = datetime.datetime.now()
    log_date = dt.strftime("%Y%m%d_%H:%M:%S")
    return log_date
