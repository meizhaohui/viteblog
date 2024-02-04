# 获取k8s集群组件状态`kubectl get cs`

[[toc]]

## 1. 查看组件状态信息
kubernetes集群的基本搭建，请参考[K8S集群部署](./deploy.md)。

之前我设置了快捷命令：
```sh
alias k8let='kubelet'
alias k8adm='kubeadm'
alias k8ctl='kubectl'
```

在k8s集群基本配置好后，可以查看k8s集群组件当前的状态信息。

```sh
[root@k8s-master ~]# k8ctl get cs
NAME                 STATUS      MESSAGE
controller-manager   Unhealthy   Get http://127.0.0.1:10252/healthz: dial tcp 127.0.0.1:10252: connect: connection refused
scheduler            Unhealthy   Get http://127.0.0.1:10251/healthz: dial tcp 127.0.0.1:10251: connect: connection refused
etcd-0               Healthy     {"health":"true"}
```

或者使用非简写命令：
```sh
[root@k8s-master ~]# k8ctl get componentstatuses
NAME                 STATUS      MESSAGE
controller-manager   Unhealthy   Get http://127.0.0.1:10252/healthz: dial tcp 127.0.0.1:10252: connect: connection refused
scheduler            Unhealthy   Get http://127.0.0.1:10251/healthz: dial tcp 127.0.0.1:10251: connect: connection refused
etcd-0               Healthy     {"health":"true"}
```

可以看到，`controller-manager`和`scheduler`的状态是`Unhealthy`不健康的。

## 2. 问题分析与处理

按参考文档1进行设置修改。

**这种情况是因为kube-controller-manager.yaml和kube-scheduler.yaml 里面配置了默认端口0。**

切换到`/etc/kubernetes/manifests`目录下，并查看目录文件列表：
```sh
[root@k8s-master ~]# cd /etc/kubernetes/manifests
[root@k8s-master manifests]# ll
total 16
-rw------- 1 root root 1887 Nov 22 20:50 etcd.yaml
-rw------- 1 root root 2739 Nov 22 20:50 kube-apiserver.yaml
-rw------- 1 root root 2595 Nov 29 17:24 kube-controller-manager.yaml
-rw------- 1 root root 1150 Nov 29 17:24 kube-scheduler.yaml
[root@k8s-master manifests]#
```

修改前请备份配置文件，我们直接在当前目录备份：
```sh
[root@k8s-master manifests]# cp kube-controller-manager.yaml{,.bak}
[root@k8s-master manifests]# cp kube-scheduler.yaml{,.bak}
```

查看配置文件`kube-controller-manager.yaml`原始内容：
```sh
[root@k8s-master manifests]# cat kube-controller-manager.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: kube-controller-manager
    tier: control-plane
  name: kube-controller-manager
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-controller-manager
    - --allocate-node-cidrs=true
    - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --bind-address=127.0.0.1
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --cluster-cidr=10.244.0.0/16
    - --cluster-name=kubernetes
    - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
    - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
    - --controllers=*,bootstrapsigner,tokencleaner
    - --kubeconfig=/etc/kubernetes/controller-manager.conf
    - --leader-elect=true
    - --node-cidr-mask-size=24
    - --port=0
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --root-ca-file=/etc/kubernetes/pki/ca.crt
    - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
    - --service-cluster-ip-range=10.96.0.0/12
    - --use-service-account-credentials=true
    image: registry.aliyuncs.com/google_containers/kube-controller-manager:v1.18.20
    imagePullPolicy: IfNotPresent
    livenessProbe:
      failureThreshold: 8
      httpGet:
        host: 127.0.0.1
        path: /healthz
        port: 10257
        scheme: HTTPS
      initialDelaySeconds: 15
      timeoutSeconds: 15
    name: kube-controller-manager
    resources:
      requests:
        cpu: 200m
    volumeMounts:
    - mountPath: /etc/ssl/certs
      name: ca-certs
      readOnly: true
    - mountPath: /etc/pki
      name: etc-pki
      readOnly: true
    - mountPath: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
      name: flexvolume-dir
    - mountPath: /etc/kubernetes/pki
      name: k8s-certs
      readOnly: true
    - mountPath: /etc/kubernetes/controller-manager.conf
      name: kubeconfig
      readOnly: true
  hostNetwork: true
  priorityClassName: system-cluster-critical
  volumes:
  - hostPath:
      path: /etc/ssl/certs
      type: DirectoryOrCreate
    name: ca-certs
  - hostPath:
      path: /etc/pki
      type: DirectoryOrCreate
    name: etc-pki
  - hostPath:
      path: /usr/libexec/kubernetes/kubelet-plugins/volume/exec
      type: DirectoryOrCreate
    name: flexvolume-dir
  - hostPath:
      path: /etc/kubernetes/pki
      type: DirectoryOrCreate
    name: k8s-certs
  - hostPath:
      path: /etc/kubernetes/controller-manager.conf
      type: FileOrCreate
    name: kubeconfig
status: {}
[root@k8s-master manifests]#
```
将文件中27行的`- --port=0`删除掉，然后保存文件。

查看配置文件`kube-scheduler.yaml`原始内容：
```sh
[root@k8s-master manifests]# cat kube-scheduler.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: kube-scheduler
    tier: control-plane
  name: kube-scheduler
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-scheduler
    - --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
    - --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
    - --bind-address=127.0.0.1
    - --kubeconfig=/etc/kubernetes/scheduler.conf
    - --leader-elect=true
    - --port=0
    image: registry.aliyuncs.com/google_containers/kube-scheduler:v1.18.20
    imagePullPolicy: IfNotPresent
    livenessProbe:
      failureThreshold: 8
      httpGet:
        host: 127.0.0.1
        path: /healthz
        port: 10259
        scheme: HTTPS
      initialDelaySeconds: 15
      timeoutSeconds: 15
    name: kube-scheduler
    resources:
      requests:
        cpu: 100m
    volumeMounts:
    - mountPath: /etc/kubernetes/scheduler.conf
      name: kubeconfig
      readOnly: true
  hostNetwork: true
  priorityClassName: system-cluster-critical
  volumes:
  - hostPath:
      path: /etc/kubernetes/scheduler.conf
      type: FileOrCreate
    name: kubeconfig
status: {}
[root@k8s-master manifests]#
```
删除19行的` - --port=0`，然后保存文件。

修改完成后，对比差异：
```sh
[root@k8s-master manifests]# diff kube-controller-manager.yaml kube-controller-manager.yaml.bak
26a27
>     - --port=0
[root@k8s-master manifests]# diff kube-scheduler.yaml kube-scheduler.yaml.bak
18a19
>     - --port=0
[root@k8s-master manifests]#
```

重启master的`kubelet`服务，并查看组件状态信息。
```sh
# 重启kubelet服务
[root@k8s-master manifests]# systemctl restart kubelet

# 查看集群组件状态信息
[root@k8s-master manifests]# k8ctl get cs
NAME                 STATUS      MESSAGE                                                                                     ERROR
scheduler            Unhealthy   Get http://127.0.0.1:10251/healthz: dial tcp 127.0.0.1:10251: connect: connection refused
controller-manager   Unhealthy   Get http://127.0.0.1:10252/healthz: dial tcp 127.0.0.1:10252: connect: connection refused
etcd-0               Healthy     {"health":"true"}
[root@k8s-master manifests]#
```

此时，可以看到，状态信息仍然还是不健康的！！

::: warning 警告
对文件操作进行编辑需要提前进行备份，建议将备份文件放到`/tmp`或者`/root`目录下，避免放到同一目录后重启kubelet问题还会复现而无法解决
:::

由于我们是在`/etc/kubernetes/manifests`进行的文件备份，我们将备份文件移动到`/root/backup_data`目录去：
```sh
[root@k8s-master manifests]# mkdir ~/backup_data
[root@k8s-master manifests]# ll
total 24
-rw------- 1 root root 1887 Nov 22 20:50 etcd.yaml
-rw------- 1 root root 2739 Nov 22 20:50 kube-apiserver.yaml
-rw------- 1 root root 2595 Nov 29 17:24 kube-controller-manager.yaml
-rw------- 1 root root 2610 Nov 29 18:56 kube-controller-manager.yaml.bak
-rw------- 1 root root 1150 Nov 29 17:24 kube-scheduler.yaml
-rw------- 1 root root 1165 Nov 29 18:56 kube-scheduler.yaml.bak
[root@k8s-master manifests]# mv *.bak ~/backup_data/
[root@k8s-master manifests]# ll
total 16
-rw------- 1 root root 1887 Nov 22 20:50 etcd.yaml
-rw------- 1 root root 2739 Nov 22 20:50 kube-apiserver.yaml
-rw------- 1 root root 2595 Nov 29 17:24 kube-controller-manager.yaml
-rw------- 1 root root 1150 Nov 29 17:24 kube-scheduler.yaml
[root@k8s-master manifests]#
```

然后再重启`kubelet`服务:
```sh
[root@k8s-master ~]# systemctl restart kubelet
```

## 3. 验证

重启`kubelet`服务后，再次查看集群组件状态信息：
```sh
[root@k8s-master ~]# k8ctl get cs
NAME                 STATUS    MESSAGE             ERROR
scheduler            Healthy   ok
controller-manager   Healthy   ok
etcd-0               Healthy   {"health":"true"}
[root@k8s-master ~]#
```

可以看到，集群组件状态已经变成健康状态了！！说明配置正确！


**如果有多个master节点，则每台master节点都要执行操作。**






参考：

- [k8s 检查集群状态提示Get http://127.0.0.1:10251/healthz: dial tcp 127.0.0.1:10251: connect: connection refuse](https://blog.csdn.net/hedao0515/article/details/125993695)