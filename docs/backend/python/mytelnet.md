# python批量telnet检测IP地址的端口是否开放

[[toc]]



## 1.  需求说明

有的时候，如果检查某个服务器到别的主机的某些端口是否能够正常联通，首先想到使用`telnet`工具。但有时候主机没有外网权限，不方便安装`telnet`包。

这时候，就可以使用python批量telnet检测IP地址的端口是否开放。



参考：[python批量telnet检测IP地址的端口是否开放](https://www.jb51.net/article/281459.htm)



## 2. 工具编写

我们直接上代码。

```python
#!/usr/bin/python
# filename: mytelnet.py
# date:     2023-12-10 00:29:52
# desc:     批量telnet检测IP地址的端口是否开放
import sys
import telnetlib


class MyTelnet:
    def __init__(self, host=None, port=None, timeout=2) -> None:
        try:
            telnetlib.Telnet(host=host, port=port, timeout=timeout)
            # 端口开启，连接成功。打印带有加粗效果的绿色文本
            print(f'\033[1;32m{host}\t{port:8}\t[OK]\033[0m')
        except:
            # 端口未开启，连接拒绝。打印带有加粗效果的黄色文本
            print(f'\033[1;33m{host}\t{port:8}\t[Refused]\033[0m')


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print(f'请指定telnet主机地址和端口号，如: \npython {sys.argv[0]} "baidu.com" 22 80')
        sys.exit()

    host = sys.argv[1]
    port_list = [int(item) for item in sys.argv[2:]]
    port_list.sort()
    print('主机端口开通情况')
    for port in port_list:
        MyTelnet(host=host, port=port)

```

运行代码，检查到百度域名的一些端口是否开通：

```sh
$ python mytelnet.py "baidu.com" 80 443 22
主机端口开通情况
baidu.com             22        [Refused]
baidu.com             80        [OK]
baidu.com            443        [OK]
```

运行效果图：

![](/img/Snipaste_2023-12-10_00-39-04.png)

