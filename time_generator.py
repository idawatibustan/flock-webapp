import random
import time

def generate_time():
    return randomDate("Feb 1, at 09:35 PM", "Feb 12, at 10:50 AM", random.random())

def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%b %d, at %I:%M %p', prop)

