from django.shortcuts import render, HttpResponse
from .serializer import ClientHandler
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from . import optimization
from . import redis_connect
from django.conf import settings

REDIS_OBJ = redis_connect.redis_connect(settings)


def dashboard(request):
  data = {
    'data': '',
  }
  return render(request, 'backends/dashboard.html', )


def hosts(request):
  host_list = models.Host.objects.all()
  print("hosts:", host_list)
  return render(request, 'monitor/hosts.html', {'host_list': host_list})


def host_detail(request, host_id):
  host_obj = models.Host.objects.get(id=host_id)
  return render(request, 'monitor/host_detail.html', {'host_obj': host_obj})


# def hosts_status(request):
#   hosts_data_serializer = serializer.StatusSerializer(request, REDIS_OBJ)
#   hosts_data = hosts_data_serializer.by_hosts()
#
#   return HttpResponse(json.dumps(hosts_data))
#
#
# def hostgroups_status(request):
#   group_serializer = serializer.GroupStatusSerializer(request, REDIS_OBJ)
#   group_serializer.get_all_groups_status()
#
#   return HttpResponse('ss')


def client_configs(request, client_id):
  print("--->", client_id)
  config_obj = ClientHandler(client_id)
  config = config_obj.fetch_configs()
  print(config)

  if config:
    return HttpResponse(json.dumps(config))


@csrf_exempt
def service_data_report(request):
  # 这里的request是客户端发来的
  print(request.method)
  if request.method == 'POST':
    try:
      print('host=%s, service=%s' % (request.POST.get('client_id'), request.POST.get('service_name')))
      data = json.loads(request.POST['data'])
      # print(data)
      # StatusData_1_memory_latest
      client_id = request.POST.get('client_id')
      service_name = request.POST.get('service_name')

      # 把数据存下来
      optimization.DataStore(client_id, service_name, data, REDIS_OBJ)

      # redis_key_format = "StatusData_%s_%s_latest" %(client_id,service_name)
      # data['report_time'] = time.time()
      # REDIS_OBJ.lpush(redis_key_format,json.dumps(data))

      # 在这里同时触发监控(在这里触发的好处是什么呢？)
      # host_obj = models.Host.objects.get(id=client_id)
      # service_triggers = get_host_triggers(host_obj)
      #
      # trigger_handler = data_processing.DataHandler(settings, connect_redis=False)
      # for trigger in service_triggers:
      #   trigger_handler.load_service_data_and_calulating(host_obj, trigger, REDIS_OBJ)
      # print("service trigger::", service_triggers)

      # 更新主机存活状态
      # host_alive_key = "HostAliveFlag_%s" % client_id
      # REDIS_OBJ.set(host_alive_key,time.time())
    except IndexError as e:
      print('----->err:', e)
  # return HttpResponse(json.dumps(data))
  return HttpResponse(json.dumps("---report success---"))
