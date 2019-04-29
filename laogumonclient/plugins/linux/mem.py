import subprocess
from psutil import *

def monitor():
    vmstat_command = "vmstat | tail -n1"
    status, result = subprocess.getstatusoutput(vmstat_command)
    if status != 0:
        value_dic = {'status': status}
    else:
        swpd, free, buff, cache, si, so = result.split()[2:8]
        used_rent = str(list(virtual_memory())[2])
        value_dic = {
            'swpd': swpd,
            'free': free,
            'buff': buff,
            'cache': cache,
            'si': si,
            'so': so,
            'status': status,
            'used_rent': used_rent,
            'has_sub_dic': False,
            'is_info': 'False',
        }
    return value_dic
