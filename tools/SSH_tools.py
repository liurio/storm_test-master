# -*-coding:utf-8-*-

import paramiko


# 登陆远程Linux主机执行特定命令
def execute_command_on_linux(host, username, password, command, port = 22):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # print "host: %s, port: %s" % (host, port)
    ssh.connect(host, port, username, password)
    execute_command = "source /etc/profile;" + "source ~/.bashrc;" + command
    # execute_command = "source ~/.bashrc;" + command
    # print "执行的命令为:%s" % execute_command
    stdin, stdout, stderr = ssh.exec_command(execute_command)
    try:
        this_out = stdout.readlines()
        this_err = stderr.readlines()
        return this_out, this_err
    except UnicodeDecodeError,e:
        print e.message
        return [],[]
    finally:
        ssh.close()



# 从linux主机上下载文件
def download_file_from_linux(host, username, password, absolute_remote_path, absolute_local_path, port = 22):
    t = paramiko.Transport((host, port))
    t.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(absolute_remote_path,absolute_local_path)
    t.close()


# 上传文件到linux主机
def upload_file_to_linux(host, username, password, absolute_local_path, absolute_remote_path, port = 22):
    t = paramiko.Transport((host, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(absolute_local_path, absolute_remote_path)
    t.close()
