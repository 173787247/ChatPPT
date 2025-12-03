# ChatPPT 新功能提交链接

## 作业要求

1. 集成图像生成模型：在搜索引擎的检索质量不高时，使用 SD 或其他文生图模型，为 PowerPoint 智能配图。
2. 使用 LangGraph 反思机制，通过 3-7 轮对话提升 ChatBot 生成质量或内容深度，再给到用户反馈。同时，ChatHistory 适配仅保留最终生成版本。
3. 使用 Streamlit 或其他前端框架，将 ChatPPT 已经集成的 Whisper， MiniCPM 等模型通过更强的交互能力，便捷地提供给用户。

## 代码文件链接

### 功能 1: 图像生成模型集成

**核心实现文件：**
- https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/src/image_generator.py

**功能说明：**
- 支持 OpenAI DALL-E 3
- 支持 Stability AI
- 支持本地 Stable Diffusion（通过 API）
- 自动为没有图片的幻灯片生成配图

**集成位置：**
- https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/src/gradio_server.py (generate_ppt_from_markdown 函数)

### 功能 2: LangGraph 反思机制

**核心实现文件：**
- https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/src/langgraph_reflection_agent.py

**功能说明：**
- 使用 LangGraph 构建多轮反思工作流
- 3-7 轮对话提升生成质量
- 只保留最终优化版本，不显示中间过程
- ChatHistory 适配：仅保留最终生成版本

**工作流程：**
1. 生成阶段：生成初始 Markdown 内容
2. 反思阶段：评估内容质量，识别改进点
3. 改进阶段：基于反思结果优化内容
4. 迭代：重复上述过程（最多 7 轮）
5. 输出：返回最终优化后的内容

### 功能 3: Streamlit 界面集成

**核心实现文件：**
- https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/src/streamlit_app.py

**功能说明：**
- **文本输入模式**：传统的文本输入生成 PPT
- **语音输入模式**：使用 Whisper 将语音转换为文字
- **混合模式**：结合文本和语音输入
- **模型集成**：
  - Whisper：语音转文字
  - MiniCPM：本地 LLM 生成内容
  - 反思机制：提升生成质量
  - 图像生成：智能配图

**启动脚本：**
- https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/run_streamlit.ps1

## 相关文档

- **功能说明文档：**
  - https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/README_NEW_FEATURES.md

- **测试脚本：**
  - https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/test_new_features.py

- **配置文件示例：**
  - https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/config.json.example

## 依赖更新

**requirements.txt：**
- https://github.com/173787247/ChatPPT/blob/gradio-chatbot-integration/requirements.txt

新增依赖：
- `langgraph>=0.0.20` - LangGraph 反思机制
- `streamlit>=1.28.0` - Streamlit 界面
- `openai-whisper>=20231117` - Whisper 语音转文字
- `transformers>=4.35.0` - MiniCPM 模型
- `torch>=2.0.0` - PyTorch（MiniCPM 需要）
- `stability-sdk>=0.8.0` - Stability AI SDK（可选）

## 仓库链接

**主仓库：**
https://github.com/173787247/ChatPPT

**分支：**
https://github.com/173787247/ChatPPT/tree/gradio-chatbot-integration

## 使用说明

### 启动 Streamlit 应用

```bash
# Windows PowerShell
.\run_streamlit.ps1

# 或直接使用
streamlit run src/streamlit_app.py
```

### 测试新功能

```bash
python test_new_features.py
```

### 配置图像生成

在 `config.json` 中添加：

```json
{
  "image_generator": {
    "provider": "openai",
    "openai_api_key": "your_key"
  }
}
```

### 使用反思机制

```python
from src.langgraph_reflection_agent import LangGraphReflectionAgent

agent = LangGraphReflectionAgent("prompts/formatter.txt", max_iterations=5)
result = agent.generate_with_reflection(user_input)
```

