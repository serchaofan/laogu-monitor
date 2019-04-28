from . import models
from psutil import *
import docker


class InfoGetter(object):
    def __init__(self):
        self.client = docker.from_env()

    def index_top_info(self):
        host_obj_list = models.Host.objects.all()
        hosts_count_num = len(host_obj_list)

        containers_count_num = len(self.client.containers.list(all=True))
        images_count_num = len(self.client.images.list())
        top_info_dic = dict(
            hosts_count=hosts_count_num,
            containers_count=containers_count_num,
            images_count=images_count_num,
        )
        return top_info_dic

    def local_containers_info(self):
        containers_list = self.client.containers.list(all=True)
        return containers_list

    def local_images_info(self):
        images_list = self.client.images.list()
        return images_list