# Proxmox VE介绍


[[toc]]



`Proxmox VE`是基于`Debian Linux`，开源的运行虚拟机和窗口的平台。`Proxmox VE`中可以实现两种虚拟化技术，`Kernel-based Virtual Machine (KVM技术)`和`container-based virtualization (LXC技术)`。

一个主要的设计目标是使管理尽可能简单。 您可以在单个节点上使用`Proxmox VE`，也可以组装多个节点的集群。 所有管理任务都可以使用我们基于`Web`的`GUI`管理界面完成，即使是初学者也可以在几分钟内设置和安装`Proxmox VE`。

Proxmox的架构图如下图所示

![proxmox_introduction.svg](/img/proxmox_introduction.svg)


## 管理中心


使用  `Proxmox VE` 一般从单节点开始。`Proxmox VE`可以将大量的节点组成集群。`Proxmox VE`默认安装时就提供有集群功能。

### 多主设置


基于WEB的GUI图形管理界面可以使你全面了解全部的KVM虚拟机/容器以及整个集群。你可以在GUI界面轻松的管理你的VM虚拟机/容器/存储或集群，不需要另外安装复杂的管理服务器。

### Proxmox集群文件系统（pmxcfs）


`Proxmox VE`使用独特的`Proxmox Cluster文件系统（pmxcfs）`，`pmxcfs`是一个用于存储配置文件的数据库驱动文件系统。使您可以存储数千个虚拟机的配置。通过使用`corosync`，可以在所有群集节点上实时复制这些文件。文件系统将所有数据存储在磁盘上的持久数据库中，但是数据的副本驻留在RAM中，RAM的最大存储大小为30MB，这对于存储数千个VM虚拟机的配置来说已经足够了。

`Proxmox VE`是唯一使用此独特群集文件系统的虚拟化平台。

### 基于Web的管理界面


Proxmox VE易于使用。在基于Web的管理界面可以完成管理任务，无需安装单独的管理工具或任何具有大型数据库的其他管理节点。多主工具允许您从群集的任何节点管理整个群集。基于Web框架的中央管理-基于`JavaScript`框架`ExtJS`-使您能够在GUI界面查看每个节点的概述历史记录，系统日志，备份或还原作业，实时迁移或HA触发等功能。

ExtJS介绍：无论是界面之美，还是功能之强，ext的表格控件都高居榜首。
单选行，多选行，高亮显示选中的行，拖拽改变列宽度，按列排序，这些基本功能ExtJS轻量级实现。

### 命令行


对于习惯于熟悉`Unix shell`或`Windows Powershell`的高级用户，`Proxmox VE`提供命令行来管理虚拟环境的所有组件，命令行界面具有智能选项卡功能以及完善的UNIX手册页文档。

### REST API


`Proxmox VE`使用`RESTful API`。我们选择`JSON`作为主要数据格式，并使用`JSON Schema`正式定义整个`API`。这样可以快速轻松地集成第三方管理工具，如自定义托管环境、基于角色的管理等。

### 基于角色的管理


您可以使用基于角色的用户和权限管理为所有对象（如VM，存储，节点等）定义粒度访问。这允许您定义权限并帮助您控制对对象的访问。此概念也称为访问控制列表：每个权限指定特定路径上的主题（用户或组）和角色（权限集）。

### 身份验证


Proxmox VE支持多种身份验证源，如`Microsoft Active Directory`，`LDAP`，`Linux PAM`标准身份验证或内置的`Proxmox VE`身份验证服务。


## 灵活的存储


`Proxmox VE`的存储模型非常灵活。虚拟机映像可以存储在单个或多个本地存储上，也可以存储在`NFS`或`SAN`上面，你可以根据你的需要任意定义你的存储。你可以使用`Debian Linux`可用的所有的存储技术。

将`VM`存储在共享存储上的一个主要好处是能够在没有任何停机的情况下实时迁移正在运行的计算机，因为群集中的所有节点都可以直接访问`VM`磁盘映像。

我们目前支持以下网络存储类型：

- LVM Group（使用iSCSI目标的网络支持）
- iSCSI目标
- NFS共享
- CIFS分享
- Ceph RBD
- 直接使用iSCSI LUN
- GlusterFS

支持的本地存储包括：

- LVM组（本地支持设备，如块设备，FC设备，DRBD等）
- 目录（存储在现有文件系统上）
- ZFS

## 集成备份和还原


集成备份工具（`vzdump`）可创建`KVM`虚拟机和容器的快照。`vzdump`备份工具会创建包括`VM/CT`配置文件在内的`VM/CT`数据的存档。

`KVM`实时备份适用于所有存储类型，包括NFS，CIFS，iSCSI LUN，Ceph RBD或分布式存储系统sheepdog的VM映像，经过优化的备份格式（稀疏文件，乱序数据，最小化I/O）使VM备份更快速高效。

## 高可用集群


多节点`Proxmox VE HA Cluster`可以定义高可用性虚拟服务器。`Proxmox VE HA Cluster`基于成熟的`Linux HA`技术，可提供稳定可靠的`HA`服务。

## 灵活的网络


`Proxmox VE`使用桥接网络模型。 所有虚拟机都可以共享一个网桥，就好像来自每个guest虚拟机的虚拟网络电缆都插入同一个交换机一样。 为了将VM连接到外部世界，桥接器连接到分配了TCP/IP配置的物理网卡。

为了进一步提高灵活性，可以使用`VLAN（IEEE 802.1q）`和网络绑定/聚合。通过这种方式，可以为Proxmox VE主机构建复杂，灵活的虚拟网络，充分利用Linux网络堆栈的强大功能。

## 集成防火墙


集成防火墙允许您在任何VM或容器接口上过滤网络数据包。常见的防火墙规则集可以分组为“安全组”。

## 为什么开源


Proxmox VE使用Linux内核，基于Debian GNU / Linux发行版。 Proxmox VE的源代码是在GNU Affero通用公共许可证版本3下发布的。这意味着您可以随时自由检查源代码或自行参与项目。

在Proxmox，我们致力于尽可能使用开源软件。使用开源软件可确保完全访问所有功能 - 以及高安全性和可靠性。每个人都应该有权访问软件的源代码来运行它，构建它或将更改提交回项目。鼓励每个人做出贡献，而Proxmox确保产品始终符合专业质量标准。

开源软件还有助于降低成本，使你的核心基础架构独立于单一供应商。

## Proxmox VE的优点


- 开源软件
- 没有供应商锁定
- Linux内核
- 安装快速且易于使用
- 基于WEB的管理界面
- REST API
- 巨大的活跃社区
- 管理成本低，部署简单

## 获取帮助


### Proxmox VE wiki


主要信息来源于[Proxmox VE wiki](https://pve.proxmox.com/wiki/Main_Page),包括参考文档和用户贡献的内容。

### 社区论坛


[Proxmox社区论坛](https://forum.proxmox.com/)

Proxmox VE本身是完全开源的，因此我们始终鼓励用户使用Proxmox VE社区论坛讨论和分享他们的知识。该论坛由Proxmox支持团队完全主持，并在全世界拥有庞大的用户群。毋庸置疑，这么大的论坛是获取信息的好地方。

### 邮件列表


通过电子邮件可以与Proxmox VE社区进行快速通信。

用户邮件列表： [PVE User List](https://pve.proxmox.com/cgi-bin/mailman/listinfo/pve-user)

开发人员的主要沟通渠道：

开发人员有邮件列表：  [PVE development discussion](https://pve.proxmox.com/cgi-bin/mailman/listinfo/pve-devel)

### 商业支持


Proxmox Server Solutions Gmbh还提供商业Proxmox VE订阅服务计划。 具有标准订阅计划的系统管理员可以访问具有保证响应时间的专用支持门户，Proxmox VE开发人员可以在出现问题时帮助他们。

### Bug Tracker


我们还在[https://bugzilla.proxmox.com](https://bugzilla.proxmox.com)上运行公共错误跟踪器。 如果您发现问题，可以在那里提交错误报告。 这样可以轻松跟踪其状态，一旦问题得到解决，您就会收到通知。

## 项目历史


该项目始于2007年，随后是2008年的第一个稳定版本。当时我们使用OpenVZ作为容器，使用KVM作为虚拟机。群集功能有限，用户界面很简单（服务器生成的网页）。

但我们使用Corosync集群堆栈快速开发了新功能，并且引入新的Proxmox集群文件系统（pmxcfs）是向前迈出的一大步，因为它完全隐藏了用户的集群复杂性。管理16个节点的集群就像管理单个节点一样简单。

我们还引入了一个新的REST API，其中包含一个用JSON-Schema编写的完整声明性规范。这使其他人能够将Proxmox VE集成到他们的基础架构中，并且可以轻松提供其他服务。

此外，新的REST API使用现代Javascript HTML5应用程序替换原始用户界面成为可能。我们还用noVNC替换了旧的基于Java的VNC控制台代码。因此，您只需要一个Web浏览器来管理您的VM。

对各种存储类型的支持是另一项重大任务。值得注意的是，Proxmox VE是2014年默认在Linux上发布ZFS的第一个发行版。另一个里程碑是能够在虚拟机管理程序节点上运行和管理Ceph存储。这样的设置极具成本效益。

当我们开始时，我们是最早为KVM提供商业支持的公司之一。 KVM项目本身不断发展，现在是一个广泛使用的虚拟机管理程序。每个版本都会提供新功能。我们开发了KVM实时备份功能，可以在任何存储类型上创建快照备份。

版本4.0最值得注意的变化是从OpenVZ迁移到LXC。容器现在已经深度集成，它们可以使用与虚拟机相同的存储和网络功能。

## 改进Proxmox VE文档


根据您希望改进的问题，您可以使用各种通信媒介来联系开发人员。

如果您在当前文档中发现错误，请使用Proxmox错误跟踪器并提出替代文本/措辞。

如果您想提出新内容，则取决于您要记录的内容：

- 如果内容特定于您的设置，那么维基文章是最佳选择。例如，如果您想记录客户系统的特定选项，例如Qemu驱动程序的哪个组合最适合不太流行的操作系统，这非常适合维基文章。

- 如果您认为内容的通用性足以引起所有用户的兴趣，那么您应该尝试将其纳入参考文档。参考文档以易于使用的asciidoc文档格式编写。编辑官方文档需要在 [git://git.proxmox.com/git/pve-docs.git](git://git.proxmox.com/git/pve-docs.git) 中克隆git存储库，然后按照README.adoc文档进行操作。

改进文档就像编辑维基百科文章一样简单，并且是开发大型开源项目的有趣尝试。


[开发者文档](https://pve.proxmox.com/wiki/Developer_Documentation)

如果您对使用Proxmox VE代码库感兴趣，可以参考开发人员文档维基文章。

