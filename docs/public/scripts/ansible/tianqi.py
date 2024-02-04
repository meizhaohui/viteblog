#coding=utf-8
import json
import requests

headers = {
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
}

response = requests.get('https://v0.yiketianqi.com/api?unescape=1&version=v61&appid=65338641&appsecret=XOP4imou&city=武汉', headers=headers)
result = response.json()
weather = result.get('wea')

class FilterModule(object):
    def filters(self):
        return {
            "split_everything": split_everything,
        }