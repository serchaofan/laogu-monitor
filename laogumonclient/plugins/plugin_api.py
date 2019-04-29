from .linux import cpu, mem, net, host_info


def get_linux_cpu():
    return cpu.monitor()


def get_linux_mem():
    return mem.monitor()


def get_linux_net():
    return net.monitor()


def get_host_info():
    return host_info.monitor()