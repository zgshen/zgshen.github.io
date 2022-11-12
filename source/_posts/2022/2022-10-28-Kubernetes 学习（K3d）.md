---
title: Kubernetes 学习（K3d）
categories: 技术
tags:
  - 技术
  - Kubernetes
toc: true
date: 2022-10-28
---

随着 Kubernetes 及其周边生态的发展，云原生技术现在已经很成熟流行了，不过 Kubernetes 架构复杂，使用门槛较高，即使自己学习的话安装一个 Kubernetes 集群也是很麻烦的事情。好在大多云厂商比如阿里腾讯云都有提供现成的容器服务，可以直接创建使用，也有一些项目简化模拟了 Kubernetes，如 Kind、Minikube 和 K3d 等，可以供开发者在本地学习和开发调试。

K3s 是一个轻量级 Kubernetes，K3d，全称 K3s in Docker，在 Docker 环境的运行的 K3s，可以在 Docker 容器中构建多个 K3s 节点，单个物理机可以运行多个 K3s 集群，每个集群可拥有多台 Server 和 Agent 节点。

k3s 包括以下一些组件：
- Containerd：一个类似 Docker 的运行时容器，但是它不支持构建镜像；
- Flannel：基于 CNI 实现的网络模型，默认使用的是 Flannel，也可以使用 Calico 等其他实现替换；
- CoreDNS：集群内部 DNS 组件；
- SQLite3：默认使用 SQLite3 进行存储，同样也支持 etcd3, MySQL, Postgres；
- Traefik：默认安装 Ingress controller 是 traefik 1.x 的版本；
- Embedded service loadbalancer：内嵌的一个服务负载均衡组件。

## 相关工具安装

K3d 项目地址 https://github.com/k3d-io/k3d，安装：
```
wget -q -O - https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) 是 Kubernetes 命令行工具，下载后建立软链接。
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
# 软链须用绝对路径
sudo ln -s /home/nathan/app/k8s/kubectl /usr/bin/kubectl
```
使用 kubectl 终端和系统不要有代理，以免影响和 K3s 集群的通讯。

kubecm是一个k8s多集群配置管理工具。
```bash
curl kubecm.tar.gz https://github.com/sunny0826/kubecm/releases/download/v$\{VERSION\}/kubecm_$\{VERSION\}_Linux_x86_64.tar.gz
tar -xf kubecm_v0.21.0_Linux_x86_64.tar.gz
sudo ln -s /home/nathan/app/k8s/kubecm /usr/bin/kubecm

# 切换集群
kubecm s
```

[helm](https://helm.sh/) 是 Kubernetes 包管理工具，下载脚本执行安装。
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 755 get_helm.sh
./get_helm.sh
```

## 创建集群

### 用命令和指定配置文件创建集群

以下命令是创建一个一主两从的集群。
```bash
k3d cluster create command-cluster --port 8080:80@loadbalancer --port 8443:443@loadbalancer --api-port 6443 --servers 1 --agents 2
```

重点来看使用 yaml 配置文件创建集群，编写一个 dev-cluster.yaml 文件，内容如下。
老的 v1alpha2 版本和 v1alpha4 版本配置有些差异，具体看 [K3d 的官方文档](https://k3d.io/v5.4.1/usage/configfile/)。
```yaml
apiVersion: k3d.io/v1alpha4
kind: Simple
metadata:
  name: dev-cluster # 不能有下划线
servers: 1
agents: 3
kubeAPI:
  hostPort: "6443" 
ports:
  - port: 8080:80  # ingress端口映射
    nodeFilters:
      - loadbalancer
  - port: 8443:443 
    nodeFilters:
      - loadbalancer
```

指定 yaml 文件创建集群:
```bash
$  k3d cluster create --config dev-cluster.yaml
INFO[0000] Using config file dev-cluster.yaml (k3d.io/v1alpha4#simple) 
INFO[0000] portmapping '8080:80' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
INFO[0000] portmapping '8443:443' targets the loadbalancer: defaulting to [servers:*:proxy agents:*:proxy] 
...中间省略...    
INFO[0019] Injecting records for hostAliases (incl. host.k3d.internal) and for 5 network members into CoreDNS configmap... 
INFO[0021] Cluster 'dev-cluster' created successfully!  
INFO[0021] You can now use it like this:                
kubectl cluster-info
```
成功看下集群信息:
```bash
$ kubectl cluster-info
Kubernetes control plane is running at https://0.0.0.0:6443
CoreDNS is running at https://0.0.0.0:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://0.0.0.0:6443/api/v1/namespaces/kube-system/services/https:metrics-server:https/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

节点信息：
```bash
$ kubectl get node
NAME                       STATUS   ROLES                  AGE     VERSION
k3d-dev-cluster-agent-0    Ready    <none>                 3m50s   v1.24.4+k3s1
k3d-dev-cluster-agent-2    Ready    <none>                 3m49s   v1.24.4+k3s1
k3d-dev-cluster-server-0   Ready    control-plane,master   3m54s   v1.24.4+k3s1
k3d-dev-cluster-agent-1    Ready    <none>                 3m49s   v1.24.4+k3s1
``` 

### 安装 Traefik2 网关

Ingress 一个API对象，就如同其他的API对象Service、Deployment一样，负责管理外部流量对于集群内部的访问，能用来做负载均衡，搞 SSL 等。Ingress Controller 有 Traefik、Nginx Ingress、kong、istio 等等。

我们可以直接使用 Helm 来安装 Traefik2。
```bash
# 跟apt安装应用的流程相似
helm repo add traefik https://helm.traefik.io/traefik
helm repo update
helm install traefik traefik/traefik
```

等待安装完毕，查看 pod 可以看装完了没有。
```bash
$ helm install traefik traefik/traefik                       
NAME: traefik
LAST DEPLOYED: Fri Oct 28 23:17:54 2022
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Traefik Proxy 2.9.1 has been deployed successfully 
on default namespace !

$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
traefik-7b47dbff65-5wlvj   1/1     Running   0          5m2s
```

因为集群是跑在 docker 中，访问需要做端口转发：
```bash
kubectl port-forward --address=0.0.0.0 $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name) 9000:9000
```

通过 http://0.0.0.0:9000/dashboard/#/ 访问仪表盘。

![Traefik Dashboard](../images/202210/Screenshot%20from%202022-10-29%2000-10-17.png)

## 部署应用

基本概念：
- Pod：Pod 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元
- Deployment：用于管理Pod、ReplicaSet，可实现滚动升级和回滚应用、扩容和缩容。
- Label：Label以key/value键值对的形式附加到各种对象上，如Pod、Service、RC、Node等。
- Service：定义了一个服务的访问入口地址，前端的应用通过这个入口地址访问其背后的一组由Pod副本组成的集群实例，来自外部的访问请求被负载均衡到后端的各个容器应用上。Service与其后端Pod副本集群之间则是通过Label Selector实现关联。简单来说前端请求不是直接发送给Pod，而是发送到Service，Service再将请求转发给pod。

我们先随便写个 python 程序放到 Docker，并 push 到镜像库上。

```python
# 简单的python程序，接收get请求，返回heah的内容
from http.server import HTTPServer, BaseHTTPRequestHandler

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        s = str(self.headers.values())
        print(s)
        self.wfile.write(s.encode("utf-8"))

try:
    httpd = HTTPServer(('127.0.0.1', 8000), HttpHandler)
    httpd.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    httpd.socket.close()
```

编写Dockerfile：
```docker
FROM python:3.8-alpine
COPY httpserver.py httpserver.py
CMD python3 httpserver.py
```

打包镜像，打 tag，push 到 [dockerhub](https://hub.docker.com/)。
```bash
docker build -t py-server .

# 要先登录
# docker login -u akari93
docker tag py-server:latest akari93/py-server:latest
docker push akari93/py-server:latest
```

编写部署应用的 yaml 文件 [demo.yaml](https://github.com/zgshen/code-note/blob/master/tools_file/k3d/demo.yaml)，分别有两个 Deployment，py-server-1 一个副本，py-server-2 两个副本，对应两个 Service，还有一个 Ingress 用来管理外部访问。

使用 `kubectl apply -f /path/demo.yaml` 命令部署。

```bash
$ kubectl apply -f demo.yaml
deployment.apps/py-server-1 created
deployment.apps/py-server-2 created
service/demo1-svc created
service/demo2-svc created
ingress.networking.k8s.io/demo-ingress created
```

部署完毕来看下节点信息：
```bash
$ kubectl get pod 
NAME                           READY   STATUS    RESTARTS   AGE
traefik-7b47dbff65-5wlvj       1/1     Running   0          26m
py-server-2-79bd86f9d5-64cqg   1/1     Running   0          2m42s
py-server-1-579dc5ff74-wwv69   1/1     Running   0          2m42s
py-server-2-79bd86f9d5-cnt6f   1/1     Running   0          2m42s

$ kubectl get deployment
NAME          READY   UP-TO-DATE   AVAILABLE   AGE
traefik       1/1     1            1           27m
py-server-1   1/1     1            1           4m
py-server-2   2/2     2            2           4m

$ kubectl get ingress
NAME           CLASS    HOSTS                                 ADDRESS   PORTS   AGE
demo-ingress   <none>   demo1.example.com,demo2.example.com             80      4m25s
```

我们修改本地的 hosts，解析两个 example 域名，命令`vi /etc/hosts`，添加以下内容。
```
# local k3d test
127.0.0.1       demo1.example.com
127.0.0.1       demo2.example.com
```

还记得前面创建集群的 yaml 文件中，`- port: 8080:80  # ingress端口映射` 这一行把80端口映射到了宿主机8080（当然80也可以，我只是本地80有其他应用用到不想停掉而已），所以在浏览器用域名访问要用8080的端口，即 http://demo1.example.com:8080/ 和 http://demo2.example.com:8080/ 。或者用 curl 测试：

```bash
$ curl http://demo1.example.com:8080/
['demo1.example.com:8080', 'curl/7.81.0', '*/*', '10.42.1.0', 'demo1.example.com:8080', '8080', 'http', 'traefik-7b47dbff65-5wlvj', '10.42.1.0', 'gzip']%   

$ curl http://demo2.example.com:8080/
['demo2.example.com:8080', 'curl/7.81.0', '*/*', '10.42.0.1', 'demo2.example.com:8080', '8080', 'http', 'traefik-7b47dbff65-5wlvj', '10.42.0.1', 'gzip']%  
```

我们还可以修改下 Python 程序和 Dockerfile 文件，把程序日志输出到日志，然后 `kubectl exec -it py-server-2-79bd86f9d5-64cqg sh` 进入 pod 具体的两个容器，看看两个 py-server-2 程序的日志，多次访问 demo2.example.com:8080，看看有没有做负载均衡，这里就不在做测试了。


## 参考

- [1] [K3d 文档](https://k3d.io/v5.4.6/usage/configfile/)
- [2] [Kubernetes 文档](https://kubernetes.io/zh-cn/docs/home/)
- [3] [如何在本地快速启动一个 K8S 集群](https://zhuanlan.zhihu.com/p/357907926)
- [4] [使用k3d启动k3s集群](https://blog.bwcxtech.com/posts/ea0ef82f/)
- [5] [Docker Hub镜像公共仓库使用](https://www.cnblogs.com/yinzhengjie/p/12231835.html)




