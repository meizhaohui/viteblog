#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Filename: auto_deploy_gitee_page.py
Date    : 2021-04-23 21:49:26
Function: 使用selenium操作浏览器自动部署Gitee Pages服务
Author  : 梅朝辉<mzh@hellogitlab.com>
Release : V1.0

1. 定位元素，参考：史上最全！Selenium元素定位的30种方式 https://blog.csdn.net/qq_32897143/article/details/80383502
2. 源码方法，参考：GiteePages自动部署  https://www.freesion.com/article/80541046591/
"""
import os
import time

# 将驱动放在脚本同级目录下
# Chrome驱动下载地址：http://npm.taobao.org/mirrors/chromedriver/


# 第三方包
# 操作浏览器
# 安装: pip3 install selenium
# 参考：https://pypi.org/project/selenium/
from selenium import webdriver
from selenium.webdriver.common.alert import Alert

# 第三方包
# 加载.env配置文件
# 安装: pip3 install python-dotenv
# 参考：https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

base_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

# 加载环境变量
gitee_host = os.getenv('GITEE_HOST')
username = os.getenv('GITEE_USERNAME')
password = os.getenv('GITEE_PASSWORD')
image_host = os.getenv('IMAGE_HOST')

# 模拟浏览器打开到gitee登录界面

# 创建chrome浏览器和他的无头模式
options = webdriver.ChromeOptions()
# 当不需要实际打开浏览器时，可以将以下headless行取消注释
options.add_argument('--headless')
options.add_argument("--disable-setuid-sandbox")
# 将驱动放在脚本同级目录下
executable = "%s/chromedriver" % base_dir
driver = webdriver.Chrome(executable_path=executable, options=options)
driver.get('%s/login' % gitee_host)
# 将窗口最大化
driver.maximize_window()
time.sleep(2)

# 输入账号--通过html的id属性定位输入位置--改为你的账号
user_login = driver.find_element_by_id('user_login')
user_login.send_keys(username)
# 输入密码--通过html的id属性定位输入位置--改为你的密码
driver.find_element_by_id('user_password').send_keys(password)
# 点击登录按钮--通过name确定点击位置
driver.find_element_by_name('commit').click()
time.sleep(2)

# 切换到gitee pages界面
driver.get('%s/%s/%s/pages' % (gitee_host, username, image_host))
# 点击更新按钮--通过xpath确定点击位置
driver.find_element_by_xpath('//*[@id="pages-branch"]/div[7]').click()
# 确认更新提示框--这个函数的作用是确认提示框
Alert(driver).accept()
# 等待5秒更新
time.sleep(5)

# 这个print其实没事什么用,如果真的要测试脚本是否运行成功，可以用try来抛出异常
print("gitee pages服务更新成功")

# 脚本运行成功,退出浏览器
driver.quit()
