#  搭建自己的nexus私有仓库11--Nexus API接口的使用优化

[[toc]]

本文档是nexus系列课程第11篇。

- nexus系列课程第1篇，请参考 [搭建自己的nexus私有仓库1--nexus初体验](./create_your_nexus.md)
- nexus系列课程第2篇，请参考 [搭建自己的nexus私有仓库2--创建python pypi代理](./create_your_nexus_2.md)
- nexus系列课程第3篇，请参考 [搭建自己的nexus私有仓库3--创建yum ius代理](./create_your_nexus_3.md)
- nexus系列课程第4篇，请参考 [搭建自己的nexus私有仓库4--创建docker私有仓库](./create_your_nexus_4_docker_proxy.md)
- nexus系列课程第5篇，请参考 [搭建自己的nexus私有仓库5--测试docker仓库pull和push](./create_your_nexus_5_test_docker_proxy.md)
- nexus系列课程第6篇，请参考 [搭建自己的nexus私有仓库6--使用nginx反向代理](./create_your_nexus_6_nginx_proxy.md)
- nexus系列课程第7篇，请参考 [搭建自己的nexus私有仓库7--修改nexus容器时区](./create_your_nexus_7_change_timezone.md)
- nexus系列课程第8篇，请参考 [搭建自己的nexus私有仓库8--Nexus3的数据库结构](./create_your_nexus_8_nexus_database.md) 
- nexus系列课程第9篇，请参考 [搭建自己的nexus私有仓库9--Nexus API接口的使用1](./create_your_nexus_9_nexus_api.md)
- nexus系列课程第10篇，请参考 [搭建自己的nexus私有仓库10--Nexus API接口的使用2](./create_your_nexus_10_nexus_api_2.md)
## 0. 情况说明

本篇是在前两篇的基础上，通过Python调用Nexus API接口创建Nexus相关仓库。

需要完成以下需求：


- [√] Neuxs API接口调用时，是否有动态Token，如何正确获取API接口Token值。
- [√] 创建docker blob对象存储，将docker单独存放在该blob对象存储中。
- [√] 激活【Docker Bearer Token Realm】，让能够匿名下载Docker镜像。
- [√] 创建yum、pypi、maven、docker之类的仓库，docker仓库由于涉及到三种类型的仓库创建，并且有端口配置，使用API时优先创建yum和pypi代理代理仓库来测试API接口。
- 快速创建一个用户账号，如账号名为`devops`，并将给其授权能够朝docker-hosted仓库推送镜像。



## 1. 优化Python代码

通过对比观察前两篇的Python代码可以发现以下特点：

- `payload`对应的json数据，可以直接写到Python代码中，也可以通过Python代码读取json文件来获取对应配置信息。
- 除了请求的API接口的`url`路径不一样，代码其他位置内容是一样的。
- 大部分的仓库可以直接根据json配置文件文件名来判断需要创建的仓库类型，为了自定义其他文件名，我们可以单独创建一个配置文件来定义json配置文件文件名与仓库类型的关系。

创建nexus_api文件夹，并在其中创建`config`配置文件夹：

![Snipaste_2024-03-03_18-07-22.png](/img/Snipaste_2024-03-03_18-07-22.png)

nexus_api文件夹目录结构如下：

```sh
$ find
.
./config
./config/docker-group.json
./config/docker-hosted.json
./config/docker-proxy.json
./config/epel-yum-proxy.json
./config/ius-yum-proxy.json
./config/maven-proxy.json
./config/nexus.yaml
./config/pypi-proxy.json
./config/yum-proxy.json
./main.py
./requirements.txt
```



### 1.1 定义nexus仓库的配置文件

`config/nexus.yaml`配置文件用于定义需要创建的仓库的配置文件与仓库类型的对应关系。

```yaml
nexus_info:
  Repositories:
    - name: yum-proxy.json
      type: proxy
      format: yum

    - name: epel-yum-proxy.json
      type: proxy
      format: yum

    - name: ius-yum-proxy.json
      type: proxy
      format: yum

    - name: pypi-proxy.json
      type: proxy
      format: pypi

    - name: maven-proxy.json
      type: proxy
      format: maven

    - name: docker-proxy.json
      type: proxy
      format: docker

    - name: docker-hosted.json
      type: hosted
      format: docker

    - name: docker-group.json
      type: group
      format: docker

```

如果有其他类型的仓库需要创建，只用创建对应的仓库的json配置文件，并增加到`config/nexus.yaml`配置文件中即可。



### 1.2 优化Python代码

使用`pipenv`创建虚拟环境，并安装相关依赖包：

```sh
$ pipenv run pip install requests yaml loguru
```

生成依赖文件：

```sh
$ pipenv run pip freeze
certifi==2024.2.2
charset-normalizer==3.3.2
colorama==0.4.6
idna==3.6
loguru==0.7.2
PyYAML==6.0.1
requests==2.31.0
urllib3==2.2.1
win32-setctime==1.1.0
$ pipenv run pip freeze > requirements.txt
$ 
```



### 1.3 编写脚本

此处是我优化后的代码：

```python
# filename: main.py
# author: Zhaohui Mei <mzh.whut@gmail.com>
# date: 2024-3-5 22:51:31
# python: Python 3.8.5
# description: 使用Nexus API快速创建常用仓库
import sys
import json
import os

# 第三方库
import requests
import yaml
from loguru import logger


# 当前文件所在的目录
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]
print(BASE_DIR)
CONFIG_DIR = f'{BASE_DIR}/config'
LOG_DIR = f'{BASE_DIR}/log'
print(LOG_DIR)
YAML_CONFIG = f'{CONFIG_DIR}/nexus.yaml'

# 设置日志路径和日志轮转
logger.add(f'{LOG_DIR}/nexus.log', rotation="500 MB", retention=10)


class Nexus:
    def __init__(self):
        """构造函数"""
        with open(YAML_CONFIG, encoding='utf-8') as yaml_file:
            self._nexus = yaml.safe_load(yaml_file)
        self._nexus_info = self._nexus.get('nexus_info')
        # api接口基本路径
        self._path = self._nexus_info.get('API_base_path')
        # nexus api token
        self._token = self._nexus_info.get('base64_info')
        # 待创建仓库相关信息
        self._repositories = self._nexus_info.get('Repositories')
        logger.info(f'api接口基本路径:{self._path}')
        logger.info(f'api接口token信息:{self._token}')
        logger.info(f'待创建仓库相关信息:{self._repositories}')

    def curl(self, api='', method='POST', payload=None):
        """自定义请求方法
        api: api接口信息，如`/v1/blobstores/file`
        method: 请求方法，由于大部分接口都是创建仓库，因此默认使用POST方法，也可以GET方法等
        payload: 使用POST请求时，需要传输的json数据信息
        """
        api_url = f'{self._path}{api}'
        logger.info(f'请求的API接口URL: {api_url}')
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "content-type": "application/json",
            "Authorization": f"Basic {self._token}"
        }
        logger.info(f'请求头部信息: {headers}')
        try:
            response = requests.request(
                method=method, url=api_url, json=payload, headers=headers)
            logger.info(f'请求响应response: {response}')
            status_code = response.status_code
            logger.info(f'退出码：{status_code}')
            if status_code not in [200, 201, 204]:
                logger.warning(f'请求 {api_url} 接口异常 ，请检查')
                logger.info(response.json)
        except:
            logger.error('发生异常')
            sys.exit(1)

    def create_docker_blob(self):
        """创建docker blob块对象"""
        logger.info('创建docker blob块对象')
        payload = {
            "path": "docker",
            "name": "docker"
        }
        api = '/v1/blobstores/file'
        self.curl(api=api, method='POST', payload=payload)

    def set_active_realm(self):
        """设置激活的Realm"""
        logger.info('设置激活的Realm')
        payload = [
            "NexusAuthenticatingRealm",
            "NexusAuthorizingRealm",
            "DockerToken"
        ]
        api = '/v1/security/realms/active'
        self.curl(api=api, method='PUT', payload=payload)

    def create_repository(self, repo_format=None, repo_type=None, json_file=None):
        """创建单个仓库"""
        logger.info('创建仓库')
        with open(json_file) as file:
            payload = json.load(file)
        api = f'/v1/repositories/{repo_format}/{repo_type}'
        self.curl(api=api, method='POST', payload=payload)
        logger.success(f'成功创建仓库格式:{repo_format}，类型:{repo_type}')

    def create_repositories(self):
        """创建多个仓库"""
        logger.info('根据配置文件定义创建多个仓库')
        for repo in self._repositories:
            logger.info(f'当前处理的仓库repo: {repo}')
            filename = repo.get('name')
            logger.info(f'仓库配置文件名: {filename}')
            json_file = f'{CONFIG_DIR}/{filename}'
            logger.info(f'仓库配置文件绝对路径: {json_file}')
            repo_type = repo.get('type')
            repo_format = repo.get('format')
            logger.info(
                f'待创建的仓库的配置文件：{json_file}, 仓库类型: {repo_type}, 仓库格式：{repo_format}')
            self.create_repository(
                repo_format=repo_format, repo_type=repo_type, json_file=json_file)


if __name__ == '__main__':
    n = Nexus()
    n.create_docker_blob()
    n.set_active_realm()
    n.create_repositories()

```

运行代码前，默认有以下7个仓库：

![Snipaste_2024-03-05_23-00-24.png](/img/Snipaste_2024-03-05_23-00-24.png)

运行脚本：

```sh
$ .venv/Scripts/python main.py
E:\data\viteblog\docs\public\scripts\python\nexus_api
E:\data\viteblog\docs\public\scripts\python\nexus_api/log
2024-03-05 23:01:48.000 | INFO     | __main__:__init__:40 - api接口基本路径:http://nexusapi.com:8081/service/rest
2024-03-05 23:01:48.000 | INFO     | __main__:__init__:41 - api接口token信息:YWRtaW46YWRtaW4xMjM=
2024-03-05 23:01:48.000 | INFO     | __main__:__init__:42 - 待创建仓库相关信息:[{'name': 'yum-proxy.json', 'type': 'proxy', 'format': 'yum'}, {'name': 'epel-yum-proxy.json', 'type': 'proxy', 'format': 'yum'}, {'name': 'ius-yum-proxy.json', 'type': 'proxy', 'format': 'yum'}, {'name': 'pypi-proxy.json', 'type': 'proxy', 'format': 'pypi'}, {'name': 'maven-proxy.json', 'type': 'proxy', 'format': 'maven'}, {'name': 'docker-proxy.json', 'type': 'proxy', 'format': 'docker'}, {'name': 'docker-hosted.json', 'type': 'hosted', 'format': 'docker'}, {'name': 'docker-group.json', 'type': 'group', 'format': 'docker'}]
2024-03-05 23:01:48.001 | INFO     | __main__:create_docker_blob:74 - 创建docker blob块对象
2024-03-05 23:01:48.001 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/blobstores/file
2024-03-05 23:01:48.001 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.027 | INFO     | __main__:curl:62 - 请求响应response: <Response [204]>
2024-03-05 23:01:48.028 | INFO     | __main__:curl:64 - 退出码：204
2024-03-05 23:01:48.028 | INFO     | __main__:set_active_realm:84 - 设置激活的Realm
2024-03-05 23:01:48.028 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/security/realms/active
2024-03-05 23:01:48.029 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.037 | INFO     | __main__:curl:62 - 请求响应response: <Response [204]>
2024-03-05 23:01:48.038 | INFO     | __main__:curl:64 - 退出码：204
2024-03-05 23:01:48.038 | INFO     | __main__:create_repositories:104 - 根据配置文件定义创建多个仓库
2024-03-05 23:01:48.038 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'yum-proxy.json', 'type': 'proxy', 'format': 'yum'}
2024-03-05 23:01:48.038 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: yum-proxy.json
2024-03-05 23:01:48.039 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/yum-proxy.json
2024-03-05 23:01:48.039 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/yum-proxy.json, 仓库类型: proxy, 仓库格式：yum
2024-03-05 23:01:48.039 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.040 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/yum/proxy
2024-03-05 23:01:48.040 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.099 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.100 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.100 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:yum，类型:proxy
2024-03-05 23:01:48.100 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'epel-yum-proxy.json', 'type': 'proxy', 'format': 'yum'}
2024-03-05 23:01:48.101 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: epel-yum-proxy.json
2024-03-05 23:01:48.101 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/epel-yum-proxy.json
2024-03-05 23:01:48.101 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/epel-yum-proxy.json, 仓库类型: proxy, 仓库格式：yum
2024-03-05 23:01:48.102 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.102 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/yum/proxy
2024-03-05 23:01:48.102 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.203 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.203 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.204 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:yum，类型:proxy
2024-03-05 23:01:48.204 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'ius-yum-proxy.json', 'type': 'proxy', 'format': 'yum'}
2024-03-05 23:01:48.204 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: ius-yum-proxy.json
2024-03-05 23:01:48.204 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/ius-yum-proxy.json
2024-03-05 23:01:48.205 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/ius-yum-proxy.json, 仓库类型: proxy, 仓库格式：yum
2024-03-05 23:01:48.205 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.205 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/yum/proxy
2024-03-05 23:01:48.205 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.261 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.261 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.262 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:yum，类型:proxy
2024-03-05 23:01:48.262 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'pypi-proxy.json', 'type': 'proxy', 'format': 'pypi'}
2024-03-05 23:01:48.262 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: pypi-proxy.json
2024-03-05 23:01:48.262 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/pypi-proxy.json
2024-03-05 23:01:48.263 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/pypi-proxy.json, 仓库类型: proxy, 仓库格式：pypi
2024-03-05 23:01:48.263 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.263 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/pypi/proxy
2024-03-05 23:01:48.264 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.337 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.338 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.338 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:pypi，类型:proxy
2024-03-05 23:01:48.339 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'maven-proxy.json', 'type': 'proxy', 'format': 'maven'}
2024-03-05 23:01:48.339 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: maven-proxy.json
2024-03-05 23:01:48.339 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/maven-proxy.json
2024-03-05 23:01:48.339 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/maven-proxy.json, 仓库类型: proxy, 仓库格式：maven
2024-03-05 23:01:48.339 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.340 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/maven/proxy
2024-03-05 23:01:48.340 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.418 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.418 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.419 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:maven，类型:proxy
2024-03-05 23:01:48.419 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'docker-proxy.json', 'type': 'proxy', 'format': 'docker'}
2024-03-05 23:01:48.419 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: docker-proxy.json
2024-03-05 23:01:48.420 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/docker-proxy.json
2024-03-05 23:01:48.420 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/docker-proxy.json, 仓库类型: proxy, 仓库格式：docker
2024-03-05 23:01:48.420 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.421 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/docker/proxy
2024-03-05 23:01:48.421 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.515 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.515 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.516 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:docker，类型:proxy
2024-03-05 23:01:48.516 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'docker-hosted.json', 'type': 'hosted', 'format': 'docker'}
2024-03-05 23:01:48.516 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: docker-hosted.json
2024-03-05 23:01:48.517 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/docker-hosted.json
2024-03-05 23:01:48.517 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/docker-hosted.json, 仓库类型: hosted, 仓库格式：docker
2024-03-05 23:01:48.517 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.517 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/docker/hosted
2024-03-05 23:01:48.518 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.589 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.590 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.590 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:docker，类型:hosted
2024-03-05 23:01:48.590 | INFO     | __main__:create_repositories:106 - 当前处理的仓库repo: {'name': 'docker-group.json', 'type': 'group', 'format': 'docker'}
2024-03-05 23:01:48.590 | INFO     | __main__:create_repositories:108 - 仓库配置文件名: docker-group.json
2024-03-05 23:01:48.591 | INFO     | __main__:create_repositories:110 - 仓库配置文件绝对路径: E:\data\viteblog\docs\public\scripts\python\nexus_api/config/docker-group.json
2024-03-05 23:01:48.591 | INFO     | __main__:create_repositories:113 - 待创建的仓库的配置文件：E:\data\viteblog\docs\public\scripts\python\nexus_api/config/docker-group.json, 仓库类型: group, 仓库格式：docker
2024-03-05 23:01:48.591 | INFO     | __main__:create_repository:95 - 创建仓库
2024-03-05 23:01:48.592 | INFO     | __main__:curl:51 - 请求的API接口URL: http://nexusapi.com:8081/service/rest/v1/repositories/docker/group
2024-03-05 23:01:48.592 | INFO     | __main__:curl:58 - 请求头部信息: {'Accept': 'application/json', 'Content-Type': 'application/json', 'content-type': 'application/json', 'Authorization': 'Basic YWRtaW46YWRtaW4xMjM='}
2024-03-05 23:01:48.646 | INFO     | __main__:curl:62 - 请求响应response: <Response [201]>
2024-03-05 23:01:48.646 | INFO     | __main__:curl:64 - 退出码：201
2024-03-05 23:01:48.647 | SUCCESS  | __main__:create_repository:100 - 成功创建仓库格式:docker，类型:group
$
```

运行日志截图：

![Snipaste_2024-03-05_23-03-35.png](/img/Snipaste_2024-03-05_23-03-35.png)

此时再查看仓库情况：

![Snipaste_2024-03-05_23-07-00.png](/img/Snipaste_2024-03-05_23-07-00.png)



可以看到我们定义的几个仓库都创建成功了！！

### 1.4 其他说明

- 如果你需要创建其他代理仓库，只需要编写对用的仓库配置的`json`文件，并更新`nexus.yaml`配置文件即可。

- 如果你需要添加代理仓库和组聚合仓库，更新`nexus.yaml`配置文件时请将聚合仓库配置在代理仓库下面。

  