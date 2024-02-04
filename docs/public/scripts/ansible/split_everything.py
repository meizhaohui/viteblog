#coding=utf-8
import re

def split_everything(content):
    """以多个分隔符将字符串分割成列表"""
    return re.split(',|\||:|;|@', content)


class FilterModule(object):
    def filters(self):
        return {
            "split_everything": split_everything,
        }