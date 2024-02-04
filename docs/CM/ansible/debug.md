# debug调试模块

[[toc]]

## 1. 概要

- 该模块在执行期间打印语句，可用于调试变量或表达式，而不必暂停剧本。
- 与`when: `指令一起调试时很有用。
- Windows服务器上也能使用debug模块。
- 官方帮助文档 [https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html)

## 2. 模块参数

| 参数                    | 可选值           | 默认值                                     | 说明                                                         |
| ----------------------- | ---------------- | ------------------------------------------ | ------------------------------------------------------------ |
| `msg`                   |                  | "Hello world!"                             | `string`，打印的自定义消息。 如果省略，则输出默认消息。      |
| `var`                   |                  |                                            | `string`，要调试的变量名。与msg选项互斥。请注意，此选项已在Jinja2上下文中运行，并且具有隐式`{{}}`包装，因此，除非您要查找双重插值，否则不应使用Jinja2定界符。|
| `verbosity`                   |                  |   0                                         | `integer`，控制调试运行的数字，如果设置为3，则仅在`-vvv`或更高版本时运行调试。|

## 3. 运行剧本

我们参照官方示例，编写剧本并运行剧本。

```yaml
# 查看剧本文件
[ansible@master ~]$ cat debug.yml 
- hosts: node1
  vars:
    password_used: securedockerpassword
  tasks:
    # Example that prints the loopback address and gateway for each host
    - name: prints the loopback address and gateway
      debug:
        msg: System {{ inventory_hostname }} has uuid {{ ansible_product_uuid }}

    - name: print message
      debug:
        msg: System {{ inventory_hostname }} has gateway {{ ansible_default_ipv4.gateway }}
      when: ansible_default_ipv4.gateway is defined

    # Example that prints return information from the previous task
    - name: get the return information
      command:
        cmd: hostname -I
      register: result

    - name: print the result
      debug:
        var: result
        verbosity: 2

    - name: Display all variables/facts known for a host
      debug:
        var: hostvars[inventory_hostname]
        verbosity: 4

    # Example that prints two lines of messages, but only if there is an environment value set
    - debug:
        msg:
        - "Provisioning based on YOUR_KEY which is: {{ lookup('env', 'YOUR_KEY') }}"
        - "These servers were built using the password of '{{ password_used }}'. Please retain this for later use."
```

语法检查：

```sh
# 检查剧本规范，提示有一个异常，看不懂如何修改
[ansible@master ~]$ ansible-lint debug.yml 
[301] Commands should not change things if nothing needs doing
debug.yml:16
Task/Handler: get the return information

[ansible@master ~]$ 
```

在ansible-lint源码网站的issue中查到到了类似的问题[https://github.com/ansible/ansible-lint/issues/165](https://github.com/ansible/ansible-lint/issues/165)，`Handlers should be allows to run shell/command entries without when`，大意是当运行`shell`或`command`命令时，可以不需要带`when`条件判断语句。ansible-lint会去检查有没有带`when`、`changed_when`、`failed_when`之类的参数，参考[Ansible changed_when and failed_when examples](https://www.middlewareinventory.com/blog/ansible-changed_when-and-failed_when-examples/)，上面有很多使用`when`、`changed_when`、`failed_when`条件语句的示例。我们复制几个例子放在下面，你可以看看。

- 只有当操作系统是Debian时才会执行任务

```yaml
tasks:
  - name: "shut down Debian flavored systems"
    command: /sbin/shutdown -t now
    when: ansible_os_family == "Debian"
```

- 只有当httpd服务没有安装时才会执行任务

```yaml
--- 
- hosts: web
  tasks:
  - name: "Determine if the HTTPD is installed"
    register: validatehttpd
    shell: httpd

  - name: Ensure Apache is at the Latest version
    become: yes
    become_user: root
    yum:
      name: httpd
      state: latest
    when: 'not found' in validatehttpd.stdout
```

- 只有当系统是CentOS6或Debian7时才进行关机

```yaml
---
- hosts: all
  tasks:
  - name: "shut down CentOS 6 and Debian 7 systems"
    command: /sbin/shutdown -t now
    when: (ansible_distribution == "CentOS" and ansible_distribution_major_version == "6") or
          (ansible_distribution == "Debian" and ansible_distribution_major_version == "7")
```

- 只有当httpd服务没有启动时才执行任务

```yaml
--- 
- hosts: web
  tasks:
  - name: "Start the Apache HTTPD Server"
    become: true
    become_user: root
    register: starthttpdout
    shell: "httpd -k start"
    changed_when: "'already running' not in starthttpdout.stdout"

  - debug:
      msg: "{{starthttpdout.stdout}}"
```

- 只有当某些包没有安装时才执行任务

```yaml
- name: Install dependencies via Composer.
  command: "/usr/local/bin/composer global require phpunit/phpunit --prefer-dist"
  register: composer
  changed_when: "'Nothing to install or update' not in composer.stdout"
```

- 当服务器不满足硬件要求时任务失败

```yaml
---
- hosts: app
  tasks:
  - name: Making sure the /tmp has more than 1gb
    shell: "df -h /tmp|grep -v Filesystem|awk '{print $4}'|cut -d G -f1"
    register: tmpspace
    failed_when: "tmpspace.stdout|float < 1"

  - name: Making sure the /opt has more than 4gb
    shell: "df -h /opt|grep -v Filesystem|awk '{print $4}'|cut -d G -f1"
    register: tmpspace
    failed_when: "tmpspace.stdout|float < 4"

  - name: Making sure the Physical Memory more than 2gb
    shell: "cat /proc/meminfo|grep -i memtotal|awk '{print $2/1024/1024}'"
    register: memory
    failed_when: "memory.stdout|float < 2"
```

我们在剧本文件中加个`when`条件试一下！

```sh
[ansible@master ~]$ cat debug.yml 
- hosts: node1
  vars:
    password_used: securedockerpassword
  tasks:
    # Example that prints the loopback address and gateway for each host
    - name: prints the loopback address and gateway
      debug:
        msg: System {{ inventory_hostname }} has uuid {{ ansible_product_uuid }}

    - name: print message
      debug:
        msg: System {{ inventory_hostname }} has gateway {{ ansible_default_ipv4.gateway }}
      when: ansible_default_ipv4.gateway is defined

    # Example that prints return information from the previous task
    - name: get the return information
      command:
        cmd: hostname -I
      when: true
      register: result

    - name: print the result
      debug:
        var: result
        verbosity: 2

    - name: Display all variables/facts known for a host
      debug:
        var: hostvars[inventory_hostname]
        verbosity: 4

    # Example that prints two lines of messages, but only if there is an environment value set
    - debug:
        msg:
        - "Provisioning based on YOUR_KEY which is: {{ lookup('env', 'YOUR_KEY') }}"
        - "These servers were built using the password of '{{ password_used }}'. Please retain this for later use."


[ansible@master ~]$ ansible-lint debug.yml 
[ansible@master ~]$ 
```

此时可以看到，使用ansible-lint进行规范检查，没有报任何异常，说明剧本编写正常！

注意，剧本文件中使用了

```sh
{{ lookup('env', 'YOUR_KEY') }}
```
这个是`lookup`模块中读取Ansible服务器（不是远程主机）的环境变量。我们在Ansible master上面设置一下这个变量：

```sh
[ansible@master ~]$ tail -n 1 ~/.bashrc
export YOUR_KEY='myansiblekeyinmaster..432fdsfdsafdsadb'
```

注意，此处在`~/.bashrc`中添加变量后，需要重新加载一下环境：

```sh
[ansible@master ~]$ source ~/.bashrc
[ansible@master ~]$ echo $YOUR_KEY 
myansiblekeyinmaster..432fdsfdsafdsadb
```

我们再来执行一下剧本：

```sh
# 剧本文件语法检查
[ansible@master ~]$ ansible-playbook --syntax-check debug.yml 

playbook: debug.yml


# 执行剧本，查看详情
[ansible@master ~]$ ansible-playbook debug.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] *************************************************************************

TASK [Gathering Facts] ***************************************************************
ok: [node1]

TASK [prints the loopback address and gateway] ***************************************
ok: [node1] => {
    "msg": "System node1 has uuid NA"
}

TASK [print message] *****************************************************************
ok: [node1] => {
    "msg": "System node1 has gateway 10.0.3.2"
}

TASK [get the return information] ****************************************************
changed: [node1] => {"changed": true, "cmd": ["hostname", "-I"], "delta": "0:00:00.002002", "end": "2020-07-27 17:09:02.063072", "rc": 0, "start": "2020-07-27 17:09:02.061070", "stderr": "", "stderr_lines": [], "stdout": "192.168.56.111 10.0.3.15 ", "stdout_lines": ["192.168.56.111 10.0.3.15 "]}

TASK [print the result] **************************************************************
skipping: [node1] => {"skipped_reason": "Verbosity threshold not met."}

TASK [Display all variables/facts known for a host] **********************************
skipping: [node1] => {"skipped_reason": "Verbosity threshold not met."}

TASK [debug] *************************************************************************
ok: [node1] => {
    "msg": [
        "Provisioning based on YOUR_KEY which is: myansiblekeyinmaster..432fdsfdsafdsadb", 
        "These servers were built using the password of 'securedockerpassword'. Please retain this for later use."
    ]
}

PLAY RECAP ***************************************************************************
node1                      : ok=5    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0   

[ansible@master ~]$ 
```

可以看到，`print the result`和`Display all variables/facts known for a host`两个任务并没有执行，忽略的任务数为` skipped=2`,原因是`Verbosity threshold not met.`,即未达到详细程度阈值。我们重新运行时，将命令行中的`-v`改成`-vv`再运行一次：

```sh
[ansible@master ~]$ ansible-playbook debug.yml -vv
ansible-playbook 2.9.9
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 2.7.5 (default, Apr  2 2020, 13:16:51) [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)]
Using /etc/ansible/ansible.cfg as config file

PLAYBOOK: debug.yml ******************************************************************
1 plays in debug.yml

PLAY [node1] *************************************************************************

TASK [Gathering Facts] ***************************************************************
task path: /home/ansible/debug.yml:1
ok: [node1]
META: ran handlers

TASK [prints the loopback address and gateway] ***************************************
task path: /home/ansible/debug.yml:6
ok: [node1] => {
    "msg": "System node1 has uuid NA"
}

TASK [print message] *****************************************************************
task path: /home/ansible/debug.yml:10
ok: [node1] => {
    "msg": "System node1 has gateway 10.0.3.2"
}

TASK [get the return information] ****************************************************
task path: /home/ansible/debug.yml:16
changed: [node1] => {"changed": true, "cmd": ["hostname", "-I"], "delta": "0:00:00.001997", "end": "2020-07-27 17:13:37.686256", "rc": 0, "start": "2020-07-27 17:13:37.684259", "stderr": "", "stderr_lines": [], "stdout": "192.168.56.111 10.0.3.15 ", "stdout_lines": ["192.168.56.111 10.0.3.15 "]}

TASK [print the result] **************************************************************
task path: /home/ansible/debug.yml:22
ok: [node1] => {
    "result": {
        "changed": true, 
        "cmd": [
            "hostname", 
            "-I"
        ], 
        "delta": "0:00:00.001997", 
        "end": "2020-07-27 17:13:37.686256", 
        "failed": false, 
        "rc": 0, 
        "start": "2020-07-27 17:13:37.684259", 
        "stderr": "", 
        "stderr_lines": [], 
        "stdout": "192.168.56.111 10.0.3.15 ", 
        "stdout_lines": [
            "192.168.56.111 10.0.3.15 "
        ]
    }
}

TASK [Display all variables/facts known for a host] **********************************
task path: /home/ansible/debug.yml:27
skipping: [node1] => {"skipped_reason": "Verbosity threshold not met."}

TASK [debug] *************************************************************************
task path: /home/ansible/debug.yml:33
ok: [node1] => {
    "msg": [
        "Provisioning based on YOUR_KEY which is: myansiblekeyinmaster..432fdsfdsafdsadb", 
        "These servers were built using the password of 'securedockerpassword'. Please retain this for later use."
    ]
}
META: ran handlers
META: ran handlers

PLAY RECAP ***************************************************************************
node1                      : ok=6    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

[ansible@master ~]$ 
```

此时可以看到，仅一个任务`skipped=1`被忽略掉，`Display all variables/facts known for a host`被忽略，原因是`Verbosity threshold not met.`,即未达到详细程度阈值。

再查看更详细的日志：

```sh
[ansible@master ~]$ ansible-playbook debug.yml -vvvv
ansible-playbook 2.9.9
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 2.7.5 (default, Apr  2 2020, 13:16:51) [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)]
Using /etc/ansible/ansible.cfg as config file
setting up inventory plugins
host_list declined parsing /etc/ansible/hosts as it did not pass its verify_file() method
script declined parsing /etc/ansible/hosts as it did not pass its verify_file() method
auto declined parsing /etc/ansible/hosts as it did not pass its verify_file() method
Parsed /etc/ansible/hosts inventory source with ini plugin
Loading callback plugin default of type stdout, v2.0 from /usr/lib/python2.7/site-packages/ansible/plugins/callback/default.pyc

PLAYBOOK: debug.yml ******************************************************************
Positional arguments: debug.yml
become_method: sudo
inventory: (u'/etc/ansible/hosts',)
forks: 5
tags: (u'all',)
verbosity: 4
connection: smart
timeout: 10
1 plays in debug.yml

PLAY [node1] *************************************************************************

TASK [Gathering Facts] ***************************************************************
task path: /home/ansible/debug.yml:1
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'echo ~ && sleep 0'"'"''
<node1> (0, '/home/ansible\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'( umask 77 && mkdir -p "` echo /home/ansible/.ansible/tmp `"&& mkdir /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953 && echo ansible-tmp-1595841490.45-4406-255689703212953="` echo /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953 `" ) && sleep 0'"'"''
<node1> (0, 'ansible-tmp-1595841490.45-4406-255689703212953=/home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> Attempting python interpreter discovery
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'echo PLATFORM; uname; echo FOUND; command -v '"'"'"'"'"'"'"'"'/usr/bin/python'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'python3.7'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'python3.6'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'python3.5'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'python2.7'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'python2.6'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'/usr/libexec/platform-python'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'/usr/bin/python3'"'"'"'"'"'"'"'"'; command -v '"'"'"'"'"'"'"'"'python'"'"'"'"'"'"'"'"'; echo ENDFOUND && sleep 0'"'"''
<node1> (0, 'PLATFORM\nLinux\nFOUND\n/usr/bin/python\n/usr/bin/python3.6\n/usr/bin/python2.7\n/usr/libexec/platform-python\n/usr/bin/python3\n/usr/bin/python\nENDFOUND\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'/usr/bin/python && sleep 0'"'"''
<node1> (0, '{"osrelease_content": "NAME=\\"CentOS Linux\\"\\nVERSION=\\"7 (Core)\\"\\nID=\\"centos\\"\\nID_LIKE=\\"rhel fedora\\"\\nVERSION_ID=\\"7\\"\\nPRETTY_NAME=\\"CentOS Linux 7 (Core)\\"\\nANSI_COLOR=\\"0;31\\"\\nCPE_NAME=\\"cpe:/o:centos:centos:7\\"\\nHOME_URL=\\"https://www.centos.org/\\"\\nBUG_REPORT_URL=\\"https://bugs.centos.org/\\"\\n\\nCENTOS_MANTISBT_PROJECT=\\"CentOS-7\\"\\nCENTOS_MANTISBT_PROJECT_VERSION=\\"7\\"\\nREDHAT_SUPPORT_PRODUCT=\\"centos\\"\\nREDHAT_SUPPORT_PRODUCT_VERSION=\\"7\\"\\n\\n", "platform_dist_result": ["centos", "7.6.1810", "Core"]}\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
Using module file /usr/lib/python2.7/site-packages/ansible/modules/system/setup.py
<node1> PUT /home/ansible/.ansible/tmp/ansible-local-4397XWOjgA/tmp6tacW2 TO /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/AnsiballZ_setup.py
<node1> SSH: EXEC sftp -b - -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c '[node1]'
<node1> (0, 'sftp> put /home/ansible/.ansible/tmp/ansible-local-4397XWOjgA/tmp6tacW2 /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/AnsiballZ_setup.py\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug2: Remote version: 3\r\ndebug2: Server supports extension "posix-rename@openssh.com" revision 1\r\ndebug2: Server supports extension "statvfs@openssh.com" revision 2\r\ndebug2: Server supports extension "fstatvfs@openssh.com" revision 2\r\ndebug2: Server supports extension "hardlink@openssh.com" revision 1\r\ndebug2: Server supports extension "fsync@openssh.com" revision 1\r\ndebug3: Sent message fd 5 T:16 I:1\r\ndebug3: SSH_FXP_REALPATH . -> /home/ansible size 0\r\ndebug3: Looking up /home/ansible/.ansible/tmp/ansible-local-4397XWOjgA/tmp6tacW2\r\ndebug3: Sent message fd 5 T:17 I:2\r\ndebug3: Received stat reply T:101 I:2\r\ndebug1: Couldn\'t stat remote file: No such file or directory\r\ndebug3: Sent message SSH2_FXP_OPEN I:3 P:/home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/AnsiballZ_setup.py\r\ndebug3: Sent message SSH2_FXP_WRITE I:4 O:0 S:32768\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 4 32768 bytes at 0\r\ndebug3: Sent message SSH2_FXP_WRITE I:5 O:32768 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:6 O:65536 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:7 O:98304 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:8 O:131072 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:9 O:163840 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:10 O:196608 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:11 O:229376 S:25820\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 5 32768 bytes at 32768\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 6 32768 bytes at 65536\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 7 32768 bytes at 98304\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 8 32768 bytes at 131072\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 9 32768 bytes at 163840\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 10 32768 bytes at 196608\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 11 25820 bytes at 229376\r\ndebug3: Sent message SSH2_FXP_CLOSE I:4\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'chmod u+x /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/ /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/AnsiballZ_setup.py && sleep 0'"'"''
<node1> (0, '', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c -tt node1 '/bin/sh -c '"'"'/usr/bin/python /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/AnsiballZ_setup.py && sleep 0'"'"''
<node1> (0, '\r\n{"invocation": {"module_args": {"filter": "*", "gather_subset": ["all"], "fact_path": "/etc/ansible/facts.d", "gather_timeout": 10}}, "ansible_facts": {"ansible_fibre_channel_wwn": [], "module_setup": true, "ansible_distribution_version": "7.6", "ansible_distribution_file_variety": "RedHat", "ansible_env": {"LANG": "en_US.UTF-8", "TERM": "xterm", "SHELL": "/bin/bash", "XDG_RUNTIME_DIR": "/run/user/1001", "MAIL": "/var/mail/ansible", "SHLVL": "2", "SSH_TTY": "/dev/pts/1", "PWD": "/home/ansible", "LESSOPEN": "||/usr/bin/lesspipe.sh %s", "YOUR_KEY": "dfdsafhdsfdhsfjkh3423fsdhfkjgfdsgfdsjgfjafjk342hi2rhehfjkshd", "SSH_CLIENT": "192.168.56.110 43440 22", "LOGNAME": "ansible", "USER": "ansible", "HOME": "/home/ansible", "PATH": "/usr/local/bin:/usr/bin", "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:", "XDG_SESSION_ID": "14", "LC_ALL": "en_US.UTF-8", "_": "/usr/bin/python", "SSH_CONNECTION": "192.168.56.110 43440 192.168.56.111 22"}, "ansible_userspace_bits": "64", "ansible_architecture": "x86_64", "ansible_default_ipv4": {"macaddress": "08:00:27:80:41:e6", "network": "10.0.3.0", "mtu": 1500, "broadcast": "10.0.3.255", "alias": "enp0s8", "netmask": "255.255.255.0", "address": "10.0.3.15", "interface": "enp0s8", "type": "ether", "gateway": "10.0.3.2"}, "ansible_swapfree_mb": 2047, "ansible_default_ipv6": {}, "ansible_cmdline": {"LANG": "en_US.UTF-8", "BOOT_IMAGE": "/vmlinuz-3.10.0-957.el7.x86_64", "quiet": true, "rhgb": true, "rd.lvm.lv": "centos/swap", "crashkernel": "auto", "ro": true, "root": "/dev/mapper/centos-root"}, "ansible_machine_id": "9c593f2fc95d4e9b962892c9f2c7698a", "ansible_userspace_architecture": "x86_64", "ansible_product_uuid": "NA", "ansible_pkg_mgr": "yum", "ansible_distribution": "CentOS", "ansible_iscsi_iqn": "", "ansible_all_ipv6_addresses": ["fe80::2b75:f84c:7d7f:597d", "fe80::864f:a509:1db0:a8fa", "fe80::3fbb:b032:5bd8:ffe9"], "ansible_uptime_seconds": 10279, "ansible_kernel": "3.10.0-957.el7.x86_64", "ansible_system_capabilities_enforced": "True", "ansible_python": {"executable": "/usr/bin/python", "version": {"micro": 5, "major": 2, "releaselevel": "final", "serial": 0, "minor": 7}, "type": "CPython", "has_sslcontext": true, "version_info": [2, 7, 5, "final", 0]}, "ansible_is_chroot": true, "ansible_hostnqn": "", "ansible_user_shell": "/bin/bash", "ansible_product_serial": "NA", "ansible_form_factor": "Other", "ansible_distribution_file_parsed": true, "ansible_fips": false, "ansible_user_id": "ansible", "ansible_selinux_python_present": true, "ansible_kernel_version": "#1 SMP Thu Nov 8 23:39:32 UTC 2018", "ansible_local": {}, "ansible_processor_vcpus": 1, "ansible_processor": ["0", "GenuineIntel", "Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz"], "ansible_ssh_host_key_ecdsa_public": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBCdtvirfdRqiXDnJV+4cHnIx6ogqaZoypiLgYntTBwjqKHUximafQc/iYf+F8CuW6Ly532K69lIjtCtHEQpCZag=", "ansible_user_gid": 1001, "ansible_system_vendor": "innotek GmbH", "ansible_swaptotal_mb": 2047, "ansible_distribution_major_version": "7", "ansible_real_group_id": 1001, "ansible_lsb": {}, "ansible_machine": "x86_64", "ansible_ssh_host_key_rsa_public": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDiMRJ4JBNDpx7Ud13uvhZ+jWg6B2nrkaFX1nsUqovJJu/5Z5I/xKcLd3F3Jql7oxK8ysXlvP5qx/TEriFW0dN6Gl1qzeqVSCh24yt3oYJJgXklum6H+HTnaHWc9stdw09FJwppOmcLal6JQfNaNKQuNJQocDMu/xbS0XHdgYPV6LEdixkVetizIiiUv0DhkVYrKAsj2kB/PYtjjonp8ehQPhm4LVkiN89Db8L05rAZcokAD4cLtKxqyKUYUKJbbu4Hdg7wSx/sOvSX9xvTMpwZ9UHbvykwKrwC/qe9208cXk44w+C16NM1Ufy8rgphgf+B6tH12Uc8FesEqmcII50p", "ansible_user_gecos": "", "ansible_processor_threads_per_core": 1, "ansible_product_name": "VirtualBox", "ansible_all_ipv4_addresses": ["192.168.56.111", "10.0.3.15"], "ansible_python_version": "2.7.5", "ansible_product_version": "1.2", "ansible_service_mgr": "systemd", "ansible_memory_mb": {"real": {"total": 1838, "used": 262, "free": 1576}, "swap": {"cached": 0, "total": 2047, "free": 2047, "used": 0}, "nocache": {"used": 152, "free": 1686}}, "ansible_user_dir": "/home/ansible", "gather_subset": ["all"], "ansible_real_user_id": 1001, "ansible_virtualization_role": "guest", "ansible_dns": {"nameservers": ["192.168.12.158", "111.111.111.114"], "search": ["ansible.com"]}, "ansible_effective_group_id": 1001, "ansible_lo": {"features": {"tx_checksum_ipv4": "off [fixed]", "generic_receive_offload": "on", "tx_checksum_ipv6": "off [fixed]", "tx_scatter_gather_fraglist": "on [fixed]", "rx_all": "off [fixed]", "highdma": "on [fixed]", "rx_fcs": "off [fixed]", "tx_lockless": "on [fixed]", "tx_tcp_ecn_segmentation": "on", "rx_udp_tunnel_port_offload": "off [fixed]", "tx_tcp6_segmentation": "on", "tx_gso_robust": "off [fixed]", "tx_ipip_segmentation": "off [fixed]", "tx_tcp_mangleid_segmentation": "on", "tx_checksumming": "on", "vlan_challenged": "on [fixed]", "loopback": "on [fixed]", "fcoe_mtu": "off [fixed]", "scatter_gather": "on", "tx_checksum_sctp": "on [fixed]", "tx_vlan_stag_hw_insert": "off [fixed]", "rx_vlan_stag_hw_parse": "off [fixed]", "tx_gso_partial": "off [fixed]", "rx_gro_hw": "off [fixed]", "rx_vlan_stag_filter": "off [fixed]", "large_receive_offload": "off [fixed]", "tx_scatter_gather": "on [fixed]", "rx_checksumming": "on [fixed]", "tx_tcp_segmentation": "on", "netns_local": "on [fixed]", "busy_poll": "off [fixed]", "generic_segmentation_offload": "on", "tx_udp_tnl_segmentation": "off [fixed]", "tcp_segmentation_offload": "on", "l2_fwd_offload": "off [fixed]", "rx_vlan_offload": "off [fixed]", "ntuple_filters": "off [fixed]", "tx_gre_csum_segmentation": "off [fixed]", "tx_nocache_copy": "off [fixed]", "tx_udp_tnl_csum_segmentation": "off [fixed]", "udp_fragmentation_offload": "on", "tx_sctp_segmentation": "on", "tx_sit_segmentation": "off [fixed]", "tx_checksum_fcoe_crc": "off [fixed]", "hw_tc_offload": "off [fixed]", "tx_checksum_ip_generic": "on [fixed]", "tx_fcoe_segmentation": "off [fixed]", "rx_vlan_filter": "off [fixed]", "tx_vlan_offload": "off [fixed]", "receive_hashing": "off [fixed]", "tx_gre_segmentation": "off [fixed]"}, "hw_timestamp_filters": [], "mtu": 65536, "device": "lo", "promisc": false, "timestamping": ["rx_software", "software"], "ipv4": {"broadcast": "host", "netmask": "255.0.0.0", "network": "127.0.0.0", "address": "127.0.0.1"}, "ipv6": [{"scope": "host", "prefix": "128", "address": "::1"}], "active": true, "type": "loopback"}, "ansible_memtotal_mb": 1838, "ansible_device_links": {"masters": {"sda2": ["dm-0", "dm-1"]}, "labels": {}, "ids": {"sr0": ["ata-VBOX_CD-ROM_VB2-01700376"], "sda2": ["ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part2", "lvm-pv-uuid-WRY6bk-ukJT-0GM9-UNTL-v1Fv-HHM1-M8Huti"], "sda": ["ata-VBOX_HARDDISK_VB50c3dc86-fca07efb"], "sda1": ["ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part1"], "dm-0": ["dm-name-centos-root", "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3pt4l0Jwtv4SRuOhwy3VL9TYzflHGe8sn2"], "dm-1": ["dm-name-centos-swap", "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3p8ZQAYA8PkKqAQScyIogWKZhL0LHt0cRB"]}, "uuids": {"sda1": ["4418f5f3-1e44-442b-95d6-d986e27acbfd"], "dm-0": ["b902127e-4281-435a-ac4f-43c89cc21897"], "dm-1": ["cd06c96d-9a6b-402e-9140-bd991588dc39"]}}, "ansible_apparmor": {"status": "disabled"}, "ansible_proc_cmdline": {"LANG": "en_US.UTF-8", "BOOT_IMAGE": "/vmlinuz-3.10.0-957.el7.x86_64", "quiet": true, "rhgb": true, "rd.lvm.lv": ["centos/root", "centos/swap"], "crashkernel": "auto", "ro": true, "root": "/dev/mapper/centos-root"}, "ansible_memfree_mb": 1576, "ansible_processor_count": 1, "ansible_hostname": "node1", "ansible_enp0s8": {"macaddress": "08:00:27:80:41:e6", "features": {"tx_checksum_ipv4": "off [fixed]", "generic_receive_offload": "on", "tx_checksum_ipv6": "off [fixed]", "tx_scatter_gather_fraglist": "off [fixed]", "rx_all": "off", "highdma": "off [fixed]", "rx_fcs": "off", "tx_lockless": "off [fixed]", "tx_tcp_ecn_segmentation": "off [fixed]", "rx_udp_tunnel_port_offload": "off [fixed]", "tx_tcp6_segmentation": "off [fixed]", "tx_gso_robust": "off [fixed]", "tx_ipip_segmentation": "off [fixed]", "tx_tcp_mangleid_segmentation": "off", "tx_checksumming": "on", "vlan_challenged": "off [fixed]", "loopback": "off [fixed]", "fcoe_mtu": "off [fixed]", "scatter_gather": "on", "tx_checksum_sctp": "off [fixed]", "tx_vlan_stag_hw_insert": "off [fixed]", "rx_vlan_stag_hw_parse": "off [fixed]", "tx_gso_partial": "off [fixed]", "rx_gro_hw": "off [fixed]", "rx_vlan_stag_filter": "off [fixed]", "large_receive_offload": "off [fixed]", "tx_scatter_gather": "on", "rx_checksumming": "off", "tx_tcp_segmentation": "on", "netns_local": "off [fixed]", "busy_poll": "off [fixed]", "generic_segmentation_offload": "on", "tx_udp_tnl_segmentation": "off [fixed]", "tcp_segmentation_offload": "on", "l2_fwd_offload": "off [fixed]", "rx_vlan_offload": "on", "ntuple_filters": "off [fixed]", "tx_gre_csum_segmentation": "off [fixed]", "tx_nocache_copy": "off", "tx_udp_tnl_csum_segmentation": "off [fixed]", "udp_fragmentation_offload": "off [fixed]", "tx_sctp_segmentation": "off [fixed]", "tx_sit_segmentation": "off [fixed]", "tx_checksum_fcoe_crc": "off [fixed]", "hw_tc_offload": "off [fixed]", "tx_checksum_ip_generic": "on", "tx_fcoe_segmentation": "off [fixed]", "rx_vlan_filter": "on [fixed]", "tx_vlan_offload": "on [fixed]", "receive_hashing": "off [fixed]", "tx_gre_segmentation": "off [fixed]"}, "type": "ether", "pciid": "0000:00:08.0", "module": "e1000", "mtu": 1500, "device": "enp0s8", "promisc": false, "timestamping": ["tx_software", "rx_software", "software"], "ipv4": {"broadcast": "10.0.3.255", "netmask": "255.255.255.0", "network": "10.0.3.0", "address": "10.0.3.15"}, "ipv6": [{"scope": "link", "prefix": "64", "address": "fe80::3fbb:b032:5bd8:ffe9"}], "active": true, "speed": 1000, "hw_timestamp_filters": []}, "ansible_interfaces": ["lo", "enp0s3", "enp0s8"], "ansible_selinux": {"status": "disabled"}, "ansible_enp0s3": {"macaddress": "08:00:27:5d:9d:7c", "features": {"tx_checksum_ipv4": "off [fixed]", "generic_receive_offload": "on", "tx_checksum_ipv6": "off [fixed]", "tx_scatter_gather_fraglist": "off [fixed]", "rx_all": "off", "highdma": "off [fixed]", "rx_fcs": "off", "tx_lockless": "off [fixed]", "tx_tcp_ecn_segmentation": "off [fixed]", "rx_udp_tunnel_port_offload": "off [fixed]", "tx_tcp6_segmentation": "off [fixed]", "tx_gso_robust": "off [fixed]", "tx_ipip_segmentation": "off [fixed]", "tx_tcp_mangleid_segmentation": "off", "tx_checksumming": "on", "vlan_challenged": "off [fixed]", "loopback": "off [fixed]", "fcoe_mtu": "off [fixed]", "scatter_gather": "on", "tx_checksum_sctp": "off [fixed]", "tx_vlan_stag_hw_insert": "off [fixed]", "rx_vlan_stag_hw_parse": "off [fixed]", "tx_gso_partial": "off [fixed]", "rx_gro_hw": "off [fixed]", "rx_vlan_stag_filter": "off [fixed]", "large_receive_offload": "off [fixed]", "tx_scatter_gather": "on", "rx_checksumming": "off", "tx_tcp_segmentation": "on", "netns_local": "off [fixed]", "busy_poll": "off [fixed]", "generic_segmentation_offload": "on", "tx_udp_tnl_segmentation": "off [fixed]", "tcp_segmentation_offload": "on", "l2_fwd_offload": "off [fixed]", "rx_vlan_offload": "on", "ntuple_filters": "off [fixed]", "tx_gre_csum_segmentation": "off [fixed]", "tx_nocache_copy": "off", "tx_udp_tnl_csum_segmentation": "off [fixed]", "udp_fragmentation_offload": "off [fixed]", "tx_sctp_segmentation": "off [fixed]", "tx_sit_segmentation": "off [fixed]", "tx_checksum_fcoe_crc": "off [fixed]", "hw_tc_offload": "off [fixed]", "tx_checksum_ip_generic": "on", "tx_fcoe_segmentation": "off [fixed]", "rx_vlan_filter": "on [fixed]", "tx_vlan_offload": "on [fixed]", "receive_hashing": "off [fixed]", "tx_gre_segmentation": "off [fixed]"}, "type": "ether", "pciid": "0000:00:03.0", "module": "e1000", "mtu": 1500, "device": "enp0s3", "promisc": false, "timestamping": ["tx_software", "rx_software", "software"], "ipv4": {"broadcast": "192.168.56.255", "netmask": "255.255.255.0", "network": "192.168.56.0", "address": "192.168.56.111"}, "ipv6": [{"scope": "link", "prefix": "64", "address": "fe80::2b75:f84c:7d7f:597d"}, {"scope": "link", "prefix": "64", "address": "fe80::864f:a509:1db0:a8fa"}], "active": true, "speed": 1000, "hw_timestamp_filters": []}, "ansible_fqdn": "node1.ansible.com", "ansible_mounts": [{"block_used": 36953, "uuid": "4418f5f3-1e44-442b-95d6-d986e27acbfd", "size_total": 1063256064, "block_total": 259584, "mount": "/boot", "block_available": 222631, "size_available": 911896576, "fstype": "xfs", "inode_total": 524288, "options": "rw,relatime,attr2,inode64,noquota", "device": "/dev/sda1", "inode_used": 327, "block_size": 4096, "inode_available": 523961}, {"block_used": 540912, "uuid": "b902127e-4281-435a-ac4f-43c89cc21897", "size_total": 18238930944, "block_total": 4452864, "mount": "/", "block_available": 3911952, "size_available": 16023355392, "fstype": "xfs", "inode_total": 8910848, "options": "rw,relatime,attr2,inode64,noquota", "device": "/dev/mapper/centos-root", "inode_used": 50429, "block_size": 4096, "inode_available": 8860419}], "ansible_nodename": "node1.ansible.com", "ansible_domain": "ansible.com", "ansible_distribution_file_path": "/etc/redhat-release", "ansible_virtualization_type": "virtualbox", "ansible_ssh_host_key_ed25519_public": "AAAAC3NzaC1lZDI1NTE5AAAAIAl7nO9kxvd44yLD0SWqdflD/BbwsiJSMlhaJjuMi5Kc", "ansible_processor_cores": 1, "ansible_bios_version": "VirtualBox", "ansible_date_time": {"weekday_number": "1", "iso8601_basic_short": "20200727T171816", "tz": "CST", "weeknumber": "30", "hour": "17", "year": "2020", "minute": "18", "tz_offset": "+0800", "month": "07", "epoch": "1595841496", "iso8601_micro": "2020-07-27T09:18:16.164861Z", "weekday": "Monday", "time": "17:18:16", "date": "2020-07-27", "iso8601": "2020-07-27T09:18:16Z", "day": "27", "iso8601_basic": "20200727T171816164762", "second": "16"}, "ansible_distribution_release": "Core", "ansible_os_family": "RedHat", "ansible_effective_user_id": 1001, "ansible_system": "Linux", "ansible_devices": {"sr0": {"scheduler_mode": "deadline", "rotational": "1", "vendor": "VBOX", "sectors": "2097151", "links": {"masters": [], "labels": [], "ids": ["ata-VBOX_CD-ROM_VB2-01700376"], "uuids": []}, "sas_device_handle": null, "sas_address": null, "virtual": 1, "host": "", "sectorsize": "512", "removable": "1", "support_discard": "0", "model": "CD-ROM", "partitions": {}, "holders": [], "size": "1024.00 MB"}, "sda": {"scheduler_mode": "deadline", "rotational": "1", "vendor": "ATA", "sectors": "41943040", "links": {"masters": [], "labels": [], "ids": ["ata-VBOX_HARDDISK_VB50c3dc86-fca07efb"], "uuids": []}, "sas_device_handle": null, "sas_address": null, "virtual": 1, "host": "", "sectorsize": "512", "removable": "0", "support_discard": "0", "model": "VBOX HARDDISK", "partitions": {"sda2": {"sectorsize": 512, "uuid": null, "links": {"masters": ["dm-0", "dm-1"], "labels": [], "ids": ["ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part2", "lvm-pv-uuid-WRY6bk-ukJT-0GM9-UNTL-v1Fv-HHM1-M8Huti"], "uuids": []}, "sectors": "39843840", "start": "2099200", "holders": ["centos-root", "centos-swap"], "size": "19.00 GB"}, "sda1": {"sectorsize": 512, "uuid": "4418f5f3-1e44-442b-95d6-d986e27acbfd", "links": {"masters": [], "labels": [], "ids": ["ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part1"], "uuids": ["4418f5f3-1e44-442b-95d6-d986e27acbfd"]}, "sectors": "2097152", "start": "2048", "holders": [], "size": "1.00 GB"}}, "holders": [], "size": "20.00 GB"}, "dm-0": {"scheduler_mode": "", "rotational": "1", "vendor": null, "sectors": "35643392", "links": {"masters": [], "labels": [], "ids": ["dm-name-centos-root", "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3pt4l0Jwtv4SRuOhwy3VL9TYzflHGe8sn2"], "uuids": ["b902127e-4281-435a-ac4f-43c89cc21897"]}, "sas_device_handle": null, "sas_address": null, "virtual": 1, "host": "", "sectorsize": "512", "removable": "0", "support_discard": "0", "model": null, "partitions": {}, "holders": [], "size": "17.00 GB"}, "dm-1": {"scheduler_mode": "", "rotational": "1", "vendor": null, "sectors": "4194304", "links": {"masters": [], "labels": [], "ids": ["dm-name-centos-swap", "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3p8ZQAYA8PkKqAQScyIogWKZhL0LHt0cRB"], "uuids": ["cd06c96d-9a6b-402e-9140-bd991588dc39"]}, "sas_device_handle": null, "sas_address": null, "virtual": 1, "host": "", "sectorsize": "512", "removable": "0", "support_discard": "0", "model": null, "partitions": {}, "holders": [], "size": "2.00 GB"}}, "ansible_user_uid": 1001, "ansible_bios_date": "12/01/2006", "ansible_system_capabilities": [""]}}\r\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\nShared connection to node1 closed.\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'rm -f -r /home/ansible/.ansible/tmp/ansible-tmp-1595841490.45-4406-255689703212953/ > /dev/null 2>&1 && sleep 0'"'"''
<node1> (0, '', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
ok: [node1]
META: ran handlers

TASK [prints the loopback address and gateway] ***************************************
task path: /home/ansible/debug.yml:6
ok: [node1] => {
    "msg": "System node1 has uuid NA"
}

TASK [print message] *****************************************************************
task path: /home/ansible/debug.yml:10
ok: [node1] => {
    "msg": "System node1 has gateway 10.0.3.2"
}

TASK [get the return information] ****************************************************
task path: /home/ansible/debug.yml:16
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'echo ~ && sleep 0'"'"''
<node1> (0, '/home/ansible\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'( umask 77 && mkdir -p "` echo /home/ansible/.ansible/tmp `"&& mkdir /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786 && echo ansible-tmp-1595841496.31-4421-84149749061786="` echo /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786 `" ) && sleep 0'"'"''
<node1> (0, 'ansible-tmp-1595841496.31-4421-84149749061786=/home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
Using module file /usr/lib/python2.7/site-packages/ansible/modules/commands/command.py
<node1> PUT /home/ansible/.ansible/tmp/ansible-local-4397XWOjgA/tmpiZmH3d TO /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/AnsiballZ_command.py
<node1> SSH: EXEC sftp -b - -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c '[node1]'
<node1> (0, 'sftp> put /home/ansible/.ansible/tmp/ansible-local-4397XWOjgA/tmpiZmH3d /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/AnsiballZ_command.py\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug2: Remote version: 3\r\ndebug2: Server supports extension "posix-rename@openssh.com" revision 1\r\ndebug2: Server supports extension "statvfs@openssh.com" revision 2\r\ndebug2: Server supports extension "fstatvfs@openssh.com" revision 2\r\ndebug2: Server supports extension "hardlink@openssh.com" revision 1\r\ndebug2: Server supports extension "fsync@openssh.com" revision 1\r\ndebug3: Sent message fd 5 T:16 I:1\r\ndebug3: SSH_FXP_REALPATH . -> /home/ansible size 0\r\ndebug3: Looking up /home/ansible/.ansible/tmp/ansible-local-4397XWOjgA/tmpiZmH3d\r\ndebug3: Sent message fd 5 T:17 I:2\r\ndebug3: Received stat reply T:101 I:2\r\ndebug1: Couldn\'t stat remote file: No such file or directory\r\ndebug3: Sent message SSH2_FXP_OPEN I:3 P:/home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/AnsiballZ_command.py\r\ndebug3: Sent message SSH2_FXP_WRITE I:4 O:0 S:32768\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 4 32768 bytes at 0\r\ndebug3: Sent message SSH2_FXP_WRITE I:5 O:32768 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:6 O:65536 S:32768\r\ndebug3: Sent message SSH2_FXP_WRITE I:7 O:98304 S:9753\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 5 32768 bytes at 32768\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 6 32768 bytes at 65536\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: In write loop, ack for 7 9753 bytes at 98304\r\ndebug3: Sent message SSH2_FXP_CLOSE I:4\r\ndebug3: SSH2_FXP_STATUS 0\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'chmod u+x /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/ /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/AnsiballZ_command.py && sleep 0'"'"''
<node1> (0, '', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c -tt node1 '/bin/sh -c '"'"'/usr/bin/python /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/AnsiballZ_command.py && sleep 0'"'"''
<node1> (0, '\r\n{"changed": true, "end": "2020-07-27 17:18:16.575369", "stdout": "192.168.56.111 10.0.3.15 ", "cmd": ["hostname", "-I"], "rc": 0, "start": "2020-07-27 17:18:16.573293", "stderr": "", "delta": "0:00:00.002076", "invocation": {"module_args": {"creates": null, "executable": null, "_uses_shell": false, "strip_empty_ends": true, "_raw_params": "hostname -I", "removes": null, "argv": null, "warn": true, "chdir": null, "stdin_add_newline": true, "stdin": null}}}\r\n', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\nShared connection to node1 closed.\r\n')
<node1> ESTABLISH SSH CONNECTION FOR USER: None
<node1> SSH: EXEC ssh -vvv -C -o ControlMaster=auto -o ControlPersist=60s -o KbdInteractiveAuthentication=no -o PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey -o PasswordAuthentication=no -o ConnectTimeout=10 -o ControlPath=/home/ansible/.ansible/cp/1396e5f87c node1 '/bin/sh -c '"'"'rm -f -r /home/ansible/.ansible/tmp/ansible-tmp-1595841496.31-4421-84149749061786/ > /dev/null 2>&1 && sleep 0'"'"''
<node1> (0, '', 'OpenSSH_7.4p1, OpenSSL 1.0.2k-fips  26 Jan 2017\r\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 58: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_forwards: request forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 4367\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 0\r\n')
changed: [node1] => {
    "changed": true, 
    "cmd": [
        "hostname", 
        "-I"
    ], 
    "delta": "0:00:00.002076", 
    "end": "2020-07-27 17:18:16.575369", 
    "invocation": {
        "module_args": {
            "_raw_params": "hostname -I", 
            "_uses_shell": false, 
            "argv": null, 
            "chdir": null, 
            "creates": null, 
            "executable": null, 
            "removes": null, 
            "stdin": null, 
            "stdin_add_newline": true, 
            "strip_empty_ends": true, 
            "warn": true
        }
    }, 
    "rc": 0, 
    "start": "2020-07-27 17:18:16.573293", 
    "stderr": "", 
    "stderr_lines": [], 
    "stdout": "192.168.56.111 10.0.3.15 ", 
    "stdout_lines": [
        "192.168.56.111 10.0.3.15 "
    ]
}

TASK [print the result] **************************************************************
task path: /home/ansible/debug.yml:22
ok: [node1] => {
    "result": {
        "changed": true, 
        "cmd": [
            "hostname", 
            "-I"
        ], 
        "delta": "0:00:00.002076", 
        "end": "2020-07-27 17:18:16.575369", 
        "failed": false, 
        "rc": 0, 
        "start": "2020-07-27 17:18:16.573293", 
        "stderr": "", 
        "stderr_lines": [], 
        "stdout": "192.168.56.111 10.0.3.15 ", 
        "stdout_lines": [
            "192.168.56.111 10.0.3.15 "
        ]
    }
}

TASK [Display all variables/facts known for a host] **********************************
task path: /home/ansible/debug.yml:27
ok: [node1] => {
    "hostvars[inventory_hostname]": {
        "ansible_all_ipv4_addresses": [
            "192.168.56.111", 
            "10.0.3.15"
        ], 
        "ansible_all_ipv6_addresses": [
            "fe80::2b75:f84c:7d7f:597d", 
            "fe80::864f:a509:1db0:a8fa", 
            "fe80::3fbb:b032:5bd8:ffe9"
        ], 
        "ansible_apparmor": {
            "status": "disabled"
        }, 
        "ansible_architecture": "x86_64", 
        "ansible_bios_date": "12/01/2006", 
        "ansible_bios_version": "VirtualBox", 
        "ansible_check_mode": false, 
        "ansible_cmdline": {
            "BOOT_IMAGE": "/vmlinuz-3.10.0-957.el7.x86_64", 
            "LANG": "en_US.UTF-8", 
            "crashkernel": "auto", 
            "quiet": true, 
            "rd.lvm.lv": "centos/swap", 
            "rhgb": true, 
            "ro": true, 
            "root": "/dev/mapper/centos-root"
        }, 
        "ansible_date_time": {
            "date": "2020-07-27", 
            "day": "27", 
            "epoch": "1595841496", 
            "hour": "17", 
            "iso8601": "2020-07-27T09:18:16Z", 
            "iso8601_basic": "20200727T171816164762", 
            "iso8601_basic_short": "20200727T171816", 
            "iso8601_micro": "2020-07-27T09:18:16.164861Z", 
            "minute": "18", 
            "month": "07", 
            "second": "16", 
            "time": "17:18:16", 
            "tz": "CST", 
            "tz_offset": "+0800", 
            "weekday": "Monday", 
            "weekday_number": "1", 
            "weeknumber": "30", 
            "year": "2020"
        }, 
        "ansible_default_ipv4": {
            "address": "10.0.3.15", 
            "alias": "enp0s8", 
            "broadcast": "10.0.3.255", 
            "gateway": "10.0.3.2", 
            "interface": "enp0s8", 
            "macaddress": "08:00:27:80:41:e6", 
            "mtu": 1500, 
            "netmask": "255.255.255.0", 
            "network": "10.0.3.0", 
            "type": "ether"
        }, 
        "ansible_default_ipv6": {}, 
        "ansible_device_links": {
            "ids": {
                "dm-0": [
                    "dm-name-centos-root", 
                    "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3pt4l0Jwtv4SRuOhwy3VL9TYzflHGe8sn2"
                ], 
                "dm-1": [
                    "dm-name-centos-swap", 
                    "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3p8ZQAYA8PkKqAQScyIogWKZhL0LHt0cRB"
                ], 
                "sda": [
                    "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb"
                ], 
                "sda1": [
                    "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part1"
                ], 
                "sda2": [
                    "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part2", 
                    "lvm-pv-uuid-WRY6bk-ukJT-0GM9-UNTL-v1Fv-HHM1-M8Huti"
                ], 
                "sr0": [
                    "ata-VBOX_CD-ROM_VB2-01700376"
                ]
            }, 
            "labels": {}, 
            "masters": {
                "sda2": [
                    "dm-0", 
                    "dm-1"
                ]
            }, 
            "uuids": {
                "dm-0": [
                    "b902127e-4281-435a-ac4f-43c89cc21897"
                ], 
                "dm-1": [
                    "cd06c96d-9a6b-402e-9140-bd991588dc39"
                ], 
                "sda1": [
                    "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                ]
            }
        }, 
        "ansible_devices": {
            "dm-0": {
                "holders": [], 
                "host": "", 
                "links": {
                    "ids": [
                        "dm-name-centos-root", 
                        "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3pt4l0Jwtv4SRuOhwy3VL9TYzflHGe8sn2"
                    ], 
                    "labels": [], 
                    "masters": [], 
                    "uuids": [
                        "b902127e-4281-435a-ac4f-43c89cc21897"
                    ]
                }, 
                "model": null, 
                "partitions": {}, 
                "removable": "0", 
                "rotational": "1", 
                "sas_address": null, 
                "sas_device_handle": null, 
                "scheduler_mode": "", 
                "sectors": "35643392", 
                "sectorsize": "512", 
                "size": "17.00 GB", 
                "support_discard": "0", 
                "vendor": null, 
                "virtual": 1
            }, 
            "dm-1": {
                "holders": [], 
                "host": "", 
                "links": {
                    "ids": [
                        "dm-name-centos-swap", 
                        "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3p8ZQAYA8PkKqAQScyIogWKZhL0LHt0cRB"
                    ], 
                    "labels": [], 
                    "masters": [], 
                    "uuids": [
                        "cd06c96d-9a6b-402e-9140-bd991588dc39"
                    ]
                }, 
                "model": null, 
                "partitions": {}, 
                "removable": "0", 
                "rotational": "1", 
                "sas_address": null, 
                "sas_device_handle": null, 
                "scheduler_mode": "", 
                "sectors": "4194304", 
                "sectorsize": "512", 
                "size": "2.00 GB", 
                "support_discard": "0", 
                "vendor": null, 
                "virtual": 1
            }, 
            "sda": {
                "holders": [], 
                "host": "", 
                "links": {
                    "ids": [
                        "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb"
                    ], 
                    "labels": [], 
                    "masters": [], 
                    "uuids": []
                }, 
                "model": "VBOX HARDDISK", 
                "partitions": {
                    "sda1": {
                        "holders": [], 
                        "links": {
                            "ids": [
                                "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part1"
                            ], 
                            "labels": [], 
                            "masters": [], 
                            "uuids": [
                                "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                            ]
                        }, 
                        "sectors": "2097152", 
                        "sectorsize": 512, 
                        "size": "1.00 GB", 
                        "start": "2048", 
                        "uuid": "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                    }, 
                    "sda2": {
                        "holders": [
                            "centos-root", 
                            "centos-swap"
                        ], 
                        "links": {
                            "ids": [
                                "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part2", 
                                "lvm-pv-uuid-WRY6bk-ukJT-0GM9-UNTL-v1Fv-HHM1-M8Huti"
                            ], 
                            "labels": [], 
                            "masters": [
                                "dm-0", 
                                "dm-1"
                            ], 
                            "uuids": []
                        }, 
                        "sectors": "39843840", 
                        "sectorsize": 512, 
                        "size": "19.00 GB", 
                        "start": "2099200", 
                        "uuid": null
                    }
                }, 
                "removable": "0", 
                "rotational": "1", 
                "sas_address": null, 
                "sas_device_handle": null, 
                "scheduler_mode": "deadline", 
                "sectors": "41943040", 
                "sectorsize": "512", 
                "size": "20.00 GB", 
                "support_discard": "0", 
                "vendor": "ATA", 
                "virtual": 1
            }, 
            "sr0": {
                "holders": [], 
                "host": "", 
                "links": {
                    "ids": [
                        "ata-VBOX_CD-ROM_VB2-01700376"
                    ], 
                    "labels": [], 
                    "masters": [], 
                    "uuids": []
                }, 
                "model": "CD-ROM", 
                "partitions": {}, 
                "removable": "1", 
                "rotational": "1", 
                "sas_address": null, 
                "sas_device_handle": null, 
                "scheduler_mode": "deadline", 
                "sectors": "2097151", 
                "sectorsize": "512", 
                "size": "1024.00 MB", 
                "support_discard": "0", 
                "vendor": "VBOX", 
                "virtual": 1
            }
        }, 
        "ansible_diff_mode": false, 
        "ansible_distribution": "CentOS", 
        "ansible_distribution_file_parsed": true, 
        "ansible_distribution_file_path": "/etc/redhat-release", 
        "ansible_distribution_file_variety": "RedHat", 
        "ansible_distribution_major_version": "7", 
        "ansible_distribution_release": "Core", 
        "ansible_distribution_version": "7.6", 
        "ansible_dns": {
            "nameservers": [
                "192.168.12.158", 
                "111.111.111.114"
            ], 
            "search": [
                "ansible.com"
            ]
        }, 
        "ansible_domain": "ansible.com", 
        "ansible_effective_group_id": 1001, 
        "ansible_effective_user_id": 1001, 
        "ansible_enp0s3": {
            "active": true, 
            "device": "enp0s3", 
            "features": {
                "busy_poll": "off [fixed]", 
                "fcoe_mtu": "off [fixed]", 
                "generic_receive_offload": "on", 
                "generic_segmentation_offload": "on", 
                "highdma": "off [fixed]", 
                "hw_tc_offload": "off [fixed]", 
                "l2_fwd_offload": "off [fixed]", 
                "large_receive_offload": "off [fixed]", 
                "loopback": "off [fixed]", 
                "netns_local": "off [fixed]", 
                "ntuple_filters": "off [fixed]", 
                "receive_hashing": "off [fixed]", 
                "rx_all": "off", 
                "rx_checksumming": "off", 
                "rx_fcs": "off", 
                "rx_gro_hw": "off [fixed]", 
                "rx_udp_tunnel_port_offload": "off [fixed]", 
                "rx_vlan_filter": "on [fixed]", 
                "rx_vlan_offload": "on", 
                "rx_vlan_stag_filter": "off [fixed]", 
                "rx_vlan_stag_hw_parse": "off [fixed]", 
                "scatter_gather": "on", 
                "tcp_segmentation_offload": "on", 
                "tx_checksum_fcoe_crc": "off [fixed]", 
                "tx_checksum_ip_generic": "on", 
                "tx_checksum_ipv4": "off [fixed]", 
                "tx_checksum_ipv6": "off [fixed]", 
                "tx_checksum_sctp": "off [fixed]", 
                "tx_checksumming": "on", 
                "tx_fcoe_segmentation": "off [fixed]", 
                "tx_gre_csum_segmentation": "off [fixed]", 
                "tx_gre_segmentation": "off [fixed]", 
                "tx_gso_partial": "off [fixed]", 
                "tx_gso_robust": "off [fixed]", 
                "tx_ipip_segmentation": "off [fixed]", 
                "tx_lockless": "off [fixed]", 
                "tx_nocache_copy": "off", 
                "tx_scatter_gather": "on", 
                "tx_scatter_gather_fraglist": "off [fixed]", 
                "tx_sctp_segmentation": "off [fixed]", 
                "tx_sit_segmentation": "off [fixed]", 
                "tx_tcp6_segmentation": "off [fixed]", 
                "tx_tcp_ecn_segmentation": "off [fixed]", 
                "tx_tcp_mangleid_segmentation": "off", 
                "tx_tcp_segmentation": "on", 
                "tx_udp_tnl_csum_segmentation": "off [fixed]", 
                "tx_udp_tnl_segmentation": "off [fixed]", 
                "tx_vlan_offload": "on [fixed]", 
                "tx_vlan_stag_hw_insert": "off [fixed]", 
                "udp_fragmentation_offload": "off [fixed]", 
                "vlan_challenged": "off [fixed]"
            }, 
            "hw_timestamp_filters": [], 
            "ipv4": {
                "address": "192.168.56.111", 
                "broadcast": "192.168.56.255", 
                "netmask": "255.255.255.0", 
                "network": "192.168.56.0"
            }, 
            "ipv6": [
                {
                    "address": "fe80::2b75:f84c:7d7f:597d", 
                    "prefix": "64", 
                    "scope": "link"
                }, 
                {
                    "address": "fe80::864f:a509:1db0:a8fa", 
                    "prefix": "64", 
                    "scope": "link"
                }
            ], 
            "macaddress": "08:00:27:5d:9d:7c", 
            "module": "e1000", 
            "mtu": 1500, 
            "pciid": "0000:00:03.0", 
            "promisc": false, 
            "speed": 1000, 
            "timestamping": [
                "tx_software", 
                "rx_software", 
                "software"
            ], 
            "type": "ether"
        }, 
        "ansible_enp0s8": {
            "active": true, 
            "device": "enp0s8", 
            "features": {
                "busy_poll": "off [fixed]", 
                "fcoe_mtu": "off [fixed]", 
                "generic_receive_offload": "on", 
                "generic_segmentation_offload": "on", 
                "highdma": "off [fixed]", 
                "hw_tc_offload": "off [fixed]", 
                "l2_fwd_offload": "off [fixed]", 
                "large_receive_offload": "off [fixed]", 
                "loopback": "off [fixed]", 
                "netns_local": "off [fixed]", 
                "ntuple_filters": "off [fixed]", 
                "receive_hashing": "off [fixed]", 
                "rx_all": "off", 
                "rx_checksumming": "off", 
                "rx_fcs": "off", 
                "rx_gro_hw": "off [fixed]", 
                "rx_udp_tunnel_port_offload": "off [fixed]", 
                "rx_vlan_filter": "on [fixed]", 
                "rx_vlan_offload": "on", 
                "rx_vlan_stag_filter": "off [fixed]", 
                "rx_vlan_stag_hw_parse": "off [fixed]", 
                "scatter_gather": "on", 
                "tcp_segmentation_offload": "on", 
                "tx_checksum_fcoe_crc": "off [fixed]", 
                "tx_checksum_ip_generic": "on", 
                "tx_checksum_ipv4": "off [fixed]", 
                "tx_checksum_ipv6": "off [fixed]", 
                "tx_checksum_sctp": "off [fixed]", 
                "tx_checksumming": "on", 
                "tx_fcoe_segmentation": "off [fixed]", 
                "tx_gre_csum_segmentation": "off [fixed]", 
                "tx_gre_segmentation": "off [fixed]", 
                "tx_gso_partial": "off [fixed]", 
                "tx_gso_robust": "off [fixed]", 
                "tx_ipip_segmentation": "off [fixed]", 
                "tx_lockless": "off [fixed]", 
                "tx_nocache_copy": "off", 
                "tx_scatter_gather": "on", 
                "tx_scatter_gather_fraglist": "off [fixed]", 
                "tx_sctp_segmentation": "off [fixed]", 
                "tx_sit_segmentation": "off [fixed]", 
                "tx_tcp6_segmentation": "off [fixed]", 
                "tx_tcp_ecn_segmentation": "off [fixed]", 
                "tx_tcp_mangleid_segmentation": "off", 
                "tx_tcp_segmentation": "on", 
                "tx_udp_tnl_csum_segmentation": "off [fixed]", 
                "tx_udp_tnl_segmentation": "off [fixed]", 
                "tx_vlan_offload": "on [fixed]", 
                "tx_vlan_stag_hw_insert": "off [fixed]", 
                "udp_fragmentation_offload": "off [fixed]", 
                "vlan_challenged": "off [fixed]"
            }, 
            "hw_timestamp_filters": [], 
            "ipv4": {
                "address": "10.0.3.15", 
                "broadcast": "10.0.3.255", 
                "netmask": "255.255.255.0", 
                "network": "10.0.3.0"
            }, 
            "ipv6": [
                {
                    "address": "fe80::3fbb:b032:5bd8:ffe9", 
                    "prefix": "64", 
                    "scope": "link"
                }
            ], 
            "macaddress": "08:00:27:80:41:e6", 
            "module": "e1000", 
            "mtu": 1500, 
            "pciid": "0000:00:08.0", 
            "promisc": false, 
            "speed": 1000, 
            "timestamping": [
                "tx_software", 
                "rx_software", 
                "software"
            ], 
            "type": "ether"
        }, 
        "ansible_env": {
            "HOME": "/home/ansible", 
            "LANG": "en_US.UTF-8", 
            "LC_ALL": "en_US.UTF-8", 
            "LESSOPEN": "||/usr/bin/lesspipe.sh %s", 
            "LOGNAME": "ansible", 
            "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:", 
            "MAIL": "/var/mail/ansible", 
            "PATH": "/usr/local/bin:/usr/bin", 
            "PWD": "/home/ansible", 
            "SHELL": "/bin/bash", 
            "SHLVL": "2", 
            "SSH_CLIENT": "192.168.56.110 43440 22", 
            "SSH_CONNECTION": "192.168.56.110 43440 192.168.56.111 22", 
            "SSH_TTY": "/dev/pts/1", 
            "TERM": "xterm", 
            "USER": "ansible", 
            "XDG_RUNTIME_DIR": "/run/user/1001", 
            "XDG_SESSION_ID": "14", 
            "YOUR_KEY": "dfdsafhdsfdhsfjkh3423fsdhfkjgfdsgfdsjgfjafjk342hi2rhehfjkshd", 
            "_": "/usr/bin/python"
        }, 
        "ansible_facts": {
            "all_ipv4_addresses": [
                "192.168.56.111", 
                "10.0.3.15"
            ], 
            "all_ipv6_addresses": [
                "fe80::2b75:f84c:7d7f:597d", 
                "fe80::864f:a509:1db0:a8fa", 
                "fe80::3fbb:b032:5bd8:ffe9"
            ], 
            "ansible_local": {}, 
            "apparmor": {
                "status": "disabled"
            }, 
            "architecture": "x86_64", 
            "bios_date": "12/01/2006", 
            "bios_version": "VirtualBox", 
            "cmdline": {
                "BOOT_IMAGE": "/vmlinuz-3.10.0-957.el7.x86_64", 
                "LANG": "en_US.UTF-8", 
                "crashkernel": "auto", 
                "quiet": true, 
                "rd.lvm.lv": "centos/swap", 
                "rhgb": true, 
                "ro": true, 
                "root": "/dev/mapper/centos-root"
            }, 
            "date_time": {
                "date": "2020-07-27", 
                "day": "27", 
                "epoch": "1595841496", 
                "hour": "17", 
                "iso8601": "2020-07-27T09:18:16Z", 
                "iso8601_basic": "20200727T171816164762", 
                "iso8601_basic_short": "20200727T171816", 
                "iso8601_micro": "2020-07-27T09:18:16.164861Z", 
                "minute": "18", 
                "month": "07", 
                "second": "16", 
                "time": "17:18:16", 
                "tz": "CST", 
                "tz_offset": "+0800", 
                "weekday": "Monday", 
                "weekday_number": "1", 
                "weeknumber": "30", 
                "year": "2020"
            }, 
            "default_ipv4": {
                "address": "10.0.3.15", 
                "alias": "enp0s8", 
                "broadcast": "10.0.3.255", 
                "gateway": "10.0.3.2", 
                "interface": "enp0s8", 
                "macaddress": "08:00:27:80:41:e6", 
                "mtu": 1500, 
                "netmask": "255.255.255.0", 
                "network": "10.0.3.0", 
                "type": "ether"
            }, 
            "default_ipv6": {}, 
            "device_links": {
                "ids": {
                    "dm-0": [
                        "dm-name-centos-root", 
                        "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3pt4l0Jwtv4SRuOhwy3VL9TYzflHGe8sn2"
                    ], 
                    "dm-1": [
                        "dm-name-centos-swap", 
                        "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3p8ZQAYA8PkKqAQScyIogWKZhL0LHt0cRB"
                    ], 
                    "sda": [
                        "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb"
                    ], 
                    "sda1": [
                        "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part1"
                    ], 
                    "sda2": [
                        "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part2", 
                        "lvm-pv-uuid-WRY6bk-ukJT-0GM9-UNTL-v1Fv-HHM1-M8Huti"
                    ], 
                    "sr0": [
                        "ata-VBOX_CD-ROM_VB2-01700376"
                    ]
                }, 
                "labels": {}, 
                "masters": {
                    "sda2": [
                        "dm-0", 
                        "dm-1"
                    ]
                }, 
                "uuids": {
                    "dm-0": [
                        "b902127e-4281-435a-ac4f-43c89cc21897"
                    ], 
                    "dm-1": [
                        "cd06c96d-9a6b-402e-9140-bd991588dc39"
                    ], 
                    "sda1": [
                        "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                    ]
                }
            }, 
            "devices": {
                "dm-0": {
                    "holders": [], 
                    "host": "", 
                    "links": {
                        "ids": [
                            "dm-name-centos-root", 
                            "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3pt4l0Jwtv4SRuOhwy3VL9TYzflHGe8sn2"
                        ], 
                        "labels": [], 
                        "masters": [], 
                        "uuids": [
                            "b902127e-4281-435a-ac4f-43c89cc21897"
                        ]
                    }, 
                    "model": null, 
                    "partitions": {}, 
                    "removable": "0", 
                    "rotational": "1", 
                    "sas_address": null, 
                    "sas_device_handle": null, 
                    "scheduler_mode": "", 
                    "sectors": "35643392", 
                    "sectorsize": "512", 
                    "size": "17.00 GB", 
                    "support_discard": "0", 
                    "vendor": null, 
                    "virtual": 1
                }, 
                "dm-1": {
                    "holders": [], 
                    "host": "", 
                    "links": {
                        "ids": [
                            "dm-name-centos-swap", 
                            "dm-uuid-LVM-mafWexonk9bSP5E2YH5AsrS4qKWotG3p8ZQAYA8PkKqAQScyIogWKZhL0LHt0cRB"
                        ], 
                        "labels": [], 
                        "masters": [], 
                        "uuids": [
                            "cd06c96d-9a6b-402e-9140-bd991588dc39"
                        ]
                    }, 
                    "model": null, 
                    "partitions": {}, 
                    "removable": "0", 
                    "rotational": "1", 
                    "sas_address": null, 
                    "sas_device_handle": null, 
                    "scheduler_mode": "", 
                    "sectors": "4194304", 
                    "sectorsize": "512", 
                    "size": "2.00 GB", 
                    "support_discard": "0", 
                    "vendor": null, 
                    "virtual": 1
                }, 
                "sda": {
                    "holders": [], 
                    "host": "", 
                    "links": {
                        "ids": [
                            "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb"
                        ], 
                        "labels": [], 
                        "masters": [], 
                        "uuids": []
                    }, 
                    "model": "VBOX HARDDISK", 
                    "partitions": {
                        "sda1": {
                            "holders": [], 
                            "links": {
                                "ids": [
                                    "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part1"
                                ], 
                                "labels": [], 
                                "masters": [], 
                                "uuids": [
                                    "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                                ]
                            }, 
                            "sectors": "2097152", 
                            "sectorsize": 512, 
                            "size": "1.00 GB", 
                            "start": "2048", 
                            "uuid": "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                        }, 
                        "sda2": {
                            "holders": [
                                "centos-root", 
                                "centos-swap"
                            ], 
                            "links": {
                                "ids": [
                                    "ata-VBOX_HARDDISK_VB50c3dc86-fca07efb-part2", 
                                    "lvm-pv-uuid-WRY6bk-ukJT-0GM9-UNTL-v1Fv-HHM1-M8Huti"
                                ], 
                                "labels": [], 
                                "masters": [
                                    "dm-0", 
                                    "dm-1"
                                ], 
                                "uuids": []
                            }, 
                            "sectors": "39843840", 
                            "sectorsize": 512, 
                            "size": "19.00 GB", 
                            "start": "2099200", 
                            "uuid": null
                        }
                    }, 
                    "removable": "0", 
                    "rotational": "1", 
                    "sas_address": null, 
                    "sas_device_handle": null, 
                    "scheduler_mode": "deadline", 
                    "sectors": "41943040", 
                    "sectorsize": "512", 
                    "size": "20.00 GB", 
                    "support_discard": "0", 
                    "vendor": "ATA", 
                    "virtual": 1
                }, 
                "sr0": {
                    "holders": [], 
                    "host": "", 
                    "links": {
                        "ids": [
                            "ata-VBOX_CD-ROM_VB2-01700376"
                        ], 
                        "labels": [], 
                        "masters": [], 
                        "uuids": []
                    }, 
                    "model": "CD-ROM", 
                    "partitions": {}, 
                    "removable": "1", 
                    "rotational": "1", 
                    "sas_address": null, 
                    "sas_device_handle": null, 
                    "scheduler_mode": "deadline", 
                    "sectors": "2097151", 
                    "sectorsize": "512", 
                    "size": "1024.00 MB", 
                    "support_discard": "0", 
                    "vendor": "VBOX", 
                    "virtual": 1
                }
            }, 
            "discovered_interpreter_python": "/usr/bin/python", 
            "distribution": "CentOS", 
            "distribution_file_parsed": true, 
            "distribution_file_path": "/etc/redhat-release", 
            "distribution_file_variety": "RedHat", 
            "distribution_major_version": "7", 
            "distribution_release": "Core", 
            "distribution_version": "7.6", 
            "dns": {
                "nameservers": [
                    "192.168.12.158", 
                    "111.111.111.114"
                ], 
                "search": [
                    "ansible.com"
                ]
            }, 
            "domain": "ansible.com", 
            "effective_group_id": 1001, 
            "effective_user_id": 1001, 
            "enp0s3": {
                "active": true, 
                "device": "enp0s3", 
                "features": {
                    "busy_poll": "off [fixed]", 
                    "fcoe_mtu": "off [fixed]", 
                    "generic_receive_offload": "on", 
                    "generic_segmentation_offload": "on", 
                    "highdma": "off [fixed]", 
                    "hw_tc_offload": "off [fixed]", 
                    "l2_fwd_offload": "off [fixed]", 
                    "large_receive_offload": "off [fixed]", 
                    "loopback": "off [fixed]", 
                    "netns_local": "off [fixed]", 
                    "ntuple_filters": "off [fixed]", 
                    "receive_hashing": "off [fixed]", 
                    "rx_all": "off", 
                    "rx_checksumming": "off", 
                    "rx_fcs": "off", 
                    "rx_gro_hw": "off [fixed]", 
                    "rx_udp_tunnel_port_offload": "off [fixed]", 
                    "rx_vlan_filter": "on [fixed]", 
                    "rx_vlan_offload": "on", 
                    "rx_vlan_stag_filter": "off [fixed]", 
                    "rx_vlan_stag_hw_parse": "off [fixed]", 
                    "scatter_gather": "on", 
                    "tcp_segmentation_offload": "on", 
                    "tx_checksum_fcoe_crc": "off [fixed]", 
                    "tx_checksum_ip_generic": "on", 
                    "tx_checksum_ipv4": "off [fixed]", 
                    "tx_checksum_ipv6": "off [fixed]", 
                    "tx_checksum_sctp": "off [fixed]", 
                    "tx_checksumming": "on", 
                    "tx_fcoe_segmentation": "off [fixed]", 
                    "tx_gre_csum_segmentation": "off [fixed]", 
                    "tx_gre_segmentation": "off [fixed]", 
                    "tx_gso_partial": "off [fixed]", 
                    "tx_gso_robust": "off [fixed]", 
                    "tx_ipip_segmentation": "off [fixed]", 
                    "tx_lockless": "off [fixed]", 
                    "tx_nocache_copy": "off", 
                    "tx_scatter_gather": "on", 
                    "tx_scatter_gather_fraglist": "off [fixed]", 
                    "tx_sctp_segmentation": "off [fixed]", 
                    "tx_sit_segmentation": "off [fixed]", 
                    "tx_tcp6_segmentation": "off [fixed]", 
                    "tx_tcp_ecn_segmentation": "off [fixed]", 
                    "tx_tcp_mangleid_segmentation": "off", 
                    "tx_tcp_segmentation": "on", 
                    "tx_udp_tnl_csum_segmentation": "off [fixed]", 
                    "tx_udp_tnl_segmentation": "off [fixed]", 
                    "tx_vlan_offload": "on [fixed]", 
                    "tx_vlan_stag_hw_insert": "off [fixed]", 
                    "udp_fragmentation_offload": "off [fixed]", 
                    "vlan_challenged": "off [fixed]"
                }, 
                "hw_timestamp_filters": [], 
                "ipv4": {
                    "address": "192.168.56.111", 
                    "broadcast": "192.168.56.255", 
                    "netmask": "255.255.255.0", 
                    "network": "192.168.56.0"
                }, 
                "ipv6": [
                    {
                        "address": "fe80::2b75:f84c:7d7f:597d", 
                        "prefix": "64", 
                        "scope": "link"
                    }, 
                    {
                        "address": "fe80::864f:a509:1db0:a8fa", 
                        "prefix": "64", 
                        "scope": "link"
                    }
                ], 
                "macaddress": "08:00:27:5d:9d:7c", 
                "module": "e1000", 
                "mtu": 1500, 
                "pciid": "0000:00:03.0", 
                "promisc": false, 
                "speed": 1000, 
                "timestamping": [
                    "tx_software", 
                    "rx_software", 
                    "software"
                ], 
                "type": "ether"
            }, 
            "enp0s8": {
                "active": true, 
                "device": "enp0s8", 
                "features": {
                    "busy_poll": "off [fixed]", 
                    "fcoe_mtu": "off [fixed]", 
                    "generic_receive_offload": "on", 
                    "generic_segmentation_offload": "on", 
                    "highdma": "off [fixed]", 
                    "hw_tc_offload": "off [fixed]", 
                    "l2_fwd_offload": "off [fixed]", 
                    "large_receive_offload": "off [fixed]", 
                    "loopback": "off [fixed]", 
                    "netns_local": "off [fixed]", 
                    "ntuple_filters": "off [fixed]", 
                    "receive_hashing": "off [fixed]", 
                    "rx_all": "off", 
                    "rx_checksumming": "off", 
                    "rx_fcs": "off", 
                    "rx_gro_hw": "off [fixed]", 
                    "rx_udp_tunnel_port_offload": "off [fixed]", 
                    "rx_vlan_filter": "on [fixed]", 
                    "rx_vlan_offload": "on", 
                    "rx_vlan_stag_filter": "off [fixed]", 
                    "rx_vlan_stag_hw_parse": "off [fixed]", 
                    "scatter_gather": "on", 
                    "tcp_segmentation_offload": "on", 
                    "tx_checksum_fcoe_crc": "off [fixed]", 
                    "tx_checksum_ip_generic": "on", 
                    "tx_checksum_ipv4": "off [fixed]", 
                    "tx_checksum_ipv6": "off [fixed]", 
                    "tx_checksum_sctp": "off [fixed]", 
                    "tx_checksumming": "on", 
                    "tx_fcoe_segmentation": "off [fixed]", 
                    "tx_gre_csum_segmentation": "off [fixed]", 
                    "tx_gre_segmentation": "off [fixed]", 
                    "tx_gso_partial": "off [fixed]", 
                    "tx_gso_robust": "off [fixed]", 
                    "tx_ipip_segmentation": "off [fixed]", 
                    "tx_lockless": "off [fixed]", 
                    "tx_nocache_copy": "off", 
                    "tx_scatter_gather": "on", 
                    "tx_scatter_gather_fraglist": "off [fixed]", 
                    "tx_sctp_segmentation": "off [fixed]", 
                    "tx_sit_segmentation": "off [fixed]", 
                    "tx_tcp6_segmentation": "off [fixed]", 
                    "tx_tcp_ecn_segmentation": "off [fixed]", 
                    "tx_tcp_mangleid_segmentation": "off", 
                    "tx_tcp_segmentation": "on", 
                    "tx_udp_tnl_csum_segmentation": "off [fixed]", 
                    "tx_udp_tnl_segmentation": "off [fixed]", 
                    "tx_vlan_offload": "on [fixed]", 
                    "tx_vlan_stag_hw_insert": "off [fixed]", 
                    "udp_fragmentation_offload": "off [fixed]", 
                    "vlan_challenged": "off [fixed]"
                }, 
                "hw_timestamp_filters": [], 
                "ipv4": {
                    "address": "10.0.3.15", 
                    "broadcast": "10.0.3.255", 
                    "netmask": "255.255.255.0", 
                    "network": "10.0.3.0"
                }, 
                "ipv6": [
                    {
                        "address": "fe80::3fbb:b032:5bd8:ffe9", 
                        "prefix": "64", 
                        "scope": "link"
                    }
                ], 
                "macaddress": "08:00:27:80:41:e6", 
                "module": "e1000", 
                "mtu": 1500, 
                "pciid": "0000:00:08.0", 
                "promisc": false, 
                "speed": 1000, 
                "timestamping": [
                    "tx_software", 
                    "rx_software", 
                    "software"
                ], 
                "type": "ether"
            }, 
            "env": {
                "HOME": "/home/ansible", 
                "LANG": "en_US.UTF-8", 
                "LC_ALL": "en_US.UTF-8", 
                "LESSOPEN": "||/usr/bin/lesspipe.sh %s", 
                "LOGNAME": "ansible", 
                "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:", 
                "MAIL": "/var/mail/ansible", 
                "PATH": "/usr/local/bin:/usr/bin", 
                "PWD": "/home/ansible", 
                "SHELL": "/bin/bash", 
                "SHLVL": "2", 
                "SSH_CLIENT": "192.168.56.110 43440 22", 
                "SSH_CONNECTION": "192.168.56.110 43440 192.168.56.111 22", 
                "SSH_TTY": "/dev/pts/1", 
                "TERM": "xterm", 
                "USER": "ansible", 
                "XDG_RUNTIME_DIR": "/run/user/1001", 
                "XDG_SESSION_ID": "14", 
                "YOUR_KEY": "dfdsafhdsfdhsfjkh3423fsdhfkjgfdsgfdsjgfjafjk342hi2rhehfjkshd", 
                "_": "/usr/bin/python"
            }, 
            "fibre_channel_wwn": [], 
            "fips": false, 
            "form_factor": "Other", 
            "fqdn": "node1.ansible.com", 
            "gather_subset": [
                "all"
            ], 
            "hostname": "node1", 
            "hostnqn": "", 
            "interfaces": [
                "lo", 
                "enp0s3", 
                "enp0s8"
            ], 
            "is_chroot": true, 
            "iscsi_iqn": "", 
            "kernel": "3.10.0-957.el7.x86_64", 
            "kernel_version": "#1 SMP Thu Nov 8 23:39:32 UTC 2018", 
            "lo": {
                "active": true, 
                "device": "lo", 
                "features": {
                    "busy_poll": "off [fixed]", 
                    "fcoe_mtu": "off [fixed]", 
                    "generic_receive_offload": "on", 
                    "generic_segmentation_offload": "on", 
                    "highdma": "on [fixed]", 
                    "hw_tc_offload": "off [fixed]", 
                    "l2_fwd_offload": "off [fixed]", 
                    "large_receive_offload": "off [fixed]", 
                    "loopback": "on [fixed]", 
                    "netns_local": "on [fixed]", 
                    "ntuple_filters": "off [fixed]", 
                    "receive_hashing": "off [fixed]", 
                    "rx_all": "off [fixed]", 
                    "rx_checksumming": "on [fixed]", 
                    "rx_fcs": "off [fixed]", 
                    "rx_gro_hw": "off [fixed]", 
                    "rx_udp_tunnel_port_offload": "off [fixed]", 
                    "rx_vlan_filter": "off [fixed]", 
                    "rx_vlan_offload": "off [fixed]", 
                    "rx_vlan_stag_filter": "off [fixed]", 
                    "rx_vlan_stag_hw_parse": "off [fixed]", 
                    "scatter_gather": "on", 
                    "tcp_segmentation_offload": "on", 
                    "tx_checksum_fcoe_crc": "off [fixed]", 
                    "tx_checksum_ip_generic": "on [fixed]", 
                    "tx_checksum_ipv4": "off [fixed]", 
                    "tx_checksum_ipv6": "off [fixed]", 
                    "tx_checksum_sctp": "on [fixed]", 
                    "tx_checksumming": "on", 
                    "tx_fcoe_segmentation": "off [fixed]", 
                    "tx_gre_csum_segmentation": "off [fixed]", 
                    "tx_gre_segmentation": "off [fixed]", 
                    "tx_gso_partial": "off [fixed]", 
                    "tx_gso_robust": "off [fixed]", 
                    "tx_ipip_segmentation": "off [fixed]", 
                    "tx_lockless": "on [fixed]", 
                    "tx_nocache_copy": "off [fixed]", 
                    "tx_scatter_gather": "on [fixed]", 
                    "tx_scatter_gather_fraglist": "on [fixed]", 
                    "tx_sctp_segmentation": "on", 
                    "tx_sit_segmentation": "off [fixed]", 
                    "tx_tcp6_segmentation": "on", 
                    "tx_tcp_ecn_segmentation": "on", 
                    "tx_tcp_mangleid_segmentation": "on", 
                    "tx_tcp_segmentation": "on", 
                    "tx_udp_tnl_csum_segmentation": "off [fixed]", 
                    "tx_udp_tnl_segmentation": "off [fixed]", 
                    "tx_vlan_offload": "off [fixed]", 
                    "tx_vlan_stag_hw_insert": "off [fixed]", 
                    "udp_fragmentation_offload": "on", 
                    "vlan_challenged": "on [fixed]"
                }, 
                "hw_timestamp_filters": [], 
                "ipv4": {
                    "address": "127.0.0.1", 
                    "broadcast": "host", 
                    "netmask": "255.0.0.0", 
                    "network": "127.0.0.0"
                }, 
                "ipv6": [
                    {
                        "address": "::1", 
                        "prefix": "128", 
                        "scope": "host"
                    }
                ], 
                "mtu": 65536, 
                "promisc": false, 
                "timestamping": [
                    "rx_software", 
                    "software"
                ], 
                "type": "loopback"
            }, 
            "lsb": {}, 
            "machine": "x86_64", 
            "machine_id": "9c593f2fc95d4e9b962892c9f2c7698a", 
            "memfree_mb": 1576, 
            "memory_mb": {
                "nocache": {
                    "free": 1686, 
                    "used": 152
                }, 
                "real": {
                    "free": 1576, 
                    "total": 1838, 
                    "used": 262
                }, 
                "swap": {
                    "cached": 0, 
                    "free": 2047, 
                    "total": 2047, 
                    "used": 0
                }
            }, 
            "memtotal_mb": 1838, 
            "module_setup": true, 
            "mounts": [
                {
                    "block_available": 222631, 
                    "block_size": 4096, 
                    "block_total": 259584, 
                    "block_used": 36953, 
                    "device": "/dev/sda1", 
                    "fstype": "xfs", 
                    "inode_available": 523961, 
                    "inode_total": 524288, 
                    "inode_used": 327, 
                    "mount": "/boot", 
                    "options": "rw,relatime,attr2,inode64,noquota", 
                    "size_available": 911896576, 
                    "size_total": 1063256064, 
                    "uuid": "4418f5f3-1e44-442b-95d6-d986e27acbfd"
                }, 
                {
                    "block_available": 3911952, 
                    "block_size": 4096, 
                    "block_total": 4452864, 
                    "block_used": 540912, 
                    "device": "/dev/mapper/centos-root", 
                    "fstype": "xfs", 
                    "inode_available": 8860419, 
                    "inode_total": 8910848, 
                    "inode_used": 50429, 
                    "mount": "/", 
                    "options": "rw,relatime,attr2,inode64,noquota", 
                    "size_available": 16023355392, 
                    "size_total": 18238930944, 
                    "uuid": "b902127e-4281-435a-ac4f-43c89cc21897"
                }
            ], 
            "nodename": "node1.ansible.com", 
            "os_family": "RedHat", 
            "pkg_mgr": "yum", 
            "proc_cmdline": {
                "BOOT_IMAGE": "/vmlinuz-3.10.0-957.el7.x86_64", 
                "LANG": "en_US.UTF-8", 
                "crashkernel": "auto", 
                "quiet": true, 
                "rd.lvm.lv": [
                    "centos/root", 
                    "centos/swap"
                ], 
                "rhgb": true, 
                "ro": true, 
                "root": "/dev/mapper/centos-root"
            }, 
            "processor": [
                "0", 
                "GenuineIntel", 
                "Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz"
            ], 
            "processor_cores": 1, 
            "processor_count": 1, 
            "processor_threads_per_core": 1, 
            "processor_vcpus": 1, 
            "product_name": "VirtualBox", 
            "product_serial": "NA", 
            "product_uuid": "NA", 
            "product_version": "1.2", 
            "python": {
                "executable": "/usr/bin/python", 
                "has_sslcontext": true, 
                "type": "CPython", 
                "version": {
                    "major": 2, 
                    "micro": 5, 
                    "minor": 7, 
                    "releaselevel": "final", 
                    "serial": 0
                }, 
                "version_info": [
                    2, 
                    7, 
                    5, 
                    "final", 
                    0
                ]
            }, 
            "python_version": "2.7.5", 
            "real_group_id": 1001, 
            "real_user_id": 1001, 
            "selinux": {
                "status": "disabled"
            }, 
            "selinux_python_present": true, 
            "service_mgr": "systemd", 
            "ssh_host_key_ecdsa_public": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBCdtvirfdRqiXDnJV+4cHnIx6ogqaZoypiLgYntTBwjqKHUximafQc/iYf+F8CuW6Ly532K69lIjtCtHEQpCZag=", 
            "ssh_host_key_ed25519_public": "AAAAC3NzaC1lZDI1NTE5AAAAIAl7nO9kxvd44yLD0SWqdflD/BbwsiJSMlhaJjuMi5Kc", 
            "ssh_host_key_rsa_public": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDiMRJ4JBNDpx7Ud13uvhZ+jWg6B2nrkaFX1nsUqovJJu/5Z5I/xKcLd3F3Jql7oxK8ysXlvP5qx/TEriFW0dN6Gl1qzeqVSCh24yt3oYJJgXklum6H+HTnaHWc9stdw09FJwppOmcLal6JQfNaNKQuNJQocDMu/xbS0XHdgYPV6LEdixkVetizIiiUv0DhkVYrKAsj2kB/PYtjjonp8ehQPhm4LVkiN89Db8L05rAZcokAD4cLtKxqyKUYUKJbbu4Hdg7wSx/sOvSX9xvTMpwZ9UHbvykwKrwC/qe9208cXk44w+C16NM1Ufy8rgphgf+B6tH12Uc8FesEqmcII50p", 
            "swapfree_mb": 2047, 
            "swaptotal_mb": 2047, 
            "system": "Linux", 
            "system_capabilities": [
                ""
            ], 
            "system_capabilities_enforced": "True", 
            "system_vendor": "innotek GmbH", 
            "uptime_seconds": 10279, 
            "user_dir": "/home/ansible", 
            "user_gecos": "", 
            "user_gid": 1001, 
            "user_id": "ansible", 
            "user_shell": "/bin/bash", 
            "user_uid": 1001, 
            "userspace_architecture": "x86_64", 
            "userspace_bits": "64", 
            "virtualization_role": "guest", 
            "virtualization_type": "virtualbox"
        }, 
        "ansible_fibre_channel_wwn": [], 
        "ansible_fips": false, 
        "ansible_forks": 5, 
        "ansible_form_factor": "Other", 
        "ansible_fqdn": "node1.ansible.com", 
        "ansible_hostname": "node1", 
        "ansible_hostnqn": "", 
        "ansible_interfaces": [
            "lo", 
            "enp0s3", 
            "enp0s8"
        ], 
        "ansible_inventory_sources": [
            "/etc/ansible/hosts"
        ], 
        "ansible_is_chroot": true, 
        "ansible_iscsi_iqn": "", 
        "ansible_kernel": "3.10.0-957.el7.x86_64", 
        "ansible_kernel_version": "#1 SMP Thu Nov 8 23:39:32 UTC 2018", 
        "ansible_lo": {
            "active": true, 
            "device": "lo", 
            "features": {
                "busy_poll": "off [fixed]", 
                "fcoe_mtu": "off [fixed]", 
                "generic_receive_offload": "on", 
                "generic_segmentation_offload": "on", 
                "highdma": "on [fixed]", 
                "hw_tc_offload": "off [fixed]", 
                "l2_fwd_offload": "off [fixed]", 
                "large_receive_offload": "off [fixed]", 
                "loopback": "on [fixed]", 
                "netns_local": "on [fixed]", 
                "ntuple_filters": "off [fixed]", 
                "receive_hashing": "off [fixed]", 
                "rx_all": "off [fixed]", 
                "rx_checksumming": "on [fixed]", 
                "rx_fcs": "off [fixed]", 
                "rx_gro_hw": "off [fixed]", 
                "rx_udp_tunnel_port_offload": "off [fixed]", 
                "rx_vlan_filter": "off [fixed]", 
                "rx_vlan_offload": "off [fixed]", 
                "rx_vlan_stag_filter": "off [fixed]", 
                "rx_vlan_stag_hw_parse": "off [fixed]", 
                "scatter_gather": "on", 
                "tcp_segmentation_offload": "on", 
                "tx_checksum_fcoe_crc": "off [fixed]", 
                "tx_checksum_ip_generic": "on [fixed]", 
                "tx_checksum_ipv4": "off [fixed]", 
                "tx_checksum_ipv6": "off [fixed]", 
                "tx_checksum_sctp": "on [fixed]", 
                "tx_checksumming": "on", 
                "tx_fcoe_segmentation": "off [fixed]", 
                "tx_gre_csum_segmentation": "off [fixed]", 
                "tx_gre_segmentation": "off [fixed]", 
                "tx_gso_partial": "off [fixed]", 
                "tx_gso_robust": "off [fixed]", 
                "tx_ipip_segmentation": "off [fixed]", 
                "tx_lockless": "on [fixed]", 
                "tx_nocache_copy": "off [fixed]", 
                "tx_scatter_gather": "on [fixed]", 
                "tx_scatter_gather_fraglist": "on [fixed]", 
                "tx_sctp_segmentation": "on", 
                "tx_sit_segmentation": "off [fixed]", 
                "tx_tcp6_segmentation": "on", 
                "tx_tcp_ecn_segmentation": "on", 
                "tx_tcp_mangleid_segmentation": "on", 
                "tx_tcp_segmentation": "on", 
                "tx_udp_tnl_csum_segmentation": "off [fixed]", 
                "tx_udp_tnl_segmentation": "off [fixed]", 
                "tx_vlan_offload": "off [fixed]", 
                "tx_vlan_stag_hw_insert": "off [fixed]", 
                "udp_fragmentation_offload": "on", 
                "vlan_challenged": "on [fixed]"
            }, 
            "hw_timestamp_filters": [], 
            "ipv4": {
                "address": "127.0.0.1", 
                "broadcast": "host", 
                "netmask": "255.0.0.0", 
                "network": "127.0.0.0"
            }, 
            "ipv6": [
                {
                    "address": "::1", 
                    "prefix": "128", 
                    "scope": "host"
                }
            ], 
            "mtu": 65536, 
            "promisc": false, 
            "timestamping": [
                "rx_software", 
                "software"
            ], 
            "type": "loopback"
        }, 
        "ansible_local": {}, 
        "ansible_lsb": {}, 
        "ansible_machine": "x86_64", 
        "ansible_machine_id": "9c593f2fc95d4e9b962892c9f2c7698a", 
        "ansible_memfree_mb": 1576, 
        "ansible_memory_mb": {
            "nocache": {
                "free": 1686, 
                "used": 152
            }, 
            "real": {
                "free": 1576, 
                "total": 1838, 
                "used": 262
            }, 
            "swap": {
                "cached": 0, 
                "free": 2047, 
                "total": 2047, 
                "used": 0
            }
        }, 
        "ansible_memtotal_mb": 1838, 
        "ansible_mounts": [
            {
                "block_available": 222631, 
                "block_size": 4096, 
                "block_total": 259584, 
                "block_used": 36953, 
                "device": "/dev/sda1", 
                "fstype": "xfs", 
                "inode_available": 523961, 
                "inode_total": 524288, 
                "inode_used": 327, 
                "mount": "/boot", 
                "options": "rw,relatime,attr2,inode64,noquota", 
                "size_available": 911896576, 
                "size_total": 1063256064, 
                "uuid": "4418f5f3-1e44-442b-95d6-d986e27acbfd"
            }, 
            {
                "block_available": 3911952, 
                "block_size": 4096, 
                "block_total": 4452864, 
                "block_used": 540912, 
                "device": "/dev/mapper/centos-root", 
                "fstype": "xfs", 
                "inode_available": 8860419, 
                "inode_total": 8910848, 
                "inode_used": 50429, 
                "mount": "/", 
                "options": "rw,relatime,attr2,inode64,noquota", 
                "size_available": 16023355392, 
                "size_total": 18238930944, 
                "uuid": "b902127e-4281-435a-ac4f-43c89cc21897"
            }
        ], 
        "ansible_nodename": "node1.ansible.com", 
        "ansible_os_family": "RedHat", 
        "ansible_pkg_mgr": "yum", 
        "ansible_playbook_python": "/usr/bin/python2", 
        "ansible_proc_cmdline": {
            "BOOT_IMAGE": "/vmlinuz-3.10.0-957.el7.x86_64", 
            "LANG": "en_US.UTF-8", 
            "crashkernel": "auto", 
            "quiet": true, 
            "rd.lvm.lv": [
                "centos/root", 
                "centos/swap"
            ], 
            "rhgb": true, 
            "ro": true, 
            "root": "/dev/mapper/centos-root"
        }, 
        "ansible_processor": [
            "0", 
            "GenuineIntel", 
            "Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz"
        ], 
        "ansible_processor_cores": 1, 
        "ansible_processor_count": 1, 
        "ansible_processor_threads_per_core": 1, 
        "ansible_processor_vcpus": 1, 
        "ansible_product_name": "VirtualBox", 
        "ansible_product_serial": "NA", 
        "ansible_product_uuid": "NA", 
        "ansible_product_version": "1.2", 
        "ansible_python": {
            "executable": "/usr/bin/python", 
            "has_sslcontext": true, 
            "type": "CPython", 
            "version": {
                "major": 2, 
                "micro": 5, 
                "minor": 7, 
                "releaselevel": "final", 
                "serial": 0
            }, 
            "version_info": [
                2, 
                7, 
                5, 
                "final", 
                0
            ]
        }, 
        "ansible_python_version": "2.7.5", 
        "ansible_real_group_id": 1001, 
        "ansible_real_user_id": 1001, 
        "ansible_run_tags": [
            "all"
        ], 
        "ansible_selinux": {
            "status": "disabled"
        }, 
        "ansible_selinux_python_present": true, 
        "ansible_service_mgr": "systemd", 
        "ansible_skip_tags": [], 
        "ansible_ssh_host_key_ecdsa_public": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBCdtvirfdRqiXDnJV+4cHnIx6ogqaZoypiLgYntTBwjqKHUximafQc/iYf+F8CuW6Ly532K69lIjtCtHEQpCZag=", 
        "ansible_ssh_host_key_ed25519_public": "AAAAC3NzaC1lZDI1NTE5AAAAIAl7nO9kxvd44yLD0SWqdflD/BbwsiJSMlhaJjuMi5Kc", 
        "ansible_ssh_host_key_rsa_public": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDiMRJ4JBNDpx7Ud13uvhZ+jWg6B2nrkaFX1nsUqovJJu/5Z5I/xKcLd3F3Jql7oxK8ysXlvP5qx/TEriFW0dN6Gl1qzeqVSCh24yt3oYJJgXklum6H+HTnaHWc9stdw09FJwppOmcLal6JQfNaNKQuNJQocDMu/xbS0XHdgYPV6LEdixkVetizIiiUv0DhkVYrKAsj2kB/PYtjjonp8ehQPhm4LVkiN89Db8L05rAZcokAD4cLtKxqyKUYUKJbbu4Hdg7wSx/sOvSX9xvTMpwZ9UHbvykwKrwC/qe9208cXk44w+C16NM1Ufy8rgphgf+B6tH12Uc8FesEqmcII50p", 
        "ansible_swapfree_mb": 2047, 
        "ansible_swaptotal_mb": 2047, 
        "ansible_system": "Linux", 
        "ansible_system_capabilities": [
            ""
        ], 
        "ansible_system_capabilities_enforced": "True", 
        "ansible_system_vendor": "innotek GmbH", 
        "ansible_uptime_seconds": 10279, 
        "ansible_user_dir": "/home/ansible", 
        "ansible_user_gecos": "", 
        "ansible_user_gid": 1001, 
        "ansible_user_id": "ansible", 
        "ansible_user_shell": "/bin/bash", 
        "ansible_user_uid": 1001, 
        "ansible_userspace_architecture": "x86_64", 
        "ansible_userspace_bits": "64", 
        "ansible_verbosity": 4, 
        "ansible_version": {
            "full": "2.9.9", 
            "major": 2, 
            "minor": 9, 
            "revision": 9, 
            "string": "2.9.9"
        }, 
        "ansible_virtualization_role": "guest", 
        "ansible_virtualization_type": "virtualbox", 
        "discovered_interpreter_python": "/usr/bin/python", 
        "gather_subset": [
            "all"
        ], 
        "group_names": [
            "webservers"
        ], 
        "groups": {
            "all": [
                "node3", 
                "docker-node", 
                "node1", 
                "node2"
            ], 
            "dbservers": [
                "node2"
            ], 
            "ungrouped": [
                "node3", 
                "docker-node"
            ], 
            "webservers": [
                "node1"
            ]
        }, 
        "inventory_dir": "/etc/ansible", 
        "inventory_file": "/etc/ansible/hosts", 
        "inventory_hostname": "node1", 
        "inventory_hostname_short": "node1", 
        "module_setup": true, 
        "omit": "__omit_place_holder__c424340b5d84e8c4c33f1866fd42b8746c1b10a2", 
        "playbook_dir": "/home/ansible", 
        "result": {
            "changed": true, 
            "cmd": [
                "hostname", 
                "-I"
            ], 
            "delta": "0:00:00.002076", 
            "end": "2020-07-27 17:18:16.575369", 
            "failed": false, 
            "rc": 0, 
            "start": "2020-07-27 17:18:16.573293", 
            "stderr": "", 
            "stderr_lines": [], 
            "stdout": "192.168.56.111 10.0.3.15 ", 
            "stdout_lines": [
                "192.168.56.111 10.0.3.15 "
            ]
        }
    }
}

TASK [debug] *************************************************************************
task path: /home/ansible/debug.yml:33
ok: [node1] => {
    "msg": [
        "Provisioning based on YOUR_KEY which is: myansiblekeyinmaster..432fdsfdsafdsadb", 
        "These servers were built using the password of 'securedockerpassword'. Please retain this for later use."
    ]
}
META: ran handlers
META: ran handlers

PLAY RECAP ***************************************************************************
node1                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

可以看到，此时所有任务都执行了，并且没有忽略任何任务。

## 4. register注册变量

我们在剧本中也可以使用`register`关键字来注册变量，然后在后续的任务中使用变量。

以下示例是将`hostname`的输出注册到`info`变量中，然后在后一个任务中打印变量的信息：

剧本文件`register.yml`的内容如下：

```yaml
---
- hosts: node1
  tasks:
    - name: register variable
      ansible.builtin.command:
        cmd: hostname
      register: info

    - name: display variable
      ansible.builtin.debug:
        msg: The variable is {{ info['stdout'] }}

```

执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint register.yml
[ansible@master ansible_playbooks]$ ansible-playbook register.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [register variable] ***********************************************************************************************
changed: [node1] => {"changed": true, "cmd": ["hostname"], "delta": "0:00:00.010386", "end": "2023-07-22 19:34:55.456539", "rc": 0, "start": "2023-07-22 19:34:55.446153", "stderr": "", "stderr_lines": [], "stdout": "node1", "stdout_lines": ["node1"]}

TASK [display variable] ************************************************************************************************
ok: [node1] => {
    "msg": "The variable is node1"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

效果图如下：

![](/img/Snipaste_2023-07-22_19-38-04.png)

## 5. 在剧本中使用vars定义变量

也可以在剧本中通过`vars`关键字来定义变量。

以下示例`variable.yml`中用`vars`关键字定义了两个变量：

```yaml
---
- hosts: node1
  # 定义变量
  vars:
    - service_name: Nginx
    - listen_port: 80

  tasks:
    - name: display variable from variable list
      ansible.builtin.debug:
        msg: The service name is {{ service_name }} and the listen port is {{ listen_port }}

```

执行剧本文件：

```sh
[ansible@master ansible_playbooks]$ ansible-lint variable.yml
[ansible@master ansible_playbooks]$ ansible-playbook variable.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from variable list] *****************************************************************************
ok: [node1] => {
    "msg": "The service name is Nginx and the listen port is 80"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

效果图如下：

![](/img/Snipaste_2023-07-22_22-24-18.png)

可以看到，成功获取到变量`service_name`和`listen_port`的值了。

## 6. 在剧本中使用vars_files指定变量文件

我们也可以将变量写到文件中，然后在剧本中使用`vars_files`关键字来指定变量文件，请看以下示例。

首先，创建`vars`文件夹，并在`vars`文件夹下创建两个变量定义文件：

```sh
# 创建存放变量文件的文件夹
[ansible@master ansible_playbooks]$ mkdir vars

# 查看变量定义文件内容：
[ansible@master ansible_playbooks]$ cat vars/vars_file1.yaml
---
  - service_name1: Nginx
  - service_name2: Redis

[ansible@master ansible_playbooks]$ cat vars/vars_file2.yaml
---
  - listen_port1: 80
  - listen_port2: 6379

[ansible@master ansible_playbooks]$
```

编写剧本文件`vars_files.yml`:

```yaml
---
- hosts: node1
  # 定义变量文件
  vars_files:
    - vars/vars_file1.yaml
    - vars/vars_file2.yaml

  tasks:
    - name: display variable from variable list
      ansible.builtin.debug:
        msg: |
          The first service name is {{ service_name1 }} and the listen port is {{ listen_port1 }}.
          The second service name is {{ service_name2 }} and the listen port is {{ listen_port2 }}.

```

然后执行`vars_files.yml`剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint vars_files.yml
[ansible@master ansible_playbooks]$ ansible-playbook vars_files.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from variable list] *****************************************************************************
ok: [node1] => {
    "msg": "The first service name is Nginx and the listen port is 80.\nThe second service name is Redis and the listen port is 6379.\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

效果图如下：

![](/img/Snipaste_2023-07-23_22-41-57.png)
可以看到，正常从两个变量文件中获取到了服务的名称和服务的监听端口信息。

## 7. 使用vars_prompt通过交互模式获取变量

- Ansible还支持在运行剧本的时候，通过交互式的方式给定义的参数传入变量值，只需要在剧本中定义`vars_prompt`的变量名和交互式提示内容即可。
- Ansible也可以对输入的变量值进行加密处理，如采用SHA512和MD5算法加密。

以下编写一个`vars_prompt.yml`的剧本，用于在交互模式下读取服务的名称和监听端口：

```yaml
---
- hosts: node1
  # 定义交互式获取变量
  vars_prompt:
    - name: service_name
      prompt: please input the service name
      # 非私有时，会显示输入的变量值
      private: no
    - name: listen_port
      prompt: please input the service listen port
      # 设置默认端口号，也可以不设置
      default: 6666
      # 私有时。不会显示输入的变量值，对于密码输入的话，可以避免密码泄漏
      private: yes

  tasks:
    - name: display variable from variable list
      ansible.builtin.debug:
        msg: |
          The first service name is {{ service_name }} and the listen port is {{ listen_port }}.

```

运行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint vars_prompt.yml
[ansible@master ansible_playbooks]$ ansible-playbook vars_prompt.yml -v
Using /etc/ansible/ansible.cfg as config file
please input the service name: Tomcat  #<--- 此处输入了服务名称为Tomcat
please input the service listen port [6666]:   #<--- 此处未输入任何值，直接按的回车键，使用了默认的监听端口号6666

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from variable list] *****************************************************************************
ok: [node1] => {
    "msg": "The first service name is Tomcat and the listen port is 6666.\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$ ansible-playbook vars_prompt.yml -v
Using /etc/ansible/ansible.cfg as config file
please input the service name: tomcat   #<--- 此处输入了服务名称为tomcat
please input the service listen port [6666]:   #<--- 此处输入了服务监听端口号为8080

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [display variable from variable list] *****************************************************************************
ok: [node1] => {
    "msg": "The first service name is tomcat and the listen port is 8080.\n"
}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

效果图如下：

![](/img/Snipaste_2023-07-23_23-13-49.png)
可以看到，正常获取到了交互模式下用户输入的变量信息，服务名称和服务监听端口号都正常获取到了。

另外，还可以创建加密的变量，用于设置密码信息等。可参考： [ansible基础用法6_prompt 交互变量的使用](https://blog.csdn.net/zuopiezia/article/details/100762399), 后续再进行测试。

## 8.对用户输入的密码进行加密


在一节中，我们使用`vars_prompt`获取了用户的输入信息，并存储到变量中，最后打印出了用户的输入。这一节我们通过`vars_prompt`获取用户输入的密码信息，并进行加密。

### 8.1 基础知识说明

我们可以查看当前操作系统所使用的密码加密算法：

```sh
[root@node1 ~]# authconfig --test|grep hashing
 password hashing algorithm is md5
```

可以看到，当前系统密码加密算法是md5加密算法。

查看当前操作系统支持的加密算法：

```sh
[root@node1 ~]# authconfig --help|grep passalgo
  --passalgo=<descrypt|bigcrypt|md5|sha256|sha512>
```

如果要修改加密算法，可以使用以下命令：

```sh
authconfig --passalgo=sha512 --update
```

详细可参考： [Configuring System Passwords Using authconfig](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system-level_authentication_guide/authconfig-pwd)

> 密码加密算法原理
> 
> 在Linux系统中，用户密码存储在/etc/passwd文件中。但是，由于该文件权限是任何用户都可以读取的，所以直接将密码明文存储在文件中会造成安全漏洞。因此，Linux系统使用密码加密算法对用户密码进行加密。
> 
> Linux密码加密算法使用一个称为“加盐”的过程，即在密码明文的基础上添加一段随机字符串，再进行加密，最后将随机字符串和密码密文一同存储在/etc/shadow文件中。这样做的好处是让攻击者无法预测密码明文和随机字符串，增加了暴力破解密码的难度。


### 8.2 使用passlib库生成密码

参考：[passlib.hash - Password Hashing Schemes](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.html)

我们此处仅考虑和测试MD5、SHA-256、SHA-512三种加密算法。

由参考文档中已经标记MD5算法不再认为是安全的算法，推荐使用SHA-256或SHA-512加密算法。

我们来测试一下：

```py
[root@master ~]# python3
Python 3.6.8 (default, Nov 16 2020, 16:55:22)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from passlib.hash import md5_crypt, sha256_crypt, sha512_crypt
# 使用md5加密算法加密
>>> h = md5_crypt.hash("password")
>>> h
'$1$CjxICQF7$JOGLwFLcRheFJoR9YIaPz/'
>>>

# 使用SHA-256加密算法加密
>>> hash = sha256_crypt.hash("password")
>>> hash
'$5$rounds=535000$nhLk2HVjQisH0yV1$zgGQefxxGsiPzWdVXsskOTRQhojts3iOrV3sJH4koQ1'

# 设置轮转次数为12345次
>>> sha256_crypt.using(rounds=12345).hash("password")
'$5$rounds=12345$Q4Gzj5vvcuJHHvSV$JU3lO2oip.mQxomTSxTChhev8vRS7bD79wlMYhzcIXA'

# 使用SHA-512加密算法加密
>>> hash512 = sha512_crypt.hash("password")
>>> hash512
'$6$rounds=656000$0SAk.X3/TEl4Hyko$nNKdA87kzVLaKeYxYUdUmYMMkXDshoNQF94y0FF62ofyz0d17eMVNpa6GePNTgAAisQKwSOf3X7p.IWELz9BT1'

# 使用SHA-512加密算法加密，使用自定义盐为mysalt
>>> hash512 = sha512_crypt.hash("password",salt="mysalt")
>>> hash512
'$6$rounds=656000$mysalt$3.xRZpxy/z008hs6wvfEK57aZTod.CF.Q.4B70uMKJOlUi242tjNpccHhrBMFok8iQxmzChlbZsofydrFB.0G.'

# 使用SHA-512加密算法加密，设置轮转次数为5000
>>> hash512 = sha512_crypt.using(rounds=5000).hash("password",salt="mysalt")
>>> hash512
'$6$mysalt$NN1QGsmCO0hcvplH4ahY6ocho6F6TgcY8yNdMFAeO.LAeFodNPGA6KsQM5Or1AKbE4QKSqnEsC/SE0Zz3ts9y1'
```

可以看到，根据官方规范，当rounds参数设置为5000时，可以从哈希字符串中省略它。

如果省略`rounds`轮转次数信息，我们可以看到在密码字符串中，密文由3部分组成,以”$”分隔,第一部分为ID,第二部分为盐值,第三部分为加密密文。

ID与加密算法间的对应关系：


| ID值 | 加密算法 |
|------|:---------|
| 1    | MD5      |
| 5    | SHA-256  |
| 6    | SHA-512  |


### 8.3 使用Ansible加密密码并创建用户

有了以上基础后，我们来使用Ansible加密密码并创建用户。


具体可参考： [Hashing values supplied by vars_prompt](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_prompts.html#hashing-values-supplied-by-vars-prompt)

编写剧本文件`vars_prompt_encrypt.yml`：

```yaml
---
- hosts: node1
  # 定义交互式获取变量
  vars_prompt:
    - name: user_name
      prompt: please input the user name
      # 非私有时，会显示输入的变量值
      private: no
    - name: user_password
      prompt: please input the user password
      encrypt: sha512_crypt
      # 需要两次输入密码确认
      confirm: true
      salt_size: 7
      # 私有时。不会显示输入的变量值，对于密码输入的话，可以避免密码泄漏
      private: yes

  tasks:
    - name: Create user
      ansible.builtin.user:
        name: "{{ user_name }}"
        comment: "使用vars_prompt创建用户{{ user_name }}"
        password: "{{ user_password }}"
      become: yes

```

执行剧本：

```sh
[ansible@master ansible_playbooks]$ ansible-lint vars_prompt_encrypt.yml
[ansible@master ansible_playbooks]$ ansible-playbook vars_prompt_encrypt.yml -v
Using /etc/ansible/ansible.cfg as config file
please input the user name: testvar  #<--- 输入用户名
please input the user password:  #<--- 输入密码，如我输入的是password
confirm please input the user password:  #<--- 再次输入密码password

PLAY [node1] ***********************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [node1]

TASK [Create user] *****************************************************************************************************
changed: [node1] => {"changed": true, "comment": "使用vars_prompt创建用户testvar", "create_home": true, "group": 1003, "home": "/home/testvar", "name": "testvar", "password": "NOT_LOGGING_PASSWORD", "shell": "/bin/bash", "state": "present", "system": false, "uid": 1003}

PLAY RECAP *************************************************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[ansible@master ansible_playbooks]$
```

可以看到，剧本执行成功，效果图如下：

![](/img/Snipaste_2023-07-25_00-19-19.png)
此时，在节点1上面进行检查：

```sh
[root@node1 ~]# grep testvar /etc/passwd
testvar:x:1003:1003:使用vars_prompt创建用户testvar:/home/testvar:/bin/bash
[root@node1 ~]# grep testvar /etc/shadow
testvar:$6$ZPe383L$WJwlTUJ1iPj9cN1ZcH0W352jU.PPpX2lGr.dzhpR0lS/k9.jym3sztBkCXAafWMmbNGWYFcucamv8QDp6izVV/:19562:0:99999:7:::
[root@node1 ~]#
```

可以看到，用户创建成功，用户的备注信息是"使用vars_prompt创建用户testvar",使用的密码加密算法ID是"6"，也就是SHA-512加密算法，生成的7位随机盐是"ZPe383L"，而生成的密码密文是“WJwlTUJ1iPj9cN1ZcH0W352jU.PPpX2lGr.dzhpR0lS/k9.jym3sztBkCXAafWMmbNGWYFcucamv8QDp6izVV/”。


尝试远程登陆：

```sh
$ ssh testvar@cloud-node1
testvar@cloud-node1's password:
Welcome to node1
[testvar@node1 ~]$ whoami
testvar
[testvar@node1 ~]$
```

可以看到，能成功登陆，说明刚才创建的用户配置是正确的！

最后，在节点node1上面删除刚才创建的用户testvar：

```sh
[root@node1 ~]# userdel --help
Usage: userdel [options] LOGIN

Options:
  -f, --force                   force some actions that would fail otherwise
                                e.g. removal of user still logged in
                                or files, even if not owned by the user
  -h, --help                    display this help message and exit
  -r, --remove                  remove home directory and mail spool
  -R, --root CHROOT_DIR         directory to chroot into
  -P, --prefix PREFIX_DIR       prefix directory where are located the /etc/* files
  -Z, --selinux-user            remove any SELinux user mapping for the user

[root@node1 ~]# userdel -r testvar
[root@node1 ~]# grep testvar /etc/passwd
[root@node1 ~]# grep testvar /etc/shadow
[root@node1 ~]#
```

这样，测试用户就删除成功了。

