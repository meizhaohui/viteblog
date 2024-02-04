# when条件判断

[[toc]]

## 1. 官方示例

- `when`条件判断，可参考官方文档 [Conditionals](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html)

以下是官方示例中的几个示例：

### 1.1 判断操作系统
判断操作系统是否是`Debian`:

```yaml
tasks:
  - name: Shut down Debian flavored systems
    ansible.builtin.command: /sbin/shutdown -t now
    when: ansible_facts['os_family'] == "Debian"
```

多条件判断，判断操作系统是不是CentOS6或Debian7:

```yaml
tasks:
  - name: Shut down CentOS 6 and Debian 7 systems
    ansible.builtin.command: /sbin/shutdown -t now
    when: (ansible_facts['distribution'] == "CentOS" and ansible_facts['distribution_major_version'] == "6") or
          (ansible_facts['distribution'] == "Debian" and ansible_facts['distribution_major_version'] == "7")
```

### 1.2 判断变量是否定义 

判断变量是否定义：

```yaml
tasks:
    - name: Run the command if "foo" is defined
      ansible.builtin.shell: echo "I've got '{{ foo }}' and am not afraid to use it!"
      when: foo is defined

    - name: Fail if "bar" is undefined
      ansible.builtin.fail: msg="Bailing out. This play requires 'bar'"
      when: bar is undefined

```

## 2. 剧本的使用

### 2.1 条件判断的基本使用

以下编写一个脚本测试`when`关键字来进行条件判断。

编写剧本文件`when.yml`：

```yaml
- hosts: node1
  tasks:
    - name: node1 run this task
      ansible.builtin.debug:
        msg: "The hostname is: {{ ansible_hostname }}"
      when: ansible_hostname == "node1"

    - name: Multiple condition
      ansible.builtin.debug:
        msg: The memory is {{ ansible_memtotal_mb }} MB and the core number is {{ ansible_processor_cores }}
      when: ansible_memtotal_mb >= 1000 and ansible_processor_cores == 2

    - name: Create temporary file
      ansible.builtin.tempfile:
        state: file
        suffix: temp
      register: tempfile_1

    - name: Use the registered var and the file module to remove the temporary file
      ansible.builtin.file:
        path: "{{ tempfile_1.path }}"
        state: absent
      when: tempfile_1.path is defined

```

执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint when.yml
[ansible@master ansible_playbooks]$ ansible-playbook when.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [node1 run this task] *********************************************************************************************
ok: [node1] => {
    "msg": "The hostname is: node1"
}

TASK [Multiple condition] **********************************************************************************************
ok: [node1] => {
    "msg": "The memory is 3789 MB and the core number is 2"
}

TASK [Create temporary file] *******************************************************************************************
changed: [node1] => {"changed": true, "gid": 1002, "group": "ansible", "mode": "0600", "owner": "ansible", "path": "/tmp/ansible.2HNv7Ztemp", "size": 0, "state": "file", "uid": 1002}

TASK [Use the registered var and the file module to remove the temporary file] *****************************************
changed: [node1] => {"changed": true, "path": "/tmp/ansible.2HNv7Ztemp", "state": "absent"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

效果图如下：

![](/img/Snipaste_2023-08-06_13-48-39.png)
可以看到，正常获取到了节点的主机名、内存、CPU核心数、临时文件名等信息，并进行`when`条件判断，都执行成功了。

如果我们将剧本文件稍做修改：
```yaml
- hosts: node1
  tasks:
    - name: node2 run this task
      ansible.builtin.debug:
        msg: "The hostname is: {{ ansible_hostname }}"
      when: ansible_hostname == "node2"

    - name: Multiple condition
      ansible.builtin.debug:
        msg: The memory is {{ ansible_memtotal_mb }} MB and the core number is {{ ansible_processor_cores }}
      when: ansible_memtotal_mb >= 4000 and ansible_processor_cores == 2

    - name: Create temporary file
      ansible.builtin.tempfile:
        state: file
        suffix: temp
      register: tempfile_1

    - name: Use the registered var and the file module to remove the temporary file
      ansible.builtin.file:
        path: "{{ tempfile_1.path }}"
        state: absent
      when: tempfile_1.path is defined

```

然后再执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint when.yml
[ansible@master ansible_playbooks]$ ansible-playbook when.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [node2 run this task] *********************************************************************************************
skipping: [node1] => {}

TASK [Multiple condition] **********************************************************************************************
skipping: [node1] => {}

TASK [Create temporary file] *******************************************************************************************
changed: [node1] => {"changed": true, "gid": 1002, "group": "ansible", "mode": "0600", "owner": "ansible", "path": "/tmp/ansible.1OkUm6temp", "size": 0, "state": "file", "uid": 1002}

TASK [Use the registered var and the file module to remove the temporary file] *****************************************
changed: [node1] => {"changed": true, "path": "/tmp/ansible.1OkUm6temp", "state": "absent"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，由于`[node2 run this task]`和`[Multiple condition]`任务的条件判断不成立，没有运行这两个任务。


### 2.2 限定运行节点

另外，我们可以通过在主机清单中某些节点上指定变量，然后当剧本文件中通过`when`条件判断，判断该变量是否定义，如果定义了则可以让该节点运行任务。

请看下面示例：

以下配置在主机清单中增加了个变量：

```ini
[ansible@master ~]$ cat /etc/ansible/hosts
[myhosts]
node1 ansible_hostname=node1.ansible.com ansible_user=ansible ansible_port=22 node_name=mynode1
[ansible@master ~]$
```

编写剧本文件`limit_host.yml`：

```yaml
- hosts: all
  tasks:
    - name: node1 run this task with condition
      ansible.builtin.debug:
        msg: "The custom name is: {{ node_name }}"
      when: node_name is defined

    - name: node1
      ansible.builtin.debug:
        msg: "The not_exist_var is not define"
      when: not_exist_var is undefined

```

运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint limit_host.yml
[ansible@master ansible_playbooks]$ ansible-playbook limit_host.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [all] *************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [node1 run this task with condition] ******************************************************************************
ok: [node1] => {
    "msg": "The custom name is: mynode1"
}

TASK [node1] ***********************************************************************************************************
ok: [node1] => {
    "msg": "The not_exist_var is not define"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

运行效果图：

![](/img/Snipaste_2023-08-27_21-22-35.png)

可以看到，当在主机清单中`node1`节点上指定变量`node_name=mynode1`,然后在剧本文件中通过指定`when: node_name is defined`条件，来限定只有定义了`node_name`的节点才能运行该任务！这样就达到了在指定节点运行指定task任务的目的。


### 2.3 限定运行时间

当我们有个任务只能在上午运行时，或者只能在下午运行时，可以使用下面这个剧本来限制任务执行的时间。

对于ansible自带的环境变量，可以通过`setup`模块获取到：

```sh
[ansible@master ansible_playbooks]$ ansible node1 -m setup|grep -A20 'ansible_date_time'
        "ansible_date_time": {
            "date": "2023-08-27",
            "day": "27",
            "epoch": "1693147479",
            "hour": "22",
            "iso8601": "2023-08-27T14:44:39Z",
            "iso8601_basic": "20230827T224439033267",
            "iso8601_basic_short": "20230827T224439",
            "iso8601_micro": "2023-08-27T14:44:39.033267Z",
            "minute": "44",
            "month": "08",
            "second": "39",
            "time": "22:44:39",
            "tz": "CST",
            "tz_offset": "+0800",
            "weekday": "Sunday",
            "weekday_number": "0",
            "weeknumber": "34",
            "year": "2023"
        },
        "ansible_default_ipv4": {
[ansible@master ansible_playbooks]$
```

可以看到，可以通过以下环境变量获取想要的时间信息：

- `ansible_date_time.year`，运行剧本时的年份，上面的值是`2023`。
- `ansible_date_time.month`，运行剧本时的月份，上面的值是`08`。
- `ansible_date_time.day`，运行剧本时的日，上面的值是`27`。
- `ansible_date_time.date`，运行剧本时的日期，上面的值是`2023-08-27`。
- `ansible_date_time.time`，运行剧本时的时间，上面的值是`22:44:39`。
- `ansible_date_time.hour`，运行剧本时的对应的小时值，上面的值是`22`。
- `ansible_date_time.minute`，运行剧本时的对应的分钟值，上面的值是`44`。
- `ansible_date_time.second`，运行剧本时的对应的秒值，上面的值是`39`。

有了以上变量后，我们就可以限定在指定时间执行指定的任务。

请看下面示例。

编写剧本文件`get_date.yml`:

```yaml
- hosts: node1
  tasks:
    - name: print date
      ansible.builtin.debug:
        msg: "The date is: {{ ansible_date_time.date }}"

    - name: print time
      ansible.builtin.debug:
        msg: "The time is: {{ ansible_date_time.time }}"

    - name: print hour
      ansible.builtin.debug:
        msg: "The time is: {{ ansible_date_time.hour }}"

    - name: run between 00:00:00 and 12:00:00
      ansible.builtin.debug:
        msg: "The task run between 00:00:00 and 12:00:00"
      when: ansible_date_time.hour < 12

    - name: run between 12:00:00 and 24:00:00
      ansible.builtin.debug:
        msg: "The task run between 12:00:00 and 24:00:00"
      when: ansible_date_time.hour > 12

```

检查并运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint get_date.yml
[ansible@master ansible_playbooks]$ ansible-playbook get_date.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [print date] ******************************************************************************************************
ok: [node1] => {
    "msg": "The date is: 2023-08-27"
}

TASK [print time] ******************************************************************************************************
ok: [node1] => {
    "msg": "The time is: 23:01:28"
}

TASK [print hour] ******************************************************************************************************
ok: [node1] => {
    "msg": "The time is: 23"
}

TASK [run between 00:00:00 and 12:00:00] *******************************************************************************
skipping: [node1] => {}

TASK [run between 12:00:00 and 24:00:00] *******************************************************************************
ok: [node1] => {
    "msg": "The task run between 12:00:00 and 24:00:00"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

运行效果图如下：

![](/img/Snipaste_2023-08-27_23-03-57.png)

可以看到，最后两个任务只执行了一个，因为当前时间是深夜23点多，只执行了任务`TASK [run between 12:00:00 and 24:00:00]`，而忽略了任务`TASK [run between 00:00:00 and 12:00:00]`，说明我们通过`ansible_date_time.hour`来获取剧本运行的小时数，然后来判断是上午还是下午生效了。以后就可能通过该条件判断，在上午或下午对相同的主机执行不同的操作了！

