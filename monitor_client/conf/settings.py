configs = {
  'HostID': 1,
  "Server": "192.168.43.106",
  "ServerPort": 8000,
  "urls": {
    'get_configs': ['client_config', 'get'],
    'service_report': ['client_service_report/', 'post'],
  },
  # 请求超时时间
  'RequestTimeout': 30,
  # 默认更新时间5分钟
  'ConfigUpdateInterval': 300
}
