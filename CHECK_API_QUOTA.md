# 如何检查 OpenAI API 配额

## 方法 1：通过 OpenAI 平台网站检查

### 步骤：

1. **访问 OpenAI 平台**
   - 打开浏览器，访问：https://platform.openai.com
   - 使用你的 OpenAI 账户登录

2. **查看账户余额和配额**
   - 登录后，点击右上角的头像
   - 选择 "Settings" 或 "账户设置"
   - 在左侧菜单中找到 "Billing" 或 "账单"
   - 查看 "Usage" 或 "使用情况" 部分

3. **检查 API 使用情况**
   - 在 "Usage" 页面可以看到：
     - 当前余额（Current Balance）
     - 本月使用量（Monthly Usage）
     - 配额限制（Rate Limits）
     - 使用历史图表

4. **查看详细账单**
   - 点击 "Billing" → "Billing History"
   - 可以看到详细的消费记录

## 方法 2：通过 API 检查（程序化）

### 使用 Python 脚本检查：

```python
import os
import requests

api_key = os.getenv("OPENAI_API_KEY")

# 检查使用情况
headers = {
    "Authorization": f"Bearer {api_key}"
}

# 获取使用情况（需要订阅计划）
response = requests.get(
    "https://api.openai.com/v1/usage",
    headers=headers,
    params={
        "start_date": "2025-12-01",
        "end_date": "2025-12-31"
    }
)

print(response.json())
```

## 方法 3：常见配额问题

### 免费账户限制：
- **免费试用账户**：通常有 $5 或 $18 的初始额度
- **使用完后**：需要添加付款方式并充值

### 付费账户：
- **按使用量付费**：根据实际使用量计费
- **配额限制**：可能有每分钟/每天的请求限制

## 方法 4：快速检查（通过错误信息）

如果看到以下错误，说明配额问题：

```
Error code: 429
'insufficient_quota'
'You exceeded your current quota'
```

## 解决方案

### 1. 充值账户
- 访问：https://platform.openai.com/account/billing
- 添加付款方式
- 充值余额

### 2. 检查 API Key 是否正确
- 确认使用的是正确的 API Key
- 检查 API Key 是否已过期或被撤销

### 3. 使用其他 API Key
- 如果有多个账户，可以切换 API Key
- 或者创建新的 API Key

### 4. 等待配额重置
- 某些配额限制是按时间周期重置的（如每分钟/每天）
- 可以等待一段时间后重试

## 临时解决方案（仅用于测试）

如果只是需要测试界面和截图，可以：
1. 修改代码，使用模拟数据（不调用真实 API）
2. 或者先截图提交，后续再解决 API 问题

