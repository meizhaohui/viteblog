# 获取k8s集群节点状态`kubectl get nodes`

[[toc]]

## 1. 查看集群节点状态信息
kubernetes集群的基本搭建，请参考[K8S集群部署](./deploy.md)。

之前我设置了快捷命令：
```sh
alias k8let='kubelet'
alias k8adm='kubeadm'
alias k8ctl='kubectl'
```

在k8s集群基本配置好后，可以查看k8s集群节点的状态信息。

```sh
[root@k8s-master ~]# k8ctl get nodes
NAME         STATUS   ROLES    AGE     VERSION
k8s-master   Ready    master   7d15h   v1.18.20
k8s-node1    Ready    <none>   7d14h   v1.18.20
k8s-node2    Ready    <none>   7d14h   v1.18.20
```

获取帮助信息：
```sh
[root@k8s-master ~]# k8ctl get nodes --help
Display one or many resources

 Prints a table of the most important information about the specified resources. You can filter the list using a label
selector and the --selector flag. If the desired resource type is namespaced you will only see results in your current
namespace unless you pass --all-namespaces.

 Uninitialized objects are not shown unless --include-uninitialized is passed.

 By specifying the output as 'template' and providing a Go template as the value of the --template flag, you can filter
the attributes of the fetched resources.

Use "kubectl api-resources" for a complete list of supported resources.

Examples:
  # List all pods in ps output format.
  kubectl get pods

  # List all pods in ps output format with more information (such as node name).
  kubectl get pods -o wide

  # List a single replication controller with specified NAME in ps output format.
  kubectl get replicationcontroller web

  # List deployments in JSON output format, in the "v1" version of the "apps" API group:
  kubectl get deployments.v1.apps -o json

  # List a single pod in JSON output format.
  kubectl get -o json pod web-pod-13je7

  # List a pod identified by type and name specified in "pod.yaml" in JSON output format.
  kubectl get -f pod.yaml -o json

  # List resources from a directory with kustomization.yaml - e.g. dir/kustomization.yaml.
  kubectl get -k dir/

  # Return only the phase value of the specified pod.
  kubectl get -o template pod/web-pod-13je7 --template={{.status.phase}}

  # List resource information in custom columns.
  kubectl get pod test-pod -o custom-columns=CONTAINER:.spec.containers[0].name,IMAGE:.spec.containers[0].image

  # List all replication controllers and services together in ps output format.
  kubectl get rc,services

  # List one or more resources by their type and names.
  kubectl get rc/web service/frontend pods/web-pod-13je7

Options:
  -A, --all-namespaces=false: If present, list the requested object(s) across all namespaces. Namespace in current
context is ignored even if specified with --namespace.
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --chunk-size=500: Return large lists in chunks rather than all at once. Pass 0 to disable. This flag is beta and
may change in the future.
      --field-selector='': Selector (field query) to filter on, supports '=', '==', and '!='.(e.g. --field-selector
key1=value1,key2=value2). The server only supports a limited number of field queries per type.
  -f, --filename=[]: Filename, directory, or URL to files identifying the resource to get from a server.
      --ignore-not-found=false: If the requested object does not exist the command will return exit code 0.
  -k, --kustomize='': Process the kustomization directory. This flag can't be used together with -f or -R.
  -L, --label-columns=[]: Accepts a comma separated list of labels that are going to be presented as columns. Names are
case-sensitive. You can also use multiple flag options like -L label1 -L label2...
      --no-headers=false: When using the default or custom-column output format, don't print headers (default print
headers).
  -o, --output='': Output format. One of:
json|yaml|wide|name|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...
See custom columns [http://kubernetes.io/docs/user-guide/kubectl-overview/#custom-columns], golang template
[http://golang.org/pkg/text/template/#pkg-overview] and jsonpath template
[http://kubernetes.io/docs/user-guide/jsonpath].
      --output-watch-events=false: Output watch event objects when --watch or --watch-only is used. Existing objects are
output as initial ADDED events.
      --raw='': Raw URI to request from the server.  Uses the transport specified by the kubeconfig file.
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
  -l, --selector='': Selector (label query) to filter on, supports '=', '==', and '!='.(e.g. -l key1=value1,key2=value2)
      --server-print=true: If true, have the server return the appropriate table output. Supports extension APIs and
CRDs.
      --show-kind=false: If present, list the resource type for the requested object(s).
      --show-labels=false: When printing, show all labels as the last column (default hide labels column)
      --sort-by='': If non-empty, sort list types using this field specification.  The field specification is expressed
as a JSONPath expression (e.g. '{.metadata.name}'). The field in the API resource specified by this JSONPath expression
must be an integer or a string.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
  -w, --watch=false: After listing/getting the requested object, watch for changes. Uninitialized objects are excluded
if no object name is provided.
      --watch-only=false: Watch for changes to the requested object(s), without listing/getting first.

Usage:
  kubectl get
[(-o|--output=)json|yaml|wide|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...]
(TYPE[.VERSION][.GROUP] [NAME | -l label] | TYPE[.VERSION][.GROUP]/NAME ...) [flags] [options]

Use "kubectl options" for a list of global command-line options (applies to all commands).
[root@k8s-master ~]#
```

获取节点状态更多信息：
```sh
[root@k8s-master ~]# k8ctl get nodes -o wide
NAME         STATUS   ROLES    AGE   VERSION    INTERNAL-IP     EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION           CONTAINER-RUNTIME
k8s-master   Ready    master   8d    v1.18.20   192.168.56.60   <none>        CentOS Linux 7 (Core)   3.10.0-1062.el7.x86_64   docker://20.10.21
k8s-node1    Ready    <none>   8d    v1.18.20   192.168.56.61   <none>        CentOS Linux 7 (Core)   3.10.0-1062.el7.x86_64   docker://20.10.21
k8s-node2    Ready    <none>   8d    v1.18.20   192.168.56.62   <none>        CentOS Linux 7 (Core)   3.10.0-1062.el7.x86_64   docker://20.10.21
[root@k8s-master ~]#
```

可以看到，三个节点的状态都是`Ready`准备好的。但是两个节点的ROLES信息却是`<none>`。

## 2. 问题分析与处理

按参考文档1进行设置修改。

**ROLES列对应的标签名是：`kubernetes.io/role`**

**ROLES列对应的标签名是：`kubernetes.io/role`**

**ROLES列对应的标签名是：`kubernetes.io/role`**

所以对ROLES列信息的操作，就是对标签名为`kubernetes.io/role`的操作。

## 3. 增加标签

获取节点信息时，显示标签信息：
```sh
[root@k8s-master ~]# k8ctl get nodes --show-labels
NAME         STATUS   ROLES    AGE   VERSION    LABELS
k8s-master   Ready    master   11d   v1.18.20   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master,kubernetes.io/os=linux,node-role.kubernetes.io/master=
k8s-node1    Ready    <none>   11d   v1.18.20   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node1,kubernetes.io/os=linux
k8s-node2    Ready    <none>   11d   v1.18.20   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node2,kubernetes.io/os=linux
```

我们也可以使用以下命令单独查看每个节点的标签信息`kubectl label --list nodes node_name`:

```sh
[root@k8s-master ~]# k8ctl label --list nodes k8s-master
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64
kubernetes.io/hostname=k8s-master
kubernetes.io/os=linux
node-role.kubernetes.io/master=
beta.kubernetes.io/arch=amd64

[root@k8s-master ~]# k8ctl label --list nodes k8s-node1
kubernetes.io/hostname=k8s-node1
kubernetes.io/os=linux
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64

[root@k8s-master ~]# k8ctl label --list nodes k8s-node2
kubernetes.io/hostname=k8s-node2
kubernetes.io/os=linux
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64

[root@k8s-master ~]#
```

我们尝试对`k8s-node2`节点添加标签说明，设置为`work-node2`：
```sh
[root@k8s-master ~]# k8ctl label node k8s-node2 kubernetes.io/role=work-node2
node/k8s-node2 labeled
```

设置完成后，再次检查`ROLES`角色信息和标签信息：
```
# 查看节点信息，可以看到节点k8s-node2的ROLE信息已经变成work-node2了
[root@k8s-master ~]# k8ctl get nodes
NAME         STATUS   ROLES        AGE   VERSION
k8s-master   Ready    master       11d   v1.18.20
k8s-node1    Ready    <none>       11d   v1.18.20
k8s-node2    Ready    work-node2   11d   v1.18.20

# 查看节点信息时也显示标签信息
[root@k8s-master ~]# k8ctl get nodes --show-labels
NAME         STATUS   ROLES        AGE   VERSION    LABELS
k8s-master   Ready    master       11d   v1.18.20   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master,kubernetes.io/os=linux,node-role.kubernetes.io/master=
k8s-node1    Ready    <none>       11d   v1.18.20   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node1,kubernetes.io/os=linux
k8s-node2    Ready    work-node2   11d   v1.18.20   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node2,kubernetes.io/os=linux,kubernetes.io/role=work-node2

# 查看节点K8s-node2的标签信息
[root@k8s-master ~]# k8ctl label --list nodes k8s-node2
kubernetes.io/hostname=k8s-node2
kubernetes.io/os=linux
kubernetes.io/role=work-node2
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64
[root@k8s-master ~]#
```

## 4. 修改标签

假如我们现在要对`k8s-node2`的`work-node2`标签进行修改，如修改为`worker2`,尝试按增加标签的方式进行修改：
```sh
[root@k8s-master ~]# k8ctl label node k8s-node2 kubernetes.io/role=worker2
error: 'kubernetes.io/role' already has a value (work-node2), and --overwrite is false
[root@k8s-master ~]#
```
此时，可以看到，提示已经有个标签了，要想修改标签，需要增加`--overwrite`选项。


我们增加`--overwrite`选项，再进行修改：
```sh
[root@k8s-master ~]# k8ctl label node k8s-node2 kubernetes.io/role=worker2
error: 'kubernetes.io/role' already has a value (work-node2), and --overwrite is false
[root@k8s-master ~]#
```

再次查看标签信息：
```
[root@k8s-master ~]# k8ctl label --overwrite node k8s-node2 kubernetes.io/role=worker2
node/k8s-node2 labeled
[root@k8s-master ~]# k8ctl get nodes
NAME         STATUS   ROLES     AGE   VERSION
k8s-master   Ready    master    11d   v1.18.20
k8s-node1    Ready    <none>    11d   v1.18.20
k8s-node2    Ready    worker2   11d   v1.18.20

# 查看节点K8s-node2的标签信息
[root@k8s-master ~]# k8ctl label --list nodes k8s-node2
kubernetes.io/os=linux
kubernetes.io/role=worker2
beta.kubernetes.io/arch=amd64
beta.kubernetes.io/os=linux
kubernetes.io/arch=amd64
kubernetes.io/hostname=k8s-node2
[root@k8s-master ~]#
```
可以看到，修改成功。



## 5. 查询标签

查询角色是`worker2`的节点：
```sh
[root@k8s-master ~]# kubectl get nodes -l kubernetes.io/role=worker2
NAME        STATUS   ROLES     AGE   VERSION
k8s-node2   Ready    worker2   11d   v1.18.20

[root@k8s-master ~]# kubectl get nodes --selector kubernetes.io/role=worker2
NAME        STATUS   ROLES     AGE   VERSION
k8s-node2   Ready    worker2   11d   v1.18.20
[root@k8s-master ~]#
```

获取没有`kubernetes.io/role`标签信息的节点：
```sh
[root@k8s-master ~]# kubectl get nodes -l '!kubernetes.io/role'
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   11d   v1.18.20
k8s-node1    Ready    <none>   11d   v1.18.20
[root@k8s-master ~]# kubectl get nodes --selector '!kubernetes.io/role'
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   11d   v1.18.20
k8s-node1    Ready    <none>   11d   v1.18.20
```
可以看出，我们配置的ROLE角色信息，与`k8s-master`节点的角色信息字段还是有差异的，但是在角色列还是显示出了角色信息。

## 6. 删除标签

我们将设置的角色信息删除掉：
```sh
[root@k8s-master ~]# kubectl label node k8s-node2 kubernetes.io/role-
node/k8s-node2 labeled
[root@k8s-master ~]# k8ctl get nodes
NAME         STATUS   ROLES    AGE   VERSION
k8s-master   Ready    master   11d   v1.18.20
k8s-node1    Ready    <none>   11d   v1.18.20
k8s-node2    Ready    <none>   11d   v1.18.20
[root@k8s-master ~]#
```
可以看到，此时角色信息又还原了。





参考：

- [k8s中节点node的ROLES值是＜none＞](https://blog.csdn.net/Lingoesforstudy/article/details/116484624)