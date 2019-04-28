# laogu-monitor
类zabbix分布式监控系统，基于Django开发

参考视频:[跟Alex学Python之- 如何写出NB吊炸天的分布式监控系统](http://edu.51cto.com/course/6208.html?source=so)

参考项目：
* [triaquae / CrazyMonitor](https://github.com/triaquae/CrazyMonitor)
* [Mr-Linus / DCMP](https://github.com/Mr-Linus/DCMP)

* 前端模板[ColorlibHQ / gentelella](https://github.com/ColorlibHQ/gentelella)
* 图表[pyecharts / pyecharts](https://github.com/pyecharts/pyecharts)

目前的开发计划：
* 主机与主机组的管理监控        :ok_hand:
  * 主机CPU、内存、网络、负载
  * 主机的添加、删除、修改     
* 模板的定义及应用             :ok_hand:
  * 主机的模板应用
  * 主机组的模板应用
  * 服务的模板应用
* 容器管理监控(暂仅支持本地的容器)
  * 容器的管理
  * 镜像管理
  * 容器网络,数据卷管理
  * 容器服务的监控
* 用户管理                   :ok_hand:
  * 用户的添加、修改、删除
