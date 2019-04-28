import subprocess


def monitor():
    system_lang = subprocess.getoutput("echo $LANG")
    sar_command = ""
    if system_lang == 'zh_CN.UTF-8':
        sar_command = 'sar 1 3| grep "^平均时间:"'
    elif system_lang == 'en_US.UTF-8':
        sar_command = 'sar 1 3| grep "^Average:"'
    status, result = subprocess.getstatusoutput(sar_command)
    # 若不为0，则说明执行错误
    if status != 0:
        value_dic = {'status': status}
    else:
        user, nice, system, iowait, steel, idle = result.split()[2:]
        value_dic = {
            'user': user,
            'nice': nice,
            'system': system,
            'iowait': iowait,
            'steel': steel,
            'idle': idle,
            'status': status,
            'has_sub_dic': False
        }
    return value_dic
