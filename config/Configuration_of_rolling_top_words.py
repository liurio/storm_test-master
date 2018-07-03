# -*-coding:utf-8-*-
class cfg_rtw():
    # 远端产生日志的基础文件夹
    remote_log_base_path = "/usr/local/storm/logs/workers-artifacts/"
    # 远端监控文件基础文件夹
    remote_monitor_base_path = "/home/tjf_wordcount_test/rolling_top_words/storm/logs/"
    # 本地日志基础文件夹
    local_log_base_path = "E:\\test_rolling_top_words\storm\\"
    # master上jar包的位置
    remote_test_jar_file = "/home/tjf_wordcount_test/rolling_top_words/storm/jars/rollingTopWordsForStorm-1.0-jar-with-dependencies.jar"
    # 本地jar包位置
    local_test_jar_file = "E:\WorkSpace\\rollingTopWordsForStorm\\target\\rollingTopWordsForStorm-1.0-jar-with-dependencies.jar"
    # 测试用类名
    test_class_name = "cn.com.jetflow.RollingTopWords"
    # topology名称
    topology_name = "rolling-top-words-storm-topo"
    # test_mode
    test_mode = "remote"
    # worker_num
    # worker_num = 2
    worker_num = 4
    # znode_dir
    znode_dir = "/rolling-top-words-storm"
    # topic
    topic = "rolling-top-words-input-%s"
    # top_n
    top_n = 20
    # window_size
    window_size = 30000
    # slide_window_size
    slide_window_size = 2000
    # -- 产生数据使用 --
    ack = 1
    # interval
    interval = 2000
    # thread_num
    thread_num = 1
    # exec_time
    exec_time = 1200


    @staticmethod
    def init_with_value(value):
        cfg_rtw.test_mode = value["test_mode"]
        cfg_rtw.topic = value["topic"]
        cfg_rtw.top_n = value["top_n"]
        cfg_rtw.window_size = value["window_size"]
        cfg_rtw.ack = value["ack"]
        cfg_rtw.interval = value["interval"]
        cfg_rtw.thread_num = value["thread_num"]
        cfg_rtw.exec_time = value["exec_time"]

