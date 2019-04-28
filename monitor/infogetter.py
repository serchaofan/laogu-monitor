from . import models
from psutil import *
import docker
import datetime

class InfoGetter(object):
    def __init__(self):
        self.client = docker.from_env()

    def index_top_info(self):
        '''
        index的最上面一块头的信息,包括:主机数、容器数、镜像数、网络数、数据卷数、磁盘数
        :return: 信息的字典
        '''
        host_obj_list = models.Host.objects.all()
        hosts_count_num = len(host_obj_list)

        containers_count_num = len(self.client.containers.list(all=True))
        images_count_num = len(self.client.images.list())
        networks_count_num = len(self.client.networks.list())
        volumes_count_num = len(self.client.volumes.list())

        top_info_dic = dict(
            hosts_count=hosts_count_num,
            containers_count=containers_count_num,
            images_count=images_count_num,
            networks_count=networks_count_num,
            volumes_count=volumes_count_num,
        )
        return top_info_dic

    def local_containers_info(self):
        containers_list = self.client.containers.list(all=True)
        return containers_list

    def local_images_info(self):
        images_list = self.client.images.list()
        return images_list

    def local_network_info(self):
        network_list = self.client.networks.list()
        return network_list

    def local_volume_info(self):
        volume_list = self.client.volumes.list()
        return volume_list

    def local_event_info(self):
        event_list = self.client.events(
            decode=True,
            until=(datetime.datetime.now() + datetime.timedelta(seconds=-5)),
            since=(datetime.datetime.now() + datetime.timedelta(days=-1))
        )
        event_list.close()
        # self.client.events.close()
        event_list_optimized = []

        for e in event_list:
            event_dic = {}
            event_dic['Type'] = e['Type']
            event_dic['Action'] = e['Action']
            event_dic['Actor'] = e['Actor']
            event_dic['scope'] = e['scope']
            event_dic['time'] = datetime.datetime.fromtimestamp(e['time']).strftime("%Y-%m-%d %H:%M:%S")
            event_list_optimized.append(event_dic)
            # print(event_dic)
        # print(event_list)
        # print(event_list_optimized)
        return event_list_optimized

    # def local_disk_info(self):
    #     disk_info_list = disk_partitions()
    #     disk_io_list = disk_io_counters()
    #
    #     return disk_list