# laogu-monitor
类zabbix，open-falcon分布式监控系统，基于Django开发。刚开始学Django，只是边学边开发。

参考视频:[跟Alex学Python之- 如何写出NB吊炸天的分布式监控系统](http://edu.51cto.com/course/6208.html?source=so)

参考项目：
* [triaquae / CrazyMonitor](https://github.com/triaquae/CrazyMonitor)
* [open-falcon / falcon-plus](https://github.com/open-falcon/falcon-plus)
* [Mr-Linus / DCMP](https://github.com/Mr-Linus/DCMP)

* 采用的前端[puikinsh / gentelella](https://github.com/puikinsh/gentelella)，基于BootStrap与JQuery
* ~~采用的图表[highcharts / highcharts](https://github.com/highcharts/highcharts)~~
* 采用的图表echarts
* 采用的图标[FortAwesome / Font-Awesome](https://github.com/FortAwesome/Font-Awesome)

[开发日志](https://serchaofan.github.io/2018/10/09/Laogu-Monitor%E5%BC%80%E5%8F%91%E6%97%A5%E5%BF%97/)

目前的开发计划：
* 主机与主机组的管理监控
  * 主机CPU、内存、网络、负载
  * 主机的添加、删除、修改
* 服务的管理监控
  * 服务的添加、删除、修改
  * 服务的停止、启动等操作
* ~~模板的定义及应用~~
  * 主机的模板应用
  * 主机组的模板应用
  * 服务的模板应用
* ~~容器管理监控~~
  * 容器的创建、删除、修改
  * 镜像管理
  * 容器服务的监控
* 用户管理
  * 用户的添加、修改、删除
  * 用户等级划分
* ~~告警系统~~
  * 告警分类（根据服务或主机告警给不同用户）
  * 告警升级（设置阈值，对未能处理的告警进行等级提升，并通知更高一级的用户）
