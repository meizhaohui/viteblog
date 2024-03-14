# 一步一步学role角色4-include的使用

[[toc]]

## 1. 概述

这是一个序列总结文档。

- 第1节 [ansible role角色(1)](./role.md) 中，我们阅读了官方文档，并且知道了角色相关的概念。
- 第2节 [ansible role角色(2)--创建第一个role角色](./role_2.md) 创建一个简单的测试role角色。
- 第3节 [ansible role角色(3)--一步一步学role角色](./role_3.md)，base基础角色配置。

本节是在上节的基础上，使用`include`关键字来优化base剧本。



### 1.1 VirtualBox虚拟机信息记录

| 序号 | 虚拟机         | 主机名  | IP             | CPU  | 内存 | 说明             |
| ---- | -------------- | ------- | -------------- | ---- | ---- | ---------------- |
| 1    | ansible-master | ansible | 192.168.56.120 | 2核  | 4G   | Ansible控制节点  |
| 2    | ansible-node1  | node1   | 192.168.56.121 | 2核  | 2G   | Ansible工作节点1 |
| 3    | ansible-node2  | node2   | 192.168.56.122 | 2核  | 2G   | Ansible工作节点2 |
| 4    | ansible-node3  | node3   | 192.168.56.123 | 2核  | 2G   | Ansible工作节点3 |




### 1.2. 回顾

上节我编写了一个可以实际使用的角色，命名为`base`角色。该角色包含以下功能：

- 设置主机名称。
- 永久关闭SELINUX。
- 添加`yum`、`epel`源，用来加速软件安装。
- 配置pip国内镜像加速。
- 安装vim、telnet、python3、ntpdate、java、wget、lrzsz、dos2unix、git等基础包。
- 安装`safe-rm`和`trash-cli`防误删工具。
- 设置时间同步定时任务。
- 生成主机公钥私钥对。
- 设置常用快捷命令。（这个功能上节未处理）

### 1.3 角色目录结构

最开始我们的角色目录结构比较简单，仅创建`base`目录，然后创建`tasks`目录，再在`tasks`目录下面创建`main.yml`任务文件，目录结构如下：

```sh
$ tree
.
+--- base
|   +--- tasks
|   |   +--- main.yml
```

目录结构和任务文件创建完成后，我们就开始进行任务分解，构建自己的自动化任务。

如果前每个功能的任务配置都取消注释，`main.yml`文件是下面这样的：

```yaml
---
- name: Show hostname
  ansible.builtin.debug:
    msg: "{{ hostname }}"

- name: Set hostname
  ansible.builtin.hostname:
    name: "{{ ansible_hostname }}"

- name: Set SELinux prints warnings instead of enforcing
  ansible.builtin.command:
    cmd: setenforce 0

- name: Ensure SELinux is set to disable mode
  ansible.builtin.lineinfile:
    path: /etc/selinux/config
    regexp: '^SELINUX='
    line: SELINUX=disabled

- name: Get SELinux value
  ansible.builtin.command:
    cmd: getenforce

- name: Create a directory if it does not exist
  ansible.builtin.file:
    path: ~/.pip
    state: directory
    mode: '0755'

- name: Create backup directory
  ansible.builtin.file:
    path: /etc/yum.repos.d.bak
    state: directory
    mode: '0755'

- name: Backup old repo config
  ansible.builtin.copy:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    remote_src: yes
  with_items:
    - { src: '/etc/yum.repos.d/CentOS-Base.repo', dest: '/etc/yum.repos.d.bak/CentOS-Base.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-CR.repo', dest: '/etc/yum.repos.d.bak/CentOS-CR.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-Debuginfo.repo', dest: '/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-fasttrack.repo', dest: '/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-Media.repo', dest: '/etc/yum.repos.d.bak/CentOS-Media.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-Sources.repo', dest: '/etc/yum.repos.d.bak/CentOS-Sources.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-Vault.repo', dest: '/etc/yum.repos.d.bak/CentOS-Vault.repo.bak'}
    - { src: '/etc/yum.repos.d/CentOS-x86_64-kernel.repo', dest: '/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak'}

- name: Remove old repo config
  ansible.builtin.file:
    path: "{{ item }}"
    state: absent
  with_items:
    - /etc/yum.repos.d/CentOS-Base.repo
    - /etc/yum.repos.d/CentOS-CR.repo
    - /etc/yum.repos.d/CentOS-Debuginfo.repo
    - /etc/yum.repos.d/CentOS-fasttrack.repo
    - /etc/yum.repos.d/CentOS-Media.repo
    - /etc/yum.repos.d/CentOS-Sources.repo
    - /etc/yum.repos.d/CentOS-Vault.repo
    - /etc/yum.repos.d/CentOS-x86_64-kernel.repo

- name: Copy repo and pypi config
  ansible.builtin.copy:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    remote_src: no
  with_items:
    - { src: 'Centos-7.repo', dest: '/etc/yum.repos.d/Centos-7.repo'}
    - { src: 'epel-7.repo', dest: '/etc/yum.repos.d/epel-7.repo'}
    - { src: 'pip.conf', dest: '~/.pip/pip.conf'}

- name: ensure a list of packages installed
  ansible.builtin.yum:
    name: "{{ packages }}"
  vars:
    packages:
    - vim
    - telnet
    - python3
    - ntpdate
    - wget
    - lrzsz
    - git
    - java-1.8.0-openjdk
    - java-1.8.0-openjdk-devel

- name: create base folder
  ansible.builtin.file:
    path: /srv/safe-rm
    state: directory

- name: Extract safe-rm-0.12.tar.gz into /srv/safe-rm
  ansible.builtin.unarchive:
    src: safe-rm-0.12.tar.gz
    # dest目标目录必须是存在的目录
    dest: /srv/safe-rm
    owner: root
    group: root

- name: Move safe-rm to /usr/bin
  ansible.builtin.copy:
    dest: /usr/bin/safe-rm
    src: /srv/safe-rm/safe-rm-0.12/safe-rm
    remote_src: yes
    mode: '0755'

- name: Delete temp folder
  ansible.builtin.file:
    path: /srv/safe-rm
    state: absent

- name: Copy safe-rm config
  ansible.builtin.copy:
    src: safe-rm.conf
    dest: /etc/safe-rm.conf
    remote_src: no

# 注意，默认python3.6.8自带的pip版本较低，如果不升级的话，下一步的trash-cli包安装就会报异常
- name: Update pip command
  ansible.builtin.command:
    cmd: python3 -m pip install --upgrade pip

- name: Install python package
  ansible.builtin.pip:
    name: trash-cli
    executable: pip3
  vars:
    ansible_python_interpreter: /usr/bin/python3

- name: Sync time at every 10 minutes
  ansible.builtin.cron:
    name: "Sync time"
    minute: "*/10"
    # 与阿里云NTP时间源服务器同步
    job: "/usr/sbin/ntpdate ntp1.aliyun.com > /dev/null 2>&1"
    state: present

- name: Sync time at 2:30 am
  ansible.builtin.cron:
    name: "Set hardware clock time"
    minute: "30"
    hour: "2"
    # --systohc 将硬件时钟调整为与目前的系统时钟一致
    job: "/usr/sbin/hwclock --systohc > /dev/null 2>&1"
    state: present

- name: Print the IP
  ansible.builtin.debug:
    msg: "HOST_IP: {{ HOST_IP }}"

- name: Generate SSH key pair
  ansible.builtin.command:
    cmd: "ssh-keygen -C root@{{ HOST_IP }} -N '' -q -f /root/.ssh/id_rsa"

```

可以看到，剧本文件非常长，将多个功能合在一个文件里面，不便于后期维护，此时就可以使用`include`关键字，将各功能拆分成小的文件，然后使用`include`导入。

## 2. 拆分剧本文件

我们按功能进行拆分。为了测试拆分后的剧本是否能正常工作。我们先拆分出两个子任务：

- `hostname.yaml`，设置主机名称。
- `selinux.yaml`， 关闭SELINUX。

并将两个文件也放在`tasks`目录下：

```sh
[root@ansible ansible_playbooks]# tree roles/base/tasks/
roles/base/tasks/
├── hostname.yaml
├── main.yml
└── selinux.yaml

0 directories, 3 files
[root@ansible ansible_playbooks]#
```

子任务设置主机名称配置文件`hostname.yaml`内容如下：

```yaml
---
- name: Show hostname
  ansible.builtin.debug:
    msg: "{{ hostname }}"

- name: Set hostname
  ansible.builtin.hostname:
    name: "{{ ansible_hostname }}"

```

子任务关闭SELINUX配置文件`selinux.yaml`内容如下：

```yaml
---
- name: Get SELinux value
  ansible.builtin.command:
    cmd: getenforce
  register: selinux_result
  changed_when: false

- name: Set SELinux prints warnings instead of enforcing
  ansible.builtin.command:
    cmd: setenforce 0
  when: "'Disabled' not in selinux_result.stdout"

- name: Ensure SELinux is set to disable mode
  ansible.builtin.lineinfile:
    path: /etc/selinux/config
    regexp: '^SELINUX='
    line: SELINUX=disabled

- name: Get SELinux value
  ansible.builtin.command:
    cmd: getenforce
  changed_when: false

```

注意，此处子任务剧本稍微做了些修改，避免执行`setenforce 0`出现以下异常导致任务失败：

```sh
[root@ansible-node1 ~]# setenforce 0
setenforce: SELinux is disabled
[root@ansible-node1 ~]# echo $?
1
```

然后修改`main.yml`主任务文件：

```yaml
---
- include: hostname.yaml
- include: selinux.yaml

```

修改完成后，查看三个文件的内容：

```sh
[root@ansible ansible_playbooks]# cat roles/base/tasks/hostname.yaml
---
- name: Show hostname
  ansible.builtin.debug:
    msg: "{{ hostname }}"

- name: Set hostname
  ansible.builtin.hostname:
    name: "{{ ansible_hostname }}"

[root@ansible ansible_playbooks]# cat roles/base/tasks/selinux.yaml
---
- name: Get SELinux value
  ansible.builtin.command:
    cmd: getenforce
  register: selinux_result
  changed_when: false

- name: Set SELinux prints warnings instead of enforcing
  ansible.builtin.command:
    cmd: setenforce 0
  when: "'Disabled' not in selinux_result.stdout"

- name: Ensure SELinux is set to disable mode
  ansible.builtin.lineinfile:
    path: /etc/selinux/config
    regexp: '^SELINUX='
    line: SELINUX=disabled

- name: Get SELinux value
  ansible.builtin.command:
    cmd: getenforce
  changed_when: false
[root@ansible ansible_playbooks]# cat roles/base/tasks/main.yml
---
- include: hostname.yaml
- include: selinux.yaml

[root@ansible ansible_playbooks]#
```

然后执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.122]
ok: [192.168.56.121]

TASK [base : Show hostname] ******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {
    "msg": "ansible-node2"
}
ok: [192.168.56.123] => {
    "msg": "ansible-node3"
}
ok: [192.168.56.121] => {
    "msg": "ansible-node1"
}

TASK [base : Set hostname] *******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node2", "ansible_hostname": "ansible-node2", "ansible_nodename": "ansible-node2"}, "changed": false, "name": "ansible-node2"}
ok: [192.168.56.123] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node3", "ansible_hostname": "ansible-node3", "ansible_nodename": "ansible-node3"}, "changed": false, "name": "ansible-node3"}
ok: [192.168.56.121] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node1", "ansible_hostname": "ansible-node1", "ansible_nodename": "ansible-node1"}, "changed": false, "name": "ansible-node1"}

TASK [base : Get SELinux value] **************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "cmd": ["getenforce"], "delta": "0:00:00.001937", "end": "2024-03-14 20:44:52.737811", "rc": 0, "start": "2024-03-14 20:44:52.735874", "stderr": "", "stderr_lines": [], "stdout": "Disabled", "stdout_lines": ["Disabled"]}
ok: [192.168.56.123] => {"changed": false, "cmd": ["getenforce"], "delta": "0:00:00.002027", "end": "2024-03-14 20:44:52.732116", "rc": 0, "start": "2024-03-14 20:44:52.730089", "stderr": "", "stderr_lines": [], "stdout": "Disabled", "stdout_lines": ["Disabled"]}
ok: [192.168.56.122] => {"changed": false, "cmd": ["getenforce"], "delta": "0:00:00.002094", "end": "2024-03-14 20:44:52.755255", "rc": 0, "start": "2024-03-14 20:44:52.753161", "stderr": "", "stderr_lines": [], "stdout": "Disabled", "stdout_lines": ["Disabled"]}

TASK [base : Set SELinux prints warnings instead of enforcing] *******************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.123] => {"changed": false, "skip_reason": "Conditional result was False"}
skipping: [192.168.56.122] => {"changed": false, "skip_reason": "Conditional result was False"}

TASK [base : Ensure SELinux is set to disable mode] ******************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {"backup": "", "changed": false, "msg": ""}
ok: [192.168.56.122] => {"backup": "", "changed": false, "msg": ""}
ok: [192.168.56.121] => {"backup": "", "changed": false, "msg": ""}

TASK [base : Get SELinux value] **************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"changed": false, "cmd": ["getenforce"], "delta": "0:00:00.001889", "end": "2024-03-14 20:44:53.453721", "rc": 0, "start": "2024-03-14 20:44:53.451832", "stderr": "", "stderr_lines": [], "stdout": "Disabled", "stdout_lines": ["Disabled"]}
ok: [192.168.56.123] => {"changed": false, "cmd": ["getenforce"], "delta": "0:00:00.001774", "end": "2024-03-14 20:44:53.474068", "rc": 0, "start": "2024-03-14 20:44:53.472294", "stderr": "", "stderr_lines": [], "stdout": "Disabled", "stdout_lines": ["Disabled"]}
ok: [192.168.56.122] => {"changed": false, "cmd": ["getenforce"], "delta": "0:00:00.003020", "end": "2024-03-14 20:44:53.488909", "rc": 0, "start": "2024-03-14 20:44:53.485889", "stderr": "", "stderr_lines": [], "stdout": "Disabled", "stdout_lines": ["Disabled"]}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=6    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
192.168.56.122             : ok=6    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
192.168.56.123             : ok=6    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

![Snipaste_2024-03-14_20-45-19.png](/img/Snipaste_2024-03-14_20-45-19.png)

可以看到剧本能够正常执行，说明拆分主任务文件后，剧本能够正常工作！

再就是将其他几个功能依次进行拆分，并进行测试。

拆分后，目录结构如下：

```sh

[root@ansible ansible_playbooks]# tree roles/base
roles/base
├── files
│   ├── Centos-7.repo
│   ├── epel-7.repo
│   ├── pip.conf
│   ├── safe-rm-0.12.tar.gz
│   └── safe-rm.conf
├── tasks
│   ├── crontab.yaml
│   ├── hostname.yaml
│   ├── main.yml
│   ├── packages.yaml
│   ├── repositories.yaml
│   ├── safe-rm.yaml
│   ├── selinux.yaml
│   ├── ssh-keygen.yaml
│   └── trash-cli.yaml
└── vars
    └── main.yml

3 directories, 15 files
[root@ansible ansible_playbooks]#
```

以下是优化后的子任务配置文件：

- repositories.yaml 镜像源

```yaml
---
- name: Create a directory if it does not exist
  ansible.builtin.file:
    path: ~/.pip
    state: directory
    mode: '0755'

- name: Create backup directory
  ansible.builtin.file:
    path: /etc/yum.repos.d.bak
    state: directory
    mode: '0755'

- name: Backup old repo config
  ansible.builtin.copy:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    remote_src: yes
  with_items:
    - { src: '/etc/yum.repos.d', dest: '/etc/yum.repos.d.bak'}

- name: Create repositories directory
  ansible.builtin.file:
    path: /etc/yum.repos.d
    state: directory
    mode: '0755'

- name: Copy repo and pypi config
  ansible.builtin.copy:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    remote_src: no
  with_items:
    - { src: 'Centos-7.repo', dest: '/etc/yum.repos.d/Centos-7.repo'}
    - { src: 'epel-7.repo', dest: '/etc/yum.repos.d/epel-7.repo'}
    - { src: 'pip.conf', dest: '~/.pip/pip.conf'}

```

- packages.yaml 基础软件包

```yaml
---
- name: ensure a list of packages installed
  ansible.builtin.yum:
    name: "{{ packages }}"
  vars:
    packages:
    - vim
    - telnet
    - python3
    - ntpdate
    - wget
    - lrzsz
    - git
    - java-1.8.0-openjdk
    - java-1.8.0-openjdk-devel

```

- safe-rm.yaml 防误删工具

```yaml
---
- name: create base folder
  ansible.builtin.file:
    path: /srv/safe-rm
    state: directory

- name: Extract safe-rm-0.12.tar.gz into /srv/safe-rm
  ansible.builtin.unarchive:
    src: safe-rm-0.12.tar.gz
    # dest目标目录必须是存在的目录
    dest: /srv/safe-rm
    owner: root
    group: root

- name: Move safe-rm to /usr/bin
  ansible.builtin.copy:
    dest: /usr/bin/safe-rm
    src: /srv/safe-rm/safe-rm-0.12/safe-rm
    remote_src: yes
    mode: '0755'

- name: Delete temp folder
  ansible.builtin.file:
    path: /srv/safe-rm
    state: absent

- name: Copy safe-rm config
  ansible.builtin.copy:
    src: safe-rm.conf
    dest: /etc/safe-rm.conf
    remote_src: no

```



- trash-cli.yaml 防误删工具

```yaml
---
# 注意，默认python3.6.8自带的pip版本较低，如果不升级的话，下一步的trash-cli包安装就会报异常
- name: Update pip command
  ansible.builtin.command:
    cmd: python3 -m pip install --upgrade pip

- name: Install python package
  ansible.builtin.pip:
    name: trash-cli
    executable: pip3
  vars:
    ansible_python_interpreter: /usr/bin/python3

```

- crontab.yaml 定时任务

```yaml
---
- name: Sync time at every 10 minutes
  ansible.builtin.cron:
    name: "Sync time"
    minute: "*/10"
    # 与阿里云NTP时间源服务器同步
    job: "/usr/sbin/ntpdate ntp1.aliyun.com > /dev/null 2>&1"
    state: present

- name: Sync time at 2:30 am
  ansible.builtin.cron:
    name: "Set hardware clock time"
    minute: "30"
    hour: "2"
    # --systohc 将硬件时钟调整为与目前的系统时钟一致
    job: "/usr/sbin/hwclock --systohc > /dev/null 2>&1"
    state: present

```

- ssh-keygen.yaml 公钥密钥对

```yaml
---
- name: Print the IP
  ansible.builtin.debug:
    msg: "HOST_IP: {{ HOST_IP }}"

# 避免重复运行时，导致新生成密钥对失败
- name: Remove sshkey file
  ansible.builtin.file:
    path: "{{ item }}"
    state: absent
  with_items:
    - /root/.ssh/id_rsa
    - /root/.ssh/id_rsa.pub

- name: Generate SSH key pair
  ansible.builtin.command:
    cmd: "ssh-keygen -C root@{{ HOST_IP }} -N '' -q -f /root/.ssh/id_rsa"

```

优化后，重新执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [base : Show hostname] ******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {
    "msg": "ansible-node3"
}
ok: [192.168.56.121] => {
    "msg": "ansible-node1"
}
ok: [192.168.56.122] => {
    "msg": "ansible-node2"
}

TASK [base : Set hostname] *******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Get SELinux value] **************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Set SELinux prints warnings instead of enforcing] *******************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121]
skipping: [192.168.56.122]
skipping: [192.168.56.123]

TASK [base : Ensure SELinux is set to disable mode] ******************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.122]
ok: [192.168.56.121]

TASK [base : Get SELinux value] **************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Create a directory if it does not exist] ****************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [base : Create backup directory] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Backup old repo config] *********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak', u'src': u'/etc/yum.repos.d'})
ok: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak', u'src': u'/etc/yum.repos.d'})
ok: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak', u'src': u'/etc/yum.repos.d'})

TASK [base : Create backup directory] ********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [base : Copy repo and pypi config] ******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d/Centos-7.repo', u'src': u'Centos-7.repo'})
ok: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d/Centos-7.repo', u'src': u'Centos-7.repo'})
ok: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d/Centos-7.repo', u'src': u'Centos-7.repo'})
ok: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d/epel-7.repo', u'src': u'epel-7.repo'})
ok: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d/epel-7.repo', u'src': u'epel-7.repo'})
ok: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d/epel-7.repo', u'src': u'epel-7.repo'})
ok: [192.168.56.123] => (item={u'dest': u'~/.pip/pip.conf', u'src': u'pip.conf'})
ok: [192.168.56.122] => (item={u'dest': u'~/.pip/pip.conf', u'src': u'pip.conf'})
ok: [192.168.56.121] => (item={u'dest': u'~/.pip/pip.conf', u'src': u'pip.conf'})

TASK [base : ensure a list of packages installed] ********************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.122]
ok: [192.168.56.121]

TASK [create base folder] ********************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122]
changed: [192.168.56.123]
changed: [192.168.56.121]

TASK [base : Extract safe-rm-0.12.tar.gz into /srv/safe-rm] **********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123]
changed: [192.168.56.122]
changed: [192.168.56.121]

TASK [base : Move safe-rm to /usr/bin] *******************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Delete temp folder] *************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121]
changed: [192.168.56.123]
changed: [192.168.56.122]

TASK [base : Copy safe-rm config] ************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Update pip command] *************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123]
changed: [192.168.56.122]
changed: [192.168.56.121]

TASK [base : Install python package] *********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.122]
ok: [192.168.56.121]

TASK [base : Sync time at every 10 minutes] **************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [base : Sync time at 2:30 am] ***********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Print the IP] *******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "HOST_IP: 192.168.56.121"
}
ok: [192.168.56.122] => {
    "msg": "HOST_IP: 192.168.56.122"
}
ok: [192.168.56.123] => {
    "msg": "HOST_IP: 192.168.56.123"
}

TASK [base : Remove sshkey file] *************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/root/.ssh/id_rsa)
changed: [192.168.56.122] => (item=/root/.ssh/id_rsa)
changed: [192.168.56.123] => (item=/root/.ssh/id_rsa)
changed: [192.168.56.121] => (item=/root/.ssh/id_rsa.pub)
changed: [192.168.56.122] => (item=/root/.ssh/id_rsa.pub)
changed: [192.168.56.123] => (item=/root/.ssh/id_rsa.pub)

TASK [base : Generate SSH key pair] **********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122]
changed: [192.168.56.123]
changed: [192.168.56.121]

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=24   changed=6    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
192.168.56.122             : ok=24   changed=6    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
192.168.56.123             : ok=24   changed=6    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

[root@ansible ansible_playbooks]#

```

![Snipaste_2024-03-14_22-20-47.png](/img/Snipaste_2024-03-14_22-20-47.png)

![Snipaste_2024-03-14_22-21-17.png](/img/Snipaste_2024-03-14_22-21-17.png)