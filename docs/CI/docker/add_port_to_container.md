# docker容器增加端口映射

[[toc]]

## 1. 查看需要增加端口映射的容器信息

查看当前运行的容器:

```sh
[root@node1 ~]$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS          PORTS                    NAMES
6f8cca028493   1e1d45f195b1   "sh -c ${SONATYPE_DI…"   15 months ago   Up 34 minutes   0.0.0.0:8081->8081/tcp   nexus
```

可以看到nexus当前开放了8081端口，我们想给该容器增加8082和8083两个新的端口映射，并开放8082和8083端口。

查看容器ID信息：

```sh
[root@node1 ~]$ docker inspect nexus|grep Id
        "Id": "6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44",
```

记住这个ID信息，后面需要用到。

查看docker数据文件存放目录：

```sh
[root@master docker]# docker info|grep 'Docker Root Dir:.*'|sed 's/.*Docker Root Dir: //g'
/var/lib/docker
```

我们要找的容器配置文件就在`/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44`目录下。

## 2. 停止容器和docker服务

首先停止所有启动的docker容器，如我们停止nexus容器：

```sh
[root@node1 ~]$ docker stop nexus
nexus
```

再停止docker和docker.socket服务：

```sh
[root@node1 ~]$ systemctl stop docker docker.socket
[root@node1 ~]# systemctl status docker docker.socket|grep -B 1 Active
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: inactive (dead) since Thu 2023-08-17 23:24:58 CST; 15min ago
--
   Loaded: loaded (/usr/lib/systemd/system/docker.socket; disabled; vendor preset: disabled)
   Active: inactive (dead) since Thu 2023-08-17 23:25:30 CST; 15min ago
[root@node1 ~]#
```

可以看到docker和docker.socket服务都已经停掉了。

## 3. 修改配置

切换到容器对应的配置文件所在目录：

```sh
[root@node1 ~]# cd /var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# ll
total 13632
-rw-r----- 1 root root 13919914 Aug 17 23:24 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44-json.log
drwx------ 2 root root     4096 May 18  2022 checkpoints
-rw------- 1 root root     4407 Aug 17 23:24 config.v2.json
-rw-r--r-- 1 root root     1516 Aug 17 23:24 hostconfig.json
-rw-r--r-- 1 root root       13 Aug 17 22:48 hostname
-rw-r--r-- 1 root root      174 Aug 17 22:48 hosts
drwx-----x 2 root root     4096 May 18  2022 mounts
-rw-r--r-- 1 root root       89 Aug 17 22:48 resolv.conf
-rw-r--r-- 1 root root       71 Aug 17 22:48 resolv.conf.hash
```

`hostconfig.json`和`config.v2.json`就是我们需要修改的配置文件。

修改前，先进行备份。

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cp config.v2.json config.v2.json.bak
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cp hostconfig.json hostconfig.json.bak
```

查看配置文件内容：

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat config.v2.json
{"StreamConfig":{},"State":{"Running":false,"Paused":false,"Restarting":false,"OOMKilled":false,"RemovalInProgress":false,"Dead":false,"Pid":0,"ExitCode":0,"Error":"","StartedAt":"2023-08-17T14:48:24.11259762Z","FinishedAt":"2023-08-17T15:24:30.829656318Z","Health":null},"ID":"6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44","Created":"2022-05-18T12:03:30.660030886Z","Managed":false,"Path":"sh","Args":["-c","${SONATYPE_DIR}/start-nexus-repository-manager.sh"],"Config":{"Hostname":"6f8cca028493","Domainname":"","User":"nexus","AttachStdin":false,"AttachStdout":false,"AttachStderr":false,"ExposedPorts":{"8081/tcp":{}},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","container=oci","SONATYPE_DIR=/opt/sonatype","NEXUS_HOME=/opt/sonatype/nexus","NEXUS_DATA=/nexus-data","NEXUS_CONTEXT=","SONATYPE_WORK=/opt/sonatype/sonatype-work","DOCKER_TYPE=3x-docker","INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m -Djava.util.prefs.userRoot=/nexus-data/javaprefs"],"Cmd":["sh","-c","${SONATYPE_DIR}/start-nexus-repository-manager.sh"],"Image":"1e1d45f195b1","Volumes":{"/nexus-data":{}},"WorkingDir":"","Entrypoint":null,"OnBuild":null,"Labels":{"architecture":"x86_64","build-date":"2022-02-25T17:38:34.854167","com.redhat.build-host":"cpt-1008.osbs.prod.upshift.rdu2.redhat.com","com.redhat.component":"ubi8-container","com.redhat.license_terms":"https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI","com.sonatype.license":"Apache License, Version 2.0","com.sonatype.name":"Nexus Repository Manager base image","description":"The Nexus Repository Manager server           with universal support for popular component formats.","distribution-scope":"public","io.k8s.description":"The Nexus Repository Manager server           with universal support for popular component formats.","io.k8s.display-name":"Nexus Repository Manager","io.openshift.expose-services":"8081:8081","io.openshift.tags":"Sonatype,Nexus,Repository Manager","maintainer":"Sonatype \u003csupport@sonatype.com\u003e","name":"Nexus Repository Manager","release":"3.38.0","run":"docker run -d --name NAME           -p 8081:8081           IMAGE","stop":"docker stop NAME","summary":"The Nexus Repository Manager server           with universal support for popular component formats.","url":"https://sonatype.com","vcs-ref":"3aadd00326f3dd6cfe65ee31017ab98915fddb56","vcs-type":"git","vendor":"Sonatype","version":"3.38.0-01"}},"Image":"sha256:1e1d45f195b19d03ec1833561dca6f5c63f9453413247c323c24f2fbcc34bcdd","NetworkSettings":{"Bridge":"","SandboxID":"7e28c67920e8bc79c58b7e31118928877a9c52f40c19387722ff0f9cf6670420","HairpinMode":false,"LinkLocalIPv6Address":"","LinkLocalIPv6PrefixLen":0,"Networks":{"bridge":{"IPAMConfig":null,"Links":null,"Aliases":null,"NetworkID":"f9287debf1297b555d91930887c969c4267af27bd705881987bfc29e4397ee33","EndpointID":"","Gateway":"","IPAddress":"","IPPrefixLen":0,"IPv6Gateway":"","GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"MacAddress":"","DriverOpts":null,"IPAMOperational":false}},"Service":null,"Ports":null,"SandboxKey":"/var/run/docker/netns/7e28c67920e8","SecondaryIPAddresses":null,"SecondaryIPv6Addresses":null,"IsAnonymousEndpoint":false,"HasSwarmEndpoint":false},"LogPath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44-json.log","Name":"/nexus","Driver":"overlay2","OS":"linux","MountLabel":"","ProcessLabel":"","RestartCount":0,"HasBeenStartedBefore":true,"HasBeenManuallyStopped":true,"MountPoints":{"/nexus-data":{"Source":"","Destination":"/nexus-data","RW":true,"Name":"9bbc74c98f84acf7e2ee07978b71c364096685ad0b7e610e6856da7690d90189","Driver":"local","Type":"volume","Spec":{},"SkipMountpointCreation":false}},"SecretReferences":null,"ConfigReferences":null,"AppArmorProfile":"","HostnamePath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/hostname","HostsPath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/hosts","ShmPath":"","ResolvConfPath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/resolv.conf","SeccompProfile":"","NoNewPrivileges":false,"LocalLogCacheMeta":{"HaveNotifyEnabled":false}}
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat hostconfig.json
{"Binds":null,"ContainerIDFile":"","LogConfig":{"Type":"json-file","Config":{}},"NetworkMode":"default","PortBindings":{"8081/tcp":[{"HostIp":"","HostPort":"8081"}]},"RestartPolicy":{"Name":"no","MaximumRetryCount":0},"AutoRemove":false,"VolumeDriver":"","VolumesFrom":null,"CapAdd":null,"CapDrop":null,"CgroupnsMode":"host","Dns":[],"DnsOptions":[],"DnsSearch":[],"ExtraHosts":null,"GroupAdd":null,"IpcMode":"private","Cgroup":"","Links":null,"OomScoreAdj":0,"PidMode":"","Privileged":false,"PublishAllPorts":false,"ReadonlyRootfs":false,"SecurityOpt":null,"UTSMode":"","UsernsMode":"","ShmSize":67108864,"Runtime":"runc","ConsoleSize":[0,0],"Isolation":"","CpuShares":0,"Memory":0,"NanoCpus":0,"CgroupParent":"","BlkioWeight":0,"BlkioWeightDevice":[],"BlkioDeviceReadBps":null,"BlkioDeviceWriteBps":null,"BlkioDeviceReadIOps":null,"BlkioDeviceWriteIOps":null,"CpuPeriod":0,"CpuQuota":0,"CpuRealtimePeriod":0,"CpuRealtimeRuntime":0,"CpusetCpus":"","CpusetMems":"","Devices":[],"DeviceCgroupRules":null,"DeviceRequests":null,"KernelMemory":0,"KernelMemoryTCP":0,"MemoryReservation":0,"MemorySwap":0,"MemorySwappiness":null,"OomKillDisable":false,"PidsLimit":null,"Ulimits":null,"CpuCount":0,"CpuPercent":0,"IOMaximumIOps":0,"IOMaximumBandwidth":0,"MaskedPaths":["/proc/asound","/proc/acpi","/proc/kcore","/proc/keys","/proc/latency_stats","/proc/timer_list","/proc/timer_stats","/proc/sched_debug","/proc/scsi","/sys/firmware"],"ReadonlyPaths":["/proc/bus","/proc/fs","/proc/irq","/proc/sys","/proc/sysrq-trigger"]}
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]#
```

可以看到，配置文件内容是压缩后的json文件，不便于观察和修改。我们使用jq工具美化后，导入到新文件，然后再进行修改：

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat config.v2.json |jq > config.v2.jq.json
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat config.v2.jq.json
{
  "StreamConfig": {},
  "State": {
    "Running": false,
    "Paused": false,
    "Restarting": false,
    "OOMKilled": false,
    "RemovalInProgress": false,
    "Dead": false,
    "Pid": 0,
    "ExitCode": 0,
    "Error": "",
    "StartedAt": "2023-08-17T14:48:24.11259762Z",
    "FinishedAt": "2023-08-17T15:24:30.829656318Z",
    "Health": null
  },
  "ID": "6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44",
  "Created": "2022-05-18T12:03:30.660030886Z",
  "Managed": false,
  "Path": "sh",
  "Args": [
    "-c",
    "${SONATYPE_DIR}/start-nexus-repository-manager.sh"
  ],
  "Config": {
    "Hostname": "6f8cca028493",
    "Domainname": "",
    "User": "nexus",
    "AttachStdin": false,
    "AttachStdout": false,
    "AttachStderr": false,
    "ExposedPorts": {
      "8081/tcp": {}
    },
    "Tty": false,
    "OpenStdin": false,
    "StdinOnce": false,
    "Env": [
      "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
      "container=oci",
      "SONATYPE_DIR=/opt/sonatype",
      "NEXUS_HOME=/opt/sonatype/nexus",
      "NEXUS_DATA=/nexus-data",
      "NEXUS_CONTEXT=",
      "SONATYPE_WORK=/opt/sonatype/sonatype-work",
      "DOCKER_TYPE=3x-docker",
      "INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m -Djava.util.prefs.userRoot=/nexus-data/javaprefs"
    ],
    "Cmd": [
      "sh",
      "-c",
      "${SONATYPE_DIR}/start-nexus-repository-manager.sh"
    ],
    "Image": "1e1d45f195b1",
    "Volumes": {
      "/nexus-data": {}
    },
    "WorkingDir": "",
    "Entrypoint": null,
    "OnBuild": null,
    "Labels": {
      "architecture": "x86_64",
      "build-date": "2022-02-25T17:38:34.854167",
      "com.redhat.build-host": "cpt-1008.osbs.prod.upshift.rdu2.redhat.com",
      "com.redhat.component": "ubi8-container",
      "com.redhat.license_terms": "https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI",
      "com.sonatype.license": "Apache License, Version 2.0",
      "com.sonatype.name": "Nexus Repository Manager base image",
      "description": "The Nexus Repository Manager server           with universal support for popular component formats.",
      "distribution-scope": "public",
      "io.k8s.description": "The Nexus Repository Manager server           with universal support for popular component formats.",
      "io.k8s.display-name": "Nexus Repository Manager",
      "io.openshift.expose-services": "8081:8081",
      "io.openshift.tags": "Sonatype,Nexus,Repository Manager",
      "maintainer": "Sonatype <support@sonatype.com>",
      "name": "Nexus Repository Manager",
      "release": "3.38.0",
      "run": "docker run -d --name NAME           -p 8081:8081           IMAGE",
      "stop": "docker stop NAME",
      "summary": "The Nexus Repository Manager server           with universal support for popular component formats.",
      "url": "https://sonatype.com",
      "vcs-ref": "3aadd00326f3dd6cfe65ee31017ab98915fddb56",
      "vcs-type": "git",
      "vendor": "Sonatype",
      "version": "3.38.0-01"
    }
  },
  "Image": "sha256:1e1d45f195b19d03ec1833561dca6f5c63f9453413247c323c24f2fbcc34bcdd",
  "NetworkSettings": {
    "Bridge": "",
    "SandboxID": "7e28c67920e8bc79c58b7e31118928877a9c52f40c19387722ff0f9cf6670420",
    "HairpinMode": false,
    "LinkLocalIPv6Address": "",
    "LinkLocalIPv6PrefixLen": 0,
    "Networks": {
      "bridge": {
        "IPAMConfig": null,
        "Links": null,
        "Aliases": null,
        "NetworkID": "f9287debf1297b555d91930887c969c4267af27bd705881987bfc29e4397ee33",
        "EndpointID": "",
        "Gateway": "",
        "IPAddress": "",
        "IPPrefixLen": 0,
        "IPv6Gateway": "",
        "GlobalIPv6Address": "",
        "GlobalIPv6PrefixLen": 0,
        "MacAddress": "",
        "DriverOpts": null,
        "IPAMOperational": false
      }
    },
    "Service": null,
    "Ports": null,
    "SandboxKey": "/var/run/docker/netns/7e28c67920e8",
    "SecondaryIPAddresses": null,
    "SecondaryIPv6Addresses": null,
    "IsAnonymousEndpoint": false,
    "HasSwarmEndpoint": false
  },
  "LogPath": "/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44-json.log",
  "Name": "/nexus",
  "Driver": "overlay2",
  "OS": "linux",
  "MountLabel": "",
  "ProcessLabel": "",
  "RestartCount": 0,
  "HasBeenStartedBefore": true,
  "HasBeenManuallyStopped": true,
  "MountPoints": {
    "/nexus-data": {
      "Source": "",
      "Destination": "/nexus-data",
      "RW": true,
      "Name": "9bbc74c98f84acf7e2ee07978b71c364096685ad0b7e610e6856da7690d90189",
      "Driver": "local",
      "Type": "volume",
      "Spec": {},
      "SkipMountpointCreation": false
    }
  },
  "SecretReferences": null,
  "ConfigReferences": null,
  "AppArmorProfile": "",
  "HostnamePath": "/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/hostname",
  "HostsPath": "/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/hosts",
  "ShmPath": "",
  "ResolvConfPath": "/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/resolv.conf",
  "SeccompProfile": "",
  "NoNewPrivileges": false,
  "LocalLogCacheMeta": {
    "HaveNotifyEnabled": false
  }
}
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]#
```

`hostconfig.json`配置文件也是一样的操作：

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat hostconfig.json |jq > hostconfig.jq.json
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat hostconfig.jq.json
{
  "Binds": null,
  "ContainerIDFile": "",
  "LogConfig": {
    "Type": "json-file",
    "Config": {}
  },
  "NetworkMode": "default",
  "PortBindings": {
    "8081/tcp": [
      {
        "HostIp": "",
        "HostPort": "8081"
      }
    ]
  },
  "RestartPolicy": {
    "Name": "no",
    "MaximumRetryCount": 0
  },
  "AutoRemove": false,
  "VolumeDriver": "",
  "VolumesFrom": null,
  "CapAdd": null,
  "CapDrop": null,
  "CgroupnsMode": "host",
  "Dns": [],
  "DnsOptions": [],
  "DnsSearch": [],
  "ExtraHosts": null,
  "GroupAdd": null,
  "IpcMode": "private",
  "Cgroup": "",
  "Links": null,
  "OomScoreAdj": 0,
  "PidMode": "",
  "Privileged": false,
  "PublishAllPorts": false,
  "ReadonlyRootfs": false,
  "SecurityOpt": null,
  "UTSMode": "",
  "UsernsMode": "",
  "ShmSize": 67108864,
  "Runtime": "runc",
  "ConsoleSize": [
    0,
    0
  ],
  "Isolation": "",
  "CpuShares": 0,
  "Memory": 0,
  "NanoCpus": 0,
  "CgroupParent": "",
  "BlkioWeight": 0,
  "BlkioWeightDevice": [],
  "BlkioDeviceReadBps": null,
  "BlkioDeviceWriteBps": null,
  "BlkioDeviceReadIOps": null,
  "BlkioDeviceWriteIOps": null,
  "CpuPeriod": 0,
  "CpuQuota": 0,
  "CpuRealtimePeriod": 0,
  "CpuRealtimeRuntime": 0,
  "CpusetCpus": "",
  "CpusetMems": "",
  "Devices": [],
  "DeviceCgroupRules": null,
  "DeviceRequests": null,
  "KernelMemory": 0,
  "KernelMemoryTCP": 0,
  "MemoryReservation": 0,
  "MemorySwap": 0,
  "MemorySwappiness": null,
  "OomKillDisable": false,
  "PidsLimit": null,
  "Ulimits": null,
  "CpuCount": 0,
  "CpuPercent": 0,
  "IOMaximumIOps": 0,
  "IOMaximumBandwidth": 0,
  "MaskedPaths": [
    "/proc/asound",
    "/proc/acpi",
    "/proc/kcore",
    "/proc/keys",
    "/proc/latency_stats",
    "/proc/timer_list",
    "/proc/timer_stats",
    "/proc/sched_debug",
    "/proc/scsi",
    "/sys/firmware"
  ],
  "ReadonlyPaths": [
    "/proc/bus",
    "/proc/fs",
    "/proc/irq",
    "/proc/sys",
    "/proc/sysrq-trigger"
  ]
}
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]#
```

先修改`hostconfig.jq.json`配置文件，可以看到，在9行的`PortBindings`配置属性下，已经有一个8081端口的配置，也就是10-15行的内容，我们复制一下，然后在下面新增8082和8083端口配置：

![](/img/Snipaste_2023-08-18_00-07-58.png)

修改完成后，查看配置内容，注意`"8082/tcp"`和`"8083/tcp"`上一行末尾的逗号不要忘记了：

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# grep -A20 PortBindings hostconfig.jq.json
  "PortBindings": {
    "8081/tcp": [
      {
        "HostIp": "",
        "HostPort": "8081"
      }
    ],
    "8082/tcp": [
      {
        "HostIp": "",
        "HostPort": "8082"
      }
    ],
    "8083/tcp": [
      {
        "HostIp": "",
        "HostPort": "8083"
      }
    ]
  },
  "RestartPolicy": {
```


接着修改`config.v2.jq.json`, 找到`ExposedPorts`仿照之前内容添加端口映射:

修改后内容如下：

![](/img/Snipaste_2023-08-18_00-02-02.png)

查看修改后的内容：

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# grep -A4 ExposedPorts config.v2.jq.json
    "ExposedPorts": {
      "8081/tcp": {},
      "8082/tcp": {},
      "8083/tcp": {}
    },
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]#
```

将修改好的配置写入到默认配置中：

```sh
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat hostconfig.jq.json|jq -c
{"Binds":null,"ContainerIDFile":"","LogConfig":{"Type":"json-file","Config":{}},"NetworkMode":"default","PortBindings":{"8081/tcp":[{"HostIp":"","HostPort":"8081"}],"8082/tcp":[{"HostIp":"","HostPort":"8082"}],"8083/tcp":[{"HostIp":"","HostPort":"8083"}]},"RestartPolicy":{"Name":"no","MaximumRetryCount":0},"AutoRemove":false,"VolumeDriver":"","VolumesFrom":null,"CapAdd":null,"CapDrop":null,"CgroupnsMode":"host","Dns":[],"DnsOptions":[],"DnsSearch":[],"ExtraHosts":null,"GroupAdd":null,"IpcMode":"private","Cgroup":"","Links":null,"OomScoreAdj":0,"PidMode":"","Privileged":false,"PublishAllPorts":false,"ReadonlyRootfs":false,"SecurityOpt":null,"UTSMode":"","UsernsMode":"","ShmSize":67108864,"Runtime":"runc","ConsoleSize":[0,0],"Isolation":"","CpuShares":0,"Memory":0,"NanoCpus":0,"CgroupParent":"","BlkioWeight":0,"BlkioWeightDevice":[],"BlkioDeviceReadBps":null,"BlkioDeviceWriteBps":null,"BlkioDeviceReadIOps":null,"BlkioDeviceWriteIOps":null,"CpuPeriod":0,"CpuQuota":0,"CpuRealtimePeriod":0,"CpuRealtimeRuntime":0,"CpusetCpus":"","CpusetMems":"","Devices":[],"DeviceCgroupRules":null,"DeviceRequests":null,"KernelMemory":0,"KernelMemoryTCP":0,"MemoryReservation":0,"MemorySwap":0,"MemorySwappiness":null,"OomKillDisable":false,"PidsLimit":null,"Ulimits":null,"CpuCount":0,"CpuPercent":0,"IOMaximumIOps":0,"IOMaximumBandwidth":0,"MaskedPaths":["/proc/asound","/proc/acpi","/proc/kcore","/proc/keys","/proc/latency_stats","/proc/timer_list","/proc/timer_stats","/proc/sched_debug","/proc/scsi","/sys/firmware"],"ReadonlyPaths":["/proc/bus","/proc/fs","/proc/irq","/proc/sys","/proc/sysrq-trigger"]}
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat hostconfig.jq.json|jq -c > hostconfig.json
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat config.v2.jq.json |jq -c
{"StreamConfig":{},"State":{"Running":false,"Paused":false,"Restarting":false,"OOMKilled":false,"RemovalInProgress":false,"Dead":false,"Pid":0,"ExitCode":0,"Error":"","StartedAt":"2023-08-17T14:48:24.11259762Z","FinishedAt":"2023-08-17T15:24:30.829656318Z","Health":null},"ID":"6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44","Created":"2022-05-18T12:03:30.660030886Z","Managed":false,"Path":"sh","Args":["-c","${SONATYPE_DIR}/start-nexus-repository-manager.sh"],"Config":{"Hostname":"6f8cca028493","Domainname":"","User":"nexus","AttachStdin":false,"AttachStdout":false,"AttachStderr":false,"ExposedPorts":{"8081/tcp":{},"8082/tcp":{},"8083/tcp":{}},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin","container=oci","SONATYPE_DIR=/opt/sonatype","NEXUS_HOME=/opt/sonatype/nexus","NEXUS_DATA=/nexus-data","NEXUS_CONTEXT=","SONATYPE_WORK=/opt/sonatype/sonatype-work","DOCKER_TYPE=3x-docker","INSTALL4J_ADD_VM_PARAMS=-Xms2703m -Xmx2703m -XX:MaxDirectMemorySize=2703m -Djava.util.prefs.userRoot=/nexus-data/javaprefs"],"Cmd":["sh","-c","${SONATYPE_DIR}/start-nexus-repository-manager.sh"],"Image":"1e1d45f195b1","Volumes":{"/nexus-data":{}},"WorkingDir":"","Entrypoint":null,"OnBuild":null,"Labels":{"architecture":"x86_64","build-date":"2022-02-25T17:38:34.854167","com.redhat.build-host":"cpt-1008.osbs.prod.upshift.rdu2.redhat.com","com.redhat.component":"ubi8-container","com.redhat.license_terms":"https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI","com.sonatype.license":"Apache License, Version 2.0","com.sonatype.name":"Nexus Repository Manager base image","description":"The Nexus Repository Manager server           with universal support for popular component formats.","distribution-scope":"public","io.k8s.description":"The Nexus Repository Manager server           with universal support for popular component formats.","io.k8s.display-name":"Nexus Repository Manager","io.openshift.expose-services":"8081:8081","io.openshift.tags":"Sonatype,Nexus,Repository Manager","maintainer":"Sonatype <support@sonatype.com>","name":"Nexus Repository Manager","release":"3.38.0","run":"docker run -d --name NAME           -p 8081:8081           IMAGE","stop":"docker stop NAME","summary":"The Nexus Repository Manager server           with universal support for popular component formats.","url":"https://sonatype.com","vcs-ref":"3aadd00326f3dd6cfe65ee31017ab98915fddb56","vcs-type":"git","vendor":"Sonatype","version":"3.38.0-01"}},"Image":"sha256:1e1d45f195b19d03ec1833561dca6f5c63f9453413247c323c24f2fbcc34bcdd","NetworkSettings":{"Bridge":"","SandboxID":"7e28c67920e8bc79c58b7e31118928877a9c52f40c19387722ff0f9cf6670420","HairpinMode":false,"LinkLocalIPv6Address":"","LinkLocalIPv6PrefixLen":0,"Networks":{"bridge":{"IPAMConfig":null,"Links":null,"Aliases":null,"NetworkID":"f9287debf1297b555d91930887c969c4267af27bd705881987bfc29e4397ee33","EndpointID":"","Gateway":"","IPAddress":"","IPPrefixLen":0,"IPv6Gateway":"","GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"MacAddress":"","DriverOpts":null,"IPAMOperational":false}},"Service":null,"Ports":null,"SandboxKey":"/var/run/docker/netns/7e28c67920e8","SecondaryIPAddresses":null,"SecondaryIPv6Addresses":null,"IsAnonymousEndpoint":false,"HasSwarmEndpoint":false},"LogPath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44-json.log","Name":"/nexus","Driver":"overlay2","OS":"linux","MountLabel":"","ProcessLabel":"","RestartCount":0,"HasBeenStartedBefore":true,"HasBeenManuallyStopped":true,"MountPoints":{"/nexus-data":{"Source":"","Destination":"/nexus-data","RW":true,"Name":"9bbc74c98f84acf7e2ee07978b71c364096685ad0b7e610e6856da7690d90189","Driver":"local","Type":"volume","Spec":{},"SkipMountpointCreation":false}},"SecretReferences":null,"ConfigReferences":null,"AppArmorProfile":"","HostnamePath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/hostname","HostsPath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/hosts","ShmPath":"","ResolvConfPath":"/var/lib/docker/containers/6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44/resolv.conf","SeccompProfile":"","NoNewPrivileges":false,"LocalLogCacheMeta":{"HaveNotifyEnabled":false}}
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]# cat config.v2.jq.json |jq -c > config.v2.json
[root@node1 6f8cca02849370b4c271511229f36a5a0b76d20ba5b8e8391564c5d3bd0c1f44]#
```

## 4. 重启docker服务和容器

```sh
[root@node1 ~]# systemctl start docker docker.socket
[root@node1 ~]# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
[root@node1 ~]# docker start nexus
nexus
[root@node1 ~]# docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                              NAMES
6f8cca028493   1e1d45f195b1   "sh -c ${SONATYPE_DI…"   15 months ago   Up 2 seconds   0.0.0.0:8081-8083->8081-8083/tcp   nexus
[root@node1 ~]#
```

此时，查看端口监听情况：

```sh
[root@node1 ~]# netstat -tunlp|grep docker
tcp        0      0 0.0.0.0:8081            0.0.0.0:*               LISTEN      7895/docker-proxy
tcp        0      0 0.0.0.0:8082            0.0.0.0:*               LISTEN      7884/docker-proxy
tcp        0      0 0.0.0.0:8083            0.0.0.0:*               LISTEN      7871/docker-proxy
[root@node1 ~]#
```

可以看到8082和8083端口也监听了，说明容器增加端口映射配置成功了！

