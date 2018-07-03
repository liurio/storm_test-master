# -*-coding:utf-8-*-
from tools.time_tools import get_this_time
import os, time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# 按照规定样式打印log
def log_and_stdout(log_content):
    print "[%s] - [%s]" % (get_this_time(), log_content)


# # 读取已经存到本地的log，过滤出其中含有时间度量的log，并切分成规定格式的list
# def get_formatted_time_log_list():
#     result_list = None
#     if YITA_MEA_GLOBAL_VAL.SHOULD_READ_LOGS_FROM_FILE:
#         with open(YITA_MEA_GLOBAL_VAL.LOG_PATH) as openFIle:
#             file_lines = []
#             # 删除上一次的formmatted_log
#             if not os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH):
#                 os.makedirs(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH)
#             if os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH + "formatted_log_lists.csv"):
#                 os.remove(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH + "formatted_log_lists.csv")
#
#             for line in openFIle:
#                 if YITA_MEA_GLOBAL_VAL.SYMBOL_OF_TIME_MEASUREMENT in line and YITA_MEA_GLOBAL_VAL.SYMBOL_OF_MEASUREMENT in line:
#                     file_lines.append(format_each_line(line.replace("\n","")))
#
#                 # 每5000条写一次磁盘
#                 if len(file_lines) >= 50000:
#                     add_lines_to_csv_file(file_lines, YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, "formatted_log_lists.csv")
#                     del file_lines[:]
#
#             # 循环结束，将未放入的数据放入文件中
#             add_lines_to_csv_file(file_lines,YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, "formatted_log_lists.csv")
#
#
# # 格式化需要处理的原始的每一行
# def format_each_line(line):
#     YITA_MEA_GLOBAL_VAL.CNST_TIME_GLOBAL_COUNT += 1
#     list_each_line = line.replace("\n","").split("||")
#     return [
#         YITA_MEA_GLOBAL_VAL.CNST_TIME_GLOBAL_COUNT,                                       # 序号
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_HOST_IP],                              # IP
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_THREAD].split("]")[0].split("[")[1],   # thread
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_MODEL_NAME],                            # 模块
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_HIERARCHY],                             # 日志层级
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_CLSS_NAME],                             # 所属类
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_FUC_NAME],                              # 所属方法
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_PURPOSE],                               # 所属功能
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_TIME_KIND],                             # 时间类型
#         list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_TIMESTAMP],                             # 时间戳
#         get_time_from_timestamp(list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_TIMESTAMP]),    # 时间
#         "|".join([line for line in list_each_line if "result" in line]),                 # result
#         "|".join([line for line in list_each_line[YITA_MEA_GLOBAL_VAL.SORT_OF_OTHER_BEGIN:] if not "result" in line])
#             ]
#
#
# # 将时间戳处理为时间
# def get_time_from_timestamp(timestamp):
#     return time.strftime("-%H:%M:%S", time.localtime(long(timestamp) / 1000)) + "." + timestamp[-3:] + "-"
#
#
# # 将list中的内容追加到csv文件中取
# def add_lines_to_csv_file(file_lines, base_path, file_name):
#     full_name = (base_path + file_name.replace(":", "_").replace(".csv","") + ".csv").replace("\\", "/").replace(" ", "_")
#     with open(full_name, 'a') as openFile:
#         for lst in file_lines:
#             # print lst
#             try:
#                 openFile.write(u",".join(str(i) for i in lst) + u"\n")
#             except UnicodeEncodeError:
#                 print lst
#
#     time.sleep(0.1)
#
#
# """
#   第二部分：格式化日志拆分
# """
# # 格式化日志拆分
# def split_formatted_log_to_pieces():
#     if YITA_MEA_GLOBAL_VAL.SHOULD_SPLIT_LOG_FROM_FORMATTED_LOGS:
#
#         # 删除所有的中间文件，除了formatted_log_lists.csv
#         files = os.listdir(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH)
#         for file in files:
#             if not "formatted_log_lists.csv" in file:
#                 os.remove(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH + file)
#
#         # 定义一个用来存放分割后的数据的dictionary
#         dict_result_formatted_logs = {
#             "CLIENT" : [],
#             "MASTER" : [],
#             "SLAVE" : {}
#         }
#
#         # 遍历测试环境的所有主机，在slave中创建该host对应的dictionary
#         for HOST in YITA_MEA_GLOBAL_VAL.DEV_HOSTS:
#             dict_result_formatted_logs["SLAVE"][HOST] = {}
#
#         # 正式开始切分数据，首先按照模块进行切分
#         print "---- 开始切分数据 ----"
#         # for line in lst_all_time_logs:
#         with open(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH + "formatted_log_lists.csv",'r') as openFile:
#             for this_line in openFile:
#                 line = this_line.replace("\n","").split(",")
#                 this_module = line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_MODULE].upper()
#                 if this_module == "CLIENT":
#                     dict_result_formatted_logs["CLIENT"].append(line)
#
#                     # 如果列表中的数量大于10000，则保存一次
#                     if len(dict_result_formatted_logs["CLIENT"]) >= 10000:
#                         add_lines_to_csv_file(len(dict_result_formatted_logs["CLIENT"]), YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, "Client_formatted_logs.csv")
#                         del dict_result_formatted_logs["CLIENT"][:]
#
#                 elif this_module == "MASTER" :
#                     dict_result_formatted_logs["MASTER"].append(line)
#
#                     # 如果列表中的数量大于10000，则保存一次
#                     if len(dict_result_formatted_logs["MASTER"]) >= 10000:
#                         add_lines_to_csv_file(dict_result_formatted_logs["MASTER"], YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, "Master_formatted_logs.csv")
#                         del dict_result_formatted_logs["MASTER"][:]
#
#                 else:
#                     this_host = line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_IP]
#                     dict_result_formatted_logs["SLAVE"][this_host]
#                     this_thread = line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_THREAD]
#                     # print "---查看拆分过程", this_host, this_thread
#                     if dict_result_formatted_logs["SLAVE"][this_host].has_key(this_thread):
#                         dict_result_formatted_logs["SLAVE"][this_host][this_thread].append(line)
#
#                         # 如果列表中的数量大于10000，则保存一次
#                         if len(dict_result_formatted_logs["SLAVE"][this_host][this_thread]) > 10000:
#                             add_lines_to_csv_file(dict_result_formatted_logs["SLAVE"][this_host][this_thread], YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, ("Slave_formatted_logs_%s_%s.csv" % (this_host, this_thread)))
#                             del dict_result_formatted_logs["SLAVE"][this_host][this_thread][:]
#
#                     else:
#                         dict_result_formatted_logs["SLAVE"][this_host][this_thread] = [line]
#
#         # 循环结束，将还未放入文件的数据都放入文件中
#         add_lines_to_csv_file(dict_result_formatted_logs["CLIENT"], YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, "Client_formatted_logs.csv")
#         add_lines_to_csv_file(dict_result_formatted_logs["MASTER"], YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, "Master_formatted_logs.csv")
#         for host in dict_result_formatted_logs["SLAVE"].keys():
#             for thread in dict_result_formatted_logs["SLAVE"][host]:
#                 add_lines_to_csv_file(dict_result_formatted_logs["SLAVE"][host][thread], YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH, ("Slave_formatted_logs_%s_%s.csv" % (host, thread)))
#
#
# """
#   第三部分：找出时间对关系
# """
# # 对于每一个单独的csv文件，解析其中的时间对，并写入到文件中
# def analyse_all_csv_file_and_generate_time_pair():
#     if YITA_MEA_GLOBAL_VAL.SHOULD_ANALYSE_CSV_FILE:
#         # 遍历文件夹，找出所有的csv文件列表
#         csv_files = os.listdir(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH)
#         for csv_file in csv_files:
#             if "formatted_log_lists.csv" in csv_file:
#                 csv_files.remove(csv_file)
#
#         # 开始遍历csv文件，进行分析
#         for csv_file in csv_files:
#             analyse_single_csv_file(csv_file)
#
#
# # 分析每一个单独的csv_file的时间对
# def analyse_single_csv_file(csv_file):
#
#     # 创建两个list，分别用来存储start_time和end_time
#     lst_unhandled_for_start = []
#     lst_unhandled_for_end   = []
#     # 创建一个list, 用来存储 mark_time
#     lst_unhandled_for_mark = []
#
#     # 创建一个list，用来存储所有的 time pair
#     lst_time_pair_for_thie_csv = []
#
#     # 首先，将文件内容读取出来
#     if not os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH):
#         os.makedirs(YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH)
#
#     with open(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH + csv_file, 'r') as openFile:
#         for line in openFile.readlines():
#             # 将每一行用","切分为list
#             lst_this_line = line.replace("\n","").split(",")
#             this_time_kind = lst_this_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIME_KIND].upper()
#             # 根据时间类型来划分该line应该放入到哪一个list中
#             if this_time_kind == "START_TIME":
#                 lst_unhandled_for_start.append(lst_this_line)
#             elif this_time_kind == "END_TIME":
#                 lst_unhandled_for_end.append(lst_this_line)
#             elif this_time_kind == "MARK_TIME":
#                 lst_unhandled_for_mark.append(lst_this_line)
#
#             # 如果end_lst中有数据，则要开始生成time pair
#             if len(lst_unhandled_for_end) > 0:
#                 # 循环 end_lst 进行排查
#                 # for end_line in lst_unhandled_for_end:
#                 for i in xrange(len(lst_unhandled_for_end)-1, -1, -1):
#                     end_line = lst_unhandled_for_end[i]
#                     # 再循环 start_lst 进行比对
#                     for j in xrange(len(lst_unhandled_for_start)-1, -1, -1):
#                     # for start_line in lst_unhandled_for_start:
#                         start_line = lst_unhandled_for_start[j]
#                         # 判断两行属于同一个记录组
#                         if this_two_lines_are_pairs(start_line, end_line):
#                             # 生成一个time_pair的list
#                             this_time_pair = generate_time_pair_from_two_lines(start_line, end_line)
#                             # 此时，循环一下该文件中的mark_time，找出其中的mark_time
#                             for k in xrange(len(lst_unhandled_for_mark)-1, -1, -1):
#                             # for mark_line in lst_unhandled_for_mark:
#                                 mark_line = lst_unhandled_for_mark[k]
#                                 # 如果该mark_time属于这个time_pair
#                                 if this_mark_time_belong_this_time_pair(this_time_pair, mark_line):
#                                     # 将该mark_line的信息加入到该time_pair中
#                                     time_pair_append_mark_time(this_time_pair, mark_line)
#                                     del lst_unhandled_for_mark[k]
#                             # 将生成的 time pair 放入time pair的数据组中
#                             lst_time_pair_for_thie_csv.append(this_time_pair)
#                             # 将该start_line从start_line的list移除，将end_line从end_line的list移除
#                             # lst_unhandled_for_end.remove(end_line)
#                             # lst_unhandled_for_start.remove(start_line)
#                             del lst_unhandled_for_end[i]
#                             del lst_unhandled_for_start[j]
#                             # 找到了time pair，就需要先跳出循环
#                             break
#
#         # 循环完毕， 打印列表中剩余的数据量
#         # 判断有数据剩余，则打印该数据出来
#         if len(lst_unhandled_for_end) > 0 or len(lst_unhandled_for_start):
#             print "---- 该文件已经循环完毕，打印列表中剩余的数据量 ----"
#             print "lst_unhandled_for_end中的数据量为：", len(lst_unhandled_for_end)
#             for line in lst_unhandled_for_end:
#                 print line
#             print "lst_unhandled_for_start中的数据量为：", len(lst_unhandled_for_start)
#             for line in lst_unhandled_for_start:
#                 print line
#
#
#         # 循环完毕，将生成的time_pair的 list 放入到本地文件中
#         save_list_to_csv(lst_time_pair_for_thie_csv, YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH, csv_file.replace(".csv",""))
#
#
# # 判断两行属于同一个时间pair
# def this_two_lines_are_pairs(start_line, end_line):
#
#     start_host = start_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_IP]
#     start_thread = start_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_THREAD]
#     start_module = start_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_MODULE]
#     start_hierarchy = start_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_HIERARCHY]
#     start_purpose = start_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_PURPOSE]
#     start_other = start_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_OTHER]
#
#     end_host = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_IP]
#     end_thread = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_THREAD]
#     end_module = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_MODULE]
#     end_hierarchy = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_HIERARCHY]
#     end_purpose = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_PURPOSE]
#     end_other = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_OTHER]
#
#     return (start_host == end_host) and (start_thread == end_thread) and \
#             (start_module == end_module) and (start_hierarchy == end_hierarchy) and \
#             (start_purpose == end_purpose) and (start_other == end_other)
#
#
# # 从两行生成一个time pair line
# def generate_time_pair_from_two_lines(start_line, end_line):
#     start_line_copy = start_line[:]
#     # print "start_line_copy:", ",".join(start_line_copy)
#     end_timekind = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIME_KIND]
#     end_timestamp = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIMESTAMP]
#     end_time = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIME]
#     end_sort = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_SORT]
#     end_result = end_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_RESULT]
#     time_during = "%s" % (int(end_timestamp) - int(start_line_copy[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIMESTAMP]))
#     # 需要增加的lst
#     extend_lst = [end_timekind, end_timestamp, end_time, end_sort, end_result, time_during]
#
#     # print extend_lst
#     # print start_line_copy[0:11].extend(extend_lst)
#
#     result_lst = start_line_copy[0:11]
#     for content in extend_lst:
#         result_lst.append(content)
#
#     for content in start_line_copy[11:]:
#         result_lst.append(content)
#
#     return result_lst
#
#
# # 判断这个markline是否属于这个time pair
# def this_mark_time_belong_this_time_pair(this_time_pair, mark_line):
#     start_time = int(this_time_pair[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_TIMESTAMP])
#     end_time = int(this_time_pair[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIMESTAMP])
#     mark_time = int(mark_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIMESTAMP])
#
#     return (start_time < mark_time) and (end_time > mark_time)
#
#
# # 将mark_line的相关信息加入到time_pair中
# def time_pair_append_mark_time(this_time_pair, mark_line):
#     append_list = ["mark_time", mark_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIMESTAMP], mark_line[YITA_MEA_GLOBAL_VAL.FORMATTED_SORT_OF_TIME]]
#     for content in append_list:
#         this_time_pair.append(content)
#
#     return content
#
#
# # 将list保存到csv文件中
# def save_list_to_csv(list_all, base_path, file_name):
#     if len(list_all) > 0:
#         # 把空格去掉，是为了防止文件名出错
#
#         file_path = (base_path + file_name.replace(":","_") + ".csv").replace("\\","/").replace(" ","_")
#         while " " in file_path:
#             file_path.replace(" ", "")
#
#         print "----文件名称为：", file_path
#         # create_file_if_not_exists(file_path)
#         with open(file_path, 'w+') as csv_file:
#             for lst in list_all:
#                 csv_file.write(",".join(str(i) for i in lst ) + "\n")
#             # csv_file.writelines(",".join(list_all))
#             # writer = csv.writer(csv_file)
#             # writer.writerows(list_all)
#
#
# """
#   第四部分：初步统计开始
# """
# # 第四部分入口方法
# def get_first_caculate_data():
#     if YITA_MEA_GLOBAL_VAL.SHOULD_GET_CACULATE_DATA_FROM_MID:
#
#         # 把上一次生成的文件清掉
#         if os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH + "first_caculate_data.csv"):
#             log_and_stdout("清理上一次的初步分析文件 - 开始")
#             os.remove(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH + "first_caculate_data.csv")
#             log_and_stdout("清理上一次的初步分析文件 - 结束")
#
#         # 第四步，获取total_run_time
#         log_and_stdout("获取该数据量下，JOB运行的总时长 - 开始")
#         # print "结果：该数据量下，JOB运行的总时长为 %s 秒" % get_the_whole_running_time()
#         log_and_stdout("获取该数据量下，JOB运行的总时长 - 结束")
#
#         # 第五步，获取所有的 readfile 的总时长
#         log_and_stdout("获取每个线程获取read_file, gen_kv的总时长 - 开始")
#         get_read_files_total_time_per_thread()
#         log_and_stdout("获取每个线程获取read_file, gen_kv的总时长 - 结束")
#
#         # 第六步，获取所有的execute的总时长
#         log_and_stdout("获取每个线程的execute的总时长 - 开始")
#         get_execute_total_time_per_thread()
#         log_and_stdout("获取每个线程的execute的总时长 - 结束")
#
#         # 第七步，获取所有的网络传输的时长
#         log_and_stdout("获取每个线程的网络传输总时长 - 开始")
#         get_net_push_time_per_thread()
#         log_and_stdout("获取每个线程的网络传输总时长 - 结束")
#
#         # 第八步，获取binProcessingTask中generate_KV_pair的总时长
#         log_and_stdout("获取pushProcessingTask中generate_KV_pair的总时长 - 开始")
#         # get_gen_kv_total_time_per_thread()
#         log_and_stdout("获取pushProcessingTask中generate_KV_pair的总时长 - 结束")
#
#         # 第八步，获取所有的空闲时长和总时长
#         log_and_stdout("获取每个线程的空闲时长和总时长 - 开始")
#         get_thread_free_and_total_time()
#         log_and_stdout("获取每个线程的空闲时长和总时长 - 结束")
#
#
# # 获取该数据量下，JOB运行的总时长
# def get_the_whole_running_time():
#
#     total_cost_time = None
#
#     choice_1 = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + "Client_formatted_logs.csv"
#     choice_2 = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + "Master_formatted_logs.csv"
#
#     final_file_name = choice_1 if os.path.exists(choice_1) else choice_2
#
#     print "~~~~final_file_name=%s" % final_file_name
#
#     if os.path.exists(final_file_name):
#         with open(final_file_name, 'r') as openFile:
#             for line in openFile:
#                 this_line_list = line.replace("\n","").split(",")
#                 start_timestamp = this_line_list[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_TIMESTAMP]
#                 end_timestamp = this_line_list[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIMESTAMP]
#                 YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP = start_timestamp if YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP == None or int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP)  > int(start_timestamp) else YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP
#                 YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP = end_timestamp if YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP == None or int(YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP) < int(end_timestamp) else YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP
#     else:
#         YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP = 0
#         YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP = 0
#
#     total_cost_time = int(YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP) - int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP)
#     add_first_caculate_data_to_file([["all_hosts", "all_threads", u"JOB总运行时长", total_cost_time],])
#     return total_cost_time
#
#
# # 将初步统计结果加入到初步统计输出文件中
# def add_first_caculate_data_to_file(lst_line):
#     if not os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH):
#         os.makedirs(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH)
#     add_lines_to_csv_file(lst_line, YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH, "first_caculate_data.csv")
#
# # 获取每个线程中从文件系统中，读取read_files的总时长
# def get_read_files_total_time_per_thread():
#     # 遍历文件夹，找出所有的slave中flowThread的线程
#     csv_file_threads = get_all_flowthread_logs()
#
#     # 定义返回值的dictionary
#     lst_result = []
#
#     for csv_file in csv_file_threads:
#
#         full_file_path = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + csv_file
#         HOST_IP, Thread_name, total_read_file_time = get_total_time_of_certain_kind_in_file(full_file_path, "read_data_from_file")
#         _, _, total_pushProcessing_time = get_total_time_of_certain_kind_in_file(full_file_path, "PushProcessingTask_execute()")
#         lst_result.append([HOST_IP, Thread_name, "read_file_time", total_read_file_time])
#         lst_result.append([HOST_IP, Thread_name, "push_processing_time", total_pushProcessing_time])
#         lst_result.append([HOST_IP, Thread_name, "gen_kv_time", str(int(total_pushProcessing_time) - int(total_read_file_time))])
#
#     add_first_caculate_data_to_file(lst_result)
#
#
# # 获取每个线程的execute的总时长
# def get_execute_total_time_per_thread():
#     # 遍历文件夹，找出所有的slave中flowThread的线程
#     csv_file_threads = get_all_flowthread_logs()
#
#     lst_result = []
#
#     for csv_file in csv_file_threads:
#
#         full_file_path = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + csv_file
#
#         HOST_IP, Thread_name, total_execute_time = get_total_time_of_certain_kind_in_file(full_file_path, "BinProcessingTask_execute()")
#
#         lst_result.append([HOST_IP, Thread_name, "binProcessing_time", total_execute_time])
#
#     add_first_caculate_data_to_file(lst_result)
#
#
# # 找出所有记载slave的flowthread的线程
# def get_all_flowthread_logs():
#     # 遍历文件夹，找出所有的slave中flowThread的线程
#     csv_files = os.listdir(YITA_MEA_GLOBAL_VAL.CSV_FORMATTED_LOGS_PATH)
#     csv_file_threads = []
#     for csv_file in csv_files:
#         if ("Slave" in csv_file) and ("YITA_FlowThread" in csv_file):
#             csv_file_threads.append(csv_file)
#
#     return csv_file_threads
#
#
# # 获取特定种类的时间在特定文件中的总时长
# def get_total_time_of_certain_kind_in_file(file_name, log_key_word):
#     HOST_IP = None
#     Thread_name = None
#     total_read_file_time = 0
#     with open(file_name, 'r') as openFile:
#         for line in openFile:
#             this_split_lst = line.replace("\n", "").split(",")
#             # 获取 HOST_IP 和 Thread_name，用来生成数据返回值
#             if HOST_IP == None:
#                 HOST_IP = this_split_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_IP]
#                 Thread_name = this_split_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_THREAD]
#
#             # 判断该行是不是read_file时间
#             if log_key_word == this_split_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_PURPOSE]:
#                 start_time = int(this_split_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_TIMESTAMP])
#                 end_time = int(this_split_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIMESTAMP])
#                 this_long = end_time - start_time
#
#                 total_read_file_time += this_long
#
#                 # 计数用，用于统计平均时间
#                 if log_key_word == "read_data_from_file":
#                     YITA_MEA_GLOBAL_VAL.TOTAL_READ_DATA_FROM_FILE_NUM = YITA_MEA_GLOBAL_VAL.TOTAL_READ_DATA_FROM_FILE_NUM + 1
#
#
#     return HOST_IP, Thread_name, total_read_file_time
#
#
# # 得到每个线程的网络传输总时长
# def get_net_push_time_per_thread():
#     # 遍历文件夹，找出所有的slave中flowThread的线程
#     csv_file_threads = get_all_flowthread_logs()
#
#     lst_result = []
#     for csv_file in csv_file_threads:
#
#         full_file_path = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + csv_file
#
#         HOST_IP, Thread_name, total_net_push_timne = get_total_time_of_certain_kind_in_file(full_file_path, "FlushTask_execute()")
#         lst_result.append([HOST_IP, Thread_name, "net_push_time", total_net_push_timne])
#
#     add_first_caculate_data_to_file(lst_result)
#
#
# # 获取每个线程的空闲时长和总时长
# def get_thread_free_and_total_time():
#
#     csv_file_threads = get_all_flowthread_logs()
#     lst_result = []
#     for csv_file in csv_file_threads:
#         full_file_path = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + csv_file
#         # 计算总时长
#         Host_ip, thread_name, thread_total_time = get_thread_total_time_from_file(full_file_path)
#         lst_result.append([Host_ip, thread_name, "total_run_time", thread_total_time])
#         # 计算总运行时间
#         Host_ip, thread_name, total_execute_time = get_thread_total_exec_time_from_file(full_file_path)
#         lst_result.append([Host_ip, thread_name, "busy_time",total_execute_time])
#
#
#     add_first_caculate_data_to_file(lst_result)
#
#
# # 获取该flowthread的总运行时长
# def get_thread_total_time_from_file(file_path):
#     start_time = None
#     end_time = None
#     HOST_IP = None
#     Thread_name = None
#     with open(file_path, 'r') as openFile:
#         for line in openFile:
#             this_line_lst = line.replace("\n","").split(",")
#             if "99" == this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_HIERARCHY]:
#                 if HOST_IP == None:
#                     HOST_IP = this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_IP]
#                     Thread_name = this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_THREAD]
#                 start_time = this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_TIMESTAMP] if (start_time == None) or (int(start_time) > int(this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_TIMESTAMP])) else start_time
#                 end_time = this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIMESTAMP] if (end_time == None) or (int(end_time) < int(this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIMESTAMP])) else end_time
#
#     return HOST_IP, Thread_name, (int(end_time) - int(start_time))
#
#
# # 获取该flowthread的总execute_time
# def get_thread_total_exec_time_from_file(file_path):
#     total_time = 0
#     HOST_IP = None
#     Thread_name = None
#     with open(file_path, 'r') as openFile:
#         for line in openFile:
#             this_line_lst = line.replace("\n", "").split(",")
#             if HOST_IP == None:
#                 HOST_IP = this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_IP]
#                 Thread_name = this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_THREAD]
#
#             if "99" == this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_HIERARCHY]:
#                 total_time += int(this_line_lst[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIME_DURING])
#
#     return HOST_IP, Thread_name, total_time
#
#
# """
#   第五部分：画出饼图
# """
# # 第五部分入口
# # 画出各flowThread的运行占比总图
# def print_each_flowthread_run_rate():
#
#     if YITA_MEA_GLOBAL_VAL.SHOULD_PRINT_THE_PIE_PIC:
#         # 将之前的画图文件删除掉
#         print "图像文件存储目录为：%s" % YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC
#         if os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC):
#             pic_files = os.listdir(YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC)
#             for picture in pic_files:
#                 os.remove(YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC + picture)
#
#         dictinary_analyse_data = {}
#         # 读出数据
#         with open(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH + "first_caculate_data.csv", "r") as openFile:
#             for line in openFile:
#                 lst_split_line = line.replace("\n","").split(",")
#                 HOST = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_HOST]
#                 THREAD = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_THREAD]
#                 TITLE = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_TITLE]
#                 TIME_DURING = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_TIME_DURING]
#
#                 if not HOST in dictinary_analyse_data.keys():
#                     dictinary_analyse_data[HOST] = {}
#                 if not THREAD in dictinary_analyse_data[HOST].keys():
#                     dictinary_analyse_data[HOST][THREAD] = {}
#                 dictinary_analyse_data[HOST][THREAD][TITLE] = TIME_DURING
#
#         # 遍历host与thread进行绘图
#         for host in dictinary_analyse_data.keys():
#             if "all_hosts" != host:
#                 for thread in dictinary_analyse_data[host].keys():
#                     print "开始画IP为：%s，thread为：%s的flowThread的运行情况的饼图了" % (host, thread)
#                     dict_thread = dictinary_analyse_data[host][thread]
#                     read_time = int(dict_thread["read_file_time"])
#                     kv_time = int(dict_thread["gen_kv_time"])
#                     net_push_time = int(dict_thread["net_push_time"])
#                     binProcessing_time = int(dict_thread["binProcessing_time"])
#                     pushProcessing_time = int(dict_thread["push_processing_time"])
#                     other_time = int(dict_thread["busy_time"]) - binProcessing_time - net_push_time - pushProcessing_time
#                     free_time = int(dict_thread["total_run_time"]) - int(dict_thread["busy_time"])
#                     labels = [u"磁盘读-%sms" % read_time,
#                               u"产生KV-%sms" % kv_time,
#                               u"网络传输-%sms" % net_push_time,
#                               u"处理数据-%sms" % binProcessing_time,
#                               u"其他任务-%sms" % other_time ,
#                               u"空闲时间-%sms" % free_time]
#                     fracs = [read_time, kv_time, net_push_time, binProcessing_time, other_time, free_time]
#                     title = u"IP为：%s，thread为：%s的flowThread的运行情况\n" % (host, thread)
#                     pic_name = u"时间分配_%s-%s.jpg" % (host.split(".")[-1], thread.split(":")[-1])
#                     print_a_pie_pic(labels, fracs, title, pic_name)
#
#
# # 画出饼图
# def print_a_pie_pic(labels, fracs, title, pic_name):
#
#     if not os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC):
#         os.makedirs(YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC)
#
#     # labels = ['A', 'B', 'C', 'D']
#     # fracs = [15, 30.55, 44.44, 10]
#     # explode = [0, 0.1, 0, 0]  # 0.1 凸出这部分，
#     # print labels
#     # print fracs
#     plt.axes(aspect=1)  # set this , Figure is round, otherwise it is an ellipse
#     autopct = '%1.1f%%'
#
#     patches, l_text, p_text = plt.pie(x=fracs,
#                                       labels=labels,
#                                       # explode=explode,
#                                       autopct=autopct,
#                                       shadow=False,
#                                       labeldistance=1.1,
#                                       startangle=90,
#                                       pctdistance=0.6
#                                       )
#     for t in l_text:
#         t.set_size = (15)
#         t.set_properties='SimHei'
#     for t in p_text:
#         t.set_size = (15)
#     # 设置x，y轴刻度一致，这样饼图才能是圆的
#     plt.axis('equal')
#     print_title = plt.title(title)
#     print_title.set_fontsize(fontsize=15)
#     picture_name =  YITA_MEA_GLOBAL_VAL.CSV_THREAD_PIE_PIC + pic_name
#     # print picture_name
#     # plt.savefig(picture_name)
#     print u"---- 保存图片为: " + picture_name
#     plt.savefig(picture_name)
#     # plt.show()
#     plt.close()
#
#
# """
#   第六部分：将所有线程的数据求和，并画出总的饼图
# """
# # 第六部分入口
# # 将所有线程的数据求和，并画出总的饼图
# def sum_every_thread_and_print_a_pie_pic():
#
#     if YITA_MEA_GLOBAL_VAL.SHOULD_PRINT_THE_TOTAL_PIE_PIC:
#         dictinary_analyse_data = {}
#
#         # 读出数据
#         with open(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH + "first_caculate_data.csv", "r") as openFile:
#             for line in openFile:
#                 lst_split_line = line.replace("\n","").split(",")
#                 HOST = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_HOST]
#                 THREAD = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_THREAD]
#                 TITLE = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_TITLE]
#                 TIME_DURING = lst_split_line[YITA_MEA_GLOBAL_VAL.FC_SORT_OF_TIME_DURING]
#
#                 if "all_hosts" == HOST:
#                     YITA_MEA_GLOBAL_VAL.YITA_JOB_WHOLE_TIME = TIME_DURING
#
#                 if not HOST in dictinary_analyse_data.keys():
#                     dictinary_analyse_data[HOST] = {}
#                 if not THREAD in dictinary_analyse_data[HOST].keys():
#                     dictinary_analyse_data[HOST][THREAD] = {}
#                 dictinary_analyse_data[HOST][THREAD][TITLE] = TIME_DURING
#
#         total_read_time = 0
#         total_kv_time = 0
#         total_net_push_time = 0
#         total_binProcessing_time = 0
#         total_pushProcessing_time = 0
#         total_other_time = 0
#         total_free_time = 0
#         total_flowThread_run_time = 0
#
#         # 遍历host与thread进行绘图
#         for host in dictinary_analyse_data.keys():
#             if "all_hosts" != host:
#                 for thread in dictinary_analyse_data[host].keys():
#                     dict_thread = dictinary_analyse_data[host][thread]
#                     read_time = int(dict_thread["read_file_time"])
#                     kv_time = int(dict_thread["gen_kv_time"])
#                     net_push_time = int(dict_thread["net_push_time"])
#                     binProcessing_time = int(dict_thread["binProcessing_time"])
#                     pushProcessing_time = int(dict_thread["push_processing_time"])
#                     other_time = int(
#                         dict_thread["busy_time"]) - binProcessing_time - net_push_time - pushProcessing_time
#                     free_time = int(dict_thread["total_run_time"]) - int(dict_thread["busy_time"])
#
#                     total_read_time += read_time
#                     total_kv_time += kv_time
#                     total_net_push_time += net_push_time
#                     total_binProcessing_time += binProcessing_time
#                     total_pushProcessing_time += pushProcessing_time
#                     total_other_time += other_time
#                     total_free_time += free_time
#                     total_flowThread_run_time  = int(dict_thread["total_run_time"]) if int(dict_thread["total_run_time"]) > total_flowThread_run_time else total_flowThread_run_time
#
#
#
#         # 打印出该主机的所有线程总的运行情况
#         labels = [u"磁盘读-%sms" % total_read_time,
#                   u"产生KV-%sms" % total_kv_time,
#                   u"网络传输-%sms" % total_net_push_time,
#                   u"处理数据-%sms" % total_binProcessing_time,
#                   u"其他任务-%sms" % total_other_time,
#                   u"空闲时间-%sms" % total_free_time
#                   ]
#         fracs = [total_read_time, total_kv_time, total_net_push_time, total_binProcessing_time, total_other_time, total_free_time]
#         title = u"数据量为：%s的情况下的运行情况\n" % (YITA_MEA_GLOBAL_VAL.DATA_SCALE)
#         pic_name = u"数据量%s的WordCount情况.jpg" % YITA_MEA_GLOBAL_VAL.DATA_SCALE
#         print_a_pie_pic(labels, fracs, title, pic_name)
#
#         lst_line = [
#             [u"job总运行时长" , YITA_MEA_GLOBAL_VAL.YITA_JOB_WHOLE_TIME],
#             [u"磁盘读"   , total_read_time],
#             [u"产生KV"   , total_kv_time],
#             [u"网络传输" , total_net_push_time],
#             [u"处理数据" , total_binProcessing_time],
#             [u"其他任务" , total_other_time],
#             [u"空闲时间" , total_free_time],
#             [u"最大flowThread运行时长", total_flowThread_run_time],
#             [u"平均ReadFromFile时长", float(total_read_time)/ float(YITA_MEA_GLOBAL_VAL.TOTAL_READ_DATA_FROM_FILE_NUM),u"读取次数",YITA_MEA_GLOBAL_VAL.TOTAL_READ_DATA_FROM_FILE_NUM],
#             [u"平均产生KV对时长", float(total_kv_time) / float(YITA_MEA_GLOBAL_VAL.TOTAL_READ_DATA_FROM_FILE_NUM),u"读取次数",YITA_MEA_GLOBAL_VAL.TOTAL_READ_DATA_FROM_FILE_NUM]
#         ]
#
#         if os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH + "job_total_run_caculate.csv"):
#             os.remove(YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH + "job_total_run_caculate.csv")
#
#         add_lines_to_csv_file(lst_line, YITA_MEA_GLOBAL_VAL.CSV_FIRST_CACULATE_DATA_PATH, "job_total_run_caculate.csv")
#
#
# """
#   第七部分：打印一个slave中各flowThread的执行情况
# """
# # 第七部分入口
# # 打印一个slave中各flowThread的执行情况
# def print_details_in_one_slave_flowThread():
#
#     if not os.path.exists(YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC):
#         os.makedirs(YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC)
#     files = os.listdir(YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC)
#     if len(files) > 0 :
#         for file in files:
#             os.remove(YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC + file)
#
#
#     if YITA_MEA_GLOBAL_VAL.SHOULD_PRINT_THE_FLOWTHREAD_DETAIL:
#         file_paths = get_all_flowthread_logs()
#         # 遍历所有的slave节点，以单个slave为单位
#         for slave_host in YITA_MEA_GLOBAL_VAL.DEV_HOSTS:
#             # 临时跳过116与117主机
#             # if "116" not in slave_host and "117" not in slave_host and "118" not in slave_host and "119" not in slave_host:
#             dictionary_detail_of_this_slave = {}
#             # 找出该slave的所有的flowThread的细节
#             this_slave_files = [file_name for file_name in file_paths if slave_host in file_name]
#             for thread_file in this_slave_files:
#                 # 获取这个flowThread中的细节情况
#                 thread_name, dict_this_thread_detail = handle_the_thread_detail(thread_file)
#                 dictionary_detail_of_this_slave[thread_name] = dict_this_thread_detail
#             # 遍历完一个host的所有文件，则开始打印该host的flowThread的明细图
#             print_flowThread_details_in_one_host(slave_host, dictionary_detail_of_this_slave)
#
#
# # 将传入的threadfile转化为打印所需的信息
# def handle_the_thread_detail(thread_file):
#     print "---- 开始转换文件: %s ----" % thread_file
#     dictionary_result = {}
#     file_path = YITA_MEA_GLOBAL_VAL.CSV_MID_TIME_PAIR_PATH + thread_file
#     thread_name = None
#     with open(file_path, 'r') as openFile:
#         for line in openFile:
#             lst_split_line = line.replace("\n","").split(",")
#
#             # 获取该文件所属的thread_name
#             if thread_name == None:
#                 thread_name = lst_split_line[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_THREAD]
#
#             # 如果是需要展示的task，则需要处理
#             this_line_purpose = lst_split_line[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_PURPOSE]
#             if this_line_purpose in YITA_MEA_GLOBAL_VAL.SHOULD_DISPLAY_TASK.keys():
#                 start_time = lst_split_line[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_START_TIMESTAMP]
#                 end_time = lst_split_line[YITA_MEA_GLOBAL_VAL.TP_SORT_OF_END_TIMESTAMP]
#
#                 if not this_line_purpose in dictionary_result.keys():
#                     dictionary_result[this_line_purpose] = []
#
#                 dictionary_result[this_line_purpose].append({
#                     "start_time" : start_time,
#                     "end_time" : end_time
#                 })
#
#     return thread_name, dictionary_result
#
#
# # 打印一个slave上的所有的flowThread的执行细节
# def print_flowThread_details_in_one_host(slave_host, host_dictionary):
#
#     if YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP == None:
#         get_the_whole_running_time()
#
#     print "---- 开始画出%s主机的详细情况 ----" % slave_host
#     # 调整画图大小和分辨率
#     # plt.figure(figsize=(8, 8), dpi=80)
#
#
#     # plt.figure(figsize=(30, 30))
#     _, ax = plt.subplots()
#     # 建立调整后的x轴数据
#     print "~~~~查看参数-%s-%s-" % (YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP, YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP)
#     adj_x = range(0, int(YITA_MEA_GLOBAL_VAL.GLOBAL_END_TIMESTAMP) - int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP), 100)
#
#     # 设置x轴的刻度和文本
#     xticks = range(0, adj_x[-1] + 500, 500)
#     # xlabels = [get_time_from_timestamp('%s' % (value + int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP))) for value in xticks]
#     print "---- YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP = ", YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP
#     xlabels = ['%s' % (value + int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP)) for value in xticks]
#
#     ax.set_xticks(xticks)
#     ax.set_xticklabels(xlabels, rotation = 40)
#
#     # 将y轴刻度清空
#     # yticks = range(0, 34, 1)
#     # ylabels = ['%s' % (x - 3) for x in yticks]
#     # ax.set_yticklabels(ylabels)
#     # ax.set_yticklabels([])
#
#     # 设置x轴与y轴的说明
#     ax.set_xlabel(u"Job运行时间", fontproperties='SimHei', fontsize=15)
#     ax.set_ylabel(u"任 务 名 称", fontproperties='SimHei', fontsize=15)
#     title = u"IP为：%s的slave中FlowThread的运行情况:" % (slave_host)
#
#     # 遍历Slave中的所有的flowThread
#     # FlowThread_High = 4
#     FlowThread_High = 0
#     for thread_name in host_dictionary.keys():
#         NUM_FLOWTHREAD = int(thread_name.split(":")[-1])
#         print "---- 生成 %s 线程的数据, 开始, 高度为：%s ----" % (thread_name, FlowThread_High + NUM_FLOWTHREAD)
#         this_thread_dictionary = host_dictionary[thread_name]
#         for task in this_thread_dictionary.keys():
#             if "read_data_from_file" != task:
#                 print "---- 生成 %s 任务的数据1 ----" % task
#                 handled_thread_dictionary = combine_availabel_task_contents(this_thread_dictionary[task])
#                 this_thread_dictionary[task] = None
#                 for obj in handled_thread_dictionary:
#                     plot_x = [int(obj["start_time"]) - int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP),
#                               int(obj["end_time"]) - int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP)
#                               ]
#                     plot_y = [FlowThread_High + NUM_FLOWTHREAD, FlowThread_High + NUM_FLOWTHREAD]
#                     ax.plot(plot_x, plot_y, YITA_MEA_GLOBAL_VAL.SHOULD_DISPLAY_TASK[task], linewidth=YITA_MEA_GLOBAL_VAL.TIME_LINE_WIDTH)
#                 # 清空该lst, 释放内存
#                 handled_thread_dictionary = None
#         # print "---- 生成 read_data_from_file 任务的数据2 ----"
#         # for obj in combine_availabel_task_contents(this_thread_dictionary["read_data_from_file"]):
#         #     plot_x = [int(obj["start_time"]) - int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP),
#         #               int(obj["end_time"]) - int(YITA_MEA_GLOBAL_VAL.GLOBAL_START_TIMESTAMP)
#         #               ]
#         #     plot_y = [FlowThread_High, FlowThread_High]
#         #     ax.plot(plot_x, plot_y, YITA_MEA_GLOBAL_VAL.SHOULD_DISPLAY_TASK[task], linewidth=YITA_MEA_GLOBAL_VAL.TIME_LINE_WIDTH)
#         # break
#         print "---- 生成 %s 线程的数据, 完毕 ----" % thread_name
#         # 单个slave中每个flowThread的高度加1
#         # FlowThread_High += 1
#
#     # y轴的高度，设定为最高高度 加上 4
#     plt.ylim(0, FlowThread_High + 36)
#     print_title = plt.title(title, fontproperties="SimHei")
#     print_title.set_fontsize(fontsize=20)
#
#     print "图片保存在：" + ((YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC + "%s主机中FlowThread的运行情况.jpg") % slave_host)
#
#     # plt.savefig((YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC + "%s-flowthreads.jpg") % slave_host)
#     # 调整画布大小
#     fig = plt.gcf()
#     fig.set_size_inches(16.5, 14.5)
#     fig.savefig((YITA_MEA_GLOBAL_VAL.CSV_FLOWTHREAD_DETAIL_PIC + "%s-flowthreads.jpg") % slave_host)
#
#     # plt.show()
#     plt.close()
#
#
# # 将一个打印中，同一个task中可以合并的项目合并掉，减少打印负担
# def combine_availabel_task_contents(lst_task):
#     lst_return = []
#     obj_combine = None
#     # obj_current = None
#     for obj in lst_task:
#         if obj_combine == None:
#             obj_combine = obj
#         else:
#             # 如果前一个的 end_time 与 后一个的 start_time 相一致，就可以合并
#             if obj_combine["end_time"] == obj["start_time"]:
#                 obj_combine["end_time"] = obj["end_time"]
#
#             # 如果不一致，则将combine对象合并，然后将合并的对象放入返回对象中，然后取当前的对象作为合并的基础对象
#             else:
#                 lst_return.append(obj_combine)
#                 obj_combine = obj
#
#             # 当循环到最后一个对象时，将combine对象加入到返回对象中
#             if obj == lst_task[-1]:
#                 lst_return.append(obj_combine)
#
#     print "---- 合并前数据量为: %s ----" % len(lst_task)
#     print "---- 合并后数据量为：%s ----" % len(lst_return)
#     return lst_return
#


if __name__ == "__main__":
    log_and_stdout("测试成功")