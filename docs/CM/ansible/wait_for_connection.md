# wait_for_connection等待远程主机连接模块


[[toc]]

## 1. 概要

-  wait_for_connection模块，会等待远程系统，确定其是否可访问。
-  Ansible会等待`timeout`设定的超时时间。
-  在`connect_timeout`设定的连接超时时间后，重试传输连接。
-  `sleep`参数指定每睡眠几秒钟测试一次传输连接。
-  该模块利用内部可安全传输（和配置）和`ping`模块来保证正确的端到端功能。
- 官方文档：2.9版本 [https://docs.ansible.com/ansible/2.9/modules/wait_for_connection_module.html](https://docs.ansible.com/ansible/2.9/modules/wait_for_connection_module.html) 或最新版 [https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_connection_module.html](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_connection_module.html)
- reboot重启模块，可参考 [https://docs.ansible.com/ansible/2.9/modules/reboot_module.html](https://docs.ansible.com/ansible/2.9/modules/reboot_module.html)


## 2. 参数


| 参数                     | 可选值 | 默认值 | 说明                                                         |
| ------------------------ | ------ | ------ | ------------------------------------------------------------ |
| `connect_timeout`             |        |  5      | `integer`，在重试之前，等待成功连接到被控主机的最长秒数 |
| `delay`             |      |  0      | `integer`，开始轮询之前等待的秒数 |
| `sleep`             |      |    1   | `integer`，在两次检查之间休眠的秒数 |
| `timeout`             |      |   600    | `integer`，最长等待秒数 |

## 3. 官方示例

```yaml
- name: Wait 600 seconds for target connection to become reachable/usable
  wait_for_connection:

- name: Wait 300 seconds, but only start checking after 60 seconds
  wait_for_connection:
    delay: 60
    timeout: 300

# Wake desktops, wait for them to become ready and continue playbook
- hosts: all
  gather_facts: no
  tasks:
  - name: Send magic Wake-On-Lan packet to turn on individual systems
    wakeonlan:
      mac: '{{ mac }}'
      broadcast: 192.168.0.255
    delegate_to: localhost

  - name: Wait for system to become reachable
    wait_for_connection:

  - name: Gather facts for first time
    setup:

# Build a new VM, wait for it to become ready and continue playbook
- hosts: all
  gather_facts: no
  tasks:
  - name: Clone new VM, if missing
    vmware_guest:
      hostname: '{{ vcenter_ipaddress }}'
      name: '{{ inventory_hostname_short }}'
      template: Windows 2012R2
      customization:
        hostname: '{{ vm_shortname }}'
        runonce:
        - powershell.exe -ExecutionPolicy Unrestricted -File C:\Windows\Temp\ConfigureRemotingForAnsible.ps1 -ForceNewSSLCert -EnableCredSSP
    delegate_to: localhost

  - name: Wait for system to become reachable over WinRM
    wait_for_connection:
      timeout: 900

  - name: Gather facts for first time
    setup:
```


## 4. 剧本的使用

编写重启远程主机的剧本`wait_for_connection.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Reboot the machine (Wait for 5 min)
      reboot:
        reboot_timeout: 300
        msg: Reboot by Ansible
      become: yes

    - name: Wait for the machine to come back online
      wait_for_connection:
        connect_timeout: 60
        sleep: 5
        delay: 5
        timeout: 300
```

检查并执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint wait_for_connection.yml
[ansible@master ansible_playbooks]$ ansible-playbook wait_for_connection.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Reboot the machine (Wait for 5 min)] *****************************************************************************
changed: [node1] => {"changed": true, "elapsed": 38, "rebooted": true}

TASK [Wait for the machine to come back online] ************************************************************************
ok: [node1] => {"changed": false, "elapsed": 5}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到任务`Reboot the machine (Wait for 5 min)`已经执行重启主机成功，`Wait for the machine to come back online`在第1次检查时就发现远程主机可连接了！！

登陆远程主机，使用`uptime`查看启动时间：

```sh
[root@node1 ~]# uptime
 23:01:26 up 3 min,  1 user,  load average: 0.15, 0.17, 0.08
[root@node1 ~]#
```

可以看到，才启动一会儿，说明我们重启正常，`wait_for_connection`检查远程主机连接也是正常的！！