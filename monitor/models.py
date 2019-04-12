# from __future__ import unicode_literals
from django.db import models
# from . import auth
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

#主机类
class Host(models.Model):
  #主机名
  name = models.CharField(u'主机名', max_length=64, unique=True)
  #ip地址
  ip_addr = models.GenericIPAddressField(u'IP地址', unique=True)
  # #监控项
  # monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
  #状态选项
  status_choices = (
    (1, 'Online'),
    (2, 'Down'),
    (3, 'Unreachable'),
    (4, 'Offline'),
  )
  #状态，默认为Online
  status = models.IntegerField(u'状态', choices=status_choices, default=1)
  #备注
  memo = models.TextField(u'备注', blank=True, null=True)

  def __str__(self):
    return self.name

#服务指标
class ServiceIndex(models.Model):
  # 要查看的项
  name = models.CharField(u'监控项', max_length=64)
  # 该项的某个指标（如：cpu为项name，cpu的idle为指标key）
  key = models.CharField(u'指标', max_length=64)
  data_type_choices = (
    ('int', 'int'),
    ('float', 'float'),
    ('str', 'string'),
  )
  data_type = models.CharField(u'指标数据类型', max_length=32, choices=data_type_choices)
  memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

  def __str__(self):
    return "%s.%s" %(self.name, self.key)

#服务类
class Service(models.Model):
  name = models.CharField(u'服务名', max_length=64, unique=True)
  interval = models.IntegerField(u'监控间隔', default=60)
  plugin_name = models.CharField(u'插件名', max_length=64, default='n/a')
  items = models.ManyToManyField('ServiceIndex', verbose_name=u'指标列表', blank=True)
  has_sub_service = models.BooleanField(default=False, verbose_name=u'是否有子服务', help_text=u'')
  memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

  def __str__(self):
    return self.name