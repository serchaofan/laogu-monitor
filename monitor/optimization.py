from django.conf import settings
import time
import json
import copy


class DataStore(object):
  def __init__(self, client_id, service_name, data, redis_obj):
    self.client_id = client_id
    self.service_name = service_name
    self.data = data
    self.redis_obj = redis_obj
    self.process_and_save()

  def data_slice(self, redis_key_name_latest, optimize_interval):
    # 拿所有数据，执行反而会快一些，因为存放在内存中计算
    # all_data是列表
    # all_data = [
    #   [{\"iowait\": \"0.00\",...."}, 1540111739.1343265],
    #   [{\iowait\":...."}, 1540111739.231],
    #   ....
    # ]
    all_data = self.redis_obj.lrange(redis_key_name_latest, 1, -1)
    # print(all_data)
    data_set = []
    for item in all_data:
      data = json.loads(item.decode())
      # print(data)
      if len(data) == 2:
        service_data, last_save_time = data
        # 每次都会将获取最近的间隔范围内的数据
        if time.time() - last_save_time <= optimize_interval:
          data_set.append(data)
        else:
          pass
    # data_set也是列表，与all_data类似，仅仅是选取最近时间间隔内的数据
    # print(data_set)
    return data_set

  def process_and_save(self):
    print("------------service data------------")
    # status为0，data有效
    if self.data['status'] == 0:
      for key, val in settings.DATA_OPTIMIZATION.items():
        optimize_interval, max_point = val
        redis_key_name = "monitor-%s-%s-%s" % (self.client_id, self.service_name, key)
        # 取出最新存入的一个point数据
        last_point = self.redis_obj.lrange(redis_key_name, -1, -1)
        # 如果没有这个数据（即刚开始运行，第一个间隔还没到）
        if not last_point:
          # rpush一个时间戳，并没有数据
          self.redis_obj.rpush(redis_key_name, json.dumps([None, time.time()]))
        # 如果数据更新interval为0，则立刻将data添加进去
        if optimize_interval == 0:
          self.redis_obj.rpush(redis_key_name, json.dumps([self.data, time.time()]))
        # 如果interval不为0，则要考虑什么时候要优化数据
        else:
          last_point_data, last_point_save_time = json.loads(self.redis_obj.lrange(redis_key_name, -1, -1)[0].decode())

          if (time.time() - last_point_save_time) >= optimize_interval:
            redis_key_name_latest = "monitor-%s-%s-latest" % (self.client_id, self.service_name)
            # 将最近interval中的数据都存放到data_set中
            data_set = self.data_slice(redis_key_name_latest, optimize_interval)
            if len(data_set) > 0:
              # 把data_set数据交给optimize_data函数优化处理
              optimized_data = self.optimize_data(data_set)
              # print(optimized_data)
              if optimized_data:
                self.redis_obj.rpush(redis_key_name, json.dumps([optimized_data, time.time()]))
          # 同时确保数据在redis中的存储数量不超过settings中指定 的值
          if self.redis_obj.llen(redis_key_name) >= max_point:
            self.redis_obj.lpop(redis_key_name)  # 删除最旧的一个数据

  def optimize_data(self, data_set):
    optimized_data = {}
    service_data_keys = data_set[0][0].keys()
    service_data_vals = data_set[0][0]
    # 若不存在子dic
    if service_data_vals['has_sub_dic'] == False:
      # 建立每个key的列表
      # optimized_data = {
      #   "CPU": [avg, max, min, mid]
      #   "user": [avg, max, min, mid]
      #   "nice": [avg, max, min, mid]
      # }
      tmp_optimized_data = {}
      for key in service_data_keys:
        if key == 'has_sub_dic':
          continue
        optimized_data[key] = []
      tmp_optimized_data = copy.deepcopy(optimized_data)
      # 分离data_set中的各个子列表，即[{\"iowait\": \"0.00\",...."}, 1540111739.1343265],
      # 获取service_data和last_save_time
      for service_data, last_save_time in data_set:
        # print(data_set)
        # 再分离service_data中每个子项，即iowait: XX, steal: XX ....
        # 分别存入data_key和data_val
        for data_key, data_val in service_data.items():
          if data_key == 'has_sub_dic':
            continue
          # print(data_key, data_val)
          try:
            tmp_optimized_data[data_key].append(round(float(data_val), 2))
            # print(tmp_optimized_data)
          except ValueError as e:
            print("----error", e)
            pass
        # tmp_optimized_data = {
        #    "CPU": [xx, xx ,xx ..],
        #    "user": [xx,xx,xx,xx....],
        #    "nice": [xx,xx,xx,xx...]
        # }
        # print("tmp_optimized_data", tmp_optimized_data)
        for item_key, item_val in tmp_optimized_data.items():
          item_avg = self.average_data(item_val)
          item_max = self.max_data(item_val)
          item_min = self.min_data(item_val)
          item_mid = self.mid_data(item_val)
          optimized_data[item_key] = [item_avg, item_max, item_min, item_mid]

    return optimized_data


  def average_data(self, data_list):
    if len(data_list) > 0:
      return sum(data_list) / len(data_list)
    else:
      return 0


  def max_data(self, data_list):
    if len(data_list) > 0:
      return max(data_list)
    else:
      return 0


  def min_data(self, data_list):
    if len(data_list) > 0:
      return min(data_list)
    else:
      return 0


  def mid_data(self, data_list):
    if len(data_list) > 0:
      data_list.sort()
      return data_list[int(len(data_list) / 2)]
    else:
      return 0
