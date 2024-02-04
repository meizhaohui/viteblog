import os
import yaml

# 当前文件所在的目录
BASE_DIR = os.path.dirname(__file__)
YAML_CONFIG = f'{BASE_DIR}/nexus.yaml'

class Nexus:
    def __init__(self):
        """构造函数"""
        with open(YAML_CONFIG, encoding='utf-8') as yaml_file:
            self._nexus = yaml.safe_load(yaml_file)
        self._nexus_info = self._nexus.get('nexus_info')
        self._repositories = self._nexus_info.get('Repositories')

    def create_repositories(self):
        """创建仓库"""
        for repo in self._repositories:
            name = repo.get('name')
            repo_type = repo.get('type')
            repo_format = repo.get('format')
            remote_url = repo.get('remote_url')
            user_agent = repo.get('user_agent')
            print(f'仓库名称：{name}, 仓库类型: {repo_type}, '
                  f'仓库格式：{repo_format}, 远程仓库: {remote_url}， '
                  f'agent信息：{user_agent}')


if __name__ == '__main__':
    n = Nexus()
    n.create_repositories()
