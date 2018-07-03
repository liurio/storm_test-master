# -*- coding:utf-8 -*-
from config.Configuration_of_rolling_top_words import cfg_rtw


# 获取到gc的行
def get_lines():
    gc_log_file = cfg_rtw.local_log_base_path + "gc.log"
    lst_ret = []
    with open(gc_log_file, 'r') as open_file:
        for line in open_file:
            if " secs] [" in line:

                first_line = line.replace("\n","")
                second_lst_line = first_line.split(": [")[1:]
                for second_line in second_lst_line:
                    while second_line[-1] == " ":
                        second_line = second_line[:-1]
                    lst_third_lines = second_line.split(" ")[:-1]
                    lst_ret.append(" ".join(lst_third_lines))

    return lst_ret


# 处理gc日志
def handle_gc_log():
    lst_consumer_time = []
    lst_collect_space = []

    log_lines = get_lines()
    for line in log_lines:
        lst_line = line.split(" secs] ")
        lst_line2 = lst_line[0].split(" ")
        # print "line", line
        # print "lst_line2", lst_line2
        consumer_time = float(lst_line2[-1])
        lst_consumer_time.append(consumer_time)
        collect_string = ""
        if not "]" in lst_line2[-2]:
            collect_string = lst_line2[-2]
        else:
            collect_string = lst_line2[-4]

        lst_collect = collect_string.split("->")
        before_space = lst_collect[0]
        after_space = lst_collect[1].split("(")[0]
        collect_space = change_space_to_k(before_space) - change_space_to_k(after_space)
        lst_collect_space.append(collect_space)

    consumer_total_time = reduce(lambda x, y: x + y, lst_consumer_time)
    collect_total_space = reduce(lambda x, y: x + y, lst_collect_space)

    print "共进行了 %s 次的gc" % len(lst_consumer_time)
    print "共耗时 %s s" % consumer_total_time
    print "共回收了 %s m的空间" % change_k_to_m(collect_total_space)


# 将大小转换为K
def change_space_to_k(space_string):
    UNIT = space_string[-1].upper()
    if UNIT == "K":
        return float(space_string[:-1])
    elif UNIT == "M":
        return float(space_string[:-1]) * 1024
    elif UNIT == "G":
        return float(space_string[:-1]) * 1024 *1024


# 将k转换为m
def change_k_to_m(space):
    return space / 1024


if __name__ == "__main__":
    get_lines()
    handle_gc_log()










