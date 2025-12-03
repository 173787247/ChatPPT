# ChatPPT 部署作业提交

## 作业一：IP:PORT 访问截图

### 访问方式
- **IP 地址**: `YOUR_SERVER_IP`
- **端口**: `7860`
- **访问地址**: `http://YOUR_SERVER_IP:7860` 或 `https://YOUR_SERVER_IP:7860`

### 截图说明
请在此处插入 IP:PORT 访问的截图。

![IP:PORT 访问截图](screenshots/ip_port_access.png)

**截图要求**：
- 显示浏览器地址栏中的 IP:PORT 地址
- 显示 ChatPPT 界面正常运行
- 显示可以正常使用功能

---

## 作业二：域名访问链接

### 服务链接
**ChatPPT 服务地址**: `https://your-domain.com`

### 配置说明
- **域名**: `your-domain.com`
- **协议**: HTTPS
- **SSL 证书**: Let's Encrypt（自动续期）

### 访问验证
- [ ] 域名可以正常访问
- [ ] HTTPS 证书有效
- [ ] 服务功能正常
- [ ] 可以生成 PowerPoint 文件

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

### 1. 服务器准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install nginx certbot python3-certbot-nginx -y
```

### 2. 配置 Nginx
```bash
# 复制配置文件
sudo cp nginx.conf /etc/nginx/sites-available/chatppt

# 修改域名
sudo nano /etc/nginx/sites-available/chatppt

# 启用配置
sudo ln -s /etc/nginx/sites-available/chatppt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. 配置 SSL 证书
```bash
# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com

# 测试自动续期
sudo certbot renew --dry-run
```

### 4. 启动服务
```bash
# 方式一：直接运行
python src/gradio_server.py

# 方式二：使用 Docker
docker-compose up -d
```

---

## 注意事项

1. **防火墙配置**: 确保开放 80、443 端口
2. **环境变量**: 设置 `OPENAI_API_KEY` 环境变量
3. **SSL 证书**: 定期检查证书有效期
4. **日志监控**: 定期检查 Nginx 和应用程序日志
5. **资源监控**: 监控服务器 CPU、内存使用情况

---

## 更新记录

- **2024-12-03**: 初始部署配置
- **2024-12-03**: 添加 HTTPS 支持
- **2024-12-03**: 配置域名访问

