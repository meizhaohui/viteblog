# timezone模块

[[toc]]

## 0. 时区说明
- CST表示中国标准时间(China Standard Time)。中国标准时间(CST)比世界协调时间(UTC)早08:00小时。该时区为标准时区时间，主要用于 亚洲。对应时区名称`Asia/Shanghai`。
- JST表示日本标准时间(Japan Standard Time)。日本标准时间(JST)比世界协调时间(UTC)早09:00小时。该时区为标准时区时间，主要用于 亚洲。对应时区名称`Asia/Tokyo`。
- UTC(Universal Time Coordinated)，协调世界时，又称世界统一时间、世界标准时间、国际协调时间。由于英文（CUT）和法文（TUC）的缩写不同，作为妥协，简称UTC。


## 1. 概要

- `timezona`模块可以用来设置远程主机的时区信息。 
- 推荐在修改时区信息后，重启一下`crond`定时任务服务，避免定时任务在错误的时间运行。
- 官方文档：[https://docs.ansible.com/ansible/2.9/modules/timezone_module.html](https://docs.ansible.com/ansible/2.9/modules/timezone_module.html)


## 2. 参数

| 参数                     | 可选值 | 默认值 | 说明                                                         |
| ------------------------ | ------ | ------ | ------------------------------------------------------------ |
| `name`             |        |        | `string`，系统时钟的时区名称。 |
| `hwclock`             | `local`、`UTC`       |      | `string`，硬件时钟是采用 UTC 还是采用本地时区。默认是保持当前设置。注意这个选项建议不要更改，可能会配置失败，尤其是在AWS等虚拟环境中。`name`和`hwclock`参数至少要配置一个。 |


## 3. 官方示例

```yaml
- name: Set timezone to Asia/Tokyo
  timezone:
    name: Asia/Tokyo
```

## 4. 剧本的使用

先在`node1`节点上面检查一下当前时间和`crond`服务信息：

```sh
[root@node1 ~]# date
Sun Mar 19 08:28:22 CST 2023
[root@node1 ~]# systemctl status crond
● crond.service - Command Scheduler
   Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2022-03-17 09:12:52 CST; 1 years 0 months ago
 Main PID: 1582 (crond)
    Tasks: 1
   Memory: 1.5M
   CGroup: /system.slice/crond.service
           └─1582 /usr/sbin/crond -n

Warning: Journal has been rotated since unit was started. Log output is incomplete or unavailable.
```

可知`node1`节点当前系统使用的是`CST`中国标准时间。

我们参照官方示例，编写剧本文件`timezone.yml`：

```yaml
- hosts: node1
  tasks:
    - name: show the timezone 1
      command:
        cmd: ls -lah /etc/localtime
      # [301] Commands should not change things if nothing needs doing
      register: myoutput
      changed_when: myoutput.rc != 0

    - name: Set timezone to Asia/Tokyo
      timezone:
        name: Asia/Tokyo
      become: yes

    - name: Restart crond service
      service:
        name: crond
        state: restarted
      become: yes

    - name: show the timezone 2
      command:
        cmd: ls -lah /etc/localtime
      # [301] Commands should not change things if nothing needs doing
      changed_when: false
```

检查剧本文件并执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint timezone.yml
[ansible@master ansible_playbooks]$ ansible-playbook timezone.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [show the timezone 1] *********************************************************************************************
ok: [node1] => {"changed": false, "cmd": ["ls", "-lah", "/etc/localtime"], "delta": "0:00:00.010513", "end": "2023-03-19 08:29:07.221503", "rc": 0, "start": "2023-03-19 08:29:07.210990", "stderr": "", "stderr_lines": [], "stdout": "lrwxrwxrwx. 1 root root 35 Mar  7  2019 /etc/localtime -> ../usr/share/zoneinfo/Asia/Shanghai", "stdout_lines": ["lrwxrwxrwx. 1 root root 35 Mar  7  2019 /etc/localtime -> ../usr/share/zoneinfo/Asia/Shanghai"]}

TASK [Set timezone to Asia/Tokyo] **************************************************************************************
changed: [node1] => {"changed": true, "msg": "executed `/bin/timedatectl set-timezone Asia/Tokyo`"}

TASK [Restart crond service] *******************************************************************************************
changed: [node1] => {"changed": true, "name": "crond", "state": "started", "status": {"ActiveEnterTimestamp": "Thu 2022-03-17 10:12:52 JST", "ActiveEnterTimestampMonotonic": "7908144", "ActiveExitTimestampMonotonic": "0", "ActiveState": "active", "After": "system.slice time-sync.target systemd-user-sessions.service basic.target systemd-journald.socket auditd.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Thu 2022-03-17 10:12:52 JST", "AssertTimestampMonotonic": "7901557", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "yes", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Thu 2022-03-17 10:12:52 JST", "ConditionTimestampMonotonic": "7901557", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/crond.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Command Scheduler", "DevicePolicy": "auto", "EnvironmentFile": "/etc/sysconfig/crond (ignore_errors=no)", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "1582", "ExecMainStartTimestamp": "Thu 2022-03-17 10:12:52 JST", "ExecMainStartTimestampMonotonic": "7908103", "ExecMainStatus": "0", "ExecReload": "{ path=/bin/kill ; argv[]=/bin/kill -HUP $MAINPID ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "ExecStart": "{ path=/usr/sbin/crond ; argv[]=/usr/sbin/crond -n $CRONDARGS ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/crond.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "crond.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestampMonotonic": "0", "InactiveExitTimestamp": "Thu 2022-03-17 10:12:52 JST", "InactiveExitTimestampMonotonic": "7908144", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "process", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "15066", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "15066", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "1582", "MemoryAccounting": "no", "MemoryCurrent": "1593344", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "crond.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "on-failure", "RestartUSec": "30s", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "1", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "simple", "UMask": "0022", "UnitFilePreset": "enabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Thu 2022-03-17 10:12:52 JST", "WatchdogTimestampMonotonic": "7908131", "WatchdogUSec": "0"}}

TASK [show the timezone 2] *********************************************************************************************
ok: [node1] => {"changed": false, "cmd": ["ls", "-lah", "/etc/localtime"], "delta": "0:00:00.016230", "end": "2023-03-19 09:29:09.131838", "rc": 0, "start": "2023-03-19 09:29:09.115608", "stderr": "", "stderr_lines": [], "stdout": "lrwxrwxrwx 1 root root 32 Mar 19 09:29 /etc/localtime -> ../usr/share/zoneinfo/Asia/Tokyo", "stdout_lines": ["lrwxrwxrwx 1 root root 32 Mar 19 09:29 /etc/localtime -> ../usr/share/zoneinfo/Asia/Tokyo"]}

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```


在`node1`节点重新打开一个`bash`窗口，然后查看当前时间和`crond`服务信息：
```sh
[root@node1 ~]# bash
[root@node1 ~]# date
Sun Mar 19 09:29:34 JST 2023
[root@node1 ~]# systemctl status crond
● crond.service - Command Scheduler
   Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2023-03-19 09:29:08 JST; 3min 28s ago
 Main PID: 28211 (crond)
    Tasks: 1
   Memory: 676.0K
   CGroup: /system.slice/crond.service
           └─28211 /usr/sbin/crond -n

Mar 19 09:29:08 node1 systemd[1]: Started Command Scheduler.
Mar 19 09:29:08 node1 crond[28211]: (CRON) INFO (RANDOM_DELAY will be scaled with factor 5% if used.)
Mar 19 09:29:08 node1 crond[28211]: (CRON) INFO (running with inotify support)
Mar 19 09:29:08 node1 crond[28211]: (CRON) INFO (@reboot jobs will be run at computer's startup.)
[root@node1 ~]#
```

可知当前系统使用的是`JST`日本标准时间。`JST`日本标准时间比`CST`中国标准时间快一个小时。


我们可以修改剧本文件：
```yaml
- hosts: node1
  tasks:
    - name: show the timezone 1
      command:
        cmd: ls -lah /etc/localtime
      # [301] Commands should not change things if nothing needs doing
      register: myoutput
      changed_when: myoutput.rc != 0

    - name: Set timezone to UTC
      timezone:
        name: UTC
      become: yes

    - name: Restart crond service
      service:
        name: crond
        state: restarted
      become: yes

    - name: show the timezone 2
      command:
        cmd: ls -lah /etc/localtime
      # [301] Commands should not change things if nothing needs doing
      changed_when: false
```

然后再次执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-playbook timezone.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [show the timezone 1] *********************************************************************************************
ok: [node1] => {"changed": false, "cmd": ["ls", "-lah", "/etc/localtime"], "delta": "0:00:00.010431", "end": "2023-03-19 11:13:46.675419", "rc": 0, "start": "2023-03-19 11:13:46.664988", "stderr": "", "stderr_lines": [], "stdout": "lrwxrwxrwx 1 root root 32 Mar 19 09:29 /etc/localtime -> ../usr/share/zoneinfo/Asia/Tokyo", "stdout_lines": ["lrwxrwxrwx 1 root root 32 Mar 19 09:29 /etc/localtime -> ../usr/share/zoneinfo/Asia/Tokyo"]}

TASK [Set timezone to UTC] *********************************************************************************************
changed: [node1] => {"changed": true, "msg": "executed `/bin/timedatectl set-timezone UTC`"}

TASK [Restart crond service] *******************************************************************************************
changed: [node1] => {"changed": true, "name": "crond", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-03-19 00:29:08 UTC", "ActiveEnterTimestampMonotonic": "31706183388184", "ActiveExitTimestamp": "Sun 2023-03-19 00:29:08 UTC", "ActiveExitTimestampMonotonic": "31706183356308", "ActiveState": "active", "After": "system.slice time-sync.target systemd-user-sessions.service basic.target systemd-journald.socket auditd.service", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2023-03-19 00:29:08 UTC", "AssertTimestampMonotonic": "31706183363713", "Before": "multi-user.target shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "yes", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2023-03-19 00:29:08 UTC", "ConditionTimestampMonotonic": "31706183363712", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/crond.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Command Scheduler", "DevicePolicy": "auto", "EnvironmentFile": "/etc/sysconfig/crond (ignore_errors=no)", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "28211", "ExecMainStartTimestamp": "Sun 2023-03-19 00:29:08 UTC", "ExecMainStartTimestampMonotonic": "31706183388152", "ExecMainStatus": "0", "ExecReload": "{ path=/bin/kill ; argv[]=/bin/kill -HUP $MAINPID ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "ExecStart": "{ path=/usr/sbin/crond ; argv[]=/usr/sbin/crond -n $CRONDARGS ; ignore_errors=no ; start_time=[Sun 2023-03-19 00:29:08 UTC] ; stop_time=[n/a] ; pid=28211 ; code=(null) ; status=0/0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/crond.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "crond.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2023-03-19 00:29:08 UTC", "InactiveEnterTimestampMonotonic": "31706183359067", "InactiveExitTimestamp": "Sun 2023-03-19 00:29:08 UTC", "InactiveExitTimestampMonotonic": "31706183388184", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "process", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "15066", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "15066", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "28211", "MemoryAccounting": "no", "MemoryCurrent": "692224", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "crond.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "on-failure", "RestartUSec": "30s", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "1", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "simple", "UMask": "0022", "UnitFilePreset": "enabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "WatchdogTimestamp": "Sun 2023-03-19 00:29:08 UTC", "WatchdogTimestampMonotonic": "31706183388172", "WatchdogUSec": "0"}}

TASK [show the timezone 2] *********************************************************************************************
ok: [node1] => {"changed": false, "cmd": ["ls", "-lah", "/etc/localtime"], "delta": "0:00:01.011516", "end": "2023-03-19 02:13:48.992859", "rc": 0, "start": "2023-03-19 02:13:47.981343", "stderr": "", "stderr_lines": [], "stdout": "lrwxrwxrwx 1 root root 25 Mar 19 02:13 /etc/localtime -> ../usr/share/zoneinfo/UTC", "stdout_lines": ["lrwxrwxrwx 1 root root 25 Mar 19 02:13 /etc/localtime -> ../usr/share/zoneinfo/UTC"]}

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

在`node1`节点上面查看时间和时区信息：
```sh
[root@node1 ~]# bash
[root@node1 ~]# date
Sun Mar 19 02:14:01 UTC 2023
[root@node1 ~]# ls -lah /etc/localtime
lrwxrwxrwx 1 root root 25 Mar 19 02:13 /etc/localtime -> ../usr/share/zoneinfo/UTC
[root@node1 ~]#
```
可以看到时区变成了UTC标准时间。

我们最后将时区还原成`Asia/Shanghai`:
```sh
- hosts: node1
  tasks:
    - name: show the timezone 1
      command:
        cmd: ls -lah /etc/localtime
      # [301] Commands should not change things if nothing needs doing
      register: myoutput
      changed_when: myoutput.rc != 0

    - name: Set timezone to Asia/Shanghai
      timezone:
        name: Asia/Shanghai
      become: yes

    - name: Restart crond service
      service:
        name: crond
        state: restarted
      become: yes

    - name: show the timezone 2
      command:
        cmd: ls -lah /etc/localtime
      # [301] Commands should not change things if nothing needs doing
      changed_when: false
```

再次执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-playbook timezone.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [show the timezone 1] *********************************************************************************************
ok: [node1]

TASK [Set timezone to Asia/Shanghai] ***********************************************************************************
changed: [node1]

TASK [Restart crond service] *******************************************************************************************
changed: [node1]

TASK [show the timezone 2] *********************************************************************************************
ok: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

再次在`node1`节点上面查看时区等信息：

```sh
[root@node1 ~]# date
Sun Mar 19 10:22:24 CST 2023
[root@node1 ~]# ll /etc/localtime
lrwxrwxrwx 1 root root 35 Mar 19 10:21 /etc/localtime -> ../usr/share/zoneinfo/Asia/Shanghai
[root@node1 ~]# systemctl status crond
● crond.service - Command Scheduler
   Loaded: loaded (/usr/lib/systemd/system/crond.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2023-03-19 10:21:09 CST; 1min 26s ago
 Main PID: 22318 (crond)
    Tasks: 1
   Memory: 628.0K
   CGroup: /system.slice/crond.service
           └─22318 /usr/sbin/crond -n

Mar 19 10:21:09 node1 systemd[1]: Stopped Command Scheduler.
Mar 19 10:21:09 node1 systemd[1]: Started Command Scheduler.
Mar 19 10:21:09 node1 crond[22318]: (CRON) INFO (RANDOM_DELAY will be scaled with factor 22% if used.)
Mar 19 10:21:09 node1 crond[22318]: (CRON) INFO (running with inotify support)
Mar 19 10:21:09 node1 crond[22318]: (CRON) INFO (@reboot jobs will be run at computer's startup.)
[root@node1 ~]#
```

可以看到时区信息已经还原成了中国标准时间了！！

参考：
- [CST时间与JST时间换算](https://datetime360.com/cn/cst-china-jst-time/)
- [timezone – Configure timezone setting](https://docs.ansible.com/ansible/2.9/modules/timezone_module.html)
- [community.general.timezone module – Configure timezone setting](https://docs.ansible.com/ansible/latest/collections/community/general/timezone_module.html)
- [Commands should not change things if nothing needs to be done](https://deepsource.io/directory/analyzers/ansible/issues/ANS-E3001)
- [Ansible-lint warn [301] Commands should not change things if nothing needs doing](https://github.com/geerlingguy/ansible-role-certbot/issues/144)