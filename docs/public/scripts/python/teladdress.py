#!/usr/bin/python3
import requests

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

class LookupModule(LookupBase):

    def get_address(self, mobile:int):
        """获取手机号mobile对应的地址"""
        url = "https://eolink.o.apispace.com/teladress/teladress"
        token = "your_secure_token"
        payload = {"mobile":mobile}
        headers = {
            "X-APISpace-Token":token,
            "Authorization-Type":"apikey",
            "Content-Type":"application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data')
            # 省份
            province = data.get('province')
            # 城市
            city = data.get('city')
            # 运营商
            isp = data.get('isp')

            return province, city, isp

    def run(self, terms, variables, **kwargs):
        ret = []
        for term in terms:
            display.debug("teladdress lookup term: %s" % term)
            province, city, isp = self.get_address(term)
            result_str = f'归属地：{province}, {city}, 运营商: {isp}'
            ret.append(result_str)

