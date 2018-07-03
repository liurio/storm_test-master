#-*- coding:utf-8 -*-
from function.log_function import log_and_stdout

# 合并文件
def combine_files_to_one(dest_file,lst_src_files):
    with open(dest_file, 'w') as write_file:
        for file in lst_src_files:
            with open(file, 'r') as read_file:
                for line in read_file:
                    write_file.writelines(line)
                write_file.write("\n")

    log_and_stdout("文件合并完毕 - %s" % dest_file)


# 将list写入到目标文件中
def write_to_dest_file_with_lst(dest_file, lst):
    with open(dest_file, 'w') as write_file:
        for line in lst:
            write_file.write("%s\n" % line)

