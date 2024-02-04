# -*- coding: utf-8 -*-
import os
import ssl
import sys
import json
import urllib.request, urllib.error, urllib.parse

import yaml
from dotenv import load_dotenv

# 自定义包
from common_tools import my_logger, script_dir, create_log_folder, time_now, decrypt

BASE_DIR = script_dir(__file__)
LOG_FOLDER = f'{BASE_DIR}/logs'
create_log_folder(LOG_FOLDER)
TODAY = time_now('%Y-%m-%d')
# 日志文件
LOG_FILE = f'{LOG_FOLDER}/{os.path.basename(sys.argv[0])}_{TODAY}.log'
# 配置文件
CONFIG_FILE = f'{BASE_DIR}/config.yaml'
LOGGER = my_logger(LOG_FILE)
LOGGER.info('开始调用zabbix api接口创建监控项和触发器')

load_dotenv()

# TODO: 1. 新增监控项时校验键值
# TODO: 2. 编写日志监控项配置模板
# TODO: 3. 配置文件校验与优化

# 监控项可用的类型，此处仅列出常用类型
# 详细参考 https://www.zabbix.com/documentation/3.0/en/manual/api/reference/item/object#host
ITEM_TYPE_DICT = {
    'ZABBIX_AGENT': {'value': 0, 'name': 'Zabbix客户端，进程或端口监控使用'},
    'ZABBIX_AGENT_ACTIVE': {'value': 7, 'name': 'Zabbix客户端(主动式)，日志监控使用'},
}
# 信息类型
ITEM_VALUE_TYPE_DICT = {
    'float': {'value': 0, 'name': 'numeric float，浮点数'},
    'character': {'value': 1, 'name': 'character，字符'},
    'log': {'value': 2, 'name': 'log，日志'},
    'numeric_unsigned': {'value': 3, 'name': 'numeric unsigned，数字(无正负)'},
    'text': {'value': 4, 'name': 'text，文本'},
}


class ZabbixAPI:
    def __init__(self):
        """构建方法"""
        with open(CONFIG_FILE, encoding='utf-8') as yaml_config_file:
            zabbix_data = yaml.safe_load(yaml_config_file)
            LOGGER.info('zabbix_data:%s', zabbix_data)
            self.__zabbix_info = zabbix_data.get('zabbix_info')

        LOGGER.info(self.__zabbix_info)
        self.__url = os.environ.get('ZABBIX_API')
        self.__user = os.environ.get('ZABBIX_USERNAME')
        self.__password = decrypt(os.environ.get('ZABBIX_PASSWORD'))
        self.__header = {"Content-Type": "application/json-rpc"}
        self.__token_id = self.login()

    def login(self):
        """获取认证token"""
        LOGGER.info('获取认证token')
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.__user,
                "password": self.__password
            },
            "id": 0,
        }
        return self.curl(data)

    def curl(self, data):
        """发送请求"""
        LOGGER.info('发送请求')
        LOGGER.info('data: %s', data)
        # 全局取消证书验证
        ssl._create_default_https_context = ssl._create_unverified_context
        request = urllib.request.Request(self.__url, json.dumps(data).encode('utf-8'), self.__header)
        LOGGER.info('request: %s', request)
        result = urllib.request.urlopen(request)
        LOGGER.info('result: %s', result)
        response = json.loads(result.read().decode('utf-8'))
        LOGGER.info('response: %s', response)
        try:
            return response['result']
        except KeyError:
            raise KeyError

    def monit_create(self):
        """读取配置文件，并创建监控项和触发器"""
        for info in self.__zabbix_info:
            ip = info.get('ip')
            do_flag = info.get('do_flag')
            item_info = info.get('item')
            trigger_info = info.get('trigger')
            LOGGER.info('ip:%s', ip)
            LOGGER.info('do_flag:%s', do_flag)
            LOGGER.info('item_info:%s', item_info)
            LOGGER.info('trigger_info:%s', trigger_info)
            if not do_flag:
                print("配置文件中指定忽略本段监控项配置")
                LOGGER.info("配置文件中指定忽略本段监控项配置")
                continue
            # 读取监控项相关配置信息
            # 监控项配置
            item_name = item_info.get('item_name')  # 监控项的名称
            LOGGER.info('item_name:%s', item_name)
            item_type = ITEM_TYPE_DICT.get(item_info.get('item_type')).get('value')  # 监控项类型
            LOGGER.info('item_type:%s', item_type)
            item_key = item_info.get('item_key')  # 键值
            LOGGER.info('item_key:%s', item_key)
            info_type = ITEM_VALUE_TYPE_DICT.get(item_info.get('info_type')).get('value')  # 信息类型
            LOGGER.info('info_type:%s', info_type)
            delay = item_info.get('delay')  # 数据更新间隔，单位秒
            LOGGER.info('delay:%s', delay)
            delay_flex = item_info.get('delay_flex')  # 自定义时间间隔
            LOGGER.info('delay_flex:%s', delay_flex)
            history = item_info.get('history')  # 历史数据保存天数
            LOGGER.info('history:%s', history)
            trends = item_info.get('trends')  # 趋势数据保存天数
            LOGGER.info('trends:%s', trends)
            description = item_info.get('description')  # 描述信息
            LOGGER.info('description:%s', description)
            applications = item_info.get('applications')  # 应用集
            LOGGER.info('applications:%s', applications)
            status = item_info.get('status')  # 监控项状态
            LOGGER.info('status:%s', status)

            # 触发器配置
            trigger_name = trigger_info.get('name')
            LOGGER.info('trigger_name:%s', trigger_name)
            trigger_expression = trigger_info.get('expression')
            LOGGER.info('trigger_expression:%s', trigger_expression)
            trigger_comments = trigger_info.get('comments')
            LOGGER.info('trigger_comments:%s', trigger_comments)
            trigger_priority = trigger_info.get('priority')
            LOGGER.info('trigger_priority:%s', trigger_priority)
            LOGGER.info('创建监控项')
            self.create_item(
                host_ip=ip,
                item_name=item_name,
                item_type=item_type,
                item_key=item_key,
                info_type=info_type,
                delay=delay,
                delay_flex=delay_flex,
                history=history,
                trends=trends,
                description=description,
                applications=applications,
                status=status,
            )
            LOGGER.info('创建触发器')
            self.create_trigger(
                description=trigger_name,
                expression=trigger_expression,
                comments=trigger_comments,
                priority=trigger_priority,
            )

    def get_hosts(self, hostid=None):
        """获取所有主机列表信息，如果指定了hostid,则获取单个主机列表信息

        :args
        - hostid: 主机ID
        """
        LOGGER.info('获取所有主机列表信息')
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "selectGroups": "extend",
                "selectParentTemplates": ["templateid", "name"],
                "selectInterfaces": ["interfaceid", "ip"],
                "selectInventory": ["os"],
                "selectItems": ["itemid", "name"],
                "selectGraphs": ["graphid", "name"],
                "selectApplications": ["applicationid", "name"],
                "selectTriggers": ["triggerid", "name"],
                "selectScreens": ["screenid", "name"]
            },
            "auth": self.__token_id,
            "id": 1,
        }
        LOGGER.info('请求data:%s', data)
        if hostid:
            data["params"] = {
                "output": "extend",
                "hostids": hostid,
                "sortfield": "name"
            }
            LOGGER.info('指定hostid时的请求data:%s', data)
        return self.curl(data)

    def get_host(self, host_ip=None):
        """获取单个主机列表信息
        直接通过主机IP进行过滤，避免请求所有的主机信息，加速处理速度

        过滤关键信息，参考：
        https://www.zabbix.com/documentation/3.0/en/manual/api/reference_commentary#common-get-method-parameters

        :args
        - host_ip: 主机的IP
        """
        LOGGER.info('获取单个主机列表信息')
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "selectParentTemplates": ["templateid", "name"],
                "selectInterfaces": ["interfaceid", "ip"],
                "selectApplications": ["applicationid", "name"],
                "filter": {"ip": [host_ip]},  # 过滤'ip'属性是指定IP的主机信息
            },
            "auth": self.__token_id,
            "id": 1,
        }
        LOGGER.info('请求data:%s', data)
        return self.curl(data)

    def get_host_id_by_ip(self, host_ip=None):
        """通过主机IP获取主机ID

        :args
        - host_ip: 主机IP
        """
        LOGGER.info('通过主机IP获取主机ID')
        host_info = self.get_host(host_ip=host_ip)[0]
        LOGGER.info('host_info:%s', host_info)
        host_id = host_info.get('hostid')
        LOGGER.info('host_id:%s', host_id)
        return host_id

    def get_interfaceid_by_ip(self, host_ip=None):
        """获取主机接口ID信息，用于创建监控项

        :args
        - host_ip: 主机IP
        """
        LOGGER.info('获取主机接口ID信息')
        host_info = self.get_host(host_ip=host_ip)[0]
        LOGGER.info('host_info:%s', host_info)
        interfaces_info = host_info.get('interfaces')[0]
        LOGGER.info('interfaces_info:%s', interfaces_info)
        iterface_id = interfaces_info.get('interfaceid')
        LOGGER.info('iterface_id:%s', iterface_id)
        return iterface_id

    def get_host_applications(self, host_ip=None):
        """获取主机的应用集"""
        LOGGER.info('获取主机的应用集')
        host_info = self.get_host(host_ip=host_ip)[0]
        LOGGER.info('host_info:%s', host_info)
        applications_info = host_info.get('applications')
        LOGGER.info('applications_info:%s', applications_info)
        for application in applications_info:
            LOGGER.info('application:%s', application)
            print(application)
        return applications_info

    def get_host_applications_id_list(self, host_ip=None, app_name_list=None):
        """获取主机的应用集的ID列表"""
        LOGGER.info('获取主机的应用集的ID列表')
        app_id_list = []
        applications_info = self.get_host_applications(host_ip=host_ip)
        for application in applications_info:
            LOGGER.info('application:%s', application)
            if app_name_list:
                for app_name in app_name_list:
                    if application.get('name') == app_name:
                        app_id_list.append(application.get('applicationid'))
                    else:
                        if not self.appliction_exist(host_ip=host_ip, app_name=app_name):
                            crate_app_result = self.crate_application(host_ip=host_ip, app_name=app_name)
                            LOGGER.info('crate_app_result:%s', crate_app_result)
                            app_id_list.append(crate_app_result.get('applicationids')[0])
        LOGGER.info('app_id_list:%s', app_id_list)
        app_id_list = sorted(list(set(app_id_list)))
        LOGGER.info('app_id_list:%s', app_id_list)
        return app_id_list

    def appliction_exist(self, host_ip=None, app_name=None):
        """检查应用是否存在"""
        LOGGER.info('检查应用集中应用是否存在')
        applications_info = self.get_host_applications(host_ip=host_ip)
        exist_flag = app_name in [application.get('name') for application in applications_info]
        LOGGER.info('应用( %s )是否存在标志exist_flag:%s', app_name, exist_flag)
        return exist_flag

    def crate_application(self, host_ip=None, app_name=None):
        """创建主机应用集"""
        LOGGER.info('创建主机应用集')
        host_id = self.get_host_id_by_ip(host_ip=host_ip)
        data = {
            "jsonrpc": "2.0",
            "method": "application.create",
            "params": {
                "name": app_name,
                "hostid": host_id,
            },
            "auth": self.__token_id,
            "id": 1,
        }
        return self.curl(data)

    def get_item(self, host_ip=None):
        """ 获取监控项列表信息 """
        LOGGER.info('获取监控项列表信息')
        host_id = self.get_host_id_by_ip(host_ip=host_ip)
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": host_id,
                "sortfield": "name"
            },
            "auth": self.__token_id,
            "id": 1,
        }
        return self.curl(data)

    def item_key_exist(self, host_ip=None, key=None):
        """ 检查监控项对应的键值是否存在 """
        LOGGER.info('检查监控项对应的键值是否存在')
        host_id = self.get_host_id_by_ip(host_ip=host_ip)
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": host_id,
                "sortfield": "name",
                "filter": {"key_": [key]},  # 过滤'key_'属性是指定键值的主机信息
            },
            "auth": self.__token_id,
            "id": 1,
        }
        return bool(self.curl(data))

    def create_item(self, **kwargs):
        """创建监控项
        参考： https://www.zabbix.com/documentation/3.0/en/manual/api/reference/item/create

        :args:
        - kwargs 监控项相关的参数
        """
        # TODO: 监控项键值存在检查，
        LOGGER.info('创建监控项')
        host_ip = kwargs.get('host_ip')
        host_id = self.get_host_id_by_ip(host_ip=host_ip)
        item_name = kwargs.get('item_name')
        item_type = kwargs.get('item_type')
        item_key = kwargs.get('item_key')
        info_type = kwargs.get('info_type')
        delay = kwargs.get('delay')
        delay_flex = kwargs.get('delay_flex')
        history = kwargs.get('history')
        trends = kwargs.get('trends')
        description = kwargs.get('description')
        applications = kwargs.get('applications')
        applications = self.get_host_applications_id_list(host_ip=host_ip, app_name_list=applications)
        status = kwargs.get('status')

        if self.item_key_exist(host_ip=host_ip, key=item_key):
            print(f'{item_key} 对应的监控项已经存在，请检查')
            LOGGER.error(' "%s" 对应的监控项已经存在，请检查', item_key)
            sys.exit(1)

        data = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "name": item_name,  # 监控项的名称
                "type": item_type,  # 监控项类型
                "key_": item_key,  # 监控项的键值,如：proc.num[python]
                "hostid": host_id,  # 主机ID
                "interfaceid": self.get_interfaceid_by_ip(host_ip=host_ip),  # 主机接口ID， 对应 IP:10050 的ID号
                "value_type": info_type,  # 信息类型
                # "data_type": 0,  # 数据类型，十进位数字
                "delay": delay,  # 数据更新间隔，单位秒
                "delay_flex": delay_flex,  # 自定义时间间隔
                "history": history,  # 历史数据保存天数
                "trends": trends,  # 趋势数据保存天数
                "applications": applications,  # 应用集
                "description": description,  # 描述
                "status": status,  # 启用监控项
            },
            "auth": self.__token_id,
            "id": 1,
        }

        return self.curl(data)

    def create_trigger(self, **kwargs):
        """创建触发器
        参考： https://www.zabbix.com/documentation/3.0/en/manual/api/reference/trigger/object
        """
        LOGGER.info('创建监控项')
        description = kwargs.get('description')
        expression = kwargs.get('expression')
        comments = kwargs.get('comments')
        priority = kwargs.get('priority')
        LOGGER.info('description:%s', description)
        LOGGER.info('expression:%s', expression)
        LOGGER.info('comments:%s', comments)
        LOGGER.info('严重级别priority:%s', priority)
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": [
                {
                    "description": description,  # 触发器名称
                    "expression": expression,  # 描述
                    "comments": comments,  # 附加描述信息
                    "priority": priority,  # 严重级别
                }],
            "auth": self.__token_id,
            "id": 1,
        }
        return self.curl(data)


def main():
    """主函数，从配置文件中读取数据，并创建监控项和触发器"""
    zapi = ZabbixAPI()
    # h1 = zapi.get_host('127.0.0.1')
    # ip = '192.168.56.14'
    # h2 = zapi.get_host(ip)
    # print(h1)
    # print(h2)
    # print(zapi.get_host_id_by_ip(ip))
    # print(zapi.get_interfaceid_by_ip(ip))
    # print(zapi.get_host_applications(ip))
    # print(zapi.get_host_applications_id_list(ip))
    # print(zapi.get_host_applications_id_list(ip, ['OS', 'Processes', 'CPU']))
    zapi.monit_create()


if __name__ == '__main__':
    main()
