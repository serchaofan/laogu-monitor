import time
from ..conf import settings
from urllib import request, parse, error
from urllib.error import HTTPError
import json
import threading
from ..plugins import plugin_api

class ClientHandle(object):
  def __init__(self):
    self.monitored_services = {}

  def load_latest_configs(self):
    '''
    load the latest monitor configs from monitor server
    :return:
    '''
    # 获取请求方式
    request_type = settings.configs['urls']['get_configs'][1]
    # 获取请求URL以及hostid
    url = "%s/%s" % (settings.configs['urls']['get_configs'][0], settings.configs['HostID'])
    print("url: %s" % url)
    latest_configs = json.loads(self.url_request(request_type, url).decode('utf-8'))
    print(latest_configs)
    self.monitored_services.update(latest_configs)

  def forever_run(self):
    '''
    start the client program forever
    :return:
    '''
    exit_flag = False
    # 上一次更新的时间
    config_last_update_time = 0
    while not exit_flag:
      if (time.time() - config_last_update_time) > settings.configs['ConfigUpdateInterval']:
        self.load_latest_configs()
        print("Loaded latest config:", self.monitored_services)
        # 将当前时间赋给更新时间
        config_last_update_time = time.time()
        print(config_last_update_time)

      for service_name, val in self.monitored_services['services'].items():
        # 若为2，则表示是第一次读取配置，因为还没加上最后一次更新的时间
        if len(val) == 2:
          self.monitored_services['services'][service_name].append(0)
        monitor_interval = val[1]
        last_invoke_time = val[2]
        if (time.time() - last_invoke_time) > monitor_interval:
          print(last_invoke_time, time.time())
          self.monitored_services['services'][service_name][2] = time.time()
          # 启动一个新线程去调用插件（就是获取系统信息的小函数）
          t = threading.Thread(target=self.invoke_plugin, args=(service_name, val))
          t.start()
          print("Going to monitor [%s]" % service_name)
        else:
          print(
            "Going to monitor [%s] in [%2.3f] secs" % (service_name, monitor_interval - (time.time() - last_invoke_time)))
      time.sleep(1)

  def invoke_plugin(self, service_name, val):
    '''
    invoke the monitor plugin here, and send the data to monitor server after plugin returned status data each time
    :param val: [pulgin_name,monitor_interval,last_run_time]
    :return:
    '''
    plugin_name = val[0]
    if hasattr(plugin_api, plugin_name):
      func = getattr(plugin_api, plugin_name)
      plugin_callback = func()
      # print("--monitor result:",plugin_callback)

      report_data = {
        'client_id': settings.configs['HostID'],
        'service_name': service_name,
        'data': json.dumps(plugin_callback)
      }

      request_type = settings.configs['urls']['service_report'][1]
      request_url = settings.configs['urls']['service_report'][0]

      # report_data = json.dumps(report_data)
      print('---report data:', report_data)
      self.url_request(request_type=request_type, url=request_url, params=report_data)
    else:
      print(
        "\033[31;1mCanngoing to start the monitor clientot find service [%s]'s plugin name [%s] in plugin_api\033[0m" % (
        service_name, plugin_name))
    print('--plugin:', val)

  def url_request(self, request_type, url, **extra_data):
    '''
    cope with monitor server by url
    :param action: "get" or "post"
    :param url: witch url you want to request from the monitor server
    :param extra_data: extra parameters needed to be submited
    :return:
    '''
    # 完整的URL
    abs_url = "http://%s:%s/%s" % (settings.configs['Server'],
                                   settings.configs["ServerPort"],
                                   url)
    print(abs_url)
    if request_type in ('get', 'GET'):
      # print(abs_url, extra_data)
      try:
        req = request.Request(abs_url)
        with request.urlopen(req, timeout=settings.configs['RequestTimeout']) as f:
          response = f.read()
        print("response: %s" % response)
        return response
      except error.URLError as e:
        exit("\033[31;1m%s\033[0m" % e)

    elif request_type in ('post', 'POST'):
      print(abs_url, extra_data['params'])
      try:
        data_encode = parse.urlencode(extra_data['params']).encode(encoding='UTF8')
        print(data_encode)
        req = request.Request(url=abs_url, data=data_encode)
        # print(req)
        with request.urlopen(req, timeout=settings.configs['RequestTimeout']) as f:
          response = f.read()
        response = json.loads(response.decode('utf-8'))
        print("\033[31;1m[%s]:[%s]\033[0m response:\n%s" % (request_type, abs_url, response))
        return response
      except HTTPError as e:
        print(e.read())
        print('---exec', e)
        exit("\033[31;1m%s\033[0m" % e)
