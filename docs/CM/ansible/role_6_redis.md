# 一步一步学role角色6-使用ansible配置redis数据库角色



[[toc]]

## 1. 概述

这是一个序列总结文档。

- 第1节 [ansible role角色(1)](./role.md) 中，我们阅读了官方文档，并且知道了角色相关的概念。
- 第2节 [ansible role角色(2)--创建第一个role角色](./role_2.md) 创建一个简单的测试role角色。
- 第3节 [ansible role角色(3)--一步一步学role角色](./role_3.md)，base基础角色配置。
- 第4节 [ansible role角色(4)--include的使用](./role_4_include.md)，base基础角色配置优化，拆分任务功能，引入include关键字。
- 第5节 [ansible role角色5-使用ansible配置supervisor进程管理角色](./role_5_supervisor.md)，使用miniconda配置Python环境，对应Python版本为 3.10.13，并设置supervisor进程管理工具环境。引入`vars/main.yml`配置文件，设置变量配置信息。引入了默认变量、变量等配置，同样也将整个任务拆分成多个子任务。







### 1.1 VirtualBox虚拟机信息记录

| 序号 | 虚拟机         | 主机名  | IP             | CPU  | 内存 | 说明             |
| ---- | -------------- | ------- | -------------- | ---- | ---- | ---------------- |
| 1    | ansible-master | ansible | 192.168.56.120 | 2核  | 4G   | Ansible控制节点  |
| 2    | ansible-node1  | node1   | 192.168.56.121 | 2核  | 2G   | Ansible工作节点1 |
| 3    | ansible-node2  | node2   | 192.168.56.122 | 2核  | 2G   | Ansible工作节点2 |
| 4    | ansible-node3  | node3   | 192.168.56.123 | 2核  | 2G   | Ansible工作节点3 |




### 1.2. 回顾与展望

上节我编写了supervisor进程管理角色。

本篇我们在之前的supervisor进程管理角色的基础上，再来创建redis角色，用来在远程主机上面安装redis数据库。



该角色包含以下任务：

- 子任务1，redis安装与配置。包含以下事项：

  - 将编译好的redis-6.2.14.tar.gz复制到远程主机，并解压到/srv目录下。

  - 创建/srv/redis-6.2.14到/srv/redis的软链接，方便后面快速进程到redis目录下。

  - 创建/srv/redis下面的几个子目录，如conf存放配置文件、pid存放redis进程pid文件、logs日志文件和data redis数据文件夹。

  - 创建一个随机密码，用作redis的认证密码。

  - 复制配置文件到远程主机上面。

    

- 子任务2，sysctl配置。包含以下事项：

  - /etc/sysctl.conf中配置vm.overcommit_memory = 1，并使配置生效。

    

- 子任务3，supervisord应用配置。包含以下事项：

  - 将定义好的redis.ini.j2配置文件复制到远程主机的/etc/supervisord.d/redis.ini处。
  - 重启supervisord服务。



- 子任务4，设置redis相关快捷命令。包含以下事项：
  - 将定义好的alias_redis.sh.j2配置文件复制到远程主机的/root/.alias_redis.sh处。
  - .bashrc中重新加载自定义快捷命令的配置。



 创建一个主任务配置文件`main.yml`，将以上四个子任务包括进来。 



 以下是最终完成后的文件结构： 

```sh
[root@ansible ansible_playbooks]# tree roles/redis
roles/redis
├── defaults
│   └── main.yml
├── files
│   └── redis-6.2.14.tar.gz
├── tasks
│   ├── alias.yaml
│   ├── main.yml
│   ├── redis.yaml
│   ├── supervisor.yaml
│   └── sysctl.yaml
├── templates
│   ├── alias_redis.sh.j2
│   ├── redis.conf.j2
│   └── redis.ini.j2
└── vars
    └── main.yml

5 directories, 11 files
[root@ansible ansible_playbooks]#
```



## 2. 任务编写

### 2.1 创建主机清单配置文件

我们测试时，使用的是三个虚拟机作为工作节点。因此我们可以编写主机清单配置文件`hosts.ini`，其内容如下：

```ini
[redishosts]
192.168.56.121 hostname=ansible-node1
# 192.168.56.122 hostname=ansible-node2
```

在我们编写测试角色相关配置文件时，可以仅使用某一个工作节点，待在这个工作节点上面将整个角色任务都能够正常跑通后，再将所有节点放开。

因此测试时，可以这样配置：

```ini
[redishosts]
192.168.56.121 hostname=ansible-node1
# 192.168.56.122 hostname=ansible-node2
```

即，仅在第一个工作节点上面进行角色任务的编写。



### 2.2 创建剧本文件

创建一个剧本文件`redis.yml`，由该文件来调用角色任务，其内容如下：

```yaml
---
- hosts: redishosts
  roles:
    - redis

```



### 2.3 角色任务main.yml

该配置文件用来定义角色中包含哪些子任务，`roles/redis/tasks/main.yml`配置内容如下：

```yaml
---
# redis角色任务
# 安装redis
- include: redis.yaml
# 优化系统设置
- include: sysctl.yaml
# 使用supervisor进程管理工具配置redis app
- include: supervisor.yaml
# 创建快捷命令
- include: alias.yaml

```

为了分步测试，比如，最开始只想测试【安装redis】这个任务，就可以将下面这个子任务注释掉，像下面这样：

```yaml
---
# redis角色任务
# 安装redis
- include: redis.yaml
# 优化系统设置
# - include: sysctl.yaml
# 使用supervisor进程管理工具配置redis app
# - include: supervisor.yaml
# 创建快捷命令
# - include: alias.yaml
```

这样的话，就可以将精力集中在自己关心的任务上，等前面的任务配置验证无误后，再将后面的任务的注释去掉，测试下一个任务。



### 2.4 任务一-安装redis

这个任务，由`roles/redis/tasks/redis.yaml`定义，查看该文件内容：

```yaml
---
# 归档文件复制到远程主机时，会自动解压
- name: Unarchive the source package
  ansible.builtin.unarchive:
    src: redis-6.2.14.tar.gz
    dest: /srv
    remote_src: no

- name: Create a symbolic link
  ansible.builtin.file:
    src: /srv/redis-6.2.14
    dest: /srv/redis
    state: link

- name: Create a directory if it does not exist
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  with_items:
    - "{{ REDIS_BASE_DIR }}"
    - "{{ REDIS_BASE_DIR }}/conf"
    - "{{ REDIS_BASE_DIR }}/pid"
    - "{{ REDIS_BASE_DIR }}/logs"
    - "{{ REDIS_BASE_DIR }}/data"

- name: Create a random password
  ansible.builtin.set_fact:
    # 创建一个长度为32位的随机密码用作redis服务的认证密码
    REDIS_PASSWORD: "{{ lookup('ansible.builtin.password', '/dev/null length=32') }}"
  changed_when: false

- name: Display the redis password
  ansible.builtin.debug:
    msg: "{{ REDIS_PASSWORD }}"
  changed_when: false

- name: Copy redis.conf file
  ansible.builtin.template:
    src: redis.conf.j2
    dest: "{{ REDIS_BASE_DIR }}/conf/redis.conf"
    mode: '0600'
    force: yes
    remote_src: noredis 6.2.14
```

手动编译安装redis 6.2.14可参考 []()