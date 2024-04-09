# miniconda的使用

[[toc]]



## 1. 概述

- Python最新版本信息，可在Python官网查看 [https://www.python.org/downloads/](https://www.python.org/downloads/) 。
- miniconda与Python最新版本的对应关系，请参考 [Latest Miniconda installer links by Python version](https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/) 。



## 2. 下载和安装miniconda

### 2.1 下载miniconda

在Python官网下载页面 [https://www.python.org/downloads/](https://www.python.org/downloads/) 可以看到当前Python 安全版本是Python 3.10：

![Snipaste_2024-04-09_23-20-46.png](/img/Snipaste_2024-04-09_23-20-46.png)

然后在 [Latest Miniconda installer links by Python version](https://docs.anaconda.com/free/miniconda/miniconda-other-installer-links/) 页面下载Python 3.10版本对应的miniconda：

![Snipaste_2024-04-09_23-24-16.png](/img/Snipaste_2024-04-09_23-24-16.png)

在这个位置可以看到文件的SHA256 哈希值是:  8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78 。

### 2.2 检验miniconda文件

将下载下来的`Miniconda3-py310_24.1.2-0-Linux-x86_64.sh`文件上传到远程Linux服务器root家目录下。

校验文件：

```sh
[root@ansible-node3 ~]# sha256sum Miniconda3-py310_24.1.2-0-Linux-x86_64.sh |grep '8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78'
8eb5999c2f7ac6189690d95ae5ec911032fa6697ae4b34eb3235802086566d78  Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
[root@ansible-node3 ~]#
```

可以看到校验通过，说明文件正常。

### 2.3 配置conda清华大学代理加速

参考[Anaconda 镜像使用帮助](https://mirrors.tuna.tsinghua.edu.cn/help/anaconda/)

创建`~/.condarc`配置文件，并在其中增加以下配置信息：

```yaml
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch-lts: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  deepmodeling: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/

```



### 2.4 安装miniconda

安装minicoda:

```sh
# 查看帮助信息
[root@ansible-node3 ~]# ./Miniconda3-py310_24.1.2-0-Linux-x86_64.sh -h

usage: ./Miniconda3-py310_24.1.2-0-Linux-x86_64.sh [options]

Installs Miniconda3 py310_24.1.2-0

-b           run install in batch mode (without manual intervention),
             it is expected the license terms (if any) are agreed upon
-f           no error if install prefix already exists
-h           print this help message and exit
-p PREFIX    install prefix, defaults to /root/miniconda3, must not contain spaces.
-s           skip running pre/post-link/install scripts
-m           disable the creation of menu items / shortcuts
-u           update an existing installation
-t           run package tests after installation (may install conda-build)

# 将miniconda安装到/srv/miniconda目录下，并且安装过程中不需要手动交互确认
[root@ansible-node3 ~]# ./Miniconda3-py310_24.1.2-0-Linux-x86_64.sh -b -p /srv/miniconda
PREFIX=/srv/miniconda
Unpacking payload ...

Installing base environment...


Downloading and Extracting Packages:


Downloading and Extracting Packages:

Preparing transaction: done
Executing transaction: done
installation finished.

# 可以看到安装完成，查看conda版本信息
[root@ansible-node3 ~]# /srv/miniconda/bin/conda -V
conda 24.1.2

# 查看Python版本信息
[root@ansible-node3 ~]# /srv/miniconda/bin/python -V
Python 3.10.13

# 查看Python文件
[root@ansible-node3 ~]# ls -lah /srv/miniconda/bin/python*
lrwxrwxrwx 1 root root   10 Apr  9 22:12 /srv/miniconda/bin/python -> python3.10
lrwxrwxrwx 1 root root   10 Apr  9 22:12 /srv/miniconda/bin/python3 -> python3.10
lrwxrwxrwx 1 root root   10 Apr  9 22:12 /srv/miniconda/bin/python3.1 -> python3.10
-rwxr-xr-x 1 root root  17M Apr  9 22:12 /srv/miniconda/bin/python3.10
-rwxr-xr-x 1 root root 3.4K Apr  9 22:12 /srv/miniconda/bin/python3.10-config
lrwxrwxrwx 1 root root   17 Apr  9 22:12 /srv/miniconda/bin/python3-config -> python3.10-config
[root@ansible-node3 ~]#
```

至此安全的高版本Python 3.10.13安装成功了！



## 3. 创建虚拟环境

### 3.1 创建虚拟环境

使用`/srv/miniconda/bin/conda create`创建虚拟环境：

```sh
[root@ansible-node3 ~]# /srv/miniconda/bin/conda create --name supervisorpython31013 python=3.10.13
Channels:
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: /srv/miniconda/envs/supervisorpython31013

  added / updated specs:
    - python=3.10.13


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    _libgcc_mutex-0.1          |             main           3 KB  defaults
    _openmp_mutex-5.1          |            1_gnu          21 KB  defaults
    bzip2-1.0.8                |       h5eee18b_5         262 KB  defaults
    ca-certificates-2024.3.11  |       h06a4308_0         127 KB  defaults
    ld_impl_linux-64-2.38      |       h1181459_1         654 KB  defaults
    libffi-3.4.4               |       h6a678d5_0         142 KB  defaults
    libgcc-ng-11.2.0           |       h1234567_1         5.3 MB  defaults
    libgomp-11.2.0             |       h1234567_1         474 KB  defaults
    libstdcxx-ng-11.2.0        |       h1234567_1         4.7 MB  defaults
    libuuid-1.41.5             |       h5eee18b_0          27 KB  defaults
    ncurses-6.4                |       h6a678d5_0         914 KB  defaults
    openssl-3.0.13             |       h7f8727e_0         5.2 MB  defaults
    pip-23.3.1                 |  py310h06a4308_0         2.7 MB  defaults
    python-3.10.13             |       h955ad1f_0        26.8 MB  defaults
    readline-8.2               |       h5eee18b_0         357 KB  defaults
    setuptools-68.2.2          |  py310h06a4308_0         957 KB  defaults
    sqlite-3.41.2              |       h5eee18b_0         1.2 MB  defaults
    tk-8.6.12                  |       h1ccaba5_0         3.0 MB  defaults
    tzdata-2024a               |       h04d1e81_0         116 KB  defaults
    wheel-0.41.2               |  py310h06a4308_0         109 KB  defaults
    xz-5.4.6                   |       h5eee18b_0         651 KB  defaults
    zlib-1.2.13                |       h5eee18b_0         103 KB  defaults
    ------------------------------------------------------------
                                           Total:        53.7 MB

The following NEW packages will be INSTALLED:

  _libgcc_mutex      anaconda/pkgs/main/linux-64::_libgcc_mutex-0.1-main
  _openmp_mutex      anaconda/pkgs/main/linux-64::_openmp_mutex-5.1-1_gnu
  bzip2              anaconda/pkgs/main/linux-64::bzip2-1.0.8-h5eee18b_5
  ca-certificates    anaconda/pkgs/main/linux-64::ca-certificates-2024.3.11-h06a4308_0
  ld_impl_linux-64   anaconda/pkgs/main/linux-64::ld_impl_linux-64-2.38-h1181459_1
  libffi             anaconda/pkgs/main/linux-64::libffi-3.4.4-h6a678d5_0
  libgcc-ng          anaconda/pkgs/main/linux-64::libgcc-ng-11.2.0-h1234567_1
  libgomp            anaconda/pkgs/main/linux-64::libgomp-11.2.0-h1234567_1
  libstdcxx-ng       anaconda/pkgs/main/linux-64::libstdcxx-ng-11.2.0-h1234567_1
  libuuid            anaconda/pkgs/main/linux-64::libuuid-1.41.5-h5eee18b_0
  ncurses            anaconda/pkgs/main/linux-64::ncurses-6.4-h6a678d5_0
  openssl            anaconda/pkgs/main/linux-64::openssl-3.0.13-h7f8727e_0
  pip                anaconda/pkgs/main/linux-64::pip-23.3.1-py310h06a4308_0
  python             anaconda/pkgs/main/linux-64::python-3.10.13-h955ad1f_0
  readline           anaconda/pkgs/main/linux-64::readline-8.2-h5eee18b_0
  setuptools         anaconda/pkgs/main/linux-64::setuptools-68.2.2-py310h06a4308_0
  sqlite             anaconda/pkgs/main/linux-64::sqlite-3.41.2-h5eee18b_0
  tk                 anaconda/pkgs/main/linux-64::tk-8.6.12-h1ccaba5_0
  tzdata             anaconda/pkgs/main/noarch::tzdata-2024a-h04d1e81_0
  wheel              anaconda/pkgs/main/linux-64::wheel-0.41.2-py310h06a4308_0
  xz                 anaconda/pkgs/main/linux-64::xz-5.4.6-h5eee18b_0
  zlib               anaconda/pkgs/main/linux-64::zlib-1.2.13-h5eee18b_0


Proceed ([y]/n)? y


Downloading and Extracting Packages:

Preparing transaction: done
Verifying transaction: done
Executing transaction: done
#
# To activate this environment, use
#
#     $ conda activate supervisorpython31013
#
# To deactivate an active environment, use
#
#     $ conda deactivate

[root@ansible-node3 ~]# 
```

创建完成后，查看虚拟环境：

```sh
[root@ansible-node3 ~]# /srv/miniconda/bin/conda env
usage: conda env [-h] command ...

positional arguments:
  command
    config    Configure a conda environment.
    create    Create an environment based on an environment definition file.
    export    Export a given environment
    list      List the Conda environments.
    remove    Remove an environment.
    update    Update the current environment based on environment file.

options:
  -h, --help  Show this help message and exit.
[root@ansible-node3 ~]# /srv/miniconda/bin/conda env list
# conda environments:
#
base                     /srv/miniconda
supervisorpython31013     /srv/miniconda/envs/supervisorpython31013

[root@ansible-node3 ~]#  /srv/miniconda/envs/supervisorpython31013/bin/python -V
Python 3.10.13
```

这样虚拟环境`supervisorpython31013`就创建成功了。



### 3.2 在虚拟环境中安装第三方包

注意，如果直接使用conda安装Python第三方包，有可能导致conda将Python版本也给升级了，为了保持Python版本不变，我们仍然使用pip来安装第三方包。如安装supervisor包，则使用以下命令：

```sh
[root@ansible-node3 ~]# /srv/miniconda/envs/supervisorpython31013/bin/pip install supervisor
Looking in indexes: http://mirrors.aliyun.com/pypi/simple/
Collecting supervisor
  Downloading http://mirrors.aliyun.com/pypi/packages/2c/7a/0ad3973941590c040475046fef37a2b08a76691e61aa59540828ee235a6e/supervisor-4.2.5-py2.py3-none-any.whl (319 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 319.6/319.6 kB 505.6 kB/s eta 0:00:00
Requirement already satisfied: setuptools in /srv/miniconda/envs/supervisorpython31013/lib/python3.10/site-packages (from supervisor) (68.2.2)
Installing collected packages: supervisor
Successfully installed supervisor-4.2.5
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
[root@ansible-node3 ~]# /srv/miniconda/envs/supervisorpython31013/bin/pip list
Package    Version
---------- -------
pip        23.3.1
setuptools 68.2.2
supervisor 4.2.5
wheel      0.41.2
[root@ansible-node3 ~]#  
```

