# -*- coding:utf-8 -*-
from config.Configuration_of_rolling_top_words import cfg_rtw

# 打开文件，返回list
def get_lines_from_file(file_path, *filter_functions):
    re_list = []
    with open(file_path, 'r') as open_file:
        for line in open_file:
            judge = True
            for filter_function in filter_functions:
                judge = (judge and filter_function(line))

            # if "real=" in line and judge == True:
            #     print line, judge

            if judge == True:
                # if  "01 secs]" in line:
                #     print line
                #     print "==================="
                re_list.append(line.replace("\n",""))

    return re_list


# 过滤函数，过滤出含有特定字符的行
def filter_lines_contain_strings(*keywords):
    def filter_lines_function(line):
        for keyword in keywords:
            if not keyword in line:
                return False

        return True

    return filter_lines_function


# 过滤函数，过滤掉含有特定字符的行
def filter_lines_without_strings(*keywords):
    def filter_lines_function(line):
        for keyword in keywords:
            if keyword in line:
                return False

        return True

    return filter_lines_function


# 找出所有行的总耗时
def calculate_all_times(lst_line):
    all_time = 0.0
    for line in lst_line:
        if len(line.split(" ")) > 3:
            this_time = float(line.split(" ")[-2])
            # print "本次回收共耗时 %s s" % this_time
            all_time = all_time + this_time

        # print line, line.split(" ")[-2]
        # this_time = float(line.split(" ")[-2])
        # # print "本次回收共耗时 %s s" % this_time
        # all_time = all_time + this_time

    return all_time


# 计算出GC总共耗时时长
def caculate_gc_total_time(log_file):

    secs_lines = get_lines_from_file(gc_log_file, filter_lines_contain_strings("secs]"),filter_lines_without_strings("real="))
    # for line in secs_lines:
    #     print line
    print "--------------------------------"
    all_time = calculate_all_times(secs_lines)
    print "gc总共耗时%ss" % all_time
    print "------------- 分割线 -------------"


# 得到collect_string
def get_collect_string(line):
    collect_string = ""
    if "GC cleanup" in line:
        collect_string = line.split(" ")[-3][:-1]
    elif "Heap:" in line:
        collect_string = line.split(" ")[-1][:-1]
    return collect_string



# 将string中的括弧和其中的内容去掉
def get_string_without_parenthesis(string):
    return string.split("(")[0]


# 将string类型的size转换成以k为单位的long类型的size
def convert_string_size_to_long_kb_size(string_size):
    if len(string_size) > 0:
        if string_size[-1].upper() == "M":
            return float(string_size[:-1]) * 1024
        elif string_size[-1].upper() == "G":
            return float(string_size[:-1]) * 1024 * 1024
        elif string_size[-1].upper() == "K":
            return float(string_size[:-1])



# 得到from_string和to_string
def get_from_and_to_size(collect_string):
    lst_string = collect_string.split("->")
    return map(convert_string_size_to_long_kb_size,map(get_string_without_parenthesis, lst_string))


# 计算所有的回收空间大小的和
def caculate_totoal_collect_size_by_lst_pairs(lst_collect_pair):
    total_collect_size = 0.0
    for pair in lst_collect_pair:
        if not pair == None and not pair[0] == None:
            this_size = pair[0] - pair[1]
            total_collect_size = total_collect_size + this_size

    return total_collect_size


def caculate_totoal_collect_size():
    collect_lines = get_lines_from_file(gc_log_file, filter_lines_contain_strings("->"))
    lst_collect_string = map(get_collect_string, collect_lines)
    lst_pairs = map(get_from_and_to_size, lst_collect_string)
    # print "-------- 打印回收的细节，开始 --------"
    # for pair in lst_pairs:
    #     if not pair == None and not pair[0] == None:
    #         print "从 %s 回收至 %s" % ((pair[0]/1024) , (pair[1]/1024))
    # print "-------- 打印回收的细节，结束 --------"
    total_collect_size = caculate_totoal_collect_size_by_lst_pairs(lst_pairs)

    print "gc总共回收了 %s M的数据" % (total_collect_size/1024)
    print "gc总共进行了 %s 次" % len(lst_pairs)


if __name__ == "__main__":

    gc_log_file = cfg_rtw.local_log_base_path + "gc.log"

    # 计算gc总时长
    caculate_gc_total_time(gc_log_file)

    # 计算gc总回收内存大小
    caculate_totoal_collect_size()







