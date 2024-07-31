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

手动编译安装redis 6.2.14可参考 [CentOS7源码安装Redis6.2.14](../../database/redis/install_redis_with_source) 。redis-6.2.14.tar.gz 文件就是我编译好后打包后的压缩文件。

可以使用`tar -tvf`命令来查看一下压缩包里面的内容：

```sh
[root@ansible ansible_playbooks]# tar -tvf roles/redis/files/redis-6.2.14.tar.gz
drwxr-xr-x root/root         0 2024-06-10 18:25 redis-6.2.14/bin/
-rwxr-xr-x root/root   9548176 2024-06-10 18:25 redis-6.2.14/bin/redis-server
-rwxr-xr-x root/root   4830616 2024-06-10 18:25 redis-6.2.14/bin/redis-benchmark
-rwxr-xr-x root/root   5004728 2024-06-10 18:25 redis-6.2.14/bin/redis-cli
lrwxrwxrwx root/root         0 2024-06-10 18:25 redis-6.2.14/bin/redis-check-rdb -> redis-server
lrwxrwxrwx root/root         0 2024-06-10 18:25 redis-6.2.14/bin/redis-check-aof -> redis-server
lrwxrwxrwx root/root         0 2024-06-10 18:25 redis-6.2.14/bin/redis-sentinel -> redis-server
[root@ansible ansible_playbooks]#
```

本任务中使用了一些变量，是在`roles/redis/defaults/main.yml`定义的：

```sh
[root@ansible ansible_playbooks]# cat roles/redis/defaults/main.yml
---
# redis服务监听端口，默认6379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为29736
REDIS_LISTEN_PORT: 29736
# redis服务基础目录，会在访目录下面创建conf、pid、data、logs等目录，存放redis相关文件
REDIS_BASE_DIR: /srv/redis
[root@ansible ansible_playbooks]#
```

`roles/redis/defaults/main.yml`中定义角色使用的默认变量。



- `Create a random password`任务会创建一个随机密码，并保存到变量`REDIS_PASSWORD`中，
- `Copy redis.conf file`会复制配置文件`redis.conf.j2`到远程主机上面，并使用相关的变量渲染。



尝试执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] ****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]

TASK [redis : Unarchive the source package] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "-f", "/root/.ansible/tmp/ansible-tmp-1720532384.95-1737-6398051186844/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 86, "src": "/root/.ansible/tmp/ansible-tmp-1720532384.95-1737-6398051186844/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] ********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/redis", "mode": "0755", "owner": "root", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/conf", "mode": "0755", "owner": "root", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/pid", "mode": "0755", "owner": "root", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/logs", "mode": "0755", "owner": "root", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/data", "mode": "0755", "owner": "root", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 0}

TASK [redis : Create a random password] ******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"ansible_facts": {"REDIS_PASSWORD": "UFxwA2zDkOM2W5x5uredvHPvUTAbkFj1"}, "changed": false}

TASK [Display the redis password] ************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "UFxwA2zDkOM2W5x5uredvHPvUTAbkFj1"
}

TASK [Copy redis.conf file] ******************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "905b80c059e24c5c3c1255a11ae293f08db36738", "dest": "/srv/redis/conf/redis.conf", "gid": 0, "group": "root", "md5sum": "bcae9db950d9e4c1cd8cf30496e97c65", "mode": "0600", "owner": "root", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720532388.16-1803-239739885905907/source", "state": "file", "uid": 0}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=7    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 5 seconds
[root@ansible ansible_playbooks]#
```

可以看到，执行成功了。

![](/img/Snipaste_2024-07-09_21-41-06.png)

此时，在节点1上面检查一下：

```sh
[root@ansible-node1 ~]# ll /srv/redis
lrwxrwxrwx 1 root root 17 Jul  9 21:39 /srv/redis -> /srv/redis-6.2.14
[root@ansible-node1 ~]# ll /srv/redis-6.2.14
total 0
drwxr-xr-x 2 root root 134 Jun 10 18:25 bin
drwxr-xr-x 2 root root  24 Jul  9 21:39 conf
drwxr-xr-x 2 root root   6 Jul  9 21:39 data
drwxr-xr-x 2 root root   6 Jul  9 21:39 logs
drwxr-xr-x 2 root root   6 Jul  9 21:39 pid
[root@ansible-node1 ~]# ll /srv/redis/bin/
total 18936
-rwxr-xr-x 1 root root 4830616 Jun 10 18:25 redis-benchmark
lrwxrwxrwx 1 root root      12 Jun 10 18:25 redis-check-aof -> redis-server
lrwxrwxrwx 1 root root      12 Jun 10 18:25 redis-check-rdb -> redis-server
-rwxr-xr-x 1 root root 5004728 Jun 10 18:25 redis-cli
lrwxrwxrwx 1 root root      12 Jun 10 18:25 redis-sentinel -> redis-server
-rwxr-xr-x 1 root root 9548176 Jun 10 18:25 redis-server
[root@ansible-node1 ~]# grep -v '#' /srv/redis/conf/redis.conf |awk NF
bind 192.168.56.121 127.0.0.1
protected-mode no
port 29736
tcp-backlog 511
timeout 300
tcp-keepalive 300
daemonize no
pidfile /srv/redis/pid/redis_29736.pid
loglevel notice
logfile "/srv/redis/logs/redis_29736.log"
crash-log-enabled yes
databases 16
always-show-logo no
set-proc-title no
proc-title-template "{title} {listen-addr} {server-mode}"
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
rdb-del-sync-files no
dir /srv/redis/data
replica-serve-stale-data yes
replica-read-only yes
repl-diskless-sync no
repl-diskless-sync-delay 5
repl-diskless-load disabled
repl-disable-tcp-nodelay no
replica-priority 100
acllog-max-len 128
requirepass UFxwA2zDkOM2W5x5uredvHPvUTAbkFj1
maxmemory 1gb
lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no
lazyfree-lazy-user-del no
lazyfree-lazy-user-flush no
oom-score-adj no
oom-score-adj-values 0 200 800
disable-thp yes
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-load-truncated yes
aof-use-rdb-preamble yes
lua-time-limit 5000
slowlog-log-slower-than 10000
slowlog-max-len 128
latency-monitor-threshold 0
notify-keyspace-events ""
hash-max-ziplist-entries 512
hash-max-ziplist-value 64
list-max-ziplist-size -2
list-compress-depth 0
set-max-intset-entries 512
zset-max-ziplist-entries 128
zset-max-ziplist-value 64
hll-sparse-max-bytes 3000
stream-node-max-bytes 4096
stream-node-max-entries 100
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
hz 10
dynamic-hz yes
aof-rewrite-incremental-fsync yes
rdb-save-incremental-fsync yes
jemalloc-bg-thread yes
[root@ansible-node1 ~]#
```

可以看到，定义的变量都正常渲染了！并且也将剧本中临时生成的密码`UFxwA2zDkOM2W5x5uredvHPvUTAbkFj1`渲染到配置文件中了。说明我们配置没有问题。



### 2.5 任务二-优化系统设置

这个任务，由`roles/redis/tasks/sysctl.yaml`定义，查看该文件内容：

```yaml
---
# Set vm.overcommit_memory=1 in the sysctl file and reload if necessary
- ansible.posix.sysctl:
    name: vm.overcommit_memory
    value: '1'
    sysctl_set: true
    state: present
    reload: true
```



参考： [ansible.posix.sysctl module – Manage entries in sysctl.conf](https://docs.ansible.com/ansible/latest/collections/ansible/posix/sysctl_module.html#ansible-collections-ansible-posix-sysctl-module)

本节使用了一个第三方角色，使用前需要下载：

```sh
# 直接复制命令下载报错
[root@ansible ~]# ansible-galaxy collection install ansible.posix
Process install dependency map
ERROR! Unknown error when attempting to call Galaxy at 'https://galaxy.ansible.com/api/': <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:618)>
[root@ansible ~]# 

# 加上-ignore-cert忽略证书，下载成功
[root@ansible ~]# ansible-galaxy collection install ansible.posix --ignore-cert
Process install dependency map
Starting collection install process
Installing 'ansible.posix:1.5.4' to '/root/.ansible/collections/ansible_collections/ansible/posix'
[root@ansible ~]# 
```

【安装redis】这个任务我已经验证没什么问题了，现在只想测试第二个任务，像下面这样，把不关心的任务注释掉：

```yaml
---
# redis角色任务
# 安装redis
# - include: redis.yaml
# 优化系统设置
- include: sysctl.yaml
# 使用supervisor进程管理工具配置redis app
# - include: supervisor.yaml
# 创建快捷命令
# - include: alias.yaml
```

这样的话，就只用执行优化系统设置这一个任务了。



在执行任务前，我们将节点1上面的`vm.overcommit_memory`的值改成0：

```sh
[root@ansible-node1 ~]# vi /etc/sysctl.conf
[root@ansible-node1 ~]# sysctl -p
vm.overcommit_memory = 0
[root@ansible-node1 ~]# ll /etc/sysctl.conf
-rw-r--r-- 1 root root 474 Jul  9 21:50 /etc/sysctl.conf
[root@ansible-node1 ~]# 
```



然后执行一下剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] ****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]

TASK [redis : ansible.posix.sysctl] **********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 1 seconds
[root@ansible ansible_playbooks]#
```

![](/img/Snipaste_2024-07-09_21-55-00.png)



此时到节点1上面检查一下：

```sh
[root@ansible-node1 ~]# ll /etc/sysctl.conf
-rw-r--r-- 1 root root 472 Jul  9 21:51 /etc/sysctl.conf
[root@ansible-node1 ~]# cat /etc/sysctl.conf
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).
vm.overcommit_memory=1
[root@ansible-node1 ~]#
```

可以看到，文件时间和文件内容已经发生变化了的，说明剧本生效了。



### 2.6  任务三和任务四

- 任务三是使用supervisor进程管理工具配置redis app。
- 任务四是创建快捷命令。

与上一篇安装Supervisord服务并设置快捷命令没多大区别，此处就不多讲。

```sh
[root@ansible ansible_playbooks]# cat roles/redis/tasks/supervisor.yaml
---
- name: Copy redis app config
  ansible.builtin.template:
    src: redis.ini.j2
    dest: /etc/supervisord.d/redis.ini
    force: yes
    backup: yes
    remote_src: no

- name: Start service supervisord, in all cases
  ansible.builtin.service:
    name: supervisord
    state: restarted
    # 开机启动
    enabled: yes

[root@ansible ansible_playbooks]# cat roles/redis/tasks/alias.yaml
---
- name: Copy alias config
  ansible.builtin.template:
    src: alias_redis.sh.j2
    dest: /root/.alias_redis.sh
    force: yes
    backup: yes
    remote_src: no

- name: Insert block to .bashrc
  ansible.builtin.blockinfile:
    path: /root/.bashrc
    block: |
      source ~/.alias_redis.sh
    create: yes
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add redis alias"
    state: present

[root@ansible ansible_playbooks]#
```

像前几节一样，可以分别验证这两个任务。

### 2.7 复查所有任务

将`roles/redis/tasks/main.yml`配置的任务注释去掉，如下：

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

主机清单配置文件也把注释的节点放开：

可以这样配置：

```ini
[redishosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
```

即两个节点都生效。

**注意，执行剧本前，可以先把节点1之前生成的/srv/redis和/srv/redis-6.2.14目录都删除掉。避免重复执行。**

```sh
[root@ansible-node1 ~]# rm -rf /srv/redis /srv/redis-6.2.14
[root@ansible-node1 ~]# rm -f ~/.alias_redis.sh
[root@ansible-node1 ~]# sed -i '/vm.overcommit_memory/d' /etc/sysctl.conf
```





然后再次执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] ****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [redis : Unarchive the source package] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "-f", "/root/.ansible/tmp/ansible-tmp-1720534426.11-1919-220902181335175/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 86, "src": "/root/.ansible/tmp/ansible-tmp-1720534426.11-1919-220902181335175/source", "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "-f", "/root/.ansible/tmp/ansible-tmp-1720534426.13-1921-18869097021393/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1720534426.13-1921-18869097021393/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] ********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/redis", "mode": "0755", "owner": "root", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 0}
ok: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/redis", "mode": "0755", "owner": "root", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/conf", "mode": "0755", "owner": "root", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/conf", "mode": "0755", "owner": "root", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/pid", "mode": "0755", "owner": "root", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/pid", "mode": "0755", "owner": "root", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/logs", "mode": "0755", "owner": "root", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/logs", "mode": "0755", "owner": "root", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/data", "mode": "0755", "owner": "root", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/data", "mode": "0755", "owner": "root", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 0}

TASK [redis : Create a random password] ******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"ansible_facts": {"REDIS_PASSWORD": "VIUoyME7Ui5OYlsnIaT3UN5-4c9CjYKY"}, "changed": false}
ok: [192.168.56.122] => {"ansible_facts": {"REDIS_PASSWORD": "BvhIVZLLQm2QqAOyBNBQzUROncqscThE"}, "changed": false}

TASK [Display the redis password] ************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "VIUoyME7Ui5OYlsnIaT3UN5-4c9CjYKY"
}
ok: [192.168.56.122] => {
    "msg": "BvhIVZLLQm2QqAOyBNBQzUROncqscThE"
}

TASK [Copy redis.conf file] ******************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "232423869b718b8ae3e226b92eeda43eed2ffce0", "dest": "/srv/redis/conf/redis.conf", "gid": 0, "group": "root", "md5sum": "2e9a6427da0c5b876ca737186f7b9dce", "mode": "0600", "owner": "root", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720534429.71-2051-233067472987535/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "8fbd108ee64a21ea7bf62850a8c70b5f6f77bf3e", "dest": "/srv/redis/conf/redis.conf", "gid": 0, "group": "root", "md5sum": "e3449d4b407c6f15e152c2ed9464a1d8", "mode": "0600", "owner": "root", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720534429.75-2052-211039954829290/source", "state": "file", "uid": 0}

TASK [redis : ansible.posix.sysctl] **********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true}
changed: [192.168.56.121] => {"changed": true}

TASK [Copy redis app config] *****************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "c43bd01f7d0050a686a7c352fa473d0f6a58d091", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "md5sum": "0ffe83614ada33bad2c2bdcd8856f05f", "mode": "0644", "owner": "root", "size": 269, "src": "/root/.ansible/tmp/ansible-tmp-1720534431.88-2103-156545614617939/source", "state": "file", "uid": 0}
ok: [192.168.56.121] => {"changed": false, "checksum": "c43bd01f7d0050a686a7c352fa473d0f6a58d091", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/redis.ini", "size": 269, "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ***************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestampMonotonic": "0", "ActiveExitTimestampMonotonic": "0", "ActiveState": "failed", "After": "systemd-journald.socket basic.target rc-local.service nss-user-lookup.target system.slice", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Tue 2024-07-09 19:22:11 CST", "AssertTimestampMonotonic": "6057155", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Tue 2024-07-09 19:22:11 CST", "ConditionTimestampMonotonic": "6057155", "Conflicts": "shutdown.target", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "0", "ExecMainStartTimestampMonotonic": "0", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Tue 2024-07-09 19:22:11 CST] ; stop_time=[Tue 2024-07-09 19:22:11 CST] ; pid=653 ; code=exited ; status=2 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Tue 2024-07-09 19:22:11 CST", "InactiveEnterTimestampMonotonic": "6854781", "InactiveExitTimestamp": "Tue 2024-07-09 19:22:11 CST", "InactiveExitTimestampMonotonic": "6057338", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "0", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "exit-code", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "failed", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestampMonotonic": "0", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestampMonotonic": "0", "ActiveExitTimestampMonotonic": "0", "ActiveState": "failed", "After": "systemd-journald.socket basic.target rc-local.service nss-user-lookup.target system.slice", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Tue 2024-07-09 19:22:10 CST", "AssertTimestampMonotonic": "3247179", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Tue 2024-07-09 19:22:10 CST", "ConditionTimestampMonotonic": "3247179", "Conflicts": "shutdown.target", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "0", "ExecMainStartTimestampMonotonic": "0", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Tue 2024-07-09 19:22:10 CST] ; stop_time=[Tue 2024-07-09 19:22:11 CST] ; pid=644 ; code=exited ; status=2 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Tue 2024-07-09 19:22:11 CST", "InactiveEnterTimestampMonotonic": "4137458", "InactiveExitTimestamp": "Tue 2024-07-09 19:22:10 CST", "InactiveExitTimestampMonotonic": "3248006", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "0", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "exit-code", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "failed", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestampMonotonic": "0", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] *************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "9568b3d6831b8adda6c3101180229022", "mode": "0644", "owner": "root", "size": 389, "src": "/root/.ansible/tmp/ansible-tmp-1720534441.46-2148-207315589357348/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "9568b3d6831b8adda6c3101180229022", "mode": "0644", "owner": "root", "size": 389, "src": "/root/.ansible/tmp/ansible-tmp-1720534441.47-2150-102425360285898/source", "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] *******************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=12   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=12   changed=9    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 49 seconds
[root@ansible ansible_playbooks]#
```

![](/img/Snipaste_2024-07-09_22-14-59.png)

![](/img/Snipaste_2024-07-09_22-15-47.png)

此时，可以看到，两个节点上面的redis服务都正常启动了，快捷命令也可以用了：

![](/img/Snipaste_2024-07-09_22-19-00.png)

但此时，可以注意到，在不同节点上面生成了不同的密码。如果我们要配置主从节点，应该各节点设置的密码一样。



### 2.8 优化剧本

#### 2.8.1 只创建一次随机密码

上一节可以看到，剧本在两个节点分别创建了密码，这个时候就需要使用`delegate_to`指令，对`roles/redis/tasks/redis.yaml`任务进行修改，增加两行：

```yaml {32-35}
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
  # 委派给ansible控制节点
  delegate_to: localhost
  # 且只运行一次
  run_once: true

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
    remote_src: no

```

然后再次运行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] ****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [redis : Unarchive the source package] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "-f", "/root/.ansible/tmp/ansible-tmp-1720535344.71-2285-197418595161093/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 86, "src": "/root/.ansible/tmp/ansible-tmp-1720535344.71-2285-197418595161093/source", "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "-f", "/root/.ansible/tmp/ansible-tmp-1720535344.72-2287-5255114178761/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1720535344.72-2287-5255114178761/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] ********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/redis", "mode": "0755", "owner": "root", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 0}
ok: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/redis", "mode": "0755", "owner": "root", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/conf", "mode": "0755", "owner": "root", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/conf", "mode": "0755", "owner": "root", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/pid", "mode": "0755", "owner": "root", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/pid", "mode": "0755", "owner": "root", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/logs", "mode": "0755", "owner": "root", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/logs", "mode": "0755", "owner": "root", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/data", "mode": "0755", "owner": "root", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 0, "group": "root", "item": "/srv/redis/data", "mode": "0755", "owner": "root", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 0}

TASK [redis : Create a random password] ******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost] => {"ansible_facts": {"REDIS_PASSWORD": "O-podAqhbtChEpRpd:9tIciQR6FCqf9Y"}, "changed": false}

TASK [Display the redis password] ************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "O-podAqhbtChEpRpd:9tIciQR6FCqf9Y"
}
ok: [192.168.56.122] => {
    "msg": "O-podAqhbtChEpRpd:9tIciQR6FCqf9Y"
}

TASK [Copy redis.conf file] ******************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "35ac86dcf54667d9d2fa06a012402d8eb24e98ad", "dest": "/srv/redis/conf/redis.conf", "gid": 0, "group": "root", "md5sum": "8373fbc651001809d7ba9d2ab2711cba", "mode": "0600", "owner": "root", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720535348.03-2415-216445677843586/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "8220ed041e8fd61d568298e81f64568f50694f05", "dest": "/srv/redis/conf/redis.conf", "gid": 0, "group": "root", "md5sum": "2bb957d3393d9fc309aaf1dcfc0ffaf9", "mode": "0600", "owner": "root", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720535348.04-2416-59170465481199/source", "state": "file", "uid": 0}

TASK [redis : ansible.posix.sysctl] **********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}

TASK [Copy redis app config] *****************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "c43bd01f7d0050a686a7c352fa473d0f6a58d091", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/redis.ini", "size": 269, "state": "file", "uid": 0}
ok: [192.168.56.122] => {"changed": false, "checksum": "c43bd01f7d0050a686a7c352fa473d0f6a58d091", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/redis.ini", "size": 269, "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ***************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Tue 2024-07-09 22:13:53 CST", "ActiveEnterTimestampMonotonic": "10307598959", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "systemd-journald.socket basic.target rc-local.service nss-user-lookup.target system.slice", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Tue 2024-07-09 22:13:53 CST", "AssertTimestampMonotonic": "10307449900", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Tue 2024-07-09 22:13:53 CST", "ConditionTimestampMonotonic": "10307449900", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "4104", "ExecMainStartTimestamp": "Tue 2024-07-09 22:13:53 CST", "ExecMainStartTimestampMonotonic": "10307598919", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Tue 2024-07-09 22:13:53 CST] ; stop_time=[Tue 2024-07-09 22:13:53 CST] ; pid=4103 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Tue 2024-07-09 19:22:11 CST", "InactiveEnterTimestampMonotonic": "6854781", "InactiveExitTimestamp": "Tue 2024-07-09 22:13:53 CST", "InactiveExitTimestampMonotonic": "10307450210", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "4104", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Tue 2024-07-09 22:13:53 CST", "WatchdogTimestampMonotonic": "10307598938", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Tue 2024-07-09 22:14:01 CST", "ActiveEnterTimestampMonotonic": "10314359788", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "systemd-journald.socket basic.target rc-local.service nss-user-lookup.target system.slice", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Tue 2024-07-09 22:13:53 CST", "AssertTimestampMonotonic": "10306170387", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Tue 2024-07-09 22:13:53 CST", "ConditionTimestampMonotonic": "10306170387", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "2466", "ExecMainStartTimestamp": "Tue 2024-07-09 22:14:01 CST", "ExecMainStartTimestampMonotonic": "10314359771", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Tue 2024-07-09 22:13:53 CST] ; stop_time=[Tue 2024-07-09 22:14:01 CST] ; pid=2465 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Tue 2024-07-09 19:22:11 CST", "InactiveEnterTimestampMonotonic": "4137458", "InactiveExitTimestamp": "Tue 2024-07-09 22:13:53 CST", "InactiveExitTimestampMonotonic": "10306170689", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "2466", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Tue 2024-07-09 22:14:01 CST", "WatchdogTimestampMonotonic": "10314359780", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] *************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}
ok: [192.168.56.122] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] *******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.122] => {"changed": false, "msg": ""}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=12   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=11   changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 47 seconds
[root@ansible ansible_playbooks]#
```

此时，可以看到，`TASK [redis : Create a random password]`生成密码只运行了一次，并且两个节点的使用的密码是一样的，都是`O-podAqhbtChEpRpd:9tIciQR6FCqf9Y`，达到了我们想要的效果。

此时，可以在两个节点上面检查一下：

节点1上面执行命令：

```sh
[root@ansible-node1 ~]# spstatus
redis                            RUNNING   pid 5813, uptime 0:10:09
testapp                          RUNNING   pid 5814, uptime 0:10:09
[root@ansible-node1 ~]# redisStatus
root      5813  5804  0 22:29 ?        00:00:00 /srv/redis/bin/redis-server /srv/redis/conf/redis.conf
root      6452  4365  0 22:39 pts/0    00:00:00 grep --color=always --color=always redis-server
1
以上数字为1，则说明redis-server服务进程数正常
[root@ansible-node1 ~]# redisPort
tcp        0      0 127.0.0.1:29736         0.0.0.0:*               LISTEN      5813/redis-server
tcp        0      0 192.168.56.121:29736    0.0.0.0:*               LISTEN      5813/redis-server
正常监听 29736 则说明redis-server端口正常
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -p 29736
127.0.0.1:29736> auth O-podAqhbtChEpRpd:9tIciQR6FCqf9Y
OK
127.0.0.1:29736> info memory
# Memory
used_memory:874152
used_memory_human:853.66K
used_memory_rss:10579968
used_memory_rss_human:10.09M
used_memory_peak:874192
used_memory_peak_human:853.70K
used_memory_peak_perc:100.00%
used_memory_overhead:832640
used_memory_startup:812128
used_memory_dataset:41512
used_memory_dataset_perc:66.93%
allocator_allocated:1058040
allocator_active:1339392
allocator_resident:3788800
total_system_memory:8201236480
total_system_memory_human:7.64G
used_memory_lua:30720
used_memory_lua_human:30.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:1073741824
maxmemory_human:1.00G
maxmemory_policy:noeviction
allocator_frag_ratio:1.27
allocator_frag_bytes:281352
allocator_rss_ratio:2.83
allocator_rss_bytes:2449408
rss_overhead_ratio:2.79
rss_overhead_bytes:6791168
mem_fragmentation_ratio:12.70
mem_fragmentation_bytes:9746832
mem_not_counted_for_evict:4
mem_replication_backlog:0
mem_clients_slaves:0
mem_clients_normal:20504
mem_aof_buffer:8
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:0
master_failover_state:no-failover
master_replid:82c2cade691d623b36c38b60c85e8fb2044e68f4
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
127.0.0.1:29736> exit
[root@ansible-node1 ~]#
```

在节点2上面检查一下：

```sh
[root@ansible-node2 ~]# spstatus
redis                            RUNNING   pid 4130, uptime 0:10:06
testapp                          RUNNING   pid 4131, uptime 0:10:06
[root@ansible-node2 ~]# redisStatus
root      4130  3993  0 22:29 ?        00:00:00 /srv/redis/bin/redis-server /srv/redis/conf/redis.conf
root      4630  2620  0 22:39 pts/0    00:00:00 grep --color=always --color=always redis-server
1
以上数字为1，则说明redis-server服务进程数正常
[root@ansible-node2 ~]# redisPort
tcp        0      0 127.0.0.1:29736         0.0.0.0:*               LISTEN      4130/redis-server
tcp        0      0 192.168.56.122:29736    0.0.0.0:*               LISTEN      4130/redis-server
正常监听 29736 则说明redis-server端口正常
[root@ansible-node2 ~]# /srv/redis/bin/redis-cli -p 29736
127.0.0.1:29736> auth O-podAqhbtChEpRpd:9tIciQR6FCqf9Y
OK
127.0.0.1:29736> info memory
# Memory
used_memory:874152
used_memory_human:853.66K
used_memory_rss:10616832
used_memory_rss_human:10.12M
used_memory_peak:874192
used_memory_peak_human:853.70K
used_memory_peak_perc:100.00%
used_memory_overhead:832640
used_memory_startup:812128
used_memory_dataset:41512
used_memory_dataset_perc:66.93%
allocator_allocated:1058040
allocator_active:1339392
allocator_resident:3751936
total_system_memory:1927098368
total_system_memory_human:1.79G
used_memory_lua:30720
used_memory_lua_human:30.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:1073741824
maxmemory_human:1.00G
maxmemory_policy:noeviction
allocator_frag_ratio:1.27
allocator_frag_bytes:281352
allocator_rss_ratio:2.80
allocator_rss_bytes:2412544
rss_overhead_ratio:2.83
rss_overhead_bytes:6864896
mem_fragmentation_ratio:12.74
mem_fragmentation_bytes:9783696
mem_not_counted_for_evict:4
mem_replication_backlog:0
mem_clients_slaves:0
mem_clients_normal:20504
mem_aof_buffer:8
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:0
master_failover_state:no-failover
master_replid:2c6f61fe49950fc7e893c4c2e2b4faac325a53ea
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:0
second_repl_offset:-1
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
127.0.0.1:29736> exit
[root@ansible-node2 ~]#
```

可以看到，两个节点使用的认证密码都是`O-podAqhbtChEpRpd:9tIciQR6FCqf9Y`，正常认证并执行相关命令。

这样，多节点上面部署redis就配置成功了。

后续，再根据需要配置：

- redis主从配置。
- redis哨兵模式配置。
- redis集群模式配置。

待补充。

#### 2.8.2 修改redis启动用户

出于安全性的考虑，‌使用非root用户来启动Redis是推荐的。‌这样做可以避免一些潜在的安全风险，‌因为root用户拥有对系统的完全访问权限，‌如果Redis以root权限运行，‌攻击者可能会利用Redis对服务器文件进行任意操作或执行命令，‌从而对系统造成损害。‌因此，‌为了最大限度地提高系统的安全性，‌不建议以root用户的身份运行Redis。‌ 

 在实际操作中，‌可以通过创建非root用户（‌例如名为redis的用户）‌，‌并将Redis数据文件的所有者更换为该用户，‌然后使用该用户运行Redis。‌这样可以确保Redis在运行时具有适当的权限，‌同时保护系统免受潜在的安全威胁。‌ 



此处说明一下修改点。

- 修改默认配置`roles/redis/defaults/main.yml`，增加`REDIS_RUNNING_USER`默认变量：

```yaml {9-10}
---
# roles/redis/defaults/main.yml
# redis服务监听端口，默认6379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为29736
REDIS_LISTEN_PORT: 29736
# redis服务基础目录，会在访目录下面创建conf、pid、data、logs等目录，存放redis相关文件
REDIS_BASE_DIR: /srv/redis
# redis运行用户
REDIS_RUNNING_USER: redis

```

- 修改supervisor管理的redis应用的启动用户参数，配置`roles/redis/templates/redis.ini.j2`文件，增加`user = `<code v-pre>{{</code>` REDIS_RUNNING_USER }}` 行：

```ini {5}
# roles/redis/templates/redis.ini.j2
[program:redis]
command = {{ REDIS_BASE_DIR }}/bin/redis-server {{ REDIS_BASE_DIR }}/conf/redis.conf
directory = {{ REDIS_BASE_DIR }}
user = {{ REDIS_RUNNING_USER }}
stdout_logfile = {{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_LISTEN_PORT }}.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart=true

```

- 在使用redis用户前，需要创建这个用户，因此修改redis任务配置`roles/redis/tasks/redis.yaml`，增加一个`Add the user  with a specific shell`任务，并修改相关文件夹和文件的权限：

```yaml
---
# roles/redis/tasks/redis.yaml
- name: Add the user with a specific shell
  ansible.builtin.user:
    name: "{{ REDIS_RUNNING_USER }}"
    comment: Redis Database Server
    shell: /sbin/nologin

# 归档文件复制到远程主机时，会自动解压
- name: Unarchive the source package
  ansible.builtin.unarchive:
    src: redis-6.2.14.tar.gz
    dest: /srv
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

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
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
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
  # 委派给ansible控制节点
  delegate_to: localhost
  # 且只运行一次
  run_once: true

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
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

- name: Change the redis log file Permission
  ansible.builtin.file:
    path: "{{ item }}"
    state: file
    mode: '0644'
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  with_items:
    - "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_LISTEN_PORT }}.log"

```

以上修改完成后，就可以执行剧本来测试一下。

注意，在测试前，建议先将节点上原来的redis相关目录`/srv/redis`和`/srv/redis-6.2.14`等删除掉。

```sh
# 节点1操作
[root@ansible-node1 ~]# spstatus
redis                            RUNNING   pid 1519, uptime 23:07:27
testapp                          RUNNING   pid 1520, uptime 23:07:27
[root@ansible-node1 ~]# spctl stop redis
redis: stopped
[root@ansible-node1 ~]# rm -rf /srv/redis /srv/redis-6.2.14
[root@ansible-node1 ~]#
```

节点2上面也按以上相同方式处理。

有可能在测试过程中，会出现异常，这个时候就需要多次修改剧本文件，就会多次调整修改，删除节点上的测试文件等。

然后再执行剧本：

```sh

[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [redis : Add the user with a specific shell] *****************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "comment": "Redis Database Server", "create_home": false, "group": 1001, "home": "/home/redis", "name": "redis", "shell": "/sbin/nologin", "state": "present", "stderr": "Creating mailbox file: File exists\n", "stderr_lines": ["Creating mailbox file: File exists"], "system": false, "uid": 1001}
changed: [192.168.56.121] => {"changed": true, "comment": "Redis Database Server", "create_home": false, "group": 1001, "home": "/home/redis", "name": "redis", "shell": "/sbin/nologin", "state": "present", "stderr": "Creating mailbox file: File exists\n", "stderr_lines": ["Creating mailbox file: File exists"], "system": false, "uid": 1001}

TASK [redis : Unarchive the source package] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1720892475.46-3267-187039376278574/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1720892475.46-3267-187039376278574/source", "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1720892475.44-3266-256965943281383/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 62, "src": "/root/.ansible/tmp/ansible-tmp-1720892475.44-3266-256965943281383/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}

TASK [redis : Create a random password] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost] => {"ansible_facts": {"REDIS_PASSWORD": "9UyzE7Km2ew3ZX8JX3EWRlQA5fJtw10u"}, "changed": false}

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "9UyzE7Km2ew3ZX8JX3EWRlQA5fJtw10u"
}
ok: [192.168.56.122] => {
    "msg": "9UyzE7Km2ew3ZX8JX3EWRlQA5fJtw10u"
}

TASK [Copy redis.conf file] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "724885607cf69c99292ec62b3d9dfb36815d51f3", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "1255f971394eaee68eb6ad6e2874b183", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720892478.67-3396-244356909013993/source", "state": "file", "uid": 1001}
changed: [192.168.56.122] => {"changed": true, "checksum": "e396df9713d14d44a021b024056302c06092dee8", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "7ec835ec4b7f5860c27120c1c568ff55", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720892478.69-3397-270952059541256/source", "state": "file", "uid": 1001}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [redis : ansible.posix.sysctl] *******************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false}
ok: [192.168.56.122] => {"changed": false}

TASK [Copy redis app config] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "md5sum": "39a767bd4eacb07d785ca944d2f0fa5d", "mode": "0644", "owner": "root", "size": 320, "src": "/root/.ansible/tmp/ansible-tmp-1720892481.09-3464-11159189134831/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "md5sum": "39a767bd4eacb07d785ca944d2f0fa5d", "mode": "0644", "owner": "root", "size": 320, "src": "/root/.ansible/tmp/ansible-tmp-1720892481.11-3466-6292353932139/source", "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2024-07-14 10:08:26 CST", "ActiveEnterTimestampMonotonic": "53325677826", "ActiveExitTimestamp": "Sun 2024-07-14 10:08:26 CST", "ActiveExitTimestampMonotonic": "53325523344", "ActiveState": "active", "After": "system.slice rc-local.service nss-user-lookup.target systemd-journald.socket basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2024-07-14 10:08:26 CST", "AssertTimestampMonotonic": "53325553499", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2024-07-14 10:08:26 CST", "ConditionTimestampMonotonic": "53325553499", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "5312", "ExecMainStartTimestamp": "Sun 2024-07-14 10:08:26 CST", "ExecMainStartTimestampMonotonic": "53325677798", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Sun 2024-07-14 10:08:26 CST] ; stop_time=[Sun 2024-07-14 10:08:26 CST] ; pid=5311 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2024-07-14 10:08:26 CST", "InactiveEnterTimestampMonotonic": "53325553264", "InactiveExitTimestamp": "Sun 2024-07-14 10:08:26 CST", "InactiveExitTimestampMonotonic": "53325553830", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "5312", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Sun 2024-07-14 10:08:26 CST", "WatchdogTimestampMonotonic": "53325677813", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2024-07-14 10:08:34 CST", "ActiveEnterTimestampMonotonic": "53332114057", "ActiveExitTimestamp": "Sun 2024-07-14 10:08:26 CST", "ActiveExitTimestampMonotonic": "53323942123", "ActiveState": "active", "After": "nss-user-lookup.target rc-local.service systemd-journald.socket system.slice basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2024-07-14 10:08:26 CST", "AssertTimestampMonotonic": "53323967924", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2024-07-14 10:08:26 CST", "ConditionTimestampMonotonic": "53323967923", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "5298", "ExecMainStartTimestamp": "Sun 2024-07-14 10:08:34 CST", "ExecMainStartTimestampMonotonic": "53332114040", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Sun 2024-07-14 10:08:26 CST] ; stop_time=[Sun 2024-07-14 10:08:34 CST] ; pid=5296 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2024-07-14 10:08:26 CST", "InactiveEnterTimestampMonotonic": "53323967676", "InactiveExitTimestamp": "Sun 2024-07-14 10:08:26 CST", "InactiveExitTimestampMonotonic": "53323968246", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "5298", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Sun 2024-07-14 10:08:34 CST", "WatchdogTimestampMonotonic": "53332114048", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] **********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}
ok: [192.168.56.122] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "msg": ""}
ok: [192.168.56.121] => {"changed": false, "msg": ""}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=14   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=13   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 49 seconds
[root@ansible ansible_playbooks]#
```



![](/img/Snipaste_2024-07-14_10-25-06.png)

![](/img/Snipaste_2024-07-14_10-25-40.png)

此时，在节点上检查：

```sh
[root@ansible-node1 ~]# spstatus
redis                            RUNNING   pid 7092, uptime 0:03:31
testapp                          RUNNING   pid 7093, uptime 0:03:31
[root@ansible-node1 ~]# redisStatus
redis     7092  7083  0 10:23 ?        00:00:00 /srv/redis/bin/redis-server /srv/redis/conf/redis.conf
root      7236  1484  0 10:26 pts/0    00:00:00 grep --color=always --color=always redis-server
1
以上数字为1，则说明redis-server服务进程数正常
[root@ansible-node1 ~]# redisPort
tcp        0      0 127.0.0.1:29736         0.0.0.0:*               LISTEN      7092/redis-server
tcp        0      0 192.168.56.121:29736    0.0.0.0:*               LISTEN      7092/redis-server
正常监听 29736 则说明redis-server端口正常
[root@ansible-node1 ~]# cat /srv/redis/logs/redis_29736.log
7092:C 14 Jul 2024 10:23:08.516 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
7092:C 14 Jul 2024 10:23:08.516 # Redis version=6.2.14, bits=64, commit=00000000, modified=0, pid=7092, just started
7092:C 14 Jul 2024 10:23:08.516 # Configuration loaded
7092:M 14 Jul 2024 10:23:08.516 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
7092:M 14 Jul 2024 10:23:08.516 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
7092:M 14 Jul 2024 10:23:08.516 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
7092:M 14 Jul 2024 10:23:08.516 * monotonic clock: POSIX clock_gettime
7092:M 14 Jul 2024 10:23:08.516 * Running mode=standalone, port=29736.
7092:M 14 Jul 2024 10:23:08.516 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
7092:M 14 Jul 2024 10:23:08.516 # Server initialized
7092:M 14 Jul 2024 10:23:08.516 * Ready to accept connections
[root@ansible-node1 ~]#
```

可以看到，redis是用redis账号启动了，解决了启用用户的问题。



但这个时候，查看日志又提示了警告信息`Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.`。

解释如下：
第一行：Redis 建议把 open files 至少设置成10032，那么这个10032是如何来的呢？因为 maxclients 默认是10000，这些是用来处理客户端连接的，除此 之外，Redis 内部会使用最多32个文件描述符，所以这里的10032=10000+32。
第二行：Redis 不能将 open files 设置成10032，因为它没有权限设置。
第三行：当前系统的 open files 是4096，所以将 maxclients 设置成4096-32=4064个，如果你想设置更高的 maxclients，请使用 ulimit-n 来设置。
从上面的三行日志分析可以看出 open files 的限制优先级比 maxclients 大。 Open files 的设置方法如下： `ulimit –Sn {max-open-files}` 。

而在redis配置文件中，关于maxclients的配置说明如下：

```ini
# maxclients 10000
# BEGIN MEIZHAOHUI COMMENTS
#   设置同时连接的最大客户端数量。
#   默认情况下，此限制设置为 10000 个客户端。
#   但是如果 Redis 服务器无法配置进程文件限制以允许指定的限制，
#   则允许的最大客户端数量将设置为当前文件限制减 32（因为 Redis 保留了一些文件描述符供内部使用）。
#
#   一旦达到限制，Redis 将关闭所有新连接并发送错误"已达到最大客户端数量"。
#
#   重要提示：使用 Redis 集群时，最大连接数也与集群总线共享：
#   集群中的每个节点都将使用两个连接，一个传入，另一个传出。
#   如果集群非常大，则必须相应地调整限制的大小。
#   我们不单独设置。
# END MEIZHAOHUI COMMENTS
```



参考 [Why redis can not set maximum open file https://stackoverflow.com/questions/36880321/why-redis-can-not-set-maximum-open-file](https://stackoverflow.com/questions/36880321/why-redis-can-not-set-maximum-open-file)



只需要在以下配置中增加两行即可：

```
# /etc/security/limits.conf
redis soft nofile 10000
redis hard nofile 10000
```

此处说明一下修改点。

- 修改默认配置`roles/redis/defaults/main.yml`，增加`NET_CORE_SOMAXCONN_VALUE`和`REDIS_OPEN_FILES_VALUE`变量：

```yaml {11-21}
---
# roles/redis/defaults/main.yml
# redis服务监听端口，默认6379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为29736
REDIS_LISTEN_PORT: 29736
# redis服务基础目录，会在访目录下面创建conf、pid、data、logs等目录，存放redis相关文件
REDIS_BASE_DIR: /srv/redis
# redis运行用户
REDIS_RUNNING_USER: redis
# BEGIN MEIZHAOHUI COMMENTS
# net.core.somaxconn参数优化，与redis配置文件中tcp-backlog参数对应
#   在linux系统中控制tcp三次握手已完成连接队列的长度
#   在高并发系统中，你需要设置一个较高的tcp-backlog来避免客户端连接速度慢的问题（三次握手的速度）
#   取 /proc/sys/net/core/somaxconn 和 tcp-backlog 配置两者中的小值
#   对于负载很大的服务程序来说一般会将它修改为2048或者更大。
#   在/etc/sysctl.conf中添加:net.core.somaxconn = 2048，然后在终端中执行sysctl -p
# END MEIZHAOHUI COMMENTS
NET_CORE_SOMAXCONN_VALUE: 511
# redis open files
REDIS_OPEN_FILES_VALUE: 10032

```

- 修改系统设置任务`roles/redis/tasks/sysctl.yaml`:

```sh
---
# roles/redis/tasks/sysctl.yaml
# Set vm.overcommit_memory=1 in the sysctl file and reload if necessary
- name: Set vm.overcommit_memory value
  ansible.posix.sysctl:
    name: vm.overcommit_memory
    value: '1'
    sysctl_set: true
    state: present
    reload: true

# Set net.core.somaxconn in the sysctl file and reload if necessary
- name: Set net.core.somaxconn value
  ansible.posix.sysctl:
    name: net.core.somaxconn
    # 该参数系统默认值为128
    # 使用|string 过滤器转换一下，避免出现以下告警
    # [WARNING]: The value 511 (type int) in a string field was converted to u'511' (type string). 
    # If this does not look like what you expect, quote the entire value to ensure it does not change.
    value: "{{ NET_CORE_SOMAXCONN_VALUE|string }}"
    sysctl_set: true
    state: present
    reload: true

- name: Set redis open files
  ansible.builtin.blockinfile:
    path: /etc/security/limits.conf
    block: |
      {{ REDIS_RUNNING_USER }} soft nofile {{ REDIS_OPEN_FILES_VALUE }}
      {{ REDIS_RUNNING_USER }} hard nofile {{ REDIS_OPEN_FILES_VALUE }}
    insertbefore: "# End of file"

```

然后再执行剧本(**注意，此时注释了其他任务**)：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [redis : Set vm.overcommit_memory value] *********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": true}
ok: [192.168.56.121] => {"changed": true}

TASK [redis : Set net.core.somaxconn value] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": true}
ok: [192.168.56.122] => {"changed": true}

TASK [Set redis open files] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 34 seconds
[root@ansible ansible_playbooks]#
```

然后在节点检查：

```sh
[root@ansible-node1 ~]# cat /etc/sysctl.conf
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).
vm.overcommit_memory=1
net.core.somaxconn=511
[root@ansible-node1 ~]# cat /etc/security/limits.conf
# /etc/security/limits.conf
#
#This file sets the resource limits for the users logged in via PAM.
#It does not affect resource limits of the system services.
#
#Also note that configuration files in /etc/security/limits.d directory,
#which are read in alphabetical order, override the settings in this
#file in case the domain is the same or more specific.
#That means for example that setting a limit for wildcard domain here
#can be overriden with a wildcard setting in a config file in the
#subdirectory, but a user specific setting here can be overriden only
#with a user specific setting in the subdirectory.
#
#Each line describes a limit for a user in the form:
#
#<domain>        <type>  <item>  <value>
#
#Where:
#<domain> can be:
#        - a user name
#        - a group name, with @group syntax
#        - the wildcard *, for default entry
#        - the wildcard %, can be also used with %group syntax,
#                 for maxlogin limit
#
#<type> can have the two values:
#        - "soft" for enforcing the soft limits
#        - "hard" for enforcing hard limits
#
#<item> can be one of the following:
#        - core - limits the core file size (KB)
#        - data - max data size (KB)
#        - fsize - maximum filesize (KB)
#        - memlock - max locked-in-memory address space (KB)
#        - nofile - max number of open file descriptors
#        - rss - max resident set size (KB)
#        - stack - max stack size (KB)
#        - cpu - max CPU time (MIN)
#        - nproc - max number of processes
#        - as - address space limit (KB)
#        - maxlogins - max number of logins for this user
#        - maxsyslogins - max number of logins on the system
#        - priority - the priority to run user process with
#        - locks - max number of file locks the user can hold
#        - sigpending - max number of pending signals
#        - msgqueue - max memory used by POSIX message queues (bytes)
#        - nice - max nice priority allowed to raise to values: [-20, 19]
#        - rtprio - max realtime priority
#
#<domain>      <type>  <item>         <value>
#

#*               soft    core            0
#*               hard    rss             10000
#@student        hard    nproc           20
#@faculty        soft    nproc           20
#@faculty        hard    nproc           50
#ftp             hard    nproc           0
#@student        -       maxlogins       4

# BEGIN ANSIBLE MANAGED BLOCK
redis soft nofile 10032
redis hard nofile 10032
# END ANSIBLE MANAGED BLOCK
# End of file
[root@ansible-node1 ~]#
```

经过一翻折腾，发现重启多次仍然提示 open files 异常。

搜索后参考 [使用supervisor启动进程open files too many问题](https://blog.csdn.net/aninstein/article/details/131786807)

原来是supervisord的坑。修改`/usr/lib/systemd/system/supervisord.service`:

```ini {10-11}
# /usr/lib/systemd/system/supervisord.service
[Unit]
Description=Process Monitoring and Control Daemon
After=rc-local.service nss-user-lookup.target

[Service]
Type=forking
# ExecStart=/usr/bin/supervisord -c /etc/supervisord.conf
ExecStart=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf
# LimitNOFILE或LimitNPROC参数设置为infinity时，表示容器单进程最大文件句柄数为1048576
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target

```

即增加10-11行的内容。

```sh
[root@ansible-node1 ~]# systemctl daemon-reload
```

重新加载配置。

然后再执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [redis : Add the user with a specific shell] *****************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "comment": "Redis Database Server", "create_home": false, "group": 1001, "home": "/home/redis", "name": "redis", "shell": "/sbin/nologin", "state": "present", "stderr": "Creating mailbox file: File exists\n", "stderr_lines": ["Creating mailbox file: File exists"], "system": false, "uid": 1001}
changed: [192.168.56.121] => {"changed": true, "comment": "Redis Database Server", "create_home": false, "group": 1001, "home": "/home/redis", "name": "redis", "shell": "/sbin/nologin", "state": "present", "stderr": "Creating mailbox file: File exists\n", "stderr_lines": ["Creating mailbox file: File exists"], "system": false, "uid": 1001}

TASK [redis : Unarchive the source package] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1720903688.19-4911-200924152103276/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1720903688.19-4911-200924152103276/source", "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1720903688.18-4910-187976715343617/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 62, "src": "/root/.ansible/tmp/ansible-tmp-1720903688.18-4910-187976715343617/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}

TASK [redis : Create a random password] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost] => {"ansible_facts": {"REDIS_PASSWORD": "qTukR4-AEs-f2UnbUZcb1YCuRL2jm-Z_"}, "changed": false}

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "qTukR4-AEs-f2UnbUZcb1YCuRL2jm-Z_"
}
ok: [192.168.56.122] => {
    "msg": "qTukR4-AEs-f2UnbUZcb1YCuRL2jm-Z_"
}

TASK [Copy redis.conf file] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "3e91e16b1aba6f87b19fd22cc84ad34ee9013f9d", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "c0e6ce087349b14144be60bdbcebc0ef", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720903691.73-5041-236608481155038/source", "state": "file", "uid": 1001}
changed: [192.168.56.121] => {"changed": true, "checksum": "323e883d1b8109f1ca2992f98498193b60539217", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "42206af1e348d80d318c3fbe1aebf16f", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1720903691.69-5040-52013618510395/source", "state": "file", "uid": 1001}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [redis : Set vm.overcommit_memory value] *********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}

TASK [redis : Set net.core.somaxconn value] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}

TASK [Set redis open files] ***************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "msg": ""}
ok: [192.168.56.121] => {"changed": false, "msg": ""}

TASK [Copy redis app config] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "md5sum": "39a767bd4eacb07d785ca944d2f0fa5d", "mode": "0644", "owner": "root", "size": 320, "src": "/root/.ansible/tmp/ansible-tmp-1720903695.15-5146-269746074010550/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "md5sum": "39a767bd4eacb07d785ca944d2f0fa5d", "mode": "0644", "owner": "root", "size": 320, "src": "/root/.ansible/tmp/ansible-tmp-1720903695.14-5144-84941134135140/source", "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2024-07-14 13:25:57 CST", "ActiveEnterTimestampMonotonic": "2229887468", "ActiveExitTimestamp": "Sun 2024-07-14 13:25:57 CST", "ActiveExitTimestampMonotonic": "2229746282", "ActiveState": "active", "After": "systemd-journald.socket basic.target nss-user-lookup.target system.slice rc-local.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2024-07-14 13:25:57 CST", "AssertTimestampMonotonic": "2229770166", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2024-07-14 13:25:57 CST", "ConditionTimestampMonotonic": "2229770165", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "4619", "ExecMainStartTimestamp": "Sun 2024-07-14 13:25:57 CST", "ExecMainStartTimestampMonotonic": "2229887451", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Sun 2024-07-14 13:25:57 CST] ; stop_time=[Sun 2024-07-14 13:25:57 CST] ; pid=4618 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2024-07-14 13:25:57 CST", "InactiveEnterTimestampMonotonic": "2229769965", "InactiveExitTimestamp": "Sun 2024-07-14 13:25:57 CST", "InactiveExitTimestampMonotonic": "2229770846", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "4619", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Sun 2024-07-14 13:25:57 CST", "WatchdogTimestampMonotonic": "2229887460", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2024-07-14 13:27:50 CST", "ActiveEnterTimestampMonotonic": "3289058094", "ActiveExitTimestamp": "Sun 2024-07-14 13:27:41 CST", "ActiveExitTimestampMonotonic": "3280837027", "ActiveState": "active", "After": "rc-local.service system.slice systemd-journald.socket nss-user-lookup.target basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2024-07-14 13:27:42 CST", "AssertTimestampMonotonic": "3280930436", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2024-07-14 13:27:42 CST", "ConditionTimestampMonotonic": "3280930436", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "3847", "ExecMainStartTimestamp": "Sun 2024-07-14 13:27:50 CST", "ExecMainStartTimestampMonotonic": "3289058072", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Sun 2024-07-14 13:27:42 CST] ; stop_time=[Sun 2024-07-14 13:27:50 CST] ; pid=3846 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2024-07-14 13:27:42 CST", "InactiveEnterTimestampMonotonic": "3280930185", "InactiveExitTimestamp": "Sun 2024-07-14 13:27:42 CST", "InactiveExitTimestampMonotonic": "3280931240", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "3847", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Sun 2024-07-14 13:27:50 CST", "WatchdogTimestampMonotonic": "3289058084", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] **********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}
ok: [192.168.56.121] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.122] => {"changed": false, "msg": ""}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=16   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=15   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 51 seconds
[root@ansible ansible_playbooks]#
```

此时查看节点redis运行情况和日志信息：

```sh
[root@ansible-node1 ~]# spstatus
redis                            RUNNING   pid 5980, uptime 0:02:52
testapp                          RUNNING   pid 5981, uptime 0:02:52
[root@ansible-node1 ~]# redisStatus
redis     5980  5970  0 13:30 ?        00:00:00 /srv/redis/bin/redis-server /srv/redis/conf/redis.conf
root      6259  1482  0 13:32 pts/0    00:00:00 grep --color=always --color=always redis-server
1
以上数字为1，则说明redis-server服务进程数正常
[root@ansible-node1 ~]# redisPort
tcp        0      0 127.0.0.1:29736         0.0.0.0:*               LISTEN      5980/redis-server
tcp        0      0 192.168.56.121:29736    0.0.0.0:*               LISTEN      5980/redis-server
正常监听 29736 则说明redis-server端口正常
[root@ansible-node1 ~]# cat /srv/redis/logs/redis_29736.log
5980:C 14 Jul 2024 13:30:02.524 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
5980:C 14 Jul 2024 13:30:02.524 # Redis version=6.2.14, bits=64, commit=00000000, modified=0, pid=5980, just started
5980:C 14 Jul 2024 13:30:02.524 # Configuration loaded
5980:M 14 Jul 2024 13:30:02.525 * monotonic clock: POSIX clock_gettime
5980:M 14 Jul 2024 13:30:02.525 * Running mode=standalone, port=29736.
5980:M 14 Jul 2024 13:30:02.525 # Server initialized
5980:M 14 Jul 2024 13:30:02.526 * Ready to accept connections
[root@ansible-node1 ~]#
```

可以看到redis正常运行，并且日志中没有异常警告信息。



## 3. Redis多节点集群配置

### 3.1 Redis主从模式配置

在前面的讲解中，ansible使用redis角色剧本，可以在各节点上面创建并启动一个redis实例，相互之间没有关联。

假设我们已经使用前面的剧本将三个节点上面的redis正常启动了。

我们手动配置一下主机模式。


| 序号 | 虚拟机        | IP             | 角色             |
| ---- | ------------- | -------------- | ---------------- |
| 1    | ansible-node1 | 192.168.56.121 | Redis master主   |
| 2    | ansible-node2 | 192.168.56.122 | Redis slave1 从1 |
| 3    | ansible-node3 | 192.168.56.123 | Redis slave2 从2 |

一主多从架构图：

![](/img/Snipaste_2024-07-21_14-57-34.png)

我们只需要在Redis slave1和Redis slave2节点上面修改一下配置：

```sh
[root@ansible-node2 ~]# grep -C3 'replicaof <masterip> <masterport>' /srv/redis/conf/redis.conf
#    network partition replicas automatically try to reconnect to masters
#    and resynchronize with them.
#
# replicaof <masterip> <masterport>
# BEGIN MEIZHAOHUI COMMENTS
#   关于 Redis 复制，有几件事需要尽快了解。
#   1) Redis 复制是异步的，但您可以配置主服务器，如果它似乎与至少给定数量的副本没有连接，则停止接受写入。
[root@ansible-node2 ~]# grep -C3 'masterauth <master-password>' /srv/redis/conf/redis.conf
# starting the replication synchronization process, otherwise the master will
# refuse the replica request.
#
# masterauth <master-password>
#
# BEGIN MEIZHAOHUI COMMENTS
#   masterauth配置指令用于设置连接到主节点（如果Redis实例是复制的从节点）时所需的密码。
[root@ansible-node2 ~]#
```

- 在`# replicaof <masterip> <masterport>` 上一行增加`replicaof 192.168.56.121 29736`。
- 在`# masterauth <master-password>` 上一行增加`masterauth .N5VknxU0L4DbLsB,b.LOd6UJKULzYIe`。

注意上面的`masterauth`后面的密码可以在配置文件里面查`requirepass`的值查到。

配置后，然后重启节点redis服务：

```sh
# 节点2和节点3做相同的操作
[root@ansible-node2 ~]# spstatus
redis                            RUNNING   pid 2629, uptime 0:14:51
testapp                          RUNNING   pid 2630, uptime 0:14:51
[root@ansible-node2 ~]# spctl restart redis
redis: stopped
redis: started
[root@ansible-node2 ~]# spstatus
redis                            RUNNING   pid 2661, uptime 0:00:04
testapp                          RUNNING   pid 2630, uptime 0:14:59
[root@ansible-node2 ~]#
```

此时，如果查看日志提示以下异常，则说明各节点防火墙不通：

```sh
2661:S 15 Jul 2024 21:52:40.252 * Ready to accept connections
2661:S 15 Jul 2024 21:52:40.254 * Connecting to MASTER 192.168.56.121:29736
2661:S 15 Jul 2024 21:52:40.254 * MASTER <-> REPLICA sync started
2661:S 15 Jul 2024 21:52:40.254 # Error condition on socket for SYNC: No route to host
```

**此时应在三个节点防火墙放行Redis的29736端口**：

```sh
[root@ansible-node1 ~]# systemctl status firewalld
● firewalld.service - firewalld - dynamic firewall daemon
   Loaded: loaded (/usr/lib/systemd/system/firewalld.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2024-07-15 21:31:03 CST; 25min ago
     Docs: man:firewalld(1)
 Main PID: 662 (firewalld)
   CGroup: /system.slice/firewalld.service
           └─662 /usr/bin/python2 -Es /usr/sbin/firewalld --nofork --nopid

Jul 15 21:31:02 ansible-node1 systemd[1]: Starting firewalld - dynamic firewall daemon...
Jul 15 21:31:03 ansible-node1 systemd[1]: Started firewalld - dynamic firewall daemon.
Jul 15 21:31:03 ansible-node1 firewalld[662]: WARNING: AllowZoneDrifting is enabled. This is considered an insecure configuration option. It will be removed in a future release. Please consider disabling it now.
[root@ansible-node1 ~]# firewall-cmd --zone=public --add-port=29736/tcp --permanent
success
[root@ansible-node1 ~]# firewall-cmd --reload
success
```

**注意，三个节点都执行以上操作！**

然后，在主节点nsible-node1上面查看集群信息：

```sh
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -p 29736 -a .N5VknxU0L4DbLsB,b.LOd6UJKULzYIe
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.123,port=29736,state=online,offset=546,lag=0
slave1:ip=192.168.56.122,port=29736,state=online,offset=546,lag=0
master_failover_state:no-failover
master_replid:fdcdff5ed9900e2fbd0d80a9b4ca31fc78a72142
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:546
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:546
127.0.0.1:29736> info memory
# Memory
used_memory:1965032
used_memory_human:1.87M
used_memory_rss:10567680
used_memory_rss_human:10.08M
used_memory_peak:2024856
used_memory_peak_human:1.93M
used_memory_peak_perc:97.05%
used_memory_overhead:1922240
used_memory_startup:812128
used_memory_dataset:42792
used_memory_dataset_perc:3.71%
allocator_allocated:2029776
allocator_active:2334720
allocator_resident:4792320
total_system_memory:8201236480
total_system_memory_human:7.64G
used_memory_lua:30720
used_memory_lua_human:30.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:1073741824
maxmemory_human:1.00G
maxmemory_policy:noeviction
allocator_frag_ratio:1.15
allocator_frag_bytes:304944
allocator_rss_ratio:2.05
allocator_rss_bytes:2457600
rss_overhead_ratio:2.21
rss_overhead_bytes:5775360
mem_fragmentation_ratio:5.49
mem_fragmentation_bytes:8643664
mem_not_counted_for_evict:4
mem_replication_backlog:1048576
mem_clients_slaves:41024
mem_clients_normal:20504
mem_aof_buffer:8
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0
127.0.0.1:29736>
```

可以看到，有两个从节点在线：

```
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.123,port=29736,state=online,offset=546,lag=0
slave1:ip=192.168.56.122,port=29736,state=online,offset=546,lag=0
```

在从节点上面也可以看到对应的master主节点信息：

在节点2上面查看：

```sh
# 在节点2上面查看
[root@ansible-node2 ~]# /srv/redis/bin/redis-cli -p 29736 -a .N5VknxU0L4DbLsB,b.LOd6UJKULzYIe
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:6
master_sync_in_progress:0
slave_read_repl_offset:700
slave_repl_offset:700
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:fdcdff5ed9900e2fbd0d80a9b4ca31fc78a72142
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:700
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:700
127.0.0.1:29736>
```

在节点3上面查看：

```sh
[root@ansible-node3 ~]# /srv/redis/bin/redis-cli -p 29736 -a .N5VknxU0L4DbLsB,b.LOd6UJKULzYIe
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:9
master_sync_in_progress:0
slave_read_repl_offset:812
slave_repl_offset:812
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:fdcdff5ed9900e2fbd0d80a9b4ca31fc78a72142
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:812
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:812
127.0.0.1:29736>
```

有了以上基础后，我们就可以来修改ansible redis角色中的任务配置，增加配置文件`/srv/redis/conf/redis.conf`的修改即可。



在进行修改前，我们在主机清单中，加一个变量`REDIS_ROLE`，用来标记各节点redis的角色。

```ini
[root@ansible ansible_playbooks]# cat hosts.ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3

[redishosts]
192.168.56.121 hostname=ansible-node1 REDIS_ROLE=master
192.168.56.122 hostname=ansible-node2 REDIS_ROLE=slave
192.168.56.123 hostname=ansible-node3 REDIS_ROLE=slave

[root@ansible ansible_playbooks]#
```

通过下面的ad hoc命令可以知道，能够正常获取到master节点IP以及`REDIS_ROLE`变量的值：

```sh
[root@ansible ansible_playbooks]# ansible -i hosts.ini redishosts -m debug -a 'msg={{ groups["redishosts"]|first }}'
192.168.56.122 | SUCCESS => {
    "msg": "192.168.56.121"
}
192.168.56.121 | SUCCESS => {
    "msg": "192.168.56.121"
}
192.168.56.123 | SUCCESS => {
    "msg": "192.168.56.121"
}
[root@ansible ansible_playbooks]# ansible -i hosts.ini redishosts -m debug -a 'msg={{ REDIS_ROLE }}'
192.168.56.122 | SUCCESS => {
    "msg": "slave"
}
192.168.56.121 | SUCCESS => {
    "msg": "master"
}
192.168.56.123 | SUCCESS => {
    "msg": "slave"
}
[root@ansible ansible_playbooks]#

```

我将第一个节点当做master主节点。这个是修改后的`roles/redis/tasks/redis.yaml`任务文件：

```yaml {64-84}
---
# roles/redis/tasks/redis.yaml
- name: Add the user with a specific shell
  ansible.builtin.user:
    name: "{{ REDIS_RUNNING_USER }}"
    comment: Redis Database Server
    create_home: no
    shell: /sbin/nologin

# 归档文件复制到远程主机时，会自动解压
- name: Unarchive the source package
  ansible.builtin.unarchive:
    src: redis-6.2.14.tar.gz
    dest: /srv
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

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
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
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
  # 委派给ansible控制节点
  delegate_to: localhost
  # 且只运行一次
  run_once: true

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
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

- name: Set replicaof masterip masterport info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis.conf"
    # 默认将redishosts组中第一个节点作为master节点
    block: |
      replicaof {{ groups["redishosts"]|first }} {{ REDIS_LISTEN_PORT }}
    insertbefore: "# replicaof <masterip> <masterport>"
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add replicaof masterip masterport"
  when: REDIS_ROLE == "slave"

- name: Set masterauth master-password info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis.conf"
    # 默认将redishosts组中第一个节点作为master节点
    block: |
      masterauth {{ REDIS_PASSWORD }}
    insertbefore: "# masterauth <master-password>"
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add masterauth master-password"
  when: REDIS_ROLE == "slave"

- name: Change the redis log file Permission
  ansible.builtin.file:
    path: "{{ item }}"
    state: touch
    mode: '0644'
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  with_items:
    - "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_LISTEN_PORT }}.log"

```

64-84行是新增的两个任务。

特别注意，要使用`marker: "# {mark} meizhaohui add replicaof masterip masterport"`和` marker: "# {mark} meizhaohui add masterauth master-password"`标记不同的块。

最终ansible自动修改后，效果是这样的：

![](/img/Snipaste_2024-07-15_23-08-18.png)

再次执行剧本前，各节点删除掉`/srv/redis`和`/srv/redis-6.2.14`目录：

```sh
# 节点1
[root@ansible-node1 ~]# spctl stop redis && rm -rf /srv/redis*
redis: stopped
[root@ansible-node1 ~]# spstatus
redis                            STOPPED   Jul 15 10:42 PM
testapp                          RUNNING   pid 2623, uptime 1:04:18
[root@ansible-node1 ~]#


# 节点2
redis: stopped
[root@ansible-node2 ~]# spstatus
redis                            STOPPED   Jul 15 10:42 PM
testapp                          RUNNING   pid 2630, uptime 1:04:48
[root@ansible-node2 ~]#

# 节点3
[root@ansible-node3 ~]# spctl stop redis && rm -rf /srv/redis*
redis: stopped
[root@ansible-node3 ~]# spstatus
redis                            STOPPED   Jul 15 10:43 PM
testapp                          RUNNING   pid 2657, uptime 1:05:24
[root@ansible-node3 ~]#
```

执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [redis : Add the user with a specific shell] *****************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}
ok: [192.168.56.123] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}
ok: [192.168.56.122] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}

TASK [redis : Unarchive the source package] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1721055442.28-2957-10273322333054/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1721055442.28-2957-10273322333054/source", "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1721055442.27-2955-129517936894016/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1721055442.27-2955-129517936894016/source", "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1721055442.26-2954-99490698300656/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 62, "src": "/root/.ansible/tmp/ansible-tmp-1721055442.26-2954-99490698300656/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}

TASK [redis : Create a random password] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost] => {"ansible_facts": {"REDIS_PASSWORD": "4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl"}, "changed": false}

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl"
}
ok: [192.168.56.122] => {
    "msg": "4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl"
}
ok: [192.168.56.123] => {
    "msg": "4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl"
}

TASK [Copy redis.conf file] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "3b45fd1f159af854c26458774deb901746858e54", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "fa3b734925d5340de817a51431f77c95", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1721055445.92-3149-108344121809696/source", "state": "file", "uid": 1001}
changed: [192.168.56.121] => {"changed": true, "checksum": "8d7239f632126bf5bc92392bbc48f04dc4765ce6", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "20f8c162bc5971e6d2114bced27e48a0", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1721055445.87-3148-265766574635350/source", "state": "file", "uid": 1001}
changed: [192.168.56.123] => {"changed": true, "checksum": "cc2cde227020319bccb1e7298c102af4e55d2640", "dest": "/srv/redis/conf/redis.conf", "gid": 1001, "group": "redis", "md5sum": "d46576e49ad1ee132364f6beb01c9e6c", "mode": "0600", "owner": "redis", "size": 143309, "src": "/root/.ansible/tmp/ansible-tmp-1721055445.94-3152-94390159209799/source", "state": "file", "uid": 1001}

TASK [redis : Set replicaof masterip masterport info] *************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
changed: [192.168.56.123] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}

TASK [redis : Set masterauth master-password info] ****************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
changed: [192.168.56.123] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [redis : Set vm.overcommit_memory value] *********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.123] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}

TASK [redis : Set net.core.somaxconn value] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false}
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.123] => {"changed": false}

TASK [Set redis open files] ***************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.123] => {"changed": false, "msg": ""}
ok: [192.168.56.122] => {"changed": false, "msg": ""}

TASK [Copy redis app config] **************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {"changed": false, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/redis.ini", "size": 320, "state": "file", "uid": 0}
ok: [192.168.56.121] => {"changed": false, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/redis.ini", "size": 320, "state": "file", "uid": 0}
ok: [192.168.56.122] => {"changed": false, "checksum": "7fee8741b6f619eeb8b186685fabed33e251711a", "dest": "/etc/supervisord.d/redis.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/redis.ini", "size": 320, "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-15 22:44:49 CST", "ActiveEnterTimestampMonotonic": "4428184861", "ActiveExitTimestamp": "Mon 2024-07-15 22:44:49 CST", "ActiveExitTimestampMonotonic": "4428027281", "ActiveState": "active", "After": "rc-local.service systemd-journald.socket system.slice basic.target nss-user-lookup.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-15 22:44:49 CST", "AssertTimestampMonotonic": "4428058505", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-15 22:44:49 CST", "ConditionTimestampMonotonic": "4428058505", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "3842", "ExecMainStartTimestamp": "Mon 2024-07-15 22:44:49 CST", "ExecMainStartTimestampMonotonic": "4428184844", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-15 22:44:49 CST] ; stop_time=[Mon 2024-07-15 22:44:49 CST] ; pid=3841 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-15 22:44:49 CST", "InactiveEnterTimestampMonotonic": "4428058242", "InactiveExitTimestamp": "Mon 2024-07-15 22:44:49 CST", "InactiveExitTimestampMonotonic": "4428058854", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "3842", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-15 22:44:49 CST", "WatchdogTimestampMonotonic": "4428184853", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-15 22:44:49 CST", "ActiveEnterTimestampMonotonic": "4430880817", "ActiveExitTimestamp": "Mon 2024-07-15 22:44:49 CST", "ActiveExitTimestampMonotonic": "4430721711", "ActiveState": "active", "After": "nss-user-lookup.target system.slice basic.target systemd-journald.socket rc-local.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-15 22:44:49 CST", "AssertTimestampMonotonic": "4430753122", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-15 22:44:49 CST", "ConditionTimestampMonotonic": "4430753122", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "3840", "ExecMainStartTimestamp": "Mon 2024-07-15 22:44:49 CST", "ExecMainStartTimestampMonotonic": "4430880795", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-15 22:44:49 CST] ; stop_time=[Mon 2024-07-15 22:44:49 CST] ; pid=3839 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-15 22:44:49 CST", "InactiveEnterTimestampMonotonic": "4430752846", "InactiveExitTimestamp": "Mon 2024-07-15 22:44:49 CST", "InactiveExitTimestampMonotonic": "4430753499", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "3840", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-15 22:44:49 CST", "WatchdogTimestampMonotonic": "4430880806", "WatchdogUSec": "0"}}
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-15 22:44:49 CST", "ActiveEnterTimestampMonotonic": "4431718001", "ActiveExitTimestamp": "Mon 2024-07-15 22:44:49 CST", "ActiveExitTimestampMonotonic": "4431565710", "ActiveState": "active", "After": "system.slice nss-user-lookup.target rc-local.service basic.target systemd-journald.socket", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-15 22:44:49 CST", "AssertTimestampMonotonic": "4431591594", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-15 22:44:49 CST", "ConditionTimestampMonotonic": "4431591594", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "3721", "ExecMainStartTimestamp": "Mon 2024-07-15 22:44:49 CST", "ExecMainStartTimestampMonotonic": "4431717984", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-15 22:44:49 CST] ; stop_time=[Mon 2024-07-15 22:44:49 CST] ; pid=3720 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-15 22:44:49 CST", "InactiveEnterTimestampMonotonic": "4431591360", "InactiveExitTimestamp": "Mon 2024-07-15 22:44:49 CST", "InactiveExitTimestampMonotonic": "4431592065", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "3721", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-15 22:44:49 CST", "WatchdogTimestampMonotonic": "4431717992", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] **********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}
ok: [192.168.56.121] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}
ok: [192.168.56.123] => {"changed": false, "checksum": "599beb1752ee30b5f09948097ad94bbddfe1dd94", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/root/.alias_redis.sh", "size": 389, "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.122] => {"changed": false, "msg": ""}
ok: [192.168.56.123] => {"changed": false, "msg": ""}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=16   changed=6    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
192.168.56.122             : ok=17   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=17   changed=8    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 11 seconds
[root@ansible ansible_playbooks]#
```

![](/img/Snipaste_2024-07-15_22-59-12.png)

![](/img/Snipaste_2024-07-15_22-59-43.png)

此时，在各节点检查主从是否生效：

```sh
# 节点1 Redis master主节点
[root@ansible-node1 ~]# grep 'requirepass' /srv/redis/conf/redis.conf
# If the master is password protected (using the "requirepass" configuration
# IMPORTANT NOTE: starting with Redis 6 "requirepass" is just a compatibility
# The requirepass is not compatable with aclfile option and the ACL LOAD
# command, these will cause requirepass to be ignored.
# requirepass foobared
#   重要提示：从 Redis 6 开始，"requirepass"只是新 ACL 系统之上的兼容层。
#   requirepass 与 aclfile 选项和 ACL LOAD 命令不兼容，
#   这些将导致 requirepass 被忽略。
requirepass 4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl
# So use the 'requirepass' option to protect your instance.
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -p 29736 -a 4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.123,port=29736,state=online,offset=56,lag=0
slave1:ip=192.168.56.122,port=29736,state=online,offset=56,lag=0
master_failover_state:no-failover
master_replid:a12791a094e6e5568ee1607a66aafd9cd5a4bd66
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:56
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:56
127.0.0.1:29736>
127.0.0.1:29736> set name redis
OK
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736>


# 节点2 Redis slave1 从1
[root@ansible-node2 ~]# /srv/redis/bin/redis-cli -p 29736 -a 4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:9
master_sync_in_progress:0
slave_read_repl_offset:350
slave_repl_offset:350
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:a12791a094e6e5568ee1607a66aafd9cd5a4bd66
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:350
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:350
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736>


# 节点3 Redis slave2 从2
[root@ansible-node3 ~]# /srv/redis/bin/redis-cli -p 29736 -a 4WxOdog__:-Q3g2UU3tFCI3xk7Dp_xbl
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:8
master_sync_in_progress:0
slave_read_repl_offset:364
slave_repl_offset:364
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:a12791a094e6e5568ee1607a66aafd9cd5a4bd66
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:364
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:364
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736>
```

可以看到，一主两从的redis集群生效了！

### 3.2 优化Redis主从模式配置

如果我们想通过redis这一个ansible role角色来写成redis主从模式、哨兵模式和集群模式的配置，由于后面哨兵模式和集群模式配置，每个节点上面都会起至少两个redis实例，为了避免配置文件名重复之类的问题，我们将相关配置文件名都加上端口号信息。

主要涉及以下几个配置：

- `/srv/redis/redis.conf`，将这个配置文件修改为带端口的名称，如`/srv/redis/redis_29736.conf`。
- `/srv/redis/redis.conf`配置文件中涉及持久化的文件名称，如`appendonly.aof`和`dump.rdb`,也加上端口号信息，如`appendonly_29736.aof`和`dump_29736.rdb`。
- supervisor进程管理工具的应用配置文件`/etc/supervisord.d/redis.ini`，也带上端口号，如`/etc/supervisord.d/redis_29736.ini`。并且该配置文件中指定应用名称`[program:redis]`的配置和启动命令配置`command = /srv/redis/bin/redis-server /srv/redis/conf/redis.conf`也需要做相应修改。

对剧本文件进行一些修改，以下截图是修改点：

![](/img/Snipaste_2024-07-21_11-22-24.png)

在重新执行剧本前，先将三个节点上面的相关文件删除掉：

```sh
spctl stop redis && rm -rf /etc/supervisord.d/redis.ini && rm -rf /srv/redis* && spctl update && spstatus
```

```sh
# 三个节点都执行命令，清除之前的redis相关文件
[root@ansible-node1 ~]# spctl stop redis && rm -rf /etc/supervisord.d/redis.ini && rm -rf /srv/redis* && spctl update && spstatus
redis: stopped
redis: stopped
redis: removed process group
testapp                          RUNNING   pid 1527, uptime 1:10:00
[root@ansible-node1 ~]#
```



修改后的`hosts.ini`配置文件：

```ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3

[redishosts]
192.168.56.121 hostname=ansible-node1 REDIS_ROLE=master REDIS_APP_NAME=redis-master
192.168.56.122 hostname=ansible-node2 REDIS_ROLE=slave  REDIS_APP_NAME=redis-slave1
192.168.56.123 hostname=ansible-node3 REDIS_ROLE=slave  REDIS_APP_NAME=redis-slave2

```

此时增加了个`REDIS_APP_NAME`变量，用来标记supervisor管理的应用名称。

`roles/redis/tasks/supervisor.yaml`配置文件中修改目录配置文件名称：

```yaml {6}
---
# roles/redis/tasks/supervisor.yaml
- name: Copy redis app config
  ansible.builtin.template:
    src: redis.ini.j2
    dest: /etc/supervisord.d/redis_{{ REDIS_LISTEN_PORT }}.ini
    force: yes
    backup: yes
    remote_src: no

- name: Start service supervisord, in all cases
  ansible.builtin.service:
    name: supervisord
    state: restarted
    # 开机启动
    enabled: yes

```



`roles/redis/templates/redis.ini.j2`模板文件，修改应用名称和启动命令：

```ini {2,3}
# roles/redis/templates/redis.ini.j2
[program:{{ REDIS_APP_NAME }}]
command = {{ REDIS_BASE_DIR }}/bin/redis-server {{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_LISTEN_PORT }}.conf
directory = {{ REDIS_BASE_DIR }}
user = {{ REDIS_RUNNING_USER }}
stdout_logfile = {{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_LISTEN_PORT }}.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart=true

```



`roles/redis/templates/redis.conf.j2`配置文件中，修改`dbfilename`和`appendfilename`参数的值：

```sh
[root@ansible ansible_playbooks]# grep REDIS_LISTEN_PORT roles/redis/templates/redis.conf.j2
port {{ REDIS_LISTEN_PORT }}
dbfilename dump_{{ REDIS_LISTEN_PORT }}.rdb
appendfilename "appendonly_{{ REDIS_LISTEN_PORT }}.aof"
[root@ansible ansible_playbooks]#
```



`roles/redis/tasks/redis.yaml`  redis安装任务中，修改配置文件路径，带上端口号信息：

```yaml {59,68,79}
---
# roles/redis/tasks/redis.yaml
- name: Add the user with a specific shell
  ansible.builtin.user:
    name: "{{ REDIS_RUNNING_USER }}"
    comment: Redis Database Server
    create_home: no
    shell: /sbin/nologin

# 归档文件复制到远程主机时，会自动解压
- name: Unarchive the source package
  ansible.builtin.unarchive:
    src: redis-6.2.14.tar.gz
    dest: /srv
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

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
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  with_items:
    - "{{ REDIS_BASE_DIR }}"
    - "{{ REDIS_BASE_DIR }}/conf"
    - "{{ REDIS_BASE_DIR }}/pid"
    - "{{ REDIS_BASE_DIR }}/logs"
    - "{{ REDIS_BASE_DIR }}/data"

- name: Create a random password
  ansible.builtin.set_fact:
    # 创建一个长度为128位的随机密码用作redis服务的认证密码
    # 密码要足够复杂(64个字符以上)，因为redis的性能很高
    # 如果密码比较简单，完全是可以在一段时间内通过暴力来破译密码
    REDIS_PASSWORD: "{{ lookup('ansible.builtin.password', '/dev/null length=128') }}"
  changed_when: false
  # 委派给ansible控制节点
  delegate_to: localhost
  # 且只运行一次
  run_once: true

- name: Display the redis password
  ansible.builtin.debug:
    msg: "{{ REDIS_PASSWORD }}"
  changed_when: false

- name: Copy redis.conf file
  ansible.builtin.template:
    src: redis.conf.j2
    dest: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_LISTEN_PORT }}.conf"
    mode: '0600'
    force: yes
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

- name: Set replicaof masterip masterport info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_LISTEN_PORT }}.conf"
    # 默认将redishosts组中第一个节点作为master节点
    block: |
      replicaof {{ groups["redishosts"]|first }} {{ REDIS_LISTEN_PORT }}
    insertbefore: "# replicaof <masterip> <masterport>"
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add replicaof masterip masterport"
  when: REDIS_ROLE == "slave"

- name: Set masterauth master-password info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_LISTEN_PORT }}.conf"
    # 默认将redishosts组中第一个节点作为master节点
    block: |
      masterauth {{ REDIS_PASSWORD }}
    insertbefore: "# masterauth <master-password>"
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add masterauth master-password"
  when: REDIS_ROLE == "slave"

- name: Change the redis log file Permission
  ansible.builtin.file:
    path: "{{ item }}"
    state: touch
    mode: '0644'
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  with_items:
    - "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_LISTEN_PORT }}.log"

```



然后执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [redis : Add the user with a specific shell] *****************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [redis : Unarchive the source package] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121]
changed: [192.168.56.122]
changed: [192.168.56.123]

TASK [redis : Create a symbolic link] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121]
changed: [192.168.56.123]
changed: [192.168.56.122]

TASK [redis : Create a directory if it does not exist] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis)
changed: [192.168.56.123] => (item=/srv/redis)
changed: [192.168.56.122] => (item=/srv/redis)
changed: [192.168.56.123] => (item=/srv/redis/conf)
changed: [192.168.56.121] => (item=/srv/redis/conf)
changed: [192.168.56.122] => (item=/srv/redis/conf)
changed: [192.168.56.123] => (item=/srv/redis/pid)
changed: [192.168.56.121] => (item=/srv/redis/pid)
changed: [192.168.56.122] => (item=/srv/redis/pid)
changed: [192.168.56.121] => (item=/srv/redis/logs)
changed: [192.168.56.123] => (item=/srv/redis/logs)
changed: [192.168.56.122] => (item=/srv/redis/logs)
changed: [192.168.56.123] => (item=/srv/redis/data)
changed: [192.168.56.121] => (item=/srv/redis/data)
changed: [192.168.56.122] => (item=/srv/redis/data)

TASK [redis : Create a random password] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost]

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6"
}
ok: [192.168.56.122] => {
    "msg": "EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6"
}
ok: [192.168.56.123] => {
    "msg": "EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6"
}

TASK [Copy redis.conf file] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122]
changed: [192.168.56.121]
changed: [192.168.56.123]

TASK [redis : Set replicaof masterip masterport info] *************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121]
changed: [192.168.56.122]
changed: [192.168.56.123]

TASK [redis : Set masterauth master-password info] ****************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121]
changed: [192.168.56.123]
changed: [192.168.56.122]

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29736.log)
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29736.log)
changed: [192.168.56.123] => (item=/srv/redis/logs/redis_29736.log)

TASK [redis : Set vm.overcommit_memory value] *********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.123]
ok: [192.168.56.122]

TASK [redis : Set net.core.somaxconn value] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [Set redis open files] ***************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [Copy redis app config] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123]
changed: [192.168.56.121]
changed: [192.168.56.122]

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122]
changed: [192.168.56.123]
changed: [192.168.56.121]

TASK [redis : Copy alias config] **********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [redis : Insert block to .bashrc] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=16   changed=7    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
192.168.56.122             : ok=17   changed=9    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=17   changed=9    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 12 seconds
[root@ansible ansible_playbooks]# 
```

然后，在节点检查：

```sh
[root@ansible-node1 ~]# spstatus
redis-master                     RUNNING   pid 5095, uptime 0:00:11
testapp                          RUNNING   pid 5096, uptime 0:00:11
[root@ansible-node1 ~]# ll /srv/redis/conf/
total 144
-rw------- 1 redis redis 143633 Jul 21 11:48 redis_29736.conf
[root@ansible-node1 ~]# ll /srv/redis/data/
total 4
-rw-r--r-- 1 redis redis   0 Jul 21 11:48 appendonly_29736.aof
-rw-r--r-- 1 redis redis 176 Jul 21 11:49 dump_29736.rdb
[root@ansible-node1 ~]# ll /etc/supervisord.d/
total 12
-rw-r--r-- 1 root root  36 Apr 24 22:36 app.ini
-rw-r--r-- 1 root root 333 Jul 21 11:48 redis_29736.ini
-rw-r--r-- 1 root root 269 Jul  7 18:20 redis.ini.3180.2024-07-14@09:49:46~
[root@ansible-node1 ~]# grep '^requirepass' /srv/redis/conf/redis_29736.conf
requirepass EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -p 29736
127.0.0.1:29736> auth EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6
OK
127.0.0.1:29736> info memory
# Memory
used_memory:1964872
used_memory_human:1.87M
used_memory_rss:10420224
used_memory_rss_human:9.94M
used_memory_peak:1984880
used_memory_peak_human:1.89M
used_memory_peak_perc:98.99%
used_memory_overhead:1922384
used_memory_startup:812272
used_memory_dataset:42488
used_memory_dataset_perc:3.69%
allocator_allocated:2162480
allocator_active:2449408
allocator_resident:4816896
total_system_memory:8201236480
total_system_memory_human:7.64G
used_memory_lua:30720
used_memory_lua_human:30.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:1073741824
maxmemory_human:1.00G
maxmemory_policy:noeviction
allocator_frag_ratio:1.13
allocator_frag_bytes:286928
allocator_rss_ratio:1.97
allocator_rss_bytes:2367488
rss_overhead_ratio:2.16
rss_overhead_bytes:5603328
mem_fragmentation_ratio:5.30
mem_fragmentation_bytes:8455416
mem_not_counted_for_evict:4
mem_replication_backlog:1048576
mem_clients_slaves:41024
mem_clients_normal:20504
mem_aof_buffer:8
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.123,port=29736,state=online,offset=154,lag=1
slave1:ip=192.168.56.122,port=29736,state=online,offset=154,lag=0
master_failover_state:no-failover
master_replid:92734da33e6878504a76c2d381527b01a3b79bbe
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:154
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:154
127.0.0.1:29736>
```

![](/img/Snipaste_2024-07-21_12-00-21.png)

节点2和节点3上面也可以正常看到redis启动成功的：

```sh
# 节点2
[root@ansible-node2 ~]# spstatus
redis-slave1                     RUNNING   pid 5340, uptime 0:00:16
testapp                          RUNNING   pid 5341, uptime 0:00:16
[root@ansible-node2 ~]# /srv/redis/bin/redis-cli -p 29736
127.0.0.1:29736> auth EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6
OK
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736> info memory
# Memory
used_memory:1944352
used_memory_human:1.85M
used_memory_rss:10539008
used_memory_rss_human:10.05M
used_memory_peak:1944512
used_memory_peak_human:1.85M
used_memory_peak_perc:99.99%
used_memory_overhead:1902224
used_memory_startup:812448
used_memory_dataset:42128
used_memory_dataset_perc:3.72%
allocator_allocated:2156912
allocator_active:2449408
allocator_resident:4927488
total_system_memory:1927098368
total_system_memory_human:1.79G
used_memory_lua:30720
used_memory_lua_human:30.00K
used_memory_scripts:0
used_memory_scripts_human:0B
number_of_cached_scripts:0
maxmemory:1073741824
maxmemory_human:1.00G
maxmemory_policy:noeviction
allocator_frag_ratio:1.14
allocator_frag_bytes:292496
allocator_rss_ratio:2.01
allocator_rss_bytes:2478080
rss_overhead_ratio:2.14
rss_overhead_bytes:5611520
mem_fragmentation_ratio:5.54
mem_fragmentation_bytes:8635672
mem_not_counted_for_evict:124
mem_replication_backlog:1048576
mem_clients_slaves:0
mem_clients_normal:41000
mem_aof_buffer:128
mem_allocator:jemalloc-5.1.0
active_defrag_running:0
lazyfree_pending_objects:0
lazyfreed_objects:0
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:2
master_sync_in_progress:0
slave_read_repl_offset:1163
slave_repl_offset:1163
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:92734da33e6878504a76c2d381527b01a3b79bbe
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:1163
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:1163
127.0.0.1:29736>
```



节点3查看：

```sh
[root@ansible-node3 ~]# /srv/redis/bin/redis-cli -p 29736
127.0.0.1:29736> auth EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6
OK
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:5
master_sync_in_progress:0
slave_read_repl_offset:1247
slave_repl_offset:1247
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:92734da33e6878504a76c2d381527b01a3b79bbe
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:1247
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:1247
127.0.0.1:29736> 
```



可以看到，相关文件名中已经带上了端口号，并且redis主从信息正常。



### 3.3 Redis Sentinel哨兵模式配置

> 主从复制的问题
>
> Redis的主从复制模式可以将主节点的数据改变同步给从节点，这样从节点可以起到两个作用：第一，作为主节点的一个备份，一旦主节点出现了故障不可达的情况下，从节点可以作为后备“顶”上来，并且保证数据尽量不丢失。第二，从节点可以扩展主节点的读能力，一旦主节点不能支撑住大并发的读操作，从节点可以在一定程度上帮助主节点分担读能力。
>
> 但是主从复制也带来了以下问题。
>
> 1. 一旦主节点出现故障，需要手动将一个从节点晋升为主节点，同时需要修改应用方的主节点地址，还需要命令其他从节点去复制新的主节点，整个过程都需要人工干预。
>
> 2.  主节点的写能力受到单机的限制。
> 3. 主节点的存储能力受到单机的限制。



当主节点出现故障时，Redis Sentinel哨兵模式能自动完成故障发现和故障转移，并通知应用方，从而实现真正的高可用。

下面是1个主节点、2个从节点、3个哨兵节点组成的的Redis Sentinel哨兵模式的架构图：

![](/img/Snipaste_2024-07-21_15-22-02.png)



启动哨兵模式的步骤如下：

- 先按正常流程启动1主2从的Redis主从集群。
- 三个节点，复制一份原来的`/srv/redis/conf/redis_29736.conf`配置文件，假设哨兵程序监听端口是`39736`，则哨兵程序的配置文件为`/srv/redis/conf/redis_39736.conf`。
- 然后三个节点分别启动哨兵程序。



配置哨兵模式时，需要在原来主从模式的配置的基础上，增加以下一些内容：

```
# 设置主服务器的名字，以及其地址和端口。
# 2 是最少需要多少个哨兵同意主服务器已经失效才会进行故障转移
# 假设192.168.56.121为redis的主节点
sentinel monitor mymaster 192.168.56.121 29736 2
# 如果一个服务器在指定的毫秒数内没有响应，则认为它是不可用的
sentinel down-after-milliseconds mymaster 30000
# 在故障转移期间，可以有几个从服务器同时进行同步
sentinel parallel-syncs mymaster 1
# 如果故障转移超过这个时间，则认为故障转移失败
sentinel failover-timeout mymaster 180000
# 配置主节点的密码，防止哨兵节点对主节点无法监控
sentinel auth-pass mymaster EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6
```

另外，由于主节点配置了`requirepass`参数，建议除了从节点配置`masterauth`配置主节点密码外，主节点以及三个哨兵节点也配置`masterauth`配置主节点密码。

```
masterauth EvtoIl9H6fjsQlsfUOv43MX9jHQmgEExcViOaKG.m2Yv.v1293jD,Fdd8vUlSgDuQw6MC3:t__r,tvWut71Y,U9:,b-v8kIAZQMwLH983b:OaUzR6mOXMsVcllgyJRE6
```

另外，在哨兵配置文件中，**不要**设置`replicaof <masterip> <masterport>`，避免出现不必要的从节点。





这时需要考虑Ansible该如何配置哨兵节点的任务了。

- 优化redis主从和redis哨兵模式的supervisor管理的应用的启动顺序。
- 增加一个redis哨兵模式的任务，仅当定义了`REDIS_SENTINEL_APP_NAME`环境变量时才执行这些任务。
- 优化快捷命令。

第二步需要使用`include_tasks`关键字和`when`条件判断。第一次使用时，可以简单测试一下：

```sh
[root@ansible ansible_playbooks]# cat hosts.ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3

[redishosts]
# REDIS_ROLE 代表主从节点的角色
#   REDIS_ROLE=master 则表明该节点部署redis主节点
#   REDIS_ROLE=slave  则表明该节点部署redis从节点
# REDIS_APP_NAME          代表使用supervisor管理的redis主从应用的名称，主从模式时，必须配置这个环境变量
# REDIS_SENTINEL_APP_NAME 代表使用supervisor管理的redis哨兵应用的名称，哨兵模式时，必须配置这个环境变量

192.168.56.121 hostname=ansible-node1 REDIS_ROLE=master REDIS_APP_NAME=redis-master REDIS_SENTINEL_APP_NAME=sentinel1
192.168.56.122 hostname=ansible-node2 REDIS_ROLE=slave  REDIS_APP_NAME=redis-slave1 REDIS_SENTINEL_APP_NAME=sentinel2
192.168.56.123 hostname=ansible-node3 REDIS_ROLE=slave  REDIS_APP_NAME=redis-slave2 REDIS_SENTINEL_APP_NAME=sentinel3


[root@ansible ansible_playbooks]# cat roles/redis/tasks/main.yml
---
# redis角色任务
# 安装redis
#- include: redis.yaml
# 优化系统设置
#- include: sysctl.yaml
# 使用supervisor进程管理工具配置redis app
#- include: supervisor.yaml
# 创建快捷命令
#- include: alias.yaml
- name: Config redis sentinel tasks
  include_tasks: redis-sentinel.yaml
  when: REDIS_SENTINEL_APP_NAME is defined
[root@ansible ansible_playbooks]# cat roles/redis/tasks/redis-sentinel.yaml
---
# roles/redis/tasks/redis-sentinel.yaml
- name: Display the redis password
  ansible.builtin.debug:
    msg: "{{ REDIS_PASSWORD }}"
  changed_when: false

[root@ansible ansible_playbooks]#
```

以上将不相关的任务注释掉了。

然后执行测试：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v -e REDIS_PASSWORD=123456
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [Config redis sentinel tasks] ********************************************************************************************************************************************************************************************************************************************
included: /root/ansible_playbooks/roles/redis/tasks/redis-sentinel.yaml for 192.168.56.123, 192.168.56.122, 192.168.56.121

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "123456"
}
ok: [192.168.56.123] => {
    "msg": "123456"
}
ok: [192.168.56.122] => {
    "msg": "123456"
}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 2 seconds
[root@ansible ansible_playbooks]# 
```

![](/img/Snipaste_2024-07-21_23-01-16.png)

可以看到，能够正常判断环境变量是否定义，并调用相关任务文件。



此处主要讲一些变化的点。

#### 3.3.1  默认变量修改

默认变量配置文件`roles/redis/defaults/main.yml`中增加了`REDIS_SENTINEL_LISTEN_PORT: 49736`配置：

```yaml {23-26}
---
# roles/redis/defaults/main.yml
# redis服务监听端口，默认6379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为29736
REDIS_LISTEN_PORT: 29736
# redis服务基础目录，会在访目录下面创建conf、pid、data、logs等目录，存放redis相关文件
REDIS_BASE_DIR: /srv/redis
# redis运行用户
REDIS_RUNNING_USER: redis
# BEGIN MEIZHAOHUI COMMENTS
# net.core.somaxconn参数优化，与redis配置文件中tcp-backlog参数对应
#   在linux系统中控制tcp三次握手已完成连接队列的长度
#   在高并发系统中，你需要设置一个较高的tcp-backlog来避免客户端连接速度慢的问题（三次握手的速度）
#   取 /proc/sys/net/core/somaxconn 和 tcp-backlog 配置两者中的小值
#   对于负载很大的服务程序来说一般会将它修改为2048或者更大。
#   在/etc/sysctl.conf中添加:net.core.somaxconn = 2048，然后在终端中执行sysctl -p
# END MEIZHAOHUI COMMENTS
NET_CORE_SOMAXCONN_VALUE: 511
# redis open files
REDIS_OPEN_FILES_VALUE: 10032

# redis哨兵程序服务监听端口，默认26379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为49736
REDIS_SENTINEL_LISTEN_PORT: 49736

```

用来标记redis哨兵程序监听的端口号。



#### 3.3.2 增加哨兵程序配置文件模板

增加哨兵程序配置文件模板`roles/redis/templates/redis-sentinel.conf.j2`，差不多是直接从文件模板`roles/redis/templates/redis.conf.j2`复制过来的，只有少许修改，主要是跟端口`REDIS_SENTINEL_LISTEN_PORT`相关的配置:

```sh
[root@ansible ansible_playbooks]# grep REDIS_SENTINEL_LISTEN_PORT roles/redis/templates/redis-sentinel.conf.j2
#   建议修改为10000以上，60000以下的端口，我这里设置为{{ REDIS_SENTINEL_LISTEN_PORT }}
port {{ REDIS_SENTINEL_LISTEN_PORT }}
pidfile {{ REDIS_BASE_DIR }}/pid/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.pid
logfile "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.log"
dbfilename dump_{{ REDIS_SENTINEL_LISTEN_PORT }}.rdb
appendfilename "appendonly_{{ REDIS_SENTINEL_LISTEN_PORT }}.aof"
[root@ansible ansible_playbooks]#
```



#### 3.3.3 快捷命令修改

修改快捷命令配置文件`roles/redis/templates/alias_redis.sh.j2`：

```sh {7-9}
# roles/redis/templates/alias_redis.sh.j2
# meizhaohui add this
# redis相关的快捷命令
alias redisStatus='ps -ef|grep --color=always redis-server && ps -ef|grep -v grep|grep -c redis-server && echo "以上数字为1，则说明redis-server服务进程数正常"'
alias redisPort='netstat -tunlp|grep redis-server && echo "正常监听 {{ REDIS_LISTEN_PORT }} 则说明redis-server端口正常"'
alias cdRedis='cd {{ REDIS_BASE_DIR }} && pwd && ls -lah'
alias cmdRedis='{{ REDIS_BASE_DIR }}/bin/redis-cli -p {{ REDIS_LISTEN_PORT }} -a {{ REDIS_PASSWORD }}'
alias cmdRedisSentinel='{{ REDIS_BASE_DIR }}/bin/redis-cli -p {{ REDIS_SENTINEL_LISTEN_PORT }} -a {{ REDIS_PASSWORD }}'
alias cleanRedisTemplate='spctl stop all && rm -rf /etc/supervisord.d/redis*.ini && rm -rf /srv/redis* && spctl update && spctl start testapp && spstatus'

```

主要增加了第7-9行的三个命令，使得能快速进入到redis命令行或者哨兵命令行。



#### 3.3.4  supervisor应用配置文件修改

修改了`roles/redis/templates/redis.ini.j2`文件，在其中加上了启动优先级参数，redis主从模式程序要比哨兵程序先启动起来，所以其优先级数值要小一点：

```ini {12-13}
# roles/redis/templates/redis.ini.j2
[program:{{ REDIS_APP_NAME }}]
command = {{ REDIS_BASE_DIR }}/bin/redis-server {{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_LISTEN_PORT }}.conf
directory = {{ REDIS_BASE_DIR }}
user = {{ REDIS_RUNNING_USER }}
stdout_logfile = {{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_LISTEN_PORT }}.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart = true
# 设置优先级，程序启停的优先级，数字越小优先级越高，默认999
priority = 991

```

12-13行的`priority = 991`参数是新增的。



然后增加了一个supervisor管理哨兵程序的配置文件`roles/redis/templates/redis-sentinel.ini.j2`：

```ini
# roles/redis/templates/redis-sentinel.ini.j2
[program:{{ REDIS_SENTINEL_APP_NAME }}]
command = {{ REDIS_BASE_DIR }}/bin/redis-server {{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.conf --sentinel
directory = {{ REDIS_BASE_DIR }}
user = {{ REDIS_RUNNING_USER }}
stdout_logfile = {{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart = true
# 设置优先级，程序启停的优先级，数字越小优先级越高，默认999
# 哨兵程序要在主从节点启动后再启动
priority = 992

```

此配置文件中的优先级参数`priority = 992`，数值992比991大，因此会在redis主从程序后面再启动。



#### 3.3.5 增加哨兵程序任务配置文件

增加哨兵程序任务配置文件`roles/redis/tasks/redis-sentinel.yaml`:

```yaml
---
# roles/redis/tasks/redis-sentinel.yaml
- name: Display the redis password
  ansible.builtin.debug:
    msg: "{{ REDIS_PASSWORD }}"
  changed_when: false

- name: Copy sentinel redis-sentinel.conf file
  ansible.builtin.template:
    src: redis-sentinel.conf.j2
    dest: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.conf"
    mode: '0600'
    force: yes
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"

- name: Set sentinel monitor info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.conf"
    # 默认将redishosts组中第一个节点作为master节点
    # 注意此处sentinel monitor mymaster后面要用 REDIS_LISTEN_PORT 这个变量
    block: |
      sentinel monitor mymaster {{ groups["redishosts"]|first }} {{ REDIS_LISTEN_PORT }} 2
      sentinel down-after-milliseconds mymaster 30000
      sentinel parallel-syncs mymaster 1
      sentinel failover-timeout mymaster 180000
      sentinel auth-pass mymaster {{ REDIS_PASSWORD }}
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add sentinel monitor info"

- name: Set masterauth master-password info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.conf"
    # 默认将redishosts组中第一个节点作为master节点
    block: |
      masterauth {{ REDIS_PASSWORD }}
    insertbefore: "# masterauth <master-password>"
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add masterauth master-password info"

# 确保master主节点也配置了masterauth参数，这样就算自动切换主备后，原来的主节点还是可以与新的主节点正常连接
- name: Set masterauth master-password info by sentinel task
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_LISTEN_PORT }}.conf"
    # 默认将redishosts组中第一个节点作为master节点
    block: |
      masterauth {{ REDIS_PASSWORD }}
    insertbefore: "# masterauth <master-password>"
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add masterauth master-password by sentinel task"
  when: REDIS_ROLE == "master"


- name: Change the redis log file Permission
  ansible.builtin.file:
    path: "{{ item }}"
    state: touch
    mode: '0644'
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  with_items:
    - "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.log"

- name: Copy redis sentinel app config
  ansible.builtin.template:
    src: redis-sentinel.ini.j2
    dest: /etc/supervisord.d/redis_{{ REDIS_SENTINEL_LISTEN_PORT }}.ini
    force: yes
    backup: yes
    remote_src: no

- name: Start service supervisord, in all cases
  ansible.builtin.service:
    name: supervisord
    state: restarted
    # 开机启动
    enabled: yes

```

哨兵程序任务包含以下几个子任务：

- 打印之前主从模式生成的密码信息，确认能正常获取到密码值。
- 复制哨兵程序的配置文件到`/srv/redis/conf`目录下。
- 在哨兵程序配置文件新增哨兵相关的配置。
- 在哨兵程序配置文件新增`masterauth`配置。
- 在原来定义的主节点程序配置文件新增`masterauth`配置，避免哨兵模式切换主从后，原来的主节点连接新主节点异常。
- 修改哨兵程序生成的日志文件的权限。
- 复制supervisor管理的哨兵模式应用的配置文件到`/etc/supervisord.d`目录下。
- 重启supervisord服务，相当于走动supervisor管理的应用。



#### 3.3.6 角色入口main.yml修改

角色入口配置文件`roles/redis/tasks/main.yml`:

```yaml {12-15}
---
# roles/redis/tasks/main.yml
# redis角色任务
# 安装redis
- include: redis.yaml
# 优化系统设置
- include: sysctl.yaml
# 使用supervisor进程管理工具配置redis app
- include: supervisor.yaml
# 创建快捷命令
- include: alias.yaml
# 根据是否定义REDIS_SENTINEL_APP_NAME环境变量决定是否要部署Redis哨兵模式
- name: Config redis sentinel tasks
  include_tasks: redis-sentinel.yaml
  when: REDIS_SENTINEL_APP_NAME is defined

```

根据是否定义`REDIS_SENTINEL_APP_NAME`环境变量决定是否要部署Redis哨兵模式。



整体修改完成后，就可以再执行一次剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [redis : Add the user with a specific shell] *****************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}
ok: [192.168.56.121] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}
ok: [192.168.56.123] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}

TASK [redis : Unarchive the source package] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1721660458.25-1750-40699391183509/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1721660458.25-1750-40699391183509/source", "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1721660458.25-1749-45607075935599/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 62, "src": "/root/.ansible/tmp/ansible-tmp-1721660458.25-1749-45607075935599/source", "state": "directory", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1721660458.25-1751-167305569162976/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1721660458.25-1751-167305569162976/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}

TASK [redis : Create a random password] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost] => {"ansible_facts": {"REDIS_PASSWORD": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"}, "changed": false}

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
}
ok: [192.168.56.122] => {
    "msg": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
}
ok: [192.168.56.123] => {
    "msg": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
}

TASK [Copy redis.conf file] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "4ce46b404b2c7516807b6adfe433d2ae22f44dc7", "dest": "/srv/redis/conf/redis_29736.conf", "gid": 1001, "group": "redis", "md5sum": "b8fa152db9b7210bcb9680e0c078f156", "mode": "0600", "owner": "redis", "size": 143635, "src": "/root/.ansible/tmp/ansible-tmp-1721660462.04-1957-97742589587220/source", "state": "file", "uid": 1001}
changed: [192.168.56.121] => {"changed": true, "checksum": "5594f4a034d82b473ea58badbefaf069d4b27381", "dest": "/srv/redis/conf/redis_29736.conf", "gid": 1001, "group": "redis", "md5sum": "8577c2622bef21aecbf8f24981e1936a", "mode": "0600", "owner": "redis", "size": 143635, "src": "/root/.ansible/tmp/ansible-tmp-1721660462.03-1956-190203928889994/source", "state": "file", "uid": 1001}
changed: [192.168.56.123] => {"changed": true, "checksum": "9b5cb299a9fe87a8e14e71253283bfe28b3158d4", "dest": "/srv/redis/conf/redis_29736.conf", "gid": 1001, "group": "redis", "md5sum": "436042844c97eae5f03ee9dd1efe7eb8", "mode": "0600", "owner": "redis", "size": 143635, "src": "/root/.ansible/tmp/ansible-tmp-1721660462.03-1958-200147488818600/source", "state": "file", "uid": 1001}

TASK [redis : Set replicaof masterip masterport info] *************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.123] => {"changed": true, "msg": "Block inserted"}

TASK [redis : Set masterauth master-password info] ****************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.123] => {"changed": true, "msg": "Block inserted"}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [redis : Set vm.overcommit_memory value] *********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {"changed": false}
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}

TASK [redis : Set net.core.somaxconn value] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false}
ok: [192.168.56.123] => {"changed": false}
ok: [192.168.56.122] => {"changed": false}

TASK [Set redis open files] ***************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "msg": ""}
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.123] => {"changed": false, "msg": ""}

TASK [Copy redis app config] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "checksum": "aaa5344a8312bc6da3246c38088923e8c912791b", "dest": "/etc/supervisord.d/redis_29736.ini", "gid": 0, "group": "root", "md5sum": "4b8f904776ca3c2c6329a459f30a304c", "mode": "0644", "owner": "root", "size": 436, "src": "/root/.ansible/tmp/ansible-tmp-1721660465.15-2154-103467409679906/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "7ce883fd950f5aacc1b800fcc4c97ec7cbb77bbf", "dest": "/etc/supervisord.d/redis_29736.ini", "gid": 0, "group": "root", "md5sum": "1cd63f0886facca1c9a5a23e11bc34b2", "mode": "0644", "owner": "root", "size": 436, "src": "/root/.ansible/tmp/ansible-tmp-1721660465.15-2153-22373585574838/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "checksum": "48057e5e81533766dffda990bb64bca798714790", "dest": "/etc/supervisord.d/redis_29736.ini", "gid": 0, "group": "root", "md5sum": "1fd47702de8f0e16dedd8d80752cb50e", "mode": "0644", "owner": "root", "size": 436, "src": "/root/.ansible/tmp/ansible-tmp-1721660465.14-2152-279157428657391/source", "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-22 21:38:08 CST", "ActiveEnterTimestampMonotonic": "2772174044", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "nss-user-lookup.target rc-local.service systemd-journald.socket system.slice basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-22 21:38:08 CST", "AssertTimestampMonotonic": "2772050139", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-22 21:38:08 CST", "ConditionTimestampMonotonic": "2772050139", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "1611", "ExecMainStartTimestamp": "Mon 2024-07-22 21:38:08 CST", "ExecMainStartTimestampMonotonic": "2772174027", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-22 21:38:08 CST] ; stop_time=[Mon 2024-07-22 21:38:08 CST] ; pid=1610 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-22 20:52:01 CST", "InactiveEnterTimestampMonotonic": "4928705", "InactiveExitTimestamp": "Mon 2024-07-22 21:38:08 CST", "InactiveExitTimestampMonotonic": "2772050426", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "1611", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-22 21:38:08 CST", "WatchdogTimestampMonotonic": "2772174036", "WatchdogUSec": "0"}}
changed: [192.168.56.123] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-22 21:38:16 CST", "ActiveEnterTimestampMonotonic": "2775203345", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "nss-user-lookup.target basic.target system.slice systemd-journald.socket rc-local.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-22 21:38:16 CST", "AssertTimestampMonotonic": "2775038947", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-22 21:38:16 CST", "ConditionTimestampMonotonic": "2775038947", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "1584", "ExecMainStartTimestamp": "Mon 2024-07-22 21:38:16 CST", "ExecMainStartTimestampMonotonic": "2775203328", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-22 21:38:16 CST] ; stop_time=[Mon 2024-07-22 21:38:16 CST] ; pid=1583 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-22 20:52:05 CST", "InactiveEnterTimestampMonotonic": "5545606", "InactiveExitTimestamp": "Mon 2024-07-22 21:38:16 CST", "InactiveExitTimestampMonotonic": "2775039248", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "1584", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-22 21:38:16 CST", "WatchdogTimestampMonotonic": "2775203337", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-22 21:38:14 CST", "ActiveEnterTimestampMonotonic": "2776496627", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "systemd-journald.socket rc-local.service basic.target system.slice nss-user-lookup.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-22 21:38:13 CST", "AssertTimestampMonotonic": "2775325829", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-22 21:38:13 CST", "ConditionTimestampMonotonic": "2775325829", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "1583", "ExecMainStartTimestamp": "Mon 2024-07-22 21:38:14 CST", "ExecMainStartTimestampMonotonic": "2776496609", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-22 21:38:13 CST] ; stop_time=[Mon 2024-07-22 21:38:14 CST] ; pid=1582 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-22 20:52:01 CST", "InactiveEnterTimestampMonotonic": "4655421", "InactiveExitTimestamp": "Mon 2024-07-22 21:38:13 CST", "InactiveExitTimestampMonotonic": "2775326124", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "1583", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-22 21:38:14 CST", "WatchdogTimestampMonotonic": "2776496618", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] **********************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"backup_file": "/root/.alias_redis.sh.2880.2024-07-22@23:01:17~", "changed": true, "checksum": "44d1e43cd9371a4ece8ab5227c6a1f4fff85616f", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "38ad0bd8db6cdb3a5724aebc0dd8b3ce", "mode": "0644", "owner": "root", "size": 960, "src": "/root/.ansible/tmp/ansible-tmp-1721660474.88-2229-75206700185886/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => {"backup_file": "/root/.alias_redis.sh.2791.2024-07-22@23:01:17~", "changed": true, "checksum": "44d1e43cd9371a4ece8ab5227c6a1f4fff85616f", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "38ad0bd8db6cdb3a5724aebc0dd8b3ce", "mode": "0644", "owner": "root", "size": 960, "src": "/root/.ansible/tmp/ansible-tmp-1721660474.87-2227-69998990258787/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"backup_file": "/root/.alias_redis.sh.2892.2024-07-22@23:01:17~", "changed": true, "checksum": "44d1e43cd9371a4ece8ab5227c6a1f4fff85616f", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "38ad0bd8db6cdb3a5724aebc0dd8b3ce", "mode": "0644", "owner": "root", "size": 960, "src": "/root/.ansible/tmp/ansible-tmp-1721660474.97-2231-64036346704526/source", "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.123] => {"changed": false, "msg": ""}
ok: [192.168.56.122] => {"changed": false, "msg": ""}

TASK [Config redis sentinel tasks] ********************************************************************************************************************************************************************************************************************************************
included: /root/ansible_playbooks/roles/redis/tasks/redis-sentinel.yaml for 192.168.56.121, 192.168.56.122, 192.168.56.123

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
}
ok: [192.168.56.122] => {
    "msg": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
}
ok: [192.168.56.123] => {
    "msg": "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
}

TASK [Copy sentinel redis-sentinel.conf file] *********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "697b6aa7a3edb3b32d49559d0c3a43047b0e2f91", "dest": "/srv/redis/conf/redis_49736.conf", "gid": 1001, "group": "redis", "md5sum": "d94e73ef1794bf58f8f51c0f6c8f94be", "mode": "0600", "owner": "redis", "size": 143650, "src": "/root/.ansible/tmp/ansible-tmp-1721660476.4-2314-157950892700652/source", "state": "file", "uid": 1001}
changed: [192.168.56.122] => {"changed": true, "checksum": "4df7ca0d752d13d3207b21a55649140b77c57569", "dest": "/srv/redis/conf/redis_49736.conf", "gid": 1001, "group": "redis", "md5sum": "0f04a8716e2fd10da0a6f84eea6dd711", "mode": "0600", "owner": "redis", "size": 143650, "src": "/root/.ansible/tmp/ansible-tmp-1721660476.41-2315-173677361051331/source", "state": "file", "uid": 1001}
changed: [192.168.56.123] => {"changed": true, "checksum": "34625d9a0f527d60c6a0c441d48188ba813a8900", "dest": "/srv/redis/conf/redis_49736.conf", "gid": 1001, "group": "redis", "md5sum": "49ef1198fd962fa3f2cfcaeaa2a190e0", "mode": "0600", "owner": "redis", "size": 143650, "src": "/root/.ansible/tmp/ansible-tmp-1721660476.42-2316-87095469706960/source", "state": "file", "uid": 1001}

TASK [redis : Set sentinel monitor info] **************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.121] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.123] => {"changed": true, "msg": "Block inserted"}

TASK [redis : Set masterauth master-password info] ****************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.123] => {"changed": true, "msg": "Block inserted"}
changed: [192.168.56.122] => {"changed": true, "msg": "Block inserted"}

TASK [redis : Set masterauth master-password info by sentinel task] ***********************************************************************************************************************************************************************************************************
skipping: [192.168.56.123] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.122] => {"changed": false, "skip_reason": "Conditional result was False"}
changed: [192.168.56.121] => {"changed": true, "msg": "Block inserted"}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_49736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_49736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_49736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_49736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_49736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_49736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs/redis_49736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_49736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_49736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [Copy redis sentinel app config] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "b63be5dd50cea34012f996a6555a6a72ecca70d7", "dest": "/etc/supervisord.d/redis_49736.ini", "gid": 0, "group": "root", "md5sum": "53d1fee9379b90fa4c3515e5b56839bb", "mode": "0644", "owner": "root", "size": 504, "src": "/root/.ansible/tmp/ansible-tmp-1721660478.52-2456-143132312465275/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "773e05031e5f700159d6bce7cde39636ed0c48b8", "dest": "/etc/supervisord.d/redis_49736.ini", "gid": 0, "group": "root", "md5sum": "bddbb831900db2b8266c34238dadd69e", "mode": "0644", "owner": "root", "size": 504, "src": "/root/.ansible/tmp/ansible-tmp-1721660478.55-2457-212274000036364/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "checksum": "3193c9450b7655eaa7b9d362ada86a962251e117", "dest": "/etc/supervisord.d/redis_49736.ini", "gid": 0, "group": "root", "md5sum": "7b043bb0d0f54aa5e70c914c879197ff", "mode": "0644", "owner": "root", "size": 504, "src": "/root/.ansible/tmp/ansible-tmp-1721660478.56-2459-116953211993694/source", "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-22 23:01:08 CST", "ActiveEnterTimestampMonotonic": "7751748551", "ActiveExitTimestamp": "Mon 2024-07-22 23:01:08 CST", "ActiveExitTimestampMonotonic": "7751595220", "ActiveState": "active", "After": "nss-user-lookup.target rc-local.service systemd-journald.socket system.slice basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-22 23:01:08 CST", "AssertTimestampMonotonic": "7751622350", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-22 23:01:08 CST", "ConditionTimestampMonotonic": "7751622350", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "2696", "ExecMainStartTimestamp": "Mon 2024-07-22 23:01:08 CST", "ExecMainStartTimestampMonotonic": "7751748533", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-22 23:01:08 CST] ; stop_time=[Mon 2024-07-22 23:01:08 CST] ; pid=2695 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-22 23:01:08 CST", "InactiveEnterTimestampMonotonic": "7751621878", "InactiveExitTimestamp": "Mon 2024-07-22 23:01:08 CST", "InactiveExitTimestampMonotonic": "7751622777", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "2696", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-22 23:01:08 CST", "WatchdogTimestampMonotonic": "7751748542", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-22 23:01:16 CST", "ActiveEnterTimestampMonotonic": "7758166704", "ActiveExitTimestamp": "Mon 2024-07-22 23:01:08 CST", "ActiveExitTimestampMonotonic": "7749936880", "ActiveState": "active", "After": "systemd-journald.socket rc-local.service basic.target system.slice nss-user-lookup.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-22 23:01:08 CST", "AssertTimestampMonotonic": "7749969799", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-22 23:01:08 CST", "ConditionTimestampMonotonic": "7749969799", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "2791", "ExecMainStartTimestamp": "Mon 2024-07-22 23:01:16 CST", "ExecMainStartTimestampMonotonic": "7758166678", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-22 23:01:08 CST] ; stop_time=[Mon 2024-07-22 23:01:16 CST] ; pid=2790 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-22 23:01:08 CST", "InactiveEnterTimestampMonotonic": "7749969581", "InactiveExitTimestamp": "Mon 2024-07-22 23:01:08 CST", "InactiveExitTimestampMonotonic": "7749970654", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "2791", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-22 23:01:16 CST", "WatchdogTimestampMonotonic": "7758166691", "WatchdogUSec": "0"}}
changed: [192.168.56.123] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Mon 2024-07-22 23:01:16 CST", "ActiveEnterTimestampMonotonic": "7755202523", "ActiveExitTimestamp": "Mon 2024-07-22 23:01:08 CST", "ActiveExitTimestampMonotonic": "7747026643", "ActiveState": "active", "After": "nss-user-lookup.target basic.target system.slice systemd-journald.socket rc-local.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Mon 2024-07-22 23:01:08 CST", "AssertTimestampMonotonic": "7747058165", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Mon 2024-07-22 23:01:08 CST", "ConditionTimestampMonotonic": "7747058165", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "2803", "ExecMainStartTimestamp": "Mon 2024-07-22 23:01:16 CST", "ExecMainStartTimestampMonotonic": "7755202507", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Mon 2024-07-22 23:01:08 CST] ; stop_time=[Mon 2024-07-22 23:01:16 CST] ; pid=2802 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Mon 2024-07-22 23:01:08 CST", "InactiveEnterTimestampMonotonic": "7747057919", "InactiveExitTimestamp": "Mon 2024-07-22 23:01:08 CST", "InactiveExitTimestampMonotonic": "7747058459", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "2803", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Mon 2024-07-22 23:01:16 CST", "WatchdogTimestampMonotonic": "7755202516", "WatchdogUSec": "0"}}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=25   changed=15   unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
192.168.56.122             : ok=25   changed=16   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
192.168.56.123             : ok=25   changed=16   unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 1 minutes, 5 seconds
[root@ansible ansible_playbooks]#
```

这个时候就可以在三个节点上完成哨兵模式的部署。

![](/img/Snipaste_2024-07-22_23-04-55.png)

![](/img/Snipaste_2024-07-22_23-04-25.png)

此时，在三个节点上面检查一下：

节点1上操作：

```sh
# 节点1上操作
[root@ansible-node1 ~]# spstatus
redis-master                     RUNNING   pid 3290, uptime 0:01:27
sentinel1                        RUNNING   pid 3291, uptime 0:01:27
testapp                          RUNNING   pid 3292, uptime 0:01:27
[root@ansible-node1 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.122,port=29736,state=online,offset=20941,lag=1
slave1:ip=192.168.56.123,port=29736,state=online,offset=21085,lag=1
master_failover_state:no-failover
master_replid:b946962afd176a9de504e0dc8111e2b2e7d9b8ff
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:21373
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:21373
127.0.0.1:29736> set name redis
OK
127.0.0.1:29736> set num 1
OK
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736> get num
"1"
127.0.0.1:29736> exit
[root@ansible-node1 ~]# cmdRedisSentinel
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.121:29736,slaves=2,sentinels=3
127.0.0.1:49736> sentinel sentinels mymaster
1)  1) "name"
    2) "55b5bcbf7ec40828525634ab1e3544cd5c95b51b"
    3) "ip"
    4) "192.168.56.122"
    5) "port"
    6) "49736"
    7) "runid"
    8) "55b5bcbf7ec40828525634ab1e3544cd5c95b51b"
    9) "flags"
   10) "sentinel"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "177"
   19) "last-ping-reply"
   20) "177"
   21) "down-after-milliseconds"
   22) "30000"
   23) "last-hello-message"
   24) "486"
   25) "voted-leader"
   26) "?"
   27) "voted-leader-epoch"
   28) "0"
2)  1) "name"
    2) "1fe1c2a126761eb68cf1ff2794a37710f2b5b4b3"
    3) "ip"
    4) "192.168.56.123"
    5) "port"
    6) "49736"
    7) "runid"
    8) "1fe1c2a126761eb68cf1ff2794a37710f2b5b4b3"
    9) "flags"
   10) "sentinel"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "268"
   19) "last-ping-reply"
   20) "268"
   21) "down-after-milliseconds"
   22) "30000"
   23) "last-hello-message"
   24) "445"
   25) "voted-leader"
   26) "?"
   27) "voted-leader-epoch"
   28) "0"
127.0.0.1:49736> sentinel get-master-addr-by-name mymaster
1) "192.168.56.121"
2) "29736"
127.0.0.1:49736>

```



节点2上操作：

```sh
[root@ansible-node2 ~]# spstatus
redis-slave1                     RUNNING   pid 3336, uptime 0:01:24
sentinel2                        RUNNING   pid 3337, uptime 0:01:24
testapp                          RUNNING   pid 3338, uptime 0:01:24
[root@ansible-node2 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:0
master_sync_in_progress:0
slave_read_repl_offset:89364
slave_repl_offset:89364
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:b946962afd176a9de504e0dc8111e2b2e7d9b8ff
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:89364
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:89364
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736> get num
"1"
127.0.0.1:29736> exit
[root@ansible-node2 ~]# cmdRedisSentinel
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.121:29736,slaves=2,sentinels=3
127.0.0.1:49736> sentinel sentinels mymaster
1)  1) "name"
    2) "1fe1c2a126761eb68cf1ff2794a37710f2b5b4b3"
    3) "ip"
    4) "192.168.56.123"
    5) "port"
    6) "49736"
    7) "runid"
    8) "1fe1c2a126761eb68cf1ff2794a37710f2b5b4b3"
    9) "flags"
   10) "sentinel"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "809"
   19) "last-ping-reply"
   20) "809"
   21) "down-after-milliseconds"
   22) "30000"
   23) "last-hello-message"
   24) "336"
   25) "voted-leader"
   26) "?"
   27) "voted-leader-epoch"
   28) "0"
2)  1) "name"
    2) "f81fe7b2c20ab05792002fbf51ec88378ead7b59"
    3) "ip"
    4) "192.168.56.121"
    5) "port"
    6) "49736"
    7) "runid"
    8) "f81fe7b2c20ab05792002fbf51ec88378ead7b59"
    9) "flags"
   10) "sentinel"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "809"
   19) "last-ping-reply"
   20) "809"
   21) "down-after-milliseconds"
   22) "30000"
   23) "last-hello-message"
   24) "1180"
   25) "voted-leader"
   26) "?"
   27) "voted-leader-epoch"
   28) "0"
127.0.0.1:49736> sentinel get-master-addr-by-name mymaster
1) "192.168.56.121"
2) "29736"
127.0.0.1:49736>

```



节点3上操作：

```sh
[root@ansible-node3 ~]# spstatus
redis-slave2                     RUNNING   pid 3348, uptime 0:08:45
sentinel3                        RUNNING   pid 3349, uptime 0:08:45
testapp                          RUNNING   pid 3350, uptime 0:08:45
[root@ansible-node3 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:0
master_sync_in_progress:0
slave_read_repl_offset:112976
slave_repl_offset:112976
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:b946962afd176a9de504e0dc8111e2b2e7d9b8ff
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:112976
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:168
repl_backlog_histlen:112809
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736> get num
"1"
127.0.0.1:29736> exit
[root@ansible-node3 ~]# cmdRedisSentinel
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.121:29736,slaves=2,sentinels=3
127.0.0.1:49736> sentinel sentinels mymaster
1)  1) "name"
    2) "f81fe7b2c20ab05792002fbf51ec88378ead7b59"
    3) "ip"
    4) "192.168.56.121"
    5) "port"
    6) "49736"
    7) "runid"
    8) "f81fe7b2c20ab05792002fbf51ec88378ead7b59"
    9) "flags"
   10) "sentinel"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "632"
   19) "last-ping-reply"
   20) "632"
   21) "down-after-milliseconds"
   22) "30000"
   23) "last-hello-message"
   24) "153"
   25) "voted-leader"
   26) "?"
   27) "voted-leader-epoch"
   28) "0"
2)  1) "name"
    2) "55b5bcbf7ec40828525634ab1e3544cd5c95b51b"
    3) "ip"
    4) "192.168.56.122"
    5) "port"
    6) "49736"
    7) "runid"
    8) "55b5bcbf7ec40828525634ab1e3544cd5c95b51b"
    9) "flags"
   10) "sentinel"
   11) "link-pending-commands"
   12) "0"
   13) "link-refcount"
   14) "1"
   15) "last-ping-sent"
   16) "0"
   17) "last-ok-ping-reply"
   18) "632"
   19) "last-ping-reply"
   20) "632"
   21) "down-after-milliseconds"
   22) "30000"
   23) "last-hello-message"
   24) "631"
   25) "voted-leader"
   26) "?"
   27) "voted-leader-epoch"
   28) "0"
127.0.0.1:49736> sentinel get-master-addr-by-name mymaster
1) "192.168.56.121"
2) "29736"
127.0.0.1:49736> exit
[root@ansible-node3 ~]#
```

可以看到，三个节点的哨兵程序都能正常获取到主节点信息，从节点能正常获取到主节点设置的键的值。



#### 3.3.7 测试哨兵模式的自动切换

编写一个python连接哨兵模式的程序`test_redis_sentinel.py`:

```py
# filename: test_redis_sentinel.py
# pip install redis
from redis import Sentinel
 
# 哨兵的地址和端口，格式为(host, port)
sentinels = [('192.168.56.121', 49736), ('192.168.56.122', 49736), ('192.168.56.123', 49736)]
password = "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
service_name = 'mymaster'
# 创建Sentinel实例
# sentinel_kwargs 用来配置哨兵的密码。password用来配置redis密码
sentinel = Sentinel(sentinels, socket_timeout=0.1, sentinel_kwargs={'password': password}, password=password)
 
# 获取主服务器
master = sentinel.master_for(service_name, socket_timeout=0.1, password=password)
print(f'master:{master}')
master_info = sentinel.discover_master(service_name)
master_ip = master_info[0]
master_port = master_info[1]
print(f'master ip:{master_ip}')
print(f'master port:{master_port}')
 
# 获取从服务器
slave = sentinel.slave_for(service_name, socket_timeout=0.1, password=password)
 
# 使用主服务器或从服务器进行操作
master.set('key', 'value')
print(master.get('key'))
print(master.get('name'))
print(master.get('num'))
```

然后执行python程序：

![](/img/Snipaste_2024-07-22_23-18-23.png)

可以看到，能够正常获取到集群的主节点，并能完成数据的读和写。



此时，我们尝试将节点1上的的`redis-master`程序关掉：

```sh
# 查看当前程序运行状态
[root@ansible-node1 ~]# spstatus
redis-master                     RUNNING   pid 3290, uptime 0:18:31
sentinel1                        RUNNING   pid 3291, uptime 0:18:31
testapp                          RUNNING   pid 3292, uptime 0:18:31

# 停止redis-master主程序
[root@ansible-node1 ~]# spctl stop redis-master
redis-master: stopped

# 再次查看当前程序运行状态
[root@ansible-node1 ~]# spstatus
redis-master                     STOPPED   Jul 22 11:20 PM
sentinel1                        RUNNING   pid 3291, uptime 0:18:45
testapp                          RUNNING   pid 3292, uptime 0:18:45

# 进入到哨兵模式命令行
[root@ansible-node1 ~]# cmdRedisSentinel
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
# 查看哨兵信息
# 刚开始执行几次，还是发现当前主节点是192.168.56.121:29736
# 多执行几次，发现主节点发生变化 
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.121:29736,slaves=2,sentinels=3
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.121:29736,slaves=2,sentinels=3

# 过一会再查看，发现主节点已经切换到192.168.56.122:29736了
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.122:29736,slaves=2,sentinels=3
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.122:29736,slaves=2,sentinels=3
127.0.0.1:49736>

```

我们客户端程序再执行一次：


![](/img/Snipaste_2024-07-22_23-24-31.png)

中以看到，执行成功了，客户端程序并没有做什么变更。

此时，在节点2上面查看集群主从信息：

```sh
[root@ansible-node2 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:1
slave0:ip=192.168.56.123,port=29736,state=online,offset=310086,lag=1
master_failover_state:no-failover
master_replid:8d8c74c5556afff89f66ee57bb33c209f4460c5a
master_replid2:b946962afd176a9de504e0dc8111e2b2e7d9b8ff
master_repl_offset:310086
second_repl_offset:233811
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:310086
127.0.0.1:29736>
```

可以看到，此时只有一个从节点。

此时，把节点1上面的`redis-master`程序启动起来：

```sh
[root@ansible-node1 ~]# spstatus
redis-master                     STOPPED   Jul 22 11:20 PM
sentinel1                        RUNNING   pid 3291, uptime 0:24:51
testapp                          RUNNING   pid 3292, uptime 0:24:51
[root@ansible-node1 ~]# spctl start redis-master
redis-master: started
[root@ansible-node1 ~]# spstatus
redis-master                     RUNNING   pid 3339, uptime 0:00:07
sentinel1                        RUNNING   pid 3291, uptime 0:26:36
testapp                          RUNNING   pid 3292, uptime 0:26:36
[root@ansible-node1 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.122
master_port:29736
master_link_status:up
master_last_io_seconds_ago:0
master_sync_in_progress:0
slave_read_repl_offset:331677
slave_repl_offset:331677
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:8d8c74c5556afff89f66ee57bb33c209f4460c5a
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:331677
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:328905
repl_backlog_histlen:2773
127.0.0.1:29736>
```

可以看到，新启动的节点已经变成新主节点的从节点了。

此时再在节点2上面查看集群信息：

```sh
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.123,port=29736,state=online,offset=342259,lag=1
slave1:ip=192.168.56.121,port=29736,state=online,offset=342259,lag=1
master_failover_state:no-failover
master_replid:8d8c74c5556afff89f66ee57bb33c209f4460c5a
master_replid2:b946962afd176a9de504e0dc8111e2b2e7d9b8ff
master_repl_offset:342259
second_repl_offset:233811
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:342259
127.0.0.1:29736>

```

此时，可以看到`192.168.56.122`已经变成新主的slave了！

这就完成了一次主从的自动切换。

相应的，你可以再进行其他测试，看看主节点有没有自动切换。



再尝试把节点2上面的`redis-slave1`程序停掉，看看哨兵集群是否能自动切换主节点：

```sh
[root@ansible-node2 ~]# spstatus
redis-slave1                     RUNNING   pid 1539, uptime 0:24:27
sentinel2                        RUNNING   pid 1540, uptime 0:24:27
testapp                          RUNNING   pid 1541, uptime 0:24:27
[root@ansible-node2 ~]# spctl stop redis-slave1
redis-slave1: stopped
[root@ansible-node2 ~]# spstatus
redis-slave1                     STOPPED   Jul 23 08:32 PM
sentinel2                        RUNNING   pid 1540, uptime 0:25:23
testapp                          RUNNING   pid 1541, uptime 0:25:23
[root@ansible-node2 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
Could not connect to Redis at 127.0.0.1:29736: Connection refused
not connected> exit
[root@ansible-node2 ~]# cmdRedisSentinel
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=odown,address=192.168.56.122:29736,slaves=2,sentinels=3
127.0.0.1:49736> info sentinel
# Sentinel
sentinel_masters:1
sentinel_tilt:0
sentinel_running_scripts:0
sentinel_scripts_queue_length:0
sentinel_simulate_failure_flags:0
master0:name=mymaster,status=ok,address=192.168.56.121:29736,slaves=2,sentinels=3
127.0.0.1:49736>
```

可以看到，此时主节点又切到第1个节点`192.168.56.121`上面去了。

在应用端测试，可以看到能正常读写：

![](/img/Snipaste_2024-07-23_20-35-37.png)

再次将节点2上面的redis-slave1应用程序启动起来：

```sh

[root@ansible-node2 ~]# spctl start redis-slave1
redis-slave1: started
[root@ansible-node2 ~]# spstatus
redis-slave1                     RUNNING   pid 1606, uptime 0:00:04
sentinel2                        RUNNING   pid 1540, uptime 0:29:16
testapp                          RUNNING   pid 1541, uptime 0:29:16
[root@ansible-node2 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.

# 再次查看主从信息
127.0.0.1:29736> info replication
# Replication
role:slave
master_host:192.168.56.121
master_port:29736
master_link_status:up
master_last_io_seconds_ago:2
master_sync_in_progress:0
slave_read_repl_offset:366934
slave_repl_offset:366934
slave_priority:100
slave_read_only:1
replica_announced:1
connected_slaves:0
master_failover_state:no-failover
master_replid:6de1fb8743e4ad1d2df9ffa207f40074116d8aad
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:366934
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:365602
repl_backlog_histlen:1333
127.0.0.1:29736> get client
"New"
127.0.0.1:29736>
```

可以看到，节点2又变成了从节点了。

而节点1此时可以看到两个从节点：

```sh
[root@ansible-node1 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:1
slave0:ip=192.168.56.123,port=29736,state=online,offset=356185,lag=0
master_failover_state:no-failover
master_replid:6de1fb8743e4ad1d2df9ffa207f40074116d8aad
master_replid2:5fa790a931d3bac3bff6dad30b6e9a4379bed2de
master_repl_offset:356185
second_repl_offset:320539
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:356185
127.0.0.1:29736> get client
"New"
127.0.0.1:29736> get name
"redis"
127.0.0.1:29736> get num
"1"
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:2
slave0:ip=192.168.56.123,port=29736,state=online,offset=368662,lag=0
slave1:ip=192.168.56.122,port=29736,state=online,offset=368662,lag=0
master_failover_state:no-failover
master_replid:6de1fb8743e4ad1d2df9ffa207f40074116d8aad
master_replid2:5fa790a931d3bac3bff6dad30b6e9a4379bed2de
master_repl_offset:368662
second_repl_offset:320539
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:368662
127.0.0.1:29736>
```

也就说明哨兵模式下主节点挂了后，可以自动切换主节点，不需要人工干预，对应用没多大影响。



### 3.4 Redis cluster集群模式配置

#### 3.4.1 单主机测试Redis集群模式

当遇到单机内存、并发、流量等瓶颈时，可以采用Redis Cluster集群架构方案达到负载均衡的目的。

> - Redis Cluster 集群节点最小配置 6 个节点以上(3 主 3 从)，其中主节点提供读写操作，从节点作为备用节点，不提供请求，只作为故障转移使用。
> - Redis Cluster 采用虚拟槽分区，所有的键根据哈希函数映射到 0～16383 个（2的14次幂）整数槽内，每个节点负责维护一部分槽以及槽所印映射的键值数据。 

 Redis cluster集群模式一般由多个节点组成，节点数量至少为6个才能保证组成完整高可用的集群。

- 每个节点需要开启配置`cluster-enabled yes`，让Redis运行在集群模式下。
- 建议为集群内所有节点统一目录，一般分为4个目录：conf、data、logs、pid，分别存放配置、数据、日志和PID文件。（这与之前的主从模式、哨兵模式是一样的。）
- 把6个节点的配置统一放在`conf`目录下。

集群模式下，相对于普通的主从模式，需要特别关注以下几个配置：

```ini
# 端口
port 6379
# redis认证密码
requirepass “alonglonglongpassword”
# redis主节点认证密码
masterauth “alonglonglongpassword”
# PID文件
pidfile "/srv/redis/pid/redis_6379.pid"
# 日志文件
logfile "/srv/redis/logs/redis_6379.log"
# 数据文件夹
dir "/srv/redis/data"
# 开启集群模式
cluster-enabled yes
# 集群内部配置文件名称，由redis自动管理
cluster-config-file nodes-6379.conf
# 节点超时时间，单位毫秒
cluster-node-timeout 15000
```

如果我们在单个虚拟机上面测试，节点端口分别是6379、6380、6381、6382、6383和6384。



supervisord管理的redis集群配置文件：

```sh
[root@ansible-node1 ~]# cat /etc/supervisord.d/redis_6379.ini
# roles/redis/templates/redis.ini.j2
[program:redis-6379]
command = /srv/redis/bin/redis-server /srv/redis/conf/redis_6379.conf
directory = /srv/redis
user = redis
stdout_logfile = /srv/redis/logs/redis_6379.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart = true
# 设置优先级，程序启停的优先级，数字越小优先级越高，默认999
priority = 981
[root@ansible-node1 ~]# cat /etc/supervisord.d/redis_6380.ini
# roles/redis/templates/redis.ini.j2
[program:redis-6380]
command = /srv/redis/bin/redis-server /srv/redis/conf/redis_6380.conf
directory = /srv/redis
user = redis
stdout_logfile = /srv/redis/logs/redis_6380.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart = true
# 设置优先级，程序启停的优先级，数字越小优先级越高，默认999
priority = 982
[root@ansible-node1 ~]#
```



6个配置文件：

```sh
[root@ansible-node1 ~]# ll /srv/redis/conf/redis_6*.conf
-rw-r--r-- 1 redis redis 144108 Jul 23 21:38 /srv/redis/conf/redis_6379.conf
-rw-r--r-- 1 redis redis 144108 Jul 23 21:39 /srv/redis/conf/redis_6380.conf
-rw-r--r-- 1 redis redis 144108 Jul 23 21:39 /srv/redis/conf/redis_6381.conf
-rw-r--r-- 1 redis redis 144108 Jul 23 21:39 /srv/redis/conf/redis_6382.conf
-rw-r--r-- 1 redis redis 144108 Jul 23 21:39 /srv/redis/conf/redis_6383.conf
-rw-r--r-- 1 redis redis 144108 Jul 23 21:39 /srv/redis/conf/redis_6384.conf
[root@ansible-node1 ~]#
```



然后启动6个redis应用：

```sh
[root@ansible-node1 ~]# spstatus
redis-6379                       RUNNING   pid 1822, uptime 3:28:21
redis-6380                       RUNNING   pid 1823, uptime 3:28:21
redis-6381                       RUNNING   pid 1824, uptime 3:28:21
redis-6382                       RUNNING   pid 1825, uptime 3:28:21
redis-6383                       RUNNING   pid 1826, uptime 3:28:21
redis-6384                       RUNNING   pid 1827, uptime 3:28:21
redis-master                     RUNNING   pid 1828, uptime 3:28:21
sentinel1                        RUNNING   pid 1829, uptime 3:28:21
testapp                          RUNNING   pid 1830, uptime 3:28:21
```

6个节点启动后，需要使用以下命令创建集群：

```sh
/srv/redis/bin/redis-cli -a JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI --cluster create 192.168.56.121:6379 192.168.56.121:6380 192.168.56.121:6381  192.168.56.121:6382 192.168.56.121:6383 192.168.56.121:6384 --cluster-replicas 1
```





然后登陆Redis集群：

```sh
# 如果像之前一样，仅修改一下连接的redis端口
# 获取键值时，会提示 `(error) MOVED 5798 192.168.56.121:6380` 之类的异常
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -p 6379 -a JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6379> get name
(error) MOVED 5798 192.168.56.121:6380
127.0.0.1:6379> get num
"2"
127.0.0.1:6379> exit

# 集群模式登陆，应加上-c参数
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -p 6379 -a JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI -c
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6379> get name
-> Redirected to slot [5798] located at 192.168.56.121:6380
"redis"
192.168.56.121:6380> get num
-> Redirected to slot [2765] located at 192.168.56.121:6379
"2"
192.168.56.121:6379>

```

查看集群相关的信息：

```sh
# 查看节点主从信息
192.168.56.121:6379> info replication
# Replication
role:master
connected_slaves:1
slave0:ip=192.168.56.121,port=6384,state=online,offset=14504,lag=1
master_failover_state:no-failover
master_replid:ca2eb58e2282600fb969469e5ad09d1a807ef179
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:14504
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:14504


# 实例是否启用集群模式：0-否，1-是
192.168.56.121:6379> info cluster
# Cluster
cluster_enabled:1


# 查看集群当前状态
192.168.56.121:6379> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_ping_sent:10569
cluster_stats_messages_pong_sent:11096
cluster_stats_messages_sent:21665
cluster_stats_messages_ping_received:11096
cluster_stats_messages_pong_received:10569
cluster_stats_messages_received:21665


# 查看集群节点信息
192.168.56.121:6379> cluster nodes
b1bce5bf7382a021199c8e17d6a205e41773ac2e 192.168.56.121:6384@16384 slave 6bdee7485abec10b60749e491711fd901ca1d7f4 0 1722090816000 1 connected
c88f61a916a41ae950c5c3fbcd358daf6aa367bd 192.168.56.121:6382@16382 slave 61c6d15057db3108c80729916fa4a98e49fbb1b7 0 1722090817000 2 connected
61c6d15057db3108c80729916fa4a98e49fbb1b7 192.168.56.121:6380@16380 master - 0 1722090816766 2 connected 5461-10922
54e0a585328f639e8ed1157441096e699c579219 192.168.56.121:6381@16381 master - 0 1722090817782 3 connected 10923-16383
6bdee7485abec10b60749e491711fd901ca1d7f4 192.168.56.121:6379@16379 myself,master - 0 1722090816000 1 connected 0-5460
6fc4ab4b958ce58f4c258806183e08fbd7610d41 192.168.56.121:6383@16383 slave 54e0a585328f639e8ed1157441096e699c579219 0 1722090819362 3 connected
192.168.56.121:6379>
```



节点连接redis集群：

```py
# filename: test_redis_cluster.py
# pip install redis
from redis import RedisCluster
from redis.cluster import ClusterNode

password = "JeaAG-aTBYq4XVjY3dmygoyvdkWyn-yu3msMsG-1JbTLMKQyLFcs_Lo1mcs-" \
           "pNpVvxDO:cnJZciXlYJoSNBosAiLhPG,sZXGXsBBc0h-xHVnFNTF.31m3visfh0NheJI"
# 假设你的Redis集群节点在本地的6379, 6380, 6381, 6382, 6383, 6384端口上
startup_nodes = [
    ClusterNode(host="192.168.56.121", port="6379"),
    ClusterNode(host="192.168.56.121", port="6380"),
    ClusterNode(host="192.168.56.121", port="6381"),
    ClusterNode(host="192.168.56.121", port="6382"),
    ClusterNode(host="192.168.56.121", port="6383"),
    ClusterNode(host="192.168.56.121", port="6384"),

]

# 连接到Redis集群
rc = RedisCluster(startup_nodes=startup_nodes,
                  decode_responses=True,
                  password=password)

# 使用Redis集群
rc.set("foo", "barbar")
print(rc.get("foo"))
print(rc.get("name"))
print(rc.get("num"))

```



![](/img/Snipaste_2024-07-27_22-46-20.png)

可以看到，程序能够正常读写Redis集群。

#### 3.4.2 三虚拟机部署三主三从6节点集群



三主三从6节点的集群模式。


| 序号 | 虚拟机        | IP             | 角色                             |
| ---- | ------------- | -------------- | -------------------------------- |
| 1    | ansible-node1 | 192.168.56.121 | redis-cluster-1、redis-cluster-2 |
| 2    | ansible-node2 | 192.168.56.122 | redis-cluster-3、redis-cluster-4 |
| 3    | ansible-node3 | 192.168.56.123 | redis-cluster-5、redis-cluster-6 |



#### 3.4.3 默认变量修改

默认变量配置文件`roles/redis/defaults/main.yml`中增加了`REDIS_CLUSTER_SLAVE_LISTEN_PORT: 29737`配置：

```yaml {28-30}
---
# roles/redis/defaults/main.yml
# redis服务监听端口，默认6379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为29736
REDIS_LISTEN_PORT: 29736
# redis服务基础目录，会在访目录下面创建conf、pid、data、logs等目录，存放redis相关文件
REDIS_BASE_DIR: /srv/redis
# redis运行用户
REDIS_RUNNING_USER: redis
# BEGIN MEIZHAOHUI COMMENTS
# net.core.somaxconn参数优化，与redis配置文件中tcp-backlog参数对应
#   在linux系统中控制tcp三次握手已完成连接队列的长度
#   在高并发系统中，你需要设置一个较高的tcp-backlog来避免客户端连接速度慢的问题（三次握手的速度）
#   取 /proc/sys/net/core/somaxconn 和 tcp-backlog 配置两者中的小值
#   对于负载很大的服务程序来说一般会将它修改为2048或者更大。
#   在/etc/sysctl.conf中添加:net.core.somaxconn = 2048，然后在终端中执行sysctl -p
# END MEIZHAOHUI COMMENTS
NET_CORE_SOMAXCONN_VALUE: 511
# redis open files
REDIS_OPEN_FILES_VALUE: 10032

# redis哨兵程序服务监听端口，默认26379
# 使用默认的端口号不是很安全，为了安全一点，需要修改默认的端口号
# 建议修改为10000以上，60000以下的端口，我这里设置为49736
REDIS_SENTINEL_LISTEN_PORT: 49736

# Redis集群模式下主程序监听端口,使用REDIS_LISTEN_PORT变量定义的值
# Redis集群模式下从程序监听端口
REDIS_CLUSTER_SLAVE_LISTEN_PORT: 29737

```

增加第28-30行的变量`REDIS_CLUSTER_SLAVE_LISTEN_PORT`，用于指定Redis集群模式下从程序监听端口。

而Redis集群模式下master主节点的监听端口仍然使用`REDIS_LISTEN_PORT`变量定义的端口号。



#### 3.4.4 增加集群程序配置文件模板



增加集群程序配置文件模板`roles/redis/templates/redis-cluster.conf.j2`，差不多是直接从文件模板`roles/redis/templates/redis.conf.j2`复制过来的，只有少许修改，主要是跟端口`REDIS_CLUSTER_LISTEN_PORT`相关的配置:

```sh
[root@ansible ansible_playbooks]# grep REDIS_CLUSTER_LISTEN_PORT roles/redis/templates/redis-cluster.conf.j2
#   建议修改为10000以上，60000以下的端口，我这里设置为{{ REDIS_CLUSTER_LISTEN_PORT }}
port {{ REDIS_CLUSTER_LISTEN_PORT }}
pidfile {{ REDIS_BASE_DIR }}/pid/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.pid
# logfile "/srv/redis/logs/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.log"
logfile "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.log"
dbfilename dump_{{ REDIS_CLUSTER_LISTEN_PORT }}.rdb
appendfilename "appendonly_{{ REDIS_CLUSTER_LISTEN_PORT }}.aof"
[root@ansible ansible_playbooks]#
```

对比两个模板文件的差异：

![](/img/Snipaste_2024-07-31_21-47-46.png)



而下面几个跟集群强相关的配置，在集群配置任务文件`roles/redis/tasks/redis-cluster.yaml`中指定：

```ini
# 开启集群模式
cluster-enabled yes
# 集群内部配置文件名称，由redis自动管理
cluster-config-file nodes-6379.conf
# 节点超时时间，单位毫秒
cluster-node-timeout 15000
```



#### 3.4.5 快捷命令修改

随着Ansible角色的功能越来越多，我增加了更多的快捷命令。下面是修改后的`roles/redis/templates/alias_redis.sh.j2`快捷命令的模板文件。

```sh {21,29,31,39}
# roles/redis/templates/alias_redis.sh.j2
# meizhaohui add this
# redis相关的快捷命令
# 快速切换到Redis工作目录
alias cdRedis='cd {{ REDIS_BASE_DIR }} && pwd && ls -lah'
# !!!! 快速清理Redis测试数据，生产环境谨慎使用
alias cleanRedisTemplate='spctl stop all && rm -rf /etc/supervisord.d/redis*.ini && rm -rf /srv/redis* && spctl update && spctl start testapp && spstatus'
# 快速获取Redis密码
alias getRedisPassword='grep "^requirepass" {{ REDIS_BASE_DIR }}/conf/redis*|head -n 1'

# Redis三种部署模式下的快捷命令
##############################################
# 主从模式下的查看Redis服务进程和端口状态
# 三种部署模式下，主从模式的快捷命令是一直存在的
alias redisStatus='ps -ef|grep -v grep|grep --color=always redis-server && ps -ef|grep -v grep|grep -c redis-server && echo "以上数字为1，则说明redis-server服务进程数正常"'
alias redisPort='netstat -tunlp|grep -v grep|grep --color=always redis-server && echo "正常监听 {{ REDIS_LISTEN_PORT }} 则说明redis-server端口正常"'
# Redis主从模式命令行
alias cmdRedis='{{ REDIS_BASE_DIR }}/bin/redis-cli -p {{ REDIS_LISTEN_PORT }} -a {{ REDIS_PASSWORD }}'
##############################################

{% if REDIS_SENTINEL_APP_NAME is defined %}
##############################################
# 哨兵模式下的查看Redis服务进程和端口状态
alias redisSentinelStatus='ps -ef|grep -v grep|grep --color=always redis-server && ps -ef|grep -v grep|grep -c redis-server && echo "以上数字为2，则说明redis-server哨兵模式进程数正常"'
alias redisSentinelPort='netstat -tunlp|grep -v grep|grep --color=always redis-server|grep --color=always -E "{{ REDIS_LISTEN_PORT }}|{{ REDIS_SENTINEL_LISTEN_PORT }}" && echo "正常监听 {{ REDIS_LISTEN_PORT }} 和 {{ REDIS_SENTINEL_LISTEN_PORT }} 则说明redis-server哨兵模式端口正常"'
# Redis哨兵模式命令行
alias cmdRedisSentinel='{{ REDIS_BASE_DIR }}/bin/redis-cli -p {{ REDIS_SENTINEL_LISTEN_PORT }} -a {{ REDIS_PASSWORD }}'
##############################################
{% endif %}

{% if REDIS_CLUSTER_APP_NAME is defined %}
##############################################
# 集群模式下的查看Redis服务进程和端口状态
alias redisClusterStatus='ps -ef|grep -v grep|grep --color=always redis-server && ps -ef|grep -v grep|grep -c redis-server && echo "以上数字为2，则说明redis-server集群模式进程数正常"'
alias redisClusterPort='netstat -tunlp|grep -v grep|grep --color=always redis-server|grep --color=always -E "{{ REDIS_LISTEN_PORT }}|{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}" && echo "正常监听 {{ REDIS_LISTEN_PORT }} 和 {{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }} 则说明redis-server集群模式端口正常"'
# Redis集群模式命令行
alias cmdRedisCluster='{{ REDIS_BASE_DIR }}/bin/redis-cli -p {{ REDIS_LISTEN_PORT }} -a {{ REDIS_PASSWORD }} -c'
##############################################
{% endif %}

```

在快捷命令模板文件中第21行和31行，分别增加了`if REDIS_SENTINEL_APP_NAME is defined`和`if REDIS_CLUSTER_APP_NAME is defined`判断语句，用于确认到底设置哨兵模式下的快捷命令还是设置集群模式下的快捷命令。



#### 3.4.6 supervisor应用配置文件修改

由于在3.3.4节已经修改了`roles/redis/templates/redis.ini.j2`文件，并增加了启动优先级参数配置`priority = 991`。这个配置在集群模式下不用再修改。

新增一个集群模板下的从节点的supervisor应用配置文件`roles/redis/templates/redis-cluster.ini.j2`：

```ini
# roles/redis/templates/redis-cluster.ini.j2
[program:{{ REDIS_CLUSTER_APP_NAME }}]
command = {{ REDIS_BASE_DIR }}/bin/redis-server {{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.conf
directory = {{ REDIS_BASE_DIR }}
user = {{ REDIS_RUNNING_USER }}
stdout_logfile = {{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 10
redirect_stderr = true
autorestart = true
autostart = true
# 设置优先级，程序启停的优先级，数字越小优先级越高，默认999
# 集群从节点程序要在主节点启动后再启动
priority = 992

```

也就是先启动集群master主节点后，再启动slave从节点。



#### 3.4.7 增加集群程序任务配置文件

增加集群程序任务配置文件`roles/redis/tasks/redis-cluster.yaml`:

```yaml
---
# roles/redis/tasks/redis-cluster.yaml
- name: Display the redis password
  ansible.builtin.debug:
    msg: "{{ REDIS_PASSWORD }}"
  changed_when: false

- name: Copy cluster redis-cluster.conf file
  ansible.builtin.template:
    # 这个地方注意，如果使用with_items来循环变量，
    # 则在模板文件redis-cluster.conf.j2中是使用`{{ item }}` 来代替端口号变量的
    # 为了让模板文件里面的意义更明确，我使用loop方式来循环变量
    # 然后使用loop_control来设置loop_var来代替item变量，并配置到模板文件中
    # 详细可参考 https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html#accessing-the-name-of-your-loop-var
    src: redis-cluster.conf.j2
    # dest: "{{ REDIS_BASE_DIR }}/conf/redis_{{ item }}.conf"
    dest: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.conf"
    mode: '0600'
    force: yes
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  # with_items:
  loop:
    - "{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}"
  loop_control:
    loop_var: REDIS_CLUSTER_LISTEN_PORT

- name: Set redis cluster info
  ansible.builtin.blockinfile:
    path: "{{ REDIS_BASE_DIR }}/conf/redis_{{ item }}.conf"
    # 默认将redishosts组中第一个节点作为master节点
    # 注意此处sentinel monitor mymaster后面要用 REDIS_LISTEN_PORT 这个变量
    block: |
      # 开启集群模式
      cluster-enabled yes
      # 集群内部配置文件名称，由redis自动管理
      cluster-config-file nodes-{{ item }}.conf
      # 节点超时时间，单位毫秒
      cluster-node-timeout 15000
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add sentinel monitor info"
  loop:
    - "{{ REDIS_LISTEN_PORT }}"
    - "{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}"

- name: Change the redis log file Permission
  ansible.builtin.file:
    path: "{{ item }}"
    state: touch
    mode: '0644'
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
  with_items:
    - "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.log"

- name: Copy redis cluster app config
  ansible.builtin.template:
    src: redis-cluster.ini.j2
    dest: /etc/supervisord.d/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.ini
    force: yes
    backup: yes
    remote_src: no

- name: Start service supervisord, in all cases
  ansible.builtin.service:
    name: supervisord
    state: restarted
    # 开机启动
    enabled: yes

- name: Print create cluster command
  ansible.builtin.debug:
    # --cluster-yes 参数会自动地回答 "yes"
    # 此除不自动创建集群，而是生成创建集群的命令，便于部署后，记录部署命令，方便后期查询Redis命令过程
    msg: |
        Please run the follow command to create cluster:
        {{ REDIS_BASE_DIR }}/bin/redis-cli -a {{ REDIS_PASSWORD }} --cluster-yes --cluster-replicas 1 --cluster create {{ groups["redishosts"]|first }}:{{ REDIS_LISTEN_PORT }} {{ groups["redishosts"]|first }}:{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }} {{ groups["redishosts"][1] }}:{{ REDIS_LISTEN_PORT }} {{ groups["redishosts"][1] }}:{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }} {{ groups["redishosts"][2] }}:{{ REDIS_LISTEN_PORT }} {{ groups["redishosts"][2] }}:{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}
  changed_when: false
  # 委派给Redis第一个主机
  delegate_to: "{{ groups['redishosts']|first }}"
  # 且只运行一次
  run_once: true

```



这一节的集群任务配置比较特别，最开始想着设置集群模式Ansible任务时不在主从模式的基础配置上配置，自己单独创建一个任务，用来设置集群主节点和从节点。所以有了最开始的`Copy cluster redis-cluster.conf file`任务来循环两个变量，一个是Redis集群模式下主程序监听端口`REDIS_CLUSTER_MASTER_LISTEN_PORT: 29736`，另一个是Redis集群模式下从程序监听端口`REDIS_CLUSTER_SLAVE_LISTEN_PORT: 29737`,此时就要根据端口不同，在Redis程序的配置文件里面使用不同的端口变量。因此就有了使用`loop`和`loop_control.loop_var`来设置循环变量名的任务配置。

这个时候配置文件里面跟自定义循环变量`REDIS_CLUSTER_LISTEN_PORT`相关的配置：

```sh
[root@ansible ansible_playbooks]# grep REDIS_CLUSTER_LISTEN_PORT roles/redis/templates/redis-cluster.conf.j2
#   建议修改为10000以上，60000以下的端口，我这里设置为{{ REDIS_CLUSTER_LISTEN_PORT }}
port {{ REDIS_CLUSTER_LISTEN_PORT }}
pidfile {{ REDIS_BASE_DIR }}/pid/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.pid
# logfile "/srv/redis/logs/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.log"
logfile "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_CLUSTER_LISTEN_PORT }}.log"
dbfilename dump_{{ REDIS_CLUSTER_LISTEN_PORT }}.rdb
appendfilename "appendonly_{{ REDIS_CLUSTER_LISTEN_PORT }}.aof"
[root@ansible ansible_playbooks]#
```



后来发现，我不需要再单独配置三个节点上的Redis master任务，因为主从任务第一步就是这样做过了。

如果`Copy cluster redis-cluster.conf file`任务不用`loop`循环，其实可以直接使用`REDIS_CLUSTER_SLAVE_LISTEN_PORT`这个变量配置即可。

```yaml
- name: Copy cluster redis-cluster.conf file
  ansible.builtin.template:
    src: redis-cluster.conf.j2
    dest: "{{ REDIS_BASE_DIR }}/conf/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.conf"
    mode: '0600'
    force: yes
    remote_src: no
    owner: "{{ REDIS_RUNNING_USER }}"
    group: "{{ REDIS_RUNNING_USER }}"
```

相应的任务就像上面这样简单。然后配置文件中跟端口相关的，就用`REDIS_CLUSTER_SLAVE_LISTEN_PORT`变量代替就行了。

此时，只用将模板文件里面的`REDIS_CLUSTER_LISTEN_PORT`替换成`REDIS_CLUSTER_SLAVE_LISTEN_PORT`即可，就像下面这样：

```sh
[root@ansible ansible_playbooks]# grep REDIS_CLUSTER_SLAVE_LISTEN_PORT roles/redis/templates/redis-cluster.conf.j2
#   建议修改为10000以上，60000以下的端口，我这里设置为{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}
port {{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}
pidfile {{ REDIS_BASE_DIR }}/pid/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.pid
# logfile "/srv/redis/logs/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.log"
logfile "{{ REDIS_BASE_DIR }}/logs/redis_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.log"
dbfilename dump_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.rdb
appendfilename "appendonly_{{ REDIS_CLUSTER_SLAVE_LISTEN_PORT }}.aof"
[root@ansible ansible_playbooks]#
```

#### 3.4.8  角色入口main.yml修改

角色入口配置文件`roles/redis/tasks/main.yml`:

```yaml
---
# roles/redis/tasks/main.yml
# redis角色任务
# 安装redis
- include: redis.yaml
# 优化系统设置
- include: sysctl.yaml
# 使用supervisor进程管理工具配置redis app
- include: supervisor.yaml
# 创建快捷命令
- include: alias.yaml
# 根据是否定义REDIS_SENTINEL_APP_NAME环境变量决定是否要部署Redis哨兵模式
- name: Config redis sentinel tasks
  include_tasks: redis-sentinel.yaml
  when: REDIS_SENTINEL_APP_NAME is defined and REDIS_CLUSTER_APP_NAME is not defined
# 根据是否定义REDIS_CLUSTER_APP_NAME环境变量决定是否要部署Redis集群模式
- name: Config redis cluster tasks
  include_tasks: redis-cluster.yaml
  when: REDIS_SENTINEL_APP_NAME is not defined and REDIS_CLUSTER_APP_NAME is defined
```

由于哨兵模式和集群模式不能同时步骤，因此在角色入口中增加了两个`when`条件判断。

- 当`REDIS_SENTINEL_APP_NAME`变量定义了，`REDIS_CLUSTER_APP_NAME`变量未定义时，就按哨兵模式部署。
- 当`REDIS_SENTINEL_APP_NAME`变量未定义，`REDIS_CLUSTER_APP_NAME`变量定义了时，就按集群模式部署。



此时优化后的`hosts.ini`配置文件如下：

```ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3

[redishosts]
# !!!! redis部署的时候，三种类型不能都配置，应选择其中一种配置

# 类型1，主从模式配置
# REDIS_ROLE 代表主从节点的角色
#   REDIS_ROLE=master 则表明该节点部署redis主节点
#   REDIS_ROLE=slave  则表明该节点部署redis从节点
# REDIS_APP_NAME          代表使用supervisor管理的redis主从应用的名称，主从模式时，必须配置这个环境变量
# REDIS_SENTINEL_APP_NAME 代表使用supervisor管理的redis哨兵应用的名称，哨兵模式时，必须配置这个环境变量
# 192.168.56.121 hostname=ansible-node1 REDIS_ROLE=master
# 192.168.56.122 hostname=ansible-node2 REDIS_ROLE=slave
# 192.168.56.123 hostname=ansible-node3 REDIS_ROLE=slave
#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# 类型2，哨兵模式配置
# REDIS_ROLE 代表主从节点的角色
#   REDIS_ROLE=master 则表明该节点部署redis主节点
#   REDIS_ROLE=slave  则表明该节点部署redis从节点
# REDIS_APP_NAME          代表使用supervisor管理的redis主从应用的名称，主从模式时，必须配置这个环境变量
# REDIS_SENTINEL_APP_NAME 代表使用supervisor管理的redis哨兵应用的名称，哨兵模式时，必须配置这个环境变量
# 192.168.56.121 hostname=ansible-node1 REDIS_ROLE=master REDIS_APP_NAME=redis-master REDIS_SENTINEL_APP_NAME=sentinel1
# 192.168.56.122 hostname=ansible-node2 REDIS_ROLE=slave  REDIS_APP_NAME=redis-slave1 REDIS_SENTINEL_APP_NAME=sentinel2
# 192.168.56.123 hostname=ansible-node3 REDIS_ROLE=slave  REDIS_APP_NAME=redis-slave2 REDIS_SENTINEL_APP_NAME=sentinel3
#----------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------
# 类型3，集群模式配置
# REDIS_ROLE 代表主从节点的角色
#   REDIS_ROLE=master 则表明该节点部署redis主节点
#   REDIS_ROLE=slave  则表明该节点部署redis从节点
# REDIS_APP_NAME          代表使用supervisor管理的redis主从应用master的名称，主从模式时，必须配置这个环境变量
# REDIS_CLUSTER_APP_NAME  代表使用supervisor管理的redis集群应用slave的名称， 集群模式时，必须配置这个环境变量
192.168.56.121 hostname=ansible-node1 REDIS_ROLE=master REDIS_APP_NAME=redis-cluster-1 REDIS_CLUSTER_APP_NAME=redis-cluster-2
192.168.56.122 hostname=ansible-node2 REDIS_ROLE=master REDIS_APP_NAME=redis-cluster-3 REDIS_CLUSTER_APP_NAME=redis-cluster-4
192.168.56.123 hostname=ansible-node3 REDIS_ROLE=master REDIS_APP_NAME=redis-cluster-5 REDIS_CLUSTER_APP_NAME=redis-cluster-6
#----------------------------------------------------------------------------------------------------------

```





整体修改完成后，就可以再执行一次剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini redis.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [redishosts] *************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [redis : Add the user with a specific shell] *****************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}
ok: [192.168.56.122] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}
ok: [192.168.56.123] => {"append": false, "changed": false, "comment": "Redis Database Server", "group": 1001, "home": "/home/redis", "move_home": false, "name": "redis", "shell": "/sbin/nologin", "state": "present", "uid": 1001}

TASK [redis : Unarchive the source package] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1722438276.17-3712-90570485465826/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1722438276.17-3712-90570485465826/source", "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1722438276.17-3710-113782554686148/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 79, "src": "/root/.ansible/tmp/ansible-tmp-1722438276.17-3710-113782554686148/source", "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv", "-z", "--owner=redis", "--group=redis", "-f", "/root/.ansible/tmp/ansible-tmp-1722438276.15-3709-169842930830397/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 62, "src": "/root/.ansible/tmp/ansible-tmp-1722438276.15-3709-169842930830397/source", "state": "directory", "uid": 0}

TASK [redis : Create a symbolic link] *****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/redis", "gid": 0, "group": "root", "mode": "0777", "owner": "root", "size": 17, "src": "/srv/redis-6.2.14", "state": "link", "uid": 0}

TASK [redis : Create a directory if it does not exist] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis", "mode": "0755", "owner": "redis", "path": "/srv/redis-6.2.14", "size": 17, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/conf) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/conf", "mode": "0755", "owner": "redis", "path": "/srv/redis/conf", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/pid) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/pid", "mode": "0755", "owner": "redis", "path": "/srv/redis/pid", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/logs", "mode": "0755", "owner": "redis", "path": "/srv/redis/logs", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.121] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/data) => {"ansible_loop_var": "item", "changed": true, "gid": 1001, "group": "redis", "item": "/srv/redis/data", "mode": "0755", "owner": "redis", "path": "/srv/redis/data", "size": 6, "state": "directory", "uid": 1001}

TASK [redis : Create a random password] ***************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> localhost] => {"ansible_facts": {"REDIS_PASSWORD": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"}, "changed": false}

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
}
ok: [192.168.56.122] => {
    "msg": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
}
ok: [192.168.56.123] => {
    "msg": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
}

TASK [Copy redis.conf file] ***************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "980092dc52696352ac293e540c41d136f2d5cd16", "dest": "/srv/redis/conf/redis_29736.conf", "gid": 1001, "group": "redis", "md5sum": "5e90d4ac18075b4117ace021d2f41229", "mode": "0600", "owner": "redis", "size": 143862, "src": "/root/.ansible/tmp/ansible-tmp-1722438279.59-3904-106712456085095/source", "state": "file", "uid": 1001}
changed: [192.168.56.123] => {"changed": true, "checksum": "a821a334242c9ea24fd69a8d74cc4a2ddb0cf74f", "dest": "/srv/redis/conf/redis_29736.conf", "gid": 1001, "group": "redis", "md5sum": "5b5c03adbe2a4a62bc6db8a8acdbe53b", "mode": "0600", "owner": "redis", "size": 143862, "src": "/root/.ansible/tmp/ansible-tmp-1722438279.61-3905-3570142264372/source", "state": "file", "uid": 1001}
changed: [192.168.56.121] => {"changed": true, "checksum": "f6b51861b7a18be98ed91c6beae308ccd40e17c1", "dest": "/srv/redis/conf/redis_29736.conf", "gid": 1001, "group": "redis", "md5sum": "3d72ee68a72632a4afbef70ef4946933", "mode": "0600", "owner": "redis", "size": 143862, "src": "/root/.ansible/tmp/ansible-tmp-1722438279.6-3903-277467351838764/source", "state": "file", "uid": 1001}

TASK [redis : Set replicaof masterip masterport info] *************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.122] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.123] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [redis : Set masterauth master-password info] ****************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.122] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.123] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs/redis_29736.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29736.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29736.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [redis : Set vm.overcommit_memory value] *********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.123] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}

TASK [redis : Set net.core.somaxconn value] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false}
ok: [192.168.56.121] => {"changed": false}
ok: [192.168.56.123] => {"changed": false}

TASK [Set redis open files] ***************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "msg": ""}
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.123] => {"changed": false, "msg": ""}

TASK [Copy redis app config] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "e010505123d4902d0b111b152967c20d945d877e", "dest": "/etc/supervisord.d/redis_29736.ini", "gid": 0, "group": "root", "md5sum": "a4bb01a35d72b9d92eb873a6e934598a", "mode": "0644", "owner": "root", "size": 439, "src": "/root/.ansible/tmp/ansible-tmp-1722438282.04-4071-191268302655959/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "checksum": "d1387c58d0b676d8c1c5d31627d52e7a3ae1d395", "dest": "/etc/supervisord.d/redis_29736.ini", "gid": 0, "group": "root", "md5sum": "d6c2cfa3fd42b39297fd5ab00d69e4de", "mode": "0644", "owner": "root", "size": 439, "src": "/root/.ansible/tmp/ansible-tmp-1722438282.06-4074-170174061044641/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "72185daa846522823689a7f6d62df55ad7ee4b9d", "dest": "/etc/supervisord.d/redis_29736.ini", "gid": 0, "group": "root", "md5sum": "3e2f53bc88c9aaafeed3f3549247f3da", "mode": "0644", "owner": "root", "size": 439, "src": "/root/.ansible/tmp/ansible-tmp-1722438282.05-4072-114502681878553/source", "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Wed 2024-07-31 22:17:05 CST", "ActiveEnterTimestampMonotonic": "2592716734", "ActiveExitTimestamp": "Wed 2024-07-31 22:17:05 CST", "ActiveExitTimestampMonotonic": "2592493536", "ActiveState": "active", "After": "systemd-journald.socket system.slice nss-user-lookup.target rc-local.service basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Wed 2024-07-31 22:17:05 CST", "AssertTimestampMonotonic": "2592591538", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Wed 2024-07-31 22:17:05 CST", "ConditionTimestampMonotonic": "2592591537", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "4580", "ExecMainStartTimestamp": "Wed 2024-07-31 22:17:05 CST", "ExecMainStartTimestampMonotonic": "2592716717", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Wed 2024-07-31 22:17:05 CST] ; stop_time=[Wed 2024-07-31 22:17:05 CST] ; pid=4578 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Wed 2024-07-31 22:17:05 CST", "InactiveEnterTimestampMonotonic": "2592591280", "InactiveExitTimestamp": "Wed 2024-07-31 22:17:05 CST", "InactiveExitTimestampMonotonic": "2592591832", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "4580", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Wed 2024-07-31 22:17:05 CST", "WatchdogTimestampMonotonic": "2592716725", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Wed 2024-07-31 22:17:05 CST", "ActiveEnterTimestampMonotonic": "2594915411", "ActiveExitTimestamp": "Wed 2024-07-31 22:17:05 CST", "ActiveExitTimestampMonotonic": "2594724784", "ActiveState": "active", "After": "system.slice nss-user-lookup.target systemd-journald.socket basic.target rc-local.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Wed 2024-07-31 22:17:05 CST", "AssertTimestampMonotonic": "2594791251", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Wed 2024-07-31 22:17:05 CST", "ConditionTimestampMonotonic": "2594791251", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "4554", "ExecMainStartTimestamp": "Wed 2024-07-31 22:17:05 CST", "ExecMainStartTimestampMonotonic": "2594915393", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Wed 2024-07-31 22:17:05 CST] ; stop_time=[Wed 2024-07-31 22:17:05 CST] ; pid=4553 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Wed 2024-07-31 22:17:05 CST", "InactiveEnterTimestampMonotonic": "2594790828", "InactiveExitTimestamp": "Wed 2024-07-31 22:17:05 CST", "InactiveExitTimestampMonotonic": "2594791625", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "4554", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Wed 2024-07-31 22:17:05 CST", "WatchdogTimestampMonotonic": "2594915402", "WatchdogUSec": "0"}}
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Wed 2024-07-31 22:17:05 CST", "ActiveEnterTimestampMonotonic": "2595749152", "ActiveExitTimestamp": "Wed 2024-07-31 22:17:05 CST", "ActiveExitTimestampMonotonic": "2595573329", "ActiveState": "active", "After": "system.slice basic.target systemd-journald.socket rc-local.service nss-user-lookup.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Wed 2024-07-31 22:17:05 CST", "AssertTimestampMonotonic": "2595630632", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Wed 2024-07-31 22:17:05 CST", "ConditionTimestampMonotonic": "2595630632", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "4587", "ExecMainStartTimestamp": "Wed 2024-07-31 22:17:05 CST", "ExecMainStartTimestampMonotonic": "2595749136", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Wed 2024-07-31 22:17:05 CST] ; stop_time=[Wed 2024-07-31 22:17:05 CST] ; pid=4586 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Wed 2024-07-31 22:17:05 CST", "InactiveEnterTimestampMonotonic": "2595630431", "InactiveExitTimestamp": "Wed 2024-07-31 22:17:05 CST", "InactiveExitTimestampMonotonic": "2595630877", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "4587", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Wed 2024-07-31 22:17:05 CST", "WatchdogTimestampMonotonic": "2595749144", "WatchdogUSec": "0"}}

TASK [redis : Copy alias config] **********************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"backup_file": "/root/.alias_redis.sh.5725.2024-07-31@23:04:44~", "changed": true, "checksum": "8440d69c007b7d7388ae44766e3a6b7bf8f69c6d", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "3217d6d8e5ae24dc9d2ebdff9a1c4241", "mode": "0644", "owner": "root", "size": 2099, "src": "/root/.ansible/tmp/ansible-tmp-1722438283.62-4151-50395483474870/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"backup_file": "/root/.alias_redis.sh.5776.2024-07-31@23:04:44~", "changed": true, "checksum": "8440d69c007b7d7388ae44766e3a6b7bf8f69c6d", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "3217d6d8e5ae24dc9d2ebdff9a1c4241", "mode": "0644", "owner": "root", "size": 2099, "src": "/root/.ansible/tmp/ansible-tmp-1722438283.61-4148-79565800441436/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => {"backup_file": "/root/.alias_redis.sh.5769.2024-07-31@23:04:44~", "changed": true, "checksum": "8440d69c007b7d7388ae44766e3a6b7bf8f69c6d", "dest": "/root/.alias_redis.sh", "gid": 0, "group": "root", "md5sum": "3217d6d8e5ae24dc9d2ebdff9a1c4241", "mode": "0644", "owner": "root", "size": 2099, "src": "/root/.ansible/tmp/ansible-tmp-1722438283.59-4146-28763835120711/source", "state": "file", "uid": 0}

TASK [redis : Insert block to .bashrc] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"changed": false, "msg": ""}
ok: [192.168.56.121] => {"changed": false, "msg": ""}
ok: [192.168.56.123] => {"changed": false, "msg": ""}

TASK [Config redis sentinel tasks] ********************************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.122] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.123] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [Config redis cluster tasks] *********************************************************************************************************************************************************************************************************************************************
included: /root/ansible_playbooks/roles/redis/tasks/redis-cluster.yaml for 192.168.56.121, 192.168.56.122, 192.168.56.123

TASK [Display the redis password] *********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
}
ok: [192.168.56.122] => {
    "msg": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
}
ok: [192.168.56.123] => {
    "msg": "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
}

TASK [Copy cluster redis-cluster.conf file] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item=29737) => {"REDIS_CLUSTER_LISTEN_PORT": 29737, "ansible_loop_var": "REDIS_CLUSTER_LISTEN_PORT", "changed": true, "checksum": "d28095a10ffebba0c29c3e5ff4570d9741769bb4", "dest": "/srv/redis/conf/redis_29737.conf", "gid": 1001, "group": "redis", "md5sum": "bfed3338bd599f109e67729c33e7709b", "mode": "0600", "owner": "redis", "size": 143707, "src": "/root/.ansible/tmp/ansible-tmp-1722438284.97-4240-87903810918065/source", "state": "file", "uid": 1001}
changed: [192.168.56.121] => (item=29737) => {"REDIS_CLUSTER_LISTEN_PORT": 29737, "ansible_loop_var": "REDIS_CLUSTER_LISTEN_PORT", "changed": true, "checksum": "17af9ffc6723c209cb3d7e30a1d237614b34e493", "dest": "/srv/redis/conf/redis_29737.conf", "gid": 1001, "group": "redis", "md5sum": "eac3d1f60e77232ad607df36da6b1565", "mode": "0600", "owner": "redis", "size": 143707, "src": "/root/.ansible/tmp/ansible-tmp-1722438284.97-4239-232614154171372/source", "state": "file", "uid": 1001}
changed: [192.168.56.123] => (item=29737) => {"REDIS_CLUSTER_LISTEN_PORT": 29737, "ansible_loop_var": "REDIS_CLUSTER_LISTEN_PORT", "changed": true, "checksum": "340017c9f9a6c0d17b8dd93bf16394f0dbe947bf", "dest": "/srv/redis/conf/redis_29737.conf", "gid": 1001, "group": "redis", "md5sum": "97d30b0d343aa326f4abf4bf9b4140c9", "mode": "0600", "owner": "redis", "size": 143707, "src": "/root/.ansible/tmp/ansible-tmp-1722438284.97-4241-211864853392154/source", "state": "file", "uid": 1001}

TASK [Set redis cluster info] *************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => (item=29736) => {"ansible_loop_var": "item", "changed": true, "item": 29736, "msg": "Block inserted"}
changed: [192.168.56.122] => (item=29736) => {"ansible_loop_var": "item", "changed": true, "item": 29736, "msg": "Block inserted"}
changed: [192.168.56.121] => (item=29736) => {"ansible_loop_var": "item", "changed": true, "item": 29736, "msg": "Block inserted"}
changed: [192.168.56.123] => (item=29737) => {"ansible_loop_var": "item", "changed": true, "item": 29737, "msg": "Block inserted"}
changed: [192.168.56.122] => (item=29737) => {"ansible_loop_var": "item", "changed": true, "item": 29737, "msg": "Block inserted"}
changed: [192.168.56.121] => (item=29737) => {"ansible_loop_var": "item", "changed": true, "item": 29737, "msg": "Block inserted"}

TASK [Change the redis log file Permission] ***********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/srv/redis/logs/redis_29737.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29737.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29737.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.122] => (item=/srv/redis/logs/redis_29737.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29737.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29737.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}
changed: [192.168.56.123] => (item=/srv/redis/logs/redis_29737.log) => {"ansible_loop_var": "item", "changed": true, "dest": "/srv/redis/logs/redis_29737.log", "gid": 1001, "group": "redis", "item": "/srv/redis/logs/redis_29737.log", "mode": "0644", "owner": "redis", "size": 0, "state": "file", "uid": 1001}

TASK [Copy redis cluster app config] ******************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "29540833b5bb7ed2e44155f83c2846e844331953", "dest": "/etc/supervisord.d/redis_29737.ini", "gid": 0, "group": "root", "md5sum": "bcb37b503767f4d8cab2d3eb5983d87b", "mode": "0644", "owner": "root", "size": 504, "src": "/root/.ansible/tmp/ansible-tmp-1722438286.71-4363-76362813721597/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "checksum": "5062428b79f20aa1baa9ffe7203367af51086534", "dest": "/etc/supervisord.d/redis_29737.ini", "gid": 0, "group": "root", "md5sum": "93d8964977507a81fdb3678ee195eeb2", "mode": "0644", "owner": "root", "size": 504, "src": "/root/.ansible/tmp/ansible-tmp-1722438286.72-4362-96347827770081/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "checksum": "877847c18de37d6ac1231447598f423ec7861b56", "dest": "/etc/supervisord.d/redis_29737.ini", "gid": 0, "group": "root", "md5sum": "b183b7a1a79b93951877ac31865fa617", "mode": "0644", "owner": "root", "size": 504, "src": "/root/.ansible/tmp/ansible-tmp-1722438286.76-4364-229139754029966/source", "state": "file", "uid": 0}

TASK [redis : Start service supervisord, in all cases] ************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Wed 2024-07-31 23:04:43 CST", "ActiveEnterTimestampMonotonic": "5450811189", "ActiveExitTimestamp": "Wed 2024-07-31 23:04:43 CST", "ActiveExitTimestampMonotonic": "5450642051", "ActiveState": "active", "After": "systemd-journald.socket system.slice nss-user-lookup.target rc-local.service basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Wed 2024-07-31 23:04:43 CST", "AssertTimestampMonotonic": "5450672751", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Wed 2024-07-31 23:04:43 CST", "ConditionTimestampMonotonic": "5450672751", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "5636", "ExecMainStartTimestamp": "Wed 2024-07-31 23:04:43 CST", "ExecMainStartTimestampMonotonic": "5450811173", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Wed 2024-07-31 23:04:43 CST] ; stop_time=[Wed 2024-07-31 23:04:43 CST] ; pid=5635 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Wed 2024-07-31 23:04:43 CST", "InactiveEnterTimestampMonotonic": "5450672510", "InactiveExitTimestamp": "Wed 2024-07-31 23:04:43 CST", "InactiveExitTimestampMonotonic": "5450673051", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "5636", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Wed 2024-07-31 23:04:43 CST", "WatchdogTimestampMonotonic": "5450811181", "WatchdogUSec": "0"}}
changed: [192.168.56.122] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Wed 2024-07-31 23:04:43 CST", "ActiveEnterTimestampMonotonic": "5453058079", "ActiveExitTimestamp": "Wed 2024-07-31 23:04:43 CST", "ActiveExitTimestampMonotonic": "5452891164", "ActiveState": "active", "After": "system.slice nss-user-lookup.target systemd-journald.socket basic.target rc-local.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Wed 2024-07-31 23:04:43 CST", "AssertTimestampMonotonic": "5452923734", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Wed 2024-07-31 23:04:43 CST", "ConditionTimestampMonotonic": "5452923734", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "5687", "ExecMainStartTimestamp": "Wed 2024-07-31 23:04:43 CST", "ExecMainStartTimestampMonotonic": "5453058062", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Wed 2024-07-31 23:04:43 CST] ; stop_time=[Wed 2024-07-31 23:04:43 CST] ; pid=5686 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Wed 2024-07-31 23:04:43 CST", "InactiveEnterTimestampMonotonic": "5452923476", "InactiveExitTimestamp": "Wed 2024-07-31 23:04:43 CST", "InactiveExitTimestampMonotonic": "5452924032", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "5687", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Wed 2024-07-31 23:04:43 CST", "WatchdogTimestampMonotonic": "5453058071", "WatchdogUSec": "0"}}
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestamp": "Wed 2024-07-31 23:04:43 CST", "ActiveEnterTimestampMonotonic": "5453905339", "ActiveExitTimestamp": "Wed 2024-07-31 23:04:43 CST", "ActiveExitTimestampMonotonic": "5453735528", "ActiveState": "active", "After": "system.slice basic.target systemd-journald.socket rc-local.service nss-user-lookup.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Wed 2024-07-31 23:04:43 CST", "AssertTimestampMonotonic": "5453770880", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Wed 2024-07-31 23:04:43 CST", "ConditionTimestampMonotonic": "5453770880", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/supervisord.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "5680", "ExecMainStartTimestamp": "Wed 2024-07-31 23:04:43 CST", "ExecMainStartTimestampMonotonic": "5453905321", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[Wed 2024-07-31 23:04:43 CST] ; stop_time=[Wed 2024-07-31 23:04:43 CST] ; pid=5679 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Wed 2024-07-31 23:04:43 CST", "InactiveEnterTimestampMonotonic": "5453770520", "InactiveExitTimestamp": "Wed 2024-07-31 23:04:43 CST", "InactiveExitTimestampMonotonic": "5453771388", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "65535", "LimitNPROC": "31193", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "31193", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "5680", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Wed 2024-07-31 23:04:43 CST", "WatchdogTimestampMonotonic": "5453905330", "WatchdogUSec": "0"}}

TASK [redis : Print create cluster command] ***********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121 -> 192.168.56.121] => {
    "msg": "Please run the follow command to create cluster:\n/srv/redis/bin/redis-cli -a fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R --cluster-yes --cluster-replicas 1 --cluster create 192.168.56.121:29736 192.168.56.121:29737 192.168.56.122:29736 192.168.56.122:29737 192.168.56.123:29736 192.168.56.123:29737\n"
}

PLAY RECAP ********************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=24   changed=13   unreachable=0    failed=0    skipped=3    rescued=0    ignored=0
192.168.56.122             : ok=22   changed=13   unreachable=0    failed=0    skipped=3    rescued=0    ignored=0
192.168.56.123             : ok=22   changed=13   unreachable=0    failed=0    skipped=3    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 13 seconds
[root@ansible ansible_playbooks]#
```

执行过程最后几个任务的截图：

![](/img/Snipaste_2024-07-31_23-08-06.png)



- `Set redis cluster info`这个任务就是在各个配置文件后面增加启用redis集群模式相关的配置项。
- `Print create cluster command` 这个任务就是打印出来创建Redis三主三从6节点集群模式的命令。

我们在各个节点上检查一下：

```sh
# 在节点1上面检查
# 查看运行的应用信息
[root@ansible-node1 ~]# spstatus
redis-cluster-1                  RUNNING   pid 6223, uptime 0:09:22
redis-cluster-2                  RUNNING   pid 6224, uptime 0:09:22
testapp                          RUNNING   pid 6225, uptime 0:09:22


# 查看生成的Redis配置文件最后的集群模式开关信息
[root@ansible-node1 ~]# tail /srv/redis/conf/redis_29736.conf
#
# ignore-warnings ARM64-COW-BUG
# BEGIN meizhaohui add sentinel monitor info
# 开启集群模式
cluster-enabled yes
# 集群内部配置文件名称，由redis自动管理
cluster-config-file nodes-29736.conf
# 节点超时时间，单位毫秒
cluster-node-timeout 15000
# END meizhaohui add sentinel monitor info
[root@ansible-node1 ~]# tail /srv/redis/conf/redis_29737.conf
#
# ignore-warnings ARM64-COW-BUG
# BEGIN meizhaohui add sentinel monitor info
# 开启集群模式
cluster-enabled yes
# 集群内部配置文件名称，由redis自动管理
cluster-config-file nodes-29737.conf
# 节点超时时间，单位毫秒
cluster-node-timeout 15000
# END meizhaohui add sentinel monitor info


# 查看Redis相关的快捷命令
[root@ansible-node1 ~]# alias|grep -i Redis
alias cdRedis='cd /srv/redis && pwd && ls -lah'
alias cleanRedisTemplate='spctl stop all && rm -rf /etc/supervisord.d/redis*.ini && rm -rf /srv/redis* && spctl update && spctl start testapp && spstatus'
alias cmdRedis='/srv/redis/bin/redis-cli -p 29736 -a fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R'
alias cmdRedisCluster='/srv/redis/bin/redis-cli -p 29736 -a fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R -c'
alias getRedisPassword='grep "^requirepass" /srv/redis/conf/redis*|head -n 1'
alias redisClusterPort='netstat -tunlp|grep -v grep|grep --color=always redis-server|grep --color=always -E "29736|29737" && echo "正常监听 29736 和 29737 则说明redis-server集群模式端口正常"'
alias redisClusterStatus='ps -ef|grep -v grep|grep --color=always redis-server && ps -ef|grep -v grep|grep -c redis-server && echo "以上数字为2，则说明redis-server集群模式进程数正常"'
alias redisPort='netstat -tunlp|grep -v grep|grep --color=always redis-server && echo "正常监听 29736 则说明redis-server端口正常"'
alias redisStatus='ps -ef|grep -v grep|grep --color=always redis-server && ps -ef|grep -v grep|grep -c redis-server && echo "以上数字为1，则说明redis-server服务进程数正常"'


# 复制ansible里面的输出，创建Redis集群
[root@ansible-node1 ~]# /srv/redis/bin/redis-cli -a fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R --cluster-yes --cluster-replicas 1 --cluster create                                        192.168.56.121:29736 192.168.56.121:29737 192.168.56.122:29736 192.168.56.122:29737 192.168.56.123:29736 192.168.56.123:29737
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 192.168.56.122:29737 to 192.168.56.121:29736
Adding replica 192.168.56.123:29737 to 192.168.56.122:29736
Adding replica 192.168.56.121:29737 to 192.168.56.123:29736
M: 9f28f72e23019d1d8fdacbada6acbf2974b28c33 192.168.56.121:29736
   slots:[0-5460] (5461 slots) master
S: 8c46b1b8426b7dce74772fd98d184af3215d7537 192.168.56.121:29737
   replicates 7c63efd0d2e2da39ab505fc0f7c8c9cd6175067f
M: 23d7c73e2c31509742a387e7aae60cf7d8a87726 192.168.56.122:29736
   slots:[5461-10922] (5462 slots) master
S: 29aa6da47ad27731aa1ebec8c364148e0c4971f0 192.168.56.122:29737
   replicates 9f28f72e23019d1d8fdacbada6acbf2974b28c33
M: 7c63efd0d2e2da39ab505fc0f7c8c9cd6175067f 192.168.56.123:29736
   slots:[10923-16383] (5461 slots) master
S: 5ffb824a80c004cdf5ff3a97bc090506141e7cbf 192.168.56.123:29737
   replicates 23d7c73e2c31509742a387e7aae60cf7d8a87726
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
.....
>>> Performing Cluster Check (using node 192.168.56.121:29736)
M: 9f28f72e23019d1d8fdacbada6acbf2974b28c33 192.168.56.121:29736
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: 23d7c73e2c31509742a387e7aae60cf7d8a87726 192.168.56.122:29736
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
S: 8c46b1b8426b7dce74772fd98d184af3215d7537 192.168.56.121:29737
   slots: (0 slots) slave
   replicates 7c63efd0d2e2da39ab505fc0f7c8c9cd6175067f
S: 5ffb824a80c004cdf5ff3a97bc090506141e7cbf 192.168.56.123:29737
   slots: (0 slots) slave
   replicates 23d7c73e2c31509742a387e7aae60cf7d8a87726
M: 7c63efd0d2e2da39ab505fc0f7c8c9cd6175067f 192.168.56.123:29736
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: 29aa6da47ad27731aa1ebec8c364148e0c4971f0 192.168.56.122:29737
   slots: (0 slots) slave
   replicates 9f28f72e23019d1d8fdacbada6acbf2974b28c33
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
[root@ansible-node1 ~]#
```

可以看到，集群创建完成了。



![](/img/Snipaste_2024-07-31_23-17-51.png)

最后，再测试一下快捷命令能不能正常使用：

```sh
[root@ansible-node1 ~]# getRedisPassword
/srv/redis/conf/redis_29736.conf:requirepass fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMVi8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R
[root@ansible-node1 ~]# redisStatus
redis     6223  6214  0 23:04 ?        00:00:00 /srv/redis/bin/redis-server /srv/redis/conf/redis_29736.conf
redis     6224  6214  0 23:04 ?        00:00:00 /srv/redis/bin/redis-server /srv/redis/conf/redis_29737.conf
2
以上数字为1，则说明redis-server服务进程数正常
[root@ansible-node1 ~]# redisPort
tcp        0      0 127.0.0.1:39736         0.0.0.0:*               LISTEN      6223/redis-server
tcp        0      0 192.168.56.121:39736    0.0.0.0:*               LISTEN      6223/redis-server
tcp        0      0 127.0.0.1:39737         0.0.0.0:*               LISTEN      6224/redis-server
tcp        0      0 192.168.56.121:39737    0.0.0.0:*               LISTEN      6224/redis-server
tcp        0      0 127.0.0.1:29736         0.0.0.0:*               LISTEN      6223/redis-server
tcp        0      0 192.168.56.121:29736    0.0.0.0:*               LISTEN      6223/redis-server
tcp        0      0 127.0.0.1:29737         0.0.0.0:*               LISTEN      6224/redis-server
tcp        0      0 192.168.56.121:29737    0.0.0.0:*               LISTEN      6224/redis-server
正常监听 29736 则说明redis-server端口正常
[root@ansible-node1 ~]# cmdRedis
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> info replication
# Replication
role:master
connected_slaves:1
slave0:ip=192.168.56.122,port=29737,state=online,offset=406,lag=0
master_failover_state:no-failover
master_replid:cea936999e901523976cfdb4f14c270bad583fb8
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:406
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:406
127.0.0.1:29736> exit
[root@ansible-node1 ~]# cmdRedisCluster
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:29736> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_ping_sent:323
cluster_stats_messages_pong_sent:315
cluster_stats_messages_sent:638
cluster_stats_messages_ping_received:310
cluster_stats_messages_pong_received:323
cluster_stats_messages_meet_received:5
cluster_stats_messages_received:638
127.0.0.1:29736> cluster nodes
23d7c73e2c31509742a387e7aae60cf7d8a87726 192.168.56.122:29736@39736 master - 0 1722439227857 3 connected 5461-10922
8c46b1b8426b7dce74772fd98d184af3215d7537 192.168.56.121:29737@39737 slave 7c63efd0d2e2da39ab505fc0f7c8c9cd6175067f 1722439228866 1722439224000 5 connected
5ffb824a80c004cdf5ff3a97bc090506141e7cbf 192.168.56.123:29737@39737 slave 23d7c73e2c31509742a387e7aae60cf7d8a87726 0 1722439227000 3 connected
7c63efd0d2e2da39ab505fc0f7c8c9cd6175067f 192.168.56.123:29736@39736 master - 0 1722439224828 5 connected 10923-16383
9f28f72e23019d1d8fdacbada6acbf2974b28c33 192.168.56.121:29736@39736 myself,master - 0 1722439225000 1 connected 0-5460
29aa6da47ad27731aa1ebec8c364148e0c4971f0 192.168.56.122:29737@39737 slave 9f28f72e23019d1d8fdacbada6acbf2974b28c33 0 1722439226843 1 connected
127.0.0.1:29736>
```

可以看到快捷命令可以使用，但`redisStatus`和`redisPort`的输出稍微有点不对，因为这两个命令之前是给Redis主从节点配置的。（少许差异此处不作修复，可以手动修改一下！）

而`cmdRedisCluster`是正常可以用的。





#### 3.4.9  测试集群模式读写

编写一个python连接集群模式的程序`test_redis_3master_3slave_cluster.py`:

```python
# filename: test_redis_3master_3slave_cluster.py
# pip install redis
from redis import RedisCluster
from redis.cluster import ClusterNode

password = "fKYeyA5br3rL7hN.nVykeyz:cFfhn5G,NJ_WwPbpRA5c5xdi66s1gyuvYZMV" \
           "i8E6.rvGN4Hft_0.:pKbB6kfLWend96MvJgWNyNd386xnwV1NDHHMeGnB-rs7xneAL2R"
# 假设你的Redis集群节点在三个主机上的29736, 29737端口上
startup_nodes = [
    ClusterNode(host="192.168.56.121", port="29736"),
    ClusterNode(host="192.168.56.121", port="29737"),
    ClusterNode(host="192.168.56.122", port="29736"),
    ClusterNode(host="192.168.56.122", port="29737"),
    ClusterNode(host="192.168.56.123", port="29736"),
    ClusterNode(host="192.168.56.123", port="29737"),

]

# 连接到Redis集群
rc = RedisCluster(startup_nodes=startup_nodes,
                  decode_responses=True,
                  password=password)

# 使用Redis集群
rc.set("foo", "bar")
print(rc.get("foo"))
print(rc.get("name"))
print(rc.get("num"))

```



执行脚本：

![](/img/Snipaste_2024-07-31_23-29-38.png)

可以看到，能正常读写。

注意，测试redis哨兵模式和集群模式使用的python版本和redis包信息：

```sh
$ python -V
Python 3.8.5
                                                                                         
$ pip list|grep redis
redis              5.0.7
```








参考：

- [Redis集群部署的三种模式](https://cloud.tencent.com/developer/article/2169883)
- [你管这破玩意叫哨兵？](https://mp.weixin.qq.com/s/6qhK1oHXP_VzfgR9BjYVJg)