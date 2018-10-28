# from __future__ import unicode_literals
from django.db import models
from . import auth
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy

#主机类
class Host(models.Model):
  #主机名
  name = models.CharField(u'主机名', max_length=64, unique=True)
  #ip地址
  ip_addr = models.GenericIPAddressField(u'IP地址', unique=True)
  #主机群组
  host_groups = models.ManyToManyField('HostGroup', verbose_name=u'主机组名', blank=True)
  #模板
  templates = models.ManyToManyField('Template', verbose_name=u'模板名', blank=True)
  #监控选项
  monitored_by_choices = (
    ('agent', 'Agent'),
    ('snmp', 'SNMP'),
    ('wget', 'WGET'),
  )
  #监控项
  monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
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

#主机组类
class HostGroup(models.Model):
  name = models.CharField(u'主机组名', max_length=64, unique=True)
  templates = models.ManyToManyField("Template", verbose_name=u'模板名', blank=True)
  memo = models.TextField(u"备注", blank=True, null=True)

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

#模板类
class Template(models.Model):
  name = models.CharField(u'模板名', max_length=64, unique=True)
  services = models.ManyToManyField('Service', verbose_name='服务列表')
  triggers = models.ManyToManyField('Trigger', verbose_name='触发器列表', blank=True)

  def __str__(self):
    return self.name

#触发器表达式类
class TriggerExpression(models.Model):
  trigger = models.ForeignKey('Trigger', verbose_name=u'所属触发器', on_delete=models.CASCADE)
  service = models.ForeignKey(Service, verbose_name=u'关联服务', on_delete=models.CASCADE)
  service_index = models.ForeignKey(ServiceIndex, verbose_name=u'关联服务指标', on_delete=models.CASCADE)
  specified_index_key = models.CharField(u'只监控专门指定的指标key', max_length=64, blank=True)
  operator_type_choices = (
    ('eq', '='),
    ('lt', '<'),
    ('gt', '>'),
  )
  operator_type = models.CharField(u'运算符', choices=operator_type_choices, max_length=64)
  data_calc_type_choices = (
    ('avg', 'Average'),
    ('max', 'Max'),
    ('hit', 'Hit'),
    ('last', 'Last'),
  )
  data_calc_func = models.CharField(u'数据处理方式', choices=data_calc_type_choices, max_length=64)
  data_calc_args = models.CharField(u'函数传入参数', help_text=u'逗号分隔多个参数', max_length=64)
  threshold = models.IntegerField(u'阈值')
  logic_type_choices = (
    ('or', 'OR'),
    ('and', 'AND'),
  )
  logic_type = models.CharField(u'与一个条件的逻辑关系', choices=logic_type_choices, max_length=32)

  def __str__(self):
    return "%s %s(%s(%s))" %(self.service_index, self.operator_type, self.data_calc_func, self.data_calc_args)

# 触发器类
class Trigger(models.Model):
  name = models.CharField(u'触发器名', max_length=64)
  severity_choices = (
    (1, 'Information'),
    (2, 'Warning'),
    (3, 'Average'),
    (4, 'High'),
    (5, 'Diaster'),
  )
  severity = models.IntegerField(u'告警级别', choices=severity_choices)
  enabled = models.BooleanField(default=True, verbose_name=u'是否开启')
  memo = models.TextField(u'备注', blank=True, null=True)

  def __str__(self):
    return "<service: %s, severity: %s>" %(self.name, self.severity)

# 动作类
class Action(models.Model):
  name = models.CharField(u'动作名', max_length=64, unique=True)
  host_groups = models.ManyToManyField('HostGroup', blank=True, verbose_name=u'主机组')
  hosts = models.ManyToManyField('Host', blank=True, verbose_name=u'主机')
  triggers = models.ManyToManyField('Trigger', blank=True, verbose_name=u'触发器', help_text=u"想让哪些trigger触发当前报警动作")
  conditions = models.TextField(u'告警条件')
  interval = models.IntegerField(u'告警间隔(s)', default=300)
  operations = models.ManyToManyField('ActionOperation', verbose_name=u'操作')
  recover_notice = models.BooleanField(u'故障恢复后发送通知消息', default=True)
  recover_subject = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'故障恢复后通知主题')
  recover_message = models.TextField(blank=True, null=True, verbose_name=u'故障恢复后通知消息')
  enabled = models.BooleanField(default=True, verbose_name=u'是否开启')

  def __str__(self):
    return self.name

# 动作实现类
class ActionOperation(models.Model):
  name = models.CharField(u'动作操作名', max_length=64)
  step = models.SmallIntegerField(u'第n次告警', default=1)
  action_type_choices = (
    ('email', 'Email'),
    ('sms', 'SMS'),
    ('script', 'RunScript'),
  )
  action_type = models.CharField(u'动作类型', choices=action_type_choices, max_length=64)
  # notifiers = models.ManyToManyField('UserProfile', verbose_name=u"通知对象", blank=True)
  default_msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''
  msg_format = models.TextField(u"消息格式", default=default_msg_format)

  def __str__(self):
    return self.name
#
# class Maintenance(models.Model):
#   name = models.CharField(max_length=64, unique=True)
#   hosts = models.ManyToManyField('Host', blank=True)
#   host_groups = models.ManyToManyField('HostGroup', blank=True)
#   content = models.TextField(u'维护内容')
#   start_time = models.DateTimeField()
#   end_time = models.DateTimeField()
#
#   def __str__(self):
#     return self.name
#
# # 事件日志类
# class EventLog(models.Model):
#   event_type_choices = (
#     (0, '报警事件'),
#     (1, '维护事件')
#   )
#   # 事件类型
#   event_type = models.SmallIntegerField(choices=event_type_choices, default=0)
#   host = models.ForeignKey("Host", on_delete=models.CASCADE)
#   trigger = models.ForeignKey("Trigger", blank=True, null=True, on_delete=models.CASCADE)
#   log = models.TextField(blank=True, null=True)
#   date = models.DateTimeField(auto_now_add=True)
#
#   def __str__(self):
#     return "host: %s  %s" % (self.host, self.log)
#
# # 通知用户类
# class UserProfile(auth.AbstractBaseUser, auth.PermissionsMixin):
#   email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
#   password = models.CharField(ugettext_lazy('password'), max_length=128,
#                               help_text=mark_safe('''<a class='btn-link' href='password'>重置密码</a>'''))
#   phone = models.BigIntegerField(blank=True, null=True)
#   weixin = models.CharField(max_length=64, blank=True, null=True)
#   is_active = models.BooleanField(default=True)
#   is_admin = models.BooleanField(default=False)
#   is_staff = models.BooleanField(
#     verbose_name='staff status',
#     default=True,
#     help_text='Designates whether the user can log into this admin site.',
#   )
#   name = models.CharField(max_length=32)
#   memo = models.TextField('备注', blank=True, null=True, default=None)
#   date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)
#   # 用户名填充
#   USERNAME_FIELD = 'email'
#   REQUIRED_FIELDS = ['name']
#
#   def get_full_name(self):
#     return self.email
#
#   def get_short_name(self):
#     return self.email
#
#   def __str__(self):
#     return self.email
#
#   def has_perms(self, perm, obj=None):
#     return True
#
#   # 是否允许该用户查看指定应用
#   def has_module_perms(self, app_label):
#     return True
#
#   # @property
#   # 该用户是管理员吗
#   def is_superuser(self):
#     return self.is_admin
#
#   objects = auth.UserManager()
#
#   class Meta:
#     verbose_name = '账户'
#     verbose_name_plural = '账户'