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

    def create_docker_blob(self):
        """创建docker blob块对象"""
        logger.info('创建docker blob块对象')
        payload = {
            "path": "docker",
            "name": "docker"
        }
        api = '/v1/blobstores/file'
        self.curl(api=api, method='POST', payload=payload)

    def create_repositories(self):
        """创建仓库"""
        for repo in self._repositories:
            filename = repo.get('name')
            repo_type = repo.get('type')
            repo_format = repo.get('format')
            logger.info(
                f'待创建的仓库的配置文件：{filename}, 仓库类型: {repo_type}, 仓库格式：{repo_format}')


if __name__ == '__main__':
    n = Nexus()
    n.create_docker_blob()
    n.create_repositories()


######################################################################
# 获取所有Blob对象存储
# import requests

# url = "http://nexusapi.com:8081/service/rest/v1/blobstores"

# headers = {
#     "Accept": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

######################################################################
# 创建Blob对象存储
# import requests

# url = "http://nexusapi.com:8081/service/rest/v1/blobstores/file"

# payload = {
#     "path": "blobpath",
#     "name": "blobname"
# }
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)

######################################################################
# 创建yum-proxy代理仓库
# import requests

# url = "http://nexusapi.com:8081/service/rest/v1/repositories/yum/proxy"

# payload = {
#     "name": "yum-proxy",
#     "online": True,
#     "storage": {
#         "blobStoreName": "default",
#         "strictContentTypeValidation": True
#     },
#     "proxy": {
#         "remoteUrl": "https://mirrors.tuna.tsinghua.edu.cn/centos",
#         "contentMaxAge": 1440,
#         "metadataMaxAge": 1440
#     },
#     "negativeCache": {
#         "enabled": True,
#         "timeToLive": 1440
#     },
#     "httpClient": {
#         "blocked": False,
#         "autoBlock": True,
#         "connection": {
#             "retries": 0,
#             "userAgentSuffix": "Email: yourname@email.com",
#             "timeout": 60,
#             "enableCircularRedirects": False,
#             "enableCookies": False,
#             "useTrustStore": False
#         }
#     }
# }
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)


# ######################################################################
# # 创建pypi-proxy代理仓库
# import requests

# url = "http://nexusapi.com:8081/service/rest/v1/repositories/pypi/proxy"

# payload = {
#     "name": "pypi-proxy",
#     "online": True,
#     "storage": {
#         "blobStoreName": "default",
#         "strictContentTypeValidation": True
#     },
#     "proxy": {
#         "remoteUrl": "https://pypi.tuna.tsinghua.edu.cn",
#         "contentMaxAge": 1440,
#         "metadataMaxAge": 1440
#     },
#     "negativeCache": {
#         "enabled": True,
#         "timeToLive": 1440
#     },
#     "httpClient": {
#         "blocked": False,
#         "autoBlock": True,
#         "connection": {
#             "retries": 0,
#             "userAgentSuffix": "Email: yourname@email.com",
#             "timeout": 60,
#             "enableCircularRedirects": False,
#             "enableCookies": False,
#             "useTrustStore": False
#         }
#     }
# }
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)
# print(response.status_code)


# ######################################################################
# # 创建maven-proxy代理仓库
# import requests

# url = "http://nexusapi.com:8081/service/rest/v1/repositories/maven/proxy"

# payload = {
#     "name": "maven-proxy",
#     "online": True,
#     "storage": {
#         "blobStoreName": "default",
#         "strictContentTypeValidation": True
#     },
#     "proxy": {
#         "remoteUrl": "https://maven.aliyun.com/repository/public",
#         "contentMaxAge": 1440,
#         "metadataMaxAge": 1440
#     },
#     "negativeCache": {
#         "enabled": True,
#         "timeToLive": 1440
#     },
#     "httpClient": {
#         "blocked": False,
#         "autoBlock": True,
#         "connection": {
#             "retries": 0,
#             "userAgentSuffix": "Email: yourname@email.com",
#             "timeout": 60,
#             "enableCircularRedirects": False,
#             "enableCookies": False,
#             "useTrustStore": False
#         }
#     },
#     "maven": {
#         "versionPolicy": "RELEASE",
#         "layoutPolicy": "STRICT",
#         "contentDisposition": "ATTACHMENT"
#     }
# }
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)
# print(response.status_code)


# ######################################################################
# # 创建docker-proxy代理仓库
# import os

# import requests
# import json

# url = "http://nexusapi.com:8081/service/rest/v1/repositories/docker/proxy"
# script_path = os.path.abspath(__file__)
# parent_dir = os.path.join(script_path, '..')
# filename = f"{parent_dir}/nexus_api/docker-proxy.json"

# with open(filename) as file:
#     payload = json.load(file)
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)
# print(response.status_code)


# ######################################################################
# # 创建docker-hosted本地仓库
# import os

# import requests
# import json

# url = "http://nexusapi.com:8081/service/rest/v1/repositories/docker/hosted"
# script_path = os.path.abspath(__file__)
# parent_dir = os.path.join(script_path, '..')
# filename = f"{parent_dir}/nexus_api/docker-hosted.json"

# with open(filename) as file:
#     payload = json.load(file)
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)
# print(response.status_code)


######################################################################
# 创建docker-group聚合仓库


# url = "http://nexusapi.com:8081/service/rest/v1/repositories/docker/group"
# script_path = os.path.abspath(__file__)
# parent_dir = os.path.join(script_path, '..')
# filename = f"{parent_dir}/nexus_api/docker-group.json"

# with open(filename) as file:
#     payload = json.load(file)
# headers = {
#     "Accept": "application/json",
#     "Content-Type": "application/json",
#     "content-type": "application/json",
#     "Authorization": "Basic YWRtaW46YWRtaW4xMjM="
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)
# print(response.status_code)
