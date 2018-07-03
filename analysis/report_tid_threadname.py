# -*- coding:utf-8 -*-
from config.Configuration_of_rolling_top_words import *

# 从jstack日志中获取flowThreads的进程号
def get_tid_threadname_from_jstack_log(path = cfg_rtw.local_log_base_path + "jstack.log"):
    return_dictionary = {}
    with open(path, 'r') as read_file:
        for line in read_file:
            if "nid=" in line and "0x" in line:
                this_thread_name = line.split("\"")[1]
                lst_line = line.replace("\n","").split(" ")
                for member in lst_line:
                    if "nid=" in member:
                        this_tid_16 = member.replace("nid=","")
                        this_tid = int(this_tid_16,16)
                        return_dictionary[this_thread_name] = this_tid

    return return_dictionary

if __name__ == "__main__":


    path = cfg_rtw.local_log_base_path + "jstack.log"

    dictionary_result = get_tid_threadname_from_jstack_log(path)

    lst_threadname = dictionary_result.keys()
    lst_threadname.sort()

    for key in lst_threadname:
        print "%s \t %s" % ( dictionary_result[key],key)