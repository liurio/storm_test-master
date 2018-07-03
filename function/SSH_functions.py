# -*-coding:utf-8-*-
from tools.SSH_tools import *
from log_function import log_and_stdout
from config.Configuration import cfg_all
from config.Configuration_of_rolling_top_words import cfg_rtw
from tools.time_tools import get_timestamp, format_ms_time
from tools.file_tools import write_to_dest_file_with_lst, combine_files_to_one
from scripts.Scripts_of_rolling_top_words import script_rtw
import multiprocessing
import os


"""
 1.抽象化功能区
"""

"""
 1.1 执行命令区域
"""


# 到指定主机上执行命令
def execute_command_on_machine(machine_ip, lst_command, print_command = False):
    if print_command:
        log_and_stdout("需要被执行的命令为：%s" % lst_command)

    this_out, this_error = execute_command_on_linux(
        machine_ip,
        cfg_all.USERNAME,
        cfg_all.PASSWORD,
        ";".join(lst_command))
    if len(this_out) > 0:
        this_out = [x.replace("\n","") for x in this_out]
    if len(this_error) > 0:
        this_error = [x.replace("\n","") for x in this_error]
    return this_out, this_error

# 到Master主机上执行命令
def execute_command_on_master(lst_command, print_command = False):
    return execute_command_on_machine(
        cfg_all.MASTER_HOST,
        lst_command,
        print_command
    )


# 到Pidstat主机上执行命令
def execute_command_on_pidstat_machine(lst_command, print_command = False):
    return execute_command_on_machine(
        cfg_all.PIDSTAT_HOST,
        lst_command,
        print_command
    )

"""
 1.2 下载文件区域
"""
# 到指定主机上下载文件
def download_file_from_machine(machine_ip, remote_file, local_file, port = 22):
    download_file_from_linux(
        machine_ip,
        cfg_all.USERNAME,
        cfg_all.PASSWORD,
        remote_file,
        local_file,
        port)


# 从Master上下载文件
def download_file_from_master(remote_file, local_file, port = 22):
    download_file_from_machine(
        cfg_all.MASTER_HOST,
        remote_file,
        local_file,
        port
    )


# 从pidstat机器上下载文件
def download_file_from_pidstat_machine(remote_file, local_file, port = 22):
    download_file_from_machine(
        cfg_all.PIDSTAT_HOST,
        remote_file,
        local_file,
        port
    )


"""
 1.3 上传文件区域
"""
# 上传文件到指定主机上
def upload_file_to_machine(machine_ip, local_file, remote_file, port = 22):
    upload_file_to_linux(
        machine_ip,
        cfg_all.USERNAME,
        cfg_all.PASSWORD,
        local_file,
        remote_file,
        port)


# 上传文件至Master主机
def upload_file_to_master(local_file, remote_file, port = 22):
    upload_file_to_machine(
        cfg_all.MASTER_HOST,
        local_file,
        remote_file
    )


# 上传文件至pidstat主机
def upload_file_to_pidstat_machine(local_file, remote_file, port = 22):
    upload_file_to_machine(
        cfg_all.PIDSTAT_HOST,
        remote_file,
        local_file
    )


"""
 1.4 文件互传区
"""
# 将一个文件从一个主机传到另一个主机
def scp_file_from_a_to_b(machine_a, machine_b, username, path_a, path_b, file_name):
    source_file = path_a + file_name
    dest_file = "%s@%s:%s%s" % (username, machine_b, path_b, file_name)
    scp_command = ["""scp %s %s""" % (source_file, dest_file)]
    execute_command_on_machine(machine_a, scp_command)


# 将一个文件从master传到另一台机器的同一位置
def scp_file_from_mastet_to_other_same_path(other_machine, path, file_name):
    scp_file_from_a_to_b(
        cfg_all.MASTER_HOST,
        other_machine,
        "root",
        path,
        path,
        file_name
    )

"""
 具体功能区
"""

# 到master主机上开始测试
def start_rtw_test_on_master_f():
    jar_file = cfg_rtw.remote_test_jar_file
    class_name = cfg_rtw.test_class_name
    topology = cfg_rtw.topology_name
    mode = cfg_rtw.test_mode
    worker_num = cfg_rtw.worker_num
    zk_hosts = cfg_all.zk_servers
    znode_dir = cfg_rtw.znode_dir
    topic = cfg_rtw.topic
    top_n = cfg_rtw.top_n
    window_size = cfg_rtw.window_size
    slide_window_size = cfg_rtw.slide_window_size
    rtw_start_script = script_rtw.get_command_of_start_test(
        jar_file,
        class_name,
        topology,
        mode,
        worker_num,
        zk_hosts,
        znode_dir,
        topic,
        top_n,
        window_size,
        slide_window_size
    )
    print rtw_start_script
    this_out, this_err = execute_command_on_master(rtw_start_script,print_command=True)
    return this_out, this_err


# 得到master上的worker的pid
def get_worker_pid_of_storm_in_running():
    # return get_worker_pid_of_storm_on(cfg_all.MASTER_HOST)
    return get_worker_pid_of_storm_on_pidstat_machine()

# 得到指定主机的slave的pid
def get_worker_pid_of_storm_on(machine_ip):
    lst_command = script_rtw.get_command_of_get_worder_pid()
    this_out, this_err = execute_command_on_machine(machine_ip, lst_command)
    try:
        return map(int, this_out)
    except TypeError, e:
            e.message


# 得到pidstat主机的worker的pid
def get_worker_pid_of_storm_on_pidstat_machine():
    return get_worker_pid_of_storm_on(cfg_all.PIDSTAT_HOST)


def path_compare(x,y):
    x_sort = int(x.split("-")[6])
    y_sort = int(y.split("-")[6])
    if x_sort < y_sort:
        return -1
    else:
        return 1


# 获取storm日志目录下最后一个log目录(包含topology)
def get_last_log_path_for_topology(machine_ip):
    lst_command = [
        "ls -l %s | awk '{print $9}'" % cfg_rtw.remote_log_base_path
    ]
    # print lst_command
    lst_log_paths, _ = execute_command_on_machine(machine_ip, lst_command)
    lst_handled_log_path = filter(lambda x: cfg_rtw.topology_name in x, lst_log_paths)
    lst_handled_log_path.sort(path_compare)

    # lst_command2 = [
    #     "ls -l %s%s/ | awk '{print $9}'" % (cfg_rtw.remote_log_base_path,lst_handled_log_path[-1])
    # ]
    # lst_log_paths_port, _ = execute_command_on_machine(machine_ip, lst_command2)
    # print "lst_handled_log_path:", lst_handled_log_path[-1]
    return "%s%s/" % (cfg_rtw.remote_log_base_path,lst_handled_log_path[-1])


# 下载执行日志
def download_test_logs_f():
    lst_result = []
    for machine_ip in cfg_all.SLAVE_HOSTS:
        lst_command = [
            """cat %s/*/worker.log | egrep '\+\+\+\+\+|\#\#\#\#\#'""" % get_last_log_path_for_topology(machine_ip)
        ]
        this_out, _ = execute_command_on_machine(machine_ip, lst_command)
        lst_result.extend(this_out)
    write_to_dest_file_with_lst(cfg_rtw.local_log_base_path + "worker.log", lst_result)


# 下载gc的log
def download_gc_logs_f():
    machine_ip = cfg_all.PIDSTAT_HOST
    lst_command = [
        """cat %s/*/gc.log.*""" % get_last_log_path_for_topology(machine_ip)
    ]
    this_out, _ = execute_command_on_machine(machine_ip, lst_command)

    write_to_dest_file_with_lst(cfg_rtw.local_log_base_path + "gc.log", this_out)


# # 下载vmstat的日志
# def download_vmstat_logs():
#     remote_vmstat_log_file = cfg_rtw.remote_monitor_base_path + "vmstat.log"
#     local_absolute_log_file = cfg_rtw.local_log_base_path + "vmstat.log"
#     download_file_from_pidstat_machine(remote_vmstat_log_file, local_absolute_log_file)


# 上传jar包，上传到所有的master和slave节点上面去
def upload_jars_to_master():
    local_absolute_jar_file = cfg_rtw.local_test_jar_file
    remote_absolute_jar_file = cfg_rtw.remote_test_jar_file
    upload_file_to_master(local_absolute_jar_file, remote_absolute_jar_file)
    # storm中不需要分发jar包
    # for machin_ip in cfg_all.SLAVE_HOSTS:
    #     if not machin_ip == cfg_all.MASTER_HOST:
    #         upload_file_to_machine(machin_ip, local_absolute_jar_file, remote_absolute_jar_file)


# 启动nethogs监控脚本
def start_nethogs_monitor_f():
    monitor_log_file = cfg_rtw.remote_monitor_base_path + "nethogs.log"
    # lst_worker_pids = map(lambda x: "%s" % x, get_worker_pid_of_storm_on_pidstat_machine())
    # # print lst_worker_pids
    # worker_pids = "|".join(lst_worker_pids)
    lst_command = script_rtw.get_command_of_nethogs_monitor(monitor_log_file)
    execute_command_on_pidstat_machine(lst_command, print_command=True)


# kill nethogs 监控脚本
def kill_nethogs_monitor_f():
    lst_command = script_rtw.get_command_of_kill_nethogs_monitor()
    execute_command_on_pidstat_machine(lst_command, print_command=True)


# 下载nethogs日志
def download_nethogs_log_f():
    remote_log_file = cfg_rtw.remote_monitor_base_path + "nethogs.log"
    local_log_file = cfg_rtw.local_log_base_path + "nethogs.log"
    download_file_from_pidstat_machine(remote_log_file, local_log_file)


# 启动vmstat监控脚本
def start_vmstat_monitor():
    monitor_log_file = cfg_rtw.remote_monitor_base_path + "vmstat.log"
    clearn_command = "echo '' > %s" % monitor_log_file
    monitor_command = """vmstat -n 1 | awk '{ printf "%s\\t",$0; system("date +\\"[%s\\"]"); }' >> """ + monitor_log_file
    lst_command = [
        clearn_command,
        monitor_command
        ]
    execute_command_on_pidstat_machine(lst_command,print_command=True)


# kill vmstat
def kill_vmstat_monitor():
    command = "ps -ef | grep vmstat | grep -v grep | awk '{print $2}'"
    lst_vmstat_pids, _ = execute_command_on_pidstat_machine([command])
    for pid in lst_vmstat_pids:
        kill_command = "kill %s" % pid
        execute_command_on_pidstat_machine([kill_command], print_command=True)


# 启动jstack
def start_jstack_monitor():
    lst_storm_worker_pids = map(int, get_worker_pid_of_storm_on_pidstat_machine())
    worker_num = len(lst_storm_worker_pids)
    jstack_log_file = cfg_rtw.remote_monitor_base_path + "jstack.log"
    lst_command = []
    for i in xrange(20):
        lst_command.append("sleep 1")
        lst_command.append("jstack %s >> %s" % (lst_storm_worker_pids[i % worker_num], jstack_log_file))
    execute_command_on_pidstat_machine(lst_command, print_command=True)


# 启动pidstat监控
def start_pid_monitor():
    lst_storm_worker_pids = map(int, get_worker_pid_of_storm_on_pidstat_machine())
    # 删除已有的pidstat监控文件
    delete_old_pidstat_monitor_file()
    # 启动一个新的进程去分别对每一个pidstat进行监控
    lst_process = []
    for worker_pid in lst_storm_worker_pids:
        worker_monitor_process = multiprocessing.Process(target=start_pidstat_monitor_with_pid, args=(worker_pid,))
        lst_process.append(worker_monitor_process)
    for process in lst_process:
        process.start()
    for process in lst_process:
        process.join()


# 每次启动指定pid的pidstat监控
def start_pid_monitor_for_pids(lst_pid):
    # lst_storm_worker_pids = map(int, get_worker_pid_of_storm_on_pidstat_machine())
    # 删除已有的pidstat监控文件
    # delete_old_pidstat_monitor_file()
    # 启动一个新的进程去分别对每一个pidstat进行监控
    if len(lst_pid) > 0:
        lst_process = []
        for worker_pid in lst_pid:
            worker_monitor_process = multiprocessing.Process(target=start_pidstat_monitor_with_pid, args=(worker_pid,))
            lst_process.append(worker_monitor_process)
        for process in lst_process:
            process.start()
        for process in lst_process:
            process.join()


# 启动指定pid的pidstat监控
def start_pidstat_monitor_with_pid(pid):
    pidstat_log_file = cfg_rtw.remote_monitor_base_path + ("pidstat_storm_%s.log" % pid)
    lst_command = [
        "echo '' > %s" % pidstat_log_file,
        "pidstat -d -r -u -w -t -h -p %s 1 >> %s" % (pid, pidstat_log_file)
    ]
    execute_command_on_pidstat_machine(lst_command, print_command=True)


# 删除已有的pidstat监控文件
def delete_old_pidstat_monitor_file():
    pidstat_log_file = cfg_rtw.remote_monitor_base_path + "pidstat_storm*"
    lst_command = [
        "rm -f %s" % pidstat_log_file
    ]
    execute_command_on_pidstat_machine(lst_command, print_command=True)


# 关闭pidstat监控
def kill_pidstat_monitor():
    kill_command = "kill `ps -ef | grep pidstat | grep -v grep | awk '{print $2}'`"
    execute_command_on_pidstat_machine([kill_command])


# 关闭指定pid的pidstat监控
def kill_pidstat_monitor_with_pid(pid):
    kill_command = "kill `ps -ef | grep pidstat | grep %s | grep -v grep | awk '{print $2}'`" % pid
    execute_command_on_pidstat_machine([kill_command],print_command=True)


# 启动数据生成
def start_gen_data_for_rolling_top_words():
    kafka_server = cfg_all.kafka_servers
    ack = cfg_rtw.ack
    topic = cfg_rtw.topic
    interval = cfg_rtw.interval
    thread_num = cfg_rtw.thread_num
    gen_data_script = script_rtw.get_command_of_gen_rolling_top_words(
        kafka_server,
        ack,
        topic,
        interval,
        thread_num,
    )
    try:
        this_out, this_error = execute_command_on_master(gen_data_script, print_command=True)
        # log_and_stdout("生成数据 - 标准输出")
        # print "\n".join(this_out)
        # log_and_stdout("生成数据 - error输出")
        # print "\n".join(this_error)
        # log_and_stdout("生成数据 - 输出结束")
        write_to_dest_file_with_lst(
            cfg_rtw.local_log_base_path + "gen_data.log",
            this_out
        )
    except TypeError, e:
            e.message
    return this_out, this_error


# 停止数据生成
def stop_gen_data_for_rolling_top_words():
    stop_command = "kill `ps -ef | grep RollingTopWordsData | grep -v grep | awk '{print $2}'`"
    try:
        this_out, this_error = execute_command_on_master([stop_command], print_command=True)
        log_and_stdout("停止生成数据 - 标准输出")
        print "\n".join(this_out)
        log_and_stdout("停止生成数据 - error输出")
        print "\n".join(this_error)
        log_and_stdout("停止生成数据 - 输出结束")
    except TypeError, e:
            e.message
    return this_out, this_error


# 停止rolling_top_words
def stop_rolling_top_words():
    topology_name = cfg_rtw.topology_name
    lst_kill_command = script_rtw.get_command_of_kill_topology(topology_name)
    try:
        this_out, this_error = execute_command_on_master(lst_kill_command, print_command=True)
        log_and_stdout("停止测试 - 标准输出")
        print "\n".join(this_out)
        log_and_stdout("停止测试 - error输出")
        print "\n".join(this_error)
        log_and_stdout("停止测试 - 输出结束")
    except TypeError, e:
            e.message
    return this_out, this_error


# 添加topic
def add_topic_for_rtw_f():
    zk_servers = cfg_all.zk_servers
    topic = cfg_rtw.topic
    log_and_stdout("添加topic - %s ，开始" % topic)
    lst_command = script_rtw.get_command_of_add_topic(zk_servers, topic)
    execute_command_on_master(lst_command, print_command=True)
    log_and_stdout("添加topic - %s ，结束" % topic)


# 删除topic
def delete_topic_for_rtw_f():
    zk_servers = cfg_all.zk_servers
    topic = cfg_rtw.topic
    log_and_stdout("删除topic - %s ，开始" % topic)
    lst_command = script_rtw.get_command_of_delete_topic(zk_servers, topic)
    execute_command_on_master(lst_command, print_command=True)
    log_and_stdout("删除topic - %s ，结束" % topic)



# 下载pidstat日志
def download_pidstat_logs_f():
    pidstat_log_path = cfg_rtw.remote_monitor_base_path + "pidstat_storm*"
    lst_remote_pid_filenames, _ = execute_command_on_pidstat_machine(["ls -l %s | awk '{print $9}'" % pidstat_log_path ])
    # print lst_remote_pid_filenames
    lst_local_pid_filenames = map(lambda x: cfg_rtw.local_log_base_path + x.split("/")[-1], lst_remote_pid_filenames)
    # 删除本地的文件
    delete_local_old_pidstat_log()
    for remote_file in lst_remote_pid_filenames:
        download_file_from_pidstat_machine(remote_file, cfg_rtw.local_log_base_path + remote_file.split("/")[-1])
    # 合并pidstat日志
    combine_files_to_one(
        cfg_rtw.local_log_base_path + "pidstat.log",
        lst_local_pid_filenames
    )


# 删除本地旧的pidstat日志
def delete_local_old_pidstat_log():
    for file in os.listdir(cfg_rtw.local_log_base_path):
        if "pidstat_storm" in file:
            local_file = os.path.join(cfg_rtw.local_log_base_path, file)
            if os.path.isfile(local_file):
                os.remove(local_file)


# 下载jstack的日志
def download_jstack_logs_f():
    remote_jstack_log_file = cfg_rtw.remote_monitor_base_path + "jstack.log"
    local_absolute_log_file = cfg_rtw.local_log_base_path + "jstack.log"
    download_file_from_pidstat_machine(remote_jstack_log_file, local_absolute_log_file)


# 下载vmstat的日志
def download_vmstat_logs_f():
    remote_vmstat_log_file = cfg_rtw.remote_monitor_base_path + "vmstat.log"
    local_absolute_log_file = cfg_rtw.local_log_base_path + "vmstat.log"
    download_file_from_pidstat_machine(remote_vmstat_log_file, local_absolute_log_file)





