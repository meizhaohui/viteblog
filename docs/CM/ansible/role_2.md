# 第一个role角色

[[toc]]

## 1. 概述

- 在上一节 [ansible role角色(1)](./role.md) 中，我们阅读了官方文档，并且知道了角色相关的概念。从这节开始，我们就开始使用Ansible role功能来搭建自己的自动化环境。



## 2. 编写第一个role角色

### 2.1 编写角色文件

我是在`~/ansible_playbooks`目录下进行一系列测试操作的。为了测试角色，在该目录下创建`roles`目录，我将第一个角色命名为`first_role`。

首先创建`roles`文件夹，用于存放自动编写的各种角色文件。

```sh
[ansible@ansible ~]$ cd ansible_playbooks/
[ansible@ansible ansible_playbooks]$ mkdir -p roles
[ansible@ansible ansible_playbooks]$
```

创建第一个角色文件夹`first_role`：

```sh
[ansible@ansible ansible_playbooks]$ cd roles/
[ansible@ansible roles]$ mkdir -p first_role
[ansible@ansible roles]$
```

创建第一个角色对应的`tasks`文件夹，用于存放对应任务文件：

```sh
[ansible@ansible roles]$ mkdir -p first_role/tasks
```

然后，创建角色任务`main.yml`：

```sh
[ansible@ansible roles]$ touch first_role/tasks/main.yml
```

然后使用vim编辑其内容，任务文件`first_role/tasks/main.yml`内容如下：

```yaml
---
  - name: Say hello
    ansible.builtin.debug:
      msg: "Hello world!"

```

这样一个最简单的role角色就配置好了！！

### 2.2 调用role角色

现在来编写一个调用该角色的playbook剧本文件，命名为`first_role.yml`，将其放在`roles`目录下：

```sh
[ansible@ansible roles]$ touch first_role.yml
```

其内容如下：

```yaml
---
- hosts: node1
  roles:
    - first_role

```

此时`roles`文件夹下，目录结构如下：

```sh
[ansible@ansible roles]$ find
.
./first_role
./first_role/tasks
./first_role/tasks/main.yml
./first_role.yml
[ansible@ansible roles]$
```



检查剧本语法：

```sh
[ansible@ansible roles]$ ansible-lint first_role.yml
```



执行剧本：

```sh
[ansible@ansible roles]$ ansible-playbook first_role.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] *****************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************
ok: [node1]

TASK [first_role : Say hello] ************************************************************************************************
ok: [node1] => {
    "msg": "Hello world!"
}

PLAY RECAP *******************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@ansible roles]$
```

执行效果：

![](/img/Snipaste_2023-11-19_23-01-02.png)

可以看到，一个简单的role角色被我们成功调用了，并成功输入“‘Hello world!’”。



## 3. 总结

- role角色并不关心哪些主机哪些设备使用它，它只是关于一个功能的集合，只需要编写一个playbook去引用role角色即可。
- role角色中的目录，并不是所有目录都是必须的。
- role角色用于层次化、结构化的组织多个playbook。 
- role主要的作用是可以单独的通过一个有组织的结构、通过单独的目录管理如变量、文件、任务、模块、以及处理任务等。
-  roles主要依赖于目录的命名和摆放，默认tasks/main.yml是所有任务的人口，使用roles的过程也可以认为是目录规范化命名的过程。 
-  在实际的工作当中，一个完整的项目实际上是很多功能体的组合，如果将所有的功能写在一个playbook中会存在如代码耦合程度高、playbook长而维护成本大、灵活性低等一系列的问题。 我们使用role角色可以解决这个问题。

后续随着我们对role理解得更加深入后，我们可以编写出更加复杂功能更加强大的角色。



我们一起努力吧。

