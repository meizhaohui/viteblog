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

