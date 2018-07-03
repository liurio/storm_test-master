# -*- coding:utf-8 -*-
from function.SSH_functions import *
import time


# 上传jar包
def refresh_rtw_jars():
    log_and_stdout("上传jar包 - 开始")
    # storm只需上传jar包到主节点即可
    upload_jars_to_master()
    log_and_stdout("上传jar包 - 结束")


# 确认一个干净的环境，因为用到topology，所以该逻辑要放到参数配置后
def clean_the_environment():
    log_and_stdout("清理环境 - 开始")
    # 停止所有的监控程序
    kill_all_the_monitor()
    # 停止生成数据
    stop_gen_data_for_rolling_top_words()
    # 停止该topology的storm程序
    stop_rolling_top_words()
    log_and_stdout("清理环境 - 结束")


# 停止所有的监控程序
def kill_all_the_monitor():
    # 停止vmstat
    kill_vmstat_monitor()
    # 停止pidstat
    kill_pidstat_monitor()
    # 停止nethogs
    kill_nethogs_monitor_f()


# 正常程序中 - 停止所有的监控程序
def kill_all_the_monitor_for_correct():
    # 停止vmstat
    kill_vmstat_monitor()
    # 停止pidstat
    kill_pidstat_monitor()
    # 停止nethogs
    kill_nethogs_monitor_f()


# 添加topic
def add_topic():
    log_and_stdout("添加topic - 开始")
    log_and_stdout("topic的值为：%s" % cfg_rtw.topic)
    add_topic_for_rtw_f()
    log_and_stdout("添加topic - 结束")


# 删除topic
def delete_topic():
    delete_topic_for_rtw_f()


# 启动监控程序
def start_rtw_monitor(config_value):

    log_and_stdout(u"启动监控 - 开始")
    monitor_pidstat_process = get_process(do_monitor, config_value, "pidstat")
    monitor_vmstat_process = get_process(do_monitor, config_value, "vmstat")
    monitor_jstack_process = get_process(do_monitor, config_value, "jstack")
    monitor_nethogs_process = get_process(do_monitor, config_value, "nethogs")

    monitor_pidstat_process.start()
    monitor_vmstat_process.start()
    monitor_jstack_process.start()
    monitor_nethogs_process.start()
    log_and_stdout(u"启动监控 - 结束")
    return monitor_pidstat_process, monitor_vmstat_process, monitor_jstack_process, monitor_nethogs_process


# 为方法启动一个线程
def get_process(function, config_dictionary, parameter=None):

    new_process = multiprocessing.Process(
        target= init_new_process,
        args=(function, config_dictionary, parameter)
    )
    return new_process


# 初始化环境，执行目标函数
def init_new_process(function, config_dictionary, parameter):

    cfg_rtw.init_with_value(config_dictionary)

    if parameter == None:
        function()
    else:
        function(parameter)


# do monitor
def do_monitor(monitor_type):
    log_and_stdout("监控项目 - %s 开始" % monitor_type )
    if monitor_type == "pidstat":
        monitor_function = pidstat_monitor_handler
    elif monitor_type == "vmstat":
        monitor_function = start_vmstat_monitor
    elif monitor_type == "jstack":
        monitor_function = start_jstack_monitor
    elif monitor_type == "nethogs":
        monitor_function = start_nethogs_monitor_f

    do_monitor_prototype(monitor_function)
    log_and_stdout("监控项目 - %s 结束" % monitor_type)


# pidstat的监控控制
def pidstat_monitor_handler():
    # 删除旧的pidstat日志
    delete_old_pidstat_monitor_file()
    lst_storm_workder_pids = map(lambda x: "%s" % x, get_worker_pid_of_storm_on_pidstat_machine())
    # 启动已有的worker的pidstat监控
    start_pid_monitor_for_pids(lst_storm_workder_pids)
    set_runned_pids = set(lst_storm_workder_pids)
    set_running_pids = set(lst_storm_workder_pids)
    # 只要worker还在运行之中
    while True:

        # 获得现有的workder的pids
        lst_storm_workder_pids = map(lambda x: "%s" % x, get_worker_pid_of_storm_on_pidstat_machine())
        if len(lst_storm_workder_pids) > 0:
            set_current_pids = set(lst_storm_workder_pids)
            # 找到之前运行，现在已经不运行的pid
            set_to_be_close = set_running_pids - set_current_pids
            # 关掉这些pid
            print "******需要关掉：" , set_to_be_close
            for pid in set_to_be_close:
                kill_pidstat_monitor_with_pid(pid)
            # 找到新增的pid
            lst_to_be_start = list(set_current_pids - set_running_pids)
            print "******需要新增：", lst_to_be_start
            # 启动这些pid的pidstat的监控
            start_pid_monitor_for_pids(lst_to_be_start)
            # 更新set_running_pids
            print "set_running_pids", set_running_pids
            set_running_pids = set_current_pids.copy()
            # 更新set_runned_pids
            print "set_runned_pids: ", set_runned_pids
            set_runned_pids = set_runned_pids | set_running_pids

            # 将所有的pid的lst写入到本地的文件中
            write_to_dest_file_with_lst(
                cfg_rtw.local_log_base_path + "all_workder_pids.log",
                list(set_runned_pids)
            )
        # 每1s循环一次
        time.sleep(1)

    for pid in set_running_pids:
        kill_pidstat_monitor_with_pid(pid)



# 检测到程序在运行后，启动monitor程序
def do_monitor_prototype(monitor_function):
    # 在Yita程序启动之前，睡眠
    while not worker_is_already_running():
        time.sleep(1)
    # 启动monitor
    monitor_function()


# 确认worker程序已经运行
def worker_is_already_running():
    return len(get_worker_pid_of_storm_in_running()) > 0


# 启动测试程序
def start_rtw_test(config_value):
    log_and_stdout("启动测试 - 开始")
    start_rtw_process = get_process(
        start_rtw_test_on_master_f,
        config_value
    )
    start_rtw_process.start()
    log_and_stdout("启动测试 - 结束")
    return start_rtw_process


# 启动数据生成线程，往kafka中写入数据
def start_gen_data_for_rtw(config_value):
    log_and_stdout("启动数据生成 - 开始")
    gen_data_process = get_process(
        start_gen_data_for_rolling_top_words,
        config_value
    )
    gen_data_process.start()
    log_and_stdout("启动数据生成 - 结束")
    return gen_data_process


# 结束整个测试
def stop_the_whole_test(monitor_pidstat):
    # 第一步，关闭监控程序
    kill_all_the_monitor()

    # 第二步，关闭数据写入线程
    stop_gen_data_for_rolling_top_words()

    # 第三步，关闭storm程序
    stop_rolling_top_words()
    # 关闭monitor_pidstate线程
    monitor_pidstat.terminate()
    # 第四步，下载日志
    download_all_the_logs()


# 下载所有日志
def download_all_the_logs():
    # 下载gc日志
    download_gc_logs_f()
    # 下载测试日志
    download_test_logs_f()
    # 下载pidstat日志
    download_pidstat_logs_f()
    # 下载jstack日志
    download_jstack_logs_f()
    # 下载vmstat日志
    download_vmstat_logs_f()
    # 下载nethogs日志
    download_nethogs_log_f()


if __name__ == "__main__":
    download_all_the_logs()
