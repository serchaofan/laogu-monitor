from django.contrib import admin
from django import forms
from .models import *


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    '''
    主机管理：
        主机id
        主机名
        主机IP地址
        主机状态
    '''
    list_display = (
        'id',
        'name',
        'ip_addr',
        'status'
    )
    filter_horizontal = ('host_groups', 'templates')



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    '''
    服务管理：
        服务名
        收集间隔（分钟）
        插件名
    '''
    filter_horizontal = ('items',)
    list_display = (
        'name',
        'interval',
        'plugin_name'
    )


@admin.register(ServiceIndex)
class ServiceIndexAdmin(admin.ModelAdmin):
    '''
    服务指标：
        监控项
        指标
        数据类型
    '''
    list_display = (
        'name',
        'key',
        'data_type'
    )


@admin.register(HostGroup)
class HostGroupAdmin(admin.ModelAdmin):
    '''
    主机组
        主机组名
        # 模板
    '''
    list_display = (
        'name',
        # 'templates'
    )
    filter_horizontal = ('templates',)


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    '''
    模板
        模板名
        # 服务
    '''
    list_display = (
        'name',
        # 'services'
    )
    filter_horizontal = (
        'services',
    )