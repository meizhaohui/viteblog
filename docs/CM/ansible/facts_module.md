# 编写facts模块

[[toc]]

## 1. 概述

- 在[setup事实变量模块](./setup.md)中我们可以自定义fact事实变量，但该方式灵活性不是很强，因为需要每台机器上都存在一个那样的文件。
- 本节我们通过编写模块的方式收集facts信息。就是相当于自己写一个功能跟`setup`模块类似的模块。
- 如果只是编写facts信息采集，编写流程很简单，只需要按照编写module模块的要求编写即可，唯一要求是在最后需要把所有的facts信息(JSON格式)存储到`ansible_facts` key下。
- 官方文档 ansible 2.9版本 [Ansible module development: getting started](https://docs.ansible.com/ansible/2.9/dev_guide/developing_modules_general.html)。
- 官方文档ansible 9版本 [Developing modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html) 

### 1.1 VirtualBox虚拟机信息记录

我使用以下虚拟机进行测试。详细可参考 [一步一步学role角色-base基础角色配置](./role_3.md)

| 序号 | 虚拟机         | 主机名  | IP             | CPU  | 内存 | 说明             |
| ---- | -------------- | ------- | -------------- | ---- | ---- | ---------------- |
| 1    | ansible-master | ansible | 192.168.56.120 | 2核  | 4G   | Ansible控制节点  |
| 2    | ansible-node1  | node1   | 192.168.56.121 | 2核  | 2G   | Ansible工作节点1 |
| 3    | ansible-node2  | node2   | 192.168.56.122 | 2核  | 2G   | Ansible工作节点2 |
| 4    | ansible-node3  | node3   | 192.168.56.123 | 2核  | 2G   | Ansible工作节点3 |

## 2. 创建一个模块的步骤

### 2.1 官方示例

- 强烈推荐你使用`venv`或`virtualenv`来进行Python开发。（即不影响系统默认环境）

为了创建一个模块，需要做以下步骤：

> 1. Create a `library` directory in your workspace, your test play should live in the same directory.
> 2. Create your new module file: `$ touch library/my_test.py`. Or just open/create it with your editor of choice.
> 3. Paste the content below into your new module file. It includes the [required Ansible format and documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#developing-modules-documenting), a simple [argument spec for declaring the module options](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec), and some example code.
> 4. Modify and extend the code to do what you want your new module to do. See the [programming tips](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html#developing-modules-best-practices) and [Python 3 compatibility](https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html#developing-python-3) pages for pointers on writing clean and concise module code.

即：

1. 在你的工作空间创建一个`library`的文件夹，你用于测试的剧本文件也应在这个工作空间目录下。
2. 创建模块文件 `$ touch library/my_test.py`.
3. 将以下示例代码粘贴到该模块文件中。 
4. 修改或扩展示例代码，使其能满足你的要求。

我们直接参考官方文档ansible 9版本的示例，编写`my_test.py`模块文件：

```py
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```

创建一个信息或事实模块，官方有以下要求：

> [Creating an info or a facts module](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#id3)
>
> Ansible gathers information about the target machines using facts  modules, and gathers information on other objects or files using info  modules. If you find yourself trying to add `state: info` or `state: list` to an existing module, that is often a sign that a new dedicated `_facts` or `_info` module is needed.
>
> In Ansible 2.8 and onwards, we have two type of information modules, they are `*_info` and `*_facts`.
>
> If a module is named `_facts`, it should be because its main purpose is returning `ansible_facts`. Do not name modules that do not do this with `_facts`. Only use `ansible_facts` for information that is specific to the host machine, for example  network interfaces and their configuration, which operating system and  which programs are installed.
>
> Modules that query/return general information (and not `ansible_facts`) should be named `_info`. General information is non-host specific information, for example  information on online/cloud services (you can access different accounts  for the same online service from the same host), or information on VMs  and containers accessible from the machine, or information on individual files or programs.
>
> Info and facts modules, are just like any other Ansible Module, with a few minor requirements:
> 1. They MUST be named `something_info`  or `something_facts`, where`something`  is singular.
> 2. Info `*_info` modules MUST return in the form of the [result dictionary](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values) so other modules can access them.
> 3. Fact `*_facts` modules MUST return in the `ansible_facts` field of the [result dictionary](https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values) so other modules can access them.
> 4. They MUST support [check_mode](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html#check-mode-dry).
> 5. They MUST NOT make any changes to the system.
> 6. They MUST document the [return fields](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#return-block) and [examples](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#examples-block).
>
> The rest is just like creating a normal module.

大意是：

- Ansible通过facts事实模块，可以收集目标主机上面的信息，也可以使用info信息模块来获取其他对象或文件。
- Ansible 2.8之后，就有两种类型的信息模块，一种是`*_info`，另一种是`*_facts`。
- 如是是`*_facts`模块，则是事实变量模块，返回值应该是`ansible_facts`。
- 它们要支持检查模式；不能对系统产生变更；必须包含返回值。

我们先不管上面这些，直接看官方文档后面的内容。



### 2.2 校验模块

校验模块大致可分为以下几个步骤：

- 使用远程工作节点校验你的模块。
- 使用Ansible控制节点校验你的模块。
- 不通过Ansible来校验模块使用的Python文件。
- 通过playbook剧本文件来校验模块。



#### 2.2.1 使用Ad-hoc命令测试-使用远程工作节点校验模块


最简单的测试方法是使用ansible 的Ad-hoc命令：

```sh
ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' remotehost
```

我们来测试一下。

先看一下相关的文件：

```sh
# 查看主机清单文件
[root@ansible ansible_playbooks]# cat base_hosts.ini
[basehosts]
192.168.56.121 hostname=ansible-node1
192.168.56.122 hostname=ansible-node2
192.168.56.123 hostname=ansible-node3

# 查看自定义库目录下的文件
[root@ansible ansible_playbooks]# ll library/
total 8
-rw-r--r--. 1 root root 4173 Mar 21 21:23 my_test.py
[root@ansible ansible_playbooks]#
```

`library/my_test.py`目录的文件内容就是官方示例的内容。我未作任务修改。

直接按官方给定的命令来执行，注意，执行时，将`remotehost`换成`-i base_hosts.ini all`:

```sh
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a "name=hello new=true" -i base_hosts.ini all
192.168.56.121 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}
192.168.56.122 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}
192.168.56.123 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}
[root@ansible ansible_playbooks]#
```

可以看到，剧本正常执行了，且有输出。三个工作节点输出结果是一样的。

#### 2.2.2 使用Ad-hoc命令测试-使用Ansible控制节点校验模块

直接使用Ansible控制节点校验：

执行下面这个命令即可：

```sh
ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' localhost
```

我实际测试下：

```sh
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a "name=hello new=true" localhost
localhost | CHANGED => {
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}
[root@ansible ansible_playbooks]#
```

可以看到， 除了没有`ansible_facts`信息，其他信息和使用工作节点测试是一样的。



#### 2.2.3 不通过Ansible命令直接校验python文件

创建参数json配置文件，然后查看其内容：

```sh
[root@ansible ansible_playbooks]# cat /tmp/args.json
{
    "ANSIBLE_MODULE_ARGS": {
        "name": "hello",
        "new": true
    }
}
```

![Snipaste_2024-03-21_23-05-09.png](/img/Snipaste_2024-03-21_23-05-09.png)

然后直接执行python脚本：

```sh
python library/my_test.py /tmp/args.json
```

实际执行下：

```sh
[root@ansible ansible_playbooks]# python library/my_test.py /tmp/args.json

{"invocation": {"module_args": {"new": true, "name": "hello"}}, "message": "goodbye", "changed": true, "original_message": "hello"}
[root@ansible ansible_playbooks]#
```

可以看到，输出与官方示例稍微有些差异。但也能正常输入。



#### 2.2.4 使用剧本测试模块

创建`testmod.yml`剧本文件 ，并加入以下内容：

```yaml
- name: test my new module
  hosts: localhost
  tasks:
  - name: run the new module
    my_test:
      name: 'hello'
      new: true
    register: testout
  - name: dump test output
    debug:
      msg: '{{ testout }}'

```

查看并执行剧本：

```sh
[root@ansible ansible_playbooks]# cat testmod.yml
- name: test my new module
  hosts: localhost
  tasks:
  - name: run the new module
    my_test:
      name: 'hello'
      new: true
    register: testout
  - name: dump test output
    debug:
      msg: '{{ testout }}'

[root@ansible ansible_playbooks]# ansible-playbook testmod.yml
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [test my new module] ********************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [localhost]

TASK [run the new module] ********************************************************************************************************************************************************************************************************************************************************************
changed: [localhost]

TASK [dump test output] **********************************************************************************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": {
        "changed": true,
        "failed": false,
        "message": "goodbye",
        "original_message": "hello"
    }
}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

![Snipaste_2024-03-21_23-14-56.png](/img/Snipaste_2024-03-21_23-14-56.png)

可以看到，剧本成功执行！！

注意，最后输出的`msg`中多出的`"failed": false,`是在使用`register: testout`注册变量时，Ansible自动加入的信息。 Ansible 中的 `register` 关键字用于注册任务的输出，以便后续的任务可以使用这些输出。当你在 Ansible 中使用 `register` 关键字时，输出通常包含 `failed`、`changed`、`end` 等字段，以表示任务的状态。 



调试通了官方示例代码，下一步就是改变测试逻辑，弄清示例代码每行代码的含义，然后再来写自己的模块。



### 2.3 示例模块剖析

下面我们对示例模块进行深度剖析和修改测试。

首先对示例代码加上中文注释，便于理解：

```python
#!/usr/bin/python

# 版权和开源协议信息
# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

# 模块的描述信息，如名称以及简短的描述
DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# 注意，如果将这个模块作为collection的一部分，则应使用语义版本控制
# version_added: 版本信息
# description: 解释模板的长的描述信息
# options: 可选参数，包括参数名称、描述、是否可选、类型等信息
# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# 根据你的collection来指定下面这个值
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

# 作者信息，如姓名(@github地址)
author:
    - Your Name (@yourGitHubHandle)
'''

# 模块示例
EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

# 返回值
RETURN = r'''
# 这些是可能的返回值的示例，通常应该使用其他名称作为返回值
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

# 模块调用的函数，这个是自定义模块最重要的部分


def run_module():
    # 定义模块使用的参数，包括参数名称、类型、是否可选、默认值等
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # 将结果传递到dict字典对象中
    # 我们主要关心是否产生变更和状态信息
    # 如果模块对目标主机进行了修改，则表明发生了变更
    # 任何你想回传给Ansible的数据信息都可以包含到状态信息中
    # 在后续其他任务中你也可以使用这些状态信息
    #
    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # AnsibleModule对象是我们使用Ansible的抽象
    # 包括实例化、常见属性将会作为参数传递给执行器
    # 并且表明是否该模块是否支持检查模式
    #
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # 如果用户仅在检查模式下使用此模块，我们不对环境进行任何更改，
    # 只需返回当前的没有修改的状态
    #
    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # 根据需要操纵或修改状态
    # 这将是你的模块将做它需要做的事情的部分
    # 也就是说，这里才是自定义模块中自己需要追加或修改的最重要的部分
    #
    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # 使用您需要的任何逻辑来确定该模块是否存在
    # 对你的目标进行了任何修改
    #
    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # 模块执行过程中，如果出现异常或者导致失败的条件状态，运行
    # AnsibleModule.fail_json() 传入消息和结果
    #
    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # 模块正常退出时，传递返回值
    #
    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

```

