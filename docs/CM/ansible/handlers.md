# handlers触发器

[[toc]]

## 0. 场景引入

我们在 [lineinfile文件内容修改模块](./lineinfile.md) 模块中曾经向nginx配置文件最后写入了三行无意义的备注信息：

```sh
[root@node1 ~]# tail -n 3 /etc/nginx/nginx.conf
# Orange
# Apple
# Banana
[root@node1 ~]#
```

本节我们尝试将三行无意义的备注信息去掉，然后再重启Nginx服务，编写ansible剧本`handlers.yml`如下：

```yaml
- hosts: node1
  tasks:
    - name: Delete multiple lines
      ansible.builtin.lineinfile:
        path: /etc/nginx/nginx.conf
        line: "{{ item }}"
        backup: yes
        state: absent
        validate: /usr/sbin/nginx -t -c %s
      with_items:
        - '# Orange'
        - '# Apple'
        - '# Banana'
      become: yes

    - name: Restart Nginx server
      ansible.builtin.service:
        name: nginx
        state: restarted
      become: yes
```

运行一次剧本文件：
```sh
[ansible@master ~]$ cd ansible_playbooks/
[ansible@master ansible_playbooks]$ ansible-lint handlers.yml
[ansible@master ansible_playbooks]$ ansible-playbook handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Delete multiple lines] *******************************************************************************************
changed: [node1] => (item=# Orange)
changed: [node1] => (item=# Apple)
changed: [node1] => (item=# Banana)

TASK [Restart Nginx server] ********************************************************************************************
changed: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

此时，在node1节点查看配置文件以及nginx状态信息：

```sh
[root@node1 ~]# tail -n 3 /etc/nginx/nginx.conf

}

[root@node1 ~]# systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2023-07-08 22:16:43 CST; 12min ago
  Process: 22826 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 22822 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 22820 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 22828 (nginx)
    Tasks: 3
   Memory: 2.0M
   CGroup: /system.slice/nginx.service
           ├─22828 nginx: master process /usr/sbin/nginx
           ├─22829 nginx: worker process
           └─22830 nginx: worker process


Jul 08 22:16:43 node1 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Jul 08 22:16:43 node1 nginx[22822]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Jul 08 22:16:43 node1 nginx[22822]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Jul 08 22:16:43 node1 systemd[1]: Started The nginx HTTP and reverse proxy server.
[root@node1 ~]#
```

可以看到，配置文件已经修改了，最后三行的注释已经没有了，然后nginx服务也在22:16:43重启了。

我们再次执行一次剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-playbook handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Delete multiple lines] *******************************************************************************************
ok: [node1] => (item=# Orange)
ok: [node1] => (item=# Apple)
ok: [node1] => (item=# Banana)

TASK [Restart Nginx server] ********************************************************************************************
changed: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

此时，再在节点node1查看配置文件信息和nginx服务信息：
```sh
[root@node1 ~]# tail -n 3 /etc/nginx/nginx.conf

}

[root@node1 ~]# systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2023-07-08 22:30:57 CST; 34s ago
  Process: 26713 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 26709 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 26707 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 26715 (nginx)
    Tasks: 3
   Memory: 2.0M
   CGroup: /system.slice/nginx.service
           ├─26715 nginx: master process /usr/sbin/nginx
           ├─26716 nginx: worker process
           └─26717 nginx: worker process

Jul 08 22:30:57 node1 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Jul 08 22:30:57 node1 nginx[26709]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Jul 08 22:30:57 node1 nginx[26709]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Jul 08 22:30:57 node1 systemd[1]: Started The nginx HTTP and reverse proxy server.
[root@node1 ~]#
```

此时可以看到，配置文件没有变化，但nginx服务在22:30:57重启了。此时就有个问题，无论`Delete multiple lines`任务是否修改了nginx的配置文件，后面的`Restart Nginx server`任务都会执行。

我们期望的是当配置文件发生变化时，我们才执行后面的重启nginx服务任务。如果配置文件没有发生变化，则不用执行nginx重启任务。

这个时候`handlers`触发器就派上用场了！！

## 1. handlers简介

- 在Ansible中，handlers是一种特殊类型的任务，用于在Playbook的最后执行一些特定的操作。Handlers通常用于响应其他任务的事件或变化，例如服务重启或配置文件更改。有点像代码中的条件语句，只有满足某条件后才执行！
- `handlers`和`tasks`很类似，但是只能被`tasks`通知时才会触发运行！
- `handlers`只会在任务执行完成后执行，即使被通知了很多次，也只会执行一次！只有当任务真正`changed`时，才能触发后面的`handlers`里面的任务的执行。
- 官方文档请参考 [Handlers: running operations on change](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html#handlers-running-operations-on-change)

## 2. 官方示例

```yaml
---
- name: Verify apache installation
  hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  remote_user: root
  tasks:
    - name: Ensure apache is at the latest version
      ansible.builtin.yum:
        name: httpd
        state: latest

    - name: Write the apache config file
      ansible.builtin.template:
        src: /srv/httpd.j2
        dest: /etc/httpd.conf
      notify:
        - Restart apache

    - name: Ensure apache is running
      ansible.builtin.service:
        name: httpd
        state: started

  handlers:
    - name: Restart apache
      ansible.builtin.service:
        name: httpd
        state: restarted
```

在该示例中，当httpd升级到最新版本，并修改配置文件后，才通知重启httpd服务。

## 3. handlers触发器的使用

### 3.1 未配置notify通知参数

为了使用handlers触发器，我们将nginx配置文件最后一行写入`# Orange`：

```sh
[root@node1 ~]# echo '# Orange' >> /etc/nginx/nginx.conf
[root@node1 ~]# tail /etc/nginx/nginx.conf
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}

# Orange
[root@node1 ~]# ll /etc/nginx/nginx.conf
-rw-r--r-- 1 root root 2473 Jul  8 22:58 /etc/nginx/nginx.conf
[root@node1 ~]#
```

我们修改一下`handlers.yml`文件，只删除文件最后一行内容：

```yaml
- hosts: node1
  tasks:
    - name: Delete multiple lines
      ansible.builtin.lineinfile:
        path: /etc/nginx/nginx.conf
        line: "{{ item }}"
        state: absent
      with_items:
        - '# Orange'
      become: yes

  handlers:
    - name: Restart Nginx server
      ansible.builtin.service:
        name: nginx
        state: restarted
      become: yes
```

执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint handlers.yml
[ansible@master ansible_playbooks]$ ansible-playbook handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Delete multiple lines] *******************************************************************************************
changed: [node1] => (item=# Orange)

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

此时，可以看到`Restart Nginx server`任务并没有被执行！

查看一下node1节点上的配置文件和时间信息：
```sh
[root@node1 ~]# tail /etc/nginx/nginx.conf
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}

[root@node1 ~]# ll /etc/nginx/nginx.conf
-rw-r--r-- 1 root root 2464 Jul  8 23:01 /etc/nginx/nginx.conf
[root@node1 ~]#
```

可以看到，最后一行被执行，文件时间发生了变化。

- 当没有配置`notify`通知参数时，虽然设置了`handlers`触发器，但触发器中的任务并不会被执行！

### 3.2 使用notify通知参数

再次将node1节点上的配置还原，并查看文件时间和nginx服务状态：
```sh
[root@node1 ~]# echo '# Orange' >> /etc/nginx/nginx.conf
[root@node1 ~]# tail /etc/nginx/nginx.conf
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}

# Orange
[root@node1 ~]# ll /etc/nginx/nginx.conf
-rw-r--r-- 1 root root 2473 Jul  8 23:09 /etc/nginx/nginx.conf
[root@node1 ~]# systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2023-07-08 22:30:57 CST; 39min ago
  Process: 26713 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 26709 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 26707 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 26715 (nginx)
    Tasks: 3
   Memory: 2.1M
   CGroup: /system.slice/nginx.service
           ├─26715 nginx: master process /usr/sbin/nginx
           ├─26716 nginx: worker process
           └─26717 nginx: worker process

Jul 08 22:30:57 node1 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Jul 08 22:30:57 node1 nginx[26709]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Jul 08 22:30:57 node1 nginx[26709]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Jul 08 22:30:57 node1 systemd[1]: Started The nginx HTTP and reverse proxy server.
[root@node1 ~]#
```

然后，修改`handlers.yml`剧本文件：

```yaml
- hosts: node1
  tasks:
    - name: Delete multiple lines
      ansible.builtin.lineinfile:
        path: /etc/nginx/nginx.conf
        line: "{{ item }}"
        state: absent
      with_items:
        - '# Orange'
      become: yes
      notify:
        - Restart Nginx server

  handlers:
    - name: Restart Nginx server
      ansible.builtin.service:
        name: nginx
        state: restarted
      become: yes
```

此时第一次执行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint handlers.yml
[ansible@master ansible_playbooks]$ ansible-playbook handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Delete multiple lines] *******************************************************************************************
changed: [node1] => (item=# Orange)

RUNNING HANDLER [Restart Nginx server] *********************************************************************************
changed: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到`TASK [Delete multiple lines]`的状态是`changed`，即做了实际的改变，此时触发器执行了任务`Restart Nginx server`,即重启了nginx服务。

我们去节点node1上检查一下：

```sh
[root@node1 ~]# tail /etc/nginx/nginx.conf
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}

[root@node1 ~]# ll /etc/nginx/nginx.conf
-rw-r--r-- 1 root root 2464 Jul  8 23:12 /etc/nginx/nginx.conf
[root@node1 ~]# systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
   Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
   Active: active (running) since Sat 2023-07-08 23:12:19 CST; 2min 44s ago
  Process: 4463 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
  Process: 4459 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
  Process: 4457 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
 Main PID: 4465 (nginx)
    Tasks: 3
   Memory: 2.0M
   CGroup: /system.slice/nginx.service
           ├─4465 nginx: master process /usr/sbin/nginx
           ├─4466 nginx: worker process
           └─4467 nginx: worker process

Jul 08 23:12:19 node1 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Jul 08 23:12:19 node1 nginx[4459]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Jul 08 23:12:19 node1 nginx[4459]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Jul 08 23:12:19 node1 systemd[1]: Started The nginx HTTP and reverse proxy server.
[root@node1 ~]#
```

可以看到，nginx配置文件是最后一行的`# Orange`被删除了，nginx服务也被重启了！

我们再次执行一次剧本文件，看看效果是什么：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Delete multiple lines] *******************************************************************************************
ok: [node1] => (item=# Orange)

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

此时，可以看到`TASK [Delete multiple lines] `任务的状态是`ok`，并没有真正的发生`changed`改变，所以此时没有触发任务`Restart Nginx server`的执行。

此时，再去查看node1节点上的配置文件时间信息以及nginx服务的时间信息，发现都没有发生变化！

这就说明了，当nginx配置发生变化时，才执行nginx服务的重启；当nginx配置未发生变化时，不执行nginx服务的重启任务，这就是`handlers`触发器的作用！

## 4. handler触发器其他说明

### 4.1 notify机制

- `tasks`任务可以通过使用`notify`关键字来设置一个或多个`handlers`触发器程序。
- 当任务真正发生改变时(状态是`changed`)时触发器就会触发对应的任务执行。
- `notify`关键字接受`handlers`名称列表或者`handlers`名称字符串。
- `handler`执行的顺序与`handler`在playbook中定义的顺序是相同的，与”handler被notify”的顺序无关。
- 如果相同的`handler`被通知多次时，最终只执行一次。例如，如果多个任务更新配置文件并通知重启`Apache`服务，Ansible只会重启一次`Apache`服务，避免没必要的多次重启服务。

以下示例是配置文件发生变化后，通知重启`memcached`和`httpd`服务：

```yaml
tasks:
- name: Template configuration file
  ansible.builtin.template:
    src: template.j2
    dest: /etc/foo.conf
  notify:
    - Restart apache
    - Restart memcached

handlers:
  - name: Restart memcached
    ansible.builtin.service:
      name: memcached
      state: restarted

  - name: Restart apache
    ansible.builtin.service:
      name: apache
      state: restarted
```

为了测试通知机制，我们在节点node1上面安装一下`memcached`包并启动服务：

```sh
[root@node1 ~]# yum install -y memcached
[root@node1 ~]# systemctl start memcached
[root@node1 ~]# systemctl status memcached|grep Active
   Active: active (running) since Sun 2023-07-09 09:22:34 CST; 16min ago
```
可以看到memcached服务在09:22:34启动了！

查看一下nginx服务状态：

```sh
[root@node1 ~]# systemctl status nginx|grep Active
   Active: active (running) since Sun 2023-07-09 09:34:36 CST; 4min 7s ago
[root@node1 ~]#
```
可以看到nginx服务是2023-07-09 09:34:36启动的。

我们修改一下官方示例，得到以下剧本文件`notify_handlers.yml`:

```yaml
- hosts: node1
  tasks:
    - name: Template configuration file 1
      ansible.builtin.template:
        src: handlers_template.j2
        dest: /etc/handlers_1.conf
      # notify接受触发器任务名称列表
      notify:
        - Restart nginx
        - Restart memcached
      become: yes

    - name: Template configuration file 2
      ansible.builtin.template:
        src: handlers_template.j2
        dest: /etc/handlers_2.conf
      # notify接受触发器任务名称字符串
      notify: Restart nginx
      become: yes

  handlers:
    - name: Restart memcached
      ansible.builtin.service:
        name: memcached
        state: restarted
      become: yes

    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
      become: yes
```

创建模板文件：

```sh
[ansible@master ansible_playbooks]$ echo "test notify handlers" > templates/handlers_template.j2
[ansible@master ansible_playbooks]$ cat templates/handlers_template.j2
test notify handlers
[ansible@master ansible_playbooks]$
```

此时运行剧本：
```sh
[ansible@master ansible_playbooks]$ ansible-lint notify_handlers.yml
[ansible@master ansible_playbooks]$ ansible-playbook notify_handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Template configuration file 1] ***********************************************************************************
changed: [node1]

TASK [Template configuration file 2] ***********************************************************************************
changed: [node1]

RUNNING HANDLER [Restart memcached] ************************************************************************************
changed: [node1]

RUNNING HANDLER [Restart nginx] ****************************************************************************************
changed: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

通过本次剧本的执行，可以验证以下几点：

- `notify`接受触发器任务名称列表，如`notify: - Restart nginx`这样，`notify`也接受触发器任务名称字符串，如`notify: Restart nginx`这样。
- 在任务`Template configuration file 1`中需要通知`Restart nginx`和`Restart memcached`两个触发器任务，在`Template configuration file 2`中需要通知`Restart nginx`触发器任务，`Restart nginx`触发器任务被通知了多次，但最终执行效果中可以看到`Restart nginx`触发器任务只执行了一次！**说明触发器任务最多只执行一次，不会执行多次！**
- 在任务`Template configuration file 1`中需要通知`Restart nginx`和`Restart memcached`两个触发器任务，`Restart nginx`触发器任务在前，`Restart memcached`触发器任务在后，但实际执行时，是先执行`RUNNING HANDLER [Restart memcached]`,后执行`RUNNING HANDLER [Restart nginx]`，即与`notify`中定义的顺序无关，而是与`handlers`中定义的任务顺序相同，即在`handlers`中先定义的任务先执行，后定义的任务后执行。

此时，在节点node1上面检查生成的配置文件以及服务情况：

```sh
[root@node1 ~]# ll /etc/handlers_*
-rw-r--r-- 1 root root 21 Jul  9 09:40 /etc/handlers_1.conf
-rw-r--r-- 1 root root 21 Jul  9 09:40 /etc/handlers_2.conf
[root@node1 ~]# cat /etc/handlers_1.conf
test notify handlers
[root@node1 ~]# cat /etc/handlers_2.conf
test notify handlers
[root@node1 ~]# systemctl status memcached|grep Active
   Active: active (running) since Sun 2023-07-09 09:40:06 CST; 1min 8s ago
[root@node1 ~]# systemctl status nginx|grep Active
   Active: active (running) since Sun 2023-07-09 09:40:06 CST; 1min 15s ago
[root@node1 ~]#
```

可以看到，配置文件生成成功，并且`memcached`和`nginx`服务都在`2023-07-09 09:40:06`的时候启动了！说明触发器中的任务执行了。

再次执行一次剧本文件：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook notify_handlers.yml

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Template configuration file 1] ***********************************************************************************
ok: [node1]

TASK [Template configuration file 2] ***********************************************************************************
ok: [node1]

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

由于上一次执行剧本时，已经生成了配置文件，这次不会重新生成，因此`TASK [Template configuration file 1]`和`TASK [Template configuration file 2]`任务的状态都是`ok`，不是`changed`，因此不会触发后面触发器任务。

### 4.2 命名触发器

- `handlers`触发器任务必须设置全局唯一的名称，这样`tasks`任务就可以通过`notify`通知这些触发器任务。
- `handlers`触发器可以使用`listen`关键字来监听由多个触发器任务组成的组主题。
- 通过使用`listen`关键字，使得同时通知多个触发器任务变得更容易，无论这些触发器任务命名成什么都没有关系。

以下是在任务执行完成后，执行重启web服务的示例：

```yaml
- hosts: node1
  tasks:
    - name: Restart everything
      command: echo "this task will restart the web services"
      notify: "restart web services"
      become: yes
      # [301] Commands should not change things if nothing needs doing
      register: myoutput
      changed_when: myoutput.rc == 0

  handlers:
    - name: Restart memcached
      ansible.builtin.service:
        name: memcached
        state: restarted
      listen: "restart web services"
      become: yes

    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
      listen: "restart web services"
      become: yes
```

在执行剧本前，在节点node1上面查看nginx和memecached服务的状态信息：

```sh
[root@node1 ~]# systemctl status memcached|grep Active
   Active: active (running) since Sun 2023-07-09 09:40:06 CST; 13h ago
[root@node1 ~]# systemctl status nginx|grep Active
   Active: active (running) since Sun 2023-07-09 09:40:06 CST; 13h ago
[root@node1 ~]#
```

然后执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-playbook naming_handlers.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Restart everything] **********************************************************************************************
changed: [node1] => {"changed": true, "cmd": ["echo", "this task will restart the web services"], "delta": "0:00:00.010154", "end": "2023-07-09 23:06:21.326729", "rc": 0, "start": "2023-07-09 23:06:21.316575", "stderr": "", "stderr_lines": [], "stdout": "this task will restart the web services", "stdout_lines": ["this task will restart the web services"]}

RUNNING HANDLER [Restart memcached] ************************************************************************************
changed: [node1] => {"changed": true, "name": "memcached", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-07-09 09:40:06 CST", "ActiveEnterTimestampMonotonic": "9455685640456", "ActiveExitTimestamp": "Sun 2023-07-09 09:40:06 CST", "ActiveExitTimestampMonotonic": "9455685627167", "ActiveState": "active", "After": "system.slice network.target systemd-journald.socket basic.target", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2023-07-09 09:40:06 CST", "AssertTimestampMonotonic": "9455685635489", "Before": "httpd.service shutdown.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "no", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2023-07-09 09:40:06 CST", "ConditionTimestampMonotonic": "9455685635489", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/memcached.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "Memcached", "DevicePolicy": "auto", "EnvironmentFile": "/etc/sysconfig/memcached (ignore_errors=yes)", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "21492", "ExecMainStartTimestamp": "Sun 2023-07-09 09:40:06 CST", "ExecMainStartTimestampMonotonic": "9455685640423", "ExecMainStatus": "0", "ExecStart": "{ path=/usr/bin/memcached ; argv[]=/usr/bin/memcached -u $USER -p $PORT -m $CACHESIZE -c $MAXCONN $OPTIONS ; ignore_errors=no ; start_time=[Sun 2023-07-09 09:40:06 CST] ; stop_time=[n/a] ; pid=21492 ; code=(null) ; status=0/0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/memcached.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "memcached.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2023-07-09 09:40:06 CST", "InactiveEnterTimestampMonotonic": "9455685627745", "InactiveExitTimestamp": "Sun 2023-07-09 09:40:06 CST", "InactiveExitTimestampMonotonic": "9455685640456", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "control-group", "KillSignal": "15", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "15066", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "15066", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "21492", "MemoryAccounting": "no", "MemoryCurrent": "790528", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "memcached.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "no", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "6", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "30s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "simple", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "disabled", "WatchdogTimestamp": "Sun 2023-07-09 09:40:06 CST", "WatchdogTimestampMonotonic": "9455685640445", "WatchdogUSec": "0"}}

RUNNING HANDLER [Restart nginx] ****************************************************************************************
changed: [node1] => {"changed": true, "name": "nginx", "state": "started", "status": {"ActiveEnterTimestamp": "Sun 2023-07-09 09:40:06 CST", "ActiveEnterTimestampMonotonic": "9455686083958", "ActiveExitTimestamp": "Sun 2023-07-09 09:40:06 CST", "ActiveExitTimestampMonotonic": "9455686040308", "ActiveState": "active", "After": "system.slice network-online.target -.mount remote-fs.target nss-lookup.target basic.target systemd-journald.socket tmp.mount", "AllowIsolate": "no", "AmbientCapabilities": "0", "AssertResult": "yes", "AssertTimestamp": "Sun 2023-07-09 09:40:06 CST", "AssertTimestampMonotonic": "9455686060529", "Before": "shutdown.target multi-user.target", "BlockIOAccounting": "no", "BlockIOWeight": "18446744073709551615", "CPUAccounting": "no", "CPUQuotaPerSecUSec": "infinity", "CPUSchedulingPolicy": "0", "CPUSchedulingPriority": "0", "CPUSchedulingResetOnFork": "no", "CPUShares": "18446744073709551615", "CanIsolate": "no", "CanReload": "yes", "CanStart": "yes", "CanStop": "yes", "CapabilityBoundingSet": "18446744073709551615", "CollectMode": "inactive", "ConditionResult": "yes", "ConditionTimestamp": "Sun 2023-07-09 09:40:06 CST", "ConditionTimestampMonotonic": "9455686060528", "Conflicts": "shutdown.target", "ControlGroup": "/system.slice/nginx.service", "ControlPID": "0", "DefaultDependencies": "yes", "Delegate": "no", "Description": "The nginx HTTP and reverse proxy server", "DevicePolicy": "auto", "ExecMainCode": "0", "ExecMainExitTimestampMonotonic": "0", "ExecMainPID": "21604", "ExecMainStartTimestamp": "Sun 2023-07-09 09:40:06 CST", "ExecMainStartTimestampMonotonic": "9455686083931", "ExecMainStatus": "0", "ExecReload": "{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx -s reload ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 }", "ExecStart": "{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx ; ignore_errors=no ; start_time=[Sun 2023-07-09 09:40:06 CST] ; stop_time=[Sun 2023-07-09 09:40:06 CST] ; pid=21602 ; code=exited ; status=0 }", "ExecStartPre": "{ path=/usr/sbin/nginx ; argv[]=/usr/sbin/nginx -t ; ignore_errors=no ; start_time=[Sun 2023-07-09 09:40:06 CST] ; stop_time=[Sun 2023-07-09 09:40:06 CST] ; pid=21598 ; code=exited ; status=0 }", "FailureAction": "none", "FileDescriptorStoreMax": "0", "FragmentPath": "/usr/lib/systemd/system/nginx.service", "GuessMainPID": "yes", "IOScheduling": "0", "Id": "nginx.service", "IgnoreOnIsolate": "no", "IgnoreOnSnapshot": "no", "IgnoreSIGPIPE": "yes", "InactiveEnterTimestamp": "Sun 2023-07-09 09:40:06 CST", "InactiveEnterTimestampMonotonic": "9455686053191", "InactiveExitTimestamp": "Sun 2023-07-09 09:40:06 CST", "InactiveExitTimestampMonotonic": "9455686064435", "JobTimeoutAction": "none", "JobTimeoutUSec": "0", "KillMode": "process", "KillSignal": "3", "LimitAS": "18446744073709551615", "LimitCORE": "18446744073709551615", "LimitCPU": "18446744073709551615", "LimitDATA": "18446744073709551615", "LimitFSIZE": "18446744073709551615", "LimitLOCKS": "18446744073709551615", "LimitMEMLOCK": "65536", "LimitMSGQUEUE": "819200", "LimitNICE": "0", "LimitNOFILE": "4096", "LimitNPROC": "15066", "LimitRSS": "18446744073709551615", "LimitRTPRIO": "0", "LimitRTTIME": "18446744073709551615", "LimitSIGPENDING": "15066", "LimitSTACK": "18446744073709551615", "LoadState": "loaded", "MainPID": "21604", "MemoryAccounting": "no", "MemoryCurrent": "2215936", "MemoryLimit": "18446744073709551615", "MountFlags": "0", "Names": "nginx.service", "NeedDaemonReload": "no", "Nice": "0", "NoNewPrivileges": "no", "NonBlocking": "no", "NotifyAccess": "none", "OOMScoreAdjust": "0", "OnFailureJobMode": "replace", "PIDFile": "/run/nginx.pid", "PermissionsStartOnly": "no", "PrivateDevices": "no", "PrivateNetwork": "no", "PrivateTmp": "yes", "ProtectHome": "no", "ProtectSystem": "no", "RefuseManualStart": "no", "RefuseManualStop": "no", "RemainAfterExit": "no", "Requires": "system.slice basic.target -.mount", "RequiresMountsFor": "/var/tmp", "Restart": "no", "RestartUSec": "100ms", "Result": "success", "RootDirectoryStartOnly": "no", "RuntimeDirectoryMode": "0755", "SameProcessGroup": "no", "SecureBits": "0", "SendSIGHUP": "no", "SendSIGKILL": "yes", "Slice": "system.slice", "StandardError": "inherit", "StandardInput": "null", "StandardOutput": "journal", "StartLimitAction": "none", "StartLimitBurst": "5", "StartLimitInterval": "10000000", "StartupBlockIOWeight": "18446744073709551615", "StartupCPUShares": "18446744073709551615", "StatusErrno": "0", "StopWhenUnneeded": "no", "SubState": "running", "SyslogLevelPrefix": "yes", "SyslogPriority": "30", "SystemCallErrorNumber": "0", "TTYReset": "no", "TTYVHangup": "no", "TTYVTDisallocate": "no", "TasksAccounting": "no", "TasksCurrent": "3", "TasksMax": "18446744073709551615", "TimeoutStartUSec": "1min 30s", "TimeoutStopUSec": "5s", "TimerSlackNSec": "50000", "Transient": "no", "Type": "forking", "UMask": "0022", "UnitFilePreset": "disabled", "UnitFileState": "enabled", "WantedBy": "multi-user.target", "Wants": "network-online.target", "WatchdogTimestamp": "Sun 2023-07-09 09:40:06 CST", "WatchdogTimestampMonotonic": "9455686083945", "WatchdogUSec": "0"}}

PLAY RECAP *************************************************************************************************************
node1                      : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

此时，在节点node1上面查看服务状态信息：

```sh
[root@node1 ~]# systemctl status memcached|grep Active
   Active: active (running) since Sun 2023-07-09 23:06:22 CST; 2min 0s ago
[root@node1 ~]# systemctl status nginx|grep Active
   Active: active (running) since Sun 2023-07-09 23:06:22 CST; 2min 2s ago
```

可以看到memecached和nginx服务都重启了。

由于`Restart memcached`和`Restart nginx`两个触发器任务的`listen: "restart web services"`监听相同，被认为是相同的组，因此在`Restart everything`任务中使用`notify: "restart web services"`通知触发器时，会通知触发器组下面的所有任务，也就是`Restart memcached`和`Restart nginx`两个触发器任务都会被触发执行。






