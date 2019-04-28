from __future__ import unicode_literals
from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# from .redis_con import redis_connect

from pyecharts import *
from .graphgenerator import *
from .infogetter import InfoGetter


def demo1(request):
    # host_obj = Host.objects.get(id=hostid)
    info_getter = InfoGetter()

    template = loader.get_template('index.html')

    line1 = cpu_line(Line('CPU-user-1min', width=650, height=300), "monitor-1-linux-cpu-1min", "user")
    line2 = cpu_line(Line('CPU-idle-1min', width=650, height=300), "monitor-1-linux-cpu-1min", "idle")

    line3 = net_line_latest(Line('Net-packets_sent-latest', width=650, height=300), "packets_sent")
    line4 = net_line_latest(Line('Net-packets_recv-latest', width=650, height=300), "packets_recv")

    gauge1 = mem_gauge_latest(Gauge('Mem-latest', width=300, height=300))

    net_page = Page()
    cpu_page = Page()

    cpu_page.add(line1)
    cpu_page.add(line2)
    net_page.add(line3)
    net_page.add(line4)
    # print(page)
    context = dict(
        page1=cpu_page.render_embed(),
        page2=net_page.render_embed(),
        mem_gauge=gauge1.render_embed(),
        top_info_dic=InfoGetter.index_top_info(info_getter),
        containers_list=InfoGetter.local_containers_info(info_getter),
        images_list=InfoGetter.local_images_info(info_getter),
        event_list=InfoGetter.local_event_info(info_getter)
    )
    return HttpResponse(template.render(context, request))


def demo2(request, hostid):
    host_obj = Host.objects.get(id=hostid)

    template = loader.get_template('host.html')

    l1 = cpu_line(Line('CPU-user-1min', width=650, height=300), "monitor-1-linux-cpu-1min", "user")
    l2 = cpu_line(Line('CPU-idle-1min', width=650, height=300), "monitor-1-linux-cpu-1min", "idle")

    l3 = net_line_latest(Line('Net-packets_sent-latest', width=650, height=300), "packets_sent")
    l4 = net_line_latest(Line('Net-packets_recv-latest', width=650, height=300), "packets_recv")

    g1 = mem_gauge_latest(Gauge('Mem-latest', width=300, height=300))

    npage = Page()
    cpage = Page()

    cpage.add(l1)
    cpage.add(l2)
    npage.add(l3)
    npage.add(l4)
    context = dict(
        p1=cpage.render_embed(),
        p2=npage.render_embed(),
        mg=g1.render_embed(),
        hostobj=host_obj
    )
    return HttpResponse(template.render(context, request))