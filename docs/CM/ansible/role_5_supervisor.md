# 一步一步学role角色5-使用ansible配置supervisor进程管理角色



[[toc]]

## 1. 概述

这是一个序列总结文档。

- 第1节 [ansible role角色(1)](./role.md) 中，我们阅读了官方文档，并且知道了角色相关的概念。
- 第2节 [ansible role角色(2)--创建第一个role角色](./role_2.md) 创建一个简单的测试role角色。
- 第3节 [ansible role角色(3)--一步一步学role角色](./role_3.md)，base基础角色配置。
- 第4节 [ansible role角色(4)--include的使用](./role_4_include.md)，base基础角色配置优化，拆分任务功能，引入include关键字。

本节是在前几节的基础上，使用miniconda配置Python环境，对应Python版本为 3.10.13，并设置supervisor进程管理工具环境。引入`vars/main.yml`配置文件，设置变量配置信息。





### 1.1 VirtualBox虚拟机信息记录

| 序号 | 虚拟机         | 主机名  | IP             | CPU  | 内存 | 说明             |
| ---- | -------------- | ------- | -------------- | ---- | ---- | ---------------- |
| 1    | ansible-master | ansible | 192.168.56.120 | 2核  | 4G   | Ansible控制节点  |
| 2    | ansible-node1  | node1   | 192.168.56.121 | 2核  | 2G   | Ansible工作节点1 |
| 3    | ansible-node2  | node2   | 192.168.56.122 | 2核  | 2G   | Ansible工作节点2 |
| 4    | ansible-node3  | node3   | 192.168.56.123 | 2核  | 2G   | Ansible工作节点3 |




### 1.2. 回顾与展望

上节我编写了一个可以实际使用的base角色，但使用yum安装Python的版本（Python 3.6.8）较低，Python官方已经不再支持。因此本节就使用miniconda来配置高版本的Python。

本篇文章不介绍miniconda如何使用，miniconda的使用，可参考 [miniconda的使用](../../backend/python/miniconda.md) 。着重介绍如何创建supervisor进程管理角色。



该角色包含以下功能：

- 将miniconda安装程序上传到远程节点。
- 校验miniconda安装程序SHA256散列值。
- 指定miniconda安装目录，在非交互模式下安装miniconda。
- 在conda环境下，创建supervisor虚拟环境。
- 在supervisor虚拟环境下安装Python第三方包supervisor。
- 复制supervisor进程管理工具配置文件`/etc/supervisord.conf`。
- 创建目录`/etc/supervisord.d`，用于存放supervisor进程管理工具管理的应用配置文件。
- 复制测试应用配置文件`app.ini`到目录`/etc/supervisord.d`中。
- 复制启动文件`supervisord.service`到路径 `/usr/lib/systemd/system/supervisord.service`。
- 启动supervisord服务。
- 设置supervisor相关快捷命令。