# ansible loop循环

[[toc]]

## 1. 概述

- ansible循环官方文档 [Loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)
- ansible提供`loop`、`with_<lookup>`、`until`等关键字来多次执行任务。
- ansible在2.5版本中引入了`loop`循环，它尚未完全替代 `with_<lookup>`，但ansible官方建议在大多数用例中使用它。
- ansible并没有废弃`with_<lookup>`,目前认为该语法仍然是有效的。

## 2. loop与with_的区别

> The with_lookup keywords rely on Lookup plugins - even items is a lookup.
> 
> The loop keyword is equivalent to with_list, and is the best choice for simple loops.
> 
> The loop keyword will not accept a string as input, see Ensuring list input for loop: using query rather than lookup.
> 
> Generally speaking, any use of with_\* covered in Migrating from with_X to loop can be updated to use loop.
> 
> Be careful when changing with_items to loop, as with_items performed implicit single-level flattening. You may need to use flatten(1) with loop to match the exact outcome.

即：
- `with_*`依赖`lookup`插件，`items`也是一个`lookup`插件。
- `loop`关键字与`with_list`等价，对于简单循环，使用`loop`是最好的选择。
- `loop`关键字不接受字符串输入。
- 通常来说，使用`with_*`关键字时，也可以使用`loop`进行代替。
- 当从`with_items`转换成`loop`时，需要特别小心。你需要使用`flatten(1)`对列表进行展平。


### 2.1 列表展平

- `flatten`过滤器请参考 [ansible.builtin.flatten filter – flatten lists within a list](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/flatten_filter.html#ansible-builtin-flatten-filter-flatten-lists-within-a-list) 。

 For example, to get the same output as:

```yaml
with_items:
  - 1
  - [2,3]
  - 4
```

转换成`loop`时，需要这样：

```yaml
loop: "{{ [1, [2, 3], 4] | flatten(1) }}"
```

我们来编写`loop.yml`剧本文件，来测试一下：

```yaml
- hosts: node1
  tasks:
    - name: use with_items
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      with_items:
        - 1
        - [2,3]
        - 4

    - name: use loop with flatten
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      loop: "{{ [1, [2, 3], 4] | flatten(1) }}"

    - name: use loop without flatten
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      loop: "{{ [1, [2, 3], 4] }}"

```

检查剧本并运行：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [use with_items] **************************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=2) => {
    "msg": "The number is: 2"
}
ok: [node1] => (item=3) => {
    "msg": "The number is: 3"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}

TASK [use loop with flatten] *******************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=2) => {
    "msg": "The number is: 2"
}
ok: [node1] => (item=3) => {
    "msg": "The number is: 3"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}

TASK [use loop without flatten] ****************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=[2, 3]) => {
    "msg": "The number is: [2, 3]"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

运行效果图：

![](/img/Snipaste_2023-08-30_20-34-02.png)

可以看到，`with_items`默认会将列表的的元素展平1层，子元素`[2,3]`被展平后，当作两个元素`2`和`3`被打印了出来，此时与使用

```yaml
loop: "{{ [1, [2, 3], 4] | flatten(1) }}"
```

等价。当`loop`中没有使用`flatten`过滤器时，子元素被原样打印出来，子元素`[2,3]`被当作一个元素输出了。

为了更深入研究两者的不同，我们修改一下剧本文件内容：

```yaml
- hosts: node1
  tasks:
    - name: use with_items
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      with_items:
        - 1
        - [2,3]
        - 4
        - [[5,6],[7,8]]

    - name: use loop with flatten one level
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      loop: "{{ [1, [2, 3], 4, [[5,6],[7,8]]] | flatten(1) }}"

    - name: use loop with flatten two level
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      loop: "{{ [1, [2, 3], 4, [[5,6],[7,8]]] | flatten(2) }}"

    - name: use loop flatten
      ansible.builtin.debug:
        msg: "The number is: {{ item }}"
      loop: "{{ [1, [2, 3], 4, [[5,6],[7,8]]]|flatten }}"

```

在最后增加了元素`[[5,6],[7,8]]`，然后再次运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ****************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************
ok: [node1]

TASK [use with_items] *******************************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=2) => {
    "msg": "The number is: 2"
}
ok: [node1] => (item=3) => {
    "msg": "The number is: 3"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}
ok: [node1] => (item=[5, 6]) => {
    "msg": "The number is: [5, 6]"
}
ok: [node1] => (item=[7, 8]) => {
    "msg": "The number is: [7, 8]"
}

TASK [use loop with flatten one level] **************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=2) => {
    "msg": "The number is: 2"
}
ok: [node1] => (item=3) => {
    "msg": "The number is: 3"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}
ok: [node1] => (item=[5, 6]) => {
    "msg": "The number is: [5, 6]"
}
ok: [node1] => (item=[7, 8]) => {
    "msg": "The number is: [7, 8]"
}

TASK [use loop with flatten two level] **************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=2) => {
    "msg": "The number is: 2"
}
ok: [node1] => (item=3) => {
    "msg": "The number is: 3"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}
ok: [node1] => (item=5) => {
    "msg": "The number is: 5"
}
ok: [node1] => (item=6) => {
    "msg": "The number is: 6"
}
ok: [node1] => (item=7) => {
    "msg": "The number is: 7"
}
ok: [node1] => (item=8) => {
    "msg": "The number is: 8"
}

TASK [use loop flatten] *********************************************************************************************
ok: [node1] => (item=1) => {
    "msg": "The number is: 1"
}
ok: [node1] => (item=2) => {
    "msg": "The number is: 2"
}
ok: [node1] => (item=3) => {
    "msg": "The number is: 3"
}
ok: [node1] => (item=4) => {
    "msg": "The number is: 4"
}
ok: [node1] => (item=5) => {
    "msg": "The number is: 5"
}
ok: [node1] => (item=6) => {
    "msg": "The number is: 6"
}
ok: [node1] => (item=7) => {
    "msg": "The number is: 7"
}
ok: [node1] => (item=8) => {
    "msg": "The number is: 8"
}

PLAY RECAP ******************************************************************************************************************
node1                      : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到,`with_items`只会展平一层，`[[5,6],[7,8]]`展平后输出`[5,6]`,`[7,8]`两个元素，但不会被再次展平。而:

```yaml
loop: "{{ [1, [2, 3], 4, [[5,6],[7,8]]] | flatten(2) }}"
```
会展平2层，所有数字单独输出了。而:

```yaml
loop: "{{ [1, [2, 3], 4, [[5,6],[7,8]]]|flatten }}"
```
不指定层数时，则将所有子元素全部展平。

### 2.2 loop不一定比with_方便

- 任何需要在`loop`中使用`lookup`的`with_*`语句都不应转换为使用`loop`循环关键字。例如，不要执行以下操作：

```yaml
loop: "{{ lookup('fileglob', '*.txt', wantlist=True) }}"
```

应直接使用以下表达式更简洁：

```yaml
with_fileglob: '*.txt'
```

此时可以看到，使用`with_fileglob`语法更简洁明了！

## 3. 标准循环

### 3.1 简单循环

执行重启任务时，你可以直接在任务中通过将字符串组成的列表写成一个标准循环：

```yaml
- name: Add several users
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    groups: "wheel"
  loop:
     - testuser1
     - testuser2
```

以上示例，会创建`testuser1`和`testuser2`两个用户。

你也可以提前定义一个列表变量，或者写到`vars`块中，然后就可以像下面这样引用列表变量了：

```yaml
loop: "{{ somelist }}"
```

达到的效果，与下面这种创建两个任务的剧本效果是一样的：

```yaml
- name: Add user testuser1
  ansible.builtin.user:
    name: "testuser1"
    state: present
    groups: "wheel"

- name: Add user testuser2
  ansible.builtin.user:
    name: "testuser2"
    state: present
    groups: "wheel"
```

但我们通过循环就可以少写一个任务。

有的插件支持接受列表作为一个参数，像`yum`、`apt`包管理工具，支持列表参数，这时比使用`loop`循环更好。

如下示例：

```yaml
- name: Optimal yum
  ansible.builtin.yum:
    name: "{{ list_of_packages }}"
    state: present

- name: Non-optimal yum, slower and may cause issues with interdependencies
  ansible.builtin.yum:
    name: "{{ item }}"
    state: present
  loop: "{{ list_of_packages }}"
```

此时使用`loop`循环时，可能会出现依赖性问题，安装变得更慢等。

### 3.2 迭代列表子项

如果您有哈希列表，则可以在循环中引用子项。如：

```yaml
- name: Add several users
  ansible.builtin.user:
    name: "{{ item.name }}"
    state: present
    groups: "{{ item.groups }}"
  loop:
    - { name: 'testuser1', groups: 'wheel' }
    - { name: 'testuser2', groups: 'root' }
```

可以看到，通过`item.name`或`item.groups`就可以访问列表子项的`name`和`groups`属性了。

将条件与循环组合时，`when:`语句会针对每个项目单独处理，详细可参考[Using conditionals in loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html#using-conditionals-in-loops)

此处摘取一个示例：

```yaml
tasks:
    - name: Run with items greater than 5
      ansible.builtin.command: echo {{ item }}
      loop: [ 0, 2, 4, 6, 8, 10 ]
      when: item > 5
```

此示例只会输出列表中大于5的元素。

编写剧本文件`with_loop.yml`：

```yaml
- hosts: node1
  tasks:
    - name: Run with items greater than 5
      ansible.builtin.command: echo {{ item }}
      loop: [ 0, 2, 4, 6, 8, 10 ]
      when: item > 5
```

运行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-playbook with_loop.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Run with items greater than 5] ***********************************************************************************
skipping: [node1] => (item=0)  => {"ansible_loop_var": "item", "changed": false, "item": 0, "skip_reason": "Conditional result was False"}
skipping: [node1] => (item=2)  => {"ansible_loop_var": "item", "changed": false, "item": 2, "skip_reason": "Conditional result was False"}
skipping: [node1] => (item=4)  => {"ansible_loop_var": "item", "changed": false, "item": 4, "skip_reason": "Conditional result was False"}
changed: [node1] => (item=6) => {"ansible_loop_var": "item", "changed": true, "cmd": ["echo", "6"], "delta": "0:00:00.011140", "end": "2023-09-03 13:30:34.422449", "item": 6, "rc": 0, "start": "2023-09-03 13:30:34.411309", "stderr": "", "stderr_lines": [], "stdout": "6", "stdout_lines": ["6"]}
changed: [node1] => (item=8) => {"ansible_loop_var": "item", "changed": true, "cmd": ["echo", "8"], "delta": "0:00:00.011377", "end": "2023-09-03 13:30:34.679076", "item": 8, "rc": 0, "start": "2023-09-03 13:30:34.667699", "stderr": "", "stderr_lines": [], "stdout": "8", "stdout_lines": ["8"]}
changed: [node1] => (item=10) => {"ansible_loop_var": "item", "changed": true, "cmd": ["echo", "10"], "delta": "0:00:00.013275", "end": "2023-09-03 13:30:34.933122", "item": 10, "rc": 0, "start": "2023-09-03 13:30:34.919847", "stderr": "", "stderr_lines": [], "stdout": "10", "stdout_lines": ["10"]}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，当item=0/2/4时，没有执行`echo`语句，因为其不满足条件`item>5`,所以被忽略了。

### 3.3 迭代字典

要迭代一个字典，请使用`dict2items`过滤器：

```yaml
- name: Using dict2items
  ansible.builtin.debug:
    msg: "{{ item.key }} - {{ item.value }}"
  loop: "{{ tag_data | dict2items }}"
  vars:
    tag_data:
      Environment: dev
      Application: payment
```

示例打印出一字典的键和键值。

编写剧本文件`loop_dict.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Using dict2items
      ansible.builtin.debug:
        msg: "{{ item.key }} - {{ item.value }}"
      loop: "{{ tag_data | dict2items }}"
      vars:
        tag_data:
          Environment: dev
          Application: payment
```

运行效果：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_dict.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_dict.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Using dict2items] ************************************************************************************************
ok: [node1] => (item={u'key': u'Environment', u'value': u'dev'}) => {
    "msg": "Environment - dev"
}
ok: [node1] => (item={u'key': u'Application', u'value': u'payment'}) => {
    "msg": "Application - payment"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```


## 4. 在循环中注册变量

可以将循环的输出注册到变量中，请看以下示例。

编写剧本文件`loop_register.yml`：

```yaml
- hosts: node1
  tasks:
    - name: Register loop output as a variable
      ansible.builtin.shell: "echo {{ item }}"
      loop:
        - "one"
        - "two"
      register: ECHO

    - name: print variable ECHO
      ansible.builtin.debug:
        msg: "The ECHO value is: {{ ECHO }}"
```

检查并运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_register.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_register.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Register loop output as a variable] ******************************************************************************
changed: [node1] => (item=one) => {"ansible_loop_var": "item", "changed": true, "cmd": "echo one", "delta": "0:00:00.012806", "end": "2023-09-03 22:35:44.884414", "item": "one", "rc": 0, "start": "2023-09-03 22:35:44.871608", "stderr": "", "stderr_lines": [], "stdout": "one", "stdout_lines": ["one"]}
changed: [node1] => (item=two) => {"ansible_loop_var": "item", "changed": true, "cmd": "echo two", "delta": "0:00:00.013549", "end": "2023-09-03 22:35:45.152964", "item": "two", "rc": 0, "start": "2023-09-03 22:35:45.139415", "stderr": "", "stderr_lines": [], "stdout": "two", "stdout_lines": ["two"]}

TASK [print variable ECHO] *********************************************************************************************
ok: [node1] => {
    "msg": "The ECHO value is: {'msg': u'All items completed', 'changed': True, 'results': [{'stderr_lines': [], 'ansible_loop_var': u'item', u'end': u'2023-09-03 22:35:44.884414', 'failed': False, u'stdout': u'one', u'changed': True, u'rc': 0, 'item': u'one', u'cmd': u'echo one', u'stderr': u'', u'delta': u'0:00:00.012806', u'invocation': {u'module_args': {u'creates': None, u'executable': None, u'_uses_shell': True, u'strip_empty_ends': True, u'_raw_params': u'echo one', u'removes': None, u'argv': None, u'warn': True, u'chdir': None, u'stdin_add_newline': True, u'stdin': None}}, 'stdout_lines': [u'one'], u'start': u'2023-09-03 22:35:44.871608'}, {'stderr_lines': [], 'ansible_loop_var': u'item', u'end': u'2023-09-03 22:35:45.152964', 'failed': False, u'stdout': u'two', u'changed': True, u'rc': 0, 'item': u'two', u'cmd': u'echo two', u'stderr': u'', u'delta': u'0:00:00.013549', u'invocation': {u'module_args': {u'creates': None, u'executable': None, u'_uses_shell': True, u'strip_empty_ends': True, u'_raw_params': u'echo two', u'removes': None, u'argv': None, u'warn': True, u'chdir': None, u'stdin_add_newline': True, u'stdin': None}}, 'stdout_lines': [u'two'], u'start': u'2023-09-03 22:35:45.139415'}]}"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

当您使用带有循环的`register`注册变量时，放置在变量中的数据结构将包含一个结果属性，该属性是来自模块的所有响应的列表。 这与使用不带循环的寄存器时返回的数据结构不同。

复杂的循环请参考官方文档。


## 5. 循环主机清单

如果你要对主机清单（Inventory）进行循环，或者对其子集进行循环，你可以使用`loop`和`ansible_play_batch`或`groups`变量来进行循环处理：

编写剧本文件`loop_inventory.yml`：

```yaml
- hosts: all
  tasks:
    - name: Show all the hosts in the inventory
      ansible.builtin.debug:
        msg: "{{ item }}"
      loop: "{{ groups['all'] }}"

    - name: Show all the hosts in the current play
      ansible.builtin.debug:
        msg: "{{ item }}"
      loop: "{{ ansible_play_batch }}"
```

检查并运行：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_inventory.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_inventory.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [all] *************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Show all the hosts in the inventory] *****************************************************************************
ok: [node1] => (item=node1) => {
    "msg": "node1"
}

TASK [Show all the hosts in the current play] **************************************************************************
ok: [node1] => (item=node1) => {
    "msg": "node1"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

由于我测试的时候只有一个节点`node1`，所以就算`hosts；all`指定是所有主机，显示也是只有`node1`一台主机。但可以看到通过`groups['all']`或`ansible_play_batch`变量输出的结果是一样的。

Ansible中的特殊变量，可以参考: [Special Variables](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html)


## 6. 循环控制

- 可以通过`loop_control`关键字对循环进行控制，如控制item标签名称、循环暂停、索引变量等。

### 6.1 设置标签名称

> When looping over complex data structures, the console output of your task can be enormous.

即当循环复杂的数据结构时，任务的控制台输出可能会很大，不便于阅读。通过设置标签名称，可以使控制台输出更易读。

我们参考官方示例写一个循环剧本`loop_lebel.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Show servers info
      ansible.builtin.debug:
        msg: "The server name is: {{ item }}"
      loop:
        - name: server1
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb

        - name: server2
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb

```

剧本中对两个服务器信息进行循环处理。

检查并运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_label.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_label.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Show servers info] ***********************************************************************************************
ok: [node1] => (item={u'disks': u'3gb', u'ram': u'15Gb', u'name': u'server1', u'network': {u'nic02': u'10Gb', u'nic01': u'100Gb'}}) => {
    "msg": "The server name is: {u'disks': u'3gb', u'ram': u'15Gb', u'name': u'server1', u'network': {u'nic02': u'10Gb', u'nic01': u'100Gb'}}"
}
ok: [node1] => (item={u'disks': u'3gb', u'ram': u'15Gb', u'name': u'server2', u'network': {u'nic02': u'10Gb', u'nic01': u'100Gb'}}) => {
    "msg": "The server name is: {u'disks': u'3gb', u'ram': u'15Gb', u'name': u'server2', u'network': {u'nic02': u'10Gb', u'nic01': u'100Gb'}}"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

![](/img/Snipaste_2023-09-05_21-34-22.png)

可以看到，此时item对应的标签信息就是循环对象的值，直接输出了服务器字典信息。

下面来设置标签：

```yaml
- hosts: node1
  tasks:
    - name: Show servers info
      ansible.builtin.debug:
        msg: "The server name is: {{ item }}"
      loop:
        - name: server1
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb

        - name: server2
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb
      loop_control:
        label: "{{ item.name }}"

```

此时，通过`loop_control`控制，增加标签:

```yaml
label: "{{ item.name }}"
```

此时运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook loop_label.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ************************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************
ok: [node1]

TASK [Show servers info] ************************************************************************************************
ok: [node1] => (item=server1) => {
    "msg": "The server name is: {u'disks': u'3gb', u'ram': u'15Gb', u'name': u'server1', u'network': {u'nic02': u'10Gb', u'nic01': u'100Gb'}}"
}
ok: [node1] => (item=server2) => {
    "msg": "The server name is: {u'disks': u'3gb', u'ram': u'15Gb', u'name': u'server2', u'network': {u'nic02': u'10Gb', u'nic01': u'100Gb'}}"
}

PLAY RECAP **************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

效果图如下：

![](/img/Snipaste_2023-09-05_21-49-37.png)

可以看到标签信息已经变了，如`item=server1`、`item=server2`，这个时候没有像默认那样显示非常多的信息了，说明标签控制起作用了。



### 6.2 循环内部暂停

可以使用`pause`关键字来控制暂停的秒数。

编写剧本文件`loop_pause.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Show servers info
      ansible.builtin.command:
        cmd: 'echo "The server name is: {{ item.name }}."'
      loop:
        - name: server1
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb

        - name: server2
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb
      loop_control:
        label: "{{ item.name }}"
        # 暂停30秒
        pause: 30
```

执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_pause.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_pause.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ************************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************
ok: [node1]

TASK [Show servers info] ************************************************************************************************
changed: [node1] => (item=server1) => {"ansible_loop_var": "item", "changed": true, "cmd": ["echo", "The server name is: server1."], "delta": "0:00:00.011319", "end": "2023-09-05 22:21:42.923280", "item": {"disks": "3gb", "name": "server1", "network": {"nic01": "100Gb", "nic02": "10Gb"}, "ram": "15Gb"}, "rc": 0, "start": "2023-09-05 22:21:42.911961", "stderr": "", "stderr_lines": [], "stdout": "The server name is: server1.", "stdout_lines": ["The server name is: server1."]}
changed: [node1] => (item=server2) => {"ansible_loop_var": "item", "changed": true, "cmd": ["echo", "The server name is: server2."], "delta": "0:00:00.011203", "end": "2023-09-05 22:22:13.215488", "item": {"disks": "3gb", "name": "server2", "network": {"nic01": "100Gb", "nic02": "10Gb"}, "ram": "15Gb"}, "rc": 0, "start": "2023-09-05 22:22:13.204285", "stderr": "", "stderr_lines": [], "stdout": "The server name is: server2.", "stdout_lines": ["The server name is: server2."]}

PLAY RECAP **************************************************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

效果图：

![](/img/Snipaste_2023-09-05_22-21-59.png)
可以看到，循环第一个item时，中间明显有等待效果，第二个item并没有马上显示出来。

过了段时间后，第二个item也显示出来了：
![](/img/Snipaste_2023-09-05_22-23-02.png)

观察输出结果中的`start`值，服务器`server1`的输出值是`"start": "2023-09-05 22:21:42.911961"`，约为`22:21:43`, 服务器`server2`的输出值是`"start": "2023-09-05 22:22:13.204285"`，约为`22:22:13`，两者相差30秒，说明循环中间真的是暂停了30秒钟了。


### 6.3 设置索引

> To keep track of where you are in a loop, use the index_var directive with loop_control. This directive specifies a variable name to contain the current loop index.

要跟踪循环中的位置，请使用带有`loop_control`的`index_var`指令。 该指令指定一个变量名来包含当前循环索引。

也就是通过`index_var`来指定循环中索引使用的变量名称，通过该变量，就可以获取索引值。

- 索引默认从0开始计算。

请看下示例，编写剧本文件`loop_index.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Count our fruit
      ansible.builtin.debug:
        msg: "{{ item }} with index {{ my_idx }}"
      loop:
        - apple
        - banana
        - pear
      loop_control:
        index_var: my_idx
```

执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_index.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_index.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ************************************************************************************************************

TASK [Gathering Facts] **************************************************************************************************
ok: [node1]

TASK [Count our fruit] **************************************************************************************************
ok: [node1] => (item=apple) => {
    "msg": "apple with index 0"
}
ok: [node1] => (item=banana) => {
    "msg": "banana with index 1"
}
ok: [node1] => (item=pear) => {
    "msg": "pear with index 2"
}

PLAY RECAP **************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，依次输出`apple with index 0`、`banana with index 1`、`pear with index 2`，循环中的索引值从0开始，依次是1、2等等。

### 6.4 扩展循环变量

> As of Ansible 2.8 you can get extended loop information using the extended option to loop control. This option will expose the following information.

从Ansible 2.8版本开始，你可以配置`extended`选项然后获取扩展循环变量信息。

```yaml
loop_control:
  extended: true
```
包括以下变量信息：


| 序号 | 变量                   | 说明                                 |
|------|------------------------|--------------------------------------|
| 1    | ansible_loop.allitems  | 循环列表中所有的元素组成的列表       |
| 2    | ansible_loop.index     | 当前索引号（从1开始计算索引）          |
| 3    | ansible_loop.index0    | 当前索引号（从0开始计算索引）          |
| 4    | ansible_loop.revindex  | 反向索引，当前索引号（从1开始计算索引） |
| 5    | ansible_loop.revindex0 | 反向索引，当前索引号（从0开始计算索引） |
| 6    | ansible_loop.first     | 第一个元素                            |
| 7    | ansible_loop.last      | 最后一个元素                          |
| 8    | ansible_loop.length    | 循环列表长度                         |
| 9    | ansible_loop.previtem  | 前一个元素                            |
| 10   | ansible_loop.nextitem  | 后一个元素                            |


我们来测试一下。

查看ansible版本信息：

```sh
[ansible@master ~]$ ansible --version
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /bin/ansible
  python version = 2.7.5 (default, Nov 16 2020, 22:23:17) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
[ansible@master ~]$
```

当前ansible版本是ansible 2.9.27，说明支持扩展循环变量。

编写剧本文件`loop_extended.yml`:

```yaml
- hosts: node1
  tasks:
    - name: List our programming languages
      ansible.builtin.debug:
        msg: |
          The {{ ansible_loop.index }} language is {{ item }}.
          The length is {{ ansible_loop.length }}.
          The list is {{ ansible_loop.allitems }}.
          The previous item is {{ ansible_loop.previtem }}.
          The following item is {{ ansible_loop.nextitem }}.
      loop:
        - Java
        - Python
        - C++
        - C
        - Golang
        - PHP
      when: 1 < ansible_loop.index < ansible_loop.length
      loop_control:
        extended: true

```

检查并运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint loop_extended.yml
[ansible@master ansible_playbooks]$ ansible-playbook loop_extended.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [List our programming languages] **********************************************************************************
skipping: [node1] => (item=Java)  => {"ansible_loop": {"allitems": ["Java", "Python", "C++", "C", "Golang", "PHP"], "first": true, "index": 1, "index0": 0, "last": false, "length": 6, "nextitem": "Python", "revindex": 6, "revindex0": 5}, "ansible_loop_var": "item", "item": "Java"}
ok: [node1] => (item=Python) => {
    "msg": "The 2 language is Python.\nThe length is 6.\nThe list is [u'Java', u'Python', u'C++', u'C', u'Golang', u'PHP'].\nThe previous item is Java.\nThe following item is C++.\n"
}
ok: [node1] => (item=C++) => {
    "msg": "The 3 language is C++.\nThe length is 6.\nThe list is [u'Java', u'Python', u'C++', u'C', u'Golang', u'PHP'].\nThe previous item is Python.\nThe following item is C.\n"
}
ok: [node1] => (item=C) => {
    "msg": "The 4 language is C.\nThe length is 6.\nThe list is [u'Java', u'Python', u'C++', u'C', u'Golang', u'PHP'].\nThe previous item is C++.\nThe following item is Golang.\n"
}
ok: [node1] => (item=Golang) => {
    "msg": "The 5 language is Golang.\nThe length is 6.\nThe list is [u'Java', u'Python', u'C++', u'C', u'Golang', u'PHP'].\nThe previous item is C.\nThe following item is PHP.\n"
}
skipping: [node1] => (item=PHP)  => {"ansible_loop": {"allitems": ["Java", "Python", "C++", "C", "Golang", "PHP"], "first": false, "index": 6, "index0": 5, "last": true, "length": 6, "previtem": "Golang", "revindex": 1, "revindex0": 0}, "ansible_loop_var": "item", "item": "PHP"}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

运行效果图：

![](/img/Snipaste_2023-09-08_22-30-59.png)
可以看到，当循环第一个元素`Java`时，并没有`previtem`属性，但有`nextitem`属性，其值是第二个元素`Python`，当循环到最后一个元素`PHP`时，没有`nextitem`属性，但有`previtem`属性，其值是第五个元素`Golang`。为了让剧本能够正常运行，特意加了条件判断`when: 1 < ansible_loop.index < ansible_loop.length`，如果不加该条件判断的话，在循环第一个元素`Java`时，会提示`previtem`属性不存在异常。



## 7. 从`with_X`迁移至`loop`

- 在大多数情况下，循环使用`loop`关键字比使用`with_X`样式循环效果更好。


此处不详细展开说明，只是罗列官方的几个示例。

### 7.1 with_list

- `with_list`可以直接使用`loop`代替。

```yaml
- name: with_list
  ansible.builtin.debug:
    msg: "{{ item }}"
  with_list:
    - one
    - two

- name: with_list -> loop
  ansible.builtin.debug:
    msg: "{{ item }}"
  loop:
    - one
    - two
```

### 7.2 with_items

- `with_items`可以使用`loop`和`flatten`过滤器代替。

```yaml
- name: with_items
  ansible.builtin.debug:
    msg: "{{ item }}"
  with_items: "{{ items }}"

- name: with_items -> loop
  ansible.builtin.debug:
    msg: "{{ item }}"
  loop: "{{ items|flatten(levels=1) }}"
```

其他`with_X`关键字请参考官方文档 [Loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)。

