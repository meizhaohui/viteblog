# callback回调插件

[[toc]]



## 1. 概述

- callback是Ansible的一个回调功能，我们可以在运行Ansible的时候调用这个功能。
- 比如希望在执行playbook失败后发送邮件，或者希望每次执行playbook的结果存到日志或者数据库中。
- 在callback插件里面，我们可以很方便地拿到Ansible执行状态信息。然后可以定义一个callback动作，在playbook的某个运行状态下进行调用。
- callback回调插件官方示例 [https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#callback-plugins](https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#callback-plugins) 。
- 官方文档 Callback plugins [https://docs.ansible.com/ansible/latest/plugins/callback.html#callback-plugins](https://docs.ansible.com/ansible/latest/plugins/callback.html#callback-plugins)
- log_plays – write playbook output to log file [https://docs.ansible.com/ansible/2.9/plugins/callback/log_plays.html#log-plays-write-playbook-output-to-log-file](https://docs.ansible.com/ansible/2.9/plugins/callback/log_plays.html#log-plays-write-playbook-output-to-log-file)
- mail – Sends failure events via email [https://docs.ansible.com/ansible/2.9/plugins/callback/mail.html#mail-callback](https://docs.ansible.com/ansible/2.9/plugins/callback/mail.html#mail-callback)



