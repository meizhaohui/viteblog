# tags标签

[[toc]]

## 1. 概述

- 如果你有一个超大的playbook剧本文件，有时并不想运行剧本文件中所有的任务，这个时候`tags`标签可以解决这个问题，通过`tags`标签可以运行或者忽略(execute or skip)剧本中的部分任务。
- 你需要给任务添加标签，然后在运行剧本时选项相应的标签。
- 详细可参考官方文档 [Tags](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tags.html)

## 2. 官方示例

- 你可以给任务添加一个或多个标签。
- 你可以在剧本中添加标签，也可以在task任务文件，或者`role`角色中添加标签。

以下示例是不同任务设置不同的标签：

```yaml
tasks:
- name: Install the servers
  ansible.builtin.yum:
    name:
    - httpd
    - memcached
    state: present
  tags:
  - packages
  - webservers

- name: Configure the service
  ansible.builtin.template:
    src: templates/src.j2
    dest: /etc/foo.conf
  tags:
  - configuration

```

- 你也可以给不同的任务设置相同的标签信息。

以下示例中，有3个任务被设置成了相同的标签`ntp`：
```yaml
---
# file: roles/common/tasks/main.yml

- name: Install ntp
  ansible.builtin.yum:
    name: ntp
    state: present
  tags: ntp

- name: Configure ntp
  ansible.builtin.template:
    src: ntp.conf.j2
    dest: /etc/ntp.conf
  notify:
  - restart ntpd
  tags: ntp

- name: Enable and run ntpd
  ansible.builtin.service:
    name: ntpd
    state: started
    enabled: true
  tags: ntp

- name: Install NFS utils
  ansible.builtin.yum:
    name:
    - nfs-utils
    - nfs-util-lib
    state: present
  tags: filesharing

```

如果你在运行剧本时使用`--tags ntp`参数，Ansible只会运行标签为`ntp`的三个任务，第4个任务`Install NFS utils`没有`ntp`标签，将会被忽略，不会执行。

- 你也可以为多个任务组成的块设置标签：

```yaml
# myrole/tasks/main.yml
- name: ntp tasks
  tags: ntp
  block:
  - name: Install ntp
    ansible.builtin.yum:
      name: ntp
      state: present

  - name: Configure ntp
    ansible.builtin.template:
      src: ntp.conf.j2
      dest: /etc/ntp.conf
    notify:
    - restart ntpd

  - name: Enable and run ntpd
    ansible.builtin.service:
      name: ntpd
      state: started
      enabled: true

- name: Install NFS utils
  ansible.builtin.yum:
    name:
    - nfs-utils
    - nfs-util-lib
    state: present
  tags: filesharing

```
以上示例中，在剧本顶层使用`block`定义一个块，并且使用`tags: ntp`来定义块标签为`ntp`。

- 也可以为整个剧本设置一个标签，可参考官方示例。
- 其他关于角色中配置标签的示例，可参考官方文档。


## 3. 使用剧本

请看以下剧本示例，定义三个任务，每个任务设置一个标签：

```yaml
- hosts: node1
  tasks:
    - name: The first task
      ansible.builtin.debug:
        msg: "executed the tag1 task"
      tags: tag1

    - name: The second task
      ansible.builtin.debug:
        msg: "executed the tag2 task"
      tags: tag2

    - name: The third task
      ansible.builtin.debug:
        msg: "executed the tag3 task"
      tags: tag3

    - name: The fourth task
      ansible.builtin.debug:
        msg: "executed the last task that no tag"

```

查看标签相关的命令行帮助信息：

```sh
[ansible@master ~]$ ansible-playbook --help|grep tags
                        [--skip-tags SKIP_TAGS] [-C] [--syntax-check] [-D]
                        [--list-tags] [--step] [--start-at-task START_AT_TASK]
  --list-tags           list all available tags
  --skip-tags SKIP_TAGS
                        only run plays and tasks whose tags do not match these
  -t TAGS, --tags TAGS  only run plays and tasks tagged with these values
[ansible@master ~]$

```

可以看到:

- `--list-tags`会列出所有有效的标签。
- `--skip-tags`仅运行**不**匹配指定标签的任务。
- `-t`或`--tags`仅运行匹配指定标签的任务。

### 3.1 列出所有标签

使用`--list-tags`可以列出所有的标签。

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --list-tags tags.yml

playbook: tags.yml

  play #1 (node1): node1	TAGS: []
      TASK TAGS: [tag1, tag2, tag3]
[ansible@master ansible_playbooks]$
```

此时，可以看到，任务一共有三个标签，`tag1`、`tag2`和`tag3`。

在列表标签时，也可以使用`--list-tasks`列出标签对应的任务名称：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --list-tags --list-tasks tags.yml

playbook: tags.yml

  play #1 (node1): node1	TAGS: []
    tasks:
      The first task	   TAGS: [tag1]
      The second task	TAGS: [tag2]
      The third task	   TAGS: [tag3]
      TASK TAGS: [tag1, tag2, tag3]

```
可以看到，标签对应的任务名称也显示了出来！



### 3.2 执行单个标签对应的任务

- `-t`或`--tags`仅运行匹配指定标签的任务。

我们来尝试运行指定标签对应的任务。

```sh
# 执行tag1标签对应的任务
[ansible@master ansible_playbooks]$ ansible-playbook --tags=tag1 tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The first task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag1 task"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$

# 执行tag2标签对应的任务
[ansible@master ansible_playbooks]$ ansible-playbook --tags=tag2 tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The second task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag2 task"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

# 执行tag3标签对应的任务
[ansible@master ansible_playbooks]$ ansible-playbook --tags=tag3 tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The third task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag3 task"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

### 3.3 执行多个标签对应的任务

如执行`tag1`和`tag2`标签对应的任务：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --tags=tag1,tag2 tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The first task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag1 task"
}

TASK [The second task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag2 task"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$ ansible-playbook --tags tag1,tag2 tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The first task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag1 task"
}

TASK [The second task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag2 task"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$

```

### 3.4 忽略某个标签对应的任务

- `--skip-tags`仅运行**不**匹配指定标签的任务。也就是可以忽略某些标签对应的任务。

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --skip-tags="tag1" tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The second task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag2 task"
}

TASK [The third task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag3 task"
}

TASK [The fourth task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the last task that no tag"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

忽略`tag1`对应的任务时，`The first task`任务没有被执行。`The second task`、`The third task`和`The fourth task`执行了，虽然第4个任务`The fourth task`没有标签名，但也被执行了，即`--skip-tags`只是忽略其匹配的任务，其他任务都是会执行的。

### 3.5 忽略多个标签对应的任务

也可以一次性忽略多个标签：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --skip-tags="tag1,tag2,tag3" tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The fourth task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the last task that no tag"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，此时仅`The fourth task`第4个任务执行了，其他任务被忽略了！

### 3.6 执行有标签的任务

可以使用`--tags tagged`来运行有标签的任务。

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --tags=tagged tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The first task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag1 task"
}

TASK [The second task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag2 task"
}

TASK [The third task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag3 task"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，有标签的`The first task`、`The second task`和`The third task`三个任务执行了，第4个任务`The fourth task`没有标签，没有执行！

### 3.7 执行没有标签的任务

可以使用`--tags untagged`来运行没有标签的任务。

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --tags=untagged tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The fourth task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the last task that no tag"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，仅第4个任务`The fourth task`没有标签，执行了。其他三个任务有标签没有执行！


### 3.8 其他特殊标签

- 当使用`--tags all`时，表示运行所有所有任务，忽略标签。这是Ansible默认的行为。
- `always`标签，是一直会执行的标签。
- `never`标签，是一直不会执行的标签！

```sh
[ansible@master ansible_playbooks]$ ansible-playbook --tags=all tags.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [The first task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag1 task"
}

TASK [The second task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag2 task"
}

TASK [The third task] **************************************************************************************************
ok: [node1] => {
    "msg": "executed the tag3 task"
}

TASK [The fourth task] *************************************************************************************************
ok: [node1] => {
    "msg": "executed the last task that no tag"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，所有任务都执行了！与没有指定`--tag all`的效果一样！

