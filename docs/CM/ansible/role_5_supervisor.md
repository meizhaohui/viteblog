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



### 2.4 任务1-安装mincoda

这个任务，由`roles/supervisor/tasks/miniconda.yaml`定义，查看该文件内容：

```yaml
---
- name: Copy install shell file
  ansible.builtin.copy:
    src: "{{ MINICONDA_SHELL_FILENAME }}"
    dest: "/tmp/{{ MINICONDA_SHELL_FILENAME }}"
    force: yes
    backup: yes
    remote_src: no
    mode: u=rwx,g=r,o=r

- name: Copy the sha256 info file
  ansible.builtin.copy:
    src: sha256info.txt
    dest: /tmp/sha256info.txt
    force: yes
    backup: yes
    remote_src: no

- name: Check the sha256 value of the shell file
  ansible.builtin.command:
    cmd: sha256sum -c sha256info.txt
    chdir: /tmp
  register: result
  failed_when:
    - result.rc != 0

- name: Copy condarc config file
  ansible.builtin.template:
    src: condarc.j2
    dest: "/root/.condarc"
    force: yes
    backup: yes
    remote_src: no

- name: Install miniconda
  ansible.builtin.command:
    # cmd: "/tmp/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh -b -p /srv/miniconda3"
    cmd: "/tmp/{{ MINICONDA_SHELL_FILENAME }} -b -p {{ MINICONDA_BASE_DIR }}"

- name: Remove install shell file
  ansible.builtin.file:
    path: "/tmp/{{ MINICONDA_SHELL_FILENAME }}"
    state: absent

```

可以看到，这个任务中，又分了6个子任务：

- 任务1-`Copy install shell file`，复制从 https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/ 下载的miniconda shell安装文件到远程主机上。手动下载的安装文件保存到` roles/supervisor/files/`目录下。

```sh
[root@ansible ansible_playbooks]# ll roles/supervisor/files/
total 131796
-rw-r--r--. 1 root root        36 Apr 24 22:36 app.ini
-rw-r--r--. 1 root root 134948792 Apr 18 23:00 Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
-rw-r--r--. 1 root root       108 May 22 22:17 sha256info.txt
[root@ansible ansible_playbooks]# cd roles/supervisor/files/
[root@ansible files]# cat sha256info.txt
8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78  Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
[root@ansible files]# sha256sum -c sha256info.txt
Miniconda3-py310_24.1.2-0-Linux-x86_64.sh: OK
[root@ansible files]#
```



- 任务2-`Copy the sha256 info file`，复制散列校验文件`roles/supervisor/files/sha256info.txt`到远程主机上。

这个文件可以通过下面的命令生成：

```sh
[root@ansible files]# sha256sum Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78  Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
[root@ansible files]#
```

通过该命令查出的sha256散列值，刚好可以与miniconda官网上给出的散列值进行对比，散列值相同则说明文件是正常的。

- 任务3-`Check the sha256 value of the shell file`，则会校验复制到远程主机上面的miniconda shell安装文件散列值对不对，不对的话，则会异常，不继续执行后续步骤。
- 任务4-`Copy condarc config file`，复制condarc的配置文件到远程主机，加速miniconda的安装。
- 任务5-`Install miniconda`，执行miniconda安装脚本来安装miniconda，并指定安装目录。
- 任务6-`Remove install shell file`，安装完成后，删除掉复制到远程主机上面miniconda安装脚本，释放磁盘空间。



在`roles/supervisor/tasks/miniconda.yaml`文件中，可以看到使用了一些双大括号包裹的配置，如<code  v-pre>"{{ MINICONDA_SHELL_FILENAME }}"</code>，这个是变量的引用。下面就来说明一下变量。



### 2.5 默认变量

在`roles/supervisor/defaults/main.yml`中定义了一些角色中使用的默认变量：

- 变量名使用大写形式，如`MINICONDA_SHELL_FILENAME`。
- 一行定义一个变量名。

```yaml
---
# 从 https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/ 下载的miniconda shell安装文件的名称
MINICONDA_SHELL_FILENAME: Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
# miniconda虚拟环境目录，Ansible会将miniconda环境安装到该目录下
MINICONDA_BASE_DIR: /srv/miniconda3
# 虚拟环境名称
VIRTUAL_ENV_NAME: supervisorPython3.10.13
# 虚拟环境Python版本
VIRTUAL_PYTHON_VERSION: 3.10.13
# supervisor服务的基础目录，在该目录下创建 logs, socket, pid等目录，变量路径最后不需要带斜杠
SUPERVISOR_BASE_DIR: /srv/supervisor
# supervisor服务的配置文件
SUPERVISORD_CONFIG_FILE: /etc/supervisord.conf
# 虚拟环境supervisor可执行文件路径,如 /srv/miniconda3/envs/supervisorPython3.10.13/bin
SUPERVISORD_DIR_PATH: "{{ MINICONDA_BASE_DIR }}/envs/{{ VIRTUAL_ENV_NAME }}/bin"
# 登陆supervisor web控制台的用户名
SUPERVISOR_USERNAME: admin
# 登陆supervisor web控制台的密码
SUPERVISOR_PASSWORD: admin@123

```

这些变量可以直接在角色中的任务中使用，也可以在`roles/supervisor/templates/`模板文件夹下的模板中使用。

### 2.6 与远程主机相关的变量

可以将远程主机相关的变量，如`IP`信息等，定义在`roles/supervisor/vars/main.yml`变量配置文件中。如我定义了一个`HOST_IP`，来获取远程主机的IP值：

```yaml
---
HOST_IP: "{{ hostvars[inventory_hostname]['inventory_hostname'] }}"

```



### 2.7 内容不动态渲染的文件

在`roles/supervisor/files/`文件夹保存的文件，会原样从Ansible控制主机复制到远程主机上，其中没有使用定义的变量。在任务配置文件中应使用`ansible.builtin.copy`模块，而不是`ansible.builtin.template`模块。

示例：

```sh
# 查看roles/supervisor/files 文件夹有哪些文件
[root@ansible ansible_playbooks]# ll roles/supervisor/files/
total 131796
-rw-r--r--. 1 root root        36 Apr 24 22:36 app.ini
-rw-r--r--. 1 root root 134948792 Apr 18 23:00 Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
-rw-r--r--. 1 root root       108 May 22 22:17 sha256info.txt


# 查看散列校验文件的内容
[root@ansible ansible_playbooks]# cat roles/supervisor/files/sha256info.txt
8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78  Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
[root@ansible ansible_playbooks]#

# 查看用于配置supervisor测试应用的配置文件
[root@ansible ansible_playbooks]# cat roles/supervisor/files/app.ini
[program:testapp]
command=/bin/cat

[root@ansible ansible_playbooks]#
```



### 2.8 内容动态渲染的文件

在`roles/supervisor/templates/`文件夹保存的文件，会将引用变量的位置，用变量的值来进行代替，并渲染成最终的值。在任务配置文件中应使用`ansible.builtin.template`模块，而不是`ansible.builtin.copy`模块，刚好与上一节的内容不动态渲染的文件使用的模块相反。

当然，如果你在`roles/supervisor/templates/`文件夹保存的文件，没使用变量，此时也应使用`ansible.builtin.template`模块来复制文件，不能用`ansible.builtin.copy`模块来复制文件。



示例：

```sh
# condarc.j2中没有使用变量，但在`Copy condarc config file`任务中还是使用的ansible.builtin.template模块
[root@ansible ansible_playbooks]# cat roles/supervisor/templates/condarc.j2
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  deepmodeling: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/

[root@ansible ansible_playbooks]#

# supervisord.service.j2中使用了默认变量SUPERVISORD_DIR_PATH和SUPERVISORD_CONFIG_FILE
[root@ansible ansible_playbooks]# cat roles/supervisor/templates/supervisord.service.j2
# /usr/lib/systemd/system/supervisord.service
[Unit]
Description=Process Monitoring and Control Daemon
After=rc-local.service nss-user-lookup.target

[Service]
Type=forking
# ExecStart=/usr/bin/supervisord -c /etc/supervisord.conf
ExecStart={{ SUPERVISORD_DIR_PATH }}/supervisord -c {{ SUPERVISORD_CONFIG_FILE }}

[Install]
WantedBy=multi-user.target
[root@ansible ansible_playbooks]#
```

