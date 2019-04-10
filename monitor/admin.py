from django.contrib import admin

from django import forms
from . import models

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class HostAdmin(admin.ModelAdmin):
    list_display = ('id',
                     'name',
                     'ip_addr',
                     'status'
                    )
    filter_horizontal = ('host_groups',
                         'templates'
                         )

class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ('name',
                    'interval',
                    'plugin_name'
                    )


admin.site.register(models.Host, HostAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.ServiceIndex)
