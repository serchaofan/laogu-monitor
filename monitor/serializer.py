from . import models
import json
import time
from django.core.exceptions import ObjectDoesNotExist
from psutil import *
import docker


# 处理客户端发来的信息
class ClientHandler(object):
    def __init__(self, client_id):
        # 主机序号
        self.client_id = client_id
        # 主机的配置服务
        self.client_configs = {
            "services": {}
        }

    # 获取客户端配置
    def fetch_configs(self):
        try:
            # 获取客户端主机对象
            host_obj = models.Host.objects.get(id=self.client_id)
            # print("host_obj:", host_obj.host_groups.select_related())
            # print("host_obj: ", host_obj.ip_addr, host_obj.host_groups.name, host_obj.templates.select_related())
            template_list = list(host_obj.templates.select_related())
            # print("template_list: ", template_list)

            for host_group in host_obj.host_groups.select_related():
                # print("host_group", host_group)
                template_list.extend(host_group.templates.select_related())

            # print("template_list", template_list)

            for template in template_list:
                # print("template", template)
                for service in template.services.select_related():
                    # print("service", service)
                    self.client_configs['services'][service.name] = [service.plugin_name, service.interval]

        except ObjectDoesNotExist:
            print(ObjectDoesNotExist)
        return self.client_configs


# 状态序列化
class StatusSerializer(object):
    def __init__(self, request, redis):
        self.request = request
        self.redis = redis

    # 序列化所有主机信息
    def by_hosts(self):
        '''
        serialize all the hosts
        :return:
        '''
        # 主机对象
        host_obj_list = models.Host.objects.all()
        # print("host_obj_list:", host_obj_list)
        host_data_list = []
        for h in host_obj_list:
            # 所有主机信息表
            host_data_list.append(self.single_host_info(h))
        # host_data_list = [data, data, data,...]
        return host_data_list

    # 序列化单个主机的信息，传入单个主机对象
    def single_host_info(self, host_obj):
        # print(host_obj.status_choices[0][1])
        data = {
            'id': host_obj.id,
            'name': host_obj.name,
            'ip_addr': host_obj.ip_addr,
            'host_group': host_obj.host_groups.select_related(),
            'status': host_obj.status_choices[host_obj.status-1][1],
            # 'status': host_obj.status,
            'uptime': None,
            'last_update': None,
            # 'total_services': None,
            # 'ok_nums': None,
        }
        # 获取主机的uptime
        uptime = self.get_host_uptime(host_obj)
        # self.get_triggers(host_obj)
        if uptime:
            # print('uptime:', uptime)
            data['uptime'] = uptime[0]['uptime']
            # print('mktime :', time.gmtime(uptime[1]))
            data['last_update'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(uptime[1]))

        return data

    # 获取主机的uptime
    def get_host_uptime(self, host_obj):
        redis_key = 'StatusData_%s_uptime_latest' % host_obj.id
        last_data_point = self.redis.lrange(redis_key, -1, -1)
        if last_data_point:
            last_data_point, last_update = json.loads(last_data_point[0])
            return last_data_point, last_update
