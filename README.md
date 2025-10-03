
# 离线环境 Docker 软件包下载与安装指南

## 概述

本文档介绍如何在联网机器上通过 Docker 容器下载特定架构和系统版本的软件包，并将其转移到离线环境中进行安装。
此处放置一张流程图

## PS.
1.安装Docker:Docker可以安装docker desktop或者docker engine,下面为Ubuntu提供docker engine的自动安装脚本和手动安装流程,为windows提供了一个安装docker desktop的链接。
2.下载所需镜像:其实就是下载与离线电脑架构(如ARM/AMD)、版本(如Ubuntu22.04/Ubuntu20.04)的镜像。
3.在容器内下载所需包:以download-only模式下载，不会安装，对于ubuntu来说，会下载许多.deb包。
4.将安装包拷贝到本地:使用U盘或SCP远程传输均可,注意修改为自己的路径。
5.在离线的电脑安装:建议先模拟安装确保没有冲突后再安装(同教程)。
![img1](https://github.com/WangYiNingbigdatabase/test/blob/main/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202025-10-03%20164645.png)
## 1. Docker 安装与配置

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
## 2. 下载对应系统架构和版本的 Docker 镜像

### 2.1 AMD64 架构
bash
docker run -it --rm ubuntu:22.04 bash
### 2.2 ARM64 架构
bash
创建多平台构建器（如需要）
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
下载并运行 ARM64 架构的 Ubuntu
docker pull --platform linux/arm64 arm64v8/ubuntu:22.04
docker run -it --rm --platform linux/arm64 arm64v8/ubuntu:22.04 bash
验证架构
uname -m
## 3. 在容器中下载所需软件包
bash
进入容器后执行
apt update
apt install -y --download-only libeigen3-dev liborocos-kdl-dev libkdl-parser-dev liburdfdom-dev libnlopt-dev
## 4. 将软件包拷贝到本地
bash
查找容器 ID 或名称
docker ps -a
拷贝软件包到本地
docker cp <容器ID或名称>:/var/cache/apt/archives/ ~/Desktop/offline-packages/
## 5. 将安装包传输到离线电脑

### 5.1 使用 SCP 传输（通过网络）
bash
scp -r ~/Desktop/offline-packages/ user@192.168.1.200:~/Downloads/
### 5.2 使用 U盘 传输（物理方式）
将 `~/Desktop/offline-packages/` 目录复制到 U盘，然后在离线电脑上从 U盘 复制到目标位置。

## 6. 离线环境安装验证

### 6.1 模拟安装测试
bash
sudo dpkg --dry-run -i ~/Downloads/offline-packages/*.deb
### 6.2 正式安装
如果模拟安装无冲突提示，执行正式安装：
bash
sudo dpkg -i ~/Downloads/offline-packages/*.deb
## 注意事项

1. 如果模拟安装提示 "conflicts with" 或 "breaks existing packages"，需要手动解决依赖冲突
2. 确保离线环境与下载环境的系统版本和架构一致
3. 对于复杂的依赖关系，可能需要下载并安装所有依赖包
4. 建议在下载前确认所需软件包的准确名称和版本

## 参考资源

- [Docker 官方文档](https://docs.docker.com/)
- [阿里云开源镜像站](https://mirrors.aliyun.com/)
- [DaoCloud 镜像加速服务](https://github.com/DaoCloud/public-image-mirror)
- [USTC 开源镜像站](https://mirrors.ustc.edu.cn/)
