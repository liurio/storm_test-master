# -*-coding:utf-8-*-
class cfg_all():
    # 测试环境的MASTER主机
    MASTER_HOST = "10.47.168.116"
    # slave主机的IP
    # SLAVE_HOSTS = ["10.47.168.116", "10.47.168.117"]
    SLAVE_HOSTS = ["10.47.168.117", "10.47.168.118", "10.47.168.119", "10.47.168.120"]
    # 监控的主机地址
    PIDSTAT_HOST = "10.47.168.117"
    USERNAME = "root"
    PASSWORD = "jetflow123"
    # kafka servers
    kafka_servers = "jfsh16:9092,jfsh17:9092,jfsh18:9092,jfsh19:9092,jfsh20:9092"
    # zookeeper servers
    zk_servers = "jfsh16:2181,jfsh17:2181,jfsh18:2181,jfsh19:2181,jfsh20:2181"