from .linux import cpu, mem

def get_linux_cpu():
  return cpu.monitor()

def get_linux_mem():
  return mem.monitor()