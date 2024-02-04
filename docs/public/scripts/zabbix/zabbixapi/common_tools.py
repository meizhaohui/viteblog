#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author  : 梅朝辉

@Time    : 2023年2月13日14:57:07
@File    : common_tools.py
@Version : V1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description : 通用工具函数
@update:
V1.0 2023年2月13日14:57:07 构建通用工具函数
"""
import os
import base64
from datetime import datetime
import logging

# 可用的关键值
PASSWORD_SALT = '15_I_Wn2kDIH6RWv'


def script_dir(file=__file__):
    """返回当前脚本的所在目录,如果是在别的目录中引用的话，建议带上__file__作为参数"""
    return os.path.abspath(os.path.dirname(file))


def create_log_folder(path):
    """创建日志文件夹"""
    if not os.path.exists(path):
        os.mkdir(path)


def my_logger(logfile=None):
    """定义通用日志模板
    用法：
    LOGGER = mylogger('test.log')
    LOGGER.warn('warning')
    LOGGER.error('error')
    LOGGER.info('info')
    """
    # 配置日志文件，每天生成一个新的日志文件
    logging.basicConfig(
        level=logging.INFO,
        filename=logfile,
        filemode='a',
        format='%(asctime)s %(filename)s[line:%(lineno)d]===> %(levelname)s: %(message)s',
    )
    # 增加日志颜色
    # 参考：https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    logging.addLevelName(
        logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(
        logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
    logger = logging.getLogger(__name__)

    return logger


def time_now(fmt=None):
    """返回当前时间的字符串"""
    if fmt is None:
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    else:
        return datetime.now().strftime(fmt)


def encrypt(plain_text: str, salt=PASSWORD_SALT):
    """对明文字符串进行base64加密"""
    # 类型注解（Type annotations），参考:https://docs.python.org/3/library/typing.html

    # input:  'hello world !!!'
    # output: 'MTVfSV9XbjJrRElINlJXdmhlbGxvIHdvcmxkICEhIQ=='
    # 想将字符串转编码成base64, 要先将字符串转换成二进制数据
    # 被编码的参数必须是二进制数据
    plain_text = '%s%s' % (salt, plain_text)
    cipher_bit = base64.b64encode(plain_text.encode('utf-8'))
    # 将二进制字符串转换成普通字符串
    cipher_text = str(cipher_bit)[2:-1]
    return cipher_text


def decrypt(cipher_text: str, salt=PASSWORD_SALT):
    """对密文字符串进行base64解密"""
    # 类型注解（Type annotations），参考:https://docs.python.org/3/library/typing.html

    # input:  'SkNEWmpjZHpoZWxsbyB3b3JsZCAhISE='
    # output: 'hello world !!!'
    plain_text_with_salt = base64.b64decode(cipher_text).decode("utf-8")
    salt_length = len(salt)
    plain_text = plain_text_with_salt[salt_length:]
    return plain_text


def star_url_passwd(url: str):
    """对带用户名和密码的URL进行星号替换处理"""
    secure_password = url
    if len(url.split('@')) > 1:
        prefix = url.split('@')[0].rsplit(':', maxsplit=1)[0]
        suffix = url.split('@')[1]
        secure_password = f'{prefix}:********@{suffix}'
    return secure_password


if __name__ == '__init__':
    print(encrypt('securepass'))
    print(decrypt('MTVfSV9XbjJrRElINlJXdnNlY3VyZXBhc3M='))
