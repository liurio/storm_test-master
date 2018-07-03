# -*-coding:utf-8-*-
import time

# 获取标准化的时间
def get_this_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


# 获取时间戳
def get_timestamp():
    t = time.time()
    return int(round(t * 1000))


# 将毫秒时长格式化输出
def format_ms_time(timestamp):
    ms = timestamp % 1000
    seconds = (timestamp / 1000) % 60
    minutes = timestamp / 1000 / 60

    format_output = ""
    if minutes > 0:
        format_output = format_output + "%s min " % minutes
    if seconds > 0:
        format_output = format_output + "%s s " % seconds
    format_output = format_output + "%s ms" % ms
    return format_output