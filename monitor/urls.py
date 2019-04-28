from django.conf.urls import url
from django.contrib import admin
from . import views, userview, graphview

urlpatterns = [
    # 主页（登录页）
    url(r'^$', userview.login_redirect),
    url(r'login/$', userview.login_page),
    # 登录处理
    url(r'login_handle/$', userview.user_login),
    # 登出处理
    url(r'logout_handle/$', userview.user_logout),
    # index面板（展示主页）
    # url(r'^index/$', userview.index),
    url(r'^index/$', graphview.demo1),
    url(r'^hostlist/$', views.hosts_status),
    url(r'^host/(\d+)/$', graphview.demo2),
    url(r'^containerlist/$', views.containers_status),
    url(r'^imagelist/$', views.images_status),
    url(r'^networklist/$', views.network_status),
    url(r'^volumelist/$', views.volume_status),
    url(r'^eventlist/$', views.event_status),
    # 客户端配置接收，d为主机号
    url(r'^client_config/(\d+)/$', views.client_configs),
    # 客户端服务数据处理
    url(r'^client_service_report/$', views.service_data_report),
    # url(r'^admin/$', userview.admin_page)
]
