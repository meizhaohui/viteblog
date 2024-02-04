# 工具列表
[[toc]]

以下列出自己认为非常好用的工具，排名不分先后。

## 1. 截图工具`Snipaste`

`Snipaste`支持windows和MacOS系统，官网地址[https://www.snipaste.com/](https://www.snipaste.com/),按`F1`截图。
![Snipaste.png](/img/Snipaste.png)



## 2. Markdown编辑工具`Typora`或`MacDown`

Typora支持windows、Linux和MacOS系统，MacDown是在MacOS系统上的Markdown编辑器，两个编辑器都不错。

Typora所见即所得模式比较好，下载地址[https://www.typora.io/](https://www.typora.io/)。而我也比较喜欢MacDown左侧输入文本右侧自动显示最后生成的效果预览，下载地址[https://macdown.uranusjr.com/](https://macdown.uranusjr.com/)。

## 3. 在线生成Markdown表格`TableConvert`

在线生成Markdown表格`TableConvert`地址[https://tableconvert.com/](https://tableconvert.com/)

![tableconvert.png](/img/tableconvert.png)

该网站也可以从Excel表格、外部URL、XML文件等导入源数据，来生成Markdown表格信息。你可以非常轻松地获得对应的Markdown表格语法，实现一键转换，几乎不需要花费太多时间。

也可以通过API接口将需要的表格转换成Markdown表格语法。详细可参考 [https://tableconvert.com/api/#post-/convert/excel-to-markdown](https://tableconvert.com/api/#post-/convert/excel-to-markdown)。



## 4. 制作U盘启动盘`Rufus`和`Etcher`

`Rufus`支持windows系统，官网地址 [http://rufus.ie/](http://rufus.ie/)   

![rufus_en_2x.png](/img/rufus_en_2x.png)

`Etcher`支持windows、Linux和MacOS系统，官网地址[https://www.balena.io/etcher/](https://www.balena.io/etcher/)

![etcher_step.gif](/img/etcher_step.gif)


## 5. 国内开源镜像站

使用国内开源镜像站，可以使我们下载软件的速度更快，更方便！

### 5.1 阿里云镜像站

阿里云官方镜像站，提供极速全面的系统镜像服务，链接[https://developer.aliyun.com/mirror/](https://developer.aliyun.com/mirror/)。

![aliyun_mirror](/img/aliyun_mirror.png)



### 5.2 清华大学镜像站

清脂大学开源软件镜像站，链接[https://mirrors.tuna.tsinghua.edu.cn/](https://mirrors.tuna.tsinghua.edu.cn/)

![tsinghua_mirror.png](/img/tsinghua_mirror.png)

## 6. jsDelivr – Open Source CDN 开源CDN

[https://www.jsdelivr.com/?docs=gh](https://www.jsdelivr.com/?docs=gh), 可以用这个网站进行图片等的加速！

![](/img/20200511233130.png)

## 7. cmder windows系统上面的命令行工具

Windows系统自带的`cmd`命令行使用起来非常不方便，粘贴文本必须使用鼠标，不能使用快捷键，我们可以使用`cmder`工具使用windows系统上面的命令行工具。

官网地址：[https://cmder.net/](https://cmder.net/)

界面如下图所示：

![cmder](https://cmder.net/img/main.png)

将`Cmder.exe`文件所在目录添加到`Path`环境变量中，以管理员身份打开`cmd`命令行容器，执行以下命令注册右键：

```sh
// 设置任意地方鼠标右键启动Cmder
Cmder.exe /REGISTER ALL
```

## 8. 录屏软件EV录屏

EV录屏支持windows操作系统和MacOS操作系统。录屏非常方便，可以全屏录制也可以选定区域录制。

官网地址：[https://www.ieway.cn/evcapture.html](https://www.ieway.cn/evcapture.html)


## 9. windows系统传输文件到远程备份服务器工具putty

putty官网介绍`PuTTY: a free SSH and Telnet client`即是一个免费的SSH和Telnet客户端，我们可以通过它提供的`pscp`将windows系统的文件传输到远程的备份服务器中。

官网地址[https://www.chiark.greenend.org.uk/~sgtatham/putty/](https://www.chiark.greenend.org.uk/~sgtatham/putty/)

## 10. 终端分屏工具tmux

Tmux工具可以使SSH连接会话与窗口解绑，通过tmux工具可以使窗口关闭时，会话仍然不终止。下次连接时可以继续该会话。

详细可参考 阮一峰的网络日志 Tmux 使用教程http://www.ruanyifeng.com/blog/2019/10/tmux.html 

其常用命令如下：

- `tmux` 启动一个tmux窗口。此时按`ctrl+b d`或输入命令`tmux detach`将当前会话与窗口分离。
- `tmux ls`可以查看所有会话。
- `tmux attach -t ID/NAME`或`tmux a -t ID/NAME`通过会话id或name名称接入会话。
- `tmux kill-session -t ID/NAME`通过指定会话id或name名称来杀死会话。
- `tmux new -s session_name`创建会话时指定会话名称。
- `tmux rename-session -t ID/NAME new-name`或`tmux rename -t ID/NAME new-name`重命名会话名称。

使用示例：

```sh
$ tmux   # 启动一个会话，并按快捷键ctrl + b  d 分离会话与窗口
[detached (from session 0)]
$ tmux ls  # 查看当前存在的会话
0: 1 windows (created Wed Mar 17 06:45:51 2021)
$ tmux a -t 0  # 重新连接到会话，进入到会话中
[detached (from session 0)]
$ tmux rename -t 0 test  # 将ID为0的会话重命名为test
$ tmux ls  # 列出当前存在的会话，可以看到会话名称已经变成test了，但会话的创建时间并没有更新
test: 1 windows (created Wed Mar 17 06:45:51 2021)
$ tmux a -t test  # 接入到test会话
[detached (from session test)]
$ tmux new -s deploy  # 创建一个名称为deploy的会话
[detached (from session deploy)]
$ tmux ls  # 查看当前存在的会话
deploy: 1 windows (created Wed Mar 17 06:53:20 2021)
test: 1 windows (created Wed Mar 17 06:45:51 2021)
$ tmux kill-session -t test  # 杀死test会话
$ tmux ls  # 查看当前存在的会话
deploy: 1 windows (created Wed Mar 17 06:53:20 2021)
```

 

## 11. 图床工具PicGo

PicGo官网地址： [https://github.com/PicGo/](https://github.com/PicGo/)

PicGo的使用可参考： [PicGo：免费搭建个人图床](https://zhuanlan.zhihu.com/p/128014135)

注意，`repo`地址处不用写`https://gitee.com/`字符。

![image-20210421233656676](/img/image-20210421233656676.png)

参考： [PicGo 配置Gitee 图床](https://www.pianshen.com/article/12391560560/)



截图成功后，使用快捷键`command + shift + P`就可以调用PicGo上传图片了，上传成功后自动复制链接地址。

![](/img/20210421234510.png)



## 12. JSON解析工具jq

非常好用的json解析工具`jq`。

![](/img/20210821171120.png)

- 官方地址：[https://github.com/stedolan/jq](https://github.com/stedolan/jq) 。
- 你也可以参考我写的总结文档 [JSON解析工具-jq](../../OS/Centos/json_tool_jq.html) 。

## 13. Mac  App 启动和切换工具Manico

Manico 是一个为 macOS 设计的快速的 App 启动和切换工具。参考：[https://manico.im/](https://manico.im/)

![](https://manico.im/static/img/manico-homepage-banner@2x.5948f72d46dc.png)

按`Option`键⌥则可以调出app选择切换器，按住⌥的同时再按相应的数字键则可以快速切换到对应的应用。

Manico 默认使用 Option + 数字组件键。

2021年11月30日我花40元购买了该软件，现在没有弹窗。

![](/img/20211130214529.png)



## 14. 终端连接工具termius

- 官网地址：[https://www.termius.com/](https://www.termius.com/)



![](https://assets-global.website-files.com/5c7036349b5477bf13f828cf/6126f64cecfe794c371ddf30_6112100c32644a0172698ab3_hero_new_semaphore_2x-min.png)

优点：

- 免费
- 支持用户名密码和密钥模式
- 常用脚本片段（同时发送到多个主机）
- 全平台
- 云同步（注册一个账号即可）

缺点：

- SFTP需要付费才能使用
- 云同步需要付费版才可使用
- 默认为英文界面

快捷键：

![](/img/20211120221017.png)



## 15. windows终端连接工具MobaXterm

这也是一款非常不错的终端连接工具。

- 官网地址：[https://mobaxterm.mobatek.net/](https://mobaxterm.mobatek.net/)

![](https://mobaxterm.mobatek.net/img/moba/features/feature-terminal.png)

解除会话限制方法：参考 [https://github.com/flygon2018/MobaXterm-keygen](https://github.com/flygon2018/MobaXterm-keygen)

```py
Usage:
    MobaXterm-Keygen.py <UserName> <Version>

    <UserName>:      The Name licensed to
    <Version>:       The Version of MobaXterm
                     Example:    10.9
```

[download MobaXterm-Keygen.py](/scripts/python/MobaXterm-Keygen.py)

## 16. 文本编辑器Sublime Text

- 官网地址： [https://www.sublimetext.com/](https://www.sublimetext.com/)

![](https://www.sublimetext.com/screenshots/sublime_text_4_multi_select.gif)

## 17. SwitchHosts

SwitchHosts是一个管理、快速切换Hosts小工具，开源软件，一键切换Hosts配置，非常实用，高效。

下载地址: [https://github.com/oldj/SwitchHosts/releases](https://github.com/oldj/SwitchHosts/releases)



## 18. Windows对比工具Beyound Compare

试用处理。

注册表中删除 `\HKEY_CURRENT_USER\Software\ScooterSoftware\Beyond Compare 4\CacheId` 根据这个路径找到`CacheID`右击删除掉就可以 然后重新打开beyond compare。





## 19. 远程文件复制工具WinSCP

官网地址 [https://winscp.net/eng/index.php](https://winscp.net/eng/index.php)。

![](https://winscp-static-746341.c.cdn77.org/data/media/screenshots/commander.png)



## 20. FinalShell

FinalShell也可以进行远程终端连接，文件复制等！



## 21. Everything

Windows系统上面快速搜索文件。

官网地址：[https://www.voidtools.com/zh-cn/](https://www.voidtools.com/zh-cn/)

## 22. 变量名搜索CODELF

当在写代码时，有个变量名不知道用英文怎么表示，可以去这个网站上搜索一下，看看别的大佬是怎么表示的。

官网地址： [https://unbug.github.io/codelf/](https://unbug.github.io/codelf/)

## 23. 生成代码图片carbon

官网地址: [https://carbon.now.sh/](https://carbon.now.sh/)

## 24. 文件管理器ranger

ranger 是一个终端文件管理器，通过 ranger 可以实现和 windows 中类似的资源管理器的展示功能。

- 官网地址: [ranger](https://ranger.github.io/)
- 文档: [docs](https://ranger.github.io/ranger.1.html)

安装:

```sh
$ sudo pip install ranger-fm
```



## 25. 在线画图工具 excalidraw

Excalidraw 是一款开源的画图工具。

- 官网地址 [https://excalidraw.com/](https://excalidraw.com/)
- GitHub源码 [https://github.com/excalidraw/excalidraw](https://github.com/excalidraw/excalidraw)

使用该工具画的图：

![](/img/excalidraw.png)

## 26. 让屏幕显示你按的键盘符号

KeyCastr。这是一款 GitHub 上的开源免费软件，它可以让 Mac 在屏幕上实时显示你按下的键盘符号，比如在键盘上按了「command + shift + S」 键，屏幕上就会显示「⌘ ⇧ S」符号。

- 官网地址 [https://github.com/keycastr/keycastr](https://github.com/keycastr/keycastr)


## 27. windows 软件卸载工具Geek Uninstaller

Geek Uninstaller，官网[https://geekuninstaller.com/](https://geekuninstaller.com/)。

> Efficient and Fast, Small and Portable. 100% Free。
>    - Clean Removal and Force Removal
>    - Native X64 support
>    - Easy-to-use User Interface
>    - Uninstall Microsoft Store Apps

![](https://geekuninstaller.com/assets/images/screen_1.png)

## 28. 科学上网工具

有的时候，使用百度或必应搜索还是搜索不到自己想要的答案，这时候可以借助科学上网工具v2ray，进行代理，正常访问 Google等网站。

![](/img/Snipaste_2023-11-12_22-32-56.png)

最新版本V2RayN的系统代理默认关闭，开启方法：在任务栏找到V字图标，右键点击。悬停在【系统代理】选项卡，在弹出选项中选择【自动配置系统代理】。

![](/img/Snipaste_2023-11-12_22-36-13.png)



## 29. Umi-OCR 文字识别工具

-  Umi-OCR 是一款免费、开源、可批量的离线 OCR 软件，基于 PaddleOCR，适用于 Windows10/11 平台。
- 下载地址：[https://gitee.com/mirrors/Umi-OCR](https://gitee.com/mirrors/Umi-OCR) 。

![](https://tupian.li/images/2022/10/27/icon---256.png)

![](https://tupian.li/images/2023/11/19/65599097ab5f4.png)

效果图：

![](/img/Snipaste_2023-12-01_22-57-51.png)