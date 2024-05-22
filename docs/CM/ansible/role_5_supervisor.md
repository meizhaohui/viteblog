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

- 1. 将miniconda安装程序上传到远程节点。
- 2. 校验miniconda安装程序SHA256散列值。
- 3. 指定miniconda安装目录，在非交互模式下安装miniconda。
- 4. 在conda环境下，创建supervisor虚拟环境。
- 5. 在supervisor虚拟环境下安装Python第三方包supervisor。
- 6. 复制supervisor进程管理工具配置文件`/etc/supervisord.conf`。
- 7. 创建目录`/etc/supervisord.d`，用于存放supervisor进程管理工具管理的应用配置文件。
- 8. 复制测试应用配置文件`app.ini`到目录`/etc/supervisord.d`中。
- 9. 复制启动文件`supervisord.service`到路径 `/usr/lib/systemd/system/supervisord.service`。
- 10. 启动supervisord服务。
- 11. 设置supervisor相关快捷命令。



### 1.3 规划

现在对以上11个任务进行分类，分成几个小的任务组。

- 可以将任务1-3分成一个任务组，用来安装miniconda，当独创建一个任务文件`miniconda.yaml`。
- 将任务4，创建supervisor虚拟环境，当作一个独立任务，创建任务文件`virtual_env.yaml`。
- 将任务5-10分成一个任务组，用来配置supervisor进程管理环境，创建任务文件`supervisor.yaml`。
- 最后，将任务11单独作为一个任务组，用来创建快捷命令，创建任务文件`alias.yaml`。

然后，再创建一个主任务配置文件`main.yml`，将以上四个子任务包括进来。

以下是最终完成后的文件结构：

```sh
[root@ansible ansible_playbooks]# tree roles/supervisor
roles/supervisor
├── defaults
│   └── main.yml
├── files
│   ├── app.ini
│   ├── Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
│   └── sha256info.txt
├── tasks
│   ├── alias.yaml
│   ├── main.yml
│   ├── miniconda.yaml
│   ├── supervisor.yaml
│   └── virtual_env.yaml
├── templates
│   ├── alias_supervisor.sh.j2
│   ├── condarc.j2
│   ├── supervisord.conf.j2
│   └── supervisord.service.j2
└── vars
    └── main.yml

5 directories, 14 files
[root@ansible ansible_playbooks]#
```

## 2. 任务编写

### 2.1 创建主机清单配置文件

我们测试时，使用的是三个虚拟机作为工作节点。因此我们可以编写主机清单配置文件`hosts.ini`，其内容如下：

```ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3
```

在我们编写测试角色相关配置文件时，可以仅使用某一个工作节点，待在这个工作节点上面将整个角色任务都能够正常跑通后，再将所有节点放开。

因此测试时，可以这样配置：

```ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
# 192.168.56.122 hostname=ansible-node2
# 192.168.56.123 hostname=ansible-node3
```

即，仅在第一个工作节点上面进行角色任务的编写。



### 2.2 创建剧本文件

创建一个剧本文件`supervisor.yml`，由该文件来调用角色任务，其内容如下：

```yaml
---
- hosts: supervisorhosts
  roles:
    - supervisor

```



### 2.3 角色任务main.yml

该配置文件用来定义角色中包含哪些子任务，`roles/supervisor/tasks/main.yml`配置内容如下：

```yaml
---
# supervisor角色任务
# 安装minicoda
- include: miniconda.yaml
# 创建虚拟环境
- include: virtual_env.yaml
# 配置supervisor进程管理工具
- include: supervisor.yaml
# 创建快捷命令
- include: alias.yaml

```

为了分步测试，比如，最开始只想测试【安装minicoda】这个任务，就可以将下面这个子任务注释掉，像下面这样：

```yaml
---
# supervisor角色任务
# 安装mincoda
- include: miniconda.yaml
# 创建虚拟环境
#- include: virtual_env.yaml
# 配置supervisor进程管理工具
#- include: supervisor.yaml
# 创建快捷命令
#- include: alias.yaml

```

这样的话，就可以将精力集中在自己关心的任务上，等前面的任务配置验证无误后，再将后面的任务的注释去掉，测试下一个任务。