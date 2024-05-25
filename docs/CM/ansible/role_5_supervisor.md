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



### 2.4 任务一-安装mincoda

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

### 2.9 尝试运行第一个任务-安装mincoda

在运行任务前，再次确认一下剧本文件和主机清单配置：

```sh
[root@ansible ansible_playbooks]# cat supervisor.yml
---
- hosts: supervisorhosts
  roles:
    - supervisor

[root@ansible ansible_playbooks]# cat hosts.ini
[supervisorhosts]
192.168.56.121 hostname=ansible-node1
# 192.168.56.122 hostname=ansible-node2
# 192.168.56.123 hostname=ansible-node3

[root@ansible ansible_playbooks]#
```

由于我当前正在测试自己写的角色任务文件，只选择一个工作节点来测试，另外两个工作节点先注释掉，这样可以提升测试效率。



执行命令`ansible-playbook -i hosts.ini supervisor.yml -v`来调用剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini supervisor.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [supervisorhosts] ***********************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]

TASK [supervisor : Copy install shell file] **************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "d80c76dc3fa4af07900daf1dd628863f1f56a67c", "dest": "/tmp/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh", "gid": 0, "group": "root", "mode": "0744", "owner": "root", "path": "/tmp/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh", "size": 134948792, "state": "file", "uid": 0}

TASK [supervisor : Copy the sha256 info file] ************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "1c64874cd584cf30f32d30e34c6cb0b8a46b471e", "dest": "/tmp/sha256info.txt", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/tmp/sha256info.txt", "size": 108, "state": "file", "uid": 0}

TASK [supervisor : Check the sha256 value of the shell file] *********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "cmd": ["sha256sum", "-c", "sha256info.txt"], "delta": "0:00:00.237958", "end": "2024-05-23 23:08:06.611481", "failed_when_result": false, "rc": 0, "start": "2024-05-23 23:08:06.373523", "stderr": "", "stderr_lines": [], "stdout": "Miniconda3-py310_24.1.2-0-Linux-x86_64.sh: OK", "stdout_lines": ["Miniconda3-py310_24.1.2-0-Linux-x86_64.sh: OK"]}

TASK [supervisor : Copy condarc config file] *************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "d6edf310e69bb5ea7d54068817d9b60653e31a1b", "dest": "/root/.condarc", "gid": 0, "group": "root", "mode": "0744", "owner": "root", "path": "/root/.condarc", "size": 777, "state": "file", "uid": 0}

TASK [supervisor : Install miniconda] ********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "cmd": ["/tmp/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh", "-b", "-p", "/srv/miniconda3"], "delta": "0:00:08.590488", "end": "2024-05-23 23:08:15.983518", "rc": 0, "start": "2024-05-23 23:08:07.393030", "stderr": "\r  0%|          | 0/73 [00:00<?, ?it/s]\rExtracting : python-3.10.13-h955ad1f_0.conda:   0%|          | 0/73 [00:01<?, ?it/s]\rExtracting : python-3.10.13-h955ad1f_0.conda:   1%|▏         | 1/73 [00:01<01:35,  1.33s/it]\rExtracting : _libgcc_mutex-0.1-main.conda:   1%|▏         | 1/73 [00:01<01:35,  1.33s/it]   \rExtracting : ca-certificates-2023.12.12-h06a4308_0.conda:   3%|▎         | 2/73 [00:01<01:34,  1.33s/it]\rExtracting : ld_impl_linux-64-2.38-h1181459_1.conda:   4%|▍         | 3/73 [00:01<01:32,  1.33s/it]     \rExtracting : libstdcxx-ng-11.2.0-h1234567_1.conda:   5%|▌         | 4/73 [00:01<01:31,  1.33s/it]  \rExtracting : pybind11-abi-4-hd3eb1b0_1.conda:   7%|▋         | 5/73 [00:01<01:30,  1.33s/it]     \rExtracting : tzdata-2023d-h04d1e81_0.conda:   8%|▊         | 6/73 [00:01<01:28,  1.33s/it]  \rExtracting : libgomp-11.2.0-h1234567_1.conda:  10%|▉         | 7/73 [00:01<01:27,  1.33s/it]\rExtracting : _openmp_mutex-5.1-1_gnu.conda:  11%|█         | 8/73 [00:01<01:26,  1.33s/it]  \rExtracting : libgcc-ng-11.2.0-h1234567_1.conda:  12%|█▏        | 9/73 [00:01<01:24,  1.33s/it]\rExtracting : bzip2-1.0.8-h7b6447c_0.conda:  14%|█▎        | 10/73 [00:01<01:23,  1.33s/it]    \rExtracting : c-ares-1.19.1-h5eee18b_0.conda:  15%|█▌        | 11/73 [00:01<01:22,  1.33s/it]\rExtracting : fmt-9.1.0-hdb19cb5_0.conda:  16%|█▋        | 12/73 [00:01<01:20,  1.33s/it]    \rExtracting : icu-73.1-h6a678d5_0.conda:  18%|█▊        | 13/73 [00:01<01:19,  1.33s/it] \rExtracting : libev-4.33-h7f8727e_1.conda:  19%|█▉        | 14/73 [00:01<01:18,  1.33s/it]\rExtracting : libffi-3.4.4-h6a678d5_0.conda:  21%|██        | 15/73 [00:01<01:16,  1.33s/it]\rExtracting : libuuid-1.41.5-h5eee18b_0.conda:  22%|██▏       | 16/73 [00:01<01:15,  1.33s/it]\rExtracting : lz4-c-1.9.4-h6a678d5_0.conda:  23%|██▎       | 17/73 [00:01<01:14,  1.33s/it]   \rExtracting : ncurses-6.4-h6a678d5_0.conda:  25%|██▍       | 18/73 [00:01<01:12,  1.33s/it]\rExtracting : ncurses-6.4-h6a678d5_0.conda:  26%|██▌       | 19/73 [00:01<00:04, 13.10it/s]\rExtracting : openssl-3.0.13-h7f8727e_0.conda:  26%|██▌       | 19/73 [00:01<00:04, 13.10it/s]\rExtracting : reproc-14.2.4-h295c915_1.conda:  27%|██▋       | 20/73 [00:01<00:04, 13.10it/s] \rExtracting : xz-5.4.5-h5eee18b_0.conda:  29%|██▉       | 21/73 [00:01<00:03, 13.10it/s]     \rExtracting : yaml-cpp-0.8.0-h6a678d5_0.conda:  30%|███       | 22/73 [00:01<00:03, 13.10it/s]\rExtracting : zlib-1.2.13-h5eee18b_0.conda:  32%|███▏      | 23/73 [00:01<00:03, 13.10it/s]   \rExtracting : libedit-3.1.20230828-h5eee18b_0.conda:  33%|███▎      | 24/73 [00:01<00:03, 13.10it/s]\rExtracting : libnghttp2-1.57.0-h2d74bed_0.conda:  34%|███▍      | 25/73 [00:01<00:03, 13.10it/s]   \rExtracting : libssh2-1.10.0-hdbd6064_2.conda:  36%|███▌      | 26/73 [00:01<00:03, 13.10it/s]   \rExtracting : libxml2-2.10.4-hf1b16e4_1.conda:  37%|███▋      | 27/73 [00:01<00:03, 13.10it/s]\rExtracting : pcre2-10.42-hebb0a14_0.conda:  38%|███▊      | 28/73 [00:01<00:03, 13.10it/s]   \rExtracting : readline-8.2-h5eee18b_0.conda:  40%|███▉      | 29/73 [00:01<00:03, 13.10it/s]\rExtracting : reproc-cpp-14.2.4-h295c915_1.conda:  41%|████      | 30/73 [00:01<00:03, 13.10it/s]\rExtracting : tk-8.6.12-h1ccaba5_0.conda:  42%|████▏     | 31/73 [00:02<00:03, 13.10it/s]        \rExtracting : tk-8.6.12-h1ccaba5_0.conda:  44%|████▍     | 32/73 [00:02<00:01, 21.24it/s]\rExtracting : zstd-1.5.5-hc292b87_0.conda:  44%|████▍     | 32/73 [00:02<00:01, 21.24it/s]\rExtracting : krb5-1.20.1-h143b758_1.conda:  45%|████▌     | 33/73 [00:02<00:01, 21.24it/s]\rExtracting : libarchive-3.6.2-h6ac8c49_2.conda:  47%|████▋     | 34/73 [00:02<00:01, 21.24it/s]\rExtracting : libsolv-0.7.24-he621ea3_0.conda:  48%|████▊     | 35/73 [00:02<00:01, 21.24it/s]  \rExtracting : sqlite-3.41.2-h5eee18b_0.conda:  49%|████▉     | 36/73 [00:02<00:01, 21.24it/s] \rExtracting : libcurl-8.5.0-h251f7ec_0.conda:  51%|█████     | 37/73 [00:02<00:01, 21.24it/s]\rExtracting : libmamba-1.5.6-haf1ee3a_0.conda:  52%|█████▏    | 38/73 [00:02<00:01, 21.24it/s]\rExtracting : menuinst-2.0.2-py310h06a4308_0.conda:  53%|█████▎    | 39/73 [00:02<00:01, 21.24it/s]\rExtracting : archspec-0.2.1-pyhd3eb1b0_0.conda:  55%|█████▍    | 40/73 [00:02<00:01, 21.24it/s]   \rExtracting : boltons-23.0.0-py310h06a4308_0.conda:  56%|█████▌    | 41/73 [00:02<00:01, 21.24it/s]\rExtracting : boltons-23.0.0-py310h06a4308_0.conda:  58%|█████▊    | 42/73 [00:02<00:01, 28.28it/s]\rExtracting : brotli-python-1.0.9-py310h6a678d5_7.conda:  58%|█████▊    | 42/73 [00:02<00:01, 28.28it/s]\rExtracting : certifi-2024.2.2-py310h06a4308_0.conda:  59%|█████▉    | 43/73 [00:02<00:01, 28.28it/s]   \rExtracting : charset-normalizer-2.0.4-pyhd3eb1b0_0.conda:  60%|██████    | 44/73 [00:02<00:01, 28.28it/s]\rExtracting : distro-1.8.0-py310h06a4308_0.conda:  62%|██████▏   | 45/73 [00:02<00:00, 28.28it/s]         \rExtracting : idna-3.4-py310h06a4308_0.conda:  63%|██████▎   | 46/73 [00:02<00:00, 28.28it/s]    \rExtracting : jsonpointer-2.1-pyhd3eb1b0_0.conda:  64%|██████▍   | 47/73 [00:02<00:00, 28.28it/s]\rExtracting : libmambapy-1.5.6-py310h2dafd23_0.conda:  66%|██████▌   | 48/73 [00:02<00:00, 28.28it/s]\rExtracting : packaging-23.1-py310h06a4308_0.conda:  67%|██████▋   | 49/73 [00:02<00:00, 28.28it/s]  \rExtracting : platformdirs-3.10.0-py310h06a4308_0.conda:  68%|██████▊   | 50/73 [00:02<00:00, 28.28it/s]\rExtracting : pluggy-1.0.0-py310h06a4308_1.conda:  70%|██████▉   | 51/73 [00:02<00:00, 28.28it/s]       \rExtracting : pycosat-0.6.6-py310h5eee18b_0.conda:  71%|███████   | 52/73 [00:02<00:00, 28.28it/s]\rExtracting : pycparser-2.21-pyhd3eb1b0_0.conda:  73%|███████▎  | 53/73 [00:02<00:00, 28.28it/s]  \rExtracting : pysocks-1.7.1-py310h06a4308_0.conda:  74%|███████▍  | 54/73 [00:02<00:00, 28.28it/s]\rExtracting : ruamel.yaml.clib-0.2.6-py310h5eee18b_1.conda:  75%|███████▌  | 55/73 [00:02<00:00, 28.28it/s]\rExtracting : setuptools-68.2.2-py310h06a4308_0.conda:  77%|███████▋  | 56/73 [00:02<00:00, 28.28it/s]     \rExtracting : setuptools-68.2.2-py310h06a4308_0.conda:  78%|███████▊  | 57/73 [00:02<00:00, 37.97it/s]\rExtracting : tqdm-4.65.0-py310h2f386ee_0.conda:  78%|███████▊  | 57/73 [00:02<00:00, 37.97it/s]      \rExtracting : truststore-0.8.0-py310h06a4308_0.conda:  79%|███████▉  | 58/73 [00:02<00:00, 37.97it/s]\rExtracting : wheel-0.41.2-py310h06a4308_0.conda:  81%|████████  | 59/73 [00:02<00:00, 37.97it/s]    \rExtracting : cffi-1.16.0-py310h5eee18b_0.conda:  82%|████████▏ | 60/73 [00:02<00:00, 37.97it/s] \rExtracting : jsonpatch-1.32-pyhd3eb1b0_0.conda:  84%|████████▎ | 61/73 [00:02<00:00, 37.97it/s]\rExtracting : pip-23.3.1-py310h06a4308_0.conda:  85%|████████▍ | 62/73 [00:02<00:00, 37.97it/s] \rExtracting : pip-23.3.1-py310h06a4308_0.conda:  86%|████████▋ | 63/73 [00:02<00:00, 29.97it/s]\rExtracting : ruamel.yaml-0.17.21-py310h5eee18b_0.conda:  86%|████████▋ | 63/73 [00:02<00:00, 29.97it/s]\rExtracting : urllib3-2.1.0-py310h06a4308_1.conda:  88%|████████▊ | 64/73 [00:02<00:00, 29.97it/s]      \rExtracting : cryptography-42.0.2-py310hdda0065_0.conda:  89%|████████▉ | 65/73 [00:02<00:00, 29.97it/s]\rExtracting : requests-2.31.0-py310h06a4308_1.conda:  90%|█████████ | 66/73 [00:02<00:00, 29.97it/s]    \rExtracting : zstandard-0.19.0-py310h5eee18b_0.conda:  92%|█████████▏| 67/73 [00:02<00:00, 29.97it/s]\rExtracting : conda-content-trust-0.2.0-py310h06a4308_0.conda:  93%|█████████▎| 68/73 [00:02<00:00, 29.97it/s]\rExtracting : conda-package-streaming-0.9.0-py310h06a4308_0.conda:  95%|█████████▍| 69/73 [00:02<00:00, 29.97it/s]\rExtracting : conda-package-handling-2.2.0-py310h06a4308_0.conda:  96%|█████████▌| 70/73 [00:02<00:00, 29.97it/s] \rExtracting : conda-24.1.2-py310h06a4308_0.conda:  97%|█████████▋| 71/73 [00:02<00:00, 29.97it/s]                \rExtracting : conda-24.1.2-py310h06a4308_0.conda:  99%|█████████▊| 72/73 [00:02<00:00, 35.67it/s]\rExtracting : conda-libmamba-solver-24.1.0-pyhd3eb1b0_0.conda:  99%|█████████▊| 72/73 [00:02<00:00, 35.67it/s]\r                                                                                                             ", "stderr_lines": ["", "  0%|          | 0/73 [00:00<?, ?it/s]", "Extracting : python-3.10.13-h955ad1f_0.conda:   0%|          | 0/73 [00:01<?, ?it/s]", "Extracting : python-3.10.13-h955ad1f_0.conda:   1%|▏         | 1/73 [00:01<01:35,  1.33s/it]", "Extracting : _libgcc_mutex-0.1-main.conda:   1%|▏         | 1/73 [00:01<01:35,  1.33s/it]   ", "Extracting : ca-certificates-2023.12.12-h06a4308_0.conda:   3%|▎         | 2/73 [00:01<01:34,  1.33s/it]", "Extracting : ld_impl_linux-64-2.38-h1181459_1.conda:   4%|▍         | 3/73 [00:01<01:32,  1.33s/it]     ", "Extracting : libstdcxx-ng-11.2.0-h1234567_1.conda:   5%|▌         | 4/73 [00:01<01:31,  1.33s/it]  ", "Extracting : pybind11-abi-4-hd3eb1b0_1.conda:   7%|▋         | 5/73 [00:01<01:30,  1.33s/it]     ", "Extracting : tzdata-2023d-h04d1e81_0.conda:   8%|▊         | 6/73 [00:01<01:28,  1.33s/it]  ", "Extracting : libgomp-11.2.0-h1234567_1.conda:  10%|▉         | 7/73 [00:01<01:27,  1.33s/it]", "Extracting : _openmp_mutex-5.1-1_gnu.conda:  11%|█         | 8/73 [00:01<01:26,  1.33s/it]  ", "Extracting : libgcc-ng-11.2.0-h1234567_1.conda:  12%|█▏        | 9/73 [00:01<01:24,  1.33s/it]", "Extracting : bzip2-1.0.8-h7b6447c_0.conda:  14%|█▎        | 10/73 [00:01<01:23,  1.33s/it]    ", "Extracting : c-ares-1.19.1-h5eee18b_0.conda:  15%|█▌        | 11/73 [00:01<01:22,  1.33s/it]", "Extracting : fmt-9.1.0-hdb19cb5_0.conda:  16%|█▋        | 12/73 [00:01<01:20,  1.33s/it]    ", "Extracting : icu-73.1-h6a678d5_0.conda:  18%|█▊        | 13/73 [00:01<01:19,  1.33s/it] ", "Extracting : libev-4.33-h7f8727e_1.conda:  19%|█▉        | 14/73 [00:01<01:18,  1.33s/it]", "Extracting : libffi-3.4.4-h6a678d5_0.conda:  21%|██        | 15/73 [00:01<01:16,  1.33s/it]", "Extracting : libuuid-1.41.5-h5eee18b_0.conda:  22%|██▏       | 16/73 [00:01<01:15,  1.33s/it]", "Extracting : lz4-c-1.9.4-h6a678d5_0.conda:  23%|██▎       | 17/73 [00:01<01:14,  1.33s/it]   ", "Extracting : ncurses-6.4-h6a678d5_0.conda:  25%|██▍       | 18/73 [00:01<01:12,  1.33s/it]", "Extracting : ncurses-6.4-h6a678d5_0.conda:  26%|██▌       | 19/73 [00:01<00:04, 13.10it/s]", "Extracting : openssl-3.0.13-h7f8727e_0.conda:  26%|██▌       | 19/73 [00:01<00:04, 13.10it/s]", "Extracting : reproc-14.2.4-h295c915_1.conda:  27%|██▋       | 20/73 [00:01<00:04, 13.10it/s] ", "Extracting : xz-5.4.5-h5eee18b_0.conda:  29%|██▉       | 21/73 [00:01<00:03, 13.10it/s]     ", "Extracting : yaml-cpp-0.8.0-h6a678d5_0.conda:  30%|███       | 22/73 [00:01<00:03, 13.10it/s]", "Extracting : zlib-1.2.13-h5eee18b_0.conda:  32%|███▏      | 23/73 [00:01<00:03, 13.10it/s]   ", "Extracting : libedit-3.1.20230828-h5eee18b_0.conda:  33%|███▎      | 24/73 [00:01<00:03, 13.10it/s]", "Extracting : libnghttp2-1.57.0-h2d74bed_0.conda:  34%|███▍      | 25/73 [00:01<00:03, 13.10it/s]   ", "Extracting : libssh2-1.10.0-hdbd6064_2.conda:  36%|███▌      | 26/73 [00:01<00:03, 13.10it/s]   ", "Extracting : libxml2-2.10.4-hf1b16e4_1.conda:  37%|███▋      | 27/73 [00:01<00:03, 13.10it/s]", "Extracting : pcre2-10.42-hebb0a14_0.conda:  38%|███▊      | 28/73 [00:01<00:03, 13.10it/s]   ", "Extracting : readline-8.2-h5eee18b_0.conda:  40%|███▉      | 29/73 [00:01<00:03, 13.10it/s]", "Extracting : reproc-cpp-14.2.4-h295c915_1.conda:  41%|████      | 30/73 [00:01<00:03, 13.10it/s]", "Extracting : tk-8.6.12-h1ccaba5_0.conda:  42%|████▏     | 31/73 [00:02<00:03, 13.10it/s]        ", "Extracting : tk-8.6.12-h1ccaba5_0.conda:  44%|████▍     | 32/73 [00:02<00:01, 21.24it/s]", "Extracting : zstd-1.5.5-hc292b87_0.conda:  44%|████▍     | 32/73 [00:02<00:01, 21.24it/s]", "Extracting : krb5-1.20.1-h143b758_1.conda:  45%|████▌     | 33/73 [00:02<00:01, 21.24it/s]", "Extracting : libarchive-3.6.2-h6ac8c49_2.conda:  47%|████▋     | 34/73 [00:02<00:01, 21.24it/s]", "Extracting : libsolv-0.7.24-he621ea3_0.conda:  48%|████▊     | 35/73 [00:02<00:01, 21.24it/s]  ", "Extracting : sqlite-3.41.2-h5eee18b_0.conda:  49%|████▉     | 36/73 [00:02<00:01, 21.24it/s] ", "Extracting : libcurl-8.5.0-h251f7ec_0.conda:  51%|█████     | 37/73 [00:02<00:01, 21.24it/s]", "Extracting : libmamba-1.5.6-haf1ee3a_0.conda:  52%|█████▏    | 38/73 [00:02<00:01, 21.24it/s]", "Extracting : menuinst-2.0.2-py310h06a4308_0.conda:  53%|█████▎    | 39/73 [00:02<00:01, 21.24it/s]", "Extracting : archspec-0.2.1-pyhd3eb1b0_0.conda:  55%|█████▍    | 40/73 [00:02<00:01, 21.24it/s]   ", "Extracting : boltons-23.0.0-py310h06a4308_0.conda:  56%|█████▌    | 41/73 [00:02<00:01, 21.24it/s]", "Extracting : boltons-23.0.0-py310h06a4308_0.conda:  58%|█████▊    | 42/73 [00:02<00:01, 28.28it/s]", "Extracting : brotli-python-1.0.9-py310h6a678d5_7.conda:  58%|█████▊    | 42/73 [00:02<00:01, 28.28it/s]", "Extracting : certifi-2024.2.2-py310h06a4308_0.conda:  59%|█████▉    | 43/73 [00:02<00:01, 28.28it/s]   ", "Extracting : charset-normalizer-2.0.4-pyhd3eb1b0_0.conda:  60%|██████    | 44/73 [00:02<00:01, 28.28it/s]", "Extracting : distro-1.8.0-py310h06a4308_0.conda:  62%|██████▏   | 45/73 [00:02<00:00, 28.28it/s]         ", "Extracting : idna-3.4-py310h06a4308_0.conda:  63%|██████▎   | 46/73 [00:02<00:00, 28.28it/s]    ", "Extracting : jsonpointer-2.1-pyhd3eb1b0_0.conda:  64%|██████▍   | 47/73 [00:02<00:00, 28.28it/s]", "Extracting : libmambapy-1.5.6-py310h2dafd23_0.conda:  66%|██████▌   | 48/73 [00:02<00:00, 28.28it/s]", "Extracting : packaging-23.1-py310h06a4308_0.conda:  67%|██████▋   | 49/73 [00:02<00:00, 28.28it/s]  ", "Extracting : platformdirs-3.10.0-py310h06a4308_0.conda:  68%|██████▊   | 50/73 [00:02<00:00, 28.28it/s]", "Extracting : pluggy-1.0.0-py310h06a4308_1.conda:  70%|██████▉   | 51/73 [00:02<00:00, 28.28it/s]       ", "Extracting : pycosat-0.6.6-py310h5eee18b_0.conda:  71%|███████   | 52/73 [00:02<00:00, 28.28it/s]", "Extracting : pycparser-2.21-pyhd3eb1b0_0.conda:  73%|███████▎  | 53/73 [00:02<00:00, 28.28it/s]  ", "Extracting : pysocks-1.7.1-py310h06a4308_0.conda:  74%|███████▍  | 54/73 [00:02<00:00, 28.28it/s]", "Extracting : ruamel.yaml.clib-0.2.6-py310h5eee18b_1.conda:  75%|███████▌  | 55/73 [00:02<00:00, 28.28it/s]", "Extracting : setuptools-68.2.2-py310h06a4308_0.conda:  77%|███████▋  | 56/73 [00:02<00:00, 28.28it/s]     ", "Extracting : setuptools-68.2.2-py310h06a4308_0.conda:  78%|███████▊  | 57/73 [00:02<00:00, 37.97it/s]", "Extracting : tqdm-4.65.0-py310h2f386ee_0.conda:  78%|███████▊  | 57/73 [00:02<00:00, 37.97it/s]      ", "Extracting : truststore-0.8.0-py310h06a4308_0.conda:  79%|███████▉  | 58/73 [00:02<00:00, 37.97it/s]", "Extracting : wheel-0.41.2-py310h06a4308_0.conda:  81%|████████  | 59/73 [00:02<00:00, 37.97it/s]    ", "Extracting : cffi-1.16.0-py310h5eee18b_0.conda:  82%|████████▏ | 60/73 [00:02<00:00, 37.97it/s] ", "Extracting : jsonpatch-1.32-pyhd3eb1b0_0.conda:  84%|████████▎ | 61/73 [00:02<00:00, 37.97it/s]", "Extracting : pip-23.3.1-py310h06a4308_0.conda:  85%|████████▍ | 62/73 [00:02<00:00, 37.97it/s] ", "Extracting : pip-23.3.1-py310h06a4308_0.conda:  86%|████████▋ | 63/73 [00:02<00:00, 29.97it/s]", "Extracting : ruamel.yaml-0.17.21-py310h5eee18b_0.conda:  86%|████████▋ | 63/73 [00:02<00:00, 29.97it/s]", "Extracting : urllib3-2.1.0-py310h06a4308_1.conda:  88%|████████▊ | 64/73 [00:02<00:00, 29.97it/s]      ", "Extracting : cryptography-42.0.2-py310hdda0065_0.conda:  89%|████████▉ | 65/73 [00:02<00:00, 29.97it/s]", "Extracting : requests-2.31.0-py310h06a4308_1.conda:  90%|█████████ | 66/73 [00:02<00:00, 29.97it/s]    ", "Extracting : zstandard-0.19.0-py310h5eee18b_0.conda:  92%|█████████▏| 67/73 [00:02<00:00, 29.97it/s]", "Extracting : conda-content-trust-0.2.0-py310h06a4308_0.conda:  93%|█████████▎| 68/73 [00:02<00:00, 29.97it/s]", "Extracting : conda-package-streaming-0.9.0-py310h06a4308_0.conda:  95%|█████████▍| 69/73 [00:02<00:00, 29.97it/s]", "Extracting : conda-package-handling-2.2.0-py310h06a4308_0.conda:  96%|█████████▌| 70/73 [00:02<00:00, 29.97it/s] ", "Extracting : conda-24.1.2-py310h06a4308_0.conda:  97%|█████████▋| 71/73 [00:02<00:00, 29.97it/s]                ", "Extracting : conda-24.1.2-py310h06a4308_0.conda:  99%|█████████▊| 72/73 [00:02<00:00, 35.67it/s]", "Extracting : conda-libmamba-solver-24.1.0-pyhd3eb1b0_0.conda:  99%|█████████▊| 72/73 [00:02<00:00, 35.67it/s]", "                                                                                                             "], "stdout": "PREFIX=/srv/miniconda3\nUnpacking payload ...\n\nInstalling base environment...\n\n\nDownloading and Extracting Packages: ...working... done\n\nDownloading and Extracting Packages: ...working... done\nPreparing transaction: ...working... done\nExecuting transaction: ...working... done\ninstallation finished.", "stdout_lines": ["PREFIX=/srv/miniconda3", "Unpacking payload ...", "", "Installing base environment...", "", "", "Downloading and Extracting Packages: ...working... done", "", "Downloading and Extracting Packages: ...working... done", "Preparing transaction: ...working... done", "Executing transaction: ...working... done", "installation finished."]}

TASK [supervisor : Remove install shell file] ************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "path": "/tmp/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh", "state": "absent"}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=7    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 13 seconds
[root@ansible ansible_playbooks]#
```

执行过程截图：

![](/img/Snipaste_2024-05-23_23-14-38.png)

![](/img/Snipaste_2024-05-23_23-15-37.png)

此时，可以在工作节点1上面检查一下：

```sh
[root@ansible-node1 ~]# ll /tmp/sha256info.txt
-rw-r--r-- 1 root root 108 May 22 22:17 /tmp/sha256info.txt
[root@ansible-node1 ~]# cat /tmp/sha256info.txt
8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78  Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
[root@ansible-node1 ~]# ll /root/.condarc
-rwxr--r-- 1 root root 777 Apr 18 23:10 /root/.condarc
[root@ansible-node1 ~]# cat /root/.condarc
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
[root@ansible-node1 ~]# ll /srv/miniconda3
total 32216
drwxr-xr-x  2 root root     4096 May 23 23:08 bin
drwxr-xr-x  2 root root       66 May 23 23:08 cmake
drwxr-xr-x  2 root root       30 May 23 23:08 compiler_compat
-rwxr-xr-x  1 root root 32840488 May 23 23:08 _conda
drwxr-xr-x  2 root root       19 May 23 23:08 condabin
drwxr-xr-x  2 root root     4096 May 23 23:08 conda-meta
drwxr-xr-x  2 root root        6 May 23 23:08 envs
drwxr-xr-x  4 root root       35 May 23 23:08 etc
drwxr-xr-x 26 root root     8192 May 23 23:08 include
drwxr-xr-x 19 root root     8192 May 23 23:08 lib
-rw-r--r--  1 root root    91585 Feb 24 02:39 LICENSE.txt
drwxr-xr-x  4 root root       30 May 23 23:08 man
drwxr-xr-x 76 root root     8192 May 23 23:08 pkgs
drwxr-xr-x  2 root root      203 May 23 23:08 sbin
drwxr-xr-x 15 root root      181 May 23 23:08 share
drwxr-xr-x  3 root root       22 May 23 23:08 shell
drwxr-xr-x  3 root root      146 May 23 23:08 ssl
drwxr-xr-x  3 root root       17 May 23 23:08 x86_64-conda_cos7-linux-gnu
drwxr-xr-x  3 root root       17 May 23 23:08 x86_64-conda-linux-gnu
[root@ansible-node1 ~]# cd /srv/miniconda3/bin/
[root@ansible-node1 bin]# ./conda -V
conda 24.1.2
[root@ansible-node1 bin]# ./conda env list
# conda environments:
#
base                     /srv/miniconda3
[root@ansible-node1 bin]#
```

可以看到，预期的文件已经有了，miniconda也安装到MINICONDA_BASE_DIR变量指定的目录`/srv/miniconda3`里面了，并且能够执行`conda`相关的命令。

此时，只有一个`base`环境。

可以看到，miniconda成功安装，并正常可用了，说明第一个任务配置是对的。



### 2.10 任务二-创建虚拟环境

任务二创建虚拟环境，使用的是`virtual_env.yaml`子任务，由`roles/supervisor/tasks/virtual_env.yaml`定义，查看该文件内容：

```yaml
---
- name: Create supervisor virtual environment
  ansible.builtin.command:
    # cmd: "/srv/miniconda3/bin/conda create --yes --name supervisorPython3.10.13 python=3.10.13"
    cmd: "{{ MINICONDA_BASE_DIR }}/bin/conda create --yes --name {{ VIRTUAL_ENV_NAME }} python={{ VIRTUAL_PYTHON_VERSION }}"

- name: Show virtual environments
  ansible.builtin.command:
    # cmd: "/srv/miniconda3/bin/conda env list"
    cmd: "{{ MINICONDA_BASE_DIR }}/bin/conda env list"
  changed_when: False

- name: Show virtual Python version
  ansible.builtin.command:
    # cmd: "/srv/miniconda/envs/supervisorPython3.10.13/bin/python -V"
    cmd: "{{ MINICONDA_BASE_DIR }}/envs/{{ VIRTUAL_ENV_NAME }}/bin/python -V"
  changed_when: False

```

实际上，就只用执行类似`/srv/miniconda3/bin/conda create --yes --name supervisorPython3.10.13 python=3.10.13`这样的命令，来创建一个名为`supervisorPython3.10.13`的虚拟环境，而虚拟环境的名称和Python的版本，则是由默认变量`VIRTUAL_ENV_NAME`和`VIRTUAL_PYTHON_VERSION`来定义的，2.5节中已经说明。

由于任务一已经测试完成，我们此时只想测试第二个任务，因此可以调整`roles/supervisor/tasks/main.yml`配置内容中的`include`情况，修改成这样的：

```yaml
---
# supervisor角色任务
# 安装mincoda
# - include: miniconda.yaml
# 创建虚拟环境
- include: virtual_env.yaml
# 配置supervisor进程管理工具
#- include: supervisor.yaml
# 创建快捷命令
#- include: alias.yaml
```

此时，执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini supervisor.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [supervisorhosts] ***********************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]

TASK [Create supervisor virtual environment] *************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "cmd": ["/srv/miniconda3/bin/conda", "create", "--yes", "--name", "supervisorPython3.10.13", "python=3.10.13"], "delta": "0:00:13.757764", "end": "2024-05-23 23:44:25.118665", "rc": 0, "start": "2024-05-23 23:44:11.360901", "stderr": "", "stderr_lines": [], "stdout": "Retrieving notices: ...working... done\nChannels:\n - defaults\nPlatform: linux-64\nCollecting package metadata (repodata.json): ...working... done\nSolving environment: ...working... done\n\n## Package Plan ##\n\n  environment location: /srv/miniconda3/envs/supervisorPython3.10.13\n\n  added / updated specs:\n    - python=3.10.13\n\n\nThe following packages will be downloaded:\n\n    package                    |            build\n    ---------------------------|-----------------\n    _libgcc_mutex-0.1          |             main           3 KB  defaults\n    _openmp_mutex-5.1          |            1_gnu          21 KB  defaults\n    bzip2-1.0.8                |       h5eee18b_6         262 KB  defaults\n    ca-certificates-2024.3.11  |       h06a4308_0         127 KB  defaults\n    ld_impl_linux-64-2.38      |       h1181459_1         654 KB  defaults\n    libffi-3.4.4               |       h6a678d5_1         141 KB  defaults\n    libgcc-ng-11.2.0           |       h1234567_1         5.3 MB  defaults\n    libgomp-11.2.0             |       h1234567_1         474 KB  defaults\n    libstdcxx-ng-11.2.0        |       h1234567_1         4.7 MB  defaults\n    libuuid-1.41.5             |       h5eee18b_0          27 KB  defaults\n    ncurses-6.4                |       h6a678d5_0         914 KB  defaults\n    openssl-3.0.13             |       h7f8727e_2         5.2 MB  defaults\n    pip-24.0                   |  py310h06a4308_0         2.7 MB  defaults\n    python-3.10.13             |       h955ad1f_0        26.8 MB  defaults\n    readline-8.2               |       h5eee18b_0         357 KB  defaults\n    setuptools-69.5.1          |  py310h06a4308_0        1012 KB  defaults\n    sqlite-3.45.3              |       h5eee18b_0         1.2 MB  defaults\n    tk-8.6.14                  |       h39e8969_0         3.4 MB  defaults\n    tzdata-2024a               |       h04d1e81_0         116 KB  defaults\n    wheel-0.43.0               |  py310h06a4308_0         110 KB  defaults\n    xz-5.4.6                   |       h5eee18b_1         643 KB  defaults\n    zlib-1.2.13                |       h5eee18b_1         111 KB  defaults\n    ------------------------------------------------------------\n                                           Total:        54.2 MB\n\nThe following NEW packages will be INSTALLED:\n\n  _libgcc_mutex      anaconda/pkgs/main/linux-64::_libgcc_mutex-0.1-main \n  _openmp_mutex      anaconda/pkgs/main/linux-64::_openmp_mutex-5.1-1_gnu \n  bzip2              anaconda/pkgs/main/linux-64::bzip2-1.0.8-h5eee18b_6 \n  ca-certificates    anaconda/pkgs/main/linux-64::ca-certificates-2024.3.11-h06a4308_0 \n  ld_impl_linux-64   anaconda/pkgs/main/linux-64::ld_impl_linux-64-2.38-h1181459_1 \n  libffi             anaconda/pkgs/main/linux-64::libffi-3.4.4-h6a678d5_1 \n  libgcc-ng          anaconda/pkgs/main/linux-64::libgcc-ng-11.2.0-h1234567_1 \n  libgomp            anaconda/pkgs/main/linux-64::libgomp-11.2.0-h1234567_1 \n  libstdcxx-ng       anaconda/pkgs/main/linux-64::libstdcxx-ng-11.2.0-h1234567_1 \n  libuuid            anaconda/pkgs/main/linux-64::libuuid-1.41.5-h5eee18b_0 \n  ncurses            anaconda/pkgs/main/linux-64::ncurses-6.4-h6a678d5_0 \n  openssl            anaconda/pkgs/main/linux-64::openssl-3.0.13-h7f8727e_2 \n  pip                anaconda/pkgs/main/linux-64::pip-24.0-py310h06a4308_0 \n  python             anaconda/pkgs/main/linux-64::python-3.10.13-h955ad1f_0 \n  readline           anaconda/pkgs/main/linux-64::readline-8.2-h5eee18b_0 \n  setuptools         anaconda/pkgs/main/linux-64::setuptools-69.5.1-py310h06a4308_0 \n  sqlite             anaconda/pkgs/main/linux-64::sqlite-3.45.3-h5eee18b_0 \n  tk                 anaconda/pkgs/main/linux-64::tk-8.6.14-h39e8969_0 \n  tzdata             anaconda/pkgs/main/noarch::tzdata-2024a-h04d1e81_0 \n  wheel              anaconda/pkgs/main/linux-64::wheel-0.43.0-py310h06a4308_0 \n  xz                 anaconda/pkgs/main/linux-64::xz-5.4.6-h5eee18b_1 \n  zlib               anaconda/pkgs/main/linux-64::zlib-1.2.13-h5eee18b_1 \n\n\n\nDownloading and Extracting Packages: ...working... done\nPreparing transaction: ...working... done\nVerifying transaction: ...working... done\nExecuting transaction: ...working... done\n#\n# To activate this environment, use\n#\n#     $ conda activate supervisorPython3.10.13\n#\n# To deactivate an active environment, use\n#\n#     $ conda deactivate", "stdout_lines": ["Retrieving notices: ...working... done", "Channels:", " - defaults", "Platform: linux-64", "Collecting package metadata (repodata.json): ...working... done", "Solving environment: ...working... done", "", "## Package Plan ##", "", "  environment location: /srv/miniconda3/envs/supervisorPython3.10.13", "", "  added / updated specs:", "    - python=3.10.13", "", "", "The following packages will be downloaded:", "", "    package                    |            build", "    ---------------------------|-----------------", "    _libgcc_mutex-0.1          |             main           3 KB  defaults", "    _openmp_mutex-5.1          |            1_gnu          21 KB  defaults", "    bzip2-1.0.8                |       h5eee18b_6         262 KB  defaults", "    ca-certificates-2024.3.11  |       h06a4308_0         127 KB  defaults", "    ld_impl_linux-64-2.38      |       h1181459_1         654 KB  defaults", "    libffi-3.4.4               |       h6a678d5_1         141 KB  defaults", "    libgcc-ng-11.2.0           |       h1234567_1         5.3 MB  defaults", "    libgomp-11.2.0             |       h1234567_1         474 KB  defaults", "    libstdcxx-ng-11.2.0        |       h1234567_1         4.7 MB  defaults", "    libuuid-1.41.5             |       h5eee18b_0          27 KB  defaults", "    ncurses-6.4                |       h6a678d5_0         914 KB  defaults", "    openssl-3.0.13             |       h7f8727e_2         5.2 MB  defaults", "    pip-24.0                   |  py310h06a4308_0         2.7 MB  defaults", "    python-3.10.13             |       h955ad1f_0        26.8 MB  defaults", "    readline-8.2               |       h5eee18b_0         357 KB  defaults", "    setuptools-69.5.1          |  py310h06a4308_0        1012 KB  defaults", "    sqlite-3.45.3              |       h5eee18b_0         1.2 MB  defaults", "    tk-8.6.14                  |       h39e8969_0         3.4 MB  defaults", "    tzdata-2024a               |       h04d1e81_0         116 KB  defaults", "    wheel-0.43.0               |  py310h06a4308_0         110 KB  defaults", "    xz-5.4.6                   |       h5eee18b_1         643 KB  defaults", "    zlib-1.2.13                |       h5eee18b_1         111 KB  defaults", "    ------------------------------------------------------------", "                                           Total:        54.2 MB", "", "The following NEW packages will be INSTALLED:", "", "  _libgcc_mutex      anaconda/pkgs/main/linux-64::_libgcc_mutex-0.1-main ", "  _openmp_mutex      anaconda/pkgs/main/linux-64::_openmp_mutex-5.1-1_gnu ", "  bzip2              anaconda/pkgs/main/linux-64::bzip2-1.0.8-h5eee18b_6 ", "  ca-certificates    anaconda/pkgs/main/linux-64::ca-certificates-2024.3.11-h06a4308_0 ", "  ld_impl_linux-64   anaconda/pkgs/main/linux-64::ld_impl_linux-64-2.38-h1181459_1 ", "  libffi             anaconda/pkgs/main/linux-64::libffi-3.4.4-h6a678d5_1 ", "  libgcc-ng          anaconda/pkgs/main/linux-64::libgcc-ng-11.2.0-h1234567_1 ", "  libgomp            anaconda/pkgs/main/linux-64::libgomp-11.2.0-h1234567_1 ", "  libstdcxx-ng       anaconda/pkgs/main/linux-64::libstdcxx-ng-11.2.0-h1234567_1 ", "  libuuid            anaconda/pkgs/main/linux-64::libuuid-1.41.5-h5eee18b_0 ", "  ncurses            anaconda/pkgs/main/linux-64::ncurses-6.4-h6a678d5_0 ", "  openssl            anaconda/pkgs/main/linux-64::openssl-3.0.13-h7f8727e_2 ", "  pip                anaconda/pkgs/main/linux-64::pip-24.0-py310h06a4308_0 ", "  python             anaconda/pkgs/main/linux-64::python-3.10.13-h955ad1f_0 ", "  readline           anaconda/pkgs/main/linux-64::readline-8.2-h5eee18b_0 ", "  setuptools         anaconda/pkgs/main/linux-64::setuptools-69.5.1-py310h06a4308_0 ", "  sqlite             anaconda/pkgs/main/linux-64::sqlite-3.45.3-h5eee18b_0 ", "  tk                 anaconda/pkgs/main/linux-64::tk-8.6.14-h39e8969_0 ", "  tzdata             anaconda/pkgs/main/noarch::tzdata-2024a-h04d1e81_0 ", "  wheel              anaconda/pkgs/main/linux-64::wheel-0.43.0-py310h06a4308_0 ", "  xz                 anaconda/pkgs/main/linux-64::xz-5.4.6-h5eee18b_1 ", "  zlib               anaconda/pkgs/main/linux-64::zlib-1.2.13-h5eee18b_1 ", "", "", "", "Downloading and Extracting Packages: ...working... done", "Preparing transaction: ...working... done", "Verifying transaction: ...working... done", "Executing transaction: ...working... done", "#", "# To activate this environment, use", "#", "#     $ conda activate supervisorPython3.10.13", "#", "# To deactivate an active environment, use", "#", "#     $ conda deactivate"]}

TASK [supervisor : Show virtual environments] ************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "cmd": ["/srv/miniconda3/bin/conda", "env", "list"], "delta": "0:00:00.300997", "end": "2024-05-23 23:44:25.746078", "rc": 0, "start": "2024-05-23 23:44:25.445081", "stderr": "", "stderr_lines": [], "stdout": "# conda environments:\n#\nbase                     /srv/miniconda3\nsupervisorPython3.10.13     /srv/miniconda3/envs/supervisorPython3.10.13", "stdout_lines": ["# conda environments:", "#", "base                     /srv/miniconda3", "supervisorPython3.10.13     /srv/miniconda3/envs/supervisorPython3.10.13"]}

TASK [supervisor : Show virtual Python version] **********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "cmd": ["/srv/miniconda3/envs/supervisorPython3.10.13/bin/python", "-V"], "delta": "0:00:00.002003", "end": "2024-05-23 23:44:26.101416", "rc": 0, "start": "2024-05-23 23:44:26.099413", "stderr": "", "stderr_lines": [], "stdout": "Python 3.10.13", "stdout_lines": ["Python 3.10.13"]}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 16 seconds
[root@ansible ansible_playbooks]#
```

![](/img/Snipaste_2024-05-23_23-45-23.png)

可以看到，剧本执行成功。在节点1上面去检查一下：

```sh
[root@ansible-node1 bin]# ./conda env list
# conda environments:
#
base                     /srv/miniconda3
supervisorPython3.10.13     /srv/miniconda3/envs/supervisorPython3.10.13

[root@ansible-node1 bin]# /srv/miniconda3/envs/supervisorPython3.10.13/bin/python -V
Python 3.10.13
[root@ansible-node1 bin]#
```

可以看到，虚拟环境supervisorPython3.10.13创建成功，对应虚拟环境的Python版本是Python 3.10.13。



### 2.11 任务三-配置supervisor进程管理工具

上一节我们已经创建了一个虚拟环境supervisorPython3.10.13，

下面在该虚拟环境下安装supervisor包及其依赖。然后将supervisord.conf和supervisord.service等配置文件复制到远程主机，最后启动supervisord服务。

由`roles/supervisor/tasks/supervisor.yaml`定义，查看该文件内容：

```yaml
---
- name: Install python package supervisor
  ansible.builtin.pip:
    name: supervisor
    # /srv/miniconda3/envs/supervisorPython3.10.13/bin/pip
    executable: "{{ MINICONDA_BASE_DIR }}/envs/{{ VIRTUAL_ENV_NAME }}/bin/pip"
  vars:
    ansible_python_interpreter: "{{ MINICONDA_BASE_DIR }}/envs/{{ VIRTUAL_ENV_NAME }}/bin/python"

- name: Show supervisor executable files
  ansible.builtin.find:
    paths: "{{ MINICONDA_BASE_DIR }}/envs/{{ VIRTUAL_ENV_NAME }}/bin"
    patterns: '*supervisor*'
  changed_when: False

- name: Copy supervisord.conf file
  ansible.builtin.template:
    src: supervisord.conf.j2
    dest: "{{ SUPERVISORD_CONFIG_FILE }}"
    mode: '0600'
    force: yes
    backup: yes
    remote_src: no

- name: Create a directory if it does not exist
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  with_items:
    - /etc/supervisord.d
    - "{{ SUPERVISOR_BASE_DIR }}"
    - "{{ SUPERVISOR_BASE_DIR }}/pid"
    - "{{ SUPERVISOR_BASE_DIR }}/logs"
    - "{{ SUPERVISOR_BASE_DIR }}/socket"

- name: Copy supervisor test app config
  ansible.builtin.copy:
    src: app.ini
    dest: /etc/supervisord.d/app.ini
    force: yes
    backup: yes
    remote_src: no

- name: Copy supervisor service file
  ansible.builtin.template:
    src: supervisord.service.j2
    dest: /usr/lib/systemd/system/supervisord.service
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



此处需要注意的是，通过`ansible_python_interpreter`变量来指定远程主机上的python解释器路径 ，避免使用默认的python解释器。

像前面任务二一样，修改`roles/supervisor/tasks/main.yml`配置文件，将前面两个测试好的任务关掉：

```yaml
---
# supervisor角色任务
# 安装mincoda
#- include: miniconda.yaml
# 创建虚拟环境
#- include: virtual_env.yaml
# 配置supervisor进程管理工具
- include: supervisor.yaml
# 创建快捷命令
#- include: alias.yaml

```

然后执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini supervisor.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [supervisorhosts] ***********************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]

TASK [Install python package supervisor] *****************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "cmd": ["/srv/miniconda3/envs/supervisorPython3.10.13/bin/pip", "install", "supervisor"], "name": ["supervisor"], "requirements": null, "state": "present", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv\n", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nCollecting supervisor\n  Downloading http://mirrors.aliyun.com/pypi/packages/2c/7a/0ad3973941590c040475046fef37a2b08a76691e61aa59540828ee235a6e/supervisor-4.2.5-py2.py3-none-any.whl (319 kB)\n     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 319.6/319.6 kB 163.9 kB/s eta 0:00:00\nRequirement already satisfied: setuptools in /srv/miniconda3/envs/supervisorPython3.10.13/lib/python3.10/site-packages (from supervisor) (69.5.1)\nInstalling collected packages: supervisor\nSuccessfully installed supervisor-4.2.5\n", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Collecting supervisor", "  Downloading http://mirrors.aliyun.com/pypi/packages/2c/7a/0ad3973941590c040475046fef37a2b08a76691e61aa59540828ee235a6e/supervisor-4.2.5-py2.py3-none-any.whl (319 kB)", "     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 319.6/319.6 kB 163.9 kB/s eta 0:00:00", "Requirement already satisfied: setuptools in /srv/miniconda3/envs/supervisorPython3.10.13/lib/python3.10/site-packages (from supervisor) (69.5.1)", "Installing collected packages: supervisor", "Successfully installed supervisor-4.2.5"], "version": null, "virtualenv": null}

TASK [Show supervisor executable files] ******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "examined": 75, "files": [{"atime": 1716626372.7525017, "ctime": 1716626372.7465017, "dev": 64768, "gid": 0, "gr_name": "root", "inode": 34017491, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": true, "issock": false, "isuid": false, "mode": "0755", "mtime": 1716626372.7465017, "nlink": 1, "path": "/srv/miniconda3/envs/supervisorPython3.10.13/bin/echo_supervisord_conf", "pw_name": "root", "rgrp": true, "roth": true, "rusr": true, "size": 257, "uid": 0, "wgrp": false, "woth": false, "wusr": true, "xgrp": true, "xoth": true, "xusr": true}, {"atime": 1716626372.7525017, "ctime": 1716626372.7465017, "dev": 64768, "gid": 0, "gr_name": "root", "inode": 34017493, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": true, "issock": false, "isuid": false, "mode": "0755", "mtime": 1716626372.7465017, "nlink": 1, "path": "/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisorctl", "pw_name": "root", "rgrp": true, "roth": true, "rusr": true, "size": 262, "uid": 0, "wgrp": false, "woth": false, "wusr": true, "xgrp": true, "xoth": true, "xusr": true}, {"atime": 1716626372.7525017, "ctime": 1716626372.7465017, "dev": 64768, "gid": 0, "gr_name": "root", "inode": 34017494, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": true, "issock": false, "isuid": false, "mode": "0755", "mtime": 1716626372.7465017, "nlink": 1, "path": "/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord", "pw_name": "root", "rgrp": true, "roth": true, "rusr": true, "size": 260, "uid": 0, "wgrp": false, "woth": false, "wusr": true, "xgrp": true, "xoth": true, "xusr": true}], "matched": 3, "msg": ""}

TASK [Copy supervisord.conf file] ************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "77992e3dab6a4a7605837a0ff91ef3d6156dcb33", "dest": "/etc/supervisord.conf", "gid": 0, "group": "root", "mode": "0600", "owner": "root", "path": "/etc/supervisord.conf", "size": 10925, "state": "file", "uid": 0}

TASK [supervisor : Create a directory if it does not exist] **********************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => (item=/etc/supervisord.d) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/etc/supervisord.d", "mode": "0755", "owner": "root", "path": "/etc/supervisord.d", "size": 21, "state": "directory", "uid": 0}
ok: [192.168.56.121] => (item=/srv/supervisor) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/supervisor", "mode": "0755", "owner": "root", "path": "/srv/supervisor", "size": 43, "state": "directory", "uid": 0}
ok: [192.168.56.121] => (item=/srv/supervisor/pid) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/supervisor/pid", "mode": "0755", "owner": "root", "path": "/srv/supervisor/pid", "size": 6, "state": "directory", "uid": 0}
ok: [192.168.56.121] => (item=/srv/supervisor/logs) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/supervisor/logs", "mode": "0755", "owner": "root", "path": "/srv/supervisor/logs", "size": 29, "state": "directory", "uid": 0}
ok: [192.168.56.121] => (item=/srv/supervisor/socket) => {"ansible_loop_var": "item", "changed": false, "gid": 0, "group": "root", "item": "/srv/supervisor/socket", "mode": "0755", "owner": "root", "path": "/srv/supervisor/socket", "size": 6, "state": "directory", "uid": 0}

TASK [Copy supervisor test app config] *******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "7137be46fd82131df6404446399948bd3cb4f600", "dest": "/etc/supervisord.d/app.ini", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/etc/supervisord.d/app.ini", "size": 36, "state": "file", "uid": 0}

TASK [Copy supervisor service file] **********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "checksum": "16b394317b270a868dd88147c5b179921d726eb6", "dest": "/usr/lib/systemd/system/supervisord.service", "gid": 0, "group": "root", "mode": "0644", "owner": "root", "path": "/usr/lib/systemd/system/supervisord.service", "size": 365, "state": "file", "uid": 0}

TASK [Start service supervisord, in all cases] ***********************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "enabled": true, "name": "supervisord", "state": "started", "status": {"ActiveEnterTimestampMonotonic": "0", "ActiveExitTimestampMonotonic": "0", "ActiveState": "inactive", "After": "rc-local.service system.slice basic.target nss-user-lookup.target systemd-journald.socket", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "no", "AssertTimestampMonotonic": "0", "Before": "shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "no", "ConditionTimestampMonotonic": "0", "Conflicts": "shutdown.target", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Process Monitoring and Control Daemon", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "0", "ExecMainStartTimestampMonotonic": "0", "ExecMainStatus": "0", "ExecStart": "{ path=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord ; argv[]=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/supervisord.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "supervisord.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestampMonotonic": "0", "InactiveExitTimestampMonotonic": "0", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "7259", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "7259", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "0", "MemoryAccounting": "no", "MemoryCurrent": "18446744073709551615", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "supervisord.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target system.slice", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "dead", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "18446744073709551615", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "1min 30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "disabled", "WatchdogTimestampMonotonic": "0", "WatchdogUSec": "0"}}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=8    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 8 seconds
[root@ansible ansible_playbooks]#
```

执行过程截图：

![](/img/Snipaste_2024-05-25_16-41-11.png)

可以看到，任务正常完成，中间创建supervisor相关目录和复制配置文件，由于我之前测试过，文件已经复制到远程主机上了或者文件夹已经创建过了，所以执行过程中显示任务未产生变更。最后一个任务`Start service supervisord, in all cases`可以看到，supervisord服务正常启动了。



我们在节点1上面检查一下：

```sh
[root@ansible-node1 ~]# systemctl status supervisord
● supervisord.service - Process Monitoring and Control Daemon
   Loaded: loaded (/usr/lib/systemd/system/supervisord.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2024-05-25 16:39:37 CST; 1min 5s ago
  Process: 2339 ExecStart=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf (code=exited, status=0/SUCCESS)
 Main PID: 2340 (supervisord)
   CGroup: /system.slice/supervisord.service
           ├─2340 /srv/miniconda3/envs/supervisorPython3.10.13/bin/python /srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf
           └─2349 /bin/cat

May 25 16:39:37 ansible-node1 systemd[1]: Starting Process Monitoring and Control Daemon...
May 25 16:39:37 ansible-node1 systemd[1]: Started Process Monitoring and Control Daemon.
[root@ansible-node1 ~]#  /srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisorctl status
testapp                          RUNNING   pid 2349, uptime 0:04:27
[root@ansible-node1 ~]#
```

可以看到，supervisord服务正常启动了，由其管理的`testapp`应用也正常启动了，说明supervisor进程管理工具配置正常。

到此，跟supervisor相关的配置就差不多完成了，但每次查看supervisor进程管理工具管理的应用状态，都需要输入那么长的命令，如`/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisorctl status`，将显得有点麻烦，因此，就应该为这些命令配置一些快捷命令，这就是下一个任务创建快捷命令的由来。



### 2.11 任务四-创建快捷命令

创建快捷命令的任务，由`roles/supervisor/tasks/alias.yaml`定义，查看该文件内容：

```yaml
---
- name: Copy alias config
  ansible.builtin.template:
    src: alias_supervisor.sh.j2
    dest: /root/.alias_supervisor.sh
    force: yes
    backup: yes
    remote_src: no

- name: Insert block to .bashrc
  ansible.builtin.blockinfile:
    path: /root/.bashrc
    block: |
      source ~/.alias_supervisor.sh
    create: yes
    # 注意，需要设置不同的marker标记，否则会修改以前存在的默认标记
    marker: "# {mark} meizhaohui add supervisor alias"
    state: present

```

此任务将自定义的相关快捷命令都写到`/root/.alias_supervisor.sh`这个文件里面，然后在`/root/.bashrc`中加载这个文件。

查看`alias_supervisor.sh.j2`模板内容：

```sh
# meizhaohui add this
# supervisor相关的快捷命令
alias supervisordStatus='systemctl status supervisord'
alias supervisordRestart='systemctl restart supervisord'
alias spctl='{{ SUPERVISORD_DIR_PATH }}/supervisorctl'
alias spreload='{{ SUPERVISORD_DIR_PATH }}/supervisorctl reload'
alias spstatus='sp_status'
function sp_status() {
    {{ SUPERVISORD_DIR_PATH }}/supervisorctl status $1|awk '{if($2=="RUNNING"){printf "\033[1;32m"$0"\033[0m\n"} else if($2=="STOPPED"){printf "\033[1;33m"$0"\033[0m\n"} else {print "\033[1;31m"$0"\033[0m"} }'
}

```

像前面任务一样，修改`roles/supervisor/tasks/main.yml`配置文件，将前面三个测试好的任务关掉：

```yaml
---
# supervisor角色任务
# 安装mincoda
#- include: miniconda.yaml
# 创建虚拟环境
#- include: virtual_env.yaml
# 配置supervisor进程管理工具
#- include: supervisor.yaml
# 创建快捷命令
- include: alias.yaml

```

然后执行剧本：

```sh

[root@ansible ansible_playbooks]# ansible-playbook -i hosts.ini supervisor.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [supervisorhosts] ***********************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]

TASK [supervisor : Copy alias config] ********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "ac45722c54f80be7acfbe97bd8049e8759d0fe38", "dest": "/root/.alias_supervisor.sh", "gid": 0, "group": "root", "md5sum": "782a6cbdd363ff30afbc78d83b16128d", "mode": "0644", "owner": "root", "size": 617, "src": "/root/.ansible/tmp/ansible-tmp-1716627556.73-1741-224175243910168/source", "state": "file", "uid": 0}

TASK [supervisor : Insert block to .bashrc] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "msg": "Block inserted"}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Playbook run took 0 days, 0 hours, 0 minutes, 2 seconds
[root@ansible ansible_playbooks]#
```

执行过程截图：

![](/img/Snipaste_2024-05-25_17-00-04.png)

然后在节点1上面去检查，执行一些相关的命令：

```sh
[root@ansible-node1 ~]# alias|grep super
alias spctl='/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisorctl'
alias spreload='/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisorctl reload'
alias supervisordRestart='systemctl restart supervisord'
alias supervisordStatus='systemctl status supervisord'
[root@ansible-node1 ~]# supervisordStatus
● supervisord.service - Process Monitoring and Control Daemon
   Loaded: loaded (/usr/lib/systemd/system/supervisord.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2024-05-25 16:39:37 CST; 21min ago
  Process: 2339 ExecStart=/srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf (code=exited, status=0/SUCCESS)
 Main PID: 2340 (supervisord)
   CGroup: /system.slice/supervisord.service
           ├─2340 /srv/miniconda3/envs/supervisorPython3.10.13/bin/python /srv/miniconda3/envs/supervisorPython3.10.13/bin/supervisord -c /etc/supervisord.conf
           └─2349 /bin/cat

May 25 16:39:37 ansible-node1 systemd[1]: Starting Process Monitoring and Control Daemon...
May 25 16:39:37 ansible-node1 systemd[1]: Started Process Monitoring and Control Daemon.
[root@ansible-node1 ~]# spctl status
testapp                          RUNNING   pid 2349, uptime 0:21:59
[root@ansible-node1 ~]# spctl status testapp
testapp                          RUNNING   pid 2349, uptime 0:22:03
[root@ansible-node1 ~]# spstatus
testapp                          RUNNING   pid 2349, uptime 0:22:09
[root@ansible-node1 ~]# spstatus testapp
testapp                          RUNNING   pid 2349, uptime 0:22:14
[root@ansible-node1 ~]# spctl restart testapp
testapp: stopped
testapp: started
[root@ansible-node1 ~]# spstatus
testapp                          RUNNING   pid 2672, uptime 0:00:04
[root@ansible-node1 ~]# spstatus
testapp                          RUNNING   pid 2672, uptime 0:00:08
[root@ansible-node1 ~]#
```

执行过程截图：

![](/img/Snipaste_2024-05-25_17-03-05.png)

可以看到，supervisor相关的快捷命令都能正常使用了，说明创建快捷命令这个子任务也能正常工作了！！

