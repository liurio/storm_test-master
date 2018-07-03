# -*- coding:utf-8 -*-
from Script_functions import get_lst_command


class script_rtw():

    script_of_start_test = """
    /usr/local/storm/bin/storm jar \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s \\
        %s
    """

    @staticmethod
    def get_command_of_start_test(
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
    ):
        return get_lst_command(script_rtw.script_of_start_test,(
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
        ))


    script_of_gen_data = """
    java -cp '/home/yitacm/yita-1.1.0/lib/*'                                \\
      cn.com.jetflow.yita.examples.streaming.tools.RollingTopWordsData      \\
      %s                                                                    \\
      %s                                                                    \\
      kafka.serializer.StringEncoder                                        \\
      %s                                                                    \\
      %s                                                                    \\
      %s 
    """

    @staticmethod
    def get_command_of_gen_rolling_top_words(kafka_servers, ack, topic, interval, thread_num):
        return get_lst_command(
            script_rtw.script_of_gen_data,
            (kafka_servers, ack, topic, interval, thread_num)
        )

    script_of_kill_topology = """
    storm kill %s
    """


    @staticmethod
    def get_command_of_kill_topology(topology_name):
        return get_lst_command(
            script_rtw.script_of_kill_topology,
            (topology_name)
        )


    script_of_add_topic = """
    /usr/local/kafka/bin/kafka-topics.sh --create \\
      --zookeeper %s \\
      --topic %s \\
      --replication-factor 1 \\
      --partitions 20
    """


    @staticmethod
    def get_command_of_add_topic(zk_servers, topic):
        return get_lst_command(script_rtw.script_of_add_topic, (zk_servers, topic))


    script_of_delete_topic = """
    /usr/local/kafka/bin/kafka-topics.sh --delete \\
    --zookeeper %s \\
    --topic %s
    """

    @staticmethod
    def get_command_of_delete_topic(zk_servers, topic):
        return get_lst_command(script_rtw.script_of_delete_topic, (zk_servers, topic))


    script_of_get_worker_pid = """
    ps -ef | grep storm | grep -v grep | grep org.apache.storm.daemon.worker | grep -v LogWriter | awk '{print $2}'
    """


    @staticmethod
    def get_command_of_get_worder_pid():
        return get_lst_command(script_rtw.script_of_get_worker_pid)


    # script_of_nethogs_monitor = """
    # echo "" > %s;
    # nethogs -t | awk '{ printf "{{m}}\\t",$0; system("date +\\"[{{m}}\\"]"); }' | egrep "%s" >> %s
    # """
    script_of_nethogs_monitor = """
    echo "" > %s;
    nethogs -t | awk '{ printf "{{m}}\\t",$0; system("date +\\"[{{m}}\\"]"); }' | egrep "java" >> %s
    """


    @staticmethod
    def get_command_of_nethogs_monitor(nethogs_log_file):
        lst_command =  get_lst_command(script_rtw.script_of_nethogs_monitor,(nethogs_log_file, nethogs_log_file))
        return map(lambda x: x.replace("{{m}}", "%s"), lst_command)


    script_of_kill_nethogs_monitor = """
    kill `ps -ef | grep nethogs | grep -v grep | awk '{print $2}'`
    """


    @staticmethod
    def get_command_of_kill_nethogs_monitor():
        return get_lst_command(script_rtw.script_of_kill_nethogs_monitor)