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



除了使用`ANSIBLE_LIBRARY=./library`来指定模块目录，也可以通过`-M`参数来指定模块目录，示例如下：

```sh
[root@ansible ansible_playbooks]# ansible -M library -m my_test -a 'name=hello new=true' localhost
localhost | CHANGED => {
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}
[root@ansible ansible_playbooks]#
```

和上面使用`ANSIBLE_LIBRARY=./library`来指定模块目录结果是一样的。



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



#### 2.3.1 获取模板帮助信息

主要使用`ansible-doc`命令，先看一下这个使用的帮助信息：

```sh
[root@ansible ~]# ansible-doc --help
usage: ansible-doc [-h] [--version] [-v] [-M MODULE_PATH]
                   [--playbook-dir BASEDIR]
                   [-t {become,cache,callback,cliconf,connection,httpapi,inventory,lookup,netconf,shell,module,strategy,vars}]
                   [-j] [-F | -l | -s | --metadata-dump]
                   [plugin [plugin ...]]

plugin documentation tool

positional arguments:
  plugin                Plugin

optional arguments:
  --metadata-dump       **For internal testing only** Dump json metadata for
                        all plugins.
  --playbook-dir BASEDIR
                        Since this tool does not use playbooks, use this as a
                        substitute playbook directory.This sets the relative
                        path for many features including roles/ group_vars/
                        etc.
  --version             show program's version number, config file location,
                        configured module search path, module location,
                        executable location and exit
  -F, --list_files      Show plugin names and their source files without
                        summaries (implies --list)
  -M MODULE_PATH, --module-path MODULE_PATH
                        prepend colon-separated path(s) to module library (def
                        ault=~/.ansible/plugins/modules:/usr/share/ansible/plu
                        gins/modules)
  -h, --help            show this help message and exit
  -j, --json            Change output into json format.
  -l, --list            List available plugins
  -s, --snippet         Show playbook snippet for specified plugin(s)
  -t {become,cache,callback,cliconf,connection,httpapi,inventory,lookup,netconf,shell,module,strategy,vars}, --type {become,cache,callback,cliconf,connection,httpapi,inventory,lookup,netconf,shell,module,strategy,vars}
                        Choose which plugin type (defaults to "module").
                        Available plugin types are : ('become', 'cache',
                        'callback', 'cliconf', 'connection', 'httpapi',
                        'inventory', 'lookup', 'netconf', 'shell', 'module',
                        'strategy', 'vars')
  -v, --verbose         verbose mode (-vvv for more, -vvvv to enable
                        connection debugging)

See man pages for Ansible CLI options or website for tutorials
https://docs.ansible.com
[root@ansible ~]#
```

我们主要关注以下几个参数：

- `-M MODULE_PATH, --module-path MODULE_PATH`，指定模块路径。
- `-s, --snippet`,  显示指定插件的剧本片段。
- `-j, --json`，以json格式输出。

##### 2.3.1.1  获取模块剧本片段

我们来测试一下：

```sh
[root@ansible ansible_playbooks]# ansible-doc -M library -s my_test
- name: This is my test module
  my_test:
      name:                  # (required) This is the message to send to the test module.
      new:                   # Control to demo if the result of this module is changed or not. Parameter description can be a list as well.
[root@ansible ansible_playbooks]#
```

可以看到，在`-M library`指定了模块路径为`libraray`，并指定`-s`获取剧本版本后，能够正常输出剧本版本信息。

##### 2.3.1.2 获取json格式输出

增加`-j`参数，则会以json格式输出：

```sh
[root@ansible ansible_playbooks]# ansible-doc -M library -j -s my_test 
{
    "my_test": {
        "doc": {
            "author": [
                "Your Name (@yourGitHubHandle)"
            ],
            "description": "This is my longer description explaining my test module.",
            "filename": "/root/ansible_playbooks/library/my_test.py",
            "has_action": false,
            "module": "my_test",
            "options": {
                "name": {
                    "description": "This is the message to send to the test module.",
                    "required": true,
                    "type": "str"
                },
                "new": {
                    "description": [
                        "Control to demo if the result of this module is changed or not.",
                        "Parameter description can be a list as well."
                    ],
                    "required": false,
                    "type": "bool"
                }
            },
            "short_description": "This is my test module",
            "version_added": "1.0.0"
        },
        "examples": "\n# Pass in a message\n- name: Test with a message\n  my_namespace.my_collection.my_test:\n    name: hello world\n\n# pass in a message and have changed true\n- name: Test with a message and changed output\n  my_namespace.my_collection.my_test:\n    name: hello world\n    new: true\n\n# fail the module\n- name: Test failure of the module\n  my_namespace.my_collection.my_test:\n    name: fail me\n",
        "metadata": {
            "status": [
                "preview"
            ],
            "supported_by": "community"
        },
        "return": {
            "message": {
                "description": "The output message that the test module generates.",
                "returned": "always",
                "sample": "goodbye",
                "type": "str"
            },
            "original_message": {
                "description": "The original name param that was passed in.",
                "returned": "always",
                "sample": "hello world",
                "type": "str"
            }
        }
    }
}
[root@ansible ansible_playbooks]#
```

使用`jq`命令会使json字符串更美观，效果如下：

![Snipaste_2024-03-24_17-28-04.png](/img/Snipaste_2024-03-24_17-28-04.png)

可以看到，以json格式输出，可以获取到更详细的帮助信息。而这些信息则是从我们模块源文件的`DOCUMENTATION`、`EXAMPLES`和`RETURN`这几个关键定义中获取的。

#### 2.3.2 测试模块传参

由以下代码：

```python
	module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )
```

可以知道，模块支持两个参数：`name`和`new`。

在2.2小节中，用了几种方法来测试模块是否能够正常使用。此处为了方便测试，此处使用2.2.2中Ad-hoc命令来测试。

```sh
ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' localhost
```

此时不需要与远程工作节点交换。

##### 2.3.2.1 传参测试

现在来对比传递不同的参数的输出结果：

```sh
# 由于有new=true参数，代码中result['changed'] = True将变更设置为`True`
# 此时满足变更条件，最终变更输出为`true`
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello new=true' localhost
localhost | CHANGED => {
    "changed": true,
    "message": "goodbye",
    "original_message": "hello"
}

# 由于没有设置new参数，则使用了`default=False`默认值False
# 此时不满足变更条件，最终变更输出为`false`
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=hello' localhost
localhost | SUCCESS => {
    "changed": false,
    "message": "goodbye",
    "original_message": "hello"
}

# 传输一个不存在的参数notexist，提示该参数不支持，应使用name或new参数
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'notexist=hello' localhost
localhost | FAILED! => {
    "changed": false,
    "msg": "Unsupported parameters for (my_test) module: notexist Supported parameters include: name, new"
}

# 只传输name参数，new参数则会使用默认的False
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=true' localhost
localhost | SUCCESS => {
    "changed": false,
    "message": "goodbye",
    "original_message": "true"
}

# 只传输name参数，new参数则会使用默认的False
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=1' localhost
localhost | SUCCESS => {
    "changed": false,
    "message": "goodbye",
    "original_message": "1"
}

# 一个参数也不提供，则会提示需要提供name参数
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test  localhost
localhost | FAILED! => {
    "changed": false,
    "msg": "missing required arguments: name"
}

# 可以使用多种方式表示布尔值
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=test new=false' localhost
localhost | SUCCESS => {
    "changed": false,
    "message": "goodbye",
    "original_message": "test"
}

# 可以使用多种方式表示布尔值
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=test new=True' localhost
localhost | CHANGED => {
    "changed": true,
    "message": "goodbye",
    "original_message": "test"
}

# 可以使用多种方式表示布尔值
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=test new=1' localhost
localhost | CHANGED => {
    "changed": true,
    "message": "goodbye",
    "original_message": "test"
}

# 传输异常布尔值，提示异常
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name=test new="a"' localhost
localhost | FAILED! => {
    "changed": false,
    "msg": "argument new is of type <type 'str'> and we were unable to convert to bool: The value 'a' is not a valid boolean.  Valid booleans include: 0, 'on', 'f', 'false', 1, 'no', 'n', '1', '0', 't', 'y', 'off', 'yes', 'true'"
}
[root@ansible ansible_playbooks]#
```

![Snipaste_2024-03-24_17-51-32.png](/img/Snipaste_2024-03-24_17-51-32.png)



##### 2.3.2.2 异常测试

测试异常：

```sh
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name="fail me" new=y' localhost
localhost | FAILED! => {
    "changed": true,
    "message": "goodbye",
    "msg": "You requested this to fail",
    "original_message": "fail me"
}
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name="fail me" new=n' localhost
localhost | FAILED! => {
    "changed": false,
    "message": "goodbye",
    "msg": "You requested this to fail",
    "original_message": "fail me"
}
[root@ansible ansible_playbooks]#
```

![Snipaste_2024-03-24_22-37-00.png](/img/Snipaste_2024-03-24_22-37-00.png)

此时可以看到，当传输`name="fail me"`参数后，任务执行失败。

##### 2.3.2.3 检查模式测试

测试检查模式，只用在命令后加上`-C`参数：

```sh

[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name="fail me" new=n' localhost -C
localhost | SUCCESS => {
    "changed": false,
    "message": "",
    "original_message": ""
}
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_test -a 'name="hello" new=true' localhost -C
localhost | SUCCESS => {
    "changed": false,
    "message": "",
    "original_message": ""
}
[root@ansible ansible_playbooks]#
```

可以看到，此时模块并没有获取我们传输的参数，直接输出了`changed`为`false`。

## 3. 创建facts模块

### 3.1 编写自定义facts模块

facts模块是在普通模块的基础上，有以下要求：

- 模块命名为`*_facts`。

- 返回值是`ansible_facts`。

为了编写一个我自己的facts模块，对示例Python文件进行修改。

先复制示例文件：

```sh
[root@ansible ansible_playbooks]# cp -p library/my_test.py library/my_facts.py
[root@ansible ansible_playbooks]#
```

然后修改模块文件：

```python
#!/usr/bin/python

# 版权和开源协议信息
# Copyright: (c) 2024, Zhaohui Mei <mzh.whut@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

# 模块的描述信息，如名称以及简短的描述
DOCUMENTATION = r'''
---
module: my_facts

short_description: 我的第一个facts模块

# 注意，如果将这个模块作为collection的一部分，则应使用语义版本控制
# version_added: 版本信息
# description: 解释模板的长的描述信息
# options: 可选参数，包括参数名称、描述、是否可选、类型等信息
# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: 这是我根据官方示例改造的第一个facts模块.

options:
    name:
        description: 自定义模块一个参数的名称.
        required: true
        type: str
    flag:
        description:
            - 控制变更开关.
            - 参数描述也可以写多行.
        required: false
        type: bool
# 根据你的collection来指定下面这个值
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
# extends_documentation_fragment:
#     - my_namespace.my_collection.my_doc_fragment_name

# 作者信息，如姓名(@github地址)
author:
    - Zhaohui Mei <mzh.whut@gmail.com>
'''

# 模块示例
EXAMPLES = r'''
# Pass in a message
- name: 测试消息
  my_namespace.my_collection.my_test:
    name: Python

# pass in a message and have changed true
- name: 测试消息和变更
  my_namespace.my_collection.my_test:
    name: Python
    flag: true

# fail the module
- name: 测试异常
  my_namespace.my_collection.my_test:
    name: nothing
'''

# 返回值
RETURN = r'''
# 这些是可能的返回值的示例，通常应该使用其他名称作为返回值
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: 原始name参数的值.
    type: str
    returned: always
    sample: 'Python'
message:
    description: 输出消息.
    type: str
    returned: always
    sample: '你是Python程序员'
ansible_facts:
    description: 自定义的事实变量信息.
    type: dict
    returned: always
    sample: '{"lang": ["Python"]}'
'''

# 模块调用的函数，这个是自定义模块最重要的部分


def run_module():
    # 定义模块使用的参数，包括参数名称、类型、是否可选、默认值等
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        flag=dict(type='bool', required=False, default=False)
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
    # result = dict(
    #     changed=False,
    #     original_message='',
    #     message=''
    # )
    result = dict(
        changed=False,
        original_message='',
        message='',
        ansible_facts={}
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
    result['ansible_facts']["lang"] = module.params['name'].split(',')

    # 使用您需要的任何逻辑来确定该模块是否存在
    # 对你的目标进行了任何修改
    #
    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['flag']:
        result['changed'] = True

    # 模块执行过程中，如果出现异常或者导致失败的条件状态，运行
    # AnsibleModule.fail_json() 传入消息和结果
    #
    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'nothing':
        module.fail_json(msg='你不会任何编程语言', **result)
    else:
        result['message'] = '你会使用%s等程序语言' % module.params['name']
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

然后执行测试：

```sh
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_facts -a 'name="Python" flag=false' localhost
localhost | SUCCESS => {
    "ansible_facts": {
        "lang": [
            "Python"
        ]
    },
    "changed": false,
    "message": "你会使用Python等程序语言",
    "original_message": "Python"
}
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_facts -a 'name="Python,Java" flag=false' localhost
localhost | SUCCESS => {
    "ansible_facts": {
        "lang": [
            "Python",
            "Java"
        ]
    },
    "changed": false,
    "message": "你会使用Python,Java等程序语言",
    "original_message": "Python,Java"
}
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_facts -a 'name="Python,Java,C++" flag=false' localhost
localhost | SUCCESS => {
    "ansible_facts": {
        "lang": [
            "Python",
            "Java",
            "C++"
        ]
    },
    "changed": false,
    "message": "你会使用Python,Java,C++等程序语言",
    "original_message": "Python,Java,C++"
}
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_facts -a 'name="nothing" flag=false' localhost
localhost | FAILED! => {
    "ansible_facts": {
        "lang": [
            "nothing"
        ]
    },
    "changed": false,
    "message": "",
    "msg": "你不会任何编程语言",
    "original_message": "nothing"
}
[root@ansible ansible_playbooks]# ANSIBLE_LIBRARY=./library ansible -m my_facts -a 'name="Python,Java,C++" flag=false' localhost -C
localhost | SUCCESS => {
    "ansible_facts": {},
    "changed": false,
    "message": "",
    "original_message": ""
}
[root@ansible ansible_playbooks]#
```

![Snipaste_2024-03-24_23-56-17.png](/img/Snipaste_2024-03-24_23-56-17.png)

可以看到，有事实变量输出。能正常执行我定义的模块里面的逻辑判断。说明自定义模块能正常工作。

### 3.2 在剧本中使用自定义facts模块

编写剧本文件`test_my_module.yml`：

```yaml
- hosts: basehosts
  tasks:
    - name: Use custom facts module 1
      my_facts:
        name: Python,Java,C++
        flag: false

    - name: Test my custom facts module 1
      ansible.builtin.template:
        src: facts_module.j2
        dest: /tmp/facts_module_1.txt

    - name: Use custom facts module 2
      my_facts:
        name: nothing
        flag: false

    - name: Test my custom facts module 2
      ansible.builtin.template:
        src: facts_module.j2
        dest: /tmp/facts_module_2.txt
```

并在templates目录下创建模板文件`facts_module.j2`：

```sh
{% if lang %}
    {% for i in lang -%}
        你会使用{{ i }} 编程语言
    {%- endfor %}
{% else -%}
    你不会任何编程语言
{%- endif %}
```

检查这两个文件：

```sh
[root@ansible ansible_playbooks]# ll test_my_module.yml templates/facts_module.j2
-rw-r--r--. 1 root root 156 Mar 27 22:39 templates/facts_module.j2
-rw-r--r--. 1 root root 514 Mar 27 22:35 test_my_module.yml
[root@ansible ansible_playbooks]#
```

执行剧本：

```sh

[root@ansible ansible_playbooks]# ansible-playbook -i base_hosts.ini -M library test_my_module.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [basehosts] *****************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121]
ok: [192.168.56.122]
ok: [192.168.56.123]

TASK [Use custom facts module 1] *************************************************************************************************************************************************************************************************************************************************************
ok: [192.168.56.121] => {"ansible_facts": {"lang": ["Python", "Java", "C++"]}, "changed": false, "message": "你会使用Python,Java,C++等程序语言", "original_message": "Python,Java,C++"}
ok: [192.168.56.122] => {"ansible_facts": {"lang": ["Python", "Java", "C++"]}, "changed": false, "message": "你会使用Python,Java,C++等程序语言", "original_message": "Python,Java,C++"}
ok: [192.168.56.123] => {"ansible_facts": {"lang": ["Python", "Java", "C++"]}, "changed": false, "message": "你会使用Python,Java,C++等程序语言", "original_message": "Python,Java,C++"}

TASK [Test my custom facts module 1] *********************************************************************************************************************************************************************************************************************************************************
changed: [192.168.56.122] => {"changed": true, "checksum": "7da6659c8fbb19c09f7220525b64066fc775e0c2", "dest": "/tmp/facts_module_1.txt", "gid": 0, "group": "root", "md5sum": "f86b2cc9eda465f9f22acbfc3ba71c38", "mode": "0644", "owner": "root", "size": 94, "src": "/root/.ansible/tmp/ansible-tmp-1711550474.91-3013-119894515489497/source", "state": "file", "uid": 0}
changed: [192.168.56.123] => {"changed": true, "checksum": "7da6659c8fbb19c09f7220525b64066fc775e0c2", "dest": "/tmp/facts_module_1.txt", "gid": 0, "group": "root", "md5sum": "f86b2cc9eda465f9f22acbfc3ba71c38", "mode": "0644", "owner": "root", "size": 94, "src": "/root/.ansible/tmp/ansible-tmp-1711550474.92-3015-162673818034960/source", "state": "file", "uid": 0}
changed: [192.168.56.121] => {"changed": true, "checksum": "7da6659c8fbb19c09f7220525b64066fc775e0c2", "dest": "/tmp/facts_module_1.txt", "gid": 0, "group": "root", "md5sum": "f86b2cc9eda465f9f22acbfc3ba71c38", "mode": "0644", "owner": "root", "size": 94, "src": "/root/.ansible/tmp/ansible-tmp-1711550474.9-3011-213481204124868/source", "state": "file", "uid": 0}

TASK [Use custom facts module 2] *************************************************************************************************************************************************************************************************************************************************************
fatal: [192.168.56.121]: FAILED! => {"ansible_facts": {"lang": ["nothing"]}, "changed": false, "message": "", "msg": "你不会任何编程语言", "original_message": "nothing"}
fatal: [192.168.56.122]: FAILED! => {"ansible_facts": {"lang": ["nothing"]}, "changed": false, "message": "", "msg": "你不会任何编程语言", "original_message": "nothing"}
fatal: [192.168.56.123]: FAILED! => {"ansible_facts": {"lang": ["nothing"]}, "changed": false, "message": "", "msg": "你不会任何编程语言", "original_message": "nothing"}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************
192.168.56.121             : ok=3    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
192.168.56.122             : ok=3    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
192.168.56.123             : ok=3    changed=1    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

[root@ansible ansible_playbooks]#
```

效果图如下：

![Snipaste_2024-03-27_22-41-54.png](/img/Snipaste_2024-03-27_22-41-54.png)

在节点上面查看文件信息：

```sh
[root@ansible-node1 ~]# ll /tmp/facts_module_1.txt
-rw-r--r-- 1 root root 93 Mar 27 22:51 /tmp/facts_module_1.txt
[root@ansible-node1 ~]# cat /tmp/facts_module_1.txt
    你会使用Python 编程语言你会使用Java 编程语言你会使用C++ 编程语言
[root@ansible-node1 ~]#
```

可以看到，正常将我们通过自定义facts模块指定的事实变量渲染到远程工作节点了。说明我们的自定义模块能够正常工作。

任务`Use custom facts module 2`失败是正常的，因为在模块指指定了只要`name`参数的值是`nothing`，就会将任务的状态设置为失败。

注意，此处不在乎Jinja2渲染细节，详细可参考官方文档 [欢迎来到 Jinja2](https://docs.jinkan.org/docs/jinja2/index.html)

编写其他自定义模块参考本文前述总结即可。