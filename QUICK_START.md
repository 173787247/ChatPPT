# ChatPPT Docker 快速部署指南

## 一键部署（推荐）

### Windows PowerShell

```powershell
# 1. 设置 API Key
$env:OPENAI_API_KEY="your_api_key_here"

# 2. 运行部署脚本
.\docker_deploy_simple.ps1
```

脚本会自动：
- ✅ 检查 Docker 是否安装
- ✅ 构建 Docker 镜像
- ✅ 启动容器
- ✅ 显示访问地址
- ✅ 自动打开浏览器

### 访问服务

服务启动后，访问：
- **本地**: `http://localhost:7860`
- **IP 访问**: `http://YOUR_IP:7860`（例如：`http://192.168.200.162:7860`）

## 截图步骤

1. **服务启动后，浏览器会自动打开**
   - 如果没有自动打开，手动访问显示的地址

2. **截图**
   - 使用 **Win + Shift + S** 截图
   - 确保截图包含：
     - ✅ 浏览器地址栏（显示 IP:PORT）
     - ✅ 完整的 ChatPPT 界面

3. **保存截图**
   - 文件名：`ip_port_access.png`
   - 保存位置：`screenshots\ip_port_access.png`

4. **上传截图**
   ```powershell
   .\upload_screenshot.ps1
   ```

## 手动部署（可选）

### 1. 构建镜像
```bash
docker build -t chatppt:latest .
```

### 2. 运行容器
```bash
docker run -d \
  --name chatppt \
  -p 7860:7860 \
  -e OPENAI_API_KEY="your_api_key_here" \
  -v $(pwd)/outputs:/app/outputs \
  chatppt:latest
```

### 3. 查看日志
```bash
docker logs -f chatppt
```

### 4. 访问服务
打开浏览器访问：`http://localhost:7860` 或 `http://YOUR_IP:7860`

## 常用命令

```bash
# 查看容器状态
docker ps

# 查看日志
docker logs -f chatppt

# 停止容器
docker stop chatppt

# 启动容器
docker start chatppt

# 删除容器
docker rm -f chatppt

# 查看资源使用
docker stats chatppt
```

## 提交作业

### 作业一：截图
- 截图文件：`screenshots/ip_port_access.png`
- 显示浏览器地址栏中的 IP:PORT
- 显示完整的 ChatPPT 界面

### 作业二：服务链接
- 服务地址：`http://YOUR_SERVER_IP:7860`
- 例如：`http://192.168.200.162:7860`

## 更新 SUBMISSION.md

在 `SUBMISSION.md` 中填写：
- 实际的 IP 地址和端口
- 截图路径
- 服务链接

