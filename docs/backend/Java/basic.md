# Java开发环境配置

[[toc]]

## 1. java编程环境配置

### 1.1 windows jdk环境安装配置

- JDK是Java开发工具包，JDK包含JRE，JRE包含JVM和基础类库。

- 可以去Oracle官方下载 jdk 1.8 [https://www.oracle.com/java/technologies/downloads/#java8-windows](https://www.oracle.com/java/technologies/downloads/#java8-windows) 。

- Oracle官方下载需要注册账号登陆后才能下载。

- 安装可参考 [JDK8.0的下载、安装、配置环境变量](https://www.bilibili.com/read/cv24353732)。需要注意以下几点：

  - Java安装时，不用选择【 公共JRE】，因为JDK中包含JRE。
  - 安装路径设置在`D:\ProgramFiles\Java\jdk-1.8`,不要直接安装到C盘。
  - 安装完成后，设置环境变量`JAVA_HOME`值为`D:\ProgramFiles\Java\jdk-1.8`。
  - 并将`D:\ProgramFiles\Java\jdk-1.8\bin`加入到Path环境变量中。

完成以上配置后，在命令行输入`java -version`，如果能够正常输出以下信息，则说明Java环境配置正常。

```sh
$ java -version
java version "1.8.0_401"
Java(TM) SE Runtime Environment (build 1.8.0_401-b10)
Java HotSpot(TM) 64-Bit Server VM (build 25.401-b10, mixed mode)
```

### 1.2 vscode配置java环境

#### 1.2.1 安装插件

vscode中安装以下三个插件：

- Extension Pack for Java
- Debugger for Java
- Language support for Java ™ for Visual Studio Code

#### 1.2.2 修改配置

使用快捷键Ctrl+Shift+P， 打开用户setting页面: 

```json
    // 字体大小
    "editor.fontSize": 14,
    // java环境配置
    "java.configuration.runtimes": [
        {
            "name": "JavaSE-1.8",
            "path": "D:\\ProgramFiles\\Java\\jdk-1.8"
        }
    ],
```

注意，在`editor.fontSize`配置下面增加以上jdk1.8相关的配置。`path`路径里面路径分隔符需要用两个`\`。即`\\`。

![](/img/Snipaste_2024-02-02_22-58-31.png)



#### 1.2.3 验证环境是否成功

使用快捷键Ctrl+Shift+P， 然后输入**java:create java Project**  ，不用全部输入就会显示出来：

![](/img/Snipaste_2024-02-03_19-21-38.png)

然后选择`no build tools`：

![](/img/Snipaste_2024-02-03_19-23-09.png)

在弹出的对话框中选择一个用来存放Java项目的目录：

![](/img/Snipaste_2024-02-03_19-22-29.png)

并点击【Select the project location】,在输入框内输入项目名称，**项目名称最好不要有中文或者特殊符号** ，如我输入【demo】:

![](/img/Snipaste_2024-02-03_19-23-59.png)

输入项目名称后，直接按Enter回车，此时会打开一个新的VSCODE窗口：

![](/img/Snipaste_2024-02-03_19-24-31.png)

然后选择`no build tools`：

[](/img/Snipaste_2024-02-02_22-48-24.png)

在弹出的对话框中选择一个用来存放Java项目的目录：

[](/img/Snipaste_2024-02-02_22-49-26.png)

并点击【Select the project location】,在输入框内输入项目名称，**项目名称最好不要有中文或者特殊符号** ，如我输入【demo】:

[](/img/Snipaste_2024-02-02_22-52-22.png)

输入项目名称后，直接按Enter回车，此时会打开一个新的VSCODE窗口：

[](/img/Snipaste_2024-02-02_22-53-31.png)

此时，vsvode自动给创建了项目框架， src下面的java文件就是java代码源文件：

```java
public class App {
    public static void main(String[] args) throws Exception {
        System.out.println("Hello, World!");
    }
}

```

注意`Run|Debug`并不是代码，而是插件的功能按钮，点击它们就可以运行代码。



我们直接点击`Run|Debug`就可以运行代码，以下是点击`Run`运行后的结果：

![](/img/Snipaste_2024-02-03_19-25-54.png)

可以看到，正常输出的`Hello, World!`字符串。



### 1.3 vscode配置maven环境

#### 1.3.1 安装maven

在[maven 3.6.0](https://archive.apache.org/dist/maven/maven-3/3.6.0/binaries/apache-maven-3.6.0-bin.zip) 可以下载需要用的maven安装包。

下载后，将压缩包解压到`D:\ProgramFiles\Java` 目录，此时Maven目录文件如下：

![](/img/Snipaste_2024-02-03_19-26-49.png)

设置环境变量`MAVEN_HOME`值为`D:\ProgramFiles\Java\apache-maven-3.6.0`。

并将`D:\ProgramFiles\Java\apache-maven-3.6.0\bin`加入到Path环境变量中。

然后打开命令行窗口：

```sh
$ mvn --version
Apache Maven 3.6.0 (97c98ec64a1fdfee7767ce5ffb20918da4f719f3; 2018-10-25T02:41:47+08:00)
Maven home: D:\ProgramFiles\Java\apache-maven-3.6.0\bin\..
Java version: 1.8.0_401, vendor: Oracle Corporation, runtime: D:\ProgramFiles\Java\jdk-1.8\jre
Default locale: zh_CN, platform encoding: GBK
OS name: "windows 11", version: "10.0", arch: "amd64", family: "windows"
$
```

输入`mvn --version`能正常看到以上版本信息，则说明maven环境配置正常。



#### 1.3.2 安装插件

vscode中安装以下插件：

- Maven for Java

![](/img/Snipaste_2024-02-03_19-34-45.png)


#### 1.3.3 修改配置

使用快捷键Ctrl+Shift+P， 打开用户setting页面，在vscode配置文件中，增加以下三行内容：

```json
    // maven环境配置
    "maven.executable.path": "D:\\ProgramFiles\\Java\\apache-maven-3.6.0\\bin\\mvn",
    "maven.terminal.useJavaHome": true,
    "maven.settingsFile": "D:\\ProgramFiles\\Java\\apache-maven-3.6.0\\conf\\settings.xml",
```

![](/img/Snipaste_2024-02-03_19-27-50.png)




#### 1.3.4 设置maven加速源

参考阿里云[Maven 配置](https://developer.aliyun.com/mirror/maven?spm=a2c6h.13651102.0.0.3e221b11zarqhG):

> 打开 Maven 的配置文件(windows机器一般在maven安装目录的conf/settings.xml)，在`<mirrors></mirrors>`标签中添加 mirror 子节点:
>
> ```js
> <mirror>
>     <id>aliyunmaven</id>
>     <mirrorOf>*</mirrorOf>
>     <name>阿里云公共仓库</name>
>     <url>https://maven.aliyun.com/repository/public</url>
> </mirror>
> ```

![](/img/Snipaste_2024-02-03_19-29-48.png)

直接在配置文件增加以上几行就行！



#### 1.3.5 创建maven项目

 vscode空白处点击右键选择【从maven原型创建新项目】 ：

![](/img/Snipaste_2024-02-03_19-35-24.png)

 创建项目窗口中可以选择快速创建项目【maven-archetype-quickstart】:

![](/img/Snipaste_2024-02-03_19-35-57.png)

 选择版本 ，选择1.1：

![](/img/Snipaste_2024-02-03_19-36-24.png)

 填写项目的组织，一般是公司域名的倒写，因为我是要测试`nexusapi.com` api接口的，所以我们填写`com.nexusapi` :

![](/img/Snipaste_2024-02-03_19-37-12.png)

然后，按Enter回车，在新的输入框输入项目名称，如我输入【mavendemo】：

![](/img/Snipaste_2024-02-03_19-37-35.png)

然后，按Enter回车,此时让选择项目存放的目录，我们仍然放在之前的java目录下：

![](/img/Snipaste_2024-02-03_19-38-12.png)

并点击【Select Destination Folder】,此时vscode就会自动去下载相关依赖包：

![](/img/Snipaste_2024-02-03_19-38-31.png)

很快就下载完成了，让输入一些相关的信息：

![](/img/Snipaste_2024-02-03_19-39-02.png)

我们直接回车，使用默认的版本信息【1.0-SNAPSHOT】：

[](/img/Snipaste_2024-02-03_00-22-57.png)

 Maven 将要求确认项目细节，按 **Enter** 或按 Y 确认。

此时，可以看到vscode开始创建项目：

![](/img/Snipaste_2024-02-03_19-39-37.png)

创建成功后，按任意键会关闭该终端。

![](/img/Snipaste_2024-02-03_19-40-22.png)

也可以点击右侧的【Add as Workplace Folder】，即添加为工作空间文件夹，点击该处后，vscode上面看到如下视图：

![](/img/Snipaste_2024-02-03_19-42-46.png)

此时，vscode已经打开了刚才创建的mavendemo项目，相关文件已经创建成功了。



如果有新的依赖包需要安装，可以左下角的【MAVEN】--【Run Maven Commands】选项相应命令执行即可：

![](/img/Snipaste_2024-02-03_19-44-16.png)

如果没有新的依赖包需要安装，则可以直接点【运行和调试】的图标，或者按快捷键【Ctrl+Shift+D】 ，然后点击【运行和调试】按钮，vscode则会运行Maven项目代码：

![](/img/Snipaste_2024-02-03_19-45-40.png)


可以看到，正常输出了【Hello World!】和【这是Maven项目输出！】信息，也就是说，vscode里面的maven环境配置成功了。



至此，Java的开发环境就准备好了。



