# ChatPPT Docker 部署指南

## 快速开始

### 前置要求
- Docker 已安装
- Docker Compose 已安装（可选）
- OpenAI API Key

### 方式一：使用 Docker Compose（推荐）

1. **设置环境变量**
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export OPENAI_API_KEY="your_api_key_here"
   ```

2. **启动服务**
   ```bash
   docker-compose up -d
   ```

3. **查看日志**
   ```bash
   docker-compose logs -f
   ```

4. **访问服务**
   - 本地：`http://localhost:7860`
   - 局域网：`http://YOUR_SERVER_IP:7860`

5. **停止服务**
   ```bash
   docker-compose down
   ```

### 方式二：直接使用 Docker

1. **构建镜像**
   ```bash
   docker build -t chatppt:latest .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     -p 7860:7860 \
     -e OPENAI_API_KEY="your_api_key_here" \
     -v $(pwd)/outputs:/app/outputs \
     -v $(pwd)/templates:/app/templates \
     -v $(pwd)/prompts:/app/prompts \
     --name chatppt \
     chatppt:latest
   ```

3. **查看容器状态**
   ```bash
   docker ps
   docker logs -f chatppt
   ```

4. **停止容器**
   ```bash
   docker stop chatppt
   docker rm chatppt
   ```

## 获取访问地址

### 获取服务器 IP（Windows）
```powershell
ipconfig
# 查找 IPv4 地址，例如：192.168.200.162
```

### 获取服务器 IP（Linux/Mac）
```bash
ifconfig
# 或
ip addr show
```

### 获取容器 IP
```bash
docker inspect chatppt | grep IPAddress
# 或
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' chatppt
```

## 访问方式

### 1. 通过端口映射访问（推荐）
- **本地访问**: `http://localhost:7860`
- **局域网访问**: `http://YOUR_SERVER_IP:7860`
  - 例如：`http://192.168.200.162:7860`

### 2. 通过容器 IP 访问
- 获取容器 IP 后访问：`http://CONTAINER_IP:7860`

## 截图要求

### IP:PORT 访问截图

1. **启动 Docker 容器**
   ```bash
   docker-compose up -d
   ```

2. **获取服务器 IP**
   ```powershell
   ipconfig
   ```

3. **访问服务**
   - 打开浏览器
   - 访问：`http://YOUR_SERVER_IP:7860`
   - 例如：`http://192.168.200.162:7860`

4. **截图**
   - 使用 Win + Shift + S 截图
   - 确保显示：
     - ✅ 浏览器地址栏（包含 IP:PORT）
     - ✅ 完整的 ChatPPT 界面
     - ✅ 界面正常显示

5. **保存截图**
   - 文件名：`ip_port_access.png`
   - 保存位置：`screenshots/ip_port_access.png`

## 常用命令

### 查看容器状态
```bash
docker ps
docker ps -a  # 包括已停止的容器
```

### 查看日志
```bash
docker-compose logs -f
# 或
docker logs -f chatppt
```

### 重启服务
```bash
docker-compose restart
# 或
docker restart chatppt
```

### 查看资源使用
```bash
docker stats chatppt
```

### 进入容器
```bash
docker exec -it chatppt bash
```

## 故障排除

### 容器无法启动
```bash
# 查看详细日志
docker-compose logs
docker logs chatppt

# 检查端口是否被占用
netstat -ano | findstr :7860  # Windows
lsof -i :7860  # Linux/Mac
```

### 无法访问服务
1. 检查防火墙是否开放 7860 端口
2. 检查容器是否正常运行：`docker ps`
3. 检查端口映射：`docker port chatppt`

### 环境变量未生效
```bash
# 检查环境变量
docker exec chatppt env | grep OPENAI_API_KEY

# 重新创建容器并设置环境变量
docker-compose down
docker-compose up -d
```

## 数据持久化

确保以下目录已挂载：
- `outputs/` - 生成的 PPT 文件
- `templates/` - PPT 模板文件
- `prompts/` - Prompt 文件

在 `docker-compose.yml` 中已配置：
```yaml
volumes:
  - ./outputs:/app/outputs
  - ./templates:/app/templates
  - ./prompts:/app/prompts
```

## 更新服务

```bash
# 停止旧容器
docker-compose down

# 重新构建镜像（如果代码有更新）
docker-compose build

# 启动新容器
docker-compose up -d
```

