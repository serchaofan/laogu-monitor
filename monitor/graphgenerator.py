import redis
import json
import time
from pyecharts import *
from django.conf import settings
from .redis_con import redis_connect


# 获取cpu的数据（必须是已优化的）
# 需传入要生成的线以及redis的键
def cpu_line(line, redis_key, cpu_item):
    '''
    :param line: 传入Line对象
    :param redis_key: redis库中的列表名
    :param cpu_item: cpu检测项名
    :return: Line对象
    :可选cpu_item: nice/system/iowait/steel/idle
    '''

    # 平均值
    avag = []
    # 最大值
    max = []
    # 最小值
    min = []
    # 时间x轴
    time_xaxis = []

    cpu_item_name = cpu_item
    cpu_item = []

    redis_obj = redis_connect(settings)
    list = redis_obj.lrange(redis_key, -30, -1)

    for a in list:
        # print("-----------------", a)
        b = json.loads(a)[0]
        timestamp = json.loads(a)[1]
        time_xaxis.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)))
        avag.append(b[cpu_item_name][0])
        max.append(b[cpu_item_name][1])
        min.append(b[cpu_item_name][2])

        cpu_item.append(b[cpu_item_name])

    # 添加平均值图
    line.add(cpu_item_name + '-avag', time_xaxis, avag,
             # is_datazoom_show=True,
             is_smooth=True,
             is_fill=True,
             area_opacity=0.7,
             # mark_line=["average"]
             )
    # 添加最大值图
    line.add(cpu_item_name + '-max', time_xaxis, max,
             # is_datazoom_show=True,
             is_smooth=True,
             is_fill=True,
             area_opacity=0.5,
             # mark_line=["average"]
             )
    # 添加最小值图
    line.add(cpu_item_name + '-min', time_xaxis, min,
             # is_datazoom_show=True,
             is_smooth=True,
             is_fill=True,
             area_opacity=0.3,
             # mark_line=["average"]
             )
    return line


# def cpu_line_latest(line, cpu_item):

def cpu_line_latest(line):
    time_xaxis = []
    # cpu_item_name = cpu_item
    # print(cpu_item)
    # cpu_item = []
    user = []
    system = []
    idle = []

    redis_obj = redis_connect(settings)
    list = redis_obj.lrange("monitor-1-linux-cpu-latest", -30, -1)
    for a in list:
        b = json.loads(a)[0]
        timestamp = json.loads(a)[1]
        time_xaxis.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)))
        user.append(b["user"])
        system.append(b['system'])
        idle.append(b['idle'])

    line.add("user", time_xaxis, user,
             is_smooth=True,
            isfill=True,
             )
    line.add("idle", time_xaxis, idle,
             is_smooth=True,
            isfill=True,
             )
    line.add("system", time_xaxis, system,
             is_smooth=True,
            isfill=True,
             )
    return line


def net_line_packets_latest(line):
    time_xaxis = []
    # net_item_name = net_item
    packets_recv = []
    packets_sent = []

    redis_obj = redis_connect(settings)
    list = redis_obj.lrange("monitor-1-linux-net-latest", -30, -1)

    for a in list:
        b = json.loads(a)[0]
        timestamp = json.loads(a)[1]
        time_xaxis.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)))
        packets_recv.append(round(int(b['packets_recv'])/1000))
        packets_sent.append(round(int(b['packets_sent'])/1000))

    line.add("packets_recv", time_xaxis, packets_recv,
             is_smooth=True,
             yaxis_name="接收包数量/千个",
             )
    line.add("packets_sent-", time_xaxis, packets_sent,
             is_smooth=True,
             yaxis_name="发送包数量/千个",
             )
    return line

def net_line_bytes_latest(line):
    time_xaxis = []
    # net_item_name = net_item
    bytes_recv = []
    bytes_sent = []

    redis_obj = redis_connect(settings)
    list = redis_obj.lrange("monitor-1-linux-net-latest", -30, -1)

    for a in list:
        b = json.loads(a)[0]
        timestamp = json.loads(a)[1]
        time_xaxis.append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)))
        bytes_recv.append(round(int(b['bytes_recv'])/1000))
        bytes_sent.append(round(int(b['bytes_sent'])/1000))

    line.add("bytes_recv", time_xaxis, bytes_recv,
             is_smooth=True,
             yaxis_name="kB",
             )
    line.add("bytes_sent", time_xaxis, bytes_sent,
             is_smooth=True,
             yaxis_name="kB",
             )
    return line


def mem_gauge_latest(gauge):
    redis_obj = redis_connect(settings)
    list = redis_obj.lrange("monitor-1-linux-mem-latest", -1, -1)

    b = json.loads(list[0])[0]

    rent = b['used_rent']
    gauge.add(
        "当前内存",
        "占用率",
        rent,
        angle_range=[180, 0],
        scale_range=[0, 100],
        is_legend_show=False,
        is_toolbox_show=False,
    )
    return gauge
