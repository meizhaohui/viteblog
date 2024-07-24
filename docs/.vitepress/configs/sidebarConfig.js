// 侧边栏
module.exports = {
  '/OS/': [
    {
      text: 'CentOS',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: '学会使用命令帮助', link: '/OS/Centos/X_use_help' },
        { text: 'VIM编辑器的使用', link: '/OS/Centos/X_how_to_use_vim' },
        { text: 'Bash script中的通配符与正则表达式', link: '/OS/Centos/X_wildcard_regular_expression_in_bash_script' },
        { text: 'linux下安装htop', link: '/OS/Centos/X_how_to_install_htop_in_linux' },
        { text: 'echo输出带颜色的字体', link: '/OS/Centos/X_echo_color_font' },
        { text: '防止rm -rf /误删除的方法', link: '/OS/Centos/X_forbit_use_rm_to_delete_root_path' },
        { text: '终端快捷键的使用', link: '/OS/Centos/X_hotkey_in_terminal' },
        { text: 'CentOS 7 搭建CA认证中心实现https认证', link: '/OS/Centos/certificate_authority_for_https' },
        { text: 'CentOS 7增加系统安全性', link: '/OS/Centos/X_enhance_centos_secure' },
        { text: '在VirtualBox中安装CentOS7虚拟机系统', link: '/OS/Centos/X_virtualbox_install_centos7' },
        { text: 'VirtualBox虚拟机磁盘空间扩容', link: '/OS/Centos/X_VirtualBox_enhance_hdds' },
        { text: 'JSON解析工具-jq', link: '/OS/Centos/json_tool_jq' },
        { text: '创建随机密码', link: '/OS/Centos/create_password' },
        { text: 'Linux操作系统的启动过程', link: '/OS/Centos/linux_boot' },
        { text: 'rsync+inotify实现数据实时同步', link: '/OS/Centos/rsync' },
        { text: 'NTP时间同步', link: '/OS/Centos/ntpdate' },
        { text: 'virtualbox命令行工具VBoxManage的使用', link: '/OS/Centos/virtualbox_command' },
        { text: 'CentOS 7搭建NFS服务器', link: '/OS/Centos/nfs_server' },
        { text: 'ssh-keygen创建公钥私钥对', link: '/OS/Centos/ssh-keygen' },
      ]
    },
    {
      text: 'Ubuntu',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Ubuntu桌面初始化安装配置', link: '/OS/Ubuntu/ubuntu_init' },
        { text: '更改ubuntu国内镜像源', link: '/OS/Ubuntu/ubuntu_change_repo' },
        { text: 'Ubuntu防火墙设置', link: '/OS/Ubuntu/ubuntu_firewall' }
      ]
    },
    {
      text: 'Windows',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'windows批处理的使用', link: '/OS/Windows/cmd' }
      ]
    },
    {
      text: 'RockyLinux',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'RockyLinux docs', link: '/OS/RockyLinux/' }
      ]
    },
    {
      text: 'MacOS',
      link: '/OS/MacOS/'
    },
    {
      text: 'Cobbler自动化系统',
      link: '/OS/Cobbler/'
    }
  ],
  '/frontend/': [
    {
      text: 'Vue',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'vue的基本使用', link: '/frontend/vue/vue_basic_use' },
        { text: '模板语法', link: '/frontend/vue/syntax' },
        { text: '计算属性与侦听器', link: '/frontend/vue/computed_watch' },
        { text: 'Vue-Multiselect下拉框强化插件的使用', link: '/frontend/vue/use_Vue-Multiselect' },
        { text: '动态绑定class或style样式', link: '/frontend/vue/class_style' },
        { text: 'v-if与v-show条件渲染', link: '/frontend/vue/v-if_v_show' },
        { text: 'v-for循环列表', link: '/frontend/vue/v-for' },
        { text: '事件处理', link: '/frontend/vue/events' },
        { text: '表单输入绑定', link: '/frontend/vue/forms' },
        { text: '组件基础', link: '/frontend/vue/components' }
      ]
    },
    {
      text: 'JavaScript',
      link: '/frontend/js/'
    },
  ],
  


  '/backend/': [
    {
      text: 'Python',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: "Python介绍", link: "/backend/python/X_introduction_python" },
        { text: "Python的安装", link: "/backend/python/X_install_python" },
        { text: "学会使用命令帮助", link: "/backend/python/X_use_help" },
        { text: "引号与转义符的使用", link: "/backend/python/X_quote_escape_character" },
        { text: "变量标识符的命名规则", link: "/backend/python/X_var_name_rule" },
        { text: "Python运算符", link: "/backend/python/X_operational_character" },
        { text: "内建数据组构", link: "/backend/python/X_built-in_data_structure" },
        { text: "Python的控制流", link: "/backend/python/X_control_workflow" },
        { text: "函数", link: "/backend/python/X_function" },
        { text: "装饰器", link: "/backend/python/X_decorator" },
        { text: "异常", link: "/backend/python/X_try_except_else_finally" },
        { text: "模块-sys模块", link: "/backend/python/X_system_module" },
        { text: "模块-os模块", link: "/backend/python/X_os_module" },
        { text: "python字符串处理", link: "/backend/python/X_str" },
        { text: "模块-itertools模块迭代器函数", link: "/backend/python/X_itertools_module" },
        { text: "文件的读写", link: "/backend/python/X_file_read_write" },
        { text: "常用内建模块Collections模块的使用", link: "/backend/python/X_collections_module" },
        { text: "常用内建模块之正则表达式re模块", link: "/backend/python/X_re_module" },
        { text: "面向对象编程", link: "/backend/python/X_object_oriented_programming" },
        { text: "模块-json模块", link: "/backend/python/X_json_module" },
        { text: "数据库处理", link: "/backend/python/X_database" },
        { text: "模块-UUID模块", link: "/backend/python/X_univeral_unique_identifier" },
        { text: "使用Faker生成虚拟数据", link: "/backend/python/X_faker_generate_fake_data" },
        { text: "Pipenv虚拟环境的使用", link: "/backend/python/X_pipenv" },
        { text: "Selenium安装与使用", link: "/backend/python/X_selenium_install_and_use" },
        { text: "ReviewBoard国际化配置", link: "/backend/python/X_reviewboard_i18n" },
        { text: "剖析Python Web", link: "/backend/python/X_web" },
        { text: "glob模块", link: "/backend/python/X_glob_module" },
        { text: "程序和进程", link: "/backend/python/X_Programs_and_Processes" },
        { text: "模块-日期和时间模块之calendar日历模块", link: "/backend/python/X_time_and_date_module_calendar" },
        { text: "模块-日期和时间模块之time时间模块", link: "/backend/python/X_time_and_date_module_time" },
        { text: "模块-日期和时间模块之datetime日期时间模块", link: "/backend/python/X_time_and_date_module_datetime" },
        { text: "模块-日期和时间模块之dateutil日期工具模块", link: "/backend/python/X_time_and_date_module_dateutil" },
        { text: "模块-日期和时间模块之pytz时区模块", link: "/backend/python/X_time_and_date_module_pytz" },
        { text: "模块-日期和时间模块之fleming时区模块(不推荐学习该模块)", link: "/backend/python/X_time_and_date_module_fleming" },
        { text: "模块-日期和时间模块之arrow日期时间模块", link: "/backend/python/X_time_and_date_module_arrow" },
        { text: "模块-日期和时间模块之timeit计算程序运行时间模块", link: "/backend/python/X_time_and_date_module_timeit" },
        { text: "Python并发", link: "/backend/python/X_python_concurrency" },
        { text: "网络", link: "/backend/python/X_internet" },
        { text: "模块-数据输出美化模块pprint", link: "/backend/python/X_pprint" },
        { text: "模块-表格美化输出模块prettytable", link: "/backend/python/prettytable" },
        { text: "成为真正的Python开发者", link: "/backend/python/X_tobepythonista" },
        { text: "logging模块-记录错误日志", link: "/backend/python/X_logging" },
        { text: "Python代码检查", link: "/backend/python/X_Python_style_and_static_check" },
        { text: "模块-Python代码格式化工具black", link: "/backend/python/black" },
        { text: "Python面试总结", link: "/backend/python/X_python_interview" },
        { text: "Python Cookbook小菜一碟", link: "/backend/python/X_python_cookbook" },
        { text: "查看Python第三方包的json信息", link: "/backend/python/check_python_package_json_info" },
        { text: "搭建简易的HTTP服务", link: "/backend/python/fast_web" },
        { text: "读取yaml配置文件", link: "/backend/python/yaml" },
        { text: "python批量telnet检测IP地址的端口是否开放", link: "/backend/python/mytelnet" },
        { text: "自动启动代理程序", link: "/backend/python/auto_start_proxy" },
        { text: "miniconda的使用", link: "/backend/python/miniconda" },
      ]
    },
    {
      text: 'Flask',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: '接口认证管理之Flask_HTTPAuth', link: '/backend/Flask/flask_httpauth' },
      ]
    },
    {
      text: 'Java',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Java开发环境配置', link: '/backend/Java/basic' },
        { text: 'Maven打包', link: '/backend/Java/maven' },
      ]
    },
    {
      text: 'Golang',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Golang的基本使用', link: '/backend/golang/base' },
        { text: 'GO语言之旅', link: '/backend/golang/go-tour' },
      ]
    },
    {
      text: 'PHP',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'PHP docs', link: '/backend/php/' },
      ]
    },
    {
      text: 'C语言',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'C程序设计语言总结', link: '/backend/C/the_c_programming_language_second_edition' },
        { text: '换个姿势学C语言', link: '/backend/C/newstylec' },
      ]
    },
  ],
  '/database/': [
    {
      text: 'MySQL',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'CentOS7安装mysql', link: '/database/mysql/X_00_install_mysql' },
        { text: 'mysql数据库的创建、删除与使用', link: '/database/mysql/X_01_insert_select_update_delete' },
        { text: 'mysql数据库求字段的总和、总数与均值', link: '/database/mysql/X_02_sum_count_avg' },
        { text: 'mysql数据库求字段的最大值和最小值', link: '/database/mysql/X_03_greatest_least' },
        { text: 'mysql Index column size too large', link: '/database/mysql/X_04_Index_column_size_too_large_The_maximum_column_size_is_767_bytes' },
        { text: 'MongoDB docs', link: '/database/mongodb/' },
        { text: 'Oracle docs', link: '/database/oracle/' },
        { text: 'Redis docs', link: '/database/redis/' },
      ]
    },
    {
      text: 'MongoDB',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'MongoDB docs', link: '/database/mongodb/' },
      ]
    },
    {
      text: 'Oracle',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Oracle docs', link: '/database/oracle/' },
      ]
    },
    {
      text: 'Redis',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Redis6安装与主从配置', link: '/database/redis/install_redis' },
        { text: 'CentOS7源码安装Redis6.2.14', link: '/database/redis/install_redis_with_source' },
      ]
    },
  ],
  '/monitor/': [
    {
      text: 'Supervisor',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: '进程管理工具之Supervisor', link: '/monitor/supervisor/' },
      ]
    },
    {
      text: 'Zabbix',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'zabbix日志监控Permission denied权限异常处理', link: '/monitor/zabbix/Permission_denied' },
      ]
    },
  ],
  '/CM/': [
    {
      text: 'Git',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Git的安装', link: '/CM/git/install_git' },
        { text: 'Git的基本使用', link: '/CM/git/basic_use' },
        { text: 'Git异常处理', link: '/CM/git/git_exceptions' },
        { text: 'Git版本控制管理', link: '/CM/git/version_control_with_git' },
        { text: 'CentOS7用git-daemon搭建Git服务器', link: '/CM/git/create_git_server' },
        { text: 'SSH隧道连接实现Git推送', link: '/CM/git/use_ssh_git_push' },
        { text: 'Git hooks钩子脚本的使用', link: '/CM/git/git_hooks' },
        { text: 'Git status时中文文件名乱码', link: '/CM/git/git_chinese_filename' },
        { text: 'Git commit提交模板', link: '/CM/git/git_commit_template' },
        { text: '什么是Signed-off-by', link: '/CM/git/Signed-off-by' },
        { text: 'Git多个远程仓库不同步时的补救办法', link: '/CM/git/reset_diff_repos' },
        { text: '使git status不显示某些文件', link: '/CM/git/ignore_changed_files' },
      ]
    },
    {
      text: 'SVN',
      collapsed: false, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'SVN的基本使用', link: '/CM/svn/' },
      ]
    },
    {
      text: 'Ansible',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Ansible学习笔记', link: '/CM/ansible/' },
        { text: 'Ansible初体验', link: '/CM/ansible/base' },
        { text: 'Ping连接测试模块', link: '/CM/ansible/ping' },
        { text: 'Debug调试模块', link: '/CM/ansible/debug' },
        { text: 'Command命令模块', link: '/CM/ansible/command' },
        { text: 'Shell执行远程脚本模块', link: '/CM/ansible/shell' },
        { text: 'Cron定时任务模块', link: '/CM/ansible/cron' },
        { text: 'User用户模块', link: '/CM/ansible/user' },
        { text: 'Group用户组模块', link: '/CM/ansible/group' },
        { text: 'Copy复制模块', link: '/CM/ansible/copy' },
        { text: 'File文件模块', link: '/CM/ansible/file' },
        { text: 'Yum包模块', link: '/CM/ansible/yum' },
        { text: 'Service服务模块', link: '/CM/ansible/service' },
        { text: 'Script执行本地脚本模块-不推荐', link: '/CM/ansible/script' },
        { text: 'Setup事实变量模块', link: '/CM/ansible/setup' },
        { text: 'Fetch从远程复制文件模块', link: '/CM/ansible/fetch' },
        { text: 'Find查找模块', link: '/CM/ansible/find' },
        { text: 'Firewalld防火墙模块', link: '/CM/ansible/firewalld' },
        { text: 'get_url下载文件到远程节点模块', link: '/CM/ansible/get_url' },
        { text: 'git远程仓库检出模块', link: '/CM/ansible/git' },
        { text: 'git_config git配置模块', link: '/CM/ansible/git_config' },
        { text: 'hostname修改主机名模块', link: '/CM/ansible/hostname' },
        { text: 'htpasswd用户认证模块', link: '/CM/ansible/htpasswd' },
        { text: 'jenkins_job Jenkins任务管理模块', link: '/CM/ansible/jenkins_job' },
        { text: 'jenkins_job_info Jenkins任务信息模块', link: '/CM/ansible/jenkins_job_info' },
        { text: 'ldap_attrs LDAP属性模块', link: '/CM/ansible/ldap_attr' },
        { text: 'lineinfile文件内容修改模块', link: '/CM/ansible/lineinfile' },
        { text: 'blockinfile文件块模块', link: '/CM/ansible/blockinfile' },
        { text: 'mail邮件模块', link: '/CM/ansible/mail' },
        { text: 'make编译模块', link: '/CM/ansible/make' },
        { text: 'pip python库管理模块', link: '/CM/ansible/pip' },
        { text: 'tempfile临时文件模块', link: '/CM/ansible/tempfile' },
        { text: 'template模板模块', link: '/CM/ansible/template' },
        { text: 'timezone时区模块', link: '/CM/ansible/timezone' },
        { text: 'wait_for条件等待模块', link: '/CM/ansible/wait_for' },
        { text: 'wait_for_connection等待远程主机连接模块', link: '/CM/ansible/wait_for_connection' },
        { text: 'unarchive解压模块', link: '/CM/ansible/unarchive' },
        { text: 'ansible when条件判断', link: '/CM/ansible/when' },
        { text: 'changed_when与failed_when条件判断', link: '/CM/ansible/changed_when' },
        { text: 'ansible循环', link: '/CM/ansible/loop' },
        { text: 'ansible-vault数据加密', link: '/CM/ansible/ansible-vault' },
        { text: 'ansible handlers触发器', link: '/CM/ansible/handlers' },
        { text: 'ansible tags标签', link: '/CM/ansible/tags' },
        { text: 'ansible fiter过滤器', link: '/CM/ansible/filter' },
        { text: 'lookups插件', link: '/CM/ansible/lookups' },
        { text: '编写facts模块', link: '/CM/ansible/facts_module' },
        { text: 'callback回调插件', link: '/CM/ansible/callback' },
        { text: 'ansible role角色(1)--role角色概述与相关功能概述 ', link: '/CM/ansible/role' },
        { text: 'ansible role角色(2)--创建第一个role角色', link: '/CM/ansible/role_2' },
        { text: 'ansible role角色(3)--一步一步学role角色', link: '/CM/ansible/role_3' },
        { text: 'ansible role角色(4)--include的使用', link: '/CM/ansible/role_4_include' },
        { text: '优化Ansible速度', link: '/CM/ansible/accelerate' },
        { text: 'ansible role角色(5)--supervisor进程管理角色', link: '/CM/ansible/role_5_supervisor' },
        { text: 'ansible role角色(6)--redis数据库角色', link: '/CM/ansible/role_6_redis' },
      ]
    },
    {
      text: 'Proxmox',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Proxmox Virtual Environment', link: '/CM/proxmox/' },
        { text: 'Proxmox VE介绍', link: '/CM/proxmox/X1_Introduction' },
        { text: 'Proxmox VE安装', link: '/CM/proxmox/X2_InstallingProxmoxVE' },
      ]
    },
  ],
  '/CI/': [
    {
      text: 'Jenkins',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'Jenkins安装与基本配置', link: '/CI/jenkins/install' },
        { text: 'Jenkins插件推荐', link: '/CI/jenkins/plugins' },
      ]
    },
    {
      text: 'Docker',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'docker的基本使用', link: '/CI/docker/docker_basic_use' },
        { text: '使用docker搭建nextcloud私有云盘', link: '/CI/docker/nextcloud_in_docker' },
        { text: 'docker配置redis缓存', link: '/CI/docker/redis_in_docker' },
        { text: 'docker配置PostgreSQL数据库', link: '/CI/docker/postgresql_in_docker' },
        { text: '轻量级Gogs安装与配置', link: '/CI/docker/gogs_in_docker' },
        { text: 'bridge-nf-call-iptables is disabled', link: '/CI/docker/WARNING-bridge-nf-call-iptables_is_disabled' },
        { text: '使用clair扫描Docker镜像漏洞', link: '/CI/docker/clair' },
        { text: '修改默认数据存储目录', link: '/CI/docker/change_root_dir' },
        { text: '查看下载的docker镜像的版本信息', link: '/CI/docker/the_latest_image' },
        { text: 'docker容器增加端口映射', link: '/CI/docker/add_port_to_container' },
        { text: '通过进程pid查询对应docker容器信息', link: '/CI/docker/get_container_by_pid' },
        { text: 'docker-compose的使用', link: '/CI/docker/docker-compose' },
        { text: '', link: '/CI/docker/' },
      ]
    },
    {
      text: 'nexus私有仓库',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: '搭建自己的nexus私有仓库1-nexus初体验', link: '/CI/docker/create_your_nexus' },
        { text: '搭建自己的nexus私有仓库2-创建python pypi代理', link: '/CI/docker/create_your_nexus_2' },
        { text: '搭建自己的nexus私有仓库3-创建yum ius代理', link: '/CI/docker/create_your_nexus_3' },
        { text: '搭建自己的nexus私有仓库4-创建docker私有仓库', link: '/CI/docker/create_your_nexus_4_docker_proxy' },
        { text: '搭建自己的nexus私有仓库5-测试docker仓库pull和push', link: '/CI/docker/create_your_nexus_5_test_docker_proxy' },
        { text: '搭建自己的nexus私有仓库6-使用Nginx反向代理', link: '/CI/docker/create_your_nexus_6_nginx_proxy' },
        { text: '搭建自己的nexus私有仓库7-修改nexus容器时区', link: '/CI/docker/create_your_nexus_7_change_timezone' },
        { text: '搭建自己的nexus私有仓库8-Nexus3的数据库结构', link: '/CI/docker/create_your_nexus_8_nexus_database' },
        { text: '搭建自己的nexus私有仓库9-Nexus API接口的使用1', link: '/CI/docker/create_your_nexus_9_nexus_api' },
        { text: '搭建自己的nexus私有仓库10-Nexus API接口的使用2', link: '/CI/docker/create_your_nexus_10_nexus_api_2' },
        { text: '搭建自己的nexus私有仓库11-Nexus API接口的使用3', link: '/CI/docker/create_your_nexus_11_nexus_api_3_code_optimization' },
        { text: '搭建自己的nexus私有仓库12-Nexus权限配置', link: '/CI/docker/create_your_nexus_12_user_permission' },
      ]
    },
    {
      text: 'k8s',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'k8s集群部署', link: '/CI/k8s/deploy' },
        { text: '获取k8s集群组件状态kubectl get cs', link: '/CI/k8s/k8s_get_cs' },
        { text: '获取k8s集群节点状态kubectl get nodes', link: '/CI/k8s/k8s_get_nodes' },
        { text: '获取k8s集群信息kubectl cluster-info', link: '/CI/k8s/k8s_cluster_info' },
      ]
    },
    {
      text: 'GitLab',
      collapsed: true, // 是否可折叠，默认可折叠true 
      items: [
        { text: 'CenOS7安装GitLab(使用外部Nginx配置)', link: '/CI/gitlab/X_centos7_install_gitlab_with_external_nginx' },
        { text: 'GitLab的汉化与CI持续集成gitlab-runner的配置', link: '/CI/gitlab/X_configure_gitlab_i18n_and_create_gitlab_ci_with_gitlab_runner' },
        { text: 'GitLab CI流水线配置文件.gitlab-ci.yml详解', link: '/CI/gitlab/X_gitlab_ci_.gitlab-ci.yml_detail' },
        { text: 'CenOS7安装GitLab(使用外部Nginx配置)并配置HTTPS协议', link: '/CI/gitlab/X_centos7_install_gitlab_with_external_nginx_and_https' },
      ]
    },
  ],
}




 