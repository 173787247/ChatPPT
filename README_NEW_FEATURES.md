# ChatPPT 新功能说明

## 功能 1: 图像生成模型集成

### 功能描述
在搜索引擎的检索质量不高时，使用 Stable Diffusion 或其他文生图模型，为 PowerPoint 智能配图。

### 实现方式
- 支持多种图像生成服务：
  - OpenAI DALL-E 3
  - Stability AI
  - 本地 Stable Diffusion（通过 API）

### 使用方法

1. **配置图像生成服务**（在 `config.json` 中）：
```json
{
  "image_generator": {
    "provider": "openai",
    "openai_api_key": "your_key",
    "stability_api_key": "your_key",
    "local_sd_url": "http://localhost:7860"
  }
}
```

2. **在生成 PowerPoint 时启用**：
```python
from src.gradio_server import generate_ppt_from_markdown
from src.config import Config

config = Config()
output_path, status = generate_ppt_from_markdown(
    markdown_text, 
    config, 
    enable_image_generation=True  # 启用智能配图
)
```

3. **自动配图逻辑**：
   - 如果幻灯片没有指定图片，系统会自动生成
   - 根据幻灯片标题和内容生成相关图片
   - 图片保存在 `images/generated/` 目录

## 功能 2: LangGraph 反思机制

### 功能描述
使用 LangGraph 反思机制，通过 3-7 轮对话提升 ChatBot 生成质量或内容深度，再给到用户反馈。同时，ChatHistory 适配仅保留最终生成版本。

### 实现方式
- 使用 LangGraph 构建多轮反思工作流
- 每轮包括：生成 → 反思 → 改进 → 再生成
- 最多进行 3-7 轮迭代
- 最终只返回优化后的结果

### 使用方法

```python
from src.langgraph_reflection_agent import LangGraphReflectionAgent

# 初始化反思 Agent
agent = LangGraphReflectionAgent(
    system_prompt_path="prompts/formatter.txt",
    max_iterations=5  # 3-7 轮之间
)

# 使用反思机制生成内容
markdown_text = agent.generate_with_reflection(user_input)
```

### 工作流程
1. **生成阶段**：生成初始 Markdown 内容
2. **反思阶段**：评估内容质量，识别改进点
3. **改进阶段**：基于反思结果优化内容
4. **迭代**：重复上述过程，直到达到最大迭代次数或质量满足要求
5. **输出**：返回最终优化后的内容

## 功能 3: Streamlit 界面集成

### 功能描述
使用 Streamlit 前端框架，将 ChatPPT 已经集成的 Whisper、MiniCPM 等模型通过更强的交互能力，便捷地提供给用户。

### 功能特点
- **文本输入模式**：传统的文本输入生成 PPT
- **语音输入模式**：使用 Whisper 将语音转换为文字
- **混合模式**：结合文本和语音输入
- **模型集成**：
  - Whisper：语音转文字
  - MiniCPM：本地 LLM 生成内容
  - 反思机制：提升生成质量
  - 图像生成：智能配图

### 使用方法

1. **启动 Streamlit 应用**：
```bash
streamlit run src/streamlit_app.py
```

2. **功能使用**：
   - **文本输入**：在"文本输入"标签页输入内容，点击生成
   - **语音输入**：在"语音输入"标签页上传音频文件，自动转写并生成
   - **配置选项**：
     - 启用/禁用反思机制
     - 启用/禁用智能配图
     - 选择加载 Whisper 或 MiniCPM 模型

3. **模型加载**：
   - Whisper：首次使用时会自动下载模型（base 模型）
   - MiniCPM：需要手动加载，模型较大（约 2GB）

## 配置说明

### config.json 完整配置示例

```json
{
    "input_mode": "text",
    "ppt_template": "templates/MasterTemplate.pptx",
    "layout_mapping": {
        "Title Only": 0,
        "Title and Content": 1,
        "Title and Picture": 2,
        "Title, Content, and Picture": 3
    },
    "image_generator": {
        "provider": "openai",
        "openai_api_key": "",
        "stability_api_key": "",
        "local_sd_url": "http://localhost:7860"
    },
    "reflection": {
        "enabled": true,
        "max_iterations": 5
    }
}
```

## 依赖安装

```bash
pip install -r requirements.txt
```

新增依赖：
- `langgraph>=0.0.20` - LangGraph 反思机制
- `streamlit>=1.28.0` - Streamlit 界面
- `openai-whisper>=20231117` - Whisper 语音转文字
- `transformers>=4.35.0` - MiniCPM 模型
- `torch>=2.0.0` - PyTorch（MiniCPM 需要）
- `stability-sdk>=0.8.0` - Stability AI SDK（可选）

## 文件结构

```
ChatPPT/
├── src/
│   ├── image_generator.py          # 图像生成模块
│   ├── langgraph_reflection_agent.py  # LangGraph 反思机制
│   ├── streamlit_app.py            # Streamlit 界面
│   └── ...
├── images/
│   └── generated/                   # 生成的图片目录
├── config.json                      # 配置文件
└── requirements.txt                 # 依赖列表
```

## 使用示例

### 示例 1: 使用图像生成

```python
from src.config import Config
from src.gradio_server import generate_ppt_from_markdown

config = Config()
markdown = """
# AI 技术概述
## 机器学习基础
- 监督学习
- 无监督学习
"""

# 启用智能配图
output, status = generate_ppt_from_markdown(
    markdown, 
    config, 
    enable_image_generation=True
)
```

### 示例 2: 使用反思机制

```python
from src.langgraph_reflection_agent import LangGraphReflectionAgent

agent = LangGraphReflectionAgent("prompts/formatter.txt", max_iterations=5)
result = agent.generate_with_reflection("创建一个关于深度学习的演示文稿")
```

### 示例 3: 启动 Streamlit

```bash
streamlit run src/streamlit_app.py
```

然后在浏览器中访问显示的地址（通常是 `http://localhost:8501`）

## 注意事项

1. **图像生成成本**：
   - OpenAI DALL-E 3 按图片收费
   - 建议仅在需要时启用

2. **反思机制**：
   - 会增加 API 调用次数（3-7 倍）
   - 但能显著提升生成质量

3. **模型加载**：
   - Whisper 和 MiniCPM 模型较大
   - 首次使用需要下载
   - 建议在有 GPU 的环境中使用 MiniCPM

4. **ChatHistory 适配**：
   - 反思机制只保留最终生成版本
   - 中间过程不显示给用户
   - 减少界面复杂度

