# proxmox Docs

[[toc]]



本文档主要是想将[Proxmox wiki page](https://pve.proxmox.com/wiki/Main_Page)和[Proxmox VE Administration Guide](https://pve.proxmox.com/pve-docs/pve-admin-guide.html)翻译成中文文档，方便大家学习。

2018年查找企业私有云技术时，偶尔的机会发现了`Proxmox`，自己在虚拟机上面经过一翻测试，发现很好用，后来向领导极力推荐，领导同意后，在公司内网使用`Proxmox`部署了一套企业私有云平台，现在在上面部署着一些服务，稳定运行了两年多，`Proxmox`非常不错。你值得尝试！😀😀


1. [Proxmox VE简介](./X1_Introduction.html)
2. [Proxmox VE安装](./X2_InstallingProxmoxVE.html)

## Proxmox Virtual Environment

`Proxmox Virtual Environment`是一种基于`QEMU/KVM`和`LXC`的开源服务器虚拟化管理解决方案。你可以使用集成的，易于使用的`Web`界面或`CLI`管理虚拟机,容器,高可用性群集,存储和网络。`Proxmox VE`代码根据`GNU Affero`通用公共许可证第3版获得许可。该项目由`Proxmox Server Solutions GmbH`开发和维护。

有关`Proxmox VE`主要功能的概述，请访问[Proxmox网站](https://www.proxmox.com/en/proxmox-ve/features)。

## 下载

ISO镜像下载[地址](https://pve.proxmox.com/wiki/Downloads)。

## 使用Proxmox VE

如果你是`Proxmox VE`的新用户,以下章节对你非常有益:

- [Qemu/KVM Virtual Machines](https://pve.proxmox.com/wiki/Qemu/KVM_Virtual_Machines)  和 [Linux Container](https://pve.proxmox.com/wiki/Linux_Container)  

  `Qemu/KVM`虚拟机和`Linux`容器是`Proxmox VE`支持的两种虚拟化技术.

- [Host System Administration](https://pve.proxmox.com/wiki/Host_System_Administration) 

  主机系统管理将详细介绍`Proxmox VE`主机上常用的所有任务,例如在`Linux`上设置软件包存储库,网络配置,系统软件更新,外部度量服务器,磁盘运行状况监控,逻辑卷管理器(`LVM`)和`ZFS`.

- [Cluster Manager](https://pve.proxmox.com/wiki/Cluster_Manager) 

  集群管理将向您介绍如何在群集中对`Proxmox VE`主机进行分组, 设置群集后,可以为虚拟机和容器配置高可用性。

- [High Availability](https://pve.proxmox.com/wiki/High_Availability) 

  设置群集后,可以为虚拟机和容器配置高可用性.

- [Storage](https://pve.proxmox.com/wiki/Storage) 

   存储将概述`Proxmox VE`中支持的所有存储：`GlusterFS`,用户模式`iSCSI`,`iSCSI`,`LVM`,`LVM thin`,`NFS`,`RBD`,`ZFS`,`iSCSI`上的`ZFS`等.

- [Ceph](https://pve.proxmox.com/wiki/Ceph_Server)

  使用`Ceph`设置超融合基础架构.

- [Backup and Restore](https://pve.proxmox.com/wiki/Backup_and_Restore) 

  备份和还原将说明如何使用集成备份管理器.

- [Firewall](https://pve.proxmox.com/wiki/Firewall) 

  详细介绍了内置的`Proxmox VE`防火墙的工作原理.

- [User Management](https://pve.proxmox.com/wiki/User_Management) 

  用户管理解释了身份验证和权限在`Proxmox VE`中的工作方式.

- [Developer Documentation](https://pve.proxmox.com/wiki/Developer_Documentation) 

  开发人员文档将向您展示如何访问源代码，以及如何发送补丁.
  
## 离线文档

在[https://pve.proxmox.com/pve-docs/](https://pve.proxmox.com/pve-docs/)可以获取到完整的`html`,`pdf`,`epub`格式的`Proxmox VE`参考文档.

## 操作文档和故障排除

- [操作文档](https://pve.proxmox.com/wiki/Category:HOWTO)
- [硬件信息](https://pve.proxmox.com/wiki/Category:Hardware)
- [故障排除](https://pve.proxmox.com/wiki/Category:Troubleshooting)

## 版本历史和路线图

- 查看[路线图](https://pve.proxmox.com/wiki/Roadmap),了解即将推出的功能.

## 视频教程

- 我们会定期在网站上面发布视频教程，可参见[https://www.proxmox.com/en/training/video-tutorials](https://www.proxmox.com/en/training/video-tutorials) .

## 用户推荐

- 13,000多家公司,大学,公共机构和非政府组织在生产环境中使用`Proxmox VE`.
