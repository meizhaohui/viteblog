# svn Docs

[[toc]]

- svn官网地址： [Apache Subversion](https://subversion.apache.org/)

## 1. 安装

## 1.1 服务端安装

可参考 [Apache Subversion Binary Packages](https://subversion.apache.org/packages.html) 进行安装。

也可以在 [https://www.wandisco.com/source-code-management/subversion](https://www.wandisco.com/source-code-management/subversion) 页面下载自动化安装程序：

![](/img/Snipaste_2022-09-14_21-22-21.png) 然后一键安装。



我们的系统信息：

```sh
root@4144e8c22fff:~# cat /etc/issue
Ubuntu 20.04.2 LTS \n \l
```

官网帮助信息：

> Ubuntu Linux [¶](https://subversion.apache.org/packages.html#ubuntu)
>
> - [Ubuntu Packages](https://packages.ubuntu.com/search?keywords=subversion&exact=1) (maintained by [Ubuntu Project](https://lists.ubuntu.com/mailman/listinfo/ubuntu-devel-discuss); client and server; svnserve is part of the *subversion* package, mod_dav_svn is in the separate *libapache2-svn* package)
>
>     ```
>     $ apt-get install subversion
>     $ apt-get install libapache2-svn
>     ```
>
> - [WANdisco](https://www.wandisco.com/subversion/download#ubuntu) (supported and certified by [WANdisco](https://www.wandisco.com/subversion/); *requires registration*)

我们直接使用`apt`方式进行安装。

```sh
root@4144e8c22fff:~# apt search subversion
Sorting... Done
Full Text Search... Done
hgsubversion/focal 1.9.3+git20190419+6a6ce-3ubuntu2 all
  Subversion client as Mercurial extension

kdesvn/focal 2.1.0-1build1 amd64
  Subversion client with tight KDE integration

kdesvn-kio-plugins/focal 2.1.0-1build1 amd64
  Subversion I/O slaves for KDE

libapache2-mod-svn/focal 1.13.0-3 amd64
  Apache Subversion server modules for Apache httpd

libnb-svnclientadapter-java/focal 6.7-0ubuntu2 all
  High-level Java API to subversion

libnb-svnclientadapter-java-doc/focal 6.7-0ubuntu2 all
  High-level Java API to subversion javadoc

libsvn-class-perl/focal 0.18-2 all
  perl object oriented interface for Subversion workspaces

libsvn-dev/focal 1.13.0-3 amd64
  Development files for Apache Subversion libraries

libsvn-dump-perl/focal 0.07-1 all
  module for parsing Subversion dumps

libsvn-hooks-perl/focal 1.34-2 all
  framework for implementing Subversion hooks

libsvn-java/focal 1.13.0-3 amd64
  Java bindings for Apache Subversion

libsvn-notify-perl/focal 2.87-1 all
  Subversion activity notification

libsvn-perl/focal 1.13.0-3 amd64
  Perl bindings for Apache Subversion

libsvn-svnlook-perl/focal 0.04-3 all
  module to aid using svnlook in Subversion hooks

libsvn-web-perl/focal 0.63-3 all
  Subversion repository web frontend

libsvn1/focal 1.13.0-3 amd64
  Shared libraries used by Apache Subversion

libsvnclientadapter-java/focal 1.10.12-1 all
  High-level Java API for Subversion (library)

libsvnclientadapter-java-doc/focal 1.10.12-1 all
  High-level Java API for Subversion (documentation)

libsvnkit-java/focal 1.8.14-4 all
  pure Java Subversion client library

lua-svn/focal 0.4.0-9.1 amd64
  Subversion library for the Lua language

lua-svn-dev/focal 0.4.0-9.1 amd64
  Development files for the Subversion library for the Lua language

nautilus-script-collection-svn/focal 0.9.2-0ubuntu3 all
  Nautilus subversion management scripts

python-subversion/focal 1.13.0-3 amd64
  Python bindings for Apache Subversion

python-subvertpy/focal 0.11.0~git20191228+2423bf1-2ubuntu1 amd64
  Alternative Python bindings for Subversion - Python 2

python3-subvertpy/focal 0.11.0~git20191228+2423bf1-2ubuntu1 amd64
  Alternative Python bindings for Subversion - Python 3

python3-svn/focal 1.9.9-2.1build1 amd64
  A(nother) Python 3 interface to Subversion

ruby-svn/focal 1.13.0-3 amd64
  Ruby bindings for Apache Subversion

subversion/focal 1.13.0-3 amd64
  Advanced version control system

subversion-tools/focal 1.13.0-3 amd64
  Assorted tools related to Apache Subversion

svn-all-fast-export/focal 1.0.16+git20190806-1build1 amd64
  fast-import based converter to convert repos from Subversion to git

svn-buildpackage/focal 0.8.7 all
  helper programs to maintain Debian packages with Subversion

svn-load/focal 1.6-1 all
  Enhanced import facility for Subversion

svn2cl/focal 0.14-2 all
  Generate a GNU-style ChangeLog from Subversion repository history

svnkit/focal 1.8.14-4 all
  pure Java Subversion client

tkcvs/focal 8.2.3-1.2 all
  Graphical front-end to CVS and Subversion

root@4144e8c22fff:~#
```

查看subversion包详情：
```sh
root@4144e8c22fff:~# apt show subversion/focal
Package: subversion
Version: 1.13.0-3
Priority: optional
Section: universe/devel
Origin: Ubuntu
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Original-Maintainer: James McCoy <jamessan@debian.org>
Bugs: https://bugs.launchpad.net/ubuntu/+filebug
Installed-Size: 4901 kB
Depends: libsvn1 (= 1.13.0-3), libapr1 (>= 1.5.0), libaprutil1 (>= 1.3.2+dfsg), libc6 (>= 2.4)
Suggests: db5.3-util, libapache2-mod-svn, patch, subversion-tools
Homepage: http://subversion.apache.org/
Download-Size: 824 kB
APT-Manual-Installed: yes
APT-Sources: http://mirrors.aliyun.com/ubuntu focal/universe amd64 Packages
Description: Advanced version control system

root@4144e8c22fff:~#
```

安装相关包和subversion:
```sh
root@4144e8c22fff:~# apt-get install db5.3-util libapache2-mod-svn patch  subversion subversion-tools -y
Reading package lists... Done
Building dependency tree
Reading state information... Done
libapache2-mod-svn is already the newest version (1.13.0-3).
The following additional packages will be installed:
  cpio libconfig-inifiles-perl libpopt0 libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib libsvn-perl liburi-perl postfix python-subversion python2
  python2-minimal python2.7 python2.7-minimal rsync ssl-cert subversion
Suggested packages:
  libarchive1 libwww-perl ed diffutils-doc procmail postfix-mysql postfix-pgsql postfix-ldap postfix-pcre postfix-lmdb postfix-sqlite sasl2-bin | dovecot-common
  resolvconf postfix-cdb mail-reader postfix-doc python2-doc python-tk python2.7-doc binutils binfmt-support openssh-server openssl-blacklist ruby-svn svn2cl
The following NEW packages will be installed:
  cpio db5.3-util libconfig-inifiles-perl libpopt0 libpython2-stdlib libpython2.7-minimal libpython2.7-stdlib libsvn-perl liburi-perl patch postfix
  python-subversion python2 python2-minimal python2.7 python2.7-minimal rsync ssl-cert subversion subversion-tools
0 upgraded, 20 newly installed, 0 to remove and 0 not upgraded.
Need to get 8332 kB of archives.
After this operation, 40.0 MB of additional disk space will be used.
Get:1 http://mirrors.aliyun.com/ubuntu focal/main amd64 libpopt0 amd64 1.16-14 [26.3 kB]
Get:2 http://mirrors.aliyun.com/ubuntu focal/main amd64 rsync amd64 3.1.3-8 [322 kB]
Get:3 http://mirrors.aliyun.com/ubuntu focal-security/universe amd64 libpython2.7-minimal amd64 2.7.18-1~20.04.1 [335 kB]
Get:4 http://mirrors.aliyun.com/ubuntu focal-security/universe amd64 python2.7-minimal amd64 2.7.18-1~20.04.1 [1285 kB]
Get:5 http://mirrors.aliyun.com/ubuntu focal/universe amd64 python2-minimal amd64 2.7.17-2ubuntu4 [27.5 kB]
Get:6 http://mirrors.aliyun.com/ubuntu focal-security/universe amd64 libpython2.7-stdlib amd64 2.7.18-1~20.04.1 [1887 kB]
Get:7 http://mirrors.aliyun.com/ubuntu focal-security/universe amd64 python2.7 amd64 2.7.18-1~20.04.1 [248 kB]
Get:8 http://mirrors.aliyun.com/ubuntu focal/universe amd64 libpython2-stdlib amd64 2.7.17-2ubuntu4 [7072 B]
Get:9 http://mirrors.aliyun.com/ubuntu focal/universe amd64 python2 amd64 2.7.17-2ubuntu4 [26.5 kB]
Get:10 http://mirrors.aliyun.com/ubuntu focal/main amd64 cpio amd64 2.13+dfsg-2 [86.0 kB]
Get:11 http://mirrors.aliyun.com/ubuntu focal/main amd64 db5.3-util amd64 5.3.28+dfsg1-0.6ubuntu2 [65.3 kB]
Get:12 http://mirrors.aliyun.com/ubuntu focal/universe amd64 libsvn-perl amd64 1.13.0-3 [937 kB]
Get:13 http://mirrors.aliyun.com/ubuntu focal/main amd64 liburi-perl all 1.76-2 [77.5 kB]
Get:14 http://mirrors.aliyun.com/ubuntu focal/main amd64 patch amd64 2.7.6-6 [105 kB]
Get:15 http://mirrors.aliyun.com/ubuntu focal/main amd64 ssl-cert all 1.0.39 [17.0 kB]
Get:16 http://mirrors.aliyun.com/ubuntu focal-updates/main amd64 postfix amd64 3.4.13-0ubuntu1 [1198 kB]
Get:17 http://mirrors.aliyun.com/ubuntu focal/universe amd64 python-subversion amd64 1.13.0-3 [617 kB]
Get:18 http://mirrors.aliyun.com/ubuntu focal/universe amd64 subversion amd64 1.13.0-3 [824 kB]
Get:19 http://mirrors.aliyun.com/ubuntu focal/main amd64 libconfig-inifiles-perl all 3.000002-1 [40.6 kB]
Get:20 http://mirrors.aliyun.com/ubuntu focal/universe amd64 subversion-tools amd64 1.13.0-3 [201 kB]
Fetched 8332 kB in 9s (967 kB/s)
debconf: delaying package configuration, since apt-utils is not installed
Selecting previously unselected package libpopt0:amd64.
(Reading database ... 14345 files and directories currently installed.)
Preparing to unpack .../0-libpopt0_1.16-14_amd64.deb ...
Unpacking libpopt0:amd64 (1.16-14) ...
Selecting previously unselected package rsync.
Preparing to unpack .../1-rsync_3.1.3-8_amd64.deb ...
Unpacking rsync (3.1.3-8) ...
Selecting previously unselected package libpython2.7-minimal:amd64.
Preparing to unpack .../2-libpython2.7-minimal_2.7.18-1~20.04.1_amd64.deb ...
Unpacking libpython2.7-minimal:amd64 (2.7.18-1~20.04.1) ...
Selecting previously unselected package python2.7-minimal.
Preparing to unpack .../3-python2.7-minimal_2.7.18-1~20.04.1_amd64.deb ...
Unpacking python2.7-minimal (2.7.18-1~20.04.1) ...
Selecting previously unselected package python2-minimal.
Preparing to unpack .../4-python2-minimal_2.7.17-2ubuntu4_amd64.deb ...
Unpacking python2-minimal (2.7.17-2ubuntu4) ...
Selecting previously unselected package libpython2.7-stdlib:amd64.
Preparing to unpack .../5-libpython2.7-stdlib_2.7.18-1~20.04.1_amd64.deb ...
Unpacking libpython2.7-stdlib:amd64 (2.7.18-1~20.04.1) ...
Selecting previously unselected package python2.7.
Preparing to unpack .../6-python2.7_2.7.18-1~20.04.1_amd64.deb ...
Unpacking python2.7 (2.7.18-1~20.04.1) ...
Selecting previously unselected package libpython2-stdlib:amd64.
Preparing to unpack .../7-libpython2-stdlib_2.7.17-2ubuntu4_amd64.deb ...
Unpacking libpython2-stdlib:amd64 (2.7.17-2ubuntu4) ...
Setting up libpython2.7-minimal:amd64 (2.7.18-1~20.04.1) ...
Setting up python2.7-minimal (2.7.18-1~20.04.1) ...
Linking and byte-compiling packages for runtime python2.7...
Setting up python2-minimal (2.7.17-2ubuntu4) ...
Selecting previously unselected package python2.
(Reading database ... 15130 files and directories currently installed.)
Preparing to unpack .../00-python2_2.7.17-2ubuntu4_amd64.deb ...
Unpacking python2 (2.7.17-2ubuntu4) ...
Selecting previously unselected package cpio.
Preparing to unpack .../01-cpio_2.13+dfsg-2_amd64.deb ...
Unpacking cpio (2.13+dfsg-2) ...
Selecting previously unselected package db5.3-util.
Preparing to unpack .../02-db5.3-util_5.3.28+dfsg1-0.6ubuntu2_amd64.deb ...
Unpacking db5.3-util (5.3.28+dfsg1-0.6ubuntu2) ...
Selecting previously unselected package libsvn-perl:amd64.
Preparing to unpack .../03-libsvn-perl_1.13.0-3_amd64.deb ...
Unpacking libsvn-perl:amd64 (1.13.0-3) ...
Selecting previously unselected package liburi-perl.
Preparing to unpack .../04-liburi-perl_1.76-2_all.deb ...
Unpacking liburi-perl (1.76-2) ...
Selecting previously unselected package patch.
Preparing to unpack .../05-patch_2.7.6-6_amd64.deb ...
Unpacking patch (2.7.6-6) ...
Selecting previously unselected package ssl-cert.
Preparing to unpack .../06-ssl-cert_1.0.39_all.deb ...
Unpacking ssl-cert (1.0.39) ...
Selecting previously unselected package postfix.
Preparing to unpack .../07-postfix_3.4.13-0ubuntu1_amd64.deb ...
debconf: unable to initialize frontend: Dialog
debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 76.)
debconf: falling back to frontend: Readline
Postfix Configuration
---------------------

Please select the mail server configuration type that best meets your needs.

 No configuration:
  Should be chosen to leave the current configuration unchanged.
 Internet site:
  Mail is sent and received directly using SMTP.
 Internet with smarthost:
  Mail is received directly using SMTP or by running a utility such
  as fetchmail. Outgoing mail is sent using a smarthost.
 Satellite system:
  All mail is sent to another machine, called a 'smarthost', for delivery.
 Local only:
  The only delivered mail is the mail for local users. There is no network.

  1. No configuration  2. Internet Site  3. Internet with smarthost  4. Satellite system  5. Local only
General type of mail configuration: 1         #<------- 注意，此处选择1，无邮件服务器配置

Unpacking postfix (3.4.13-0ubuntu1) ...
Selecting previously unselected package python-subversion.
Preparing to unpack .../08-python-subversion_1.13.0-3_amd64.deb ...
Unpacking python-subversion (1.13.0-3) ...
Selecting previously unselected package subversion.
Preparing to unpack .../09-subversion_1.13.0-3_amd64.deb ...
Unpacking subversion (1.13.0-3) ...
Selecting previously unselected package libconfig-inifiles-perl.
Preparing to unpack .../10-libconfig-inifiles-perl_3.000002-1_all.deb ...
Unpacking libconfig-inifiles-perl (3.000002-1) ...
Selecting previously unselected package subversion-tools.
Preparing to unpack .../11-subversion-tools_1.13.0-3_amd64.deb ...
Unpacking subversion-tools (1.13.0-3) ...
Setting up libconfig-inifiles-perl (3.000002-1) ...
Setting up cpio (2.13+dfsg-2) ...
update-alternatives: using /bin/mt-gnu to provide /bin/mt (mt) in auto mode
Setting up libsvn-perl:amd64 (1.13.0-3) ...
Setting up subversion (1.13.0-3) ...
Setting up libpython2.7-stdlib:amd64 (2.7.18-1~20.04.1) ...
Setting up ssl-cert (1.0.39) ...
debconf: unable to initialize frontend: Dialog
debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 76.)
debconf: falling back to frontend: Readline
Setting up db5.3-util (5.3.28+dfsg1-0.6ubuntu2) ...
Setting up patch (2.7.6-6) ...
Setting up postfix (3.4.13-0ubuntu1) ...
debconf: unable to initialize frontend: Dialog
debconf: (No usable dialog-like program is installed, so the dialog based frontend cannot be used. at /usr/share/perl5/Debconf/FrontEnd/Dialog.pm line 76.)
debconf: falling back to frontend: Readline
Adding group `postfix' (GID 103) ...
Done.
Adding system user `postfix' (UID 101) ...
Adding new user `postfix' (UID 101) with group `postfix' ...
Not creating home directory `/var/spool/postfix'.
Creating /etc/postfix/dynamicmaps.cf
Adding group `postdrop' (GID 104) ...
Done.
/etc/aliases does not exist, creating it.

Postfix (main.cf) was not set up.  Start with
  cp /usr/share/postfix/main.cf.debian /etc/postfix/main.cf
.  If you need to make changes, edit /etc/postfix/main.cf (and others) as
needed.  To view Postfix configuration values, see postconf(1).

After modifying main.cf, be sure to run 'systemctl reload postfix'.

invoke-rc.d: could not determine current runlevel
invoke-rc.d: policy-rc.d denied execution of start.
Setting up liburi-perl (1.76-2) ...
Setting up libpopt0:amd64 (1.16-14) ...
Setting up python2.7 (2.7.18-1~20.04.1) ...
Setting up libpython2-stdlib:amd64 (2.7.17-2ubuntu4) ...
Setting up subversion-tools (1.13.0-3) ...
Setting up python2 (2.7.17-2ubuntu4) ...
Setting up python-subversion (1.13.0-3) ...
Setting up rsync (3.1.3-8) ...
invoke-rc.d: could not determine current runlevel
invoke-rc.d: policy-rc.d denied execution of start.
Processing triggers for libc-bin (2.31-0ubuntu9.2) ...
Processing triggers for ufw (0.36-6) ...
Processing triggers for man-db (2.9.1-1) ...
Processing triggers for mime-support (3.64ubuntu1) ...
root@4144e8c22fff:~#
```


查看刚才安装的包列表信息：
```sh
root@4144e8c22fff:~# dpkg -l  db5.3-util  libapache2-mod-svn  patch  subversion-tools subversion
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name               Version                 Architecture Description
+++-==================-=======================-============-=================================================
ii  db5.3-util         5.3.28+dfsg1-0.6ubuntu2 amd64        Berkeley v5.3 Database Utilities
ii  libapache2-mod-svn 1.13.0-3                amd64        Apache Subversion server modules for Apache httpd
ii  patch              2.7.6-6                 amd64        Apply a diff file to an original
ii  subversion         1.13.0-3                amd64        Advanced version control system
ii  subversion-tools   1.13.0-3                amd64        Assorted tools related to Apache Subversion
root@4144e8c22fff:~#
```
可以看到，以上各包都安装成功了。



一般我们是将SVN系统安装在Linux操作系统上面，也可以安装到MacOS或Windows系统上。可参考官方文档。

MacOS系统：

> Mac OS X [¶](https://subversion.apache.org/packages.html#osx)
>
>- An old version of Subversion is shipped with MacOS X. See the [open source section of Apple's web site](https://www.apple.com/opensource/) for more information.
>
>- [Fink](https://pdb.finkproject.org/pdb/package.php/svn) (requires [Fink](https://www.finkproject.org/))
>
>- [Homebrew](https://brew.sh/)
>
>    ```
>    $ brew options subversion
>    $ brew install (OPTIONS) subversion
>    ```
>
>- [MacPorts](https://www.macports.org/ports.php?by=name&substr=subversion) (requires [MacPorts](https://www.macports.org/))
>
>- [WANdisco](https://www.wandisco.com/subversion/download#osx) (client and server; supported and certified by [WANdisco](https://www.wandisco.com/subversion/); *requires registration*)

如果brew安装失败，可以在Wandisco源中下载安装包，下载地址：[http://opensource.wandisco.com/osx/1.11/1.11.1/](http://opensource.wandisco.com/osx/1.11/1.11.1/)

```sh
# 下载服务端
$ wget http://opensource.wandisco.com/osx/1.11/1.11.1/Subversion-1.11.1_10.14.x.pkg
# 下载客户端
$ wget http://opensource.wandisco.com/osx/1.11/1.11.1/Subversion-Client-1.11.1_10.14.x.pkg
```

下载完成后双击安装即可。安装完成后，执行`export PATH=/opt/subversion/bin:$PATH`，将`/opt/subversion/bin`加入到环境变量中即可。



Windows系统：

> Windows [¶](https://subversion.apache.org/packages.html#windows)
>
>- [CollabNet](https://www.collab.net/downloads/subversion/) (supported and certified by [CollabNet](https://www.collab.net/subversion); *requires registration*)
>- [SlikSVN](https://www.sliksvn.com/en/download) (32- and 64-bit client MSI; maintained by [Bert Huijben](mailto:rhuijben@open.collab.net), [SharpSvn project](https://sharpsvn.open.collab.net/))
>- [TortoiseSVN](https://tortoisesvn.net/downloads/) (optionally installs 32- and 64-bit command line tools and svnserve; supported and maintained by the [TortoiseSVN project](https://tortoisesvn.net/))
>- [VisualSVN](https://www.visualsvn.com/downloads/) (32- and 64-bit client and server; supported and maintained by [VisualSVN](https://www.visualsvn.com/))
>- [WANdisco](https://www.wandisco.com/subversion/download#windows) (32- and 64-bit client and server; supported and certified by [WANdisco](https://www.wandisco.com/subversion/); *requires registration*)

可以直接在Wandisco源下载安装包：[http://opensource.wandisco.com/Windows/1.14/](http://opensource.wandisco.com/Windows/1.14/)

## 1.2 客户端安装

一般在Linux系统安装服务端时会自动安装客户端`svn`工具。在Windows系统上面，可以去 [https://tortoisesvn.net/downloads.zh.html](https://tortoisesvn.net/downloads.zh.html) 下载TortoiseSVN客户端安装使用。



## 2. svn命令行初步使用

- 查看svn帮助信息

```
root@4144e8c22fff:~# svn
Type 'svn help' for usage.
root@4144e8c22fff:~# svn --help
usage: svn <subcommand> [options] [args]
Subversion command-line client.
Type 'svn help <subcommand>' for help on a specific subcommand.
Type 'svn --version' to see the program version and RA modules,
     'svn --version --verbose' to see dependency versions as well,
     'svn --version --quiet' to see just the version number.

Most subcommands take file and/or directory arguments, recursing
on the directories.  If no arguments are supplied to such a
command, it recurses on the current directory (inclusive) by default.

Available subcommands:
   add
   auth
   blame (praise, annotate, ann)
   cat
   changelist (cl)
   checkout (co)
   cleanup
   commit (ci)
   copy (cp)
   delete (del, remove, rm)
   diff (di)
   export
   help (?, h)
   import
   info
   list (ls)
   lock
   log
   merge
   mergeinfo
   mkdir
   move (mv, rename, ren)
   patch
   propdel (pdel, pd)
   propedit (pedit, pe)
   propget (pget, pg)
   proplist (plist, pl)
   propset (pset, ps)
   relocate
   resolve
   resolved
   revert
   status (stat, st)
   switch (sw)
   unlock
   update (up)
   upgrade

(Use '-v' to show experimental subcommands.)

Subversion is a tool for version control.
For additional information, see http://subversion.apache.org/
```

- 查看SVN版本信息


```
root@4144e8c22fff:~# svn --version
svn, version 1.13.0 (r1867053)
   compiled Mar 24 2020, 12:33:36 on x86_64-pc-linux-gnu

Copyright (C) 2019 The Apache Software Foundation.
This software consists of contributions made by many people;
see the NOTICE file for more information.
Subversion is open source software, see http://subversion.apache.org/

The following repository access (RA) modules are available:

* ra_svn : Module for accessing a repository using the svn network protocol.
  - with Cyrus SASL authentication
  - handles 'svn' scheme
* ra_local : Module for accessing a repository on local disk.
  - handles 'file' scheme
* ra_serf : Module for accessing a repository via WebDAV protocol using serf.
  - using serf 1.3.9 (compiled with 1.3.9)
  - handles 'http' scheme
  - handles 'https' scheme

The following authentication credential caches are available:

* Gnome Keyring
```

- 查看SVN相关的命令行

```sh
# 输入svn后按两次tab键，则会显示svn相关的命令
root@4144e8c22fff:~# svn
svn                              svn-vendor                       svndumpfilter                    svnshell
svn-backup-dumps                 svn_apply_autoprops              svnfsfs                          svnsync
svn-bisect                       svn_load_dirs                    svnlook                          svnversion
svn-clean                        svnadmin                         svnmucc                          svnwrap
svn-hot-backup                   svnauthz                         svnraisetreeconflict
svn-mergeinfo-normalizer         svnauthz-validate                svnrdump
svn-populate-node-origins-index  svnbench                         svnserve
root@4144e8c22fff:~#
```

比较常用的有:

- `svn` SVN命令行客户端。可以进行SVN仓库的检出、提交等工作。

- `svnadmin` SVN仓库管理工具。
- `svnlook` Subversion 存储库检查工具，是SVN钩子脚本中常用的工具。
- `svnmucc`  Subversion多URL命令行客户端，在不检出SVN仓库的情况下，进行SVN数据的提交。
- `svndumpfilter` 对svn的dump导出文件进行过滤的工具。
- `svnserve`SVN存储库的服务工具，提供SVN相关的服务。



### 2.1 svn命令帮助信息

```sh
root@4144e8c22fff:~# svn --help
usage: svn <subcommand> [options] [args]
Subversion command-line client.
Type 'svn help <subcommand>' for help on a specific subcommand.
Type 'svn --version' to see the program version and RA modules,
     'svn --version --verbose' to see dependency versions as well,
     'svn --version --quiet' to see just the version number.

Most subcommands take file and/or directory arguments, recursing
on the directories.  If no arguments are supplied to such a
command, it recurses on the current directory (inclusive) by default.

Available subcommands:
   add
   auth
   blame (praise, annotate, ann)
   cat
   changelist (cl)
   checkout (co)
   cleanup
   commit (ci)
   copy (cp)
   delete (del, remove, rm)
   diff (di)
   export
   help (?, h)
   import
   info
   list (ls)
   lock
   log
   merge
   mergeinfo
   mkdir
   move (mv, rename, ren)
   patch
   propdel (pdel, pd)
   propedit (pedit, pe)
   propget (pget, pg)
   proplist (plist, pl)
   propset (pset, ps)
   relocate
   resolve
   resolved
   revert
   status (stat, st)
   switch (sw)
   unlock
   update (up)
   upgrade

(Use '-v' to show experimental subcommands.)

Subversion is a tool for version control.
For additional information, see http://subversion.apache.org/
root@4144e8c22fff:~#
```

### 2.2 svnadmin命令帮助信息

```sh
root@4144e8c22fff:~# svnadmin --help
general usage: svnadmin SUBCOMMAND REPOS_PATH  [ARGS & OPTIONS ...]
Subversion repository administration tool.
Type 'svnadmin help <subcommand>' for help on a specific subcommand.
Type 'svnadmin --version' to see the program version and FS modules.

Available subcommands:
   crashtest
   create
   delrevprop
   deltify
   dump
   dump-revprops
   freeze
   help (?, h)
   hotcopy
   info
   list-dblogs
   list-unused-dblogs
   load
   load-revprops
   lock
   lslocks
   lstxns
   pack
   recover
   rev-size
   rmlocks
   rmtxns
   setlog
   setrevprop
   setuuid
   unlock
   upgrade
   verify

root@4144e8c22fff:~#
```

### 2.3 svnlook命令帮助信息

```sh
root@4144e8c22fff:~# svnlook --help
general usage: svnlook SUBCOMMAND REPOS_PATH [ARGS & OPTIONS ...]
Subversion repository inspection tool.
Type 'svnlook help <subcommand>' for help on a specific subcommand.
Type 'svnlook --version' to see the program version and FS modules.
Note: any subcommand which takes the '--revision' and '--transaction'
      options will, if invoked without one of those options, act on
      the repository's youngest revision.

Available subcommands:
   author
   cat
   changed
   date
   diff
   dirs-changed
   filesize
   help (?, h)
   history
   info
   lock
   log
   propget (pget, pg)
   proplist (plist, pl)
   tree
   uuid
   youngest

root@4144e8c22fff:~#
```

### 2.4 svnmucc命令帮助信息

```sh
root@4144e8c22fff:~# svnmucc --help
usage: svnmucc ACTION...
Subversion multiple URL command client.
Type 'svnmucc --version' to see the program version and RA modules.

  Perform one or more Subversion repository URL-based ACTIONs, committing
  the result as a (single) new revision.

Actions:
  cp REV SRC-URL DST-URL : copy SRC-URL@REV to DST-URL
  mkdir URL              : create new directory URL
  mv SRC-URL DST-URL     : move SRC-URL to DST-URL
  rm URL                 : delete URL
  put SRC-FILE URL       : add or modify file URL with contents copied from
                           SRC-FILE (use "-" to read from standard input)
  propset NAME VALUE URL : set property NAME on URL to VALUE
  propsetf NAME FILE URL : set property NAME on URL to value read from FILE
  propdel NAME URL       : delete property NAME from URL

Valid options:
  -h, -? [--help]        : display this text
  -m [--message] ARG     : use ARG as a log message
  -F [--file] ARG        : read log message from file ARG
  -u [--username] ARG    : commit the changes as username ARG
  -p [--password] ARG    : use ARG as the password
  --password-from-stdin  : read password from stdin
  -U [--root-url] ARG    : interpret all action URLs relative to ARG
  -r [--revision] ARG    : use revision ARG as baseline for changes
  --with-revprop ARG     : set revision property in the following format:
                               NAME[=VALUE]
  --non-interactive      : do no interactive prompting (default is to
                           prompt only if standard input is a terminal)
  --force-interactive    : do interactive prompting even if standard
                           input is not a terminal
  --trust-server-cert    : deprecated;
                           same as --trust-server-cert-failures=unknown-ca
  --trust-server-cert-failures ARG
                           with --non-interactive, accept SSL server
                           certificates with failures; ARG is comma-separated
                           list of 'unknown-ca' (Unknown Authority),
                           'cn-mismatch' (Hostname mismatch), 'expired'
                           (Expired certificate),'not-yet-valid' (Not yet
                           valid certificate) and 'other' (all other not
                           separately classified certificate errors).
  -X [--extra-args] ARG  : append arguments from file ARG (one per line;
                           use "-" to read from standard input)
  --config-dir ARG       : use ARG to override the config directory
  --config-option ARG    : use ARG to override a configuration option
  --no-auth-cache        : do not cache authentication tokens
  --version              : print version information
root@4144e8c22fff:~#
```

### 2.5 svndumpfilter命令帮助信息

```sh
root@4144e8c22fff:~# svndumpfilter --help
general usage: svndumpfilter SUBCOMMAND [ARGS & OPTIONS ...]
Subversion repository dump filtering tool.
Type 'svndumpfilter help <subcommand>' for help on a specific subcommand.
Type 'svndumpfilter --version' to see the program version.

Available subcommands:
   exclude
   include
   help (?, h)

root@4144e8c22fff:~#
```

### 2.6 svnserve命令帮助信息

```sh
root@4144e8c22fff:~# svnserve --help
usage: svnserve [-d | -i | -t | -X] [options]
Subversion repository server.
Type 'svnserve --version' to see the program version.

Valid options:
  -d [--daemon]            : daemon mode
  -i [--inetd]             : inetd mode
  -t [--tunnel]            : tunnel mode
  -X [--listen-once]       : listen-once mode (useful for debugging)
  -r [--root] ARG          : root of directory to serve
  -R [--read-only]         : force read only, overriding repository config file
  --config-file ARG        : read configuration from file ARG
  --listen-port ARG        : listen port. The default port is 3690.
                             [mode: daemon, listen-once]
  --listen-host ARG        : listen hostname or IP address
                             By default svnserve listens on all addresses.
                             [mode: daemon, listen-once]
  -6 [--prefer-ipv6]       : prefer IPv6 when resolving the listen hostname
                             [IPv4 is preferred by default. Using IPv4 and IPv6
                             at the same time is not supported in daemon mode.
                             Use inetd mode or tunnel mode if you need this.]
  -c [--compression] ARG   : compression level to use for network transmissions
                             [0 .. no compression, 5 .. default,
                              9 .. maximum compression]
  -M [--memory-cache-size] ARG : size of the extra in-memory cache in MB used to
                             minimize redundant operations.
                             Default is 16.
                             0 switches to dynamically sized caches.
                             [used for FSFS and FSX repositories only]
  --cache-txdeltas ARG     : enable or disable caching of deltas between older
                             revisions.
                             Default is yes.
                             [used for FSFS and FSX repositories only]
  --cache-fulltexts ARG    : enable or disable caching of file contents
                             Default is yes.
                             [used for FSFS and FSX repositories only]
  --cache-revprops ARG     : enable or disable caching of revision properties.
                             Consult the documentation before activating this.
                             Default is no.
                             [used for FSFS and FSX repositories only]
  --cache-nodeprops ARG    : enable or disable caching of node properties
                             Default is yes.
                             [used for FSFS repositories only]
  --client-speed ARG       : Optimize network handling based on the assumption
                             that most clients are connected with a bitrate of
                             ARG Mbit/s.
                             Default is 0 (optimizations disabled).
  --block-read ARG         : Parse and cache all data found in block instead
                             of just the requested item.
                             Default is no.
                             [used for FSFS repositories in 1.9 format only]
  -T [--threads]           : use threads instead of fork [mode: daemon]
  --min-threads ARG        : Minimum number of server threads, even if idle.
                             Capped to max-threads; minimum value is 0.
                             Default is 1.
                             [used only with --threads]
  --max-threads ARG        : Maximum number of server threads, even if there
                             are more connections.  Minimum value is 1.
                             Default is 256.
                             [used only with --threads]
  --max-request-size ARG   : Maximum acceptable size of a client request in MB.
                             This implicitly limits the length of paths and
                             property values that can be sent to the server.
                             Also the peak memory usage for protocol handling
                             per server thread or sub-process.
                             0 disables the size check; default is 16.
  --max-response-size ARG  : Maximum acceptable server response size in MB.
                             Longer responses get truncated and return an
                             error.  This limits the server load e.g. when
                             checking out at the wrong path level.
                             Default is 0 (disabled).
  --foreground             : run in foreground (useful for debugging)
                             [mode: daemon]
  --single-thread          : handle one connection at a time in the parent
                             process (useful for debugging)
  --log-file ARG           : svnserve log file
  --pid-file ARG           : write server process ID to file ARG
                             [mode: daemon, listen-once]
  --tunnel-user ARG        : tunnel username (default is current uid's name)
                             [mode: tunnel]
  -h [--help]              : display this help
  --virtual-host           : virtual host mode (look for repo in directory
                             of provided hostname)
  --version                : show program version information
  -q [--quiet]             : no progress (only errors) to stderr

root@4144e8c22fff:~#
```

