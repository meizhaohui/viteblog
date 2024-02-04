# virtualbox命令行工具VBoxManage的使用

[[toc]]

## 1. 概述

我使用的VirtualBox版本是6.0.12，因此在 [https://download.virtualbox.org/virtualbox/6.0.12/](https://download.virtualbox.org/virtualbox/6.0.12/) 下载相应的用户手册UserManual.pdf：

![](/img/Snipaste_2023-11-21_23-34-24.png)

你可以根据你使用的版本，下载相应的用户手册。

- 通常情况下，我们可以通过VirtualBox GUI界面来创建虚拟机，并对虚拟机进行一系列操作。
- 通过使用命令行，可以让我操作VirtualBox更方便。



### 1.1 准备工作

将VirtualBox的安装目录加入到PATH环境变量中。如我的VirtualBox安装路径是`D:\ProgramFiles\Oracle\VirtualBox`，将该路径加入到PATH环境变量后，打开命令行就可以使用VBoxManage命令了。



### 1.2 查看帮助信息

使用`VBoxManage --help`就可以查看VirtualBox命令行的帮助信息，可以看到输出内容非常多：

```sh
$ VBoxManage --help
Oracle VM VirtualBox Command Line Management Interface Version 6.0.12
(C) 2005-2019 Oracle Corporation
All rights reserved.

Usage:

  VBoxManage [<general option>] <command>


General Options:

  [-v|--version]            print version number and exit
  [-q|--nologo]             suppress the logo
  [--settingspw <pw>]       provide the settings password
  [--settingspwfile <file>] provide a file containing the settings password
  [@<response-file>]        load arguments from the given response file (bourne style)


Commands:

  list [--long|-l] [--sorted|-s]          vms|runningvms|ostypes|hostdvds|hostfloppies|
                            intnets|bridgedifs|hostonlyifs|natnets|dhcpservers|
                            hostinfo|hostcpuids|hddbackends|hdds|dvds|floppies|
                            usbhost|usbfilters|systemproperties|extpacks|
                            groups|webcams|screenshotformats|cloudproviders|
                            cloudprofiles

  showvminfo                <uuid|vmname> [--details]
                            [--machinereadable]
  showvminfo                <uuid|vmname> --log <idx>

  registervm                <filename>

  unregistervm              <uuid|vmname> [--delete]

  createvm                  --name <name>
                            [--groups <group>, ...]
                            [--ostype <ostype>]
                            [--register]
                            [--basefolder <path>]
                            [--uuid <uuid>]
                            [--default]

  modifyvm                  <uuid|vmname>
                            [--name <name>]
                            [--groups <group>, ...]
                            [--description <desc>]
                            [--ostype <ostype>]
                            [--iconfile <filename>]
                            [--memory <memorysize in MB>]
                            [--pagefusion on|off]
                            [--vram <vramsize in MB>]
                            [--acpi on|off]
                            [--pciattach 03:04.0]
                            [--pciattach 03:04.0@02:01.0]
                            [--pcidetach 03:04.0]
                            [--ioapic on|off]
                            [--hpet on|off]
                            [--triplefaultreset on|off]
                            [--apic on|off]
                            [--x2apic on|off]
                            [--paravirtprovider none|default|legacy|minimal|
                                                hyperv|kvm]
                            [--paravirtdebug <key=value> [,<key=value> ...]]
                            [--hwvirtex on|off]
                            [--nestedpaging on|off]
                            [--largepages on|off]
                            [--vtxvpid on|off]
                            [--vtxux on|off]
                            [--pae on|off]
                            [--longmode on|off]
                            [--ibpb-on-vm-exit on|off]
                            [--ibpb-on-vm-entry on|off]
                            [--spec-ctrl on|off]
                            [--l1d-flush-on-sched on|off]
                            [--l1d-flush-on-vm-entry on|off]
                            [--mds-clear-on-sched on|off]
                            [--mds-clear-on-vm-entry on|off]
                            [--nested-hw-virt on|off]
                            [--cpu-profile "host|Intel 80[86|286|386]"]
                            [--cpuid-portability-level <0..3>
                            [--cpuid-set <leaf[:subleaf]> <eax> <ebx> <ecx> <edx>]
                            [--cpuid-remove <leaf[:subleaf]>]
                            [--cpuidremoveall]
                            [--hardwareuuid <uuid>]
                            [--cpus <number>]
                            [--cpuhotplug on|off]
                            [--plugcpu <id>]
                            [--unplugcpu <id>]
                            [--cpuexecutioncap <1-100>]
                            [--rtcuseutc on|off]
                            [--graphicscontroller none|vboxvga|vmsvga|vboxsvga]
                            [--monitorcount <number>]
                            [--accelerate3d on|off]
                            [--accelerate2dvideo on|off]
                            [--firmware bios|efi|efi32|efi64]
                            [--chipset ich9|piix3]
                            [--bioslogofadein on|off]
                            [--bioslogofadeout on|off]
                            [--bioslogodisplaytime <msec>]
                            [--bioslogoimagepath <imagepath>]
                            [--biosbootmenu disabled|menuonly|messageandmenu]
                            [--biosapic disabled|apic|x2apic]
                            [--biossystemtimeoffset <msec>]
                            [--biospxedebug on|off]
                            [--boot<1-4> none|floppy|dvd|disk|net>]
                            [--nic<1-N> none|null|nat|bridged|intnet|hostonly|
                                        generic|natnetwork]
                            [--nictype<1-N> Am79C970A|Am79C973|
                                            82540EM|82543GC|82545EM|
                                            virtio]
                            [--cableconnected<1-N> on|off]
                            [--nictrace<1-N> on|off]
                            [--nictracefile<1-N> <filename>]
                            [--nicproperty<1-N> name=[value]]
                            [--nicspeed<1-N> <kbps>]
                            [--nicbootprio<1-N> <priority>]
                            [--nicpromisc<1-N> deny|allow-vms|allow-all]
                            [--nicbandwidthgroup<1-N> none|<name>]
                            [--bridgeadapter<1-N> none|<devicename>]
                            [--hostonlyadapter<1-N> none|<devicename>]
                            [--intnet<1-N> <network name>]
                            [--nat-network<1-N> <network name>]
                            [--nicgenericdrv<1-N> <driver>
                            [--natnet<1-N> <network>|default]
                            [--natsettings<1-N> [<mtu>],[<socksnd>],
                                                [<sockrcv>],[<tcpsnd>],
                                                [<tcprcv>]]
                            [--natpf<1-N> [<rulename>],tcp|udp,[<hostip>],
                                          <hostport>,[<guestip>],<guestport>]
                            [--natpf<1-N> delete <rulename>]
                            [--nattftpprefix<1-N> <prefix>]
                            [--nattftpfile<1-N> <file>]
                            [--nattftpserver<1-N> <ip>]
                            [--natbindip<1-N> <ip>
                            [--natdnspassdomain<1-N> on|off]
                            [--natdnsproxy<1-N> on|off]
                            [--natdnshostresolver<1-N> on|off]
                            [--nataliasmode<1-N> default|[log],[proxyonly],
                                                         [sameports]]
                            [--macaddress<1-N> auto|<mac>]
                            [--mouse ps2|usb|usbtablet|usbmultitouch]
                            [--keyboard ps2|usb
                            [--uart<1-N> off|<I/O base> <IRQ>]
                            [--uartmode<1-N> disconnected|
                                             server <pipe>|
                                             client <pipe>|
                                             tcpserver <port>|
                                             tcpclient <hostname:port>|
                                             file <file>|
                                             <devicename>]
                            [--uarttype<1-N> 16450|16550A|16750
                            [--lpt<1-N> off|<I/O base> <IRQ>]
                            [--lptmode<1-N> <devicename>]
                            [--guestmemoryballoon <balloonsize in MB>]
                            [--audio none|null|dsound]
                            [--audioin on|off]
                            [--audioout on|off]
                            [--audiocontroller ac97|hda|sb16]
                            [--audiocodec stac9700|ad1980|stac9221|sb16]
                            [--clipboard disabled|hosttoguest|guesttohost|
                                         bidirectional]
                            [--draganddrop disabled|hosttoguest|guesttohost|
                                         bidirectional]
                            [--vrde on|off]
                            [--vrdeextpack default|<name>
                            [--vrdeproperty <name=[value]>]
                            [--vrdeport <hostport>]
                            [--vrdeaddress <hostip>]
                            [--vrdeauthtype null|external|guest]
                            [--vrdeauthlibrary default|<name>
                            [--vrdemulticon on|off]
                            [--vrdereusecon on|off]
                            [--vrdevideochannel on|off]
                            [--vrdevideochannelquality <percent>]
                            [--usbohci on|off]
                            [--usbehci on|off]
                            [--usbxhci on|off]
                            [--usbrename <oldname> <newname>]
                            [--snapshotfolder default|<path>]
                            [--teleporter on|off]
                            [--teleporterport <port>]
                            [--teleporteraddress <address|empty>
                            [--teleporterpassword <password>]
                            [--teleporterpasswordfile <file>|stdin]
                            [--tracing-enabled on|off]
                            [--tracing-config <config-string>]
                            [--tracing-allow-vm-access on|off]
                            [--usbcardreader on|off]
                            [--autostart-enabled on|off]
                            [--autostart-delay <seconds>]
                            [--recording on|off]
                            [--recordingscreens all|<screen ID> [<screen ID> ...]]
                            [--recordingfile <filename>]
                            [--recordingvideores <width> <height>]
                            [--recordingvideorate <rate>]
                            [--recordingvideofps <fps>]
                            [--recordingmaxtime <s>]
                            [--recordingmaxsize <MB>]
                            [--recordingopts <key=value> [,<key=value> ...]]
                            [--defaultfrontend default|<name>]

  clonevm                   <uuid|vmname>
                            [--snapshot <uuid>|<name>]
                            [--mode machine|machineandchildren|all]
                            [--options link|keepallmacs|keepnatmacs|
                                       keepdisknames|keephwuuids]
                            [--name <name>]
                            [--groups <group>, ...]
                            [--basefolder <basefolder>]
                            [--uuid <uuid>]
                            [--register]

  movevm                    <uuid|vmname>
                            --type basic
                            [--folder <path>]

  import                    <ovfname/ovaname>
                            [--dry-run|-n]
                            [--options keepallmacs|keepnatmacs|importtovdi]
                            [more options]
                            (run with -n to have options displayed
                             for a particular OVF)

  export                    <machines> --output|-o <name>.<ovf/ova/tar.gz>
                            [--legacy09|--ovf09|--ovf10|--ovf20|--opc10]
                            [--manifest]
                            [--iso]
                            [--options manifest|iso|nomacs|nomacsbutnat]
                            [--vsys <number of virtual system>]
                                    [--vmname <name>]
                                    [--product <product name>]
                                    [--producturl <product url>]
                                    [--vendor <vendor name>]
                                    [--vendorurl <vendor url>]
                                    [--version <version info>]
                                    [--description <description info>]
                                    [--eula <license text>]
                                    [--eulafile <filename>]
                            [--cloud <number of virtual system>]
                                    [--vmname <name>]
                                    [--cloudprofile <cloud profile name>]
                                    [--cloudshape <shape>]
                                    [--clouddomain <domain>]
                                    [--clouddisksize <disk size in GB>]
                                    [--cloudbucket <bucket name>]
                                    [--cloudocivcn <OCI vcn id>]
                                    [--cloudocisubnet <OCI subnet id>]
                                    [--cloudkeepobject <true/false>]
                                    [--cloudlaunchinstance <true/false>]
                                    [--cloudpublicip <true/false>]

  startvm                   <uuid|vmname>...
                            [--type gui|sdl|headless|separate]
                            [-E|--putenv <NAME>[=<VALUE>]]

  controlvm                 <uuid|vmname>
                            pause|resume|reset|poweroff|savestate|
                            acpipowerbutton|acpisleepbutton|
                            keyboardputscancode <hex> [<hex> ...]|
                            keyboardputstring <string1> [<string2> ...]|
                            keyboardputfile <filename>|
                            setlinkstate<1-N> on|off |
                            nic<1-N> null|nat|bridged|intnet|hostonly|generic|
                                     natnetwork [<devicename>] |
                            nictrace<1-N> on|off |
                            nictracefile<1-N> <filename> |
                            nicproperty<1-N> name=[value] |
                            nicpromisc<1-N> deny|allow-vms|allow-all |
                            natpf<1-N> [<rulename>],tcp|udp,[<hostip>],
                                        <hostport>,[<guestip>],<guestport> |
                            natpf<1-N> delete <rulename> |
                            guestmemoryballoon <balloonsize in MB> |
                            usbattach <uuid>|<address>
                                      [--capturefile <filename>] |
                            usbdetach <uuid>|<address> |
                            audioin on|off |
                            audioout on|off |
                            clipboard disabled|hosttoguest|guesttohost|
                                      bidirectional |
                            draganddrop disabled|hosttoguest|guesttohost|
                                      bidirectional |
                            vrde on|off |
                            vrdeport <port> |
                            vrdeproperty <name=[value]> |
                            vrdevideochannelquality <percent> |
                            setvideomodehint <xres> <yres> <bpp>
                                            [[<display>] [<enabled:yes|no> |
                                              [<xorigin> <yorigin>]]] |
                            setscreenlayout <display> on|primary <xorigin> <yorigin> <xres> <yres> <bpp> | off
                            screenshotpng <file> [display] |
                            recording on|off |
                            recording screens all|none|<screen>,[<screen>...] |
                            recording filename <file> |
                            recording videores <width>x<height> |
                            recording videorate <rate> |
                            recording videofps <fps> |
                            recording maxtime <s> |
                            recording maxfilesize <MB> |
                            setcredentials <username>
                                           --passwordfile <file> | <password>
                                           <domain>
                                           [--allowlocallogon <yes|no>] |
                            teleport --host <name> --port <port>
                                     [--maxdowntime <msec>]
                                     [--passwordfile <file> |
                                      --password <password>] |
                            plugcpu <id> |
                            unplugcpu <id> |
                            cpuexecutioncap <1-100>
                            webcam <attach [path [settings]]> | <detach [path]> | <list>
                            addencpassword <id>
                                           <password file>|-
                                           [--removeonsuspend <yes|no>]
                            removeencpassword <id>
                            removeallencpasswords
                            changeuartmode<1-N> disconnected|
                                                server <pipe>|
                                                client <pipe>|
                                                tcpserver <port>|
                                                tcpclient <hostname:port>|
                                                file <file>|
                                                <devicename>]

  discardstate              <uuid|vmname>

  adoptstate                <uuid|vmname> <state_file>

  snapshot                  <uuid|vmname>
                            take <name> [--description <desc>] [--live]
                                 [--uniquename Number,Timestamp,Space,Force] |
                            delete <uuid|snapname> |
                            restore <uuid|snapname> |
                            restorecurrent |
                            edit <uuid|snapname>|--current
                                 [--name <name>]
                                 [--description <desc>] |
                            list [--details|--machinereadable] |
                            showvminfo <uuid|snapname>

  closemedium               [disk|dvd|floppy] <uuid|filename>
                            [--delete]

  storageattach             <uuid|vmname>
                            --storagectl <name>
                            [--port <number>]
                            [--device <number>]
                            [--type dvddrive|hdd|fdd]
                            [--medium none|emptydrive|additions|
                                      <uuid|filename>|host:<drive>|iscsi]
                            [--mtype normal|writethrough|immutable|shareable|
                                     readonly|multiattach]
                            [--comment <text>]
                            [--setuuid <uuid>]
                            [--setparentuuid <uuid>]
                            [--passthrough on|off]
                            [--tempeject on|off]
                            [--nonrotational on|off]
                            [--discard on|off]
                            [--hotpluggable on|off]
                            [--bandwidthgroup <name>]
                            [--forceunmount]
                            [--server <name>|<ip>]
                            [--target <target>]
                            [--tport <port>]
                            [--lun <lun>]
                            [--encodedlun <lun>]
                            [--username <username>]
                            [--password <password>]
                            [--passwordfile <file>]
                            [--initiator <initiator>]
                            [--intnet]

  storagectl                <uuid|vmname>
                            --name <name>
                            [--add ide|sata|scsi|floppy|sas|usb|pcie]
                            [--controller LSILogic|LSILogicSAS|BusLogic|
                                          IntelAHCI|PIIX3|PIIX4|ICH6|I82078|
                            [             USB|NVMe]
                            [--portcount <1-n>]
                            [--hostiocache on|off]
                            [--bootable on|off]
                            [--rename <name>]
                            [--remove]

  bandwidthctl              <uuid|vmname>
                            add <name> --type disk|network
                                --limit <megabytes per second>[k|m|g|K|M|G] |
                            set <name>
                                --limit <megabytes per second>[k|m|g|K|M|G] |
                            remove <name> |
                            list [--machinereadable]
                            (limit units: k=kilobit, m=megabit, g=gigabit,
                                          K=kilobyte, M=megabyte, G=gigabyte)

  showmediuminfo            [disk|dvd|floppy] <uuid|filename>

  createmedium              [disk|dvd|floppy] --filename <filename>
                            [--size <megabytes>|--sizebyte <bytes>]
                            [--diffparent <uuid>|<filename>
                            [--format VDI|VMDK|VHD] (default: VDI)
                            [--variant Standard,Fixed,Split2G,Stream,ESX,
                                       Formatted]

  modifymedium              [disk|dvd|floppy] <uuid|filename>
                            [--type normal|writethrough|immutable|shareable|
                                    readonly|multiattach]
                            [--autoreset on|off]
                            [--property <name=[value]>]
                            [--compact]
                            [--resize <megabytes>|--resizebyte <bytes>]
                            [--move <path>]
                            [--setlocation <path>]
                            [--description <description string>]
  clonemedium               [disk|dvd|floppy] <uuid|inputfile> <uuid|outputfile>
                            [--format VDI|VMDK|VHD|RAW|<other>]
                            [--variant Standard,Fixed,Split2G,Stream,ESX]
                            [--existing]

  mediumproperty            [disk|dvd|floppy] set <uuid|filename>
                            <property> <value>

                            [disk|dvd|floppy] get <uuid|filename>
                            <property>

                            [disk|dvd|floppy] delete <uuid|filename>
                            <property>

  encryptmedium             <uuid|filename>
                            [--newpassword <file>|-]
                            [--oldpassword <file>|-]
                            [--cipher <cipher identifier>]
                            [--newpasswordid <password identifier>]

  checkmediumpwd            <uuid|filename>
                            <pwd file>|-

  convertfromraw            <filename> <outputfile>
                            [--format VDI|VMDK|VHD]
                            [--variant Standard,Fixed,Split2G,Stream,ESX]
                            [--uuid <uuid>]
  convertfromraw            stdin <outputfile> <bytes>
                            [--format VDI|VMDK|VHD]
                            [--variant Standard,Fixed,Split2G,Stream,ESX]
                            [--uuid <uuid>]

  getextradata              global|<uuid|vmname>
                            <key>|[enumerate]

  setextradata              global|<uuid|vmname>
                            <key>
                            [<value>] (no value deletes key)

  setproperty               machinefolder default|<folder> |
                            hwvirtexclusive on|off |
                            vrdeauthlibrary default|<library> |
                            websrvauthlibrary default|null|<library> |
                            vrdeextpack null|<library> |
                            autostartdbpath null|<folder> |
                            loghistorycount <value>
                            defaultfrontend default|<name>
                            logginglevel <log setting>
                            proxymode system|noproxy|manual
                            proxyurl <url>

  usbfilter                 add <index,0-N>
                            --target <uuid|vmname>|global
                            --name <string>
                            --action ignore|hold (global filters only)
                            [--active yes|no] (yes)
                            [--vendorid <XXXX>] (null)
                            [--productid <XXXX>] (null)
                            [--revision <IIFF>] (null)
                            [--manufacturer <string>] (null)
                            [--product <string>] (null)
                            [--remote yes|no] (null, VM filters only)
                            [--serialnumber <string>] (null)
                            [--maskedinterfaces <XXXXXXXX>]

  usbfilter                 modify <index,0-N>
                            --target <uuid|vmname>|global
                            [--name <string>]
                            [--action ignore|hold] (global filters only)
                            [--active yes|no]
                            [--vendorid <XXXX>|""]
                            [--productid <XXXX>|""]
                            [--revision <IIFF>|""]
                            [--manufacturer <string>|""]
                            [--product <string>|""]
                            [--remote yes|no] (null, VM filters only)
                            [--serialnumber <string>|""]
                            [--maskedinterfaces <XXXXXXXX>]

  usbfilter                 remove <index,0-N>
                            --target <uuid|vmname>|global

  sharedfolder              add <uuid|vmname>
                            --name <name> --hostpath <hostpath>
                            [--transient] [--readonly] [--automount]

  sharedfolder              remove <uuid|vmname>
                            --name <name> [--transient]

  guestproperty             get <uuid|vmname>
                            <property> [--verbose]

  guestproperty             set <uuid|vmname>
                            <property> [<value> [--flags <flags>]]

  guestproperty             delete|unset <uuid|vmname>
                            <property>

  guestproperty             enumerate <uuid|vmname>
                            [--patterns <patterns>]

  guestproperty             wait <uuid|vmname> <patterns>
                            [--timeout <msec>] [--fail-on-timeout]

  guestcontrol              <uuid|vmname> [--verbose|-v] [--quiet|-q]
                              [--username <name>] [--domain <domain>]
                              [--passwordfile <file> | --password <password>]

                              run [common-options]
                              [--exe <path to executable>] [--timeout <msec>]
                              [-E|--putenv <NAME>[=<VALUE>]] [--unquoted-args]
                              [--ignore-operhaned-processes] [--profile]
                              [--no-wait-stdout|--wait-stdout]
                              [--no-wait-stderr|--wait-stderr]
                              [--dos2unix] [--unix2dos]
                              -- <program/arg0> [argument1] ... [argumentN]]

                              start [common-options]
                              [--exe <path to executable>] [--timeout <msec>]
                              [-E|--putenv <NAME>[=<VALUE>]] [--unquoted-args]
                              [--ignore-operhaned-processes] [--profile]
                              -- <program/arg0> [argument1] ... [argumentN]]

                              copyfrom [common-options]
                              [--follow] [-R|--recursive]
                              <guest-src0> [guest-src1 [...]] <host-dst>

                              copyfrom [common-options]
                              [--follow] [-R|--recursive]
                              [--target-directory <host-dst-dir>]
                              <guest-src0> [guest-src1 [...]]

                              copyto [common-options]
                              [--follow] [-R|--recursive]
                              <host-src0> [host-src1 [...]] <guest-dst>

                              copyto [common-options]
                              [--follow] [-R|--recursive]
                              [--target-directory <guest-dst>]
                              <host-src0> [host-src1 [...]]

                              mkdir|createdir[ectory] [common-options]
                              [--parents] [--mode <mode>]
                              <guest directory> [...]

                              rmdir|removedir[ectory] [common-options]
                              [-R|--recursive]
                              <guest directory> [...]

                              removefile|rm [common-options] [-f|--force]
                              <guest file> [...]

                              mv|move|ren[ame] [common-options]
                              <source> [source1 [...]] <dest>

                              mktemp|createtemp[orary] [common-options]
                              [--secure] [--mode <mode>] [--tmpdir <directory>]
                              <template>

                              stat [common-options]
                              <file> [...]

  guestcontrol              <uuid|vmname> [--verbose|-v] [--quiet|-q]

                              list <all|sessions|processes|files> [common-opts]

                              closeprocess [common-options]
                              <   --session-id <ID>
                                | --session-name <name or pattern>
                              <PID1> [PID1 [...]]

                              closesession [common-options]
                              <  --all | --session-id <ID>
                                | --session-name <name or pattern> >

                              updatega|updateguestadditions|updateadditions
                              [--source <guest additions .ISO>]
                              [--wait-start] [common-options]
                              [-- [<argument1>] ... [<argumentN>]]

                              watch [common-options]

  metrics                   list [*|host|<vmname> [<metric_list>]]
                                                 (comma-separated)

  metrics                   setup
                            [--period <seconds>] (default: 1)
                            [--samples <count>] (default: 1)
                            [--list]
                            [*|host|<vmname> [<metric_list>]]

  metrics                   query [*|host|<vmname> [<metric_list>]]

  metrics                   enable
                            [--list]
                            [*|host|<vmname> [<metric_list>]]

  metrics                   disable
                            [--list]
                            [*|host|<vmname> [<metric_list>]]

  metrics                   collect
                            [--period <seconds>] (default: 1)
                            [--samples <count>] (default: 1)
                            [--list]
                            [--detach]
                            [*|host|<vmname> [<metric_list>]]

  natnetwork                add --netname <name>
                            --network <network>
                            [--enable|--disable]
                            [--dhcp on|off]
                            [--port-forward-4 <rule>]
                            [--loopback-4 <rule>]
                            [--ipv6 on|off]
                            [--port-forward-6 <rule>]
                            [--loopback-6 <rule>]

  natnetwork                remove --netname <name>

  natnetwork                modify --netname <name>
                            [--network <network>]
                            [--enable|--disable]
                            [--dhcp on|off]
                            [--port-forward-4 <rule>]
                            [--loopback-4 <rule>]
                            [--ipv6 on|off]
                            [--port-forward-6 <rule>]
                            [--loopback-6 <rule>]

  natnetwork                start --netname <name>

  natnetwork                stop --netname <name>

  natnetwork                list [<pattern>]

  hostonlyif                ipconfig <name>
                            [--dhcp |
                            --ip<ipv4> [--netmask<ipv4> (def: 255.255.255.0)] |
                            --ipv6<ipv6> [--netmasklengthv6<length> (def: 64)]]
                            create |
                            remove <name>

  dhcpserver                add|modify --netname <network_name> |
                                       --ifname <hostonly_if_name>
                            [--ip <ip_address>
                            --netmask <network_mask>
                            --lowerip <lower_ip>
                            --upperip <upper_ip>]
                            [--enable | --disable]
                            [--options [--vm <name> --nic <1-N>]
                             --id <number> [--value <string> | --remove]]
                             (multiple options allowed after --options)

  dhcpserver                remove --netname <network_name> |
                                   --ifname <hostonly_if_name>

  usbdevsource              add <source name>
                            --backend <backend>
                            --address <address>
  usbdevsource              remove <source name>

 Medium content access:

  VBoxManage mediumio <[--disk=uuid|filename] | [--dvd=uuid|filename] |
      [--floppy=uuid|filename]> [--password-file-|filename] formatfat [--quick]

  VBoxManage mediumio <[--disk=uuid|filename] | [--dvd=uuid|filename] |
      [--floppy=uuid|filename]> [--password-file-|filename] cat [--hex]
      [--offset=byte-offset] [--size=bytes] [--output=-|filename]

  VBoxManage mediumio <[--disk=uuid|filename] | [--dvd=uuid|filename] |
      [--floppy=uuid|filename]> [--password-file-|filename] stream
      [--format=image-format] [--variant=image-variant] [--output=-|filename]

 Introspection and guest debugging:

  VBoxManage debugvm <uuid|vmname> dumpvmcore [--filename=name]

  VBoxManage debugvm <uuid|vmname> info <item> [args...]

  VBoxManage debugvm <uuid|vmname> injectnmi

  VBoxManage debugvm <uuid|vmname> log [[--release] | [--debug]]
      [group-settings...]

  VBoxManage debugvm <uuid|vmname> logdest [[--release] | [--debug]]
      [destinations...]

  VBoxManage debugvm <uuid|vmname> logflags [[--release] | [--debug]] [flags...]

  VBoxManage debugvm <uuid|vmname> osdetect

  VBoxManage debugvm <uuid|vmname> osinfo

  VBoxManage debugvm <uuid|vmname> osdmesg [--lines=lines]

  VBoxManage debugvm <uuid|vmname> getregisters [--cpu=id] [reg-set.reg-name...]

  VBoxManage debugvm <uuid|vmname> setregisters [--cpu=id]
      [reg-set.reg-name=value...]

  VBoxManage debugvm <uuid|vmname> show [[--human-readable] | [--sh-export] |
      [--sh-eval] | [--cmd-set]] [settings-item...]

  VBoxManage debugvm <uuid|vmname> stack [--cpu=id]

  VBoxManage debugvm <uuid|vmname> statistics [--reset] [--descriptions]
      [--pattern=pattern]

 Extension package management:

  VBoxManage extpack install [--replace] <tarball>

  VBoxManage extpack uninstall [--force] <name>

  VBoxManage extpack cleanup

 Unattended guest OS installation:

  VBoxManage unattended detect <--iso=install-iso> [--machine-readable]

  VBoxManage unattended install <uuid|vmname> <--iso=install-iso> [--user=login]
      [--password=password] [--password-file=file] [--full-user-name=name]
      [--key=product-key] [--install-additions] [--no-install-additions]
      [--additions-iso=add-iso] [--install-txs] [--no-install-txs]
      [--validation-kit-iso=testing-iso] [--locale=ll_CC] [--country=CC]
      [--time-zone=tz] [--hostname=fqdn]
      [--package-selection-adjustment=keyword] [--dry-run]
      [--auxiliary-base-path=path] [--image-index=number]
      [--script-template=file] [--post-install-template=file]
      [--post-install-command=command]
      [--extra-install-kernel-parameters=params] [--language=lang]
      [--start-vm=session-type]
                                                                                         
$
```



### 1.3 虚拟机组

虚拟机组就是将某些虚拟机存放到一个组中，便于管理。

![](/img/Snipaste_2023-11-24_22-19-23.png)

就像上图中一下，有两个虚拟机组，一个存放Linux操作系统的虚拟机，一个存放Windows操作系统的虚拟机。

有几种方式创建虚拟机组:

- 将一个虚拟机拖动到另外一个虚拟机上。
- 选择多个虚拟机，然后选择【编组】。
- 通过命令行设置虚拟机组。

详细可参考手册1.10节：

![](/img/Snipaste_2023-11-24_22-26-47.png)

## 2. 命令行基本使用

我之前创建了一个虚拟机`basecentos7`：

![](/img/Snipaste_2023-11-21_23-47-34.png)





### 2.1 查看注册了哪些虚拟机

> **8.4 VBoxManage list** 
>
> The list command gives relevant information about your system and information about Oracle 
>
> VM VirtualBox’s current settings. 
>
> The following subcommands are available with VBoxManage list: 
>
> *•* vms: Lists all virtual machines currently registered with Oracle VM VirtualBox. By default 
>
> this displays a compact list with each VM’s name and UUID. If you also specify --long or 
>
> -l, this will be a detailed list as with the showvminfo command, see chapter 8.5, *VBox*
>
> *Manage showvminfo*, page 133. 

即：

- `VBoxManage list vms`可以列出当前在VirtualBox中注册的虚拟机。只显示每个虚拟机的`name`和`UUID`属性。
- 如果指定`--long`或`-l`参数，则显示虚拟机详细信息。

实际执行一下：

```sh
# 查看注册虚拟机
$ VBoxManage list vms
"basecentos7" {04503e84-4597-494d-bdf7-ceb80acd96bd}

# 查看注册虚拟机详情，此处只列出前4行
$ VBoxManage list vms -l|head -n 4
Name:                        basecentos7
Groups:                      /
Guest OS:                    Red Hat (64-bit)
UUID:                        04503e84-4597-494d-bdf7-ceb80acd96bd
$
```



#### 2.1.1 查看单个虚拟机详情

也可以通过`showvminfo`来查看虚拟机详情信息。

```sh
# 查看帮助信息
$ vbm help showvminfo
Oracle VM VirtualBox Command Line Management Interface Version 6.0.12
(C) 2005-2019 Oracle Corporation
All rights reserved.

Usage:

VBoxManage showvminfo       <uuid|vmname> [--details]
                            [--machinereadable]
VBoxManage showvminfo       <uuid|vmname> --log <idx>

# 查看basecentos7虚拟机的详细信息
$ vbm showvminfo basecentos7
Name:                        basecentos7
Groups:                      /
Guest OS:                    Red Hat (64-bit)
UUID:                        04503e84-4597-494d-bdf7-ceb80acd96bd
Config file:                 D:\meich_temp\data\vmdata\basecentos7\basecentos7.vbox
Snapshot folder:             D:\meich_temp\data\vmdata\basecentos7\Snapshots
Log folder:                  D:\meich_temp\data\vmdata\basecentos7\Logs
Hardware UUID:               04503e84-4597-494d-bdf7-ceb80acd96bd
Memory size                  2048MB
Page Fusion:                 disabled
VRAM size:                   16MB
CPU exec cap:                100%
HPET:                        disabled
CPUProfile:                  host
Chipset:                     piix3
Firmware:                    BIOS
Number of CPUs:              1
PAE:                         enabled
Long Mode:                   enabled
Triple Fault Reset:          disabled
APIC:                        enabled
X2APIC:                      enabled
Nested VT-x/AMD-V:           disabled
CPUID Portability Level:     0
CPUID overrides:             None
Boot menu mode:              message and menu
Boot Device 1:               Floppy
Boot Device 2:               DVD
Boot Device 3:               HardDisk
Boot Device 4:               Not Assigned
ACPI:                        enabled
IOAPIC:                      enabled
BIOS APIC mode:              APIC
Time offset:                 0ms
RTC:                         UTC
Hardw. virt.ext:             enabled
Nested Paging:               enabled
Large Pages:                 enabled
VT-x VPID:                   enabled
VT-x unr. exec.:             enabled
Paravirt. Provider:          Default
Effective Paravirt. Prov.:   KVM
State:                       powered off (since 2023-11-24T13:51:25.000000000)
Monitor count:               1
3D Acceleration:             disabled
2D Video Acceleration:       disabled
Teleporter Enabled:          disabled
Teleporter Port:             0
Teleporter Address:
Teleporter Password:
Tracing Enabled:             disabled
Allow Tracing to Access VM:  disabled
Tracing Configuration:
Autostart Enabled:           disabled
Autostart Delay:             0
Default Frontend:
Storage Controller Name (0):            IDE
Storage Controller Type (0):            PIIX4
Storage Controller Instance Number (0): 0
Storage Controller Max Port Count (0):  2
Storage Controller Port Count (0):      2
Storage Controller Bootable (0):        on
Storage Controller Name (1):            SATA
Storage Controller Type (1):            IntelAhci
Storage Controller Instance Number (1): 0
Storage Controller Max Port Count (1):  30
Storage Controller Port Count (1):      1
Storage Controller Bootable (1):        on
IDE (1, 0): Empty
SATA (0, 0): D:\meich_temp\data\vmdata\basecentos7\basecentos7.vdi (UUID: 9e158dcc-2e24-442a-80d2-4762d5588ddf)
NIC 1:                       MAC: 08002774DC60, Attachment: Host-only Interface 'VirtualBox Host-Only Ethernet Adapter', Cable connected: on, Trace: off (file: none), Type: 82540EM, Reported speed: 0 Mbps, Boot priority: 0, Promisc Policy: deny, Bandwidth group: none
NIC 2:                       MAC: 0800273FCD77, Attachment: NAT, Cable connected: on, Trace: off (file: none), Type: 82540EM, Reported speed: 0 Mbps, Boot priority: 0, Promisc Policy: deny, Bandwidth group: none
NIC 2 Settings:  MTU: 0, Socket (send: 64, receive: 64), TCP Window (send:64, receive: 64)
NIC 3:                       disabled
NIC 4:                       disabled
NIC 5:                       disabled
NIC 6:                       disabled
NIC 7:                       disabled
NIC 8:                       disabled
Pointing Device:             PS/2 Mouse
Keyboard Device:             PS/2 Keyboard
UART 1:                      disabled
UART 2:                      disabled
UART 3:                      disabled
UART 4:                      disabled
LPT 1:                       disabled
LPT 2:                       disabled
Audio:                       disabled
Audio playback:              enabled
Audio capture:               disabled
Clipboard Mode:              disabled
Drag and drop Mode:          disabled
VRDE:                        disabled
OHCI USB:                    disabled
EHCI USB:                    disabled
xHCI USB:                    disabled

USB Device Filters:

<none>

Bandwidth groups:  <none>

Shared folders:<none>

Capturing:                   not active
Capture audio:               not active
Capture screens:             0
Capture file:                D:\meich_temp\data\vmdata\basecentos7\basecentos7.webm
Capture dimensions:          1024x768
Capture rate:                512kbps
Capture FPS:                 25kbps
Capture options:

Guest:

Configured memory balloon size: 0MB
```





### 2.2 设置快捷命令

感觉手敲`VBoxManage`命令有点长，我设置一个快捷命令，后续都使用快捷命令来操作。

```sh
alias vbm='VBoxManage'
```

可以将该快捷命令加入到`~/.bashrc`配置文件中，然后重新加载配置文件，后面就可以一直使用该快捷命令了。



使用快捷命令查看注册虚拟机：

```sh
$ vbm list vms
"basecentos7" {04503e84-4597-494d-bdf7-ceb80acd96bd}
```





### 2.3 启动虚拟机

可以使用`startvm`来启动虚拟机，默认是GUI模式；也可以使用`headless`无头模式后台启动。

>**gui** 
>
>Starts a VM showing a GUI window. This is the default. 
>
>**headless** 
>
>Starts a VM without a window for remote display only

查看`starvm`的帮助信息：

```sh
$ vbm help startvm
Oracle VM VirtualBox Command Line Management Interface Version 6.0.12
(C) 2005-2019 Oracle Corporation
All rights reserved.

Usage:

VBoxManage startvm          <uuid|vmname>...
                            [--type gui|sdl|headless|separate]
                            [-E|--putenv <NAME>[=<VALUE>]]
```

#### 2.3.1 GUI模式启动虚拟机

启动basecentos7虚拟机：

```sh
$ vbm startvm basecentos7
Waiting for VM "basecentos7" to power on...
VM "basecentos7" has been successfully started.
```

效果图:

![](/img/Snipaste_2023-11-22_22-10-31.png)

此时可以看到，启动了basecentos7虚拟机，窗口自动启动，并显示在登录界面。

使用`root`账号登录后，查看虚拟机IP信息：

![](/img/Snipaste_2023-11-22_22-12-59.png)

在任务管理器可以看到此时有三个`VirtualBoxVM.exe`的进程：

![](/img/Snipaste_2023-11-22_22-28-58.png)



使用`shutdown -h now`命令将虚拟机关机。

#### 2.3.2 无头模式启动虚拟机

无头模式启动basecentos7虚拟机：

```sh
$ vbm startvm basecentos7 --type headless
Waiting for VM "basecentos7" to power on...
VM "basecentos7" has been successfully started.
```

此时，没有弹出新的窗口。在任务管理器可以看到此时有三个`VBoxHeadless.exe`的进程：

![](/img/Snipaste_2023-11-22_22-20-24.png)

此时，可以通过mobaxterm远程连接到虚拟机：

![](/img/Snipaste_2023-11-22_22-21-26.png)



通过GUI模式和无头模式对比内存使用量：

| 进程           | GUI模式（KB） | 无头模式（KB） |
| -------------- | ------- | -------- |
| 进程1          | 856     | 1120     |
| 进程2          | 1124    | 2352     |
| 进程3          | 84584   | 56524    |
| 总内存         | 86564   | 59996    |
| 下降内存大小   | 26568   | - |
| 下降内存百分比 | 30.69% | - |

可以看到内存下降百分比达到30.69%，由于我大部分都是在终端远程连接到虚拟机，所以使用无头模式可以节约内存。

### 2.4 显示正在运行的虚拟机

- 可以使用`VBoxManage list runningvms`来显示正在运行的虚拟机。

如上一节中我们启动了`basecentos7`虚拟机，现在查看一下：

```sh
$ vbm list runningvms
"basecentos7" {04503e84-4597-494d-bdf7-ceb80acd96bd}
```

可以看到显示出正在运行的虚拟机是`basecentos7`。



### 2.5 克隆虚拟机

查看克隆虚拟机使用的命令帮助信息：

```sh
$ vbm help clonevm
Oracle VM VirtualBox Command Line Management Interface Version 6.0.12
(C) 2005-2019 Oracle Corporation
All rights reserved.

Usage:

VBoxManage clonevm          <uuid|vmname>
                            [--snapshot <uuid>|<name>]
                            [--mode machine|machineandchildren|all]
                            [--options link|keepallmacs|keepnatmacs|
                                       keepdisknames|keephwuuids]
                            [--name <name>]
                            [--groups <group>, ...]
                            [--basefolder <basefolder>]
                            [--uuid <uuid>]
                            [--register]
```

参数说明：
- `--snapshot`，指定从虚拟机的哪个快照克隆，默认从当前状态克隆虚拟机。
- `--mode`, 指定克隆模式，默认使用`machine`模式，不克隆虚拟机的任何快照。
- `--options`,选项，指定如何来创建新的虚拟机。
  - `link`，创建一个链接克隆。
  - `keepallmacs` ，保持所有MAC地址。如果你不指定`--options keepnatmacs`，默认行为是为所有虚拟网卡重新生成新的MAC地址。
  - `keepnatmacs` ，当虚拟机网卡网络类型是`NAT`，保持所有MAC地址。如果你不指定`--options keepallmacs`，默认行为是为所有虚拟网卡重新生成新的MAC地址。
  - `keepdisknames` ，克隆时保留磁盘镜像名称。默认行为是重新命名磁盘镜像名称。你可以使用`keephwuuids`选项来保留硬件ID信息。
  - `keephwuuids`，保留硬件ID信息。默认行为是重新生成硬件UUID值。
- `--name`, 指定新的虚拟机的名称，默认是`name Clone`。
- `--register`，自动注册新创建的虚拟机到VirtualBox中。你也可以通过使用`registervm`来手动注册。
- `--basefolder`，指定新的虚拟机配置文件存放在哪个目录。一般可以不用修改，保持默认即可。
- `--uuid`，指定虚拟机的UUID值，请确保UUID值唯一。默认情况下，会自动生成新的UUID值。



通常情况下，需要通过克隆虚拟机来新建一个虚拟机。希望自动从当前状态克隆、自动重新生成MAC地址、自动注册虚拟机、自动生成UUID值，因此，只需要指定`--name`和`--register`两个参数就行了。



#### 2.5.1 克隆正在运行的虚拟机

::: warning 警告

正在运行的虚拟机不能克隆。

:::



上一节中basecentos7虚拟机正在运行，尝试克隆一下，克隆新的虚拟机命令为`testvm1`:

```sh
$ vbm clonevm basecentos7 --name "testvm1" --register
0%...
Progress state: VBOX_E_INVALID_OBJECT_STATE
VBoxManage.exe: error: Clone VM failed
VBoxManage.exe: error: Failed to lock source media 'basecentos7\basecentos7.vdi'
VBoxManage.exe: error: Details: code VBOX_E_INVALID_OBJECT_STATE (0x80bb0007), component MediumWrap, interface IMedium
VBoxManage.exe: error: Context: "enum RTEXITCODE __cdecl handleCloneVM(struct HandlerArg *)" at line 609 of file VBoxManageMisc.cpp
```

可以看到克隆报错了。

#### 2.5.2 克隆已经关机的虚拟机

远程登录到basecentos7虚拟机，并使用`shutdown -h now`命令关机。

虚拟机关机后，再执行克隆操作：

```sh
# 查看正在运行的虚拟机，可以看到没有正在运行的虚拟机
$ vbm list runningvms

# 克隆虚拟机，可以看到克隆成功
$ vbm clonevm basecentos7 --name "testvm1" --register
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Machine has been successfully cloned as "testvm1"

# 查看当前注册了的虚拟机
$ vbm list vms
"basecentos7" {04503e84-4597-494d-bdf7-ceb80acd96bd}
"testvm1" {6938489f-41aa-4982-903d-9fe0ea6d36f8}
```

此时查看virutalBox界面：

![](/img/Snipaste_2023-11-24_21-56-44.png)

可以看到刚才克隆的`testvm1`虚拟机。



相同的方式，我们再克隆一台`testvm2`虚拟机出来。

```sh
# 克隆虚拟机，可以看到克隆成功
$ vbm clonevm basecentos7 --name "testvm2" --register
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Machine has been successfully cloned as "testvm2"

# 查看当前注册了的虚拟机
$ vbm list vms
"basecentos7" {04503e84-4597-494d-bdf7-ceb80acd96bd}
"testvm1" {6938489f-41aa-4982-903d-9fe0ea6d36f8}
"testvm2" {b2c3364f-c077-4c2d-afd6-aafecbefa020}
```

此时查看virutalBox界面：

![](/img/Snipaste_2023-11-24_22-00-41.png)

可以看到刚才克隆的`testvm2`虚拟机。



#### 2.5.3 克隆虚拟机时设置虚拟机组

为了测试克隆时自动创建虚拟机组，我们选中`testvm`和`testvm2`虚拟机，并右键，选择【编组】，并重命名组名为`testgroup`。

编组后显示如下：

![](/img/Snipaste_2023-11-24_22-50-01.png)

此时，创建虚拟机`testvm3`，并指定虚拟机组为`/testgroup`:

```sh
$ vbm clonevm basecentos7 --name "testvm3" --register --groups "/testgroup"
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Machine has been successfully cloned as "testvm3"
```

此时，可以看到`testvm3`并没有自动加入到`/testgroup`组中：

![](/img/Snipaste_2023-11-24_22-53-04.png)



通过`modifyvm`命令将其加入到`/testgroup`组中：

```sh
$ vbm modifyvm testvm3 --groups=/testgroup
```



此时在virtualBox GUI界面没有自动刷新，没有正常将`testvm3`虚拟机放到`/testgroup`组中。

关闭virtualBox 界面，重新打开，此时可以看到`testvm3`虚拟机已经在`/testgroup`组中了：

![](/img/Snipaste_2023-11-24_22-59-28.png)

这是一个bug，对应的issue问题单 [GUI: VM grouping not updating automatically if changed via VBoxManage](https://www.virtualbox.org/ticket/20933), 该问题已经在 VirtualBox 7.0.6 and 6.1.42 中解决，由于我的版本是6.0.12，因此还有该问题。



此时查看`testvm3`的信息，也可以看到对应的group组信息不是默认的`/`组了：

```sh
$ vbm showvminfo testvm3|head -n 4
Name:                        testvm3
Groups:                      /testgroup
Guest OS:                    Red Hat (64-bit)
UUID:                        9c08154f-62e6-4f8e-a23f-75e84297e703
```



### 2.6 修改虚拟机设置

查看`modifyvm`帮助信息：

```sh
$ vbm help modifyvm
Oracle VM VirtualBox Command Line Management Interface Version 6.0.12
(C) 2005-2019 Oracle Corporation
All rights reserved.

Usage:

VBoxManage modifyvm         <uuid|vmname>
                            [--name <name>]
                            [--groups <group>, ...]
                            [--description <desc>]
                            [--ostype <ostype>]
                            [--iconfile <filename>]
                            [--memory <memorysize in MB>]
                            [--pagefusion on|off]
                            [--vram <vramsize in MB>]
                            [--acpi on|off]
                            [--pciattach 03:04.0]
                            [--pciattach 03:04.0@02:01.0]
                            [--pcidetach 03:04.0]
                            [--ioapic on|off]
                            [--hpet on|off]
                            [--triplefaultreset on|off]
                            [--apic on|off]
                            [--x2apic on|off]
                            [--paravirtprovider none|default|legacy|minimal|
                                                hyperv|kvm]
                            [--paravirtdebug <key=value> [,<key=value> ...]]
                            [--hwvirtex on|off]
                            [--nestedpaging on|off]
                            [--largepages on|off]
                            [--vtxvpid on|off]
                            [--vtxux on|off]
                            [--pae on|off]
                            [--longmode on|off]
                            [--ibpb-on-vm-exit on|off]
                            [--ibpb-on-vm-entry on|off]
                            [--spec-ctrl on|off]
                            [--l1d-flush-on-sched on|off]
                            [--l1d-flush-on-vm-entry on|off]
                            [--mds-clear-on-sched on|off]
                            [--mds-clear-on-vm-entry on|off]
                            [--nested-hw-virt on|off]
                            [--cpu-profile "host|Intel 80[86|286|386]"]
                            [--cpuid-portability-level <0..3>
                            [--cpuid-set <leaf[:subleaf]> <eax> <ebx> <ecx> <edx>]
                            [--cpuid-remove <leaf[:subleaf]>]
                            [--cpuidremoveall]
                            [--hardwareuuid <uuid>]
                            [--cpus <number>]
                            [--cpuhotplug on|off]
                            [--plugcpu <id>]
                            [--unplugcpu <id>]
                            [--cpuexecutioncap <1-100>]
                            [--rtcuseutc on|off]
                            [--graphicscontroller none|vboxvga|vmsvga|vboxsvga]
                            [--monitorcount <number>]
                            [--accelerate3d on|off]
                            [--accelerate2dvideo on|off]
                            [--firmware bios|efi|efi32|efi64]
                            [--chipset ich9|piix3]
                            [--bioslogofadein on|off]
                            [--bioslogofadeout on|off]
                            [--bioslogodisplaytime <msec>]
                            [--bioslogoimagepath <imagepath>]
                            [--biosbootmenu disabled|menuonly|messageandmenu]
                            [--biosapic disabled|apic|x2apic]
                            [--biossystemtimeoffset <msec>]
                            [--biospxedebug on|off]
                            [--boot<1-4> none|floppy|dvd|disk|net>]
                            [--nic<1-N> none|null|nat|bridged|intnet|hostonly|
                                        generic|natnetwork]
                            [--nictype<1-N> Am79C970A|Am79C973|
                                            82540EM|82543GC|82545EM|
                                            virtio]
                            [--cableconnected<1-N> on|off]
                            [--nictrace<1-N> on|off]
                            [--nictracefile<1-N> <filename>]
                            [--nicproperty<1-N> name=[value]]
                            [--nicspeed<1-N> <kbps>]
                            [--nicbootprio<1-N> <priority>]
                            [--nicpromisc<1-N> deny|allow-vms|allow-all]
                            [--nicbandwidthgroup<1-N> none|<name>]
                            [--bridgeadapter<1-N> none|<devicename>]
                            [--hostonlyadapter<1-N> none|<devicename>]
                            [--intnet<1-N> <network name>]
                            [--nat-network<1-N> <network name>]
                            [--nicgenericdrv<1-N> <driver>
                            [--natnet<1-N> <network>|default]
                            [--natsettings<1-N> [<mtu>],[<socksnd>],
                                                [<sockrcv>],[<tcpsnd>],
                                                [<tcprcv>]]
                            [--natpf<1-N> [<rulename>],tcp|udp,[<hostip>],
                                          <hostport>,[<guestip>],<guestport>]
                            [--natpf<1-N> delete <rulename>]
                            [--nattftpprefix<1-N> <prefix>]
                            [--nattftpfile<1-N> <file>]
                            [--nattftpserver<1-N> <ip>]
                            [--natbindip<1-N> <ip>
                            [--natdnspassdomain<1-N> on|off]
                            [--natdnsproxy<1-N> on|off]
                            [--natdnshostresolver<1-N> on|off]
                            [--nataliasmode<1-N> default|[log],[proxyonly],
                                                         [sameports]]
                            [--macaddress<1-N> auto|<mac>]
                            [--mouse ps2|usb|usbtablet|usbmultitouch]
                            [--keyboard ps2|usb
                            [--uart<1-N> off|<I/O base> <IRQ>]
                            [--uartmode<1-N> disconnected|
                                             server <pipe>|
                                             client <pipe>|
                                             tcpserver <port>|
                                             tcpclient <hostname:port>|
                                             file <file>|
                                             <devicename>]
                            [--uarttype<1-N> 16450|16550A|16750
                            [--lpt<1-N> off|<I/O base> <IRQ>]
                            [--lptmode<1-N> <devicename>]
                            [--guestmemoryballoon <balloonsize in MB>]
                            [--audio none|null|dsound]
                            [--audioin on|off]
                            [--audioout on|off]
                            [--audiocontroller ac97|hda|sb16]
                            [--audiocodec stac9700|ad1980|stac9221|sb16]
                            [--clipboard disabled|hosttoguest|guesttohost|
                                         bidirectional]
                            [--draganddrop disabled|hosttoguest|guesttohost|
                                         bidirectional]
                            [--vrde on|off]
                            [--vrdeextpack default|<name>
                            [--vrdeproperty <name=[value]>]
                            [--vrdeport <hostport>]
                            [--vrdeaddress <hostip>]
                            [--vrdeauthtype null|external|guest]
                            [--vrdeauthlibrary default|<name>
                            [--vrdemulticon on|off]
                            [--vrdereusecon on|off]
                            [--vrdevideochannel on|off]
                            [--vrdevideochannelquality <percent>]
                            [--usbohci on|off]
                            [--usbehci on|off]
                            [--usbxhci on|off]
                            [--usbrename <oldname> <newname>]
                            [--snapshotfolder default|<path>]
                            [--teleporter on|off]
                            [--teleporterport <port>]
                            [--teleporteraddress <address|empty>
                            [--teleporterpassword <password>]
                            [--teleporterpasswordfile <file>|stdin]
                            [--tracing-enabled on|off]
                            [--tracing-config <config-string>]
                            [--tracing-allow-vm-access on|off]
                            [--usbcardreader on|off]
                            [--autostart-enabled on|off]
                            [--autostart-delay <seconds>]
                            [--recording on|off]
                            [--recordingscreens all|<screen ID> [<screen ID> ...]]
                            [--recordingfile <filename>]
                            [--recordingvideores <width> <height>]
                            [--recordingvideorate <rate>]
                            [--recordingvideofps <fps>]
                            [--recordingmaxtime <s>]
                            [--recordingmaxsize <MB>]
                            [--recordingopts <key=value> [,<key=value> ...]]
                            [--defaultfrontend default|<name>]
```

可以看到`modifyvm`修改虚拟机的选项非常多，我们不一一测试实践。



#### 2.6.1 增加虚拟机CPU核心数

在部署 Kubernetes 时，通常需要配置2CPU的虚拟机。我配置的模板`basecentos7`的CPU核心数是1：

![](/img/Snipaste_2023-11-26_21-38-06.png)

可以看到`basecentos7`的CPU核心数是1。可以在GUI界面将处理器数量调整为2。但为了测试命令行，我直接在命令行进行修改。

- 查看修改前虚拟机CPU核心数

```sh
$ vbm showvminfo basecentos7|grep -i cpus
Number of CPUs:              1
```

可以看到是1个CPU核心。

- 使用`modifyvm`修改：

```sh
$ vbm modifyvm basecentos7 --cpus 2
```

- 再次查看修改前虚拟机CPU核心数

```sh
$ vbm showvminfo basecentos7|grep -i cpus
Number of CPUs:              2
```

可以看到是2个CPU核心，已经修改成功了。

重新在界面上查看，可以看到处理器数量已经变成了2：

![](/img/Snipaste_2023-11-26_22-08-08.png)

相同方式，将`testvm1`、`testvm2`、`testvm3`三个虚拟机的处理器数量修改为2。

```sh
$ vbm modifyvm testvm1 --cpus 2
$ vbm modifyvm testvm2 --cpus 2
$ vbm modifyvm testvm3 --cpus 2
```



#### 2.6.2 修改虚拟机说明信息

- `--description` 参数可以用来修改虚拟机说明信息。

现在来修改`basecentos7`的描述信息为"基础镜像: centos7最小化安装,仅配置静态IP 192.168.56.101"：

```sh
$ vbm modifyvm basecentos7 --description "基础镜像: centos7最小化安装,仅配置静态IP 192.168.56.101"
```

修改后，查看虚拟机信息：

![](/img/Snipaste_2023-11-26_22-38-38.png)

可以看到，描述信息已经正常显示了。

为了避免在命令行显示描述信息乱码，我们就描述信息修改为英文的。

```sh
# 再次修改虚拟机说明
$ vbm modifyvm basecentos7 --description "Base image: centos7 Minimize installation. Only config the static IP 192.168.56.101"

# 查看修改后的描述信息
$ vbm showvminfo basecentos7|grep -A1 Description
Description:
Base image: centos7 Minimize installation. Only config the static IP 192.168.56.101
```

此时在界面上也可以看到描述发生了变化。



#### 2.6.3 修改虚拟机内存

假如我想将`testvm1`作为Ansible控制节点，或者作为 Kubernetes 的主节点，希望将该虚拟机内存调大一些。将2GB=2048MB调整到4GB=4096MB，则按以下方法调整。

调整前，查看虚拟机内存信息：

```sh
$ vbm showvminfo testvm1 |grep "Memory size"
Memory size                  2048MB
```

修改内存值，默认以`MB`为单位：

```sh
$ vbm modifyvm testvm1 --memory 4096
```

再次查看虚拟机内存信息：

```sh
$ vbm showvminfo testvm1 |grep "Memory size"
Memory size                  4096MB
```

可以看到内存信息已经调整成功。





### 2.7 快照管理

可以使用`VBoxManage help snapshot`查看快照相关的帮助信息：

```sh
$ vbm help snapshot
Oracle VM VirtualBox Command Line Management Interface Version 6.0.12
(C) 2005-2019 Oracle Corporation
All rights reserved.

Usage:

VBoxManage snapshot         <uuid|vmname>
                            take <name> [--description <desc>] [--live]
                                 [--uniquename Number,Timestamp,Space,Force] |
                            delete <uuid|snapname> |
                            restore <uuid|snapname> |
                            restorecurrent |
                            edit <uuid|snapname>|--current
                                 [--name <name>]
                                 [--description <desc>] |
                            list [--details|--machinereadable] |
                            showvminfo <uuid|snapname>
$
```



#### 2.7.1 获取虚拟机快照信息

- 使用`VBoxManage snapshot <vm> list`来获取虚拟机的快照信息。

查看`testvm1`的快照信息：

```sh
$ vbm snapshot testvm1 list
This machine does not have any snapshots
```

可以看到，此时没有任何快照。



#### 2.7.2 创建快照

- 使用`VBoxManage snapshot <vm> take`来创建虚拟机的快照。
  - `<name>`，需要指定快照名称。
  - `--description <desc>`，快照的描述信息。
  - `--live`，不停止虚拟机创建关照。

最好是关机后再进行虚拟机的快照创建。

```sh
$ vbm snapshot testvm1 take "1_os_init" --description  "Minimize installation"
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Snapshot taken. UUID: 31863d6f-8d58-4d58-aa2e-01aed147602c
```

查看刚才创建的快照：

```sh
$ vbm snapshot testvm1 list
   Name: 1_os_init (UUID: 31863d6f-8d58-4d58-aa2e-01aed147602c) *
   Description:
Minimize installation
```

在VirtualBox界面上也可以看到刚创建的快照：

![](/img/Snipaste_2023-11-29_21-38-30.png)



#### 2.7.3 修改快照信息

- 使用`VBoxManage snapshot <vm> edit`来修改虚拟机的快照信息。

如修改`1_os_init`快照名称：

```sh
# 将testvm1虚拟机的1_os_init名称修改为0_os_init
$ vbm snapshot testvm1 edit 1_os_init --name "0_os_init"
                                                                                         
# 再次查看快照信息
$ vbm snapshot testvm1 list
   Name: 0_os_init (UUID: 31863d6f-8d58-4d58-aa2e-01aed147602c) *
   Description:
Minimize installation
```

在VirtualBox界面上也可以看到快照的名称发生了变化：

![](/img/Snipaste_2023-11-29_21-46-06.png)



#### 2.7.4 删除快照

- 使用`VBoxManage snapshot <vm> delete`来删除虚拟机的快照。

如将`0_os_init`快照删除：

```sh
# 将testvm1虚拟机的名称为0_os_init快照删除
$ vbm snapshot testvm1 delete "0_os_init"
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Deleting snapshot '0_os_init' (31863d6f-8d58-4d58-aa2e-01aed147602c)

# 再次查看快照信息
$ vbm snapshot testvm1 list
This machine does not have any snapshots
```

可以看到，快照已经删除了。



## 3. 综合应用

### 3.1 修改虚拟机IP

到目前为止，我已经在VirtualBox中创建了4个虚拟机了，包括：

- basecentos7，配置了静态IP，对应IP: 192.168.56.101。
- testvm1，从basecentos7克隆来的，对应IP: 192.168.56.101。
- testvm2，也是从basecentos7克隆来的，对应IP: 192.168.56.101。
- testvm3，也是从basecentos7克隆来的，对应IP: 192.168.56.101。

如果我要修改新克隆的`testvm1`的IP，该怎么做：

可以看到克隆虚拟机后，这四台虚拟机的IP都是一样的。可以在克隆完成每台新的虚拟机出来后，远程连接到`192.168.56.101`服务器，然后手动修改`/etc/sysconfig/network-scripts/ifcfg-enp0s3`配置文件中`IPADDR=192.168.56.101`这一行内容，如修改为`IPADDR=192.168.56.110`，然后重启虚拟机，这时该虚拟机的IP就是`192.168.56.110`。

我先用终端工具连接到`192.168.56.101`主机：

![](/img/Snipaste_2023-11-29_23-39-19.png)

另一种方式，就是使用`ssh`直接执行`bash -s`命令来调用脚本，自动帮修改虚拟机IP信息。

我们先来编写一个`change_ip.sh`脚本，用来修改新克隆虚拟机的IP。

```sh
#!/bin/bash
# filename: change_ip.sh
# author:   meizhaohui
configfile=/etc/sysconfig/network-scripts/ifcfg-enp0s3
IP=$1
echo "待分配IP:${IP}"
echo "IP 修改前配置文件内容："
cat "${configfile}"
sed -i "s/192.168.56.101/$IP/g" "${configfile}"
echo -e "\n=========================\n"
echo "IP 修改后配置文件内容："
cat "${configfile}"
echo "重启虚拟机。请使用新IP($IP)重新登陆。"
shutdown -r now
```

注，脚本参考：[ssh登录远程主机，让远程主机执行脚本文件，并传参](https://blog.csdn.net/weixin_44505901/article/details/130542560)

然后，在脚本所在目录执行以下命令：

```sh
cat change_ip.sh |ssh root@192.168.56.101 "bash -s" "192.168.56.110"
```

命令中：

- `"192.168.56.110"`是传递给`change_ip.sh`脚本的参数。
- `ssh root@192.168.56.101`表示通过ssh连接到192.168.56.101主机。
- `"bash -s"`表示需要在远程主机执行的命令，此处就是执行`change_ip.sh`脚本。

我们实际执行下：

```sh
$ cat change_ip.sh |ssh root@192.168.56.101 "bash -s" "192.168.56.110"
待分配IP:192.168.56.110
IP 修改前配置文件内容：
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp0s3
UUID=9ea09614-9750-4752-9dc6-d64f5535ea87
DEVICE=enp0s3
ONBOOT=yes
IPADDR=192.168.56.101

=========================

IP 修改后配置文件内容：
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp0s3
UUID=9ea09614-9750-4752-9dc6-d64f5535ea87
DEVICE=enp0s3
ONBOOT=yes
IPADDR=192.168.56.110
重启虚拟机。请使用新IP(192.168.56.110)重新登陆。
Connection to 192.168.56.101 closed by remote host.
$
```

![](/img/Snipaste_2023-11-29_23-48-30.png)

可以看到，远程主机IP修改成功。实际验证一下：

```sh
$ ssh root@192.168.56.110
X11 forwarding request failed on channel 0
Last login: Wed Nov 29 23:36:50 2023 from 192.168.56.1
[root@localhost ~]# hostname -I
192.168.56.110 10.0.3.15
[root@localhost ~]#
```

可以看到，成功登陆！！

![](/img/Snipaste_2023-11-29_23-51-38.png)

**注意，上面修改虚拟机IP的命令，是需要克隆后的虚拟机正常开机，然后才能执行脚本。**

### 3.2 从任意虚拟机克隆并设置新IP

假设我现在想对上面修改的`192.168.56.110`这台主机进行克隆，新的虚拟机名称是`ansible-master`，并设置新的IP为`192.168.56.120`。

为了让克隆操作进行得更顺利，我们先将`192.168.56.110`这台主机，也就是`testvm1`虚拟机关机。

```sh
[root@localhost ~]# shutdown -h now
Connection to 192.168.56.110 closed by remote host.
Connection to 192.168.56.110 closed.
```

此时，应编写一个更加通用的脚本，来操作`VBoxManage`命令来克隆虚拟机，并用上一节的方法设置IP。

即需要做以下事项：

- `vbm clonevm`克隆虚拟机，并设置虚拟机名称。
- `vbm startvm "ansible-master" --type headless`无头模式启动`ansible-master`虚拟机。
- 修改`change_ip.sh`脚本，使其更通用，因为待克隆的虚拟机初始IP并不是都是`IPADDR=192.168.56.101`这样的配置。
- 调用`cat change_ip.sh |ssh root@192.168.56.110 "bash -s" "192.168.56.120"`命令，设置`ansible-master`虚拟机的IP。

编写一个`clone_vm.sh`脚本，内容如下：

```sh
#!/bin/bash
# filename: clone_vm.sh
# author:   meizhaohui
old_vmname=$1
new_vmname=$2
old_ip=$3
new_ip=$4
isrunning_flag=$(VBoxManage list runningvms|grep -c "${old_vmname}")
if [[ "${isrunning_flag}" -gt 0 ]]; then
    echo "${old_vmname} 虚拟机正在运行，禁止克隆，请退出"
    exit 1
else
    echo "${old_vmname} 虚拟机未运行，开始克隆"
fi
VBoxManage clonevm "${old_vmname}" --name "${new_vmname}" --register && echo "虚拟机 ${new_vmname} 克隆成功" || exit 2
echo "启动虚拟机 ${new_vmname}"
VBoxManage startvm "${new_vmname}" --type headless
sleep 60
# cat change_ip.sh |ssh root@192.168.56.110 "bash -s" "192.168.56.120"
cat change_ip.sh |ssh root@${old_ip} "bash -s" "${new_ip}"

```

然后再对`change_ip.sh`进行优化：

```sh
#!/bin/bash
# filename: change_ip.sh
# author:   meizhaohui
configfile=/etc/sysconfig/network-scripts/ifcfg-enp0s3
IP=$1
echo "待分配IP:${IP}"
echo "IP 修改前配置文件内容："
cat "${configfile}"
sed -i "s/^IPADDR=.*$/IPADDR=$IP/g" "${configfile}"
echo -e "\n=========================\n"
echo "IP 修改后配置文件内容："
cat "${configfile}"
echo "重启虚拟机。请使用新IP($IP)重新登陆。"
shutdown -r now

```

执行克隆脚本：

```sh
$ sh clone_vm.sh testvm1 "ansible-master" 192.168.56.110 192.168.56.120
```

中间会暂停60秒钟，让虚拟机完全启动成功。

![](/img/Snipaste_2023-12-01_00-18-05.png)

执行过程：

```sh
$ sh clone_vm.sh testvm1 "ansible-master" 192.168.56.110 192.168.56.120
testvm1 虚拟机未运行，开始克隆
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Machine has been successfully cloned as "ansible-master"
虚拟机 ansible-master 克隆成功
启动虚拟机 ansible-master
Waiting for VM "ansible-master" to power on...
VM "ansible-master" has been successfully started.
stty: standard input: Inappropriate ioctl for device
X11 forwarding request failed on channel 0
待分配IP:192.168.56.120
IP 修改前配置文件内容：
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp0s3
UUID=9ea09614-9750-4752-9dc6-d64f5535ea87
DEVICE=enp0s3
ONBOOT=yes
IPADDR=192.168.56.110

=========================

IP 修改后配置文件内容：
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=enp0s3
UUID=9ea09614-9750-4752-9dc6-d64f5535ea87
DEVICE=enp0s3
ONBOOT=yes
IPADDR=192.168.56.120
重启虚拟机。请使用新IP(192.168.56.120)重新登陆。
Connection to 192.168.56.110 closed by remote host.
stty: standard input: Inappropriate ioctl for device

```

![](/img/Snipaste_2023-12-01_00-22-00.png)

可以看到，虚拟机IP修改成功。修改为`192.168.56.120`了。



然后使用`ssh`远程连接一下：

```sh
$ ssh root@192.168.56.120
Warning: Permanently added '192.168.56.120' (RSA) to the list of known hosts.
root@192.168.56.120's password:
X11 forwarding request failed on channel 0
Last login: Wed Nov 29 23:50:33 2023 from 192.168.56.1
[root@localhost ~]# hostname -I
192.168.56.120 10.0.3.15
[root@localhost ~]# uptime
 00:23:17 up 4 min,  1 user,  load average: 0.01, 0.04, 0.03
[root@localhost ~]#
```

![](/img/Snipaste_2023-12-01_00-23-29.png)

可以看到，能够正常登陆，并执行命令。

在VirtualBox 界面也可以看到ansible-master虚拟机正常在运行：

![](/img/Snipaste_2023-12-01_00-25-14.png)

