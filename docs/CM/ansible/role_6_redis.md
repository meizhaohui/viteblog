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

