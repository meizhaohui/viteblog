# 一步一步学role角色-base基础角色配置

[[toc]]

## 1. 概述

这是一个序列总结文档。

- 第1节 [ansible role角色(1)](./role.md) 中，我们阅读了官方文档，并且知道了角色相关的概念。
- 第2节 [ansible role角色(2)--创建第一个role角色](./role_2.md) 创建一个简单的测试role角色。

从这节开始，我们使用VirtualBox搭建虚拟环境，来实践Ansible角色，完成自动化运维工作。后面关于角色相关介绍都是基于以下VirtualBox虚拟机信息。



### 1.1 VirtualBox虚拟机信息记录

| 序号 | 虚拟机         | 主机名  | IP             | CPU  | 内存 | 说明             |
| ---- | -------------- | ------- | -------------- | ---- | ---- | ---------------- |
| 1    | ansible-master | ansible | 192.168.56.120 | 2核  | 4G   | Ansible控制节点  |
| 2    | ansible-node1  | node1   | 192.168.56.121 | 2核  | 2G   | Ansible工作节点1 |
| 3    | ansible-node2  | node2   | 192.168.56.122 | 2核  | 2G   | Ansible工作节点2 |
| 4    | ansible-node3  | node3   | 192.168.56.123 | 2核  | 2G   | Ansible工作节点3 |



设置快速启动ansible虚拟机命令：

```sh
alias startansible='start_ansible'
function start_ansible() {
    vbm startvm ansible-master --type headless
    vbm startvm ansible-node1 --type headless
    vbm startvm ansible-node2 --type headless
    vbm startvm ansible-node3 --type headless
}
```

将以上内容保存到`~/.bashrc`配置文件中，然后启动虚拟机：

```sh
startansible
```

启动效果如下：

![](/img/Snipaste_2024-01-01_09-07-51.png)





### 1.2 基础配置

#### 1.2.1 查看ansible控制节点与工作节点连通性

```sh
# 查看当前主机IP,可以看到是Ansible控制节点
[root@ansible ~]# hostname -I
192.168.56.120 10.0.3.15

# 查看IP绑定情况
[root@ansible ~]# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

# Ansible Test
192.168.56.120 ansible-master
192.168.56.121 ansible-node1
192.168.56.122 ansible-node2
192.168.56.123 ansible-node3

# 控制节点ping工作节点1
[root@ansible ~]# ping -c 3 ansible-node1
PING ansible-node1 (192.168.56.121) 56(84) bytes of data.
64 bytes from ansible-node1 (192.168.56.121): icmp_seq=1 ttl=64 time=0.359 ms
64 bytes from ansible-node1 (192.168.56.121): icmp_seq=2 ttl=64 time=0.208 ms
64 bytes from ansible-node1 (192.168.56.121): icmp_seq=3 ttl=64 time=0.248 ms

--- ansible-node1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.208/0.271/0.359/0.066 ms

# 控制节点ping工作节点2
[root@ansible ~]# ping -c 3 ansible-node2
PING ansible-node2 (192.168.56.122) 56(84) bytes of data.
64 bytes from ansible-node2 (192.168.56.122): icmp_seq=1 ttl=64 time=0.360 ms
64 bytes from ansible-node2 (192.168.56.122): icmp_seq=2 ttl=64 time=0.252 ms
64 bytes from ansible-node2 (192.168.56.122): icmp_seq=3 ttl=64 time=0.335 ms

--- ansible-node2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.252/0.315/0.360/0.050 ms

# 控制节点ping工作节点3
[root@ansible ~]# ping -c 3 ansible-node3
PING ansible-node3 (192.168.56.123) 56(84) bytes of data.
64 bytes from ansible-node3 (192.168.56.123): icmp_seq=1 ttl=64 time=0.365 ms
64 bytes from ansible-node3 (192.168.56.123): icmp_seq=2 ttl=64 time=0.231 ms
64 bytes from ansible-node3 (192.168.56.123): icmp_seq=3 ttl=64 time=0.221 ms

--- ansible-node3 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 1999ms
rtt min/avg/max/mdev = 0.221/0.272/0.365/0.067 ms
[root@ansible ~]#
```

可以看到ansible控制节点ping工作节点都是通的。



#### 1.2.2 配置免密登陆

```sh
# 生成公钥密钥对
[root@ansible ~]# ssh-keygen -C root@ansible-master
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Created directory '/root/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:xMkiAG8KJwhci2Px4ciQC4iqe66I5K6eLiuO0YVIUg0 root@ansible-master
The key's randomart image is:
+---[RSA 2048]----+
|B+E=             |
|X+*.+  o .       |
|BO++. . =        |
|B*.. . o         |
|+ . .   S        |
|.. .             |
|.o.              |
|X.o              |
|/%.              |
+----[SHA256]-----+

# 复制公钥到工作节点ansible-node1
[root@ansible ~]# ssh-copy-id root@ansible-node1
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
The authenticity of host 'ansible-node1 (192.168.56.121)' can't be established.
ECDSA key fingerprint is SHA256:6VBjwTbMeqBgqM3TO5lkK3LmtloB1lOtw5QXNVhzQkM.
ECDSA key fingerprint is MD5:8f:3d:0c:74:c4:01:2f:f3:5e:51:13:73:d2:80:98:68.
Are you sure you want to continue connecting (yes/no)? yes
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@ansible-node1's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@ansible-node1'"
and check to make sure that only the key(s) you wanted were added.

# 复制公钥到工作节点ansible-node2
[root@ansible ~]# ssh-copy-id root@ansible-node2
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
The authenticity of host 'ansible-node2 (192.168.56.122)' can't be established.
ECDSA key fingerprint is SHA256:6VBjwTbMeqBgqM3TO5lkK3LmtloB1lOtw5QXNVhzQkM.
ECDSA key fingerprint is MD5:8f:3d:0c:74:c4:01:2f:f3:5e:51:13:73:d2:80:98:68.
Are you sure you want to continue connecting (yes/no)? yes
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@ansible-node2's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@ansible-node2'"
and check to make sure that only the key(s) you wanted were added.

# 复制公钥到工作节点ansible-node3
[root@ansible ~]# ssh-copy-id root@ansible-node3
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
The authenticity of host 'ansible-node3 (192.168.56.123)' can't be established.
ECDSA key fingerprint is SHA256:6VBjwTbMeqBgqM3TO5lkK3LmtloB1lOtw5QXNVhzQkM.
ECDSA key fingerprint is MD5:8f:3d:0c:74:c4:01:2f:f3:5e:51:13:73:d2:80:98:68.
Are you sure you want to continue connecting (yes/no)? yes
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@ansible-node3's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@ansible-node3'"
and check to make sure that only the key(s) you wanted were added.

[root@ansible ~]#
```

测试免密登陆：

```sh
[root@ansible ~]# ssh root@ansible-node1
Last login: Fri Dec  1 23:23:16 2023 from 192.168.56.1
[root@localhost ~]# hostname -I
192.168.56.121 10.0.3.15
[root@localhost ~]# exit
logout
Connection to ansible-node1 closed.
[root@ansible ~]# ssh root@ansible-node2
Last login: Fri Dec  1 23:23:32 2023 from 192.168.56.1
[root@localhost ~]# hostname -I
192.168.56.122 10.0.3.15
[root@localhost ~]# exit
logout
Connection to ansible-node2 closed.
[root@ansible ~]# ssh root@ansible-node3
Last login: Fri Dec  1 23:24:07 2023 from 192.168.56.1
[root@localhost ~]# hostname -I
192.168.56.123 10.0.3.15
[root@localhost ~]# exit
logout
Connection to ansible-node3 closed.
[root@ansible ~]#
```

可以看到ansible控制节点可以直接登陆到三个工作节点，说明免密登陆配置成功。



#### 1.2.3 查看ansible版本信息

```sh
[root@ansible ~]# ansible --version
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/root/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Oct 14 2020, 14:45:30) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
[root@ansible ~]#
```



## 2. 实际使用的角色

此节我计划编写一个可以实际使用的角色，命名为`base`角色。该角色包含以下功能：

- 设置主机名称。
- 永久关闭SELINUX。
- 添加`yum`、`epel`源，用来加速软件安装。
- 配置pip国内镜像加速。
- 安装vim、telnet、python3、ntpdate、java、wget、lrzsz、dos2unix、git等基础包。
- 安装`safe-rm`和`trash-cli`防误删工具。
- 设置时间同步定时任务。
- 生成主机公钥私钥对。
- 设置常用快捷命令。

### 2.1 角色目录结构

最开始我们的角色目录结构比较简单，仅创建`base`目录，然后创建`tasks`目录，再在`tasks`目录下面创建`main.yml`任务文件，目录结构如下：

```sh
$ tree
.
+--- base
|   +--- tasks
|   |   +--- main.yml
```

目录结构和任务文件创建完成后，我们就开始进行任务分解，构建自己的自动化任务。



### 2.2 设置主机名称

可以参考：[hostname主机名模块](./hostname.md)

我们首先配置一个自己的主机清单`base_hosts.ini`:

```yaml
[basehosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3
```

然后，在`main.yml`文件中配置任务：

```yaml
---
- name: Show hostname
  ansible.builtin.debug:
    msg: "{{ hostname }}"

- name: Set hostname
  ansible.builtin.hostname:
    name: "{{ hostname }}"

```

### 2.3 创建角色入口剧本

在`roles`同级目录下，创建`base.yml`剧本，用来调用role角色。



`base.yml`剧本内容如下：

```yaml
---
- hosts: basehosts
  roles:
    - base

```



以上文件创建完成后，目录结构如下：

```sh
[root@ansible ansible_playbooks]# pwd
/root/ansible_playbooks
[root@ansible ansible_playbooks]# tree
.
├── base_hosts.ini
├── base.yml
└── roles
    └── base
        └── tasks
            └── main.yml

3 directories, 3 files
[root@ansible ansible_playbooks]#
```



查看节点是否能连通：

```sh
[root@ansible ansible_playbooks]# ansible -i base_hosts.ini  basehosts -m ping
192.168.56.123 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
192.168.56.122 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
192.168.56.121 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[root@ansible ansible_playbooks]#
```





### 2.4 执行剧本

在正式执行剧本前，可以使用`-C`参数检查一下剧本是否能够正常执行：

```sh
# 此处使用-i base_hosts.ini,表示使用base_hosts.ini配置文件作为主机清单
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -C

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [base : Show hostname] ******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "ansible-node1"
}
ok: [192.168.56.122] => {
    "msg": "ansible-node2"
}
ok: [192.168.56.123] => {
    "msg": "ansible-node3"
}

TASK [base : Set hostname] *******************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122]
changed: [192.168.56.121]
changed: [192.168.56.123]

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]# 
```

可以看到，可以执行。



实际执行下：

```sh

[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Show hostname] ******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "ansible-node1"
}
ok: [192.168.56.122] => {
    "msg": "ansible-node2"
}
ok: [192.168.56.123] => {
    "msg": "ansible-node3"
}

TASK [base : Set hostname] *******************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node2", "ansible_hostname": "ansible-node2", "ansible_nodename": "ansible-node2"}, "changed": true, "name": "ansible-node2"}
changed: [192.168.56.121] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node1", "ansible_hostname": "ansible-node1", "ansible_nodename": "ansible-node1"}, "changed": true, "name": "ansible-node1"}
changed: [192.168.56.123] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node3", "ansible_hostname": "ansible-node3", "ansible_nodename": "ansible-node3"}, "changed": true, "name": "ansible-node3"}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

可以看到，执行成功。



效果图：

![](/img/Snipaste_2023-12-24_15-44-01.png)



我们登陆三个节点主机查看一下：

```sh
[root@ansible ansible_playbooks]# ssh root@ansible-node1
Last login: Sun Dec 24 15:42:58 2023 from 192.168.56.120
[root@ansible-node1 ~]# hostname
ansible-node1
[root@ansible-node1 ~]# exit
logout
Connection to ansible-node1 closed.
[root@ansible ansible_playbooks]# ssh root@ansible-node2
Last login: Sun Dec 24 15:42:58 2023 from 192.168.56.120
[root@ansible-node2 ~]# hostname
ansible-node2
[root@ansible-node2 ~]# exit
logout
Connection to ansible-node2 closed.
[root@ansible ansible_playbooks]# ssh root@ansible-node3
Last login: Sun Dec 24 15:42:59 2023 from 192.168.56.120
[root@ansible-node3 ~]# hostname
ansible-node3
[root@ansible-node3 ~]# exit
logout
Connection to ansible-node3 closed.
[root@ansible ansible_playbooks]#
```

可以看到，三个节点的主机名称已经正常修改了。



### 2.5 扩展角色功能-关闭SELINUX

参考[4.1 SELINUX开启与关闭](./lineinfile.md) 增加关闭SELINUX的角色任务。



更新`main.yml`文件中配置任务：

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
```



执行前检查一下：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -C

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [base : Show hostname] ******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {
    "msg": "ansible-node3"
}
ok: [192.168.56.122] => {
    "msg": "ansible-node2"
}
ok: [192.168.56.121] => {
    "msg": "ansible-node1"
}

TASK [base : Set hostname] *******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.121]
ok: [192.168.56.123]

TASK [base : Set SELinux prints warnings instead of enforcing] *******************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.123]
skipping: [192.168.56.121]
skipping: [192.168.56.122]

TASK [base : Ensure SELinux is set to disable mode] ******************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123]
changed: [192.168.56.121]
changed: [192.168.56.122]

TASK [base : Get SELinux value] **************************************************************************************************************************************************************************************************************************************************************
skipping: [192.168.56.121]
skipping: [192.168.56.122]
skipping: [192.168.56.123]

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=4    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
192.168.56.122             : ok=4    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
192.168.56.123             : ok=4    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

可以看到，没有异常。

我们正式执行一下：

```sh

[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [base : Show hostname] ******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "ansible-node1"
}
ok: [192.168.56.122] => {
    "msg": "ansible-node2"
}
ok: [192.168.56.123] => {
    "msg": "ansible-node3"
}

TASK [base : Set hostname] *******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node3", "ansible_hostname": "ansible-node3", "ansible_nodename": "ansible-node3"}, "changed": false, "name": "ansible-node3"}
ok: [192.168.56.121] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node1", "ansible_hostname": "ansible-node1", "ansible_nodename": "ansible-node1"}, "changed": false, "name": "ansible-node1"}
ok: [192.168.56.122] => {"ansible_facts": {"ansible_domain": "", "ansible_fqdn": "ansible-node2", "ansible_hostname": "ansible-node2", "ansible_nodename": "ansible-node2"}, "changed": false, "name": "ansible-node2"}

TASK [base : Set SELinux prints warnings instead of enforcing] *******************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "cmd": ["setenforce", "0"], "delta": "0:00:00.002485", "end": "2024-01-01 09:40:33.145390", "rc": 0, "start": "2024-01-01 09:40:33.142905", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
changed: [192.168.56.122] => {"changed": true, "cmd": ["setenforce", "0"], "delta": "0:00:00.002721", "end": "2024-01-01 09:40:33.125002", "rc": 0, "start": "2024-01-01 09:40:33.122281", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
changed: [192.168.56.123] => {"changed": true, "cmd": ["setenforce", "0"], "delta": "0:00:00.002572", "end": "2024-01-01 09:40:32.773242", "rc": 0, "start": "2024-01-01 09:40:32.770670", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

TASK [base : Ensure SELinux is set to disable mode] ******************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123] => {"backup": "", "changed": false, "msg": ""}
ok: [192.168.56.121] => {"backup": "", "changed": false, "msg": ""}
ok: [192.168.56.122] => {"backup": "", "changed": false, "msg": ""}

TASK [base : Get SELinux value] **************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "cmd": ["getenforce"], "delta": "0:00:00.001958", "end": "2024-01-01 09:40:33.828562", "rc": 0, "start": "2024-01-01 09:40:33.826604", "stderr": "", "stderr_lines": [], "stdout": "Permissive", "stdout_lines": ["Permissive"]}
changed: [192.168.56.122] => {"changed": true, "cmd": ["getenforce"], "delta": "0:00:00.002160", "end": "2024-01-01 09:40:33.823896", "rc": 0, "start": "2024-01-01 09:40:33.821736", "stderr": "", "stderr_lines": [], "stdout": "Permissive", "stdout_lines": ["Permissive"]}
changed: [192.168.56.123] => {"changed": true, "cmd": ["getenforce"], "delta": "0:00:00.002604", "end": "2024-01-01 09:40:33.475934", "rc": 0, "start": "2024-01-01 09:40:33.473330", "stderr": "", "stderr_lines": [], "stdout": "Permissive", "stdout_lines": ["Permissive"]}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```



登陆3个节点检查一下：

```sh
[root@ansible ~]# ssh root@ansible-node1
Last login: Mon Jan  1 09:40:33 2024 from 192.168.56.120
[root@ansible-node1 ~]# getenforce
Permissive
[root@ansible-node1 ~]# cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted


[root@ansible-node1 ~]# exit
logout
Connection to ansible-node1 closed.
[root@ansible ~]# ssh root@ansible-node2
Last login: Mon Jan  1 09:40:33 2024 from 192.168.56.120
[root@ansible-node2 ~]# getenforce
Permissive
[root@ansible-node2 ~]# cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted


[root@ansible-node2 ~]# exit
logout
Connection to ansible-node2 closed.
[root@ansible ~]# ssh root@ansible-node3
Last login: Mon Jan  1 09:40:33 2024 from 192.168.56.120
[root@ansible-node3 ~]# getenforce
Permissive
[root@ansible-node3 ~]# cat /etc/selinux/config

# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#     enforcing - SELinux security policy is enforced.
#     permissive - SELinux prints warnings instead of enforcing.
#     disabled - No SELinux policy is loaded.
SELINUX=disabled
# SELINUXTYPE= can take one of three values:
#     targeted - Targeted processes are protected,
#     minimum - Modification of targeted policy. Only selected processes are protected.
#     mls - Multi Level Security protection.
SELINUXTYPE=targeted


[root@ansible-node3 ~]#
```

可以看到，状态已经是`SELINUX=disabled`了，说明配置成功。



### 2.6 扩展角色功能-增加镜像源



本节主要完成以下事项：

- 添加`yum`、`epel`源，用来加速软件安装。
- 配置pip国内镜像加速。

通过配置阿里云的镜像代理来加速。

参考：

- [CentOS 镜像](https://developer.aliyun.com/mirror/centos?spm=a2c6h.13651102.0.0.4e1d1b11ZjPg1b)
- [Epel 镜像](https://developer.aliyun.com/mirror/epel?spm=a2c6h.13651102.0.0.4e1d1b11ZjPg1b)
- [PyPI 镜像](https://developer.aliyun.com/mirror/pypi?spm=a2c6h.13651102.0.0.23121b11KPKUmC)

为了观察新配置的角色任务的使用，可以将之前测试好的任务注释掉。

先在以上三个参考链接中下载yum、epel源配置文件，并创建`pip.conf`配置文件，在`tasks`同级目录创建`files`目录，并将刚下载或创建的文件放在这个目录下：

```sh
$ tree
.
+--- files
|   +--- Centos-7.repo
|   +--- epel-7.repo
|   +--- pip.conf
+--- tasks
|   +--- main.yml

```



`Centos-7.repo`配置文件内容如下：

```
# CentOS-Base.repo
#
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the 
# remarked out baseurl= line instead.
#
#
 
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/os/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#released updates 
[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/updates/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/extras/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/extras/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/extras/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/centosplus/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/centosplus/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/centosplus/$basearch/
gpgcheck=1
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
 
#contrib - packages by Centos Users
[contrib]
name=CentOS-$releasever - Contrib - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/contrib/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/contrib/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/contrib/$basearch/
gpgcheck=1
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7

```



`epel-7.repo`配置文件内容如下：

```
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
baseurl=http://mirrors.aliyun.com/epel/7/$basearch
failovermethod=priority
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
 
[epel-debuginfo]
name=Extra Packages for Enterprise Linux 7 - $basearch - Debug
baseurl=http://mirrors.aliyun.com/epel/7/$basearch/debug
failovermethod=priority
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
gpgcheck=0
 
[epel-source]
name=Extra Packages for Enterprise Linux 7 - $basearch - Source
baseurl=http://mirrors.aliyun.com/epel/7/SRPMS
failovermethod=priority
enabled=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
gpgcheck=0

```



`pip.conf`配置文件内容如下：

```
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com

```

配置角色任务，可参考：

- [copy复制模块](./copy.md)
- [file文件模块](./file.md)

修改后的角色任务文件内容如下：

```yaml
---
# - name: Show hostname
#   ansible.builtin.debug:
#     msg: "{{ hostname }}"

# - name: Set hostname
#   ansible.builtin.hostname:
#     name: "{{ ansible_hostname }}"

# - name: Set SELinux prints warnings instead of enforcing
#   ansible.builtin.command:
#     cmd: setenforce 0

# - name: Ensure SELinux is set to disable mode
#   ansible.builtin.lineinfile:
#     path: /etc/selinux/config
#     regexp: '^SELINUX='
#     line: SELINUX=disabled

# - name: Get SELinux value
#   ansible.builtin.command:
#     cmd: getenforce

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

```



使用`ansible-lint`检查一下脚本语法，然后再测试执行一下剧本：

```sh
[root@ansible ansible_playbooks]# ansible-lint roles/base/tasks/main.yml
```

可以看到，没有报错。



再正式执行一下：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [base : Create a directory if it does not exist] ****************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/root/.pip", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/root/.pip", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/root/.pip", "size": 6, "state": "directory", "uid": 0}

TASK [base : Create backup directory] ********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/etc/yum.repos.d.bak", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/etc/yum.repos.d.bak", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/etc/yum.repos.d.bak", "size": 6, "state": "directory", "uid": 0}

TASK [base : Backup old repo config] *********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Base.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Base.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "ff3d54c17cc2160701adee0d5496a30354f43140", "dest": "/etc/yum.repos.d.bak/CentOS-Base.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Base.repo.bak", "src": "/etc/yum.repos.d/CentOS-Base.repo"}, "md5sum": "9098fc723b1e00c92e8515f06980d83e", "mode": "0644", "owner": "root", "size": 1664, "src": "/etc/yum.repos.d/CentOS-Base.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Base.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Base.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "ff3d54c17cc2160701adee0d5496a30354f43140", "dest": "/etc/yum.repos.d.bak/CentOS-Base.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Base.repo.bak", "src": "/etc/yum.repos.d/CentOS-Base.repo"}, "md5sum": "9098fc723b1e00c92e8515f06980d83e", "mode": "0644", "owner": "root", "size": 1664, "src": "/etc/yum.repos.d/CentOS-Base.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Base.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Base.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "ff3d54c17cc2160701adee0d5496a30354f43140", "dest": "/etc/yum.repos.d.bak/CentOS-Base.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Base.repo.bak", "src": "/etc/yum.repos.d/CentOS-Base.repo"}, "md5sum": "9098fc723b1e00c92e8515f06980d83e", "mode": "0644", "owner": "root", "size": 1664, "src": "/etc/yum.repos.d/CentOS-Base.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-CR.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-CR.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "0f7434927f6953571e4a7e1f740753cade7b1f0a", "dest": "/etc/yum.repos.d.bak/CentOS-CR.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-CR.repo.bak", "src": "/etc/yum.repos.d/CentOS-CR.repo"}, "md5sum": "445ed4f0ee3888384e854fb8527a7cde", "mode": "0644", "owner": "root", "size": 1309, "src": "/etc/yum.repos.d/CentOS-CR.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-CR.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-CR.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "0f7434927f6953571e4a7e1f740753cade7b1f0a", "dest": "/etc/yum.repos.d.bak/CentOS-CR.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-CR.repo.bak", "src": "/etc/yum.repos.d/CentOS-CR.repo"}, "md5sum": "445ed4f0ee3888384e854fb8527a7cde", "mode": "0644", "owner": "root", "size": 1309, "src": "/etc/yum.repos.d/CentOS-CR.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-CR.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-CR.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "0f7434927f6953571e4a7e1f740753cade7b1f0a", "dest": "/etc/yum.repos.d.bak/CentOS-CR.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-CR.repo.bak", "src": "/etc/yum.repos.d/CentOS-CR.repo"}, "md5sum": "445ed4f0ee3888384e854fb8527a7cde", "mode": "0644", "owner": "root", "size": 1309, "src": "/etc/yum.repos.d/CentOS-CR.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Debuginfo.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "7d2238466c9cfcaa93ae5cdff96134a243b2622b", "dest": "/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak", "src": "/etc/yum.repos.d/CentOS-Debuginfo.repo"}, "md5sum": "e9e506425094f43b5c8f053090dbf4d4", "mode": "0644", "owner": "root", "size": 649, "src": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Debuginfo.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "7d2238466c9cfcaa93ae5cdff96134a243b2622b", "dest": "/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak", "src": "/etc/yum.repos.d/CentOS-Debuginfo.repo"}, "md5sum": "e9e506425094f43b5c8f053090dbf4d4", "mode": "0644", "owner": "root", "size": 649, "src": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Debuginfo.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "7d2238466c9cfcaa93ae5cdff96134a243b2622b", "dest": "/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Debuginfo.repo.bak", "src": "/etc/yum.repos.d/CentOS-Debuginfo.repo"}, "md5sum": "e9e506425094f43b5c8f053090dbf4d4", "mode": "0644", "owner": "root", "size": 649, "src": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-fasttrack.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "c825013c88fb69ba0e2de74dc0cf9571b0e4f439", "dest": "/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak", "src": "/etc/yum.repos.d/CentOS-fasttrack.repo"}, "md5sum": "52d296f7a45f56c85d18473eca5bab16", "mode": "0644", "owner": "root", "size": 314, "src": "/etc/yum.repos.d/CentOS-fasttrack.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-fasttrack.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "c825013c88fb69ba0e2de74dc0cf9571b0e4f439", "dest": "/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak", "src": "/etc/yum.repos.d/CentOS-fasttrack.repo"}, "md5sum": "52d296f7a45f56c85d18473eca5bab16", "mode": "0644", "owner": "root", "size": 314, "src": "/etc/yum.repos.d/CentOS-fasttrack.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-fasttrack.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "c825013c88fb69ba0e2de74dc0cf9571b0e4f439", "dest": "/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-fasttrack.repo.bak", "src": "/etc/yum.repos.d/CentOS-fasttrack.repo"}, "md5sum": "52d296f7a45f56c85d18473eca5bab16", "mode": "0644", "owner": "root", "size": 314, "src": "/etc/yum.repos.d/CentOS-fasttrack.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Media.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Media.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "36e85d82f14541b3e2ad91472d990ea1f283b92f", "dest": "/etc/yum.repos.d.bak/CentOS-Media.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Media.repo.bak", "src": "/etc/yum.repos.d/CentOS-Media.repo"}, "md5sum": "1d7797c5082bd565facd68c5aa9352bf", "mode": "0644", "owner": "root", "size": 630, "src": "/etc/yum.repos.d/CentOS-Media.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Media.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Media.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "36e85d82f14541b3e2ad91472d990ea1f283b92f", "dest": "/etc/yum.repos.d.bak/CentOS-Media.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Media.repo.bak", "src": "/etc/yum.repos.d/CentOS-Media.repo"}, "md5sum": "1d7797c5082bd565facd68c5aa9352bf", "mode": "0644", "owner": "root", "size": 630, "src": "/etc/yum.repos.d/CentOS-Media.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Media.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Media.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "36e85d82f14541b3e2ad91472d990ea1f283b92f", "dest": "/etc/yum.repos.d.bak/CentOS-Media.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Media.repo.bak", "src": "/etc/yum.repos.d/CentOS-Media.repo"}, "md5sum": "1d7797c5082bd565facd68c5aa9352bf", "mode": "0644", "owner": "root", "size": 630, "src": "/etc/yum.repos.d/CentOS-Media.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Sources.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Sources.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "41f485329fec1d549c091af89122d293aeb3434b", "dest": "/etc/yum.repos.d.bak/CentOS-Sources.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Sources.repo.bak", "src": "/etc/yum.repos.d/CentOS-Sources.repo"}, "md5sum": "04d662bb1648477bf50e658a20c10145", "mode": "0644", "owner": "root", "size": 1331, "src": "/etc/yum.repos.d/CentOS-Sources.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Sources.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Sources.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "41f485329fec1d549c091af89122d293aeb3434b", "dest": "/etc/yum.repos.d.bak/CentOS-Sources.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Sources.repo.bak", "src": "/etc/yum.repos.d/CentOS-Sources.repo"}, "md5sum": "04d662bb1648477bf50e658a20c10145", "mode": "0644", "owner": "root", "size": 1331, "src": "/etc/yum.repos.d/CentOS-Sources.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Sources.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Sources.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "41f485329fec1d549c091af89122d293aeb3434b", "dest": "/etc/yum.repos.d.bak/CentOS-Sources.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Sources.repo.bak", "src": "/etc/yum.repos.d/CentOS-Sources.repo"}, "md5sum": "04d662bb1648477bf50e658a20c10145", "mode": "0644", "owner": "root", "size": 1331, "src": "/etc/yum.repos.d/CentOS-Sources.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Vault.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Vault.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "09e0a5ee36b6cba4685053c234c631e9d35eb536", "dest": "/etc/yum.repos.d.bak/CentOS-Vault.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Vault.repo.bak", "src": "/etc/yum.repos.d/CentOS-Vault.repo"}, "md5sum": "0ac7166ad220b05729b92851ab4db923", "mode": "0644", "owner": "root", "size": 8515, "src": "/etc/yum.repos.d/CentOS-Vault.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Vault.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Vault.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "09e0a5ee36b6cba4685053c234c631e9d35eb536", "dest": "/etc/yum.repos.d.bak/CentOS-Vault.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Vault.repo.bak", "src": "/etc/yum.repos.d/CentOS-Vault.repo"}, "md5sum": "0ac7166ad220b05729b92851ab4db923", "mode": "0644", "owner": "root", "size": 8515, "src": "/etc/yum.repos.d/CentOS-Vault.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-Vault.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-Vault.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "09e0a5ee36b6cba4685053c234c631e9d35eb536", "dest": "/etc/yum.repos.d.bak/CentOS-Vault.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-Vault.repo.bak", "src": "/etc/yum.repos.d/CentOS-Vault.repo"}, "md5sum": "0ac7166ad220b05729b92851ab4db923", "mode": "0644", "owner": "root", "size": 8515, "src": "/etc/yum.repos.d/CentOS-Vault.repo", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-x86_64-kernel.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "9b76bdcdc7375d5619914a07532a2a7e864513fe", "dest": "/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak", "src": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo"}, "md5sum": "f7b8db9259739ea6884df7ed056b0dc2", "mode": "0644", "owner": "root", "size": 616, "src": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-x86_64-kernel.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "9b76bdcdc7375d5619914a07532a2a7e864513fe", "dest": "/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak", "src": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo"}, "md5sum": "f7b8db9259739ea6884df7ed056b0dc2", "mode": "0644", "owner": "root", "size": 616, "src": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak', u'src': u'/etc/yum.repos.d/CentOS-x86_64-kernel.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "9b76bdcdc7375d5619914a07532a2a7e864513fe", "dest": "/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d.bak/CentOS-x86_64-kernel.repo.bak", "src": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo"}, "md5sum": "f7b8db9259739ea6884df7ed056b0dc2", "mode": "0644", "owner": "root", "size": 616, "src": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "state": "file", "uid": 0}

TASK [base : Remove old repo config] *********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-Base.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Base.repo", "path": "/etc/yum.repos.d/CentOS-Base.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-Base.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Base.repo", "path": "/etc/yum.repos.d/CentOS-Base.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-Base.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Base.repo", "path": "/etc/yum.repos.d/CentOS-Base.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-CR.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-CR.repo", "path": "/etc/yum.repos.d/CentOS-CR.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-CR.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-CR.repo", "path": "/etc/yum.repos.d/CentOS-CR.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-CR.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-CR.repo", "path": "/etc/yum.repos.d/CentOS-CR.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-Debuginfo.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "path": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-Debuginfo.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "path": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-Debuginfo.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "path": "/etc/yum.repos.d/CentOS-Debuginfo.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-fasttrack.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-fasttrack.repo", "path": "/etc/yum.repos.d/CentOS-fasttrack.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-fasttrack.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-fasttrack.repo", "path": "/etc/yum.repos.d/CentOS-fasttrack.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-fasttrack.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-fasttrack.repo", "path": "/etc/yum.repos.d/CentOS-fasttrack.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-Media.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Media.repo", "path": "/etc/yum.repos.d/CentOS-Media.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-Media.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Media.repo", "path": "/etc/yum.repos.d/CentOS-Media.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-Media.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Media.repo", "path": "/etc/yum.repos.d/CentOS-Media.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-Sources.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Sources.repo", "path": "/etc/yum.repos.d/CentOS-Sources.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-Sources.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Sources.repo", "path": "/etc/yum.repos.d/CentOS-Sources.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-Sources.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Sources.repo", "path": "/etc/yum.repos.d/CentOS-Sources.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-Vault.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Vault.repo", "path": "/etc/yum.repos.d/CentOS-Vault.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-Vault.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Vault.repo", "path": "/etc/yum.repos.d/CentOS-Vault.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-Vault.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-Vault.repo", "path": "/etc/yum.repos.d/CentOS-Vault.repo", "state": "absent"}
changed: [192.168.56.121] => (item=/etc/yum.repos.d/CentOS-x86_64-kernel.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "path": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "state": "absent"}
changed: [192.168.56.122] => (item=/etc/yum.repos.d/CentOS-x86_64-kernel.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "path": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "state": "absent"}
changed: [192.168.56.123] => (item=/etc/yum.repos.d/CentOS-x86_64-kernel.repo) => {"ansible_loop_var": "item", "changed": true, "item": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "path": "/etc/yum.repos.d/CentOS-x86_64-kernel.repo", "state": "absent"}

TASK [base : Copy repo and pypi config] ******************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d/Centos-7.repo', u'src': u'Centos-7.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "a149656624ecdf9c5549bf419925b1d8adddefb6", "dest": "/etc/yum.repos.d/Centos-7.repo", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d/Centos-7.repo", "src": "Centos-7.repo"}, "md5sum": "13151789a512213f1695a5b427b1a9ab", "mode": "0644", "owner": "root", "size": 2523, "src": "/root/.ansible/tmp/ansible-tmp-1704294124.48-3771-173675379220764/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d/Centos-7.repo', u'src': u'Centos-7.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "a149656624ecdf9c5549bf419925b1d8adddefb6", "dest": "/etc/yum.repos.d/Centos-7.repo", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d/Centos-7.repo", "src": "Centos-7.repo"}, "md5sum": "13151789a512213f1695a5b427b1a9ab", "mode": "0644", "owner": "root", "size": 2523, "src": "/root/.ansible/tmp/ansible-tmp-1704294124.5-3773-272508890716078/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d/Centos-7.repo', u'src': u'Centos-7.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "a149656624ecdf9c5549bf419925b1d8adddefb6", "dest": "/etc/yum.repos.d/Centos-7.repo", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d/Centos-7.repo", "src": "Centos-7.repo"}, "md5sum": "13151789a512213f1695a5b427b1a9ab", "mode": "0644", "owner": "root", "size": 2523, "src": "/root/.ansible/tmp/ansible-tmp-1704294124.48-3770-152346814500884/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'/etc/yum.repos.d/epel-7.repo', u'src': u'epel-7.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "2feedd589b72617f03d75c4b8a6e328cc1aad918", "dest": "/etc/yum.repos.d/epel-7.repo", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d/epel-7.repo", "src": "epel-7.repo"}, "md5sum": "bddf35db56cf6be9190fdabeae71c801", "mode": "0644", "owner": "root", "size": 664, "src": "/root/.ansible/tmp/ansible-tmp-1704294125.09-3770-201519912889303/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'/etc/yum.repos.d/epel-7.repo', u'src': u'epel-7.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "2feedd589b72617f03d75c4b8a6e328cc1aad918", "dest": "/etc/yum.repos.d/epel-7.repo", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d/epel-7.repo", "src": "epel-7.repo"}, "md5sum": "bddf35db56cf6be9190fdabeae71c801", "mode": "0644", "owner": "root", "size": 664, "src": "/root/.ansible/tmp/ansible-tmp-1704294125.08-3771-243575225339221/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'/etc/yum.repos.d/epel-7.repo', u'src': u'epel-7.repo'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "2feedd589b72617f03d75c4b8a6e328cc1aad918", "dest": "/etc/yum.repos.d/epel-7.repo", "gid": 0, "group": "root", "item": {"dest": "/etc/yum.repos.d/epel-7.repo", "src": "epel-7.repo"}, "md5sum": "bddf35db56cf6be9190fdabeae71c801", "mode": "0644", "owner": "root", "size": 664, "src": "/root/.ansible/tmp/ansible-tmp-1704294125.09-3773-79967557975172/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => (item={u'dest': u'~/.pip/pip.conf', u'src': u'pip.conf'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "e4515437dc3f92bd78a28c116210fc268680f144", "dest": "/root/.pip/pip.conf", "gid": 0, "group": "root", "item": {"dest": "~/.pip/pip.conf", "src": "pip.conf"}, "md5sum": "7a937c6e137aa3ff4942008c377b07a4", "mode": "0644", "owner": "root", "size": 103, "src": "/root/.ansible/tmp/ansible-tmp-1704294125.52-3771-213666481087417/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => (item={u'dest': u'~/.pip/pip.conf', u'src': u'pip.conf'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "e4515437dc3f92bd78a28c116210fc268680f144", "dest": "/root/.pip/pip.conf", "gid": 0, "group": "root", "item": {"dest": "~/.pip/pip.conf", "src": "pip.conf"}, "md5sum": "7a937c6e137aa3ff4942008c377b07a4", "mode": "0644", "owner": "root", "size": 103, "src": "/root/.ansible/tmp/ansible-tmp-1704294125.52-3770-277075185068516/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => (item={u'dest': u'~/.pip/pip.conf', u'src': u'pip.conf'}) => {"ansible_loop_var": "item", "changed": true, "checksum": "e4515437dc3f92bd78a28c116210fc268680f144", "dest": "/root/.pip/pip.conf", "gid": 0, "group": "root", "item": {"dest": "~/.pip/pip.conf", "src": "pip.conf"}, "md5sum": "7a937c6e137aa3ff4942008c377b07a4", "mode": "0644", "owner": "root", "size": 103, "src": "/root/.ansible/tmp/ansible-tmp-1704294125.53-3773-17986140995035/source", "state": "file", "uid": 0}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```



登陆节点检查复制的配置文件：

```sh
[root@ansible ~]# ssh root@ansible-node1
Last login: Wed Jan  3 23:02:06 2024 from 192.168.56.120
[root@ansible-node1 ~]# ll /etc/yum.repos.d
total 8
-rw-r--r-- 1 root root 2523 Jan  3 23:02 Centos-7.repo
-rw-r--r-- 1 root root  664 Jan  3 23:02 epel-7.repo
[root@ansible-node1 ~]# ll .pip/
total 4
-rw-r--r-- 1 root root 103 Jan  3 23:02 pip.conf
[root@ansible-node1 ~]# cat .pip/pip.conf
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
[root@ansible-node1 ~]#
```

可以看到，节点1已经成功复制了配置文件。

相应的，在节点2和节点3上面进行检查。可以看到，都已经生效，说明Yum源和pip镜像加速配置文件配置成功了。



### 2.7 扩展角色功能-安装基础软件包

本节我们来安装vim、telnet、python3、ntpdate、java、wget、lrzsz、dos2unix、git等基础包。

- 注意，java包名使用`java-1.8.0-openjdk`。
- 安装`java-1.8.0-openjdk-devel`包后，可以使用`jps`查看Java进程和`jstack`查看线程堆栈信息。
- 软件包的安装可以参考[yum包管理器模块](./yum.md) 。

为了专注本节的任务，我们将`main.yml`备份一下，然后再对`main.yml`任务文件增加新的任务信息。

```sh
$ ls
main.yml
$ cp main.yml main.yml.bak
$ ls
main.yml      main.yml.bak
$
```



然后，更新`main.yml`文件内容：

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
    - dos2unix
    - git
    - java-1.8.0-openjdk
    - java-1.8.0-openjdk-devel
```

::: warning  警告

通过yum安装的python版本是Python 3.6.8，版本较低，官方已经不再支持该版本。因此，不建议安装该版本。

可以参考 [使用ansible配置supervisor进程管理角色](./role_5_supervisor.md) 安装高版本的Python。

:::

检查并执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-lint roles/base/tasks/main.yml
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -C

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.123]
ok: [192.168.56.122]

TASK [base : ensure a list of packages installed] ********************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121]
^C [ERROR]: User interrupted execution
[root@ansible ansible_playbooks]# ^C
[root@ansible ansible_playbooks]# ^C
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.122]
ok: [192.168.56.121]

TASK [base : ensure a list of packages installed] ********************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "changes": {"installed": ["vim", "telnet", "python3", "ntpdate", "java-1.8.0-openjdk"]}, "msg": "", "rc": 0, "results": ...
.... # 中间日志此处忽略
PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

可以看到，剧本执行成功。



在各节点检查一下。



检查node1节点：

```sh
[root@ansible-node1 ~]# rpm -qa|grep -E 'vim|telnet|python3|ntpdate|java'
tzdata-java-2023c-1.el7.noarch
python3-pip-9.0.3-8.el7.noarch
vim-common-7.4.629-8.el7_9.x86_64
telnet-0.17-66.el7.x86_64
python-javapackages-3.4.1-11.el7.noarch
vim-minimal-7.4.629-7.el7.x86_64
python3-libs-3.6.8-21.el7_9.x86_64
python3-setuptools-39.2.0-10.el7.noarch
vim-filesystem-7.4.629-8.el7_9.x86_64
java-1.8.0-openjdk-headless-1.8.0.392.b08-2.el7_9.x86_64
vim-enhanced-7.4.629-8.el7_9.x86_64
ntpdate-4.2.6p5-29.el7.centos.2.x86_64
javapackages-tools-3.4.1-11.el7.noarch
python3-3.6.8-21.el7_9.x86_64
java-1.8.0-openjdk-1.8.0.392.b08-2.el7_9.x86_64
[root@ansible-node1 ~]# python3 -V
Python 3.6.8
[root@ansible-node1 ~]# java -version
openjdk version "1.8.0_392"
OpenJDK Runtime Environment (build 1.8.0_392-b08)
OpenJDK 64-Bit Server VM (build 25.392-b08, mixed mode)
[root@ansible-node1 ~]# echo -e "\x1dclose\x0d"|telnet baidu.com 443
Trying 110.242.68.66...
Connected to baidu.com.
Escape character is '^]'.

telnet> close
Connection closed.
[root@ansible-node1 ~]# ntpdate ntp1.aliyun.com
 7 Jan 08:14:38 ntpdate[2075]: step time server 120.25.115.20 offset 2.178265 sec
[root@ansible-node1 ~]# date
Sun Jan  7 08:14:40 CST 2024
[root@ansible-node1 ~]#
```

如果你还想安装其他的软件包，直接在`- java-1.8.0-openjdk-devel`后面添加新的行即可。



在node2和node3节点也进行相应检查，可以看到相关包已经安装成功了。



### 2.8 扩展角色功能-安装safe-rm和trash-cli防误删工具

本节主要想做的事情是给服务器安装safe-rm和trash-cli防误删工具，避免执行`rm`误删文件。

- 手动安装配置，详细可参考：[防止`rm -rf /`误删除的方法](../../OS/Centos/X_forbit_use_rm_to_delete_root_path.md)
- `safe-rm`项目官网 [https://repo.or.cz/w/safe-rm.git](https://repo.or.cz/w/safe-rm.git)
- `trash-cli`项目官网 [https://github.com/andreafrancia/trash-cli](https://github.com/andreafrancia/trash-cli)



待办事项分析：

- 从[https://launchpad.net/safe-rm/trunk/0.12/+download/safe-rm-0.12.tar.gz](https://launchpad.net/safe-rm/trunk/0.12/+download/safe-rm-0.12.tar.gz) 下载`safe-rm`的源文件。
- 解压压缩包。详细可参考[unarchive模块](./unarchive.md)
- 将解压出来的`safe-rm`文件复制到`/usr/bin`目录下。
- 给`/usr/bin/safe-rm`增加可执行权限。
- 配置`/etc/safe-rm.conf`文件。
- pip3安装`trash-cli`命令，注意，`pip3`命令依赖上一节安装的python3，如果你没有安装python3，请参考上一节。详细可参考[pip模块-管理python库依赖](./pip.md) 。



 当我们不确定执行的剧本编写是否正确时， 可以使用ad-hoc命令来检查模块的使用：

```sh
# 验证解压
[root@ansible ansible_playbooks]# ansible -i base_hosts.ini 192.168.56.121 -m unarchive -a "src=roles/base/files/safe-rm-0.12.tar.gz dest=/srv/safe-rm"
192.168.56.121 | FAILED! => {
    "changed": false,
    "msg": "dest '/srv/safe-rm' must be an existing dir"
}

# 创建目录后，再验证解压并设置权限
[root@ansible ansible_playbooks]# ansible -i base_hosts.ini 192.168.56.121 -m unarchive -a "src=roles/base/files/safe-rm-0.12.tar.gz dest=/srv/safe-rm owner=root group=root"
192.168.56.121 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "dest": "/srv/safe-rm",
    "extract_results": {
        "cmd": [
            "/usr/bin/gtar",
            "--extract",
            "-C",
            "/srv/safe-rm",
            "-z",
            "--owner=root",
            "--group=root",
            "-f",
            "/root/.ansible/tmp/ansible-tmp-1704591244.4-2381-218435202826390/source"
        ],
        "err": "",
        "out": "",
        "rc": 0
    },
    "gid": 0,
    "group": "root",
    "handler": "TgzArchive",
    "mode": "0755",
    "owner": "root",
    "size": 26,
    "src": "/root/.ansible/tmp/ansible-tmp-1704591244.4-2381-218435202826390/source",
    "state": "directory",
    "uid": 0
}

# 验证文件复制
[root@ansible ansible_playbooks]# ansible -i base_hosts.ini  192.168.56.121 -m copy -a "src=/srv/safe-rm/safe-rm-0.12/safe-rm dest=/usr/bin/safe-rm remote_src=yes mode=0755"
192.168.56.121 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "checksum": "9057a05112cb819be85f931ca7ca43995f641383",
    "dest": "/usr/bin/safe-rm",
    "gid": 0,
    "group": "root",
    "md5sum": "6f53dda881c4644a816d4e33a1045672",
    "mode": "0755",
    "owner": "root",
    "size": 6179,
    "src": "/srv/safe-rm/safe-rm-0.12/safe-rm",
    "state": "file",
    "uid": 0
}
[root@ansible ansible_playbooks]#
```



将下载好的`afe-rm-0.12.tar.gz`压缩包和配置文件`safe-rm.conf`放到`files`文件夹中：

```sh
[root@ansible ansible_playbooks]# ll roles/base/files/
total 32
-rw-r--r--. 1 root root  2523 Jan  3 07:01 Centos-7.repo
-rw-r--r--. 1 root root   664 Jan  3 07:01 epel-7.repo
-rw-r--r--. 1 root root   103 Jan  3 07:01 pip.conf
-rw-r--r--. 1 root root 16371 Jan  7 09:23 safe-rm-0.12.tar.gz
-rw-r--r--. 1 root root   264 Jan  7 09:23 safe-rm.conf
[root@ansible ansible_playbooks]# cat roles/base/files/safe-rm.conf
/
/bin
/boot
/dev
/etc
/home
/initrd
/lib
/lib64
/proc
/root
/sbin
/srv
/sys
/usr
/usr/bin
/usr/etc
/usr/include
/usr/lib
/usr/lib64
/usr/local
/usr/local/bin
/usr/local/include
/usr/local/sbin
/usr/local/share
/usr/sbin
/usr/share
/usr/src
/var
/etc/safe-rm.conf
[root@ansible ansible_playbooks]#
```



解决pip安装异常后的，任务配置如下：

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



检查剧本文件，并执行：

```sh
# 检查剧本文件语法
[root@ansible ansible_playbooks]# ansible-lint roles/base/tasks/main.yml

# 执行
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.123]
ok: [192.168.56.122]

TASK [create base folder] ********************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/srv/safe-rm", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/srv/safe-rm", "size": 6, "state": "directory", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "gid": 0, "group": "root", "mode": "0755", "owner": "root", "path": "/srv/safe-rm", "size": 6, "state": "directory", "uid": 0}

TASK [base : Extract safe-rm-0.12.tar.gz into /srv/safe-rm] **********************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "dest": "/srv/safe-rm", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv/safe-rm", "-z", "--owner=root", "--group=root", "-f", "/root/.ansible/tmp/ansible-tmp-1704631387.42-2740-78789438582595/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 26, "src": "/root/.ansible/tmp/ansible-tmp-1704631387.42-2740-78789438582595/source", "state": "directory", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "dest": "/srv/safe-rm", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv/safe-rm", "-z", "--owner=root", "--group=root", "-f", "/root/.ansible/tmp/ansible-tmp-1704631387.38-2735-75722127108714/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 26, "src": "/root/.ansible/tmp/ansible-tmp-1704631387.38-2735-75722127108714/source", "state": "directory", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "dest": "/srv/safe-rm", "extract_results": {"cmd": ["/usr/bin/gtar", "--extract", "-C", "/srv/safe-rm", "-z", "--owner=root", "--group=root", "-f", "/root/.ansible/tmp/ansible-tmp-1704631387.4-2737-135516895851295/source"], "err": "", "out": "", "rc": 0}, "gid": 0, "group": "root", "handler": "TgzArchive", "mode": "0755", "owner": "root", "size": 26, "src": "/root/.ansible/tmp/ansible-tmp-1704631387.4-2737-135516895851295/source", "state": "directory", "uid": 0}

TASK [base : Move safe-rm to /usr/bin] *******************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "9057a05112cb819be85f931ca7ca43995f641383", "dest": "/usr/bin/safe-rm", "gid": 0, "group": "root", "md5sum": "6f53dda881c4644a816d4e33a1045672", "mode": "0755", "owner": "root", "size": 6179, "src": "/srv/safe-rm/safe-rm-0.12/safe-rm", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "checksum": "9057a05112cb819be85f931ca7ca43995f641383", "dest": "/usr/bin/safe-rm", "gid": 0, "group": "root", "md5sum": "6f53dda881c4644a816d4e33a1045672", "mode": "0755", "owner": "root", "size": 6179, "src": "/srv/safe-rm/safe-rm-0.12/safe-rm", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "9057a05112cb819be85f931ca7ca43995f641383", "dest": "/usr/bin/safe-rm", "gid": 0, "group": "root", "md5sum": "6f53dda881c4644a816d4e33a1045672", "mode": "0755", "owner": "root", "size": 6179, "src": "/srv/safe-rm/safe-rm-0.12/safe-rm", "state": "file", "uid": 0}

TASK [base : Delete temp folder] *************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "path": "/srv/safe-rm", "state": "absent"}
changed: [192.168.56.122] => {"changed": true, "path": "/srv/safe-rm", "state": "absent"}
changed: [192.168.56.123] => {"changed": true, "path": "/srv/safe-rm", "state": "absent"}

TASK [base : Copy safe-rm config] ************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "checksum": "5468767a35430d62381d20a6c5f4a62413af9746", "dest": "/etc/safe-rm.conf", "gid": 0, "group": "root", "md5sum": "ec1dd9707b6bf893781f323dfe3e63a2", "mode": "0644", "owner": "root", "size": 264, "src": "/root/.ansible/tmp/ansible-tmp-1704631389.02-2837-41680136000970/source", "state": "file", "uid": 0}
changed: [192.168.56.122] => {"changed": true, "checksum": "5468767a35430d62381d20a6c5f4a62413af9746", "dest": "/etc/safe-rm.conf", "gid": 0, "group": "root", "md5sum": "ec1dd9707b6bf893781f323dfe3e63a2", "mode": "0644", "owner": "root", "size": 264, "src": "/root/.ansible/tmp/ansible-tmp-1704631389.03-2839-171791247140643/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "checksum": "5468767a35430d62381d20a6c5f4a62413af9746", "dest": "/etc/safe-rm.conf", "gid": 0, "group": "root", "md5sum": "ec1dd9707b6bf893781f323dfe3e63a2", "mode": "0644", "owner": "root", "size": 264, "src": "/root/.ansible/tmp/ansible-tmp-1704631389.04-2841-173032710486627/source", "state": "file", "uid": 0}

TASK [base : Update pip command] *************************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "cmd": ["python3", "-m", "pip", "install", "--upgrade", "pip"], "delta": "0:00:01.121285", "end": "2024-01-07 20:43:11.355694", "rc": 0, "start": "2024-01-07 20:43:10.234409", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nRequirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.3.1)", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Requirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.3.1)"]}
changed: [192.168.56.122] => {"changed": true, "cmd": ["python3", "-m", "pip", "install", "--upgrade", "pip"], "delta": "0:00:01.280217", "end": "2024-01-07 20:43:11.462224", "rc": 0, "start": "2024-01-07 20:43:10.182007", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nRequirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.3.1)", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Requirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.3.1)"]}
changed: [192.168.56.121] => {"changed": true, "cmd": ["python3", "-m", "pip", "install", "--upgrade", "pip"], "delta": "0:00:01.302047", "end": "2024-01-07 20:43:11.412732", "rc": 0, "start": "2024-01-07 20:43:10.110685", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nRequirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.3.1)", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Requirement already satisfied: pip in /usr/local/lib/python3.6/site-packages (21.3.1)"]}

TASK [base : Install python package] *********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "cmd": ["/usr/local/bin/pip3", "install", "trash-cli"], "name": ["trash-cli"], "requirements": null, "state": "present", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv\n", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nCollecting trash-cli\n  Using cached trash_cli-0.23.11.10-py3-none-any.whl\nRequirement already satisfied: typing in /usr/local/lib/python3.6/site-packages (from trash-cli) (3.7.4.3)\nRequirement already satisfied: typing-extensions in /usr/local/lib/python3.6/site-packages (from trash-cli) (4.1.1)\nRequirement already satisfied: psutil in /usr/local/lib64/python3.6/site-packages (from trash-cli) (5.9.7)\nRequirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from trash-cli) (1.16.0)\nInstalling collected packages: trash-cli\nSuccessfully installed trash-cli-0.23.11.10\n", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Collecting trash-cli", "  Using cached trash_cli-0.23.11.10-py3-none-any.whl", "Requirement already satisfied: typing in /usr/local/lib/python3.6/site-packages (from trash-cli) (3.7.4.3)", "Requirement already satisfied: typing-extensions in /usr/local/lib/python3.6/site-packages (from trash-cli) (4.1.1)", "Requirement already satisfied: psutil in /usr/local/lib64/python3.6/site-packages (from trash-cli) (5.9.7)", "Requirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from trash-cli) (1.16.0)", "Installing collected packages: trash-cli", "Successfully installed trash-cli-0.23.11.10"], "version": null, "virtualenv": null}
changed: [192.168.56.121] => {"changed": true, "cmd": ["/usr/local/bin/pip3", "install", "trash-cli"], "name": ["trash-cli"], "requirements": null, "state": "present", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv\n", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nCollecting trash-cli\n  Using cached trash_cli-0.23.11.10-py3-none-any.whl\nRequirement already satisfied: typing-extensions in /usr/local/lib/python3.6/site-packages (from trash-cli) (4.1.1)\nRequirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from trash-cli) (1.16.0)\nRequirement already satisfied: typing in /usr/local/lib/python3.6/site-packages (from trash-cli) (3.7.4.3)\nRequirement already satisfied: psutil in /usr/local/lib64/python3.6/site-packages (from trash-cli) (5.9.7)\nInstalling collected packages: trash-cli\nSuccessfully installed trash-cli-0.23.11.10\n", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Collecting trash-cli", "  Using cached trash_cli-0.23.11.10-py3-none-any.whl", "Requirement already satisfied: typing-extensions in /usr/local/lib/python3.6/site-packages (from trash-cli) (4.1.1)", "Requirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from trash-cli) (1.16.0)", "Requirement already satisfied: typing in /usr/local/lib/python3.6/site-packages (from trash-cli) (3.7.4.3)", "Requirement already satisfied: psutil in /usr/local/lib64/python3.6/site-packages (from trash-cli) (5.9.7)", "Installing collected packages: trash-cli", "Successfully installed trash-cli-0.23.11.10"], "version": null, "virtualenv": null}
changed: [192.168.56.122] => {"changed": true, "cmd": ["/usr/local/bin/pip3", "install", "trash-cli"], "name": ["trash-cli"], "requirements": null, "state": "present", "stderr": "WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv\n", "stderr_lines": ["WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv"], "stdout": "Looking in indexes: http://mirrors.aliyun.com/pypi/simple/\nCollecting trash-cli\n  Using cached trash_cli-0.23.11.10-py3-none-any.whl\nRequirement already satisfied: typing in /usr/local/lib/python3.6/site-packages (from trash-cli) (3.7.4.3)\nRequirement already satisfied: typing-extensions in /usr/local/lib/python3.6/site-packages (from trash-cli) (4.1.1)\nRequirement already satisfied: psutil in /usr/local/lib64/python3.6/site-packages (from trash-cli) (5.9.7)\nRequirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from trash-cli) (1.16.0)\nInstalling collected packages: trash-cli\nSuccessfully installed trash-cli-0.23.11.10\n", "stdout_lines": ["Looking in indexes: http://mirrors.aliyun.com/pypi/simple/", "Collecting trash-cli", "  Using cached trash_cli-0.23.11.10-py3-none-any.whl", "Requirement already satisfied: typing in /usr/local/lib/python3.6/site-packages (from trash-cli) (3.7.4.3)", "Requirement already satisfied: typing-extensions in /usr/local/lib/python3.6/site-packages (from trash-cli) (4.1.1)", "Requirement already satisfied: psutil in /usr/local/lib64/python3.6/site-packages (from trash-cli) (5.9.7)", "Requirement already satisfied: six in /usr/local/lib/python3.6/site-packages (from trash-cli) (1.16.0)", "Installing collected packages: trash-cli", "Successfully installed trash-cli-0.23.11.10"], "version": null, "virtualenv": null}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=8    changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=8    changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=8    changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

可以看到，此时已经正常执行完成，说明三个节点的`safe-rm`和`trash-cli`已经安装成功。



我们在三个节点上面测试一下。

![](/img/Snipaste_2024-01-07_20-53-38.png)

可以看到，可以正常使用`safe-rm`命令，也可以正常使用`trash-put`、`trash-list`等命令。



### 2.9 扩展角色功能-设置时间同步定时任务

本节主要想做的事情是给服务器设置定时任务，每10分钟与NTP服务器同步一次时间，来提供准确时间。

先手动执行命令看下：

```sh
[root@ansible-node1 ~]# date
Sun Jan  7 21:29:47 CST 2024
[root@ansible-node1 ~]# ntpdate ntp1.aliyun.com
 7 Jan 21:30:16 ntpdate[7882]: adjust time server 120.25.115.20 offset -0.012267 sec
[root@ansible-node1 ~]# hwclock --show
Sun 07 Jan 2024 09:30:36 PM CST  -0.260778 seconds
[root@ansible-node1 ~]# hwclock --systohc
[root@ansible-node1 ~]# hwclock --show
Sun 07 Jan 2024 09:30:49 PM CST  -0.777690 seconds
[root@ansible-node1 ~]# whereis ntpdate
ntpdate: /usr/sbin/ntpdate /usr/share/man/man8/ntpdate.8.gz
[root@ansible-node1 ~]# whereis hwclock
hwclock: /usr/sbin/hwclock /usr/share/man/man8/hwclock.8.gz
[root@ansible-node1 ~]#
```

可以看到，时间同步命令正常。



更新`main.yml`任务配置文件：

```sh
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

检查剧本文件语法，并执行角色任务：

```sh

[root@ansible ansible_playbooks]# ansible-lint roles/base/tasks/main.yml
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.123]
ok: [192.168.56.121]
ok: [192.168.56.122]

TASK [base : Sync time at every 10 minutes] **************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "envs": [], "jobs": ["Sync time"]}
changed: [192.168.56.123] => {"changed": true, "envs": [], "jobs": ["Sync time"]}
changed: [192.168.56.122] => {"changed": true, "envs": [], "jobs": ["Sync time"]}

TASK [base : Sync time at 2:30 am] ***********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.121] => {"changed": true, "envs": [], "jobs": ["Sync time", "Set hardware clock time"]}
changed: [192.168.56.122] => {"changed": true, "envs": [], "jobs": ["Sync time", "Set hardware clock time"]}
changed: [192.168.56.123] => {"changed": true, "envs": [], "jobs": ["Sync time", "Set hardware clock time"]}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#

```

可以看到执行成功。

![](/img/Snipaste_2024-01-07_21-35-06.png)



在各节点上查看定时任务详情：

```sh
[root@ansible-node1 ~]# crontab -l
#Ansible: Sync time
*/10 * * * * /usr/sbin/ntpdate ntp1.aliyun.com > /dev/null 2>&1
#Ansible: Set hardware clock time
30 2 * * * /usr/sbin/hwclock --systohc > /dev/null 2>&1
[root@ansible-node1 ~]# 
```

可以看到，定时任务配置成功了。



### 2.10 扩展角色功能-生成主机公钥私钥对

如果我手动生成主机公钥私钥对，一般是在远程主机上面执行以下命令：

```sh
[root@ansible-node1 ~]# ssh-keygen -C root@192.168.56.121
```

即使用` ssh-keygen -C root@`后面接远程主机IP的形式。

所以我们需要获取远程主机IP，并设置为变量。

角色变量的使用，可参考[playbooks-variables](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#playbooks-variables) , 也可以直接看一下摘录：

> Set defaults in roles to avoid undefined-variable errors. If you share your roles, other users can rely on the reasonable defaults you added in the `roles/x/defaults/main.yml` file, or they can easily override those values in inventory or at the command line. See [Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#playbooks-reuse-roles) for more info. For example:
>
> ```
> ---
> # file: roles/x/defaults/main.yml
> # if no other value is supplied in inventory or as a parameter, this value will be used
> http_port: 80
> ```
>
> 
>
> Set variables in roles to ensure a value is used in that role, and is not overridden by inventory variables. If you are not sharing your role with others, you can define app-specific behaviors like ports this way, in `roles/x/vars/main.yml`. If you are sharing roles with others, putting variables here makes them harder to override, although they still can by passing a parameter to the role or setting a variable with `-e`:
>
> ```
> ---
> # file: roles/x/vars/main.yml
> # this will absolutely be used in this role
> http_port: 80
> ```
>
> 
>
> Pass variables as parameters when you call roles for maximum clarity, flexibility, and visibility. This approach overrides any defaults that exist for a role. For example:
>
> ```
> roles:
>    - role: apache
>      vars:
>         http_port: 8080
> ```



#### 2.10.1 角色vars变量的使用

- 我们可以使用`register`关键字可以来注册变量，注册变量后，可以在剧本后续的任务中使用该变量。可以参考： [debug调试模块](./debug.md) 或 [Command命令模块](./command.md)。

- 也可以像上面说明的那样在role角色的`vars`目录中定义变量。

下面我们来通过以下两种方式来配置远程主机的IP信息。

更新角色任务`roles/base/tasks/main.yml`：

```yaml
---
- name: Print the IP
  ansible.builtin.debug:
    msg: "{{ hostvars[inventory_hostname]['inventory_hostname'] }}"
  register: REMOTE_IP

- name: test register variable
  ansible.builtin.debug:
    msg: "REMOTE_IP: {{ REMOTE_IP.msg }}"

- name: test role variable
  ansible.builtin.debug:
    msg: "HOST_IP: {{ HOST_IP }}"

```

在`roles/base`目录下创建`vars`目录，并在`vars`目录下创建`main.yml`变量配置文件：

```sh
[root@ansible ansible_playbooks]# ll roles/base/vars
total 4
-rw-r--r--. 1 root root 72 Jan 10 06:53 main.yml
[root@ansible ansible_playbooks]# cat roles/base/vars/main.yml
---
HOST_IP: "{{ hostvars[inventory_hostname]['inventory_hostname'] }}"
[root@ansible ansible_playbooks]#
```

此时执行剧本：

```sh
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.122]
ok: [192.168.56.123]
ok: [192.168.56.121]

TASK [base : Print the IP] *******************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "192.168.56.121"
}
ok: [192.168.56.122] => {
    "msg": "192.168.56.122"
}
ok: [192.168.56.123] => {
    "msg": "192.168.56.123"
}

TASK [base : test register variable] *********************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "REMOTE_IP: 192.168.56.121"
}
ok: [192.168.56.122] => {
    "msg": "REMOTE_IP: 192.168.56.122"
}
ok: [192.168.56.123] => {
    "msg": "REMOTE_IP: 192.168.56.123"
}

TASK [base : test role variable] *************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "HOST_IP: 192.168.56.121"
}
ok: [192.168.56.122] => {
    "msg": "HOST_IP: 192.168.56.122"
}
ok: [192.168.56.123] => {
    "msg": "HOST_IP: 192.168.56.123"
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

运行效果图：

![](/img/Snipaste_2024-01-10_20-22-12.png)

此时，可以看到，通过注册变量方式能够获取每个主机的IP值，也可以通过在`roles/base/vars/main.yml`中定义变量`HOST_IP`来获取远程主机的IP信息。

```yaml
HOST_IP: "{{ hostvars[inventory_hostname]['inventory_hostname'] }}"
```
在后续角色剧本中，我们就使用这种方式来获取远程主机IP。



#### 2.10.2 远程生成主机公钥私钥对

我们参考[非交互模式生成密钥对](../../OS/Centos/ssh-keygen.md) ,可以知道非交互模式生成密钥对时，可以使用以下命令：

```sh
 ssh-keygen -C ${USERNAME}@${IP} -N "" -q -f ~/.ssh/id_rsa
```

示例：

```sh
 ssh-keygen -C reader@192.168.56.120 -N "" -q -f ~/.ssh/id_rsa
```

更新角色任务`roles/base/tasks/main.yml`：

```yaml
---
- name: test role variable
  ansible.builtin.debug:
    msg: "HOST_IP: {{ HOST_IP }}"

- name: Generate SSH key pair
  ansible.builtin.command:
    cmd: "ssh-keygen -C root@{{ HOST_IP }} -N '' -q -f /root/.ssh/id_rsa"
```

此时执行剧本：

```sh
# 检查剧本语法，没有异常
[root@ansible ansible_playbooks]# ansible-lint roles/base/tasks/main.yml

# 执行角色任务
[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini base.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.123]
ok: [192.168.56.122]

TASK [base : test role variable] *************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {
    "msg": "HOST_IP: 192.168.56.121"
}
ok: [192.168.56.123] => {
    "msg": "HOST_IP: 192.168.56.123"
}
ok: [192.168.56.122] => {
    "msg": "HOST_IP: 192.168.56.122"
}

TASK [base : Generate SSH key pair] **********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.123] => {"changed": true, "cmd": ["ssh-keygen", "-C", "root@192.168.56.123", "-N", "", "-q", "-f", "/root/.ssh/id_rsa"], "delta": "0:00:00.067082", "end": "2024-01-19 06:33:05.785883", "rc": 0, "start": "2024-01-19 06:33:05.718801", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
changed: [192.168.56.121] => {"changed": true, "cmd": ["ssh-keygen", "-C", "root@192.168.56.121", "-N", "", "-q", "-f", "/root/.ssh/id_rsa"], "delta": "0:00:00.067161", "end": "2024-01-19 06:33:05.786424", "rc": 0, "start": "2024-01-19 06:33:05.719263", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}
changed: [192.168.56.122] => {"changed": true, "cmd": ["ssh-keygen", "-C", "root@192.168.56.122", "-N", "", "-q", "-f", "/root/.ssh/id_rsa"], "delta": "0:00:00.074333", "end": "2024-01-19 06:33:05.790880", "rc": 0, "start": "2024-01-19 06:33:05.716547", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

正常执行，没有报错。



效果图如下：

![](/img/Snipaste_2024-01-19_06-38-35.png)



在三个节点上面查看一下刚生成的公钥信息：

```sh
# 在节点1上查看公钥信息
[root@ansible-node1 ~]# ll ~/.ssh
total 12
-rw------- 1 root root  804 Jan 18 06:54 authorized_keys
-rw------- 1 root root 1679 Jan 19 06:33 id_rsa
-rw-r--r-- 1 root root  401 Jan 19 06:33 id_rsa.pub
[root@ansible-node1 ~]# cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDUMzYFs8D84UMqvWFZbn2T5DXjHOJ/7vBpLf03SsMXMM6tggqRD2aGtiCHHBUtbM0aCOJ42NRC6yrn15sT9Ko6mvmkn3mc63diHJD3lAtsHTYFC0/cyXBI1a5yz+ziWlrQXaqc5YMD6IXJoLinDw9R3ZMt6dpXhx10KDiO9xLJIvan5B4hAqCypDLGh+eyauEq2QbURKqSgs54Opm7TfLH8QaK+brGwhZW9+yrkRXSGE9XAV5TLSyObpj9/rR5/TCcEhdPaabjlsmJ7LHXUvYonfsgEs3xfcjBiktF/+TdpuQWLwo9ozQoM/iyT8EhUWhDVvEF915yTiy3BYgZN8S3 root@192.168.56.121
[root@ansible-node1 ~]# 


# 在节点2上查看公钥信息
[root@ansible-node2 ~]# ll ~/.ssh
total 12
-rw-------. 1 root root  401 Dec  2 00:12 authorized_keys
-rw-------  1 root root 1679 Jan 19 06:33 id_rsa
-rw-r--r--  1 root root  401 Jan 19 06:33 id_rsa.pub
[root@ansible-node2 ~]# cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCcKfQQymdFHW1fGzmB6K2kIAXzCFtx9Z0+TI95RU4f9Hxgq33XexWFt6VaWVmyRO7CHRkC69OW+0JMdMeU6KFdDuFCLzyreL9tjEIXqN0qU2LYhxmX+XVdk/1xZLr7KUIun0gU6RU0RuOtQ3JkIRLW9+9DoGJh1sVD/lIcjyXHMXfl6/2aygt8SAfUVeduD29nbJygtnf98JZ9gCmaeu/4A7kqFgHSnMdh9cWWsoJjwgKOnkpX1QP9XFiIMt4ZmbI0/IHpuaAD9iJgRDhQyek0tgQhWCoqvOvmVigorfvp5EjC7xxNjTpy4+//QKBBVVD5LyzlQEr+EsEgw38v0bMV root@192.168.56.122
[root@ansible-node2 ~]# 


# 在节点3上查看公钥信息
[root@ansible-node3 ~]# ll ~/.ssh
total 12
-rw-------. 1 root root  401 Dec  2 00:12 authorized_keys
-rw-------  1 root root 1675 Jan 19 06:33 id_rsa
-rw-r--r--  1 root root  401 Jan 19 06:33 id_rsa.pub
[root@ansible-node3 ~]# cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCzDYmK78kzbnWB5IgLSs4+KwOJXaFaUVz4gJeARjHs697aOx+aF1WtFSZLXDel4qGSqiq/ERaj/f3girHFfYfHCM/wSdG5iJPzF2yniE5nYUy9YOnnnDmrcdOZfXq73/OvfzbJg0PPC4xS8aweoxw9lq7m+X7M2ldZDDTQwryfDgaFlkMoQ36qH0DXA2zmbQbNZ7l+HiqhEKvz0xBUzTLgGQ7pAGntbFQohkcjGsAIVD56F3kvOpwMLdthk+xLEoAlllTdtTO6puDi/PKLO7NycP5IZ9z7JKAGcyz4MpSkSRC7Vd+EUV6Xf3ZlBxz4KyQt0xlCBPTDgQTF/G2adyVd root@192.168.56.123
[root@ansible-node3 ~]#
```

可以看到，节点上面正常生成了公钥私钥对了，并且备注信息是按`root@${IP}`这种形式创建的，满足我们的预期要求。