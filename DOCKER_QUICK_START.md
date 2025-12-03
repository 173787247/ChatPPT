# Docker 快速启动指南

## 前置检查

### 1. 确保 Docker Desktop 已启动

- 打开 Docker Desktop 应用
- 等待完全启动（系统托盘图标显示运行中）
- 状态栏应显示 "Docker Desktop is running"

### 2. 验证 Docker 运行状态

```powershell
docker ps
```

如果显示容器列表（或空列表），说明 Docker 正常运行。

## 快速部署

### 步骤 1：设置环境变量

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

### 步骤 2：运行部署脚本

```powershell
.\docker_deploy_simple.ps1
```

脚本会自动：
- ✅ 检查 Docker 是否运行
- ✅ 构建 Docker 镜像
- ✅ 启动容器
- ✅ 显示访问地址
- ✅ 自动打开浏览器

### 步骤 3：访问服务

服务启动后，访问：
- **本地**: `http://localhost:7860`
- **IP 访问**: `http://192.168.3.15:7860`

### 步骤 4：截图

1. 浏览器会自动打开（或手动访问显示的地址）
2. 使用 **Win + Shift + S** 截图
3. 确保截图包含：
   - ✅ 浏览器地址栏（显示 IP:PORT）
   - ✅ 完整的 ChatPPT 界面
4. 保存到：`screenshots\ip_port_access.png`

## 常用命令

### 查看容器状态
```powershell
docker ps
```

### 查看日志
```powershell
docker logs -f chatppt
```

### 停止容器
```powershell
docker stop chatppt
```

### 重启容器
```powershell
docker restart chatppt
```

### 删除容器
```powershell
docker rm -f chatppt
```

## 故障排查

### Docker Desktop 未运行
- 打开 Docker Desktop 应用
- 等待完全启动

### 端口被占用
```powershell
netstat -ano | findstr :7860
```
如果端口被占用，可以：
- 停止占用端口的进程
- 或修改 `docker-compose.yml` 中的端口映射

### 容器启动失败
```powershell
docker logs chatppt
```
查看详细错误信息

## 提交作业

### 作业一：截图
- 文件：`screenshots/ip_port_access.png`
- 显示：浏览器地址栏（IP:PORT）和完整界面

### 作业二：服务链接
- 链接：`http://192.168.3.15:7860`
- 在 `SUBMISSION.md` 中填写实际链接

