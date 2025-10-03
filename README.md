
# 离线环境 Docker 软件包下载与安装指南

## 概述
本文档介绍如何在联网机器上通过 Docker 容器下载特定架构和系统版本的软件包，并将其转移到离线环境中进行安装。  
## 流程介绍
![流程图](https://github.com/WangYiNingbigdatabase/test/blob/main/%E6%B5%81%E7%A8%8B%E5%9B%BE.png)
1.**安装Docker**:Docker可以安装Docker Desktop或者Docker Engine,下面为本地电脑为Ubuntu系统提供Docker Engine的自动安装脚本install_docker.py和手动安装教程,为Windows用户提供了一个安装Docker Desktop的教程链接(图形化下载与配置镜像源等)和一个下载Docker Desktop的脚本install-docker.ps1。  
2.**下载所需镜像**:其实就是下载与离线电脑架构(如ARM/AMD)、版本(如Ubuntu22.04/Ubuntu20.04)相同的镜像。  
3.**在容器内下载所需包**:以download-only模式下载，不会安装，对于ubuntu来说，会下载许多.deb包。  
4.**将安装包拷贝到本地**:docker cp命令将安装包拷贝到本地电脑上,注意修改为自己的路径。  
5.**在离线的电脑安装**:先使用U盘或SCP远程传输等方式将本地电脑上的安装包传到离线电脑上，之后进行安装。 

## 1. Docker 安装与配置
为Ubuntu提供了install_docker.py的一键安装脚本，在本文末尾也提供了手动安装的流程，若脚本无效可以查看手动安装流程  
为Windows提供了一个安装Docker Desktop的链接:https://blog.csdn.net/G_whang/article/details/144677922  
Ubuntu  
`python install_docker.py`  
Windows  
`./install-docker.ps1`
## 2. 下载对应系统架构和版本的 Docker 镜像
Ubuntu:Ctrl+Alt+T打开终端   
Windows:Win+X选择"终端管理员"  
**以下命令需要修改为你需要的版本和架构!!!**
若是AMD架构，不需要指定"--platform"  
`docker run -it --rm ubuntu:22.04 bash`  
如果是ARM架构，可以用"--platform"指定  
`docker run -it --rm --platform linux/arm64 arm64v8/ubuntu:22.04 bash`  
![失败拉取镜像](https://github.com/WangYiNingbigdatabase/test/blob/main/%E5%A4%B1%E8%B4%A5%E6%8B%89%E5%8F%96%E9%95%9C%E5%83%8F.png)  
![成功拉取镜像](https://github.com/WangYiNingbigdatabase/test/blob/main/%E6%88%90%E5%8A%9F%E6%8B%89%E5%8F%96%E9%95%9C%E5%83%8F.png)
## 3. 在容器中下载所需软件包
进入容器后执行,第二步的docker run会下载并自动进入容器  
必须先update  
`apt update`  
以下载libeigen3-dev包为例  
`apt install -y --download-only libeigen3-dev`  
![成功下载包](https://github.com/WangYiNingbigdatabase/test/blob/main/%E6%88%90%E5%8A%9F%E4%B8%8B%E8%BD%BD%E5%8C%85.png)  
下载后的安装包默认在此路径(Ubuntu):/var/cache/apt/archives/  
![查看下载包](https://github.com/WangYiNingbigdatabase/test/blob/main/%E6%9F%A5%E7%9C%8B%E4%B8%8B%E8%BD%BD%E5%8C%85.png)  
## 4. 将软件包拷贝到本地
查找容器 ID 或名称
`docker ps -a`
![查找容器](https://github.com/WangYiNingbigdatabase/test/blob/main/%E6%9F%A5%E6%89%BE%E5%AE%B9%E5%99%A8.png) 
拷贝软件包到本地,替换<容器ID或名称>为docker ps -a的结果  
`docker cp <容器ID或名称>:/var/cache/apt/archives/ ~/Desktop/offline-packages/`  
![成功拷贝包](https://github.com/WangYiNingbigdatabase/test/blob/main/%E6%88%90%E5%8A%9F%E6%8B%B7%E8%B4%9D%E5%8C%85.png) 
## 5. 将安装包传输到离线电脑

### 5.1 使用 SCP 传输（通过网络）
bash
`scp -r ~/Desktop/offline-packages/ user@192.168.1.200:~/Downloads/`  
### 5.2 使用 U盘 传输（物理方式）


## 6. 离线环境安装验证
### 6.1 模拟安装测试(离线电脑为Ubuntu)
bash
`sudo dpkg --dry-run -i ~/Downloads/offline-packages/*.deb`  
### 6.2 正式安装(离线电脑为Ubuntu)
如果模拟安装无冲突提示，执行正式安装：
bash
`sudo dpkg -i ~/Downloads/offline-packages/*.deb`  
## 注意事项

1. 下载过程中可能遇到网络问题，可以通过设置镜像源或代理解决  
2. **没有代理可能无法注册或登录**
3. 如果Docker Desktop因为setting.json或daemon.json等配置问题无法启动，可以还原默认配置。
4. 确保离线环境与下载环境的系统版本和架构一致
5. **教程中的离线电脑系统为Ubuntu系统。如果离线电脑是Windows部分命令需要调整**

## 参考资源
### 相关链接
- [Docker 官方文档](https://docs.docker.com/)
- [阿里云开源镜像站](https://mirrors.aliyun.com/)
- [DaoCloud 镜像加速服务](https://github.com/DaoCloud/public-image-mirror)
- [USTC 开源镜像站](https://mirrors.ustc.edu.cn/)
### Ubuntu安装docker engine

### 1.1 卸载旧版本并安装依赖
bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt install apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release
### 1.2 添加阿里云 Docker 镜像源
bash
添加阿里云 GPG Key
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg| sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
添加阿里云 Docker APT 源
echo "deb [arch=(dpkg−−print−architecture)signed−by=/usr/share/keyrings/docker−archive−keyring.gpg]https://mirrors.aliyun.com/docker−ce/linux/ubuntu(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
更新软件包列表
sudo apt update
sudo apt-get update
### 1.3 安装 Docker
bash  
sudo apt install docker-ce docker-ce-cli containerd.io  
验证安装  
sudo docker version  
sudo systemctl status docker  
### 1.4 配置用户权限
bash  
sudo groupadd docker  
sudo gpasswd -a ${USER} docker  
sudo service docker restart  
### 1.5 配置 Docker 镜像加速器
创建或编辑 `/etc/docker/daemon.json`：  
json  
{  
"registry-mirrors": [  
"https://docker.m.daocloud.io",  
"https://hub-mirror.c.163.com",  
"https://mirror.baidubce.com",  
"https://docker.nju.edu.cn",  
"https://docker.mirrors.sjtug.sjtu.edu.cn",  
"https://registry.docker-cn.com"  
]  
}  
重载配置并重启 Docker：  
bash  
sudo systemctl daemon-reload  
sudo systemctl restart docker  
sudo docker info  
