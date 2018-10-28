import subprocess

def monitor(frist_invoke=1):
  vmstat_command = "vmstat | tail -n1"
  status, result = subprocess.getstatusoutput(vmstat_command)
  if status != 0:
    value_dic = {'status': status}
  else:
    swpd, free, buff, cache, si, so = result.split()[2:8]
    value_dic = {
      'swpd': swpd,
      'free': free,
      'buff': buff,
      'cache': cache,
      'si': si,
      'so': so,
      'status': status,
      'has_sub_dic': False
    }
  return value_dic