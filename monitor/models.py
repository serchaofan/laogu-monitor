from django.db import models


# 主机类
class Host(models.Model):
    # 主机名
    name = models.CharField(u'主机名', max_length=64, unique=True)
    # ip地址
    ip_addr = models.GenericIPAddressField(u'IP地址', unique=True)
    # #监控项
    # monitored_by = models.CharField(u'监控方式', max_length=64, choices=monitored_by_choices)
    # 主机组
    host_groups = models.ManyToManyField("HostGroup", blank=True, verbose_name="主机组")
    # 模板
    templates = models.ManyToManyField("Template", blank=True, verbose_name="模板")
    # 状态选项
    status_choices = (
        (1, 'Online'),
        (2, 'Down'),
        (3, 'Unreachable'),
        (4, 'Offline'),
    )
    # 状态，默认为Online
    status = models.IntegerField(u'状态', choices=status_choices, default=1)
    # 主机存活
    host_alive_check_interval = models.IntegerField(u"主机存活状态检测间隔", default=30)
    # 备注
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.name


# 主机组
class HostGroup(models.Model):
    name = models.CharField(u"主机组名", max_length=64, unique=True)
    templates = models.ManyToManyField("Template", blank=True, verbose_name="模板")
    memo = models.TextField(u"备注", blank=True, null=True)

    def __str__(self):
        return self.name


# 服务指标
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
        return "%s.%s" % (self.name, self.key)


# 服务类
class Service(models.Model):
    name = models.CharField(u'服务名', max_length=64, unique=True)
    interval = models.IntegerField(u'监控间隔', default=60)
    plugin_name = models.CharField(u'插件名', max_length=64)
    items = models.ManyToManyField('ServiceIndex', verbose_name=u'指标列表', blank=True)
    has_sub_service = models.BooleanField(default=False, verbose_name=u'是否有子服务')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


# 模板
class Template(models.Model):
    name = models.CharField(u'模版名称', max_length=64, unique=True)
    services = models.ManyToManyField('Service', verbose_name=u"服务列表")
    # triggers = models.ManyToManyField('Trigger', verbose_name=u"触发器列表", blank=True)

    def __str__(self):
        return self.name
