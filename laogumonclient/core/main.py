from . import client
import subprocess


class command_handler(object):

    def __init__(self, sys_args):
        self.sys_args = sys_args
        # 如果参数小于2就退出，并打印帮助信息
        if len(self.sys_args) < 2:
            exit(self.help())
        self.command_allocator()

    def command_allocator(self):
        # 是否包含该class的属性，即start或stop
        if hasattr(self, self.sys_args[1]):
            func = getattr(self, self.sys_args[1])
            return func()
        else:
            self.help()

    def help(self):
        valid_commands = '''
    python -m monitor_client.bin.monitor [action] [args]
      start     start monitor client
      stop      stop monitor client
      '''
        exit(valid_commands)

    def start(self):
        print("开始监控客户端，按CTRL C中断")
        Client = client.ClientHandle()
        Client.forever_run()

    def stop(self):
        print("正在停止监控客户端")
        monitor_pid = subprocess.getoutput("ps -ef | grep  monitor_client.bin.monitor | head -1 | awk '{print $2}'")
        status = 1
        while status != 0:
            status, result = subprocess.getstatusoutput("kill {}".format(monitor_pid))
