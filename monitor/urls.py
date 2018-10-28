from django.conf.urls import url
from . import views, userviews

urlpatterns = [
  url(r'^$', userviews.index),
  url(r'^login/$', userviews.login_page),
  url(r'verifycode/$', userviews.verifycode),
  url(r'login_handle/$', userviews.user_login),
  url(r'logout_handle/$', userviews.user_logout),
  url(r'^dashboard/$', userviews.dashboard),
  url(r'^client_config/(\d+)/$', views.client_configs),
  url(r'^client_service_report/$', views.service_data_report),
  # url(r'hosts/status/$', views.hosts_status,name='get_hosts_status'),
  # url(r'groups/status/$', views.hostgroups_status,name='get_hostgroups_status'),
  # url(r'graphs/$', views.graphs_generator,name='get_graphs')
]
