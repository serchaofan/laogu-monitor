from django.contrib import messages
from . import form
import docker
from docker.errors import *
from docker import types


class ContainerDeploy(object):
    def __init__(self, request):
        self.client = docker.from_env()
        self.request = request

    def container_start(self, con_id):
        try:
            self.client.containers.get(con_id).start()
            messages.add_message(self.request, messages.SUCCESS, "Container: " + str(con_id) + " start SUCCESS")
        except APIError:
            messages.add_message(self.request, messages.ERROR, "Container: " + str(con_id) + " start Failed")

    def container_stop(self, con_id):
        try:
            self.client.containers.get(con_id).stop()
            messages.add_message(self.request, messages.SUCCESS, "Container: " + str(con_id) + " stop SUCCESS")
        except APIError:
            messages.add_message(self.request, messages.ERROR, "Container: " + str(con_id) + " stop Failed")

    def container_restart(self, con_id):
        try:
            self.client.containers.get(con_id).restart()
            messages.add_message(self.request, messages.SUCCESS, "Container: " + str(con_id) + " restart SUCCESS")
        except APIError:
            messages.add_message(self.request, messages.ERROR, "Container: " + str(con_id) + " restart Failed")

    def container_remove(self, con_id):
        try:
            self.client.containers.get(con_id).remove()
            messages.add_message(self.request, messages.SUCCESS, "Container: " + str(con_id) + " delete SUCCESS")
        except APIError:
            messages.add_message(self.request, messages.ERROR, "Container: " + str(con_id) + " delete Failed")

    # def container_run(self, para_dic):
    def container_run(self, image, name, ports, network, volumes, command, hostname, restart_policy, cpu_shares,
                      mem_limit, auto_remove=False):
        try:
            print("container_run------------")
            # print(para_dic)
            # print(para_dic['image'], para_dic['name'], para_dic['ports'], para_dic['volumes'])
            # print(para_dic['network'], para_dic['command'], para_dic['hostname'], para_dic['restart_policy'])
            # volumes看看能不能实现多个添加
            # self.client.containers.run(image=para_dic['image'],
            #                            name=para_dic['name'],
            #                            ports=para_dic['ports'],
            #                            network=para_dic['network'],
            #                            volumes=para_dic['volumes'],
            #                            command=para_dic['command'],
            #                            hostname=para_dic['hostname'],
            #                            auto_remove=para_dic['auto_remove'],
            #                            restart_policy=para_dic['restart_policy'],
            #                            cpu_shares=para_dic['cpu_shares'],
            #                            mem_limit=para_dic['mem_limit']
            #                            )
            self.client.containers.run(image=image,
                                       name=name,
                                       ports=ports,
                                       network=network,
                                       volumes=volumes,
                                       command=command,
                                       hostname=hostname,
                                       auto_remove=auto_remove,
                                       restart_policy=restart_policy,
                                       cpu_shares=cpu_shares,
                                       mem_limit=mem_limit,
                                       detach=True
                                       )
        except APIError as e:
            print("Container_run出错", e)


class ImageDeploy(object):
    def __init__(self, request):
        self.request = request
        self.client = docker.from_env()

    def image_delete(self, image_id):
        try:
            self.client.images.remove(image=image_id)
            messages.add_message(self.request, messages.SUCCESS, "镜像删除成功")
        except APIError as e:
            print(e)
            messages.add_message(self.request, messages.ERROR, "镜像删除失败")

    def image_search(self, image_name):
        image_list = []
        try:
            image_list = self.client.images.search(image_name)
        except APIError as e:
            print(e)

        return image_list

    def image_pull(self, image_name, image_tag):
        try:
            self.client.images.pull(image_name+":"+image_tag)
        except APIError as e:
            print(e)


class ConNetworkDeploy(object):
    def __init__(self, request):
        self.request = request
        self.client = docker.from_env()

    def network_delete(self, net_id):
        try:
            self.client.networks.get(net_id).remove()
        except APIError as e:
            print(e)

    def network_ipam_create(self, subnet, gateway):
        try:
            ipam_pool = types.IPAMPool(subnet=subnet, gateway=gateway)
            ipam_config = types.IPAMConfig(pool_configs=[ipam_pool])
            return ipam_config
        except APIError as e:
            print(e)

    def network_create(self, name, driver, scope, ipam_config):
        try:
            self.client.networks.create(name=name,
                                        scope=scope,
                                        driver=driver,
                                        ipam=ipam_config)
        except APIError as e:
            print(e)


class ConVolumeDeploy(object):
    def __init__(self, request):
        self.request = request
        self.client = docker.from_env()

    def volume_delete(self, volume_id):
        try:
            self.client.volumes.get(volume_id).remove()
        except APIError as e:
            print(e)

    def volume_create(self, name):
        try:
            self.client.volumes.create(name=name)
        except APIError as e:
            print(e)
