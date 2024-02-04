# wait_for条件等待模块


[[toc]]

## 1. 概要

-  wait_for条件等待模块会在继续执行之前等待一个条件成立。
-  您可以等待`timeout`设定的超时时间，如果不设置该参数，则使用默认的超时时间(300秒)，此时不会产生异常。
-  当服务在其初始化脚本返回后不能立即可用时，等待端口变为可用非常有用，这对于某些 Java 应用程序服务器来说很有用。
-  wait_for模块也可以用在等待匹配字符串出现在文件中后，再继续执行。
-  wait_for模块也可以用来等待文件在文件系统上可用或不存在时，再继续执行。
-  wait_for模块也可以用来等待负载均衡中某个节点关闭活动连接后，再继续执行。
- 官方文档：2.9版本 [https://docs.ansible.com/ansible/2.9/modules/wait_for_module.html](https://docs.ansible.com/ansible/2.9/modules/wait_for_module.html) 或最新版 [https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_module.html](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/wait_for_module.html)


## 2. 参数


| 参数                     | 可选值 | 默认值 | 说明                                                         |
| ------------------------ | ------ | ------ | ------------------------------------------------------------ |
| `active_connection_states`             |        |  `["ESTABLISHED", "FIN_WAIT1", "FIN_WAIT2", "SYN_RECV", "SYN_SENT", "TIME_WAIT"]`      | `list`，被算作活动连接的TCP连接状态列表 |
| `connect_timeout`             |      |  5      | `integer`，在关闭和重试之前等待连接发生的最大秒数 |
| `delay`             |      |  0      | `integer`，开始轮询之前等待的秒数 |
| `exclude_hosts`             |        |      | `list`，在查找处于`drained`耗尽状态的活动TCP连接时要忽略的主机或IP的列表。 |
| `host`             |      |  `127.0.0.1`      | `string`，等待可解析的主机名或IP地址 |
| `msg`             |      |       | `string`，不满足条件时显示的错误消息 |
| `path`             |      |       | `path`，在继续之前，文件系统中必须存在的文件的路径，与`port`参数互斥 |
| `port`             |      |       | `integer`，轮询的端口号，与`path`参数互斥 |
| `search_regex`             |      |       | `string`，可用于匹配文件或套接字连接中的字符串。默认为多行正则表达式。 |
| `port`             |      |       | `integer`，轮询的端口号，与`path`参数互斥 |
| `sleep`             |      |    1   | `integer`，在两次检查之间休眠的秒数 |
| `state`             | `absent`、`drained`  、`present`、`started`、`stopped`   |  `started`     | `string`，可以是`absent`、`drained`  、`present`、`started`、`stopped`这几种状态，当检查一个`port`端口时，`started`将确保端口是监听开放的，`stopped`将检查状态是关闭的，`drained`将检查活动连接是耗尽的。当检查`path`文件或搜索字符串是否存在时，`present`或`started`将确保文件或字符串已存在再继续执行，`absent`将检查该文件是否被删除。 |
| `timeout`             |      |   300    | `integer`，最大等待秒数。当与另一个条件一起使用时，它将强制出现错误 |

## 3. 官方示例

```yaml
- name: sleep for 300 seconds and continue with play
  wait_for:
    timeout: 300
  delegate_to: localhost

- name: Wait for port 8000 to become open on the host, don't start checking for 10 seconds
  wait_for:
    port: 8000
    delay: 10

- name: Waits for port 8000 of any IP to close active connections, don't start checking for 10 seconds
  wait_for:
    host: 0.0.0.0
    port: 8000
    delay: 10
    state: drained

- name: Wait for port 8000 of any IP to close active connections, ignoring connections for specified hosts
  wait_for:
    host: 0.0.0.0
    port: 8000
    state: drained
    exclude_hosts: 10.2.1.2,10.2.1.3

- name: Wait until the file /tmp/foo is present before continuing
  wait_for:
    path: /tmp/foo

- name: Wait until the string "completed" is in the file /tmp/foo before continuing
  wait_for:
    path: /tmp/foo
    search_regex: completed

- name: Wait until regex pattern matches in the file /tmp/foo and print the matched group
  wait_for:
    path: /tmp/foo
    search_regex: completed (?P<task>\w+)
  register: waitfor
- debug:
    msg: Completed {{ waitfor['groupdict']['task'] }}

- name: Wait until the lock file is removed
  wait_for:
    path: /var/lock/file.lock
    state: absent

- name: Wait until the process is finished and pid was destroyed
  wait_for:
    path: /proc/3466/status
    state: absent

- name: Output customized message when failed
  wait_for:
    path: /tmp/foo
    state: present
    msg: Timeout to find file /tmp/foo

# Do not assume the inventory_hostname is resolvable and delay 10 seconds at start
- name: Wait 300 seconds for port 22 to become open and contain "OpenSSH"
  wait_for:
    port: 22
    host: '{{ (ansible_ssh_host|default(ansible_host))|default(inventory_hostname) }}'
    search_regex: OpenSSH
    delay: 10
  connection: local

# Same as above but you normally have ansible_connection set in inventory, which overrides 'connection'
- name: Wait 300 seconds for port 22 to become open and contain "OpenSSH"
  wait_for:
    port: 22
    host: '{{ (ansible_ssh_host|default(ansible_host))|default(inventory_hostname) }}'
    search_regex: OpenSSH
    delay: 10
  vars:
    ansible_connection: local
```

## 4. 剧本的使用

### 4.1 端口监听检查

我们编写一个检查nginx端口的剧本文件`wait_for.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Restart nginx service
      service:
        name: nginx
        state: restarted
      become: yes

    - name: Wait for port 80 to become open on the host
      wait_for:
        port: 80
        delay: 10
      become: yes

```

检查并执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint wait_for.yml
[ansible@master ansible_playbooks]$ ansible-playbook wait_for.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Restart nginx service] *******************************************************************************************
changed: [node1] => {"changed": true, "name": "nginx", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-03-05 10:17:06 CST", "ActiveEnterTimestampMonotonic": "30503061191877", "ActiveExitTimestamp": "Sun 2023-03-05 10:17:06 CST", "ActiveExitTimestampMonotonic": "30503061149343", "ActiveState": "active", "After": "tmp.mount systemd-journald.socket nss-lookup.target basic.target system.slice network-online.target remote-fs.target -.mount", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2023-03-05 10:17:06 CST", "AssertTimestampMonotonic": "30503061164534", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "yes", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2023-03-05 10:17:06 CST", "ConditionTimestampMonotonic": "30503061164533", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/nginx.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "The nginx HTTP and reverse proxy server", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "7379", "ExecMainStartTimestamp": "Sun 2023-03-05 10:17:06 CST", "ExecMainStartTimestampMonotonic": "30503061191849", "ExecMainStatus": "0", "ExecReload": "{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx -s reload ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "ExecStart": "{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "ExecStartPre": "{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx -t ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/nginx.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "nginx.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2023-03-05 10:17:06 CST", "InactiveEnterTimestampMonotonic": "30503061159209", "InactiveExitTimestamp": "Sun 2023-03-05 10:17:06 CST", "InactiveExitTimestampMonotonic": "30503061170505", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "process", "KillSignal": "3", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "15066", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "15066", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "7379", "MemoryAccounting": "no", "MemoryCurrent": "2314240", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "nginx.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PIDFile": "/run/nginx.pid", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "yes", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "basic.target -.mount system.slice", "RequiresMountsFor": "/var/tmp", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "3", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "5s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "Wants": "network-online.target", "WatchdogTimestamp": "Sun 2023-03-05 10:17:06 CST", "WatchdogTimestampMonotonic": "30503061191863", "WatchdogUSec": "0"}}

TASK [Wait for port 80 to become open on the host] *********************************************************************
ok: [node1] => {"changed": false, "elapsed": 10, "match_groupdict": {}, "match_groups": [], "path": null, "port": 80, "search_regex": null, "state": "started"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，nginx服务重启成功，也检查80端口监听，说明`wait_for`检查正常。

我们在节点`node1`上面检查一下：
```sh
[root@node1 ~]# systemctl status nginx|grep --color=always active
   Active: active (running) since Mon 2023-03-20 22:21:44 CST; 3min 17s ago
[root@node1 ~]# netstat -tunlp|grep nginx|grep 80
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      717/nginx: master p
tcp6       0      0 :::80                   :::*                    LISTEN      717/nginx: master p
[root@node1 ~]#
```
可以看到nginx服务刚重启了，80端口也在正常监听。


### 4.2 文件检查

编写文件检查的剧本文件`wait_for_file.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Wait until the file /tmp/foo is present before continuing
      wait_for:
        path: /tmp/foo

    - name: Wait until the string "completed" is in the file /tmp/foo before continuing
      wait_for:
        path: /tmp/foo
        search_regex: completed

    - name: Output customized message when failed
      wait_for:
        path: /tmp/foo
        state: present
        delay: 20
        msg: Timeout to find file /tmp/foo

```

此时，检查并运行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-playbook wait_for_file.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Wait until the file /tmp/foo is present before continuing] *******************************************************
```

![](/img/Snipaste_2023-03-20_22-41-32.png)
可以看到，剧本没有继续向下执行。

此时，在节点`node1`上面创建一个新文件`/tmp/foo`：
```sh
[root@node1 tmp]# touch /tmp/foo && ls -lah foo
-rw-r--r-- 1 root root 0 Mar 20 22:42 foo
[root@node1 tmp]#
```

此时，在Ansible控制节点可以看到，剧本向前运行了一步：

![](/img/Snipaste_2023-03-20_22-44-22.png)
我们此时，再在节点上向文件中写入内容：

```sh
[root@node1 tmp]# echo 'test completed' > foo
[root@node1 tmp]# ls -lah foo
-rw-r--r-- 1 root root 15 Mar 20 22:45 foo
[root@node1 tmp]# cat foo
test completed
[root@node1 tmp]#
```

此时程序又执行了一步：
![](/img/Snipaste_2023-03-20_22-46-17.png)
程序等待20秒后，又自动执行了最后一步。

此时，如果我们修改剧本，在剧本中增加一个删除文件的步骤：

```yaml
- hosts: node1
  tasks:
    - name: Wait until the file /tmp/foo is present before continuing
      wait_for:
        path: /tmp/foo

    - name: Wait until the string "completed" is in the file /tmp/foo before continuing
      wait_for:
        path: /tmp/foo
        search_regex: completed

    - name: rm file
      file:
        path: /tmp/foo
        state: absent
      become: true

    - name: Output customized message when failed
      wait_for:
        path: /tmp/foo
        state: present
        timeout: 20
        msg: Timeout to find file /tmp/foo

```

此时，再次执行剧本，并且在节点`node1`上面创建一下文件：

```sh
[root@node1 tmp]# echo 'test completed' > foo
```

执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook wait_for_file.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Wait until the file /tmp/foo is present before continuing] *******************************************************
ok: [node1] => {"changed": false, "elapsed": 6, "gid": 0, "group": "root", "match_groupdict": {}, "match_groups": [], "mode": "0644", "owner": "root", "path": "/tmp/foo", "port": null, "search_regex": null, "size": 15, "state": "file", "uid": 0}

TASK [Wait until the string "completed" is in the file /tmp/foo before continuing] *************************************
ok: [node1] => {"changed": false, "elapsed": 0, "gid": 0, "group": "root", "match_groupdict": {}, "match_groups": [], "mode": "0644", "owner": "root", "path": "/tmp/foo", "port": null, "search_regex": "completed", "size": 15, "state": "file", "uid": 0}

TASK [rm file] *********************************************************************************************************
changed: [node1] => {"changed": true, "path": "/tmp/foo", "state": "absent"}

TASK [Output customized message when failed] ***************************************************************************
fatal: [node1]: FAILED! => {"changed": false, "elapsed": 20, "msg": "Timeout to find file /tmp/foo"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=4    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

![](/img/Snipaste_2023-03-20_23-11-22.png)
此时可以看到，在等待`20`秒超时时间后，没有找到文件，输出了我们自定义的消息"Timeout to find file /tmp/foo"。


注意：

- `delay`参数和`timeout`参数不同，`delay: 20`表示等待20秒钟再去进行检查操作，而`timeout: 20`是指程序不停检查最终等待20秒，如果还没检查成功，则会报超时异常，或`msg`定义的异常。

如我将剧本中最后一行的`msg: Timeout to find file /tmp/foo`注释掉，再执行剧本显示效果如下：
![](/img/Snipaste_2023-03-20_23-22-32.png)
此时的异常消息则是默认的异常输出。 