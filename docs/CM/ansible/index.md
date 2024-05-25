# Ansible学习笔记

在官方文档中，你可以看到内置插件列表，传送门 [https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/index.html#plugin-index)

- Ansible集合了众多优秀运维工具(Puppet、Cfengine、Chef、Func、Fabric)的优点，实现了批量系统配置、批量程序部署、批量运行命令等功能。
- Ansible是基于模块工作的。本身没有批量部署的能力。真正具有批量部署的是Ansible所运行的模块，Ansible只是提供一种框架。
- Ansible采用paramiko协议库，通过SSH或者ZeroMQ等连接远程主机。
- Ansible是基于一致性、安全性、高可靠性设计的轻量级自动化工具。
- Ansible的配置管理脚本playbook语法基于YAML,它是一种可读性高、用来表达数据序列的格式标准。
- Ansible模块是声明式的(declarative)，你只需使用这些模块描述被管节点期望达到的状态。
- Ansible内置模块都是等幂性的(idempotent)，在被管节点上多次执行Ansible的剧本能达到同样的效果。
- 等幂性是指如果系统已经处于期望的状态，则对系统什么也不操作。
- Ansible命令都是并发执行的，我们可以针对目标主机执行任何命令。
- 默认的并发数目由`/etc/ansible/ansible.cfg`中的`forks`值来控制的。也可以在运行Ansible命令的时候通过`-f`/`--forks`参数指定并发数。默认值是`5`。**单台主机的性能始终有限，大家根据自己机器的硬件配置做调整，建议并发数配置为CPU核数偶数倍就好。如4CPU 8GB的服务器，建议最多并发20个线程。**
- 除了增加并发数，也可以通过以下方式优化Ansible速度，详细可参考[优化Ansible速度](./accelerate.md)：
  - 开启SSH长连接。
  - 开启pipelining。
  - 开启accelerate模式。
  - 设置facts缓存。
- `ansible`或`ansible-playbook`命令行都可以使用`-e`参数来添加其他环境变量，如`-e "name=Nginx"`，从文件读取(注意在文件名前加`@`符号)，如`-e "@var.yaml"`，此时`var.yaml`内容如下即可：
```yaml
---
name: Nginx
```

- 可以使用`register`关键字可以来注册变量，注册变量后，可以在剧本后续的任务中使用该变量。可以参考： [debug调试模块](./debug.md) 或 [Command命令模块](./command.md)
- 可以使用`with_items`对列表进行循环读取，可参考 [find查找模块](./find.md) 或[lineinfile文件内容修改模块](./lineinfile.md), ansible循环更详细的说明请参考 [ansible循环](./loop.md) 。
- 在剧本文件中可以使用`when`关键字来进行条件判断。`when`的值是一个条件表达式，如果条件判断成立，则对应的task任务会执行，否则对应的task任务不执行。这里所说的成立与不成立，就是Python语言中的`True`与`False`。条件表达式也支持多个条件之间`and`或者`or`。如果我们使用一个变量进行相应的判断，一定要清楚该变量的数据类型。可以参考[when条件判断](./when.md) 。
- 与`when`条件语句类似，我们可以使用`changed_when`语句和`failed_when`语句来对命令运行的结果进行判断。对于Ansible来说，其很难判断一个命令的运行是否符合我们的实际预期，尤其是当我们使用`command`模块和`shell`模块时，如果不使用`changed_when`语句，Ansible将永远返回`changed`。大部分模块都能正确返回运行结果是否对目标主机产生影响，我们依然可以使用`changed_when`语句来对返回信息进行重写，根据任务返回结果来判定任务的运行结果是否真正符合我们预期。可以参考[changed_when与failed_when条件判断](./changed_when.md) 。
- 在剧本文件中可以给任务设置不同的标签，`tags`可以定义任务的标签。可以参考[Tags标签](./tags.md) 。
- 在任务执行完成后，可以触发指定的任务，这个时候就可以使用handlers触发器，可以参考[handlers触发器](./handlers.md) 。
- 可以使用ansible-vault保护敏感数据，可以参考[ansible-vault数据加密](./ansible-vault.md) 。
- 如果要对数据进行某些过滤处理，可以使用过滤器`filter`来完成，详细可参考 [过滤器](./filter.md) 。
- 自定义fact事实变量，可参考 [setup事实变量模块](./setup.md)。
- 编写facts模块，可参考 [编写facts模块](./facts_module.md)。
- 在剧本执行失败时，如果你想Ansible给你发邮件，可以参考[callback回调插件](./callback.md) 。
- 从外部数据拉取信息存放到变量中，可以使用lookups插件，可参考 [lookups插件](./lookups.md)。
- Ansible角色，可参考以下Role角色系列教程：
  -  [ansible role角色(1)](./role.md)，role角色概述与相关功能概述。使用Ansible Galaxy https://galaxy.ansible.com/ui/ 分享你的角色等。
  -  [ansible role角色(2)--创建第一个role角色](./role_2.md)，创建第一个测试role角色。
  -  [ansible role角色(3)--一步一步学role角色](./role_3.md)，base基础角色配置。
  -  [ansible role角色(4)--include的使用](./role_4_include.md)，base基础角色配置优化，拆分任务功能，引入include关键字。
  -  [ansible role角色(5)--使用ansible配置supervisor进程管理角色](./role_5_supervisor.md)，使用miniconda配置Python环境，对应Python版本为 3.10.13，并设置supervisor进程管理工具环境。

Ansible内置模块：

> Modules
> 1.    add_host module – Add a host (and alternatively a group) to the ansible-playbook in-memory inventory
> 1.    apt module – Manages apt-packages
> 1.    apt_key module – Add or remove an apt key
> 1.    apt_repository module – Add and remove APT repositories
> 1.    assemble module – Assemble configuration files from fragments
> 1.    assert module – Asserts given expressions are true
> 1.    async_status module – Obtain status of asynchronous task
> 1.    blockinfile module – Insert/update/remove a text block surrounded by marker lines
> 1.    command module – Execute commands on targets
> 1.    copy module – Copy files to remote locations
> 1.    cron module – Manage cron.d and crontab entries
> 1.    debconf module – Configure a .deb package
> 1.    debug module – Print statements during execution
> 1.    dnf module – Manages packages with the dnf package manager
> 1.    dpkg_selections module – Dpkg package selection selections
> 1.    expect module – Executes a command and responds to prompts
> 1.    fail module – Fail with custom message
> 1.    fetch module – Fetch files from remote nodes
> 1.    file module – Manage files and file properties
> 1.    find module – Return a list of files based on specific criteria
> 1.    gather_facts module – Gathers facts about remote hosts
> 1.    get_url module – Downloads files from HTTP, HTTPS, or FTP to node
> 1.    getent module – A wrapper to the unix getent utility
> 1.    git module – Deploy software (or files) from git checkouts
> 1.    group module – Add or remove groups
> 1.    group_by module – Create Ansible groups based on facts
> 1.    hostname module – Manage hostname
> 1.    import_playbook module – Import a playbook
> 1.    import_role module – Import a role into a play
> 1.    import_tasks module – Import a task list
> 1.    include module – Include a task list
> 1.    include_role module – Load and execute a role
> 1.    include_tasks module – Dynamically include a task list
> 1.    include_vars module – Load variables from files, dynamically within a task
> 1.    iptables module – Modify iptables rules
> 1.    known_hosts module – Add or remove a host from the known_hosts file
> 1.    lineinfile module – Manage lines in text files
> 1.    meta module – Execute Ansible ‘actions’
> 1.    package module – Generic OS package manager
> 1.    package_facts module – Package information as facts
> 1.    pause module – Pause playbook execution
> 1.    ping module – Try to connect to host, verify a usable python and return pong on success
> 1.    pip module – Manages Python library dependencies
> 1.    raw module – Executes a low-down and dirty command
> 1.    reboot module – Reboot a machine
> 1.    replace module – Replace all instances of a particular string in a file using a back-referenced regular expression
> 1.    rpm_key module – Adds or removes a gpg key from the rpm db
> 1.    script module – Runs a local script on a remote node after transferring it
> 1.    service module – Manage services
> 1.    service_facts module – Return service state information as fact data
> 1.    set_fact module – Set host variable(s) and fact(s).
> 1.    set_stats module – Define and display stats for the current ansible run
> 1.    setup module – Gathers facts about remote hosts
> 1.    shell module – Execute shell commands on targets
> 1.    slurp module – Slurps a file from remote nodes
> 1.    stat module – Retrieve file or file system status
> 1.    subversion module – Deploys a subversion repository
> 1.    systemd module – Manage systemd units
> 1.    systemd_service module – Manage systemd units
> 1.    sysvinit module – Manage SysV services.
> 1.    tempfile module – Creates temporary files and directories
> 1.    template module – Template a file out to a target host
> 1.    unarchive module – Unpacks an archive after (optionally) copying it from the local machine
> 1.    uri module – Interacts with webservices
> 1.    user module – Manage user accounts
> 1.    validate_argument_spec module – Validate role argument specs.
> 1.    wait_for module – Waits for a condition before continuing
> 1.    wait_for_connection module – Waits until remote system is reachable/usable
> 1.    yum module – Manages packages with the yum package manager
> 1.    yum_repository module – Add or remove YUM repositories


1. [Ansible初体验-Ansible的基本使用](./base.md)
2. [Ping连接测试模块](./ping.md)
3. [Debug调试模块](./debug.md)
4. [Command命令模块](./command.md)
5. [Shell执行远程脚本模块](./shell.md)
6. [Cron定时任务模块](./cron.md)
7. [User用户模块](./user.md)
8. [Group用户组模块](./group.md)
9. [Copy复制模块](./copy.md)
10. [File文件模块](./file.md)
11. [Yum包模块](./yum.md)
12. [Service服务模块](./service.md)
13. [Script执行本地脚本模块-不推荐](./script.md)
14. [Setup事实变量模块](./setup.md)
15. [Fetch从远程复制文件模块](./fetch.md)
16. [Find查找模块](./find.md)
17. [Firewalld防火墙模块](./firewalld.md)
18. [get_url下载文件到远程节点模块](./get_url.md)
19. [git远程仓库检出模块](./git.md)
20. [git_config git配置模块](./git_config.md)
21. [hostname修改主机名模块](./hostname.md)
22. [htpasswd用户认证模块](./htpasswd.md)
23. [jenkins_job Jenkins任务管理模块](./jenkins_job.md)
24. [jenkins_job_info Jenkins任务信息模块](./jenkins_job_info.md)
25. [ldap_attrs LDAP属性模块](./ldap_attr.md)
26. [lineinfile文件内容修改模块](./lineinfile.md)
27. [blockinfile文件块模块](./blockinfile.md)
28. [mail邮件模块](./mail.md)
29. [make编译模块](./make.md)
30. [pip python库管理模块](./pip.md)
31. [tempfile临时文件模块](./tempfile.md)
32. [template模板模块](./template.md)
33. [timezone时区模块](./timezone.md)
34. [wait_for条件等待模块](./wait_for.md)
35. [wait_for_connection等待远程主机连接模块](./wait_for_connection.md)
36. [unarchive解压模块](./unarchive.md)
37. [ansible when条件判断](./when.md)
38. [changed_when与failed_when条件判断](./changed_when.md)
39. [ansible循环](./loop.md)
40. [ansible-vault数据加密](./ansible-vault.md)
41. [ansible handlers触发器](./handlers.md)
42. [ansible tags标签](./tags.md)
43. [ansible fiter过滤器](./filter.md)
44. [lookups插件](./lookups.md)
45. [编写facts模块](./facts_module.md)
46. [ansible role角色(1)--role角色概述与相关功能概述 ](./role.md)
47. [ansible role角色(2)--创建第一个role角色](./role_2.md)
48. [ansible role角色(3)--一步一步学role角色](./role_3.md)
49. [ansible role角色(4)--include的使用](./role_4_include.md)
50. [优化Ansible速度](./accelerate.md)
51. [ansible role角色(5)--使用ansible配置supervisor进程管理角色](./role_5_supervisor.md)


你也可以直接看大佬的博客：

朱双印大佬的ansible轻松入门系列：

1. [ansible笔记（1）：ansible的基本概念](https://www.zsythink.net/archives/2481)
2. [ansible笔记（2）：清单配置详解](https://www.zsythink.net/archives/2509)
3. [ansible笔记（3）：ansible模块的基本使用](https://www.zsythink.net/archives/2523)
4. [ansible笔记（4）：常用模块之文件操作](https://www.zsythink.net/archives/2542)
5. [ansible笔记（5）：常用模块之文件操作（二）](https://www.zsythink.net/archives/2560)
6. [ansible笔记（6）：常用模块之命令类模块](https://www.zsythink.net/archives/2557)
7. [ansible笔记（7）：常用模块之系统类模块](https://www.zsythink.net/archives/2572)
8. [ansible笔记（8）：常用模块之系统类模块（二）](https://www.zsythink.net/archives/2580)
9. [ansible笔记（9）：常用模块之包管理模块](https://www.zsythink.net/archives/2592)
10. [ansible笔记（10）：初识ansible playbook](https://www.zsythink.net/archives/2602)
11. [ansible笔记（11）：初识ansible playbook（二）](https://www.zsythink.net/archives/2613)
12. [ansible笔记（12）：handlers的用法](https://www.zsythink.net/archives/2624)
13. [ansible笔记（13）：tags的用法](https://www.zsythink.net/archives/2641)
14. [ansible笔记（14）：变量（一）](https://www.zsythink.net/archives/2655)
15. [ansible笔记（15）：变量（二）](https://www.zsythink.net/archives/2671)
16. [ansible笔记（16）：变量（三）](https://www.zsythink.net/archives/2680)
17. [ansible笔记（17）：变量（四）](https://www.zsythink.net/archives/2698)
18. [ansible笔记（18）：变量（五）](https://www.zsythink.net/archives/2715)
19. [ansible笔记（19）：循环（一）](https://www.zsythink.net/archives/2728)
20. [ansible笔记（20）：循环（二）](https://www.zsythink.net/archives/2776)
21. [ansible笔记（21）：循环（三）](https://www.zsythink.net/archives/2781)
22. [ansible笔记（22）：循环（四）](https://www.zsythink.net/archives/2787)
23. [ansible笔记（23）：循环（五）](https://www.zsythink.net/archives/2790)
24. [ansible笔记（24）：循环（六）](https://www.zsythink.net/archives/2797)
25. [ansible笔记（25）：循环（七）](https://www.zsythink.net/archives/2804)
26. [ansible笔记（26）：条件判断](https://www.zsythink.net/archives/2810)
27. [ansible笔记（27）：条件判断与tests](https://www.zsythink.net/archives/2817)
28. [ansible笔记（28）：条件判断与block](https://www.zsythink.net/archives/2836)
29. [ansible笔记（29）：条件判断与错误处理](https://www.zsythink.net/archives/2846)
30. [ansible笔记（30）：过滤器（一）](https://www.zsythink.net/archives/2862)
31. [ansible笔记（31）：变量（六）](https://www.zsythink.net/archives/2871)
32. [ansible笔记（32）：过滤器（二）](https://www.zsythink.net/archives/2874)
33. [ansible笔记（33）：过滤器（三）](https://www.zsythink.net/archives/2885)
34. [ansible笔记（34）：lookup插件](https://www.zsythink.net/archives/2893)
35. [ansible笔记（35）：循环（八）](https://www.zsythink.net/archives/2900)
36. [ansible笔记（36）：include](https://www.zsythink.net/archives/2962)
37. [ansible笔记（37）：include（二）](https://www.zsythink.net/archives/2977)
38. [ansible笔记（38）：jinja2模板（一）](https://www.zsythink.net/archives/2999)
39. [ansible笔记（39）：jinja2模板（二）](https://www.zsythink.net/archives/3021)
40. [ansible笔记（40）：jinja2模板（三）](https://www.zsythink.net/archives/3037)
41. [ansible笔记（41）：jinja2模板（四）](https://www.zsythink.net/archives/3051)
42. [ansible笔记（42）：角色](https://www.zsythink.net/archives/3063)
43. [ansible笔记（43）：使用ansible-vault加密数据](https://www.zsythink.net/archives/3250)
44. [ansible笔记（44）：变量（七）](https://www.zsythink.net/archives/3270)
45. [ansible笔记（45）：常用技巧（一）](https://www.zsythink.net/archives/3277)
46. [ansible笔记（46）：常用技巧（二）](https://www.zsythink.net/archives/3282)


也可以看看马龙帅（网名"骏马金龙"）大佬的系列文章： [一步到位玩透 Ansible](https://www.junmajinlong.com/ansible/index/)