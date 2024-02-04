# 自动启动代理程序V2rayN

[[toc]]



## 1. 需求说明

我们有一个科学代理程序V2rayN，使用的规则是每天动态修改端口号，避免被墙。正常情况下，可以每天手动修改代理程序的端口号，然后重启程序。但每次手动修改并启动程序有点麻烦，因此想通过Python脚本自动启动程序。

## 2. 程序说明

### 2.1 程序目录结构

```sh
$ find . -maxdepth 1
.
./.gitignore
./.idea
./.venv
./config.yaml
./guiNConfig.json
./logs
./main.py
./Pipfile
./Pipfile.lock
./requirements.txt

```

- `main.py`程序主文件。
- `config.yaml`程序配置文件，与代理程序V2rayN相关的配置。
- `requirements.txt`依赖包配置文件。
- `guiNConfig.json`，代理程序V2rayN的配置文件备份文件，不要将该文件上传到git仓库，避免信息泄露。



### 2.2 依赖包安装说明

可以使用以下命令直接安装依赖包：

```sh
pip install -r requirements.txt
```



### 2.3 主程序

主程序`main.py`内容如下：

```python
#!/usr/bin/python3
# filename: main.py
# author: meizhaohui
# date: 2023-12-11
# desc: auto change v2rayN-Core config file.
import os
import shutil
import json
import datetime
from collections import OrderedDict
import subprocess

# 第三方包
# pip install -r requirements.txt
# 日志模块
from loguru import logger
import yaml

# 当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 日志文件夹
LOG_FILE = f'{BASE_DIR}{os.sep}logs{os.sep}auto_start.log'
# 设置日志文件，目录会自动创建
logger.add(LOG_FILE)

# V2rayN的配置文件
YAML_CONFIG = f'{BASE_DIR}{os.sep}config.yaml'
logger.info(f'V2rayN胡配置文件:{YAML_CONFIG}')
today = datetime.datetime.today()
today_str = today.strftime('%m%d')
logger.info(f'今天日期:{today_str}')


class V2RAY:
    def __init__(self):
        """构造函数"""
        with open(YAML_CONFIG, encoding='utf-8') as yaml_file:
            self._v2ray = yaml.safe_load(yaml_file)
            logger.info(f'代理程序配置:{self._v2ray}')
        # 代理程序配置信息
        self._v2ray_info = self._v2ray.get('v2rayn_info')
        logger.info(f'代理程序配置信息:{self._v2ray_info}')
        self.exe_path = self._v2ray_info.get('exe_path')
        # 代理程序名称
        self.exe_name = self._v2ray_info.get('exe_name')
        # 代理程序启动路径
        self.exe_start_path = f'{self.exe_path}{os.sep}{self.exe_name}'
        logger.info(f'代理程序启动路径:{self.exe_start_path}')
        # 代理程序配置文件
        self.default_config = f"{self.exe_path}{os.sep}{self._v2ray_info.get('config_name')}"
        logger.info(f'代理程序配置文件:{self.default_config}')
        # 代理程序备份配置文件
        self.backup_config = f"{BASE_DIR}{os.sep}{self._v2ray_info.get('config_name')}"
        logger.info(f'代理程序备份配置文件:{self.backup_config}')

    def change_config(self):
        """修改配置文件"""
        logger.info('备份配置文件')
        shutil.copyfile(self.default_config, self.backup_config)
        # 读取备份的配置文件，并写入到默认(旧的)配置文件中
        with open(self.backup_config, encoding='utf-8') as f_in, \
                open(self.default_config, mode='w', encoding='utf-8') as f_out:
            # 加载json数据时保持原来顺序
            logger.info('加载json数据时保持原来顺序')
            json_dict = json.load(f_in, object_pairs_hook=OrderedDict)
            current_port = json_dict.get('vmess')[0].get("port")
            logger.info(f'当前端口号:{current_port}')
            json_dict.get('vmess')[0]["port"] = int(f'2{today_str}')
            new_port = json_dict.get('vmess')[0].get("port")
            logger.info(f'新的端口号:{new_port}')
            logger.info('将json数据写入到配置文件中')
            json.dump(json_dict, f_out, indent=2, ensure_ascii=False)
            logger.success('配置文件修改成功')

    def start_proxy(self):
        """启动代理程序"""
        subprocess.Popen(self.exe_start_path, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.success('代理程序自动启动成功！')


if __name__ == '__main__':
    v2obj = V2RAY()
    v2obj.change_config()
    v2obj.start_proxy()

```

该程序主要做以下事情：

- 自动获取当日时间字符串，如今天是2023年12月11日，则对应月份和日期的字符串为`1211`，用于生成新的端口号，如21211。
- 从V2rayN的配置文件 `config.yaml`，读取V2rayN的路径信息`D:\ProgramFiles\v2rayN-Core`、可执行文件名称`v2rayN.exe`、配置文件名称`guiNConfig.json`等。
- 备份配置文件`guiNConfig.json`到当前目录。
- 读取备份配置文件`guiNConfig.json`内容到`json_dict`中，并对该字典中的端口号信息进行修改，修改完成后将字典信息写入到原始配置文件`guiNConfig.json`中。
- 启动V2rayN可执行程序。

### 2.4 运行程序

使用pycharm运行程序：

```sh
E:\data\github_data\vueblog\myblog\docs\.vuepress\public\scripts\python\auto_start_proxy\.venv\Scripts\python.exe E:/data/github_data/vueblog/myblog/docs/.vuepress/public/scripts/python/auto_start_proxy/main.py
2023-12-11 23:12:06.328 | INFO     | __main__:<module>:28 - V2rayN胡配置文件:E:\data\github_data\vueblog\myblog\docs\.vuepress\public\scripts\python\auto_start_proxy\config.yaml
2023-12-11 23:12:06.328 | INFO     | __main__:<module>:31 - 今天日期:1211
2023-12-11 23:12:06.328 | INFO     | __main__:__init__:39 - 代理程序配置:{'v2rayn_info': {'exe_path': 'D:\\ProgramFiles\\v2rayN-Core', 'exe_name': 'v2rayN.exe', 'config_name': 'guiNConfig.json'}}
2023-12-11 23:12:06.328 | INFO     | __main__:__init__:42 - 代理程序配置信息:{'exe_path': 'D:\\ProgramFiles\\v2rayN-Core', 'exe_name': 'v2rayN.exe', 'config_name': 'guiNConfig.json'}
2023-12-11 23:12:06.328 | INFO     | __main__:__init__:48 - 代理程序启动路径:D:\ProgramFiles\v2rayN-Core\v2rayN.exe
2023-12-11 23:12:06.328 | INFO     | __main__:__init__:51 - 代理程序配置文件:D:\ProgramFiles\v2rayN-Core\guiNConfig.json
2023-12-11 23:12:06.328 | INFO     | __main__:__init__:54 - 代理程序备份配置文件:E:\data\github_data\vueblog\myblog\docs\.vuepress\public\scripts\python\auto_start_proxy\guiNConfig.json
2023-12-11 23:12:06.328 | INFO     | __main__:change_config:58 - 备份配置文件
2023-12-11 23:12:06.328 | INFO     | __main__:change_config:64 - 加载json数据时保持原来顺序
2023-12-11 23:12:06.328 | INFO     | __main__:change_config:67 - 当前端口号:21209
2023-12-11 23:12:06.328 | INFO     | __main__:change_config:70 - 新的端口号:21211
2023-12-11 23:12:06.328 | INFO     | __main__:change_config:71 - 将json数据写入到配置文件中
2023-12-11 23:12:06.328 | SUCCESS  | __main__:change_config:73 - 配置文件修改成功
2023-12-11 23:12:06.343 | SUCCESS  | __main__:start_proxy:79 - 代理程序自动启动成功！

Process finished with exit code 0
```

运行效果图：

![](/img/Snipaste_2023-12-11_23-14-53.png)



此时可以看到V2rayN程序成功启动，并且端口号已经是配置好了的！

![](/img/Snipaste_2023-12-11_23-16-13.png)



## 3. 快速启动

可以在桌面上增加一个`start_proxy.bat`程序，来快速启动python程序。

其内容如下：

```bash
E:\data\github_data\vueblog\myblog\docs\.vuepress\public\scripts\python\auto_start_proxy\.venv\Scripts\python.exe E:\data\github_data\vueblog\myblog\docs\.vuepress\public\scripts\python\auto_start_proxy\main.py
```

注意，**文件应以ANSI编码、Windows格式保存**。不要使用UTF-8编码、Unix格式保存。

以后直接双击该批处理脚本就可以快速启动代理程序了。