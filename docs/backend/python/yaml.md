# 读取yaml配置文件

有的时候，我们可以将一些配置信息存放在yaml配置文件中，然后读取配置文件即可。

- python中可以使用PyYAML模块来读取配置文件。

- PyYAML安装方法`pip install pyyaml`。

PyYAML读取配置文件的示例。

如我们现在有一个配置文件`nexus.yaml`，其内容如下：

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

```

我们使用PyYAML来读取该配置文件：

```python
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

```

运行程序：

```sh
$ python read_yaml.py
仓库名称：yum-proxy, 仓库类型: proxy, 仓库格式：yum, 远程仓库: https://mirrors.tuna.tsinghua.edu.cn/centos/， agent信息：Sync yum repo
仓库名称：epel-proxy, 仓库类型: proxy, 仓库格式：yum, 远程仓库: https://mirrors.tuna.tsinghua.edu.cn/epel/， agent信息：Sync yum repo
```

可以看到，正常获取并输出了我们的配置文件中的配置信息！说明我们PyYAML模块可以正常使用了！

再加上一些其他的配置信息，然后利用neuxs的api接口，就可以快速创建新的nexus仓库啦！