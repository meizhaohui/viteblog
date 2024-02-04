# Jenkins插件推荐

[[toc]]

## 1. 配置jenkins插件清华源加速

- 清华大学jenkins代理地址 [https://mirrors.tuna.tsinghua.edu.cn/jenkins/](https://mirrors.tuna.tsinghua.edu.cn/jenkins/)。
- 清华大学jenkins插件更新地址 [https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json](https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json)。

::: warning 注意
`hudson.model.UpdateCenter.xml`和`default.json`都必须更换，不然不生效!

`hudson.model.UpdateCenter.xml`和`default.json`都必须更换，不然不生效!

`hudson.model.UpdateCenter.xml`和`default.json`都必须更换，不然不生效!
:::

### 1.1 修改hudson.model.UpdateCenter.xml

直接进入到jenkins安装目录`/var/lib/jenkins`：

```sh
[root@jenkins ~]# cd /var/lib/jenkins/
[root@jenkins jenkins]#
```

备份默认配置文件：

```sh
[root@jenkins jenkins]# cp -p hudson.model.UpdateCenter.xml{,.bak}
```

修改配置文件：

```sh
[root@jenkins jenkins]# sed -i 's@https://updates.jenkins.io/update-center.json@https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json@g' hudson.model.UpdateCenter.xml
```

修改完成后，查看配置信息：

```sh
[root@jenkins jenkins]# cat hudson.model.UpdateCenter.xml
<?xml version='1.1' encoding='UTF-8'?>
<sites>
  <site>
    <id>default</id>
    <url>https://mirrors.tuna.tsinghua.edu.cn/jenkins/updates/update-center.json</url>
  </site>
</sites>
[root@jenkins jenkins]#
```


### 1.2 修改default.json

切换到`/var/lib/jenkins/updates/`目录，查看`default.json`：
```sh
[root@jenkins ~]# cd /var/lib/jenkins/updates/
[root@jenkins updates]# ll default.json
-rw-r--r-- 1 jenkins jenkins 2807834 Sep 13 20:21 default.json
```

备份：

```sh
[root@jenkins updates]# cp -p default.json(,.bak)
```

将 `https://updates.jenkins.io/download` 替换成 `https://mirrors.tuna.tsinghua.edu.cn/jenkins` 。

修改文件内容：

```sh
[root@jenkins updates]# sed -i 's@https://updates.jenkins.io/download@https://mirrors.tuna.tsinghua.edu.cn/jenkins@g' default.json
```

修改完成后，可以在web界面上访问 `http://myjenkins.com:8080/restart` 重启Jenkins服务。



## 2. 插件推荐

- 1. **AnsiColor**，此插件可改变控制台输出文字的颜色。如使用`echo`输出彩色字体。`echo -e '\033[1;32m 任务执行完成 \033[0m'`。

![](/img/Snipaste_2023-09-13_22-05-47.png)

- 2. **timestamper**，Adds timestamps to the Console Output。即在控制台增加时间戳信息。 如上面图片左侧就是安装本插件后，显示出的时间信息。

以上两个插件安装后，在Job任务配置中，需要勾选`Add timestamps to the Console Output`和`Color ANSI Console Output`选项：

![](/img/Snipaste_2023-09-13_22-09-37.png)

- 3. **build-timeout**，构建超时插件，可以设置超时时间。可参考 [https://plugins.jenkins.io/build-timeout/](https://plugins.jenkins.io/build-timeout/)

![](/img/Snipaste_2023-09-13_22-20-57.png)



参考:

- [如何安装Jenkins并配置插件（清华源）](https://blog.csdn.net/qq_30273575/article/details/127147785)

