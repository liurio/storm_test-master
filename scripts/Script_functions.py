# -*- coding:utf-8 -*-


def get_lst_command(command, parameter=None):
    ret_command = command
    if ret_command.startswith("\n"):
        ret_command = ret_command[1:]
    while "; " in ret_command:
        ret_command = ret_command.replace("; ", ";")
    while ";\n" in ret_command:
        ret_command = ret_command.replace(";\n",";")

    # while " \n" in ret_command:
    #     ret_command = ret_command.replace(" \n","\n")
    # while "\n " in ret_command:
    #     ret_command = ret_command.replace("\n ","\n")
    # while "\n" in ret_command:
    #     ret_command = ret_command.replace("\n", "")
    #
    # while "\n " in ret_command:
    #     ret_command = ret_command.replace("\n ", "\n")

    if not parameter == None:
        ret_command = ret_command % parameter
    return ret_command.split(";")