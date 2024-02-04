# 搭建自己的nexus私有仓库2--创建python pypi代理

[[toc]]

本文档是nexus系列课程第2篇。
- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)

本文计划做以下事情：

- 使用nexus创建python pypi代理仓库。


以下是实验环境：


| 主机 | IP            | 主机名 | 操作系统        | docker版本 | 自定义域名   |
|------|---------------|--------|:----------------|:-----------|:-------------|
| 1    | 192.168.56.11 | nexus  | CentOS 7.6.1810 | 20.10.5    | nexushub.com |
| 2    | 192.168.56.12 | master | CentOS 7.6.1810 | 20.10.5    |              |


## 0. 准备工作

请在主机2以及你的电脑上面配置域名解析：

```sh
[root@master ~]# tail -n 1 /etc/hosts
192.168.56.11 nexushub.com
```

注意，实际操作时，请将`192.168.56.11`替换成你服务器的内网IP或者公网IP，`nexushub.com`替换成你想使用的域名。

查看清华大学开源镜像站pypi的帮助信息： [PyPI 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)

> PyPI 镜像使用帮助
>
> PyPI 镜像在每次同步成功后间隔 5 分钟同步一次。
> pip
> 临时使用
> ```sh
> pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
> ```
> 注意，simple 不能少, 是 https 而不是 http
> 设为默认
> 
> 升级 pip 到最新的版本 (>=10.0.0) 后进行配置：
> ```sh
> python -m pip install --upgrade pip
> pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
> ```
> 如果您到 pip 默认源的网络连接较差，临时使用本镜像站来升级 pip：
> 
> ```sh
> python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
> ```

URL链接 `https://pypi.tuna.tsinghua.edu.cn/simple`就是我们需要使用的代理地址。


## 1. nexus创建pypi代理仓库

上一节中，我们知道通过点击页面顶部的齿轮设置图标：

![](/img/Snipaste_2023-08-22_22-33-54.png)
进入到设置页面后，点击左侧的【Repositories】进入到仓库管理页面，点击【Create Repository】按钮，然后选择【pypi (proxy)】：

![](/img/Snipaste_2023-09-12_22-33-48.png)
- Name: 仓库名，需要唯一，不能与其他已经仓库的仓库重名，最好能通过名称知道仓库的意义。如我们pypi代理仓库，我们直接命名为pypi-proxy。
- Remote storage: 远程存储仓库的URL地址，如我们直接代理清华大学的python pypi源，其地址是 [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple), **但在配置远程地址时，需要将大部分国内源带的simple目录去掉，然后在访问时再将这个simple加上，因此我们填写 https://pypi.tuna.tsinghua.edu.cn 。**
- HTTP request setting，HTTP请求设置，我们一般只需要设置一下User-Agent请求头即可，如填写"Sync pypi repo. email: mzh.whut@gmail.com"。

配置完成后，保存。

保存后，点击新创建的`pypi-proxy`仓库，可以看到仓库详情：
![](/img/Snipaste_2023-09-12_22-55-32.png)
这里的URL [http://nexushub.com:8081/repository/pypi-proxy/](http://nexushub.com:8081/repository/pypi-proxy/) 就是我们代理仓库的地址。

客户端配置时，应使用 [http://nexushub.com:8081/repository/pypi-proxy/simple](http://nexushub.com:8081/repository/pypi-proxy/simple) 这个地址。

## 2. 客户端配置

直接将以下内容写入pip的配置文件`~/.pip/pip.conf`中：

```ini
[global]
index-url = http://nexushub.com:8081/repository/pypi-proxy/simple
trusted-host = nexushub.com
```

查看pip配置信息：

```sh
[root@master ~]# pip config list
global.index-url='http://nexushub.com:8081/repository/pypi-proxy/simple'
global.trusted-host='nexushub.com'
[root@master ~]#
```

安装python第三方包，如Flask，可参考 [https://pypi.org/project/Flask/](https://pypi.org/project/Flask/)。

```sh
[root@master ~]# pip install Flask
Looking in indexes: http://nexushub.com:8081/repository/pypi-proxy/simple
Collecting Flask
  Downloading http://nexushub.com:8081/repository/pypi-proxy/packages/flask/2.0.3/Flask-2.0.3-py3-none-any.whl (95 kB)
     |████████████████████████████████| 95 kB 5.2 MB/s
Requirement already satisfied: itsdangerous>=2.0 in /usr/local/lib/python3.6/site-packages (from Flask) (2.0.1)
Requirement already satisfied: Jinja2>=3.0 in /usr/local/lib/python3.6/site-packages (from Flask) (3.0.3)
Requirement already satisfied: Werkzeug>=2.0 in /usr/local/lib/python3.6/site-packages (from Flask) (2.0.3)
Requirement already satisfied: click>=7.1.2 in /usr/local/lib/python3.6/site-packages (from Flask) (8.0.4)
Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.6/site-packages (from click>=7.1.2->Flask) (4.8.3)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib64/python3.6/site-packages (from Jinja2>=3.0->Flask) (2.0.1)
Requirement already satisfied: dataclasses in /usr/local/lib/python3.6/site-packages (from Werkzeug>=2.0->Flask) (0.8)
Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.6/site-packages (from importlib-metadata->click>=7.1.2->Flask) (3.6.0)
Requirement already satisfied: typing-extensions>=3.6.4 in /usr/local/lib/python3.6/site-packages (from importlib-metadata->click>=7.1.2->Flask) (4.1.1)
Installing collected packages: Flask
Successfully installed Flask-2.0.3
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
[root@master ~]#
[root@master ~]# pip list|grep Flask
Flask               2.0.3
[root@master ~]#
```

可以看到，成功通过代理安装了Flask 2.0.3版本。

此时，在nexus界面Browse浏览器里面也可以看到刚才下载的Flask包被缓存了下来：

![](/img/Snipaste_2023-09-12_23-05-22.png)
说明我们的pypi配置正确，代理仓库能够正常工作了！

## 3. 自动化配置准备

为了以后通过nexus api接口创建nexus仓库的自动化配置，将pypi-proxy代理仓库的相关信息配置到`nexus.yaml`配置文件中。

```yaml
nexus_info:
  Repositories:
    - name: yum-proxy
      type: proxy
      format: yum
      remote_url: https://mirrors.tuna.tsinghua.edu.cn/centos/
      user_agent: Sync yum repo

    - name: epel-proxy
      type: proxy
      format: yum
      remote_url: https://mirrors.tuna.tsinghua.edu.cn/epel/
      user_agent: Sync yum repo

    - name: pypi-proxy
      type: proxy
      format: pypi
      remote_url: https://pypi.tuna.tsinghua.edu.cn
      user_agent: Sync python pypi repo

```

使用Python读取YAML配置文件，可参考 [读取yaml配置文件](../../backend/python/yaml.md) 。