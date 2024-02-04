# changed_when与failed_when条件判断

[[toc]]



## 1. 概述

- 与`when`条件语句类似，我们可以使用`changed_when`语句和`failed_when`语句来对命令运行的结果进行判断。对于Ansible来说，其很难判断一个命令的运行是否符合我们的实际预期，尤其是当我们使用`command`模块和`shell`模块时，如果不使用`changed_when`语句，Ansible将永远返回`changed`。大部分模块都能正确返回运行结果是否对目标主机产生影响，我们依然可以使用`changed_when`语句来对返回信息进行重写，根据任务返回结果来判定任务的运行结果是否真正符合我们预期。
- 有一些命令会将自己的运行结果写入标准错误输出`stderr`中，而不是通常的标准输出`stdout`中，这时可以使用`failed_when`来对结果进行判断，从而告诉Ansible真正的运行结果到底是成功还是失败。
- `changed_when`条件判断官方文档 [Defining “changed”](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html#id8) 。
- `failed_when`条件判断官方文档 [Defining failure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html#id7) 。



## 2. 官方示例

### 2.1 changed_when官方示例

- 通过`changed_when`可以让你通过程序退出码或输出结果决定是否向Ansible报告该任务的任务状态为`changed`改变状态。
-  多个 `changed_when` 条件的列表使用隐式`and`连接，这意味着任务仅在满足所有条件时报告更改。 如果要在满足任何条件时报告更改，则必须使用显式`or`运算符。 

```yaml
tasks:

  - name: Report 'changed' when the return code is not equal to 2
    ansible.builtin.shell: /usr/bin/billybass --mode="take me to the river"
    register: bass_result
    changed_when: "bass_result.rc != 2"

  - name: This will never report 'changed' status
    ansible.builtin.shell: wall 'beep'
    changed_when: False
```

你也可以使用多个条件：

```yaml
- name: Combine multiple conditions to override 'changed' result
  ansible.builtin.command: /bin/fake_command
  register: result
  ignore_errors: True
  changed_when:
    - '"ERROR" in result.stderr'
    - result.rc == 2
```



### 2.2 failed_when官方示例

与`changed_when`类似，你可以使用`failed_when`来决定任务在什么情况设置为`failed`状态。

- 您可以通过在命令的输出中搜索单词或短语来检查是否失败。

```yaml
- name: Fail task when the command error output prints FAILED
  ansible.builtin.command: /usr/bin/example-command -x -y -z
  register: command_result
  failed_when: "'FAILED' in command_result.stderr"
```

- 通过退出码（return code）判断是否失败。

```yaml
- name: Fail task when both files are identical
  ansible.builtin.raw: diff foo/file1 bar/file2
  register: diff_cmd
  failed_when: diff_cmd.rc == 0 or diff_cmd.rc >= 2
```

- 混合多个条件同时判断任务是否失败，需要所有条件都为`True`，才认定任务执行失败。

```yaml
- name: Check if a file exists in temp and fail task if it does
  ansible.builtin.command: ls /tmp/this_should_not_be_here
  register: result
  failed_when:
    - result.rc == 0
    - '"No such" not in result.stdout'
```



## 3. 运行剧本



### 3.1 debug模块条件判断

下面我们通过一个示例，使用`debug`模块来输出一些内容，然后查看将输出结果注册到变量中，判断变量内容是否包含指定字符串来改变任务的状态信息。

编写剧本文件`changed_when.yml`：

```yaml
- hosts: node1
  tasks:
    - name: Default message status
      ansible.builtin.debug:
        msg: "The default status"
      register: output

    - name: echo output
      ansible.builtin.debug:
        msg: "{{ output.msg }}"

    - name: Changed status
      ansible.builtin.debug:
        msg: "The changed status"
      register: msg_output
      changed_when: '"The changed status" in msg_output.msg'

    - name: Unchanged status
      ansible.builtin.debug:
        msg: "The unchanged status"
      register: msg_output
      changed_when: '"The changed status" in msg_output.msg'
```

检查并运行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint changed_when.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook changed_when.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] *********************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [node1]

TASK [Default message status] ****************************************************************************************************************************************************************************************************************************************************************
ok: [node1] => {
    "msg": "The default status"
}

TASK [echo output] ***************************************************************************************************************************************************************************************************************************************************************************
ok: [node1] => {
    "msg": "The default status"
}

TASK [Changed status] ************************************************************************************************************************************************************************************************************************************************************************
changed: [node1] => {
    "msg": "The changed status"
}

TASK [Unchanged status] **********************************************************************************************************************************************************************************************************************************************************************
ok: [node1] => {
    "msg": "The unchanged status"
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
node1                      : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$
```

运行效果图：

![](/img/Snipaste_2023-12-10_21-35-32.png)

可以看到：

- 使用`debug`输出message消息时，默认不会是`changed`改变任务状态，而是输出`OK`状态。
- 通过条件判断`changed_when: '"The changed status" in msg_output.msg'`可以看到`msg_output.msg`的值刚好是`"The changed status"`，判断结果为真，`changed_when`条件判断为真，然后任务的状态就被设置为`changed`改变状态。

### 3.2 command模块条件判断

编写一个包含`changed_when`和`failed_when`条件判断的测试剧本`changed_failed.yml`：

```yaml
- hosts: node1
  tasks:
    - name: echo message without condition
      ansible.builtin.command:
        cmd: echo "message"

    - name: echo message
      ansible.builtin.command:
        cmd: echo "message"
      register: result
      changed_when:
        # 条件判断，由于仅仅输出消息，认定任务不是changed状态
        - 1 != 1

    - name: grep not exist string
      ansible.builtin.command:
        # grep 未匹配到任务字符串时，退出码是1
        # 如果选择一行，退出状态为0；如果没有选择行，则为1；如果发生错误，则为2
        cmd: grep 'not exist string' ~/.bashrc
      register: result
      failed_when:
        - result.rc == 2

    - name: grep not exist string without condition
      ansible.builtin.command:
        # grep 未匹配到任务字符串时，退出码是1
        # 如果选择一行，退出状态为0；如果没有选择行，则为1；如果发生错误，则为2
        cmd: grep 'not exist string' ~/.bashrc

```

检查并执行剧本：

```sh
[ansible@ansible ansible_playbooks]$ ansible-lint changed_failed.yml
[ansible@ansible ansible_playbooks]$ ansible-playbook changed_failed.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] *********************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [node1]

TASK [echo message without condition] ********************************************************************************************************************************************************************************************************************************************************
changed: [node1] => {"changed": true, "cmd": ["echo", "message"], "delta": "0:00:00.009926", "end": "2023-12-10 23:01:24.794808", "rc": 0, "start": "2023-12-10 23:01:24.784882", "stderr": "", "stderr_lines": [], "stdout": "message", "stdout_lines": ["message"]}

TASK [echo message] **************************************************************************************************************************************************************************************************************************************************************************
ok: [node1] => {"changed": false, "cmd": ["echo", "message"], "delta": "0:00:00.010097", "end": "2023-12-10 23:01:25.120917", "rc": 0, "start": "2023-12-10 23:01:25.110820", "stderr": "", "stderr_lines": [], "stdout": "message", "stdout_lines": ["message"]}

TASK [grep not exist string] *****************************************************************************************************************************************************************************************************************************************************************
changed: [node1] => {"changed": true, "cmd": ["grep", "not exist string", "~/.bashrc"], "delta": "0:00:00.010260", "end": "2023-12-10 23:01:25.459597", "failed_when_result": false, "msg": "non-zero return code", "rc": 1, "start": "2023-12-10 23:01:25.449337", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

TASK [grep not exist string without condition] ***********************************************************************************************************************************************************************************************************************************************
fatal: [node1]: FAILED! => {"changed": true, "cmd": ["grep", "not exist string", "~/.bashrc"], "delta": "0:00:00.010217", "end": "2023-12-10 23:01:25.804763", "msg": "non-zero return code", "rc": 1, "start": "2023-12-10 23:01:25.794546", "stderr": "", "stderr_lines": [], "stdout": "", "stdout_lines": []}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
node1                      : ok=4    changed=2    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

[ansible@ansible ansible_playbooks]$

```

运行效果图：

![](/img/Snipaste_2023-12-10_23-06-16.png)

可以看到：

- 使用`command`模块时，如果不使用`changed_when`语句，Ansible默认返回`changed`。这从第一个任务`TASK [echo message without condition] `可以看出来。该任务状态是`changed`，输出是黄色的。
- 任务`TASK [echo message]`由于我们通过`changed_when:`条件判断`1 != 1`指定条件永远为`False`，即该任务状态不会是`changed`，任务正常运行，最后输出状态是`ok`，输出是绿色的。
- 任务`TASK [grep not exist string]`也加了`failed_when`条件判断`result.rc == 2`，只有当`grep`程序异常退出码才是2，此时才认为任务失败，虽然没有搜索到对应的关键字`not exist string`,但也不认为该任务失败，按Ansible默认逻辑就认为该任务是`changed`，输出也是黄色的。
- 任务`TASK [grep not exist string without condition] `没有条件判断，因为没有搜索到对应的关键字`not exist string`, `grep`退出码是1，不是0，Ansible认为其非正常退出，因此认为该任务失败了。
- 通过上面的统计，可以知道`changed`任务数为2，`failed`任务数为1，