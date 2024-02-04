# role角色

[[toc]]

## 1. 概述

- Ansible 在1.2版本以后就支持了role角色。在实际工作中有很多不同业务需要编写很多playbook剧本文件，如果时间一久，对些剧本文件很难进行维护，这个时候我们就可以采用role角色的方式管理playbook剧本。
- role角色是对日常使用的playbook的目录结构进行一些规范。
- role角色官方文档[Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#playbooks-reuse-roles)



## 2. 角色目录结构

- Ansible角色具有定义的目录结构，其中包含8个主要标准目录。每个角色中必须至少包含一个这样的目录。您可以省略角色中不使用的任何目录。
- 默认情况下，Ansible 将在角色内的每个目录中查找`main.yml`文件以获取相关内容,也可以命名为`main.yaml`或`main`。

目录结构说明：


|序号| 名称                | 类型 | 说明                                     |
|----|-------------------|----|----------------------------------------|
| 1 | tasks             | 目录 | 保存角色功能实现任务所在的目录                        |
| 1 | tasks/main.yml    | 文件 | 角色的入口文件，执行角色时会从此文件开始执行                 |
| 2 | handlers          | 目录 | 触发器目录                                       |
| 2 | handlers/main.yml | 文件 | 存放触发器配置文件                                       |
| 3 | library          | 目录 | 自定义模块目录                                       |
| 3 | library/my_module.py | 文件 | 自己编写的模块文件                                      |
| 4 | defaults          | 目录 | 存放默认配置信息的目录                            |
| 4 | defaults/main.yml | 文件 | 存放默认配置变量的文件，此配置中定义的变量优先级最低                            |
| 5 | vars              | 目录 | 保存变量配置信息的目录                            |
| 5 | vars/main.yml     | 文件 | 用于保存变量配置信息，可以重写默认配置文件中定义的变量                             |
| 6 | files             | 目录 | 存放文件的目录，在此目录下copy等模块可以直接使用             |
| 6 | files/main.yml    | 文件 | 角色部署文件            |
| 7 | templates         | 目录 | 存放模版文件的目录                       |
| 7 | templates/main.yml | 文件 | 模版文件                       |
| 9 | meta              | 目录 | 存放元信息相关的配置文件的目录                        |
| 9 | meta/main.yml     | 文件 | 存放此模块的一些元信息，比如所支持的Ansible最小版本以及操作系统类型等 |
| 10 | tests             | 目录 | 存放角色测试相关的内容的目录                         |
| 10 | tests/inventory   | 文件 | 测试所使用的inventory文件                      |
| 10 | tests/test.yml    | 文件 | 测试所使用的playbook                         |
| 11 | README.md         | 文件 | 用于模块说明和介绍的文件                           |


- 你也可以在文件夹中添加其他YAML文件。

如你可以将平台独有的任务写到单独的YAML文件中，然后在`tasks/main.yml`中引用，就像下面这样：

```yaml
# roles/example/tasks/main.yml
- name: Install the correct web server for RHEL
  import_tasks: redhat.yml
  when: ansible_facts['os_family']|lower == 'redhat'

- name: Install the correct web server for Debian
  import_tasks: debian.yml
  when: ansible_facts['os_family']|lower == 'debian'

# roles/example/tasks/redhat.yml
- name: Install web server
  ansible.builtin.yum:
    name: "httpd"
    state: present

# roles/example/tasks/debian.yml
- name: Install web server
  ansible.builtin.apt:
    name: "apache2"
    state: present

```

可以看到，该示例中，`redhat`和`debian`操作系统使用的包安装方式不一样，因此分开到两个不同的YAML文件中，然后在`roles/example/tasks/main.yml`文件中使用`import_tasks: redhat.yml`或`import_tasks: debian.yml`进行了任务导入。

- Role角色也可以包含自定义模块或者其他插件类型的文件，这些文件可以存放到`library`目录下。可参考 [Embedding modules and plugins in roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#embedding-modules-and-plugins-in-roles) 。

自定义模块目录结构：

```
roles/
    my_custom_modules/
        library/
            module1
            module2
```

在角色中使用模块：

```yaml
---
- hosts: webservers
  roles:
    - my_custom_modules
    - some_other_role_using_my_custom_modules
    - yet_another_role_using_my_custom_modules

```


## 3. 存储和查找角色文件

默认情况下，Ansible按以下顺序来查找角色文件：

- 如果你使用了`collections`，即内容集。详情可参考 [什么是 Ansible 内容集](https://www.redhat.com/zh/technologies/management/ansible/ansible-content-collections)。
- 剧本文件所在目录下的`roles`目录。
- `roles_path`配置中定义的路径，默认是`~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles`。
- 剧本文件所在目录。

如果你存储的角色文件不在以上默认路径中，建议通过修改`roles_path`配置来定义角色路径，这样方便Ansible找到你的角色文件。

查看默认`roles_path`配置信息：

```sh
[ansible@ansible ~]$ grep roles_path /etc/ansible/ansible.cfg
#roles_path    = /etc/ansible/roles
```
可以看到，默认为`/etc/ansible/roles`。


当然，你也可以使用绝对路径来指定角色路径：

```yaml
---
- hosts: webservers
  roles:
    - role: '/path/to/my/roles/common'
```

## 4. 使用roles角色

你可以像下面三种方式这样使用roles角色：

- 在playbook剧本层面，使用`roles`选项，这是使用roles角色最常用的方式。
- 在tasks任务层面，使用`include_role`，在剧本中可以**动态**重用该角色。
- 在tasks任务层面，使用`import_role`，在剧本中可以**静态**重用该角色。 

### 4.1 在playbook剧本层面使用角色

使用角色的经典（原始）方法是在剧本中使用`roles`角色选项：

```yaml
---
- hosts: webservers
  roles:
    - common
    - webservers
```

当你在playbook脚本层面使用`roles`选项时，对于每一个角色`x`：

>  - If roles/x/tasks/main.yml exists, Ansible adds the tasks in that file to the play.
>  - If roles/x/handlers/main.yml exists, Ansible adds the handlers in that file to the play.
>  - If roles/x/vars/main.yml exists, Ansible adds the variables in that file to the play.
>  - If roles/x/defaults/main.yml exists, Ansible adds the variables in that file to the play.
>  - If roles/x/meta/main.yml exists, Ansible adds any role dependencies in that file to the list of roles.
>  - Any copy, script, template or include tasks (in the role) can reference files in roles/x/{files,templates,tasks}/ (dir depends on task) without having to path them relatively or absolutely.

即：

- 如果定义了`tasks`任务、`handlers`触发器、`vars`变量、`defaults`默认值、`meta`元数据等的话，Ansible就会把它们添加到剧本中。
- 任何复制、脚本、模板、或者包含的任务都可以使用相对或绝对路径。

当您在剧本级别使用角色选项时，Ansible 会将角色视为静态导入，并在剧本解析期间处理它们。 Ansible 按以下顺序执行每个剧本：

> - Any pre_tasks defined in the play.
> - Any handlers triggered by pre_tasks.
> - Each role listed in roles:, in the order listed. Any role dependencies defined in the role’s meta/main.yml run first, subject to tag filtering and conditionals. See Using role dependencies for more details.
> - Any tasks defined in the play.
> - Any handlers triggered by the roles or tasks.
> - Any post_tasks defined in the play.
> - Any handlers triggered by post_tasks.

即：

- 任何`pre_tasks`定义的前置任务。
- 任何由前置任务触发的handlers触发器。
- 在`roles`角色中定义的每一个role角色，按罗列顺序执行。
- 定义在剧本中的`tasks`任务。
- 任何由角色或`tasks`任务触发的handlers触发器。

特别要注意的是，如果你在任务中使用标签了，那么在`pre_tasks`或`post_tasks`或依赖项中也应定义相应的标签信息。详细可参考 [Tags](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html#adding-tags-to-roles)。

你也可以给`roles`选项传递其他关键字参数。如:

```yaml
---
- hosts: webservers
  roles:
    - common
    - role: foo_app_instance
      vars:
        dir: '/opt/a'
        app_port: 5000
      tags: typeA
    - role: foo_app_instance
      vars:
        dir: '/opt/b'
        app_port: 5001
      tags: typeB

```

> When you add a tag to the role option, Ansible applies the tag to ALL tasks within the role.
> When using vars: within the roles: section of a playbook, the variables are added to the play variables, making them available to all tasks within the play before and after the role. This behavior can be changed by DEFAULT_PRIVATE_ROLE_VARS.

- 当你向`role`选项中添加`tag`标签时，Ansible会将这个标签应用到角色中所有的任务。
- 当在`roles`中使用`vars`变量时，这些定义的变量将会被添加到剧本变量中，这些变量可以应用在剧本所有任务中。该行为可以通过`DEFAULT_PRIVATE_ROLE_VARS`环境变量来进行改变。



### 4.2 include_role 动态重用角色

>  You can reuse roles dynamically anywhere in the `tasks` section of a play using `include_role`. While roles added in a `roles` section run before any other tasks in a play, included roles run in the order they are defined. If there are other tasks before an `include_role` task, the other tasks will run first. 

您可以在剧本的`tasks`任务部分的任何位置使用`include_role`动态重用角色。虽然在`roles`角色部分中添加的角色会先执行，但包含在剧本的`role`角色会按任务定义先后顺序来执行。如果`include_role`任务之前还有其他任务，则其他任务将首先运行。

示例：

```yaml
---
- hosts: webservers
  tasks:
    - name: Print a message
      ansible.builtin.debug:
        msg: "this task runs before the example role"

    - name: Include the example role
      include_role:
        name: example

    - name: Print a message
      ansible.builtin.debug:
        msg: "this task runs after the example role"
```

你也可以传递其他参数：

```yaml
---
- hosts: webservers
  tasks:
    - name: Include the foo_app_instance role
      include_role:
        name: foo_app_instance
      vars:
        dir: '/opt/a'
        app_port: 5000
      tags: typeA
  ...
```

将`tag`标记添加到`include_role`任务时，Ansible仅将标记应用于include本身。就像这些任务本身具有`tag`相同的标记，则可以传递-`--tags`来运行运行角色中选定的任务。



你也可以在`include_role`时使用`when`条件判断：

```yaml
---
- hosts: webservers
  tasks:
    - name: Include the some_role role
      include_role:
        name: some_role
      when: "ansible_facts['os_family'] == 'RedHat'"
```



### 4.3 import_role静态导入角色

你也可以在`tasks`任务中使用`import_role`来静态导入角色任务，这种形为与使用`roles`关键字相同。如：

```yaml
---
- hosts: webservers
  tasks:
    - name: Print a message
      ansible.builtin.debug:
        msg: "before we run our role"

    - name: Import the example role
      import_role:
        name: example

    - name: Print a message
      ansible.builtin.debug:
        msg: "after we ran our role"
```

你也可以传递其他参数：

```yaml
---
- hosts: webservers
  tasks:
    - name: Import the foo_app_instance role
      import_role:
        name: foo_app_instance
      vars:
        dir: '/opt/a'
        app_port: 5000
  ...
```

当你给`import_role`增加一个`tag`标签时，相当于是给该角色中所有任务增加一个`tag`标签。



## 5. 角色参数检验

>  Beginning with version 2.11, you may choose to enable role argument validation based on an argument specification. This specification is defined in the `meta/argument_specs.yml` file (or with the `.yaml` file extension). When this argument specification is defined, a new task is inserted at the beginning of role execution that will validate the parameters supplied for the role against the specification. If the parameters fail validation, the role will fail execution. 

从Ansible 2.11开始，你可以选择基于参数规范来启用角色参数检验。该规范在`meta/argument_specs.yml`文件中定义，当该参数规范定义后，当角色执行时，会插入一个新任务来校验参数是否满足规范要求，如果参数校验失败，那么角色将执行失败。

>  Ansible also supports role specifications defined in the role `meta/main.yml` file, as well. However, any role that defines the specs within this file will not work on versions below 2.11. For this reason, we recommend using the `meta/argument_specs.yml` file to maintain backward compatibility. 

Ansible也支持在`mate/main.yml`文件是定义参数规范，但在Ansible 2.11以下版本时不起作用，因此还是建议在`meta/argument_specs.yml`文件中定义参数规范，以保持向后兼容。



### 5.1 参数规范模式

- 必须在`meta/argument_specs.yml`文件顶层 `argument_specs`块中定义参数规范。
- 所以字段必须小写。

 **entry-point-name:** 

- 角色参数名称。
- 为了防止不期望的入口点，此处必须是`main`。
- 名称是需要执行的任务的`basename`,不带`.yml`或`.yaml`后缀。
- `short_description`: 
  - 一个简短、一行的描述。
  - 该描述会显示在`ansible-doc -t role -l`输出结果中。 
- `description`:
  
  - 长描述，可以包含多行。
- `author`:
  
  - 作者信息，如果有多个作者，可以使用多行列表定义作者信息。
- `options`:
  - 附加选项信息，选项通常被称为“参数”或“自变量”。
  - 对于每个角色选项（参数），您可以包括：
    - `option-name`: 参数名称。
    - `description`: 参数的详细描述，它应该是完整的句子。
    - `type`： 参数类型，参数允许的类型，默认是`str`字符串类型，详细可参考 [Argument spec](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#argument-spec) ;如果参数是某种类型的列表，则应指定`elements`。
    - `required`： 是否必需参数，如果值是`true`则参数是必须的；否则参数是可选的。
    - `default`: 默认值。
    
      - 如果`required`参数是`false`或者为空，则可以指定默认值，缺省的话，默认值是`null`。
      - 确保文档中的默认值与代码中的默认值相匹配。角色变量的实际默认值将始终来自`defaults/main.yml`。
      - 除非需要其他信息或条件，否则不得将默认字段列为说明的一部分。
      - 如果该值是布尔值，你应使用`true/false`,以与ansible lint兼容。
    - `choices`：参数可选值。如果为空的话，则不应设置该选项。
    - `elements`: 如果参数类型是`list`的话，则应指定此选项，用于指定列表元素的数据类型。
    - `options`:可选参数，如果该参数是字典或者列表，你可以在该参数中定义参数结构。

参数规范示例：

```yaml
# roles/myapp/meta/argument_specs.yml
---
argument_specs:
  # roles/myapp/tasks/main.yml entry point
  main:
    short_description: The main entry point for the myapp role.
    options:
      myapp_int:
        type: "int"
        required: false
        default: 42
        description: "The integer value, defaulting to 42."

      myapp_str:
        type: "str"
        required: true
        description: "The string value"

  # roles/myapp/tasks/alternate.yml entry point
  alternate:
    short_description: The alternate entry point for the myapp role.
    options:
      myapp_int:
        type: "int"
        required: false
        default: 1024
        description: "The integer value, defaulting to 1024."
```



## 6. 多次执行角色任务

- Ansible在剧本中只执行每个角色一次，即使您多次定义它，除非每个定义在角色上定义的参数不同。例如，Ansible在这样的剧本中只运行一次角色foo：

```yaml
---
- hosts: webservers
  roles:
    - foo
    - bar
    - foo
```

你有两种方式来强制要求Ansible来多次执行角色任务。



### 6.1 传递不同参数

- 如果在每个角色定义中传递不同的参数，Ansible会多次运行该角色。提供不同的变量值与传递不同的角色参数不同。此行为必须使用`roles`关键字，因为`import_role`和`include_role`不接受角色参数。

以下示例中，剧本将运行`foo`角色任务两次：

```yaml
---
- hosts: webservers
  roles:
    - { role: foo, message: "first" }
    - { role: foo, message: "second" }
```

下面的语法也可以运行`foo`角色任务两次：

```yaml
---
- hosts: webservers
  roles:
    - role: foo
      message: "first"
    - role: foo
      message: "second"
```

在以上例子中，Ansible会运行`foo`角色任务两次，因为角色定义了不同的参数。

### 6.2 使用allow_duplicates: true

- 如果在`meta/main.yml`中增加`allow_duplicates: true`选项的话，则也可以多次运行角色任务。

如：

```yaml
# playbook.yml
---
- hosts: webservers
  roles:
    - foo
    - foo

# roles/foo/meta/main.yml
---
allow_duplicates: true
```

在以上例子中，Ansible会运行`foo`角色任务两次，因为我们已经显示地启用了允许重复运行功能。

## 7. 使用角色依赖

- 当你在使用角色时，角色依赖可以自动为你拉取其他角色。
- 角色依赖关系允许您在使用角色时自动引入其他角色。
  角色依赖关系是先决条件，而不是真正的依赖关系。角色没有父/子关系。Ansible加载所有列出的角色，首先运行在`dependencies`依赖项下列出的角色，然后运行列出这些角色的角色。play剧本对象是所有角色的父对象，包括依赖项列表调用的角色。
- 角色依赖存储在`meta/main.yml`文件中，应在指定角色参数检查之前插入的角色和参数列表。

示例：

```yaml
# roles/myapp/meta/main.yml
---
dependencies:
  - role: common
    vars:
      some_parameter: 3
  - role: apache
    vars:
      apache_port: 80
  - role: postgres
    vars:
      dbname: blarg
      other_parameter: 12
```

> Ansible always executes roles listed in `dependencies` before the role that lists them. Ansible executes this pattern recursively when you use the `roles` keyword. For example, if you list role `foo` under `roles:`, role `foo` lists role `bar` under `dependencies` in its meta/main.yml file, and role `bar` lists role `baz` under `dependencies` in its meta/main.yml, Ansible executes `baz`, then `bar`, then `foo`.

即：Ansible总是在列出依赖项的角色之前执行这些角色。当您使用roles关键字时，Ansible会递归地执行此模式。

如果`foo`依赖` bar`，`bar`角色又依赖`baz`，则会先运行`baz`,再运行`bar`，最后再运行`foo`角色。



### 7.1 在剧本中多次执行角色依赖

- Ansible像对待`roles`下重复的角色一样处理重复的角色依赖。
- 除非参数、标签、`when`子句不同，否则Ansible只会执行一次角色依赖，即使角色依赖定义了多次。
- 如果在剧本中，有两个角色都定义了一个第三个角色依赖，Ansible也是执行一次角色依赖，除非你传递不同的参数、标签、`when`子句、或者使用`allow_duplicates: true`进行显示定义允许执行多次。



::: warning 警告

Role deduplication does not consult the invocation signature of parent roles. Additionally, when using `vars:` instead of role params, there is a side effect of changing variable scoping. Using `vars:` results in those variables being scoped at the play level. In the below example, using `vars:` would cause `n` to be defined as `4` throughout the entire play, including roles called before it.

In addition to the above, users should be aware that role de-duplication occurs before variable evaluation. This means that [Lazy Evaluation](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html#term-Lazy-Evaluation) may make seemingly different role invocations equivalently the same, preventing the role from running more than once.

:::

即：

- 当重复执行角色依赖时，如果使用`vars`来定义角色参数，会产生作用域副作用。

如以下示例，会导致整个剧本中n被定义为4，包括开始调用的角色。

`car`角色，依赖`wheel`角色：

```yaml
---
dependencies:
  - role: wheel
    n: 1
  - role: wheel
    n: 2
  - role: wheel
    n: 3
  - role: wheel
    n: 4
```

然后`wheel`角色又依赖两个角色`tire`和`brake`，其`meta/main.yml`包含如下内容：

```yaml
---
dependencies:
  - role: tire
  - role: brake
```

角色`tire`和`brake`的`meta/main.yml`包含如下内容：

```yaml
---
allow_duplicates: true
```

最终执行的结果可能是这样的：

```
tire(n=1)
brake(n=1)
wheel(n=1)
tire(n=2)
brake(n=2)
wheel(n=2)
...
car
```

>  To use `allow_duplicates: true` with role dependencies, you must specify it for the role listed under `dependencies`, not for the role that lists it. In the example above, `allow_duplicates: true` appears in the `meta/main.yml` of the `tire` and `brake` roles. The `wheel` role does not require `allow_duplicates: true`, because each instance defined by `car` uses different parameter values 

即要在正确的位置指定`allow_duplicates: true`参数。

## 8. 在角色中嵌入模块和插件

> This applies only to standalone roles. Roles in collections do not support plugin embedding; they must use the collection’s `plugins` structure to distribute plugins.

- 本节仅应用于独立的角色。collections集合中的角色不支持插件嵌入，他们必须使用collection集合的插件结构来分发插件。

当你编写了一个自定义模块或插件时，你也许希望将其分发作为角色的一部分。比如，你编写了一个模块用来配置公司内部软件，并且你想公司其他同事也能使用你的模块，但又不想告诉别人如何去配置Ansible库路径，你就可以将该模块包含到你 `internal_config`角色当中。



要向角色添加模块或插件，在角色的`tasks`和`handlers`的同级目录，添加一个名为“library”的目录，然后将模块直接包含在“library”目录中。



像下面这样配置目录结构：

```
roles/
    my_custom_modules/
        library/
            module1
            module2
```

该模块将可用于角色本身，以及在此角色之后调用的任何角色，如下所示：

```yaml
---
- hosts: webservers
  roles:
    - my_custom_modules
    - some_other_role_using_my_custom_modules
    - yet_another_role_using_my_custom_modules
```

如有必要，您还可以在角色中嵌入模块，以修改Ansible的核心分发中的模块。



相同的机制，你也可以嵌入自定义的过滤器。像下面这样：

```
roles/
    my_custom_filter/
        filter_plugins
            filter1
            filter2
```

你就可以使用`my_custom_filter`来调用该过滤器。



## 9. 使用Ansible Galaxy分享你的角色

- Ansible Galaxy [https://galaxy.ansible.com/ui/](https://galaxy.ansible.com/ui/) .

- Ansible Galaxy是一个免费网站，用于查找、下载、评级和审查社区开发的各种Ansible角色，是启动自动化项目的好方法。

- Ansible包含其客户端`ansible-galaxy`。Galaxy客户端允许您从Ansible Galaxy下载角色，并为创建自己的角色提供了一个出色的默认框架。

  

![](/img/Snipaste_2023-11-19_19-54-07.png)

通过Galaxy官网可以看到，需要Ansible core版本>=2.13.9 才能下载。

我们查看一下自己的Ansible版本信息：

```sh
[ansible@ansible ~]$ ansible --version
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /bin/ansible
  python version = 2.7.5 (default, Nov 16 2020, 22:23:17) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
[ansible@ansible ~]$ ansible-galaxy --version
ansible-galaxy 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /bin/ansible-galaxy
  python version = 2.7.5 (default, Nov 16 2020, 22:23:17) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
[ansible@ansible ~]$
```

可以看到，版本较低，后期可以升级版本后再尝试使用Galaxy。

