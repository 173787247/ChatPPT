# ChatPPT 环境变量配置

## 必需的环境变量

### OPENAI_API_KEY
OpenAI API Key，用于 ChatBot 功能。

**获取方式**：
1. 访问 https://platform.openai.com/api-keys
2. 登录你的 OpenAI 账号
3. 创建新的 API Key
4. 复制 API Key

**设置方式**：

#### Windows PowerShell
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

#### Windows CMD
```cmd
set OPENAI_API_KEY=your_api_key_here
```

#### Linux/Mac
```bash
export OPENAI_API_KEY="your_api_key_here"
```

#### 永久设置（Windows）
1. 右键"此电脑" -> "属性"
2. "高级系统设置" -> "环境变量"
3. 在"用户变量"中添加：
   - 变量名：`OPENAI_API_KEY`
   - 变量值：你的 API Key

#### 永久设置（Linux/Mac）
在 `~/.bashrc` 或 `~/.zshrc` 中添加：
```bash
export OPENAI_API_KEY="your_api_key_here"
```

## 可选的环境变量

### SERVER_NAME
服务器监听地址，默认为 `0.0.0.0`

### SERVER_PORT
服务器端口，默认为 `7860`

### GRADIO_SHARE
是否启用 Gradio 公共链接，默认为 `False`

## 使用 .env 文件（推荐）

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填写你的 API Key

3. 安装 python-dotenv：
   ```bash
   pip install python-dotenv
   ```

4. 在代码中加载 .env 文件（需要修改代码）

## 验证配置

运行以下命令验证环境变量是否设置成功：

### Windows PowerShell
```powershell
echo $env:OPENAI_API_KEY
```

### Windows CMD
```cmd
echo %OPENAI_API_KEY%
```

### Linux/Mac
```bash
echo $OPENAI_API_KEY
```

## 注意事项

1. **不要将 API Key 提交到 Git**：确保 `.env` 文件在 `.gitignore` 中
2. **API Key 安全**：不要分享你的 API Key
3. **费用**：使用 OpenAI API 会产生费用，请注意使用量

