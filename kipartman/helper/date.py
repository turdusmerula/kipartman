import datetime
import time

# >>> import os
# >>> os.stat("a")
# os.stat_result(st_mode=33204, st_ino=6701130, st_dev=64768, st_nlink=1, st_uid=1000, st_gid=1000, st_size=0, st_atime=1599777792, st_mtime=1599777792, st_ctime=1599777792)
# >>> import datetime
# >>> datetime.datetime.fromtimestamp(os.stat('a').st_ctime)
# datetime.datetime(2020, 9, 11, 0, 43, 12, 579379)

# os.utime(fileLocation, (modTime, modTime))

def datetime_to_utime(value):
    return time.mktime(value.timetuple())+value.microsecond/1000000.

def utime_to_datetime(value):
    return datetime.datetime.fromtimestamp(value)
