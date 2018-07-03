# -*-coding:utf-8-*-
from service.service_of_rolling_top_words import *
import time
from config.Configuration_of_rolling_top_words import cfg_rtw
from tools.time_tools import get_timestamp
from analysis.report_of_rolling_top_words import analyse_main


if __name__ == "__main__":

    """
      第一步，配置参数
    """
    log_and_stdout("配置参数 - 开始")
    config_value = {
        "test_mode":"remote",
        "topic":cfg_rtw.topic % get_timestamp(),
        "top_n":20,
        "window_size":30000,
        "ack":1,
        "interval":2000,
        # ==============此处可修改thread的数量=================
        "thread_num":1,
        # "thread_num":40,
        # "thread_num":90,
        # =====================================================
        "exec_time": 1200
    }
    cfg_rtw.init_with_value(config_value)
    log_and_stdout("配置参数 - 结束")
    # 添加topic
    add_topic()

    """
      第二步，确认一个干净的环境
    """

    clean_the_environment()


    """
      第三步，正式开始测试
    """
    try:
       # 上传jar包
        refresh_rtw_jars()

       # 启动监控程序
        monitor_pidstat, monitor_vmstat, monitor_jstack, monitor_nethogs = start_rtw_monitor(config_value)

       # 启动storm的rolling_top_words程序
        test_process = start_rtw_test(config_value)

       # 休息30s
        time.sleep(30)

       # 启动数据生成线程，往kafka中写入数据
        gen_data_process = start_gen_data_for_rtw(config_value)

       # 阻塞exec_time后，停止测试
        while not worker_is_already_running():
            time.sleep(1)
        log_and_stdout("测试程序在运行，阻塞指定时长，开始")
        time.sleep(cfg_rtw.exec_time)
        log_and_stdout("测试程序在运行，阻塞指定时长，结束")
        stop_the_whole_test(monitor_pidstat)

       # 删除topic
        delete_topic()

       # 启动分析脚本
        theoretical_window_count = cfg_rtw.exec_time * 1000 / cfg_rtw.slide_window_size
        hotword_num_per_window = cfg_rtw.window_size /  cfg_rtw.interval
        producer_out_filename = cfg_rtw.local_log_base_path + "gen_data.log"
        consumer_out_filename = cfg_rtw.local_log_base_path + "worker.log"
        analyse_main(
            theoretical_window_count,
            hotword_num_per_window,
            producer_out_filename,
            consumer_out_filename
        )


    finally:
        clean_the_environment()

