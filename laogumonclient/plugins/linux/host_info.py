from psutil import *


def monitor():
    value_dic = {}

    boottime = boot_time()
    cpu_count_num = cpu_count()
    cpu_count_logical_num = cpu_count(logical=True)
    virtual_memory_total = round(virtual_memory().total/(1024*1024*1024), 1)
    swap_memory_total = swap_memory().total/(1024*1024*1024)

    value_dic['cpu_count_num'] = str(cpu_count_num)
    value_dic['cpu_count_logical_num'] = str(cpu_count_logical_num)
    value_dic['virtual_memory_total'] = str(virtual_memory_total)
    value_dic['swap_memory_total'] = str(swap_memory_total)
    value_dic['boottime'] = str(boottime)
    value_dic['status'] = 0
    value_dic['has_sub_dic'] = False
    value_dic['is_info'] = 'True'

    return value_dic