#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

def run_cmd(cmd, check=True):
    """运行系统命令并实时输出"""
    print(f"\n>>> 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ 命令执行失败: {cmd}")
        exit(1)

def install_docker():
    print("=== Step 1: 卸载可能存在的旧版本Docker ===")
    run_cmd("sudo apt-get remove -y docker docker-engine docker.io containerd runc", check=False)

    print("=== Step 2: 安装必要依赖 ===")
    run_cmd("sudo apt-get update")
    run_cmd("sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release")

    print("=== Step 3: 添加阿里GPG Key ===")
    run_cmd("curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg")

    print("=== Step 4: 添加阿里Docker APT源 ===")
    run_cmd('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] '
            'https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" '
            '| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')

    print("=== Step 5: 更新APT源 ===")
    run_cmd("sudo apt-get update")

    print("=== Step 6: 安装Docker CE ===")
    run_cmd("sudo apt install -y docker-ce docker-ce-cli containerd.io")

    print("=== Step 7: 验证Docker安装 ===")
    run_cmd("sudo docker version")
    run_cmd("sudo systemctl status docker", check=False)

    print("=== Step 8: 将当前用户添加到docker组（免sudo运行docker）===")
    run_cmd("sudo groupadd docker || true")
    run_cmd(f"sudo gpasswd -a {os.getenv('USER')} docker")
    run_cmd("sudo service docker restart")

def config_mirrors():
    print("=== Step 9: 配置国内Docker镜像加速源 ===")
    daemon_json = r'''{
    "registry-mirrors": [
        "https://dockerproxy.com",
        "https://docker.m.daocloud.io",
        "https://cr.console.aliyun.com",
        "https://ccr.ccs.tencentyun.com",
        "https://hub-mirror.c.163.com",
        "https://mirror.baidubce.com",
        "https://docker.nju.edu.cn",
        "https://docker.mirrors.sjtug.sjtu.edu.cn",
        "https://github.com/ustclug/mirrorrequest",
        "https://registry.docker-cn.com"
    ]
}'''
    with open("/tmp/daemon.json", "w") as f:
        f.write(daemon_json)

    run_cmd("sudo mkdir -p /etc/docker")
    run_cmd("sudo mv /tmp/daemon.json /etc/docker/daemon.json")

    print("=== Step 10: 重启Docker服务并验证配置 ===")
    run_cmd("sudo systemctl daemon-reload")
    run_cmd("sudo systemctl restart docker")
    run_cmd("sudo docker info")

if __name__ == "__main__":

    #chmod +x install_docker.py
    #python3 install_docker.py
    print("🚀 开始自动安装Docker (Ubuntu专用)...")
    install_docker()
    config_mirrors()
    print("\n✅ Docker 安装 & 镜像源配置完成！请重新登录终端使用户组权限生效。")
    print("   测试命令：docker run hello-world")

