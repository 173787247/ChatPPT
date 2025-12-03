# ChatPPT 服务启动指南

## 问题诊断

根据错误信息 `ERR_CONNECTION_REFUSED`，服务没有运行。

## 解决方案

### 方案一：直接运行 Python 服务（最简单）

```powershell
# 1. 设置 API Key
$env:OPENAI_API_KEY="your_api_key_here"

# 2. 直接运行服务
python src/gradio_server.py
```

服务会在 `http://0.0.0.0:7860` 启动，然后：
- 访问：`http://localhost:7860` 或 `http://192.168.3.15:7860`
- 截图即可

### 方案二：使用 Docker（需要先启动 Docker Desktop）

#### 步骤 1：启动 Docker Desktop
1. 打开 Docker Desktop 应用
2. 等待 Docker 完全启动（状态栏显示 "Docker Desktop is running"）

#### 步骤 2：运行部署脚本
```powershell
# 设置 API Key
$env:OPENAI_API_KEY="your_api_key_here"

# 运行部署脚本
.\docker_deploy_simple.ps1
```

## 快速检查清单

- [ ] Docker Desktop 是否运行？（如果使用 Docker）
- [ ] OPENAI_API_KEY 是否设置？
- [ ] 端口 7860 是否被占用？
- [ ] 防火墙是否阻止了端口？

## 故障排查

### 检查 Docker 状态
```powershell
docker ps
```

如果显示错误，说明 Docker Desktop 没有运行。

### 检查端口占用
```powershell
netstat -ano | findstr :7860
```

如果没有输出，说明端口没有被占用，服务没有运行。

### 检查服务是否启动
```powershell
# 直接运行查看错误
python src/gradio_server.py
```

## 推荐方案

**最简单的方式**：直接运行 Python 服务，不需要 Docker

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
python src/gradio_server.py
```

然后访问 `http://192.168.3.15:7860` 即可截图。

