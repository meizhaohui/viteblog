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
