from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .deploy import ContainerDeploy, ImageDeploy, ConNetworkDeploy, ConVolumeDeploy
from .infogetter import InfoGetter
import json
import time


# docker操作（start、restart、stop、delete）
@csrf_exempt
def container_operate(request):
    con_deploy = ContainerDeploy(request)
    if request.method == 'POST':
        try:
            data = json.dumps(request.POST)
            con_shortid_list = json.loads(data)['con_shortid'].split(",")
            operation = json.loads(data)['operation']

            if operation == 'start':
                for con_shortid in con_shortid_list:
                    con_deploy.container_start(con_shortid)
            elif operation == 'stop':
                for con_shortid in con_shortid_list:
                    con_deploy.container_stop(con_shortid)
            elif operation == 'restart':
                for con_shortid in con_shortid_list:
                    con_deploy.container_restart(con_shortid)
            elif operation == 'delete':
                for con_shortid in con_shortid_list:
                    con_deploy.container_remove(con_shortid)
        except:
            print("出错")

    return redirect("/containerlist")


# docker创建操作
@csrf_exempt
def container_run(request):
    con_deploy = ContainerDeploy(request)
    if request.method == 'POST':
        try:
            print(request.POST)

            request_dic = {
                'image': '',
                'name': '',
                'cmd': '',
                'command': '',
                'hostname': '',
                'ports': '',
                'auto_remove': '',
                'cpu_shares': '',
                'mem_limit': '',
                'network': '',
                'volumes': '',
                'restart_policy': ''
            }
            if not request.POST['image']:
                messages.add_message(request, messages.ERROR, "必须指定镜像")
            else:
                request_dic['image'] = request.POST['image']
            if request.POST['name']:
                request_dic['name'] = request.POST['name']
            if request.POST['cmd']:
                request_dic['command'] = request.POST['cmd']
            if request.POST['hostname']:
                request_dic['hostname'] = request.POST['hostname']
            if 'autoremove' not in request.POST:
                request_dic['auto_remove'] = False
            elif 'autoremove' in request.POST:
                if request.POST['autoremove'] == 'on':
                    request_dic['auto_remove'] = True

            if request.POST['cpushares']:
                request_dic['cpu_shares'] = int(request.POST['cpushares'])
            if request.POST['memlimit']:
                request_dic['mem_limit'] = request.POST['memlimit']
            if request.POST['network']:
                request_dic['network'] = request.POST['network']

            if request.POST['localpath']:
                if not request.POST['bindpath']:
                    messages.add_message(request, messages.ERROR, "未指定绑定的容器目录")
                else:
                    volumes = {
                        "{}".format(request.POST['localpath']): {
                            "bind": "{}".format(request.POST['bindpath']),
                            "mode": "{}".format(request.POST['bind_option'])
                        }
                    }
                    request_dic['volumes'] = volumes

            if not request.POST['internal_port']:
                if not request.POST['exposed_port']:
                    pass
                else:
                    messages.add_message(request, messages.ERROR, "缺少容器内端口设置")
            else:
                if request.POST['exposed_port']:
                    ports = {
                        "{}/{}".format(request.POST['internal_port'], request.POST['protocol']): "{}".format(
                            request.POST['exposed_port'])
                    }
                else:
                    ports = {
                        "{}/{}".format(request.POST['internal_port'], request.POST['protocol']): "None"
                    }
                request_dic['ports'] = ports

            if request.POST['autorestart'] == 'always':
                restart_policy = {
                    "Name": "always"
                }
                request_dic['restart_policy'] = restart_policy
            elif request.POST['autorestart'] == 'on-failure':
                retryCount = int(request.POST['onfailure_num'])
                restart_policy = {
                    "Name": "on-failure",
                    "MaximumRetryCount": retryCount
                }
                request_dic['restart_policy'] = restart_policy

            print(request_dic)

            con_deploy.container_run(
                image=request_dic['image'],
                name=request_dic['name'],
                ports=request_dic['ports'],
                network=request_dic['network'],
                volumes=request_dic['volumes'],
                command=request_dic['command'],
                hostname=request_dic['hostname'],
                auto_remove=request_dic['auto_remove'],
                restart_policy=request_dic['restart_policy'],
                cpu_shares=request_dic['cpu_shares'],
                mem_limit=request_dic['mem_limit'],
            )

        except Exception as e:
            print("DeployView出错", e)
            pass
    time.sleep(3)
    return redirect("/containerlist")


# 镜像删除操作
@csrf_exempt
def image_delete_operation(request):
    image_deploy = ImageDeploy(request)
    print(request.POST)
    if request.method == 'POST':
        try:
            image_id_list = request.POST['image_id'].split(",")
            print(image_id_list)
            # print(image_id_list)
            for image_id in image_id_list:
                image_deploy.image_delete(image_id)
        except:
            print("Error")

    return redirect("/imagelist")


# 镜像操作（list和pull）
@csrf_exempt
def image_operate(request):
    image_deploy = ImageDeploy(request)
    if request.method == 'POST':
        # print(request.POST)
        image_name = request.POST['image_name']
        image_tag = request.POST['image_tag']
        # print(image_name)
        try:
            operation = request.POST['operation']
            if operation == 'search':
                image_list = image_deploy.image_search(image_name)
                context = {
                    'search_imagelist': image_list
                }
                return render(request, 'searchimagelist.html', context)
            elif operation == 'pull':
                if image_tag == '':
                    image_tag = 'latest'
                image_deploy.image_pull(image_name, image_tag)
                return redirect("/imagelist")
        except:
            print("Error")

    return redirect("/imagelist")


# 网络删除操作
@csrf_exempt
def network_delete_operation(request):
    network_deploy = ConNetworkDeploy(request)
    print(request.POST)
    if request.method == 'POST':
        try:

            network_id_list = request.POST['net_id'].split(",")
            print(network_id_list)
            for network_id in network_id_list:
                network_deploy.network_delete(network_id)
        except:
            print("Error")

    return redirect("/networklist")


# 网络创建操作
@csrf_exempt
def network_create_operation(request):
    network_deploy = ConNetworkDeploy(request)
    print(request.POST)
    if request.method == 'POST':
        try:
            ipam_config = network_deploy.network_ipam_create(subnet=request.POST['subnet'],
                                                             gateway=request.POST['gateway'])
            network_deploy.network_create(name=request.POST['name'],
                                          driver=request.POST['driver'],
                                          scope=request.POST['scope'],
                                          ipam_config=ipam_config)
        except Exception as e:
            print("Error", e)

    return redirect('/networklist')


# 数据卷删除操作
@csrf_exempt
def volume_delete_operation(request):
    volume_deploy = ConVolumeDeploy(request)
    if request.method == 'POST':
        volume_id_list = request.POST['vol_id'].split(",")
        try:
            for volume_id in volume_id_list:
                volume_deploy.volume_delete(volume_id)
        except Exception as e:
            print(e)
    return redirect('/volumelist')


# 数据卷创建操作
@csrf_exempt
def volume_create_operation(request):
    volume_deploy = ConVolumeDeploy(request)
    if request.method == 'POST':
        try:
            volume_deploy.volume_create(name=request.POST['name'])
        except Exception as e:
            print(e)

    return redirect('/volumelist')
