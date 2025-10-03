# install-docker-engine.ps1
# 使用 winget 安装 Docker Engine (最小化安装)

Write-Host "🚀 开始安装 Docker Engine (使用 winget)..."

# Step 1: 检查管理员权限
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "❌ 请使用管理员权限运行此脚本"
    exit 1
}

# Step 2: 检查 winget 是否可用
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未检测到 winget，请确保:"
    Write-Host "1. 使用 Windows 10 1709+ 或 Windows 11"
    Write-Host "2. 从 Microsoft Store 安装 App Installer"
    exit 1
}

# Step 3: 安装 Docker
Write-Host "=== Step 3: 通过 winget 安装 Docker ==="
try {
    winget install --id Docker.DockerDesktop --silent `
        --accept-package-agreements `
        --accept-source-agreements
    Write-Host "✅ Docker 安装完成"
}
catch {
    Write-Host "❌ 安装失败: $_"
    exit 1
}

# Step 5: 提示用户
Write-Host "=== Step 5: 安装完成 ==="
Write-Host "✅ Docker Engine 已安装完成！"
Write-Host "您可以完全通过命令行使用 Docker，无需打开 GUI 界面"
Write-Host "常用命令:"
Write-Host "  docker version        # 查看版本"

# 可选：禁用 Docker Desktop 开机启动
Write-Host "`n如需禁用 Docker Desktop 开机启动，可以运行:"
Write-Host "Get-ScheduledTask -TaskName 'Docker Desktop Startup' | Disable-ScheduledTask"