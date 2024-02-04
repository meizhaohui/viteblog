# MacOS使用总结

[[toc]]

## 1. 打开访达文件夹的快捷键

![finder_keymap](/img/finder_keymap.png)

说明： 

- ⌘  代表 "command"键
- ⎇  代表"option"键
- ⌃ 代表"control"键
- ⇧ 代表"shift"键

通过快捷键⌃+⌘+空格键可以调出『表情符号与人物』窗口：

![emoji](/img/emoji.png)

点击『表情符号与人物』窗口右下角的向右的箭头，调到『技术符号』处就可以看到常用的"command"等键的符号了。

![emoji_command](/img/emoji_command.png)

## 2. 常用快捷键

- cmd+, 个人偏好设置
- cmd+shift+. 显示或隐藏.开头的隐藏文件
- cmd+tab 程序之间的切换
- cmd+h 窗口隐藏
- cmd+m 窗口最小化
- cmd+n 新建窗口
- cmd+o 打开，等同于双击打开
- cmd+s 保存
- cmd+shift+s 另存为
- cmd+p 打印 print
- cmd+w 关闭 close window
- cmd+q 退出quit
- cmd+a 全选select all
- cmd+i 显示信息show info
- cmd+f 搜索search
- cmd+c 复制copy
- cmd+v 粘贴paste
- cmd+delete 删除选中文件或文件夹 或者删除一行
- option+delete 删除一个单词
- cmd+c 复制
- cmd+v 粘贴
- cmd+z 撤销
- cmd+shift+delete 清空回收站
- cmd++ 放大
- cmd+- 缩小
- cmd+t 新建选项卡tab
- cmd+r 刷新refresh
- cmd+shift+3 截取整个屏幕
- cmd+shift+4 截取选择区域
-  cmd+shift+6 截取触控条
- fn+left 到顶部home
- fn+right 到底部end
- fn+up 上一页pageup
- fn+down 下一页pagedown
- control+cmd+F 进入全屏模式
- esc 退出全屏模式
- control+up 打开调度中心，点击右上角的+加号可以创建多桌面
- control+down 应用程序窗口
- F11 显示桌面
- control+A 移动到行首
- control+E 移动到行尾


注：以上"cmd"代表「command」键。

参考：[如何优雅地使用 macOS](https://zhuanlan.zhihu.com/p/29892969)

## 3. 最小化当前页面

`command + H` 暂时隐藏当前页面，使用`command + Tab`切换回来。
`command + M` 最小化当前页面，是暂时不想用当前程序，又不想`command + W`关闭窗口或者 `command + Q`关闭程序时候用的，使用`command + Tab`切换到应用后，松开`Tab`键，再按`option`唤出。

## 4. 显示桌面

- 使用键盘：MacBook默认按F11可以实现快速显示桌面。

- 如果mac没有设置为F1-F12作为功能键使用的话按Fn F11。

- 使用触控板：使用大拇指和其他三个手指同时展开来显示桌面。

另外，可以通过设置触发角来实现快速显示桌面：

![Snipaste_2022-07-23_06-42-16.png](/img/Snipaste_2022-07-23_06-42-16.png)

设置后，将鼠标移动到右下角就可以显示桌面了。


## 5. 快速搜索应用Alfred

Alfred具有很多功能，可以参考[Alfred 究竟好用在哪里？](https://www.zhihu.com/question/32227549)

下载地址：[https://www.alfredapp.com/](https://www.alfredapp.com/)

默认使用「Cmd + Space」打开Alfred，可以自定义为双击⌘键快速唤醒Alfred。

下面列出部分功能：

1. 搜索应用，快速打开应用,直接输入应用名称即可。
2.  查找本地文件，按空格，再输入搜索关键字。
3.  网页搜索，默认使用Google搜索，可以配置百度搜索，百度搜索的话，可以输入『bd 搜索关键字』进行搜索，Alfred中百度搜索配置如下：

![alfred_baidu_search](/img/alfred_baidu_search.png)

4. 简单数学计算，如输入「2+2」则会自动计算出结果4。
5. 查字典，如输入「d lovely」则会显示lovely的翻译。Alfred中字典配置如下：

![alfred_dict_search](/img/alfred_dict_search.png)

6. 退出某个应用程序，输入「quit 应用」。

其他功能大部分需要购买`Powerpack`就不介绍了。



## 6. CheatSheet的使用

macos中快捷键特别多，有时记不住快捷键，安装CheatSheet后，可以通过长按⌘键查看当前软件的快捷键。

你可以从[https://cheatsheet-mac.en.softonic.com/mac](https://cheatsheet-mac.en.softonic.com/mac)网站上面下载安装包。

你也可以从这里下载 [CheatSheet_1.0.1.zip](/resource/pkg/CheatSheet_1.0.1.zip)

如我的火狐浏览器中长按⌘键弹出的所有的快捷键如下图：

![firefox_shortcuts](/img/firefox_shortcuts.png)

## 7. shuttle的使用
参考[https://github.com/fitztrev/shuttle](https://github.com/fitztrev/shuttle)

Shuttle是一款快捷操作管理软件，你可以通过自定义命令，将常用的命令设置成图标快捷方式显示在任务栏中，当点击自定义的命令的名称时，shuttle会自动打开终端，并执行相应的命令。

如我的shuttle配置后，显示如下：

![shuttle](/img/shuttle.png)

- 点击「编辑」可以编辑默认的配置文件。
- 点击「导出」可以将默认的配置文件导出，你可以参照这个导出的配置文件写自己的命令。
- 点击「导入」可以导入自定义配置文件。


## 8. 访达中显示隐藏文件

- 快捷键

使用`command + shift + .` 可以显示或隐藏隐藏文件。

- 终端命令行设置

显示隐藏文件

```sh
$ defaults write com.apple.finder AppleShowAllFiles -boolean true;killall Finder
```

隐藏文件

```sh
$ defaults write com.apple.finder AppleShowAllFiles -boolean false;killall Finder
```


## 9. 访达中`复制`、`制作替身`、`拷贝`的区别

- `复制`   "Duplicate"是直接在当前文件夹复制生成一个一样的文件副本。
- `制作替身` "Make Alias"是生成一个快捷方式。
- `拷贝` "Copy"是复制文件，你可以使用`command + v`粘贴到别的位置。


## 10. 访达中从当前目录打开终端Go2Shell

在官网[https://zipzapmac.com/Go2Shell](https://zipzapmac.com/Go2Shell)下载安装包，参考官网进行安装并添加到访达中。

## 11. MAC禁用Adobe Creative Cloud自启状态栏

- 禁用Creative Cloud自启

```sh
$ launchctl unload -w /Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist
```

- 恢复

```sh
$ launchctl load -w /Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist
```




## 12. MacOS-homebrew卸载重装并更换国内源

- 卸载

```sh
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/uninstall)"
```

- 重装

```sh
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

- 更新

```sh
$ brew update
```

- 更换科大镜像源

```sh
# 第一步：替换brew.git
$ cd "$(brew --repo)"
$ git remote -v
origin	https://github.com/Homebrew/brew (fetch)
origin	https://github.com/Homebrew/brew (push)
$ git remote set-url origin https://mirrors.ustc.edu.cn/brew.git
$ git remote -v
origin	https://mirrors.ustc.edu.cn/brew.git (fetch)
origin	https://mirrors.ustc.edu.cn/brew.git (push)

# 第二步：替换homebrew-core.git
$ cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
$ git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
$ git remote -v
origin	https://mirrors.ustc.edu.cn/homebrew-core.git (fetch)
origin	https://mirrors.ustc.edu.cn/homebrew-core.git (push)

# 第三步：安装brew cask
$ git clone git://mirrors.ustc.edu.cn/homebrew-cask.git /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask --depth=1
```

- 更新

```sh
$ brew update
```

::: tip 注意
以上命令请在bash shell中执行。
:::

## 13. brew常用命令

- 执行更新brew命令

```sh
brew update
```

- 搜索
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    限时8
```sh
brew search 服务名称
```

- 安装

```sh
brew install 服务名称
```


## 14. oh-my-zsh打造强大的终端

### 14.1 安装oh-my-zsh
`oh-my-zsh`源码地址：[https://github.com/ohmyzsh/ohmyzsh](https://github.com/ohmyzsh/ohmyzsh)
安装：

```sh
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

如果以上不能运行，可能直接在[https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/install.sh](https://github.com/ohmyzsh/ohmyzsh/blob/master/tools/install.sh)复制install.sh的内容下来保存到文件`install.sh`中，使用`sh install.sh`运行即可。

运行脚本后，自动安装`oh-my-zsh`并设置默认的主题。 显示如下：

![installed_ohmyzsh](/img/installed_ohmyzsh.png)

### 14.2 安装`Powerline Fonts`字体

`Powerline Fonts`字体安装参考[https://github.com/powerline/fonts](https://github.com/powerline/fonts)

```sh
# 下载
➜  ~ git clone https://github.com/powerline/fonts.git --depth=1
Cloning into 'fonts'...
remote: Enumerating objects: 310, done.
remote: Counting objects: 100% (310/310), done.
remote: Compressing objects: 100% (236/236), done.
remote: Total 310 (delta 75), reused 260 (delta 71), pack-reused 0
Receiving objects: 100% (310/310), 10.40 MiB | 16.00 KiB/s, done.
Resolving deltas: 100% (75/75), done.

# 安装
➜  ~ cd fonts && sh install.sh
Copying fonts...
Powerline fonts installed to /Users/mzh/Library/Fonts
➜  fonts git:(master)

# 清理下载文件
➜  fonts git:(master) cd .. && trash-put fonts && trash-empty
```

### 14.3 设置主题

参考[https://github.com/ohmyzsh/ohmyzsh#selecting-a-theme](https://github.com/ohmyzsh/ohmyzsh#selecting-a-theme)

选择自己喜欢的主题，可以一直用一种主题，也可以使用随机主题。

像我配置的随机主题：

![oh_my_zsh_random_theme](/img/oh_my_zsh_random_theme.png)

重新加载配置
```sh
$ source ~/.zshrc
```

显示如下：
![reload_random_theme](/img/reload_random_theme.png)


### 14.4 设置插件

可参考[https://www.zhihu.com/question/49284484](https://www.zhihu.com/question/49284484)

可用的插件列表[https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins](https://github.com/ohmyzsh/ohmyzsh/wiki/Plugins)

我配置的插件如下：

```
plugins=(
    colored-man-pages
    command-not-found
    cp
    extract
    git
    gitignore
    last-working-dir
    safe-paste
    sudo
    vi-mode
    z
    zsh_reload
)
```

### 14.5 设置常用命令假名
```sh
alias cd1='cd ..'
alias cd2='cd ../..'
alias cd3='cd ../../..'
alias cd4='cd ../../../..'
alias cd5='cd ../../../../..'
alias ls='ls -G'
alias ll='ls -lah'
alias vi='vim'
alias v.='vim ~/.zshrc'
alias s.='source ~/.zshrc && echo "Reload OK!"'
# rm-protection link to https://github.com/alanzchen/rm-protection
alias rm='echo "please use \"trash-put\" or \"safe-rm\" or \"safe-p\" to delete file."'
# use the command to save no premission file   : w ! sudo tee %
alias dkin='dockerin'
function dockerin()
{
    docker exec -it $1 /bin/bash
}
alias gp='git push && git push gitee master'
export GITHUB_TOKEN="*******securce_string*******"
alias tl="travis login --github-token=${GITHUB_TOKEN}"
alias cblog='pushd ~/Documents/GitHub/vueblog/myblog && pwd'
alias runblog='pushd ~/Documents/GitHub/vueblog/myblog && yarn docs:dev'
```

## 15. HTTP请求工具`HTTPie`

- httpie是一个httpclient工具，能帮助我们快速的进行http请求，类似于`curl`，但是语法做了很多简写，比较友好。
- 提供`http`命令，允许使用简单而自然的语法发送任意的 HTTP 请求，并会显示彩色的输出。
- 官网地址[https://github.com/jakubroztocil/httpie](https://github.com/jakubroztocil/httpie)

### 15.1 HTTPie主要特点

- 具表达力的和直观语法
- 格式化的及彩色化的终端输出
- 内置 JSON 支持
- 表单和文件上传
- HTTPS、代理和认证
- 任意请求数据
- 自定义头部
- 持久化会话
- 类似`wget`的下载
- 完善的文档
- 跨平台，支持Windows、Linux、MacOS

### 15.2 安装

```sh
# MacOS
$ brew install httpie

# Debian, Ubuntu, etc.
$ apt-get install httpie

# Fedora
$ dnf install httpie

# CentOS, RHEL, ...
$ yum install httpie

# Arch Linux
$ pacman -S httpie
```

### 15.3 使用

- 查看版本信息

```sh
$ http --version                                                                                                                                                              
2.0.0
```

- 查看帮助信息

```sh
$ http --help|head -n 15                                                                                                                                                      
usage: http [--json] [--form] [--compress] [--pretty {all,colors,format,none}]
            [--style STYLE] [--print WHAT] [--headers] [--body] [--verbose]
            [--all] [--history-print WHAT] [--stream] [--output FILE]
            [--download] [--continue]
            [--session SESSION_NAME_OR_PATH | --session-read-only SESSION_NAME_OR_PATH]
            [--auth USER[:PASS]] [--auth-type {basic,digest}] [--ignore-netrc]
            [--offline] [--proxy PROTOCOL:PROXY_URL] [--follow]
            [--max-redirects MAX_REDIRECTS] [--max-headers MAX_HEADERS]
            [--timeout SECONDS] [--check-status] [--verify VERIFY]
            [--ssl {ssl2.3,tls1,tls1.1,tls1.2}] [--cert CERT]
            [--cert-key CERT_KEY] [--ignore-stdin] [--help] [--version]
            [--traceback] [--default-scheme DEFAULT_SCHEME] [--debug]
            [METHOD] URL [REQUEST_ITEM [REQUEST_ITEM ...]]

HTTPie - a CLI, cURL-like tool for humans. <https://httpie.org>
```

帮助文档非常的详细，你可以仔细阅读一下。

参考官方的示例：

![httpie](/img/httpie.png)

你可以尝试执行以下两个命令，查看他们的区别，你得到的显示结果与官网的示例结果会有部分差异。

```sh
# 使用curl发送请求
$ curl -i -X PUT httpbin.org/put -H Content-Type:application/json -d '{"hello": "world"}'
 
 # 使用HTTPie发送请求
$ http PUT httpbin.org/bin hello=world
```

- 使用docker运行本地服务

参考：[http://httpbin.org/](http://httpbin.org/)

```sh
# 启动httpbin容器，并把容器中端口80映射到宿主机的80端口，启动后在后台运行
$ docker run -p 80:80 --name httpbin  -d kennethreitz/httpbin                                                                                                                 
722e3a9c5338ad335a99d5b1d5882156367a1b9cad7cd13ece331dcafbd0e772

# 查看正在运行的容器
$ docker ps                                                                                                                                                                   
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                NAMES
722e3a9c5338        kennethreitz/httpbin   "gunicorn -b 0.0.0.0…"   5 seconds ago       Up 4 seconds        0.0.0.0:80->80/tcp   httpbin
~
```

启动服务后，浏览器中打开`localhost`，可以看到如下效果图：

![docker_local_httpbin](/img/docker_local_httpbin.png)


- 发送GET请求

```sh
$ http localhost/get
$ http GET localhost/get
$ http http://localhost/get
$ http :/get
```
上面几种方式都是向本地80端口的'/get'地址发送GET请求，返回结果相同：

![httpie_GET](/img/httpie_GET.png)

- 发送POST请求

```sh
$ $ http POST :/post name='http ie'           
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 452
Content-Type: application/json
Date: Sat, 04 Apr 2020 15:17:09 GMT
Server: gunicorn/19.9.0

{
    "args": {},
    "data": "{\"name\": \"http ie\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "application/json, */*",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Content-Length": "19",
        "Content-Type": "application/json",
        "Host": "localhost",
        "User-Agent": "HTTPie/2.0.0"
    },
    "json": {
        "name": "http ie"
    },
    "origin": "172.17.0.1",
    "url": "http://localhost/post"
}
```
发送POST请求，返回结果如下：

![httpie_POST](/img/httpie_POST.png)


- 发送PUT请求

```sh
$ http PUT :/put X-API-Token:123 name=John                                                                                                                   [23:17:17]
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: *
Connection: keep-alive
Content-Length: 472
Content-Type: application/json
Date: Sat, 04 Apr 2020 15:21:12 GMT
Server: gunicorn/19.9.0

{
    "args": {},
    "data": "{\"name\": \"John\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "application/json, */*",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Content-Length": "16",
        "Content-Type": "application/json",
        "Host": "localhost",
        "User-Agent": "HTTPie/2.0.0",
        "X-Api-Token": "123"
    },
    "json": {
        "name": "John"
    },
    "origin": "172.17.0.1",
    "url": "http://localhost/put"
}
```

- 下载文件

如从github上面下载用户图像：

```sh
$ http --download https://avatars0.githubusercontent.com/u/18098773\?s\=40\&u\=399293cf8c7a5843e96204c625a85a8eddd3bc00\&v\=4
HTTP/1.1 200 OK
Accept-Ranges: bytes
Access-Control-Allow-Origin: *
Cache-Control: max-age=300
Connection: keep-alive
Content-Length: 3355
Content-Security-Policy: default-src 'none'
Content-Type: image/png
Date: Sat, 04 Apr 2020 15:33:28 GMT
Etag: "cf1a33071c6ac7cae4a545d5cd6439999452268e"
Expires: Sat, 04 Apr 2020 15:38:28 GMT
Last-Modified: Fri, 02 Nov 2018 01:47:05 GMT
Source-Age: 1516927
Strict-Transport-Security: max-age=31557600
Timing-Allow-Origin: https://github.com
Vary: Authorization,Accept-Encoding
Via: 1.1 varnish
X-Cache: HIT
X-Cache-Hits: 1
X-Content-Type-Options: nosniff
X-Fastly-Request-ID: 228d3d1347cc3d66ab7ef431f3ddd832e95763dd
X-Frame-Options: deny
X-GitHub-Request-Id: 3DCE:7592:11ABE:14A9D:5E718348
X-Served-By: cache-tyo19938-TYO
X-Timer: S1586014409.640497,VS0,VE1
X-Xss-Protection: 1; mode=block

Downloading 3.28 kB to "18098773.png"
Done. 3.28 kB in 0.00093s (3.44 MB/s)
```

官网和[HTTPie：替代 Curl 和 Wget 的现代 HTTP 命令行客户端](https://linux.cn/article-10765-1.html)上面有非常多的示例，你可以尝试一下。

## 16. 定制你的`Touch Bar`触控条

首先，推荐一个工具`mtmr`，参考官网地址[https://github.com/Toxblh/MTMR](https://github.com/Toxblh/MTMR) .

使用`mtmr`的初衷是想把`Dock`图标显示在触控条中，不用在屏幕中显示，这样可以增加屏幕的有效使用面积。刚好`mtmr`有这个功能!!!非常棒！👍

你可以从这里[https://mtmr.app/](https://mtmr.app/)下载安装包。

- `mtmr`全称是’`My TouchBar. My rules`‘，是一款可以让你自定义Touch Bar的工具。
- 配置dock插件则可以显示正在运行的应用图标。
- 点击`MT`应用图标，`⌘+,`打开设置，`mtmr`通过`items.json`配置文件保存设置。你可以官网示例修改默认的设置。

我的触控条自定义后显示如下图所示：

![touchbar_display](/img/touchbar_display.png)

::: tip 提示
此处使用`cmd+shift+6`截取触控条图像。
:::


我的配置文件如下：

```json
[
  {
    "type": "escape",
    "width": 60,
    "align": "left",
    "comment": "退出",
    "background": "#FF0000",
    "title": "Esc",
    "bordered": false
  },
  {
    "type": "dock",
    "width": 400,
    "align": "right",
    "comment": "显示当前打开的应用，可以实现应用间的快速切换"
  },
  {
    "type": "brightnessDown",
    "width": 32,
    "bordered": false,
    "align": "left",
    "comment": "调低亮度"
  },
  {
    "type": "brightnessUp",
    "width": 32,
    "bordered": false,
    "align": "left",
    "comment": "调高亮度"
  },
  {
    "type": "displaySleep",
    "width": 40,
    "align": "right",
    "bordered": false,
    "comment": "显示器休眠"
  },
  {
    "type": "weather",
    "align": "right",
    "icon_type": "images",
    "api_key": "ca93a0bb8cdb428552660d83249e4bc9",
    "bordered": false,
    "comment": "显示当前天气情况"
  },
  {
    "type": "mute",
    "width": 40,
    "align": "right",
    "comment": "静音"
  },
  {
    "type": "volumeDown",
    "bordered": false,
    "align": "right",
    "width": 28,
    "comment": "调低音量"

  },
  {
    "type": "volumeUp",
    "bordered": false,
    "align": "right",
    "width": 28,
    "comment": "调高音量"
  },
  {
    "type": "previous",
    "align": "right",
    "width": 38,
    "comment": "前一首"
  },
  {
    "type": "play",
    "align": "right",
    "width": 38,
    "comment": "播放、暂停"
  },
   {
    "type": "next",
    "align": "right",
    "width": 38,
    "comment": "后一首"
  },
  {
    "type": "battery",
    "align": "right",
    "bordered": false,
    "comment": "显示当前电量"
  },
  {
    "type": "timeButton",
    "formatTemplate": "HH:mm",
    "align": "right",
    "bordered": false,
    "longAction": "shellScript",
    "longExecutablePath": "/usr/bin/pmset",
    "longShellArguments": [
      "sleepnow"
    ],
    "comment": "显示当前时间，长按系统休眠"
  }
]
```

说明，`json`中的"comment"是我用作备注信息的，默认没有此字段。

通过以上配置，并且设置Dock自动隐藏功能。后续通过触控条上面的图标可以快速的切换应用了，非常方便！

参考：[使用’mtmr’定制TouchBar](https://www.dazhuanlan.com/2019/10/12/5da0c0ef35a35/)





## 17. 开启和关闭SSH服务

mac本身安装了SSH服务，默认情况下不会开机自启。

启动SSH服务：

```sh
$ sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
Password: 输入你的密码
```

查看是否启动SSH服务：

```sh
$ sudo launchctl list|grep ssh
-	0	com.openssh.sshd
```

如果看到上面的输出表示成功启动了，可以尝试通过ssh连接到本地：

```sh
$ ssh mzh@localhost
The authenticity of host 'localhost (::1)' can't be established.
ECDSA key fingerprint is SHA256:gkrDoGnOl7VCoFTyfpRO/7UGR0FeB9x0eJY1X0kLzTw.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
Password:
Last login: Mon Jun 22 20:08:51 2020
$ whoami
mzh
$ exit
Connection to localhost closed.
```

关闭SSH服务：

```sh
$ sudo launchctl unload -w /System/Library/LaunchDaemons/ssh.plist
Password:
$ sudo launchctl list|grep ssh
$ echo $?
1
```

说明已经正常关闭了SSH服务。

## 18. Xcode 中配置 clang-format 格式化 C++ 代码

参考

- https://www.cnblogs.com/Wayou/p/xcode_clang_setup.html
- https://clang.llvm.org/docs/ClangFormatStyleOptions.html
- https://llvm.org/docs/CodingStandards.html

需要创建配置文件`~/.clang-format`，最后的配置内容如下：

```yaml
$ cat .clang-format
# Filename: .clang-format
# 参考地址：https://clang.llvm.org/docs/ClangFormatStyleOptions.html
# xcode 配置设置：
# Xcode 中配置 clang-format 格式化 C++ 代码
# https://www.cnblogs.com/Wayou/p/xcode_clang_setup.html

# 语言
Language: Cpp
# 编码样式风格，可取值LLVM, Google, Chromium, Mozilla, WebKit
# BasedOnStyle: Google
BasedOnStyle: LLVM
# 缩进宽度
IndentWidth: 4
# 列数
ColumnLimit: 100
# 对齐
# 开括号(开圆括号、开尖括号、开方括号)后的对齐: Align, DontAlign, AlwaysBreak(总是在开括号后换行)
AlignAfterOpenBracket: Align
# 连续赋值时，对齐所有等号
AlignConsecutiveAssignments: true
# 在转义换行符中对齐反斜杠, Right,Left,DontAlign
AlignEscapedNewlines: Left
# 在大括号前换行: Attach(始终将大括号附加到周围的上下文), Linux(除函数、命名空间和类定义，与Attach类似),
#   Mozilla(除枚举、函数、记录定义，与Attach类似), Stroustrup(除函数定义、catch、else，与Attach类似),
#   Allman(总是在大括号前换行), GNU(总是在大括号前换行，并对于控制语句的大括号增加额外的缩进), WebKit(在函数前换行), Custom
#   注：这里认为语句块也属于函数
BreakBeforeBraces: Linux
# 最大空行数
MaxEmptyLinesToKeep: 4
# 注释对齐
AlignTrailingComments: true
# 括号后面加空格
SpaceAfterCStyleCast: true
# 赋值运算符前加空格
SpaceBeforeAssignmentOperators: true
# 行尾的注意，在//前面加空格
SpacesBeforeTrailingComments: 4
# 允许短的if语句保持在同一行,为true时，`if (a) return; `可放在一行
AllowShortIfStatementsOnASingleLine: false
# 在三元运算符前换行
BreakBeforeTernaryOperators: true
# 允许重排注释
ReflowComments: true
# 在空的小括号中加一个空格
SpaceInEmptyParentheses: true
```



## 19. vim与clang-format集成

参考：

- https://clang.llvm.org/docs/ClangFormat.html#vim-integration

![](/img/Snipaste_2021-03-03_21-55-23.png)

在上一节配置好`.clang-format`配置文件后，此处直接对vim进行配置。

第一步，查看`clang-format.py`在哪里。

```sh
$ sudo find / -name 'clang-format.py‘
/usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py
```

查找到了`clang-format.py`路径后。对以下内容进行替换：

```
map <C-K> :pyf <path-to-this-file>/clang-format.py<cr>
imap <C-K> <c-o>:pyf <path-to-this-file>/clang-format.py<cr>
```

替换其中的`<path-to-this-file>/clang-format.py`，替换后的内容为：

```
map <C-K> :pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
imap <C-K> <c-o>:pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
```

以上是设置vim快捷键。

- normal模式下，ctrl+k将格式化一行代码
-  visual模式下，ctrl+k将格式化选中代码

- insert模式下，ctrl+k将格式化一行代码

再对以下内容进行替换，当vim保存文件时，自动格式化：

```sh
function! Formatonsave()
  let l:formatdiff = 1
  pyf ~/llvm/tools/clang/tools/clang-format/clang-format.py
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp call Formatonsave()
```

将第3行`pyf ~/llvm/tools/clang/tools/clang-format/clang-format.py`替换成`pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py`,并且在第5行中，增加`.c`文件的支持，在`*.cpp`后面增加`,*.c`。

最后替换后的内容为：

```sh
function! Formatonsave()
  let l:formatdiff = 1
  pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp,*.c call Formatonsave()
```

然后将以上两段内容加到`~/.vimrc`配置文件的中。

```sh
$ tail ~/.vimrc
"注释，normal模式下，ctrl+k将格式化一行代码
"注释，visual模式下，ctrl+k将格式化选中代码
"注释，insert模式下，ctrl+k将格式化一行代码
map <C-K> :pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
imap <C-K> <c-o>:pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
function! Formatonsave()
  let l:formatdiff = 1
  pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp,*.c call Formatonsave()
```

我最新的`.vimrc`配置好下：

```sh
$ cat .vimrc
set hlsearch
set backspace=2
set autoindent
set ruler
set showmode
set nu
set bg=dark
set ts=4
set softtabstop=4
set shiftwidth=4
set fileencodings=utf-8,gbk,gb18030,gk2312
syntax on
set showcmd
set clipboard+=unnamed
set cursorline
set confirm
set autoindent
set cindent
set expandtab
set laststatus=2
" Allow saving of files as sudo when I forgot to start vim using sudo.
" cmap w!! w !sudo tee > /dev/null %
cmap w!! w !sudo sh -c "cat > %"
"SET Comment START

autocmd BufNewFile *.c,*.py,*.go,*.sh exec ":call SetComment()" |normal 10Go

func SetComment()
    if expand("%:e") == 'c'
        call setline(1, "/*")
        call append(1, ' *      Filename: '.expand("%"))
        call append(2, ' *        Author: Zhaohui Mei<mzh.whut@gmail.com>')
        call append(3, ' *   Description:      ')
        call append(4, ' *   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(5, ' * Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(6, ' */')
        call append(7, '')
        call append(8, '')
        call append(9, '')
        call append(10, '')
    elseif expand("%:e") == 'go'
        call setline(1, "/*")
        call append(1, ' *      Filename: '.expand("%"))
        call append(2, ' *        Author: Zhaohui Mei<mzh.whut@gmail.com>')
        call append(3, ' *   Description:      ')
        call append(4, ' *   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(5, ' * Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(6, ' */')
        call append(7, 'package main')
        call append(8, '')
        call append(9, 'import "fmt"')
        call append(10, '')
        call append(11, 'func main() {')
        call append(12, '    fmt.Println("vim-go")')
        call append(13, '}')
   elseif expand("%:e") == 'py'
        call setline(1, '#!/usr/bin/python3')
        call append(1, '"""')
        call append(2, '#      Filename: '.expand("%"))
        call append(3, '#        Author: Zhaohui Mei<mzh.whut@gmail.com>')
        call append(4, '#   Description:      ')
        call append(5, '#   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(6, '# Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(7, '"""')
        call append(8, '')
        call append(9, '')
        call append(10, '')
    elseif expand("%:e") == 'sh'
        call setline(1, '#!/bin/bash')
        call append(1, '##################################################')
        call append(2, '#      Filename: '.expand("%"))
        call append(3, '#        Author: Zhaohui Mei<mzh.whut@gmail.com>')
        call append(4, '#   Description:      ')
        call append(5, '#   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(6, '# Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
        call append(7, '##################################################')
        call append(8, '')
        call append(9, '')
        call append(10, '')
        endif
endfunc
map <F2> :call SetComment()<CR>:10<CR>o

"SET Comment END

"SET Last Modified Time START
func DataInsert()
    if expand("%:e") == 'c' || expand("%:e") == 'go'
        call cursor(6, 1)
        if search ('Last Modified') != 0
            let line = line('.')
            call setline(line, ' * Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
        endif
    elseif expand("%:e") == 'py' || expand("%:e") == 'sh'
        call cursor(7, 1)
        if search ('Last Modified') != 0
            let line = line('.')
            call setline(line, '# Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
        endif
    endif
endfunc
autocmd FileWritePre,BufWritePre *.c,*.py,*.go,*.sh ks|call DataInsert() |'s
"SET Last Modified Time END

"" refer:https://blog.csdn.net/qq844352155/article/details/50513072
" c代码格式化配置
"normal模式下，ctrl+k将格式化一行代码
"visual模式下，ctrl+k将格式化选中代码
"insert模式下，ctrl+k将格式化一行代码
map <C-K> :pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
imap <C-K> <c-o>:pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
function! Formatonsave()
  let l:formatdiff = 1
  pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py
endfunction
autocmd BufWritePre *.h,*.cc,*.cpp,*.c call Formatonsave()
[mzh@MacBookPro ~ ]$
```

参考上面的自动格式化C程序的代码，以及自动插入备注信息等的代码。我们可以知道`autocmd`可以做一些事情。

上面自动格式化时，并没有对`return`语句进行格式化，我想在`return`语句前插入一个空格。



可以这样修改`.vimrc`文件：

```sh
"在return前面自动插入一个空行
function AddOneLineBeforeReturn()
    " 获取最后一行行号
    let l = line("$")
    " 执行替换命令
    " 注意此处 exe表示要执行命令。
    " \"1,\".'. 表示从第1行到最后一行
    " 后面的替换命令与自己在vim执行替换动作一样的
    exe "1,".l."s/;\\r *return \-*[0-9]*;$/\r&/g"
endfunction
" 将整个缓冲区写入文件时，调用以上函数
autocmd BufWritePre *.cpp,*.c call AddOneLineBeforeReturn()
```

这个时候，保证c或cpp文件时，每次都会在`return`语句前面加一个空行。并没有判断是否原来有空格，需要优化一下。

没有找到合适的方法进行判断`return`前面是否有空行。准备学习一下`vimscript`脚本语言的编写。



下面是我优化后的`.vimrc`配置文件：

```sh

" 以英文双引号开头的是注释信息
" Filename: .vimrc
" 在vim中输入:echo $MYVIMRC 命令可以知道文件存放位置
" :echom 会将打印的信息保存起来,可通过:messages命令查看到输出的消息
" :echo 会打印信息，但不保存
" :help echo 获取命令echo的帮助信息

" 参考:
" 1. VIM学习笔记 http://yyq123.github.io/learn-vim/learn-vi-00-00-TOC.html
" 2. Vimscript编程参考 https://www.w3cschool.cn/vim/nckx1pu0.html
" 3. vim-config https://github.com/PegasusWang/vim-config
" 4. 新手如何学习vimrc配置 https://zhuanlan.zhihu.com/p/50242838
" 基本设置 {
    " 忽略大小写检索
    set ignorecase
    " 设置高亮搜索匹配
    set hlsearch
    " 边输入边搜索(实时搜索)
    set incsearch
    " 设置退格方式
    " indent 允许在自动缩进上退格
    " eol 允许在换行符上退格
    " start 允许在插入开始的位置上退格
    " 2 同 ":set backspace=indent,eol,start"
    set backspace=2
    " 开启新行时,从当前行复制缩进距离,即自动缩进
    set autoindent
    " 实现C程序的缩进
    set cindent 
    " 在vim执行命令行时，使用tab键自动补充
    set wildmenu
    " 标尺，在右下角显示当前行号和列号,逗号分隔
    set ruler
    " 在左下角显示当前VIM模式
    set showmode
    " 在状态栏显示正在输入的命令
    set showcmd
    " 显示行号
    set number
    " bg, 使用深色背景上看起来舒服的颜色,也可以设置为light
    set background=dark
    " 设置tab宽度，与ts等效
    set tabstop=4
    " 当tabstop=8时，输入一次tab会显示4个空格
    " 再输入一次tab时，vim会删除前面的4个空格，并插入一个tab字符
    set softtabstop=4
    " 自动缩进时，缩进长度为4
    set shiftwidth=4
    " 在插入模式下自动将tab替换成tabstop对应的空格
    set expandtab
    " 旧文件可用的字符集
    set fileencodings=utf-8,gbk,gb18030,gk2312
    " 设置VIM内部使用的字符编码
    set encoding=utf-8
    " 启动文件类型检查
    filetype on
    " 语法高亮
    syntax on
    " 显示当前光标所在行的横线
    set cursorline
    " 显示当前光标所在列的竖线
    set cursorcolumn
    " 文件未保存时进行提示
    set confirm
    " 总是显示状态栏
    set laststatus=2
    " 如果文件改动，则自动把内容写回文件
    set autowrite
    " 如果发现文件在VIM之外被修改，则自动载入
    set autoread

"  }

" 设置键映射前缀
" 设置-减号为前缀
" 注意此处定义时变量名是mapleader，而引用时是<leader>
let mapleader = "-"

" 映射 {
    " Allow saving of files as sudo when I forgot to start vim using sudo.
    " cmap w!! w !sudo tee > /dev/null %
    " cmap w!! w !sudo sh -c "cat > %"
    cnoremap w!! w !sudo tee % > /dev/null

    " 在浏览器中打开URL
    " 使用:call open() 命令打开url
    function! OpenURL()
        " 获取当前行的内容
        let line = getline('.')
        " 使用浏览器打开URL，注意firefox浏览器地址路径前的感叹号需要保留
        exec "!/Applications/Firefox.app/Contents/MacOS/firefox ".line
    endfunction
    " 普通模式下,设置快捷键，通过按url则会通过浏览器打开相应的URL地址
    map url :call OpenURL()<cr>

    " 插入模式下，按jj快捷键输入ESC退出键
    imap jj <esc>
    
    " 按F2插入文件注释信息
    map <F2> :call SetComment()<CR>:10<CR>o

    " 设置进入粘贴模式快捷键F10
    map <F10> :set paste<CR>

    " 通过按9跳转到行末尾，0默认跳转到行首
    map 9 $

    " ctrl + A 选中文本所有内容
    map <silent> <C-A> gg v G$
    
    " 编辑我的.vimrc配置文件
    nnoremap <leader>ev :vsplit $MYVIMRC<cr>

    " 重新加载.vimrc配置文件
    nnoremap <leader>sv :source $MYVIMRC<cr>

"  }


" 文件头注释 { 
    "SET Comment START
    autocmd BufNewFile *.c,*.py,*.go,*.sh exec ":call SetComment()" |normal 10Go

    func SetComment()
        if expand("%:e") == 'c'
            call setline(1, "/*")
            call append(1, ' *      Filename: '.expand("%"))
            call append(2, ' *        Author: Zhaohui Mei<mzh.whut@gmail.com>')
            call append(3, ' *   Description:      ')
            call append(4, ' *   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(5, ' * Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(6, ' */')
            call append(7, '')
            call append(8, '')
            call append(9, '')
            call append(10, '')
        elseif expand("%:e") == 'go'
            call setline(1, "/*")
            call append(1, ' *      Filename: '.expand("%"))
            call append(2, ' *        Author: Zhaohui Mei<mzh.whut@gmail.com>')
            call append(3, ' *   Description:      ')
            call append(4, ' *   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(5, ' * Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(6, ' */')
            call append(7, 'package main')
            call append(8, '')
            call append(9, 'import "fmt"')
            call append(10, '')
            call append(11, 'func main() {')
            call append(12, '    fmt.Println("vim-go")')
            call append(13, '}')
       elseif expand("%:e") == 'py'
            call setline(1, '#!/usr/bin/python3')
            call append(1, '"""')
            call append(2, '#      Filename: '.expand("%"))
            call append(3, '#        Author: Zhaohui Mei<mzh.whut@gmail.com>')
            call append(4, '#   Description:      ')
            call append(5, '#   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(6, '# Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(7, '"""')
            call append(8, '')
            call append(9, '')
            call append(10, '')
        elseif expand("%:e") == 'sh'
            call setline(1, '#!/bin/bash')
            call append(1, '##################################################')
            call append(2, '#      Filename: '.expand("%"))
            call append(3, '#        Author: Zhaohui Mei<mzh.whut@gmail.com>')
            call append(4, '#   Description:      ')
            call append(5, '#   Create Time: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(6, '# Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
            call append(7, '##################################################')
            call append(8, '')
            call append(9, '')
            call append(10, '')
            endif
    endfunc
    "SET Comment END
" 文件头注释 }


    "SET Last Modified Time START
    func DataInsert()
        if expand("%:e") == 'c' || expand("%:e") == 'go'
            call cursor(6, 1)
            if search ('Last Modified') != 0
                let line = line('.')
                call setline(line, ' * Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
            endif
        elseif expand("%:e") == 'py' || expand("%:e") == 'sh'
            call cursor(7, 1)
            if search ('Last Modified') != 0
                let line = line('.')
                call setline(line, '# Last Modified: '.strftime("%Y-%m-%d %H:%M:%S"))
            endif
        endif
    endfunc
    autocmd FileWritePre,BufWritePre *.c,*.py,*.go,*.sh ks|call DataInsert() |'s
    "SET Last Modified Time END

    " refer:https://blog.csdn.net/qq844352155/article/details/50513072
"  }

" 代码格式化 {
    " c代码格式化配置
    "normal模式下，ctrl+k将格式化一行代码
    "visual模式下，ctrl+k将格式化选中代码
    "insert模式下，ctrl+k将格式化一行代码
    map <C-K> :pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
    imap <C-K> <c-o>:pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py<cr>
    function! Formatonsave()
      let l:formatdiff = 1
      pyf /usr/local/Cellar/clang-format/2019-05-14/share/clang/clang-format.py
    endfunction
    autocmd BufWritePre *.h,*.cc,*.cpp,*.c call Formatonsave()
"  }




" 参考 VIM自动加载
" https://yianwillis.github.io/vimcdoc/doc/quickref.html#option-list
" https://www.w3cschool.cn/vim/xenarozt.html
" 检查不同文件类型，设置不同的tab宽度
autocmd FileType c set tabstop=4
autocmd FileType html set tabstop=2
autocmd FileType html set softtabstop=2 |set tabstop=2 |set shiftwidth=2

"在return前面自动插入一个空行
function AddOneLineBeforeReturn()
    " 获取最后一行行号
    let l = line("$")
    for linenum in range(1,l)
        let match = search(' *return ', 'W', n_num)
        let n_num = linenum + 1
        call cursor(n_num, 1)
        let match = search(' *return ', 'W', n_num)
        if match != 0
            call cursor(linenum, 1)
            call append(linenum, '')
        endif

    endfor
endfunction
" 将整个缓冲区写入文件时，调用以上函数
autocmd BufWritePre *.cpp,*.c call AddOneLineBeforeReturn()
```

## 20. Git仓库管理忽略 DS_Store 文件

作为一名使用Mac的开发者，在日常开发过程中，经常会使用Git来对代码文件夹进行版本控制。而在默认情况下，Git会把 DS_Store 文件带入版本控制的范围内。所以，可以手动将其加入 Git 的版本管理忽略列表。

1. 将 . DS_Store 加入全局的 .gitignore 文件，执行命令：

```sh
echo .DS_Store >> ~/.gitignore_global
```

2. 将这个全局的 .gitignore 文件加入Git的全局config文件中，执行命令：

```sh
git config --global core.excludesfile ~/.gitignore_global
```

哦了，.DS_Store 再也不会出现在你项目的Git代码仓库中了！

参考：[https://zhuanlan.zhihu.com/p/439868892](https://zhuanlan.zhihu.com/p/439868892)

DS_Store，英文全称是 Desktop Services Store（桌面服务存储），开头的 DS 是 Desktop Services（桌面服务） 的缩写。它是一种由macOS系统自动创建的隐藏文件，存在于每一个用「访达」打开过的文件夹下面。

DS_Store 文件的主要作用，是存储当前文件夹在桌面显示相关方面的一些自定义属性，包括文件图标的位置、文件夹上次打开时窗口的大小、展现形式和位置等。这有助于保留为特定文件夹配置的设置，例如，将桌面文件夹设置为查看按名称排序的图标，同时将下载文件夹配置为将文件显示为列表并按日期排序，最近修改的先显示。


## 21. iterm2快捷命令

iTerm2 常用快捷键：
- ⌘(command) + t 新建tab页
- ⌘(command) + d 水平分屏
- ⌘(command) + ⇧(shift) + d 纵向分屏
- ⌘(command) + ⇧(shift) + i 同时向所有终端输入命令
- ⌘(command) + 左右方向键 切换标签
- ⌘(command) + n 新建窗口
- ⌘(command) + w 关闭窗口
- ⌘(command) + Enter 全屏，再按一次关闭全屏
- ⌘(command) + 数字 切换标签
- ⌃(control) + u 删除当前光标前的字符
- ⌃(control) + l 清屏
