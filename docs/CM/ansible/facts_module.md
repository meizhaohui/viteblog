# 编写facts模块

[[toc]]

## 1. 概述

- 在[setup事实变量模块](./setup.md)中我们可以自定义fact事实变量，但该方式灵活性不是很强，因为需要每台机器上都存在一个那样的文件。
- 本节我们通过编写模块的方式收集facts信息。就是相当于自己写一个功能跟`setup`模块类似的模块。
- 如果只是编写facts信息采集，编写流程很简单，只需要按照编写module模块的要求编写即可，唯一要求是在最后需要把所有的facts信息(JSON格式)存储到`ansible_facts` key下。
- 官方文档 ansible 2.9版本 [Ansible module development: getting started](https://docs.ansible.com/ansible/2.9/dev_guide/developing_modules_general.html)。
- 官方文档ansible 9版本 [Developing modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html) 

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
>
> 1. They MUST be named `_info` or `_facts`, where <something> is singular.
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



