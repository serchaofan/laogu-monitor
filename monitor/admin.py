from django.contrib import admin

from django import forms
from . import models

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class HostAdmin(admin.ModelAdmin):
    '''
    主机管理：
        主机id
        主机名
        主机IP地址
        主机状态
    '''
    list_display = ('id',
                    'name',
                    'ip_addr',
                    'status'
                    )

class ServiceAdmin(admin.ModelAdmin):
    '''
    服务管理：
        服务名
        收集间隔（分钟）
        插件名
    '''
    filter_horizontal = ('items',)
    list_display = ('name',
                    'interval',
                    'plugin_name'
                    )


admin.site.register(models.Host, HostAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceIndex)
