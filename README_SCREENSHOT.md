# ChatPPT 截图和上传指南

## 快速开始

### 方法一：使用自动化脚本（推荐）

#### 步骤 1：启动服务并截图

```powershell
# 1. 设置环境变量
$env:OPENAI_API_KEY="your_api_key_here"

# 2. 运行截图辅助脚本
.\capture_screenshot.ps1
```

脚本会：
- ✅ 自动获取本机 IP 地址
- ✅ 启动 ChatPPT 服务
- ✅ 自动打开浏览器
- ✅ 显示访问地址

#### 步骤 2：截图

1. 浏览器会自动打开（或手动访问显示的地址）
2. 使用 **Win + Shift + S** 截图
3. 保存截图为：`screenshots/ip_port_access.png`

#### 步骤 3：上传截图

```powershell
# 运行上传脚本
.\upload_screenshot.ps1
```

脚本会：
- ✅ 检查截图文件是否存在
- ✅ 自动添加到 Git
- ✅ 提交并推送到 GitHub

### 方法二：手动操作

#### 1. 启动服务

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
python src/gradio_server.py
```

#### 2. 获取 IP 地址

```powershell
ipconfig
```

查找 IPv4 地址，例如：`192.168.1.100`

#### 3. 访问并截图

- 打开浏览器
- 访问：`http://YOUR_IP:7860`
- 使用 **Win + Shift + S** 截图
- 保存到：`screenshots/ip_port_access.png`

#### 4. 提交到 Git

```powershell
git add screenshots/ip_port_access.png
git add SUBMISSION.md
git commit -m "docs: 添加部署截图"
git push myfork gradio-chatbot-integration
```

## 截图要求

### 必须包含的内容

1. ✅ **浏览器地址栏**
   - 显示完整的 URL（IP:PORT 或 localhost:7860）
   - 例如：`http://192.168.1.100:7860`

2. ✅ **完整的 ChatPPT 界面**
   - 显示标题："ChatPPT - AI PowerPoint Generator"
   - 显示对话界面
   - 显示输入框
   - 显示"生成 PowerPoint"按钮

3. ✅ **界面正常显示**
   - 没有错误提示
   - 界面元素完整可见

### 截图工具

- **Windows 截图工具**：Win + Shift + S
- **Snipping Tool**：开始菜单搜索"截图工具"
- **浏览器截图插件**：如 Full Page Screen Capture

## 文件位置

- 截图文件：`screenshots/ip_port_access.png`
- 提交文档：`SUBMISSION.md`
- 截图指南：`SCREENSHOT_GUIDE.md`

## 常见问题

### Q: 截图文件太大怎么办？
A: 可以使用图片压缩工具，或使用 PNG 压缩：
```powershell
# 使用 PowerShell 压缩（需要安装 ImageMagick）
magick screenshots/ip_port_access.png -quality 80 screenshots/ip_port_access_compressed.png
```

### Q: 无法通过 IP 访问？
A: 
1. 检查防火墙是否开放 7860 端口
2. 确保在同一网络
3. 可以使用 `localhost:7860` 截图

### Q: Git 推送失败？
A: 检查：
1. 是否已设置远程仓库：`git remote -v`
2. 是否有推送权限
3. 网络连接是否正常

## 提交链接

截图上传后，可以提交以下链接：

- **GitHub 截图目录**：
  https://github.com/173787247/ChatPPT/tree/gradio-chatbot-integration/screenshots

- **提交文档**：
  https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/SUBMISSION.md

