from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template import loader
from pyecharts import *
import json

from .serializer import ClientHandler
from .models import *

from . import optimization
from . import redis_connect


# 载入settings中的redis配置并连接，得到redis对象
REDIS_OBJ = redis_connect.redis_connect(settings)


def dashboard(request):
  return render(request, 'backends/dashboard.html', )


  # 返回某个host的详细信息
def host_detail(request, host_id):
  host_obj = models.Host.objects.get(id=host_id)
  return render(request, 'backends/host_detail.html', {'host_obj': host_obj})


# 所有主机的简单信息
def hosts_status(request):
  hosts_data_serializer = serializer.StatusSerializer(request, REDIS_OBJ)
  hosts_data = hosts_data_serializer.by_hosts()
  # host_data = [data, data, data,...]
      # data = {
      # 'id': host_obj.id,
      # 'name': host_obj.name,
      # 'ip_addr': host_obj.ip_addr,
      # 'status': host_obj.get_status_display(),
      # 'uptime': None,
      # 'last_update': None,
  return render(request, 'backends/hosts_list.html', {'host_list': hosts_data})


# 处理获取的客户端配置信息，client_id为接收的主机号，即client_config/(\d+)
def client_configs(request, client_id):
  print("正在接收主机序号为", client_id, "的数据")
  # 调用序列化模块serializer的方法
  config_obj = ClientHandler(client_id)
  config = config_obj.fetch_configs()
  print(config)

  if config:
    return HttpResponse(json.dumps(config))

# 报告客户端的服务信息
@csrf_exempt
def service_data_report(request):
  # 这里的request是客户端发来的
  client_data_report = {
    'client_id': '0',
    'service_name': '0',
    'data': '0'
  }
  print(request.method)
  if request.method == 'POST':
    try:
      print('host=%s, service=%s' % (request.POST.get('client_id'), request.POST.get('service_name')))
      data = json.loads(request.POST['data'])
      # 例：StatusData_1_memory_latest
      client_id = request.POST.get('client_id')
      service_name = request.POST.get('service_name')

      # 把数据存下来
      optimization.DataStore(client_id, service_name, data, REDIS_OBJ)
      client_data_report['client_id'] = client_id
      client_data_report['service_name'] = service_name
      client_data_report['data'] = data
    except IndexError as e:
      print('报错：', e)
  return HttpResponse(json.dumps(client_data_report))
