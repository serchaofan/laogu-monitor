from django.shortcuts import render, HttpResponse
from . import serializer
from .serializer import ClientHandler, get_host_triggers
from .models import *
import json

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

  if config:
    return HttpResponse(json.dumps(config))
