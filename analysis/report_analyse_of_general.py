#-*- coding:utf-8 -*-
from config.Configuration_of_rolling_top_words import cfg_rtw
import matplotlib.pyplot as plt
import numpy
import os

class report_data():
    vmstat_data = {}
    pidstat_data = []
    nethogs_data = {}

    global_start_timestamp = None
    global_end_timestamp = None

    pidstat_analysed = 0

    dict_color = {
        u"西红柿红" : "tomato",
        u"苍蓝" : "cadetblue",
        u"紫色" : "m",
        u"红色" : "fuchsia",
        u"绿色" : "limegreen",
        u"天蓝色" : "skyblue",
        u"黄色" : "yellow",
        u"黑色" : "black",
        u"灰色" : "darkgrey",
        u"褐色" : "tan"
    }

    DICT_ITEM_PIDSTAT_SORT = {
        "TIME": 1, "PID": 2, "TID": 3, "USR": 4, "SYSTEM": 5, "QUEST": 6, "CPU": 7, "CPU_SORT": 8,
        "MINFLT/S": 9, "MAJFLT/S": 10, "VSZ": 11, "RSS": 12, "MEM": 13, "KB_RD/S": 14, "KB_WR/S": 15,
        "CCWR/S": 16, "CSWCH/S": 17, "NVCSWCH/S": 18, "COMMAND": 19
    }
    DICT_ITEM_VMSTAT_SORT = {
        "R": 0, "B": 1, "SWPD": 2, "FREE": 3, "BUFF": 4, "CACHE": 5, "SI": 6, "SO": 7, "BI": 8, "BO": 9,
        "IN": 10, "CS": 11, "US": 12, "SY": 13, "ID": 14, "WA": 15, "ST": 16, "TIME": 17
    }
    DICT_ITEM_NETHOGS_SORT = {
        "PID": 0, "SENT": 1, "RECEIVE": 2, "TIME": 3
    }


"""
  上下文切换分析
"""
def analyze_of_cs():

    lst_pidstat_cs = []
    # 总体的timestamp的lst
    lst_total_timestamp = []
    # print "report_data.pidstat_data", len(report_data.pidstat_data)
    for dict_pidstat_data in report_data.pidstat_data:
        lst_pidstat_timestamp = dict_pidstat_data["TIME"]
        lst_pidstat_cswch = dict_pidstat_data["CSWCH/S"]
        lst_pidstat_nvcswch = dict_pidstat_data["NVCSWCH/S"]
        lst_pidstat_tid = dict_pidstat_data["TID"]
        dict_this_pidstat_cswch = {}
        for i in xrange(len(lst_pidstat_timestamp)):
            if not lst_pidstat_tid[i] == '0':
                timestamp = long(lst_pidstat_timestamp[i])
                cswch_value = float(lst_pidstat_cswch[i])
                nvcswch_value = float(lst_pidstat_nvcswch[i])
                cswch_total = cswch_value + nvcswch_value
                if not timestamp in dict_this_pidstat_cswch.keys():
                    dict_this_pidstat_cswch[timestamp] = cswch_total
                else:
                    dict_this_pidstat_cswch[timestamp] = dict_this_pidstat_cswch[timestamp] + cswch_total
        lst_pidstat_cs.append(dict_this_pidstat_cswch)
        lst_total_timestamp.extend(dict_this_pidstat_cswch.keys())

    # 将lst_total_timestamp进行排序
    lst_total_timestamp.sort()

    dict_pidstat_cswch = {}
    for key in lst_total_timestamp:
        # contain_this_key = True
        # for dict_value in lst_pidstat_cs:
        #     if not key in dict_value.keys():
        #         contain_this_key = False
        # if contain_this_key:
        #     dict_pidstat_cswch[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_cs if key in dict_value])
        dict_pidstat_cswch[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_cs if key in dict_value])


    lst_vmstat_timestamp = report_data.vmstat_data["TIME"]
    lst_vmstat_cs_value = report_data.vmstat_data["CS"]
    dict_vmstat_cs = {}
    for i in xrange(len(lst_vmstat_timestamp)):
        timestamp = long(lst_vmstat_timestamp[i])
        cs = float(lst_vmstat_cs_value[i])
        if not timestamp in dict_vmstat_cs.keys():
            dict_vmstat_cs[timestamp] = cs
        else:
            dict_vmstat_cs[timestamp] = dict_vmstat_cs[timestamp] + cs

    lst_datas = [dict_pidstat_cswch, dict_vmstat_cs]
    lst_color = [u"西红柿红", u"苍蓝"]
    lst_tags = [u"storm context-switch", u"system context-switch"]
    xlabel = u"时间"
    ylabel = u"上下文切换"
    title = u"上下文切换情况"
    print_with_data(lst_datas, lst_color, lst_tags, xlabel, ylabel, title)


"""
  内存分析
"""
def analyze_of_mem():
    lst_pidstat_mem = []
    # 总体的timestamp的lst
    lst_total_timestamp = []
    # print "report_data.pidstat_data", len(report_data.pidstat_data)
    for dict_pidstat_data in report_data.pidstat_data:
        lst_pidstat_timestamp = dict_pidstat_data["TIME"]
        lst_pidstat_mem_value = dict_pidstat_data["MEM"]
        lst_pidstat_tid = dict_pidstat_data["TID"]
        dict_this_pidstat_mem = {}
        for i in xrange(len(lst_pidstat_timestamp)):
            if lst_pidstat_tid[i] == '0':
                timestamp = long(lst_pidstat_timestamp[i])
                mem_value = float(lst_pidstat_mem_value[i])
                if not timestamp in dict_this_pidstat_mem.keys():
                    dict_this_pidstat_mem[timestamp] = mem_value
                # else:
                #     dict_this_pidstat_mem[timestamp] = dict_this_pidstat_mem[timestamp] + mem_value
                # print timestamp, dict_this_pidstat_mem[timestamp]
        lst_pidstat_mem.append(dict_this_pidstat_mem)
        lst_total_timestamp.extend(dict_this_pidstat_mem.keys())

    # 将lst_total_timestamp进行排序
    lst_total_timestamp.sort()

    dict_pidstat_mem = {}
    for key in lst_total_timestamp:
        # contain_this_key = True
        # for dict_value in lst_pidstat_mem:
        #     if not key in dict_value.keys():
        #         contain_this_key = False
        # if contain_this_key:
        #     dict_pidstat_mem[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_mem if key in dict_value.keys()])
        dict_pidstat_mem[key] = reduce(lambda x, y: x + y,
                                       [dict_value[key] for dict_value in lst_pidstat_mem if key in dict_value.keys()])

    lst_datas = [dict_pidstat_mem]
    lst_color = [u"西红柿红"]
    lst_tags = [u"storm MEM"]
    xlabel = u"时间"
    ylabel = u"内存使用率"
    title = u"内存使用率"
    print_with_data(lst_datas, lst_color, lst_tags, xlabel, ylabel, title)


"""
  Net IO分析
"""
def analyze_of_NetIO():
    dict_nethogs_sent = {}
    dict_nethogs_receive = {}
    lst_nethogs_timestamp = report_data.nethogs_data["TIME"]
    lst_nethogs_sent = report_data.nethogs_data["SENT"]
    lst_nethogs_receive = report_data.nethogs_data["RECEIVE"]
    lst_nethogs_pid = report_data.nethogs_data["PID"]
    dict_nethogs_sent = {}
    dict_nethogs_receive = {}
    for i in xrange(len(lst_nethogs_timestamp)):
        timestamp = long(lst_nethogs_timestamp[i])
        sent = float(lst_nethogs_sent[i])
        receive = float(lst_nethogs_receive[i])
        # print timestamp, cpu_total
        if not timestamp in dict_nethogs_sent.keys():
            dict_nethogs_sent[timestamp] = sent
        else:
            dict_nethogs_sent[timestamp] = dict_nethogs_sent[timestamp] + sent

        if not timestamp in dict_nethogs_receive.keys():
            dict_nethogs_receive[timestamp] = receive
        else:
            dict_nethogs_receive[timestamp] = dict_nethogs_receive[timestamp] + receive

    lst_datas = [dict_nethogs_sent, dict_nethogs_receive]
    lst_color = [u"西红柿红", u"苍蓝"]
    lst_tags = [u"storm Net IO sent", u"storm Net IO receive"]
    xlabel = u"时间"
    ylabel = u"Net IO 速率（KB/S）"
    title = u"Net IO 速率（KB/S）"
    print_with_data(lst_datas, lst_color, lst_tags, xlabel, ylabel, title)


"""
  Disk IO 分析
"""
def analyze_of_DiskIO():
    lst_pidstat_rd = []
    lst_pidstat_wr = []
    # 总体的timestamp的lst
    lst_total_timestamp = []
    for dict_pidstat_data in report_data.pidstat_data:
        lst_pidstat_timestamp = dict_pidstat_data["TIME"]
        lst_pidstat_rd_value = dict_pidstat_data["KB_RD/S"]
        lst_pidstat_wr_value = dict_pidstat_data["KB_WR/S"]
        lst_pidstat_tid = dict_pidstat_data["TID"]
        dict_this_pidstat_rd = {}
        dict_this_pidstat_wr = {}
        for i in xrange(len(lst_pidstat_timestamp)):
            if lst_pidstat_tid[i] == '0':
                timestamp = long(lst_pidstat_timestamp[i])
                rd_value = float(lst_pidstat_rd_value[i])
                wr_value = float(lst_pidstat_wr_value[i])
                # print timestamp, lst_pidstat_tid[i], cpu_value
                dict_this_pidstat_rd[timestamp] = rd_value
                dict_this_pidstat_wr[timestamp] = wr_value
                # print timestamp, cpu_value
        lst_pidstat_rd.append(dict_this_pidstat_rd)
        lst_pidstat_wr.append(dict_this_pidstat_wr)
        lst_total_timestamp.extend(dict_this_pidstat_rd.keys())

    # 将lst_total_timestamp进行排序
    lst_total_timestamp.sort()

    dict_pidstat_rd = {}
    for key in lst_total_timestamp:
        # contain_this_key = True
        # for dict_value in lst_pidstat_rd:
        #     if not key in dict_value.keys():
        #         contain_this_key = False
        # if contain_this_key:
        #     dict_pidstat_rd[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_rd if
        dict_pidstat_rd[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_rd if key in dict_value.keys()])

    dict_pidstat_wr = {}
    for key in lst_total_timestamp:
        # contain_this_key = True
        # for dict_value in lst_pidstat_wr:
        #     if not key in dict_value.keys():
        #         contain_this_key = False
        # if contain_this_key:
        #     dict_pidstat_wr[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_wr if
        dict_pidstat_wr[key] = reduce(lambda x, y: x + y, [dict_value[key] for dict_value in lst_pidstat_wr if key in dict_value.keys()])

    lst_datas = [dict_pidstat_rd, dict_pidstat_wr]
    lst_color = [u"西红柿红", u"苍蓝"]
    lst_tags = [u"storm Disk Read/s", u"storm Disk Write/s"]
    xlabel = u"时间"
    ylabel = u"Disk IO 速率（KB）"
    title = u"Disk IO 速率（KB/S）"
    print_with_data(lst_datas, lst_color, lst_tags, xlabel, ylabel, title)


"""
  CPU分析
"""
def analyze_of_cpu():

    lst_pidstat_cpu = []
    # 总体的timestamp的lst
    lst_total_timestamp = []
    for dict_pidstat_data in report_data.pidstat_data:
        lst_pidstat_timestamp = dict_pidstat_data["TIME"]
        lst_pidstat_cpu_value = dict_pidstat_data["CPU"]
        lst_pidstat_tid = dict_pidstat_data["TID"]
        dict_this_pidstat_cpu = {}
        for i in xrange(len(lst_pidstat_timestamp)):
            if lst_pidstat_tid[i] == '0':
                timestamp = long(lst_pidstat_timestamp[i])
                cpu_value = float(lst_pidstat_cpu_value[i])
                # print timestamp, lst_pidstat_tid[i], cpu_value
                dict_this_pidstat_cpu[timestamp] = cpu_value
                # print timestamp, cpu_value
        lst_pidstat_cpu.append(dict_this_pidstat_cpu)
        lst_total_timestamp.extend(dict_this_pidstat_cpu.keys())

    # 将lst_total_timestamp进行排序
    lst_total_timestamp.sort()

    dict_pidstat_cpu = {}
    for key in lst_total_timestamp:
        # contain_this_key = True
        # for dict_value in lst_pidstat_cpu:
        #     if not key in dict_value.keys():
        #         contain_this_key = False
        # if contain_this_key:
        #     dict_pidstat_cpu[key] = reduce(lambda x,y: x + y, [dict_value[key] for dict_value in lst_pidstat_cpu if key in dict_value.keys()])
        # 简单的将lst_pidstat_cpu中的同一timestamp的值相加即可
        dict_pidstat_cpu[key] = reduce(lambda x,y: x + y, [dict_value[key] for dict_value in lst_pidstat_cpu if key in dict_value.keys()])

    lst_vmstat_timestamp = report_data.vmstat_data["TIME"]
    lst_vmstat_cpu_us = report_data.vmstat_data["US"]
    lst_vmstat_cpu_sy = report_data.vmstat_data["SY"]
    dict_vmstat_cpu = {}
    for i in xrange(len(lst_vmstat_timestamp)):
        timestamp = long(lst_vmstat_timestamp[i])
        cpu_us = float(lst_vmstat_cpu_us[i])
        cpu_sy = float(lst_vmstat_cpu_sy[i])
        cpu_total = cpu_us + cpu_sy
        # print timestamp, cpu_total
        if not timestamp in dict_vmstat_cpu.keys():
            dict_vmstat_cpu[timestamp] = cpu_total * 32
        else:
            dict_vmstat_cpu[timestamp] = dict_vmstat_cpu[timestamp] + cpu_total * 32

    lst_datas = [dict_pidstat_cpu, dict_vmstat_cpu]
    lst_color = [u"西红柿红", u"苍蓝"]
    lst_tags = [u"storm CPU", u"system CPU"]
    xlabel = u"时间"
    ylabel = u"CPU占用率"
    title = u"CPU使用率"
    print_with_data(lst_datas, lst_color, lst_tags, xlabel, ylabel, title)


"""
  画图函数
"""
def print_with_data(lst_datas, lst_color, lst_tags, xlabel, ylabel, title):
    get_statistic_with_data(lst_datas, lst_tags)
    _, ax = plt.subplots()
    ax.set_xlabel(xlabel, fontproperties='SimHei', fontsize=15)
    ax.set_ylabel(ylabel, fontproperties='SimHei', fontsize=15)
    ax.set_title(title, fontproperties='SimHei', fontsize=15)
    for i in xrange(len(lst_datas)):
        dict_data = lst_datas[i]
        lst_timestamp = dict_data.keys()
        lst_timestamp.sort()
        lst_value = [dict_data[x] for x in lst_timestamp]
        lst_x_value = [x - lst_timestamp[0] for x in lst_timestamp]
        tag = lst_tags[i]
        color = report_data.dict_color[lst_color[i]]
        ax.plot(
            lst_x_value,
            lst_value,
            color,
            linewidth = 3.5,
            label = tag
        )

    ax.legend(loc="upper right")
    plt.show()


"""
  统计数据
"""
def get_statistic_with_data(lst_data, lst_tags):
    for i in xrange(len(lst_data)):
        dict_data = lst_data[i]
        tag = lst_tags[i]
        lst_timestamp = dict_data.keys()
        lst_timestamp.sort()
        lst_value = [dict_data[x] for x in lst_timestamp]
        narray = numpy.array(lst_value)
        N = len(lst_value)
        max = narray.max()
        min = narray.min()
        mean = narray.mean()
        var = narray.var()
        larger_num = 0
        for value in lst_value:
            if value > mean:
                larger_num = larger_num + 1

        threshold = 0
        if "CPU" in tag:
            threshold = 3200
        elif "MEM" in tag:
            threshold = 100
        saturation_num = 0
        if threshold > 0:
            for value in lst_value:
                if value > threshold:
                    saturation_num = saturation_num + 1

        print "---------------- 统计信息如下 -------------------"
        print u"%s的平均值为：%s，最大值为：%s，最小值为：%s, 方差为 %s, 饱和时长为 %s，运行总时长为 %s s, 其中大于平均值的时长为 %s s" % ( \
            tag, mean, max, min, var, saturation_num, N, larger_num)
        print "-------------- 统计信息打印完毕 -----------------"






""""
  预处理，将数据读入，并格式化
"""
def pre_process_data(path=cfg_rtw.local_log_base_path):

    # pidstat日志处理
    lst_pidstat_logs = get_local_pidstat_logs(path)
    # print len(lst_pidstat_logs)
    for pidstat_log in lst_pidstat_logs:
        handle_pidstat_log(path, pidstat_log)
    # vmstat日志处理
    handle_vmstat_log(path)

    # nethogs日志处理
    handle_nethogs_log(path)


# 处理nethogs日志
def handle_nethogs_log(path=cfg_rtw.local_log_base_path):

    # 获取到该次用到的所有的pid
    lst_pidstat_logs = get_local_pidstat_logs(path)
    lst_pids = map(lambda x: x.replace("pidstat_storm_","").replace(".log",""), lst_pidstat_logs)

    nethogs_log_file = path + "nethogs.log"
    dict_data = {}
    with open(nethogs_log_file, 'r') as open_file:
        for line in open_file:
            lst_line = line.replace("\n","").split("\t")
            if len(lst_line) == 4:
                timestamp = lst_line[report_data.DICT_ITEM_NETHOGS_SORT["TIME"]].replace("[","").replace("]","")
                this_timestamp = long(timestamp)
                pid = lst_line[report_data.DICT_ITEM_NETHOGS_SORT["PID"]].split("/")[-2]
                if pid in lst_pids:
                    sent = lst_line[report_data.DICT_ITEM_NETHOGS_SORT["SENT"]]
                    receive = lst_line[report_data.DICT_ITEM_NETHOGS_SORT["RECEIVE"]]
                    if not this_timestamp in dict_data.keys():
                        dict_data[this_timestamp] = [pid, sent, receive, timestamp]
                    else:
                        lst_old = dict_data[this_timestamp]
                        lst_new = [pid, sent, receive, timestamp]
                        lst_new[1] = "%s" % (float(lst_new[1]) + float(lst_old[1]))
                        lst_new[2] = "%s" % (float(lst_new[2]) + float(lst_old[2]))
                        lst_new[3] = "%s" % (float(lst_new[3]) + float(lst_old[3]))

    # 排序
    lst_timestamp = dict_data.keys()
    lst_timestamp.sort()
    lst_value_sorts = []

    # 裁剪出有效的lst_timestamp
    if report_data.global_start_timestamp == None:
        lst_pidstat_logs = get_local_pidstat_logs(path)
        for pidstat_log in lst_pidstat_logs:
            handle_pidstat_log(path, pidstat_log)
            # handle_pidstat_log(path)
    lst_timestamp = [x for x in lst_timestamp if
                     x >= report_data.global_start_timestamp and x <= report_data.global_end_timestamp]

    lst_data_sorted = [dict_data[x] for x in lst_timestamp]
    for key in report_data.DICT_ITEM_NETHOGS_SORT.keys():
        sort = report_data.DICT_ITEM_NETHOGS_SORT[key]
        lst_value = [x[sort] for x in lst_data_sorted]
        report_data.nethogs_data[key] = lst_value



# 处理vmstat日志
def handle_vmstat_log(path=cfg_rtw.local_log_base_path):
    VMSTAT_LOG = path + "vmstat.log"
    dict_data = {}
    with open(VMSTAT_LOG, 'r') as open_file:
        for line in open_file:
            if "[" in line and "]" in line and not "---" in line and not "swpd" in line:
                line = line.replace("[","").replace("]","")
                while line[0] == " ":
                    line = line[1:]
                # print line
                line = line.replace("\n","").replace("\t", " ")
                while "  " in line:
                    line = line.replace("  ", " ")
                lst_line = line.split(" ")
                if len(lst_line) >= report_data.DICT_ITEM_VMSTAT_SORT["TIME"]:
                    # print lst_line
                    this_timestamp = long(lst_line[report_data.DICT_ITEM_VMSTAT_SORT["TIME"]])
                    dict_data[this_timestamp] = lst_line

    # 排序
    lst_timestamp = dict_data.keys()
    lst_timestamp.sort()
    lst_value_sorts = []

    # 裁剪出有效的lst_timestamp
    if report_data.global_start_timestamp == None:
        lst_pidstat_logs = get_local_pidstat_logs(path)
        for pidstat_log in lst_pidstat_logs:
            handle_pidstat_log(path, pidstat_log)
        # handle_pidstat_log(path)
    lst_timestamp = [x for x in lst_timestamp if x >= report_data.global_start_timestamp and x <= report_data.global_end_timestamp]

    lst_data_sorted = [dict_data[x] for x in lst_timestamp]
    for key in report_data.DICT_ITEM_VMSTAT_SORT.keys():
        sort = report_data.DICT_ITEM_VMSTAT_SORT[key]
        lst_value = [x[sort] for x in lst_data_sorted]
        report_data.vmstat_data[key] = lst_value
        # print "key", key, "value", lst_value


# 获取pidstat日志
def get_local_pidstat_logs(path):
    lst_pidstat_logs = []
    for file in os.listdir(path):
        if "pidstat_storm_" in file:
            if os.path.isfile(os.path.join(path, file)):
                lst_pidstat_logs.append(file)
    # print lst_pidstat_logs
    return lst_pidstat_logs




# 处理pidstat日志
def handle_pidstat_log(path=cfg_rtw.local_log_base_path, pidstat_log="pidstat.log"):
    if report_data.pidstat_analysed < len(get_local_pidstat_logs(path)):
        report_data.pidstat_analysed = report_data.pidstat_analysed + 1
        PIDSTAT_LOG = path + pidstat_log
        dict_data = {}
        # 读取文件内容
        with open(PIDSTAT_LOG, 'r') as open_file:
            for line in open_file:
                # print line
                if len(line) > 10 and not "Linux" in line and not "Time" in line:
                    while "  " in line:
                        line = line.replace("  ", " ")
                    lst_line = line.replace("\n", "").split(" ")
                    this_time_stamp = long(lst_line[report_data.DICT_ITEM_PIDSTAT_SORT["TIME"]])
                    if not this_time_stamp in dict_data:
                        dict_data[this_time_stamp] = []
                    dict_data[this_time_stamp].append(lst_line)
        # 排序
        lst_timestamp = dict_data.keys()
        lst_timestamp.sort()
        lst_value_sorts = []

        if report_data.global_start_timestamp == None:
            if len(lst_timestamp) > 0:
                report_data.global_start_timestamp = lst_timestamp[0]
                report_data.global_end_timestamp = lst_timestamp[-1]
        else:
            if len(lst_timestamp) > 0:
                report_data.global_start_timestamp = lst_timestamp[0] if lst_timestamp[0] < report_data.global_start_timestamp else report_data.global_start_timestamp
                report_data.global_end_timestamp = lst_timestamp[-1] if lst_timestamp[-1] > report_data.global_end_timestamp else report_data.global_end_timestamp

        lst_data_sorted = [dict_data[x] for x in lst_timestamp]
        lst_data_sorted = extend_list(lst_data_sorted)
        # 生成一个pidstat_data的dictionary，并加入到pidstat的list中
        dic_of_this_log = {}
        for key in report_data.DICT_ITEM_PIDSTAT_SORT.keys():
            sort = report_data.DICT_ITEM_PIDSTAT_SORT[key]
            lst_value = [x[sort] for x in lst_data_sorted]
            dic_of_this_log[key] = lst_value
            # if key == "TID" or key == "TIME" or key == "CSWCH/S":
            #     print "key", key, "value", lst_value
        report_data.pidstat_data.append(dic_of_this_log)


# 将dictionary展开
def extend_list(lst_value):
    lst_result = []
    for sub_lst in lst_value:
        lst_result.extend(sub_lst)
    return lst_result


if __name__ == "__main__":

    """"
      预处理，将数据读入，并格式化
    """
    # pre_process_data()
    pre_process_data(cfg_rtw.local_log_base_path)

    """
      CPU分析
    """
    analyze_of_cpu()

    """
      内存分析
    """
    analyze_of_mem()

    """
      上下文切换分析
    """
    analyze_of_cs()

    """
      Disk IO分析
    """
    analyze_of_DiskIO()

    """
      Net IO分析
    """
    analyze_of_NetIO()

    """
      系统上下文切换分析
    """

