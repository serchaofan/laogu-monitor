from .linux import cpu, mem, net


def get_linux_cpu():
    return cpu.monitor()


def get_linux_mem():
    return mem.monitor()


def get_linux_net():
    return net.monitor()
