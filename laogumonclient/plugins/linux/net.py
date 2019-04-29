from psutil import *


def monitor():
    nic_list_data = net_io_counters(pernic=True, nowrap=False)

    value_dict = {
        # 'inet_name': '',
        'bytes_sent': '',
        'bytes_recv': '',
        'packets_sent': '',
        'packets_recv': '',
        'status': 0,
        'has_sub_dic': False,
        'is_info': 'False',
        # 'sub_dic_key': [],
    }

    # for nic_data_name in nic_list_data:
    # bytes_sent
    # bytes_sent = str(nic_list_data[nic_data_name][0])
    bytes_sent = str(nic_list_data['wlp2s0'][0])
    # bytes_recv
    # bytes_recv = str(nic_list_data[nic_data_name][1])
    bytes_recv = str(nic_list_data['wlp2s0'][1])
    # packets_sent
    # packets_sent = str(nic_list_data[nic_data_name][2])
    packets_sent = str(nic_list_data['wlp2s0'][2])
    # packets_recv
    # packets_recv = str(nic_list_data[nic_data_name][3])
    packets_recv = str(nic_list_data['wlp2s0'][3])

    value_dict['bytes_sent'] = bytes_sent
    value_dict['bytes_recv'] = bytes_recv
    value_dict['packets_sent'] = packets_sent
    value_dict['packets_recv'] = packets_recv


    print(value_dict)
    return value_dict
