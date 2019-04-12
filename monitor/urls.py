from django.conf.urls import url
from . import views, userviews

urlpatterns = [
  # 主页（登录页）
  url(r'^$', userviews.login_page),
  # 登录处理
  url(r'login_handle/$', userviews.user_login),
  # 登出处理
  url(r'logout_handle/$', userviews.user_logout),
  # dashboard面板（展示主页）
  url(r'^dashboard/$', userviews.dashboard),
  # 客户端配置接收，d为主机号
  url(r'^client_config/(\d+)/$', views.client_configs),
  # 客户端服务数据处理
  url(r'^client_service_report/$', views.service_data_report),
  # 所有主机的列表
  url(r'^hosts/$', views.hosts_status),
  # 单个主机详细监控页面
  url(r'^host_detail/(\d+)/$', views.host_detail)
]
