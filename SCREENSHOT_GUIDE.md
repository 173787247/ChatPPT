# ChatPPT 截图指南

## 作业要求

1. **作业一**：将 ChatPPT 发布为 HTTPS 服务（IP:PORT 形式访问），提交截图
2. **作业二**：使用域名发布 ChatPPT 服务，提交服务链接

## 截图步骤

### 步骤 1：启动 ChatPPT 服务

#### 方式一：使用启动脚本（推荐）

**Windows PowerShell:**
```powershell
# 1. 设置环境变量（如果未设置）
$env:OPENAI_API_KEY="your_api_key_here"

# 2. 运行启动脚本
.\start_server.ps1
```

**Windows CMD:**
```cmd
# 1. 设置环境变量（如果未设置）
set OPENAI_API_KEY=your_api_key_here

# 2. 运行启动脚本
start_server.bat
```

#### 方式二：直接运行

```powershell
# 设置环境变量
$env:OPENAI_API_KEY="your_api_key_here"

# 启动服务
python src/gradio_server.py
```

### 步骤 2：访问服务

服务启动后，你会看到类似以下输出：
```
Running on local URL:  http://127.0.0.1:7860
Running on public URL: https://xxxxx.gradio.live
```

#### 本地访问
- 打开浏览器
- 访问：`http://localhost:7860`

#### IP:PORT 访问（作业一）
- 获取本机 IP 地址：
  ```powershell
  # Windows PowerShell
  ipconfig
  # 查找 IPv4 地址，例如：192.168.1.100
  ```
- 在同一网络的其他设备上访问：`http://YOUR_IP:7860`
- 或者在本机访问：`http://YOUR_IP:7860`

### 步骤 3：截图要求

#### 作业一截图（IP:PORT 访问）

1. **打开浏览器**，访问 `http://YOUR_IP:7860`
2. **截图要求**：
   - ✅ 显示浏览器地址栏，包含 IP:PORT（例如：`http://192.168.1.100:7860`）
   - ✅ 显示完整的 ChatPPT 界面
   - ✅ 界面正常显示，可以看到输入框和按钮
   - ✅ 可以验证服务正常运行

3. **保存截图**：
   - 文件名：`ip_port_access.png`
   - 保存位置：`screenshots/ip_port_access.png`

#### 截图示例说明

```
浏览器地址栏应显示：
http://192.168.1.100:7860

界面应显示：
- ChatPPT 标题
- 对话界面
- 输入框
- "生成 PowerPoint" 按钮
```

### 步骤 4：配置 HTTPS 和域名（作业二）

#### 4.1 配置 Nginx 反向代理

1. **安装 Nginx**（Linux 服务器）：
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **配置 Nginx**：
   ```bash
   sudo nano /etc/nginx/sites-available/chatppt
   ```
   
   使用项目中的 `nginx.conf` 作为模板，修改域名

3. **启用配置**：
   ```bash
   sudo ln -s /etc/nginx/sites-available/chatppt /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

#### 4.2 配置 SSL 证书

```bash
sudo certbot --nginx -d your-domain.com
```

#### 4.3 访问域名

- HTTPS: `https://your-domain.com`

### 步骤 5：保存截图和链接

1. **截图保存**：
   - 将截图保存到 `screenshots/ip_port_access.png`

2. **更新 SUBMISSION.md**：
   - 打开 `SUBMISSION.md`
   - 填写实际的 IP 地址和域名链接
   - 添加截图引用

3. **提交到 GitHub**：
   ```bash
   git add screenshots/ SUBMISSION.md
   git commit -m "docs: 添加部署截图和服务链接"
   git push myfork gradio-chatbot-integration
   ```

## 快速测试（本地）

如果只是测试功能，可以在本地运行：

```powershell
# 1. 设置 API Key
$env:OPENAI_API_KEY="your_api_key_here"

# 2. 启动服务
python src/gradio_server.py

# 3. 在浏览器访问
# http://localhost:7860
```

## 常见问题

### Q: 服务启动失败
A: 检查：
- OPENAI_API_KEY 是否设置
- Python 依赖是否安装完整
- 端口 7860 是否被占用

### Q: 无法通过 IP 访问
A: 检查：
- 防火墙是否开放 7860 端口
- 是否在同一网络
- IP 地址是否正确

### Q: 如何获取本机 IP
A: 
- Windows: `ipconfig` 查看 IPv4 地址
- Linux/Mac: `ifconfig` 或 `ip addr`

## 提交格式

### GitHub 提交
- 截图文件：`screenshots/ip_port_access.png`
- 提交文档：`SUBMISSION.md`

### 在线文档提交
- 创建腾讯文档
- 上传截图
- 填写服务链接
- 设置为可公开阅读

