# Docker Desktop 更新后操作指南

## 更新后验证

### 1. 验证 Docker 是否正常运行

```powershell
# 检查 Docker 版本
docker --version

# 检查 Docker 是否运行
docker ps
```

如果命令正常执行，说明 Docker 已成功更新并运行。

### 2. 验证 Docker Compose（如果使用）

```powershell
docker-compose --version
```

## 部署步骤

### 步骤 1：设置环境变量

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

### 步骤 2：运行部署脚本

```powershell
.\docker_deploy_simple.ps1
```

### 步骤 3：等待服务启动

脚本会：
1. 构建 Docker 镜像（首次运行可能需要几分钟）
2. 启动容器
3. 显示访问地址
4. 自动打开浏览器

### 步骤 4：访问并截图

- 访问地址：`http://192.168.3.15:7860`
- 使用 Win + Shift + S 截图
- 保存到：`screenshots\ip_port_access.png`

## 常见问题

### 更新后 Docker 无法启动
- 重启计算机
- 检查 Windows 功能中是否启用了虚拟化
- 检查 WSL 2 是否已安装

### 镜像构建失败
```powershell
# 清理旧的构建缓存
docker system prune -a

# 重新构建
docker build -t chatppt:latest .
```

### 端口冲突
如果 7860 端口被占用，可以修改 `docker-compose.yml`：
```yaml
ports:
  - "7861:7860"  # 改为其他端口
```

## 快速验证清单

- [ ] Docker Desktop 已更新并运行
- [ ] `docker ps` 命令正常执行
- [ ] OPENAI_API_KEY 已设置
- [ ] 运行 `.\docker_deploy_simple.ps1`
- [ ] 服务成功启动
- [ ] 可以访问 `http://192.168.3.15:7860`
- [ ] 截图已保存

## 备用方案

如果 Docker 仍有问题，可以直接运行 Python 服务：

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
python src/gradio_server.py
```

然后访问 `http://192.168.3.15:7860` 截图。

