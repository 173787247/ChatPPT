# 如何获取 OpenAI API Key

## 步骤 1：访问 OpenAI 平台

1. 打开浏览器，访问：**https://platform.openai.com**
2. 如果没有账号，点击 "Sign up" 注册
3. 如果有账号，点击 "Log in" 登录

## 步骤 2：登录账号

- 使用你的 OpenAI 账号登录
- 或者使用 Google/Microsoft 账号登录

## 步骤 3：进入 API Keys 页面

登录后，有两种方式进入 API Keys 页面：

### 方式一：通过菜单
1. 点击右上角的头像或用户名
2. 在下拉菜单中选择 "API keys"

### 方式二：直接访问
直接访问：**https://platform.openai.com/api-keys**

## 步骤 4：创建新的 API Key

1. 在 API Keys 页面，点击 **"Create new secret key"** 按钮
2. 输入一个名称（可选，用于识别这个 Key 的用途）
   - 例如：`ChatPPT-Development`
3. 点击 **"Create secret key"** 按钮

## 步骤 5：复制并保存 API Key

⚠️ **重要提示**：
- API Key 只会显示一次
- 请立即复制并妥善保存
- 如果丢失，需要重新创建

1. 复制显示的 API Key（格式类似：`sk-...`）
2. 保存到安全的地方（密码管理器、文本文件等）

## 步骤 6：设置环境变量

### Windows PowerShell
```powershell
$env:OPENAI_API_KEY="sk-your-actual-api-key-here"
```

### Windows CMD
```cmd
set OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 永久设置（Windows）
1. 右键"此电脑" → "属性"
2. "高级系统设置" → "环境变量"
3. 在"用户变量"中点击"新建"：
   - 变量名：`OPENAI_API_KEY`
   - 变量值：你的 API Key（以 `sk-` 开头）

## 验证 API Key

设置后，可以验证：

### Windows PowerShell
```powershell
echo $env:OPENAI_API_KEY
```

### Windows CMD
```cmd
echo %OPENAI_API_KEY%
```

## 费用说明

⚠️ **重要**：
- OpenAI API 是**付费服务**
- 使用 API 会产生费用
- 建议设置使用限额和监控费用
- 可以在 OpenAI 平台查看使用量和费用

### 设置使用限额
1. 访问：https://platform.openai.com/account/billing/limits
2. 设置每月使用限额
3. 设置硬性限额以防止超支

## 安全建议

1. ✅ **不要分享 API Key**：不要将 API Key 提交到公开的 Git 仓库
2. ✅ **使用环境变量**：不要硬编码在代码中
3. ✅ **定期轮换**：定期更换 API Key
4. ✅ **设置限额**：设置使用限额防止意外超支
5. ✅ **监控使用**：定期检查 API 使用情况

## 常见问题

### Q: API Key 格式是什么？
A: OpenAI API Key 通常以 `sk-` 开头，例如：`sk-proj-xxxxxxxxxxxxx`

### Q: 可以创建多个 API Key 吗？
A: 可以，建议为不同项目创建不同的 API Key，便于管理和追踪

### Q: API Key 丢失了怎么办？
A: 需要重新创建，旧的 Key 无法恢复

### Q: 如何查看 API 使用情况？
A: 访问：https://platform.openai.com/usage

### Q: 如何查看费用？
A: 访问：https://platform.openai.com/account/billing

## 快速链接

- **API Keys 页面**：https://platform.openai.com/api-keys
- **使用情况**：https://platform.openai.com/usage
- **账单管理**：https://platform.openai.com/account/billing
- **使用限额**：https://platform.openai.com/account/billing/limits

