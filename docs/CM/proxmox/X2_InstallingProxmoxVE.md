# Proxmox VE安装


[[toc]]



Proxmox VE基于Debian，附带一个安装CD-ROM，其中包括一个完整的Debian系统（5.x版本的"stretch"）以及所有必需的`Proxmox VE`软件包。

安装程序只询问您几个问题，然后对本地磁盘进行分区，安装所有必需的软件包，并配置系统，包括基本网络设置。 您可以在几分钟内获得功能齐全的系统。推荐使用这种方法安装。

Proxmox VE可以安装在现有的Debian系统之上。 但此选项仅建议高级用户使用，因为有必要详细了解Proxmox VE。


## 系统要求


对于生产服务器，需要高质量的服务器设备。 请记住，如果您在一台计算机上运行10个虚拟服务器，然后遇到硬件故障，则会丢失10个服务。 Proxmox VE支持群集，这意味着由于包含群集功能，可以集中管理多个Proxmox VE安装。

Proxmox VE可以使用本地存储（DAS），SAN，NAS以及分布式存储（Ceph RBD）。 详细信息请参见存储章节。

### 最低配置要求


- CPU：64位（Intel EMT64或AMD64）
- 支持KVM全虚拟化Intel VT /AMD-V的CPU/主板
- RAM：1 GB RAM，以及用于虚拟机/容器的额外RAM
- 硬盘
- 一个网卡

### 推荐的系统要求


- CPU：64位（Intel EMT64或AMD64），推荐使用多核CPU
- 支持KVM全虚拟化Intel VT /AMD-V的CPU/主板
- RAM：8 GB RAM，以及用于虚拟机/容器的额外RAM
- 具有电池保护的写入缓存（“BBU”）或基于闪存的保护的硬件RAID
- 快速硬盘驱动器，15k rpm SAS，Raid10的最佳效果
- 至少有两个网卡，具体取决于您需要的存储技术

### 简单的性能概述


在已安装的Proxmox VE系统上，您可以运行附带的`pveperf`脚本以获取CPU和硬盘性能的概述。

::: tip 说明

这只是一个非常快速和通用的基准。 建议进行更详细的测试，尤其是有关系统I/O性能的测试。
:::
    
### 支持的WEB浏览器用于访问WEB图形界面


要使用WEB图形界面，需要一个现代浏览器，其中包括：

- Firefox浏览器，本年度发布的版本，或最新的扩展支持版本
- Chrome浏览器，本年度发布的版本
- Microsoft目前支持的Internet Explorer版本（IE 11或IE Edge或更高版本）
- Apple目前支持的Safari版本（Safari 9或更高版本）

如果Proxmox VE检测到您正在从移动设备进行连接，您将被重定向到基于触摸的轻量级UI。


## 使用Proxmox VE安装CD-ROM


您可以从[https://www.proxmox.com/en/downloads](https://www.proxmox.com/en/downloads)下载ISO。 它包括以下内容：

- 完整的操作系统（Debian Linux，64位）
- Proxmox VE安装程序，使用ext4，ext3，xfs或ZFS对硬盘驱动器进行分区并安装操作系统。
- Proxmox VE内核（Linux），支持LXC和KVM
- 用于管理虚拟机，容器和资源的完整工具集
- 工具集的WEB管理界面


::: warning 警告

在安装过程中，默认使用整个服务器，并删除所有现有数据。请对服务器数据提前进行备份！！！
:::   
    
请插入安装CD-ROM，然后从该驱动器启动。 之后您可以选择以下菜单选项：

![pve-grub-menu.png](/img/pve-grub-menu.png)


- Install Proxmox VE 正常安装

::: tip 说明

可以仅使用键盘来完成安装向导。 可以通过按下ALT键并与相应按钮中带下划线的字符组合来按下按钮。 例如，ALT + N按下“下一步”按钮。
:::

- Install Proxmox VE (Debug mode) 调试模式安装

以调试模式开始安装。 它在几个安装步骤打开一个`shell`控制台，这样你就可以在出现问题时进行调试。 请按`CTRL-D`退出这些调试控制台并继续安装。 此选项主要面向开发人员，不适用于一般用途。
  
- Rescue Boot 救援模式

此选项允许您引导现有安装。它搜索所有连接的硬盘，如果找到现有安装，则使用现有Linux内核直接引导到该磁盘。 如果引导块（grub）出现问题，或者BIOS无法从磁盘读取引导块，可以使用此种模式。
    
- Test Memory 测试内存

运行memtest86+。这有助于检查您的内存是否正常运行且没有错误。
  
