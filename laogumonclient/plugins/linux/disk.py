from psutil import *


def monitor():
    disk_partitions_list = disk_partitions()
    # disk_usage_list = disk

