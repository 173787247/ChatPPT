# ChatPPT 部署作业提交

## 作业一：Docker IP:PORT 访问截图

### 部署方式
使用 Docker 容器部署，通过 IP:PORT 访问

### 访问方式
- **IP 地址**: `YOUR_SERVER_IP` 或 `localhost`
- **端口**: `7860`
- **访问地址**: `http://YOUR_SERVER_IP:7860`

### 截图说明
请在此处插入 IP:PORT 访问的截图。

![IP:PORT 访问截图](screenshots/ip_port_access.png)

**截图要求**：
- ✅ 显示浏览器地址栏中的 IP:PORT 地址（例如：`http://192.168.200.162:7860`）
- ✅ 显示 ChatPPT 界面正常运行
- ✅ 显示可以正常使用功能
- ✅ 界面完整显示，包括输入框和按钮

---

## 作业二：Docker 服务链接

### 服务链接
**ChatPPT Docker 服务地址**: `http://YOUR_SERVER_IP:7860`

### 部署信息
- **部署方式**: Docker 容器
- **访问协议**: HTTP
- **端口映射**: `7860:7860`

### 访问验证
- [x] Docker 容器正常运行
- [x] 服务可以通过 IP:PORT 访问
- [x] 服务功能正常
- [x] 可以生成 PowerPoint 文件

---

## 部署信息

### 服务器信息
- **操作系统**: Ubuntu 22.04 LTS
- **Python 版本**: 3.10+
- **部署方式**: Docker / 直接运行

### 技术栈
- **Web 框架**: Gradio
- **反向代理**: Nginx
- **SSL 证书**: Let's Encrypt (Certbot)
- **容器化**: Docker (可选)

---

## 部署步骤记录

### 1. 使用 Docker 部署（推荐）

#### 方式一：使用 docker-compose
```bash
# 设置环境变量
export OPENAI_API_KEY="your_api_key_here"

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 方式二：直接使用 Docker
```bash
# 构建镜像
docker build -t chatppt:latest .

# 运行容器
docker run -d \
  -p 7860:7860 \
  -e OPENAI_API_KEY="your_api_key_here" \
  -v $(pwd)/outputs:/app/outputs \
  --name chatppt \
  chatppt:latest

# 查看日志
docker logs -f chatppt

# 停止容器
docker stop chatppt
docker rm chatppt
```

### 2. 获取容器 IP 地址
```bash
# 查看容器 IP
docker inspect chatppt | grep IPAddress

# 或使用
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' chatppt
```

### 3. 访问服务
- **通过端口映射**: `http://localhost:7860` 或 `http://YOUR_SERVER_IP:7860`
- **通过容器 IP**: `http://CONTAINER_IP:7860`

---

## 注意事项

1. **防火墙配置**: 确保开放 7860 端口
2. **环境变量**: 设置 `OPENAI_API_KEY` 环境变量
3. **Docker 状态**: 定期检查容器运行状态
4. **日志监控**: 使用 `docker logs` 查看容器日志
5. **资源监控**: 使用 `docker stats` 监控容器资源使用
6. **数据持久化**: 确保 `outputs` 目录已挂载，生成的 PPT 文件不会丢失

---

## 更新记录

- **2024-12-03**: 初始部署配置
- **2024-12-03**: 添加 HTTPS 支持
- **2024-12-03**: 配置域名访问

