# ChatPPT 部署文档

## 部署方式

### 方式一：IP:PORT 访问（HTTP/HTTPS）

#### 1. 直接运行 Gradio 服务

```bash
cd ChatPPT
python src/gradio_server.py
```

默认会在 `http://0.0.0.0:7860` 启动服务。

#### 2. 使用 Nginx 反向代理配置 HTTPS

##### 安装 Nginx 和 Certbot

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install nginx certbot python3-certbot-nginx
```

##### 配置 Nginx

创建配置文件 `/etc/nginx/sites-available/chatppt`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/chatppt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

##### 配置 SSL 证书

```bash
sudo certbot --nginx -d your-domain.com
```

#### 3. 使用 Docker 部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  chatppt:
    build: .
    ports:
      - "7860:7860"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./outputs:/app/outputs
    restart: unless-stopped
```

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "src/gradio_server.py"]
```

运行：

```bash
docker-compose up -d
```

### 方式二：使用域名访问

#### 1. 配置域名 DNS

在域名提供商处添加 A 记录：
- 类型：A
- 主机记录：@ 或 chatppt
- 记录值：你的服务器 IP 地址

#### 2. 配置 Nginx 反向代理（同上）

#### 3. 配置 SSL 证书（同上）

## 访问方式

### IP:PORT 访问
- HTTP: `http://YOUR_IP:7860`
- HTTPS: `https://YOUR_IP:7860` (需要配置 SSL)

### 域名访问
- HTTP: `http://your-domain.com`
- HTTPS: `https://your-domain.com` (推荐)

## 截图和链接

### 作业一：IP:PORT 访问截图

![IP:PORT 访问截图](screenshots/ip_port_access.png)

访问地址：`https://YOUR_IP:7860`

### 作业二：域名访问链接

服务链接：`https://your-domain.com`

## 注意事项

1. 确保防火墙开放相应端口（7860 或 80/443）
2. 配置 SSL 证书以确保 HTTPS 访问
3. 设置环境变量 `OPENAI_API_KEY`
4. 确保服务器有足够的资源运行服务

