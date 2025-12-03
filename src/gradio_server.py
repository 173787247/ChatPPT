"""
Gradio ChatBot 界面
支持将用户输入转换为 ChatPPT PowerPoint 标准输入格式（Markdown），并最终生成 PowerPoint 文件
"""
import os
import gradio as gr
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import Config
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from template_manager import load_template, get_layout_mapping
from layout_manager import LayoutManager
from slide_builder import SlideBuilder
from data_structures import PowerPoint, Slide
from logger import LOG


class ChatBot:
    """ChatBot 类，用于将用户输入转换为 Markdown 格式"""
    
    def __init__(self, system_prompt_path: str, api_key: Optional[str] = None):
        """
        初始化 ChatBot
        
        Args:
            system_prompt_path: System Prompt 文件路径
            api_key: OpenAI API Key（如果为 None，则从环境变量读取）
        """
        # 读取 System Prompt
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            self.system_prompt = f.read()
        
        # 初始化 LLM
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("需要提供 OPENAI_API_KEY 环境变量或参数")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=api_key
        )
        
        # 对话历史
        self.conversation_history = []
    
    def format_to_markdown(self, user_input: str) -> str:
        """
        将用户输入转换为 Markdown 格式
        
        Args:
            user_input: 用户输入的自然语言
            
        Returns:
            str: 转换后的 Markdown 格式文本
        """
        # 构建消息
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"请将以下内容转换为 ChatPPT 标准输入格式（Markdown）：\n\n{user_input}")
        ]
        
        # 调用 LLM
        try:
            response = self.llm.invoke(messages)
            markdown_text = response.content.strip()
            
            # 清理响应（移除可能的代码块标记）
            if markdown_text.startswith('```'):
                lines = markdown_text.split('\n')
                if lines[0].startswith('```'):
                    lines = lines[1:]
                if lines[-1].startswith('```'):
                    lines = lines[:-1]
                markdown_text = '\n'.join(lines)
            
            LOG.info("成功将用户输入转换为 Markdown 格式")
            return markdown_text
        except Exception as e:
            LOG.error(f"转换失败: {str(e)}")
            raise


def generate_ppt_from_markdown(markdown_text: str, config: Config) -> tuple[str, str]:
    """
    从 Markdown 文本生成 PowerPoint 文件
    
    Args:
        markdown_text: Markdown 格式的输入文本
        config: 配置对象
        
    Returns:
        tuple: (输出文件路径, 状态消息)
    """
    try:
        # 加载模板
        template_path = config.ppt_template
        prs = load_template(template_path)
        
        # 获取布局映射
        layout_mapping = get_layout_mapping(prs)
        
        # 解析输入文本
        powerpoint_data, presentation_title = parse_input_text(markdown_text, layout_mapping)
        
        # 使用 LayoutManager 自动分配布局
        layout_manager = LayoutManager(layout_mapping)
        
        # 重新构建幻灯片，使用自动布局分配
        new_slides = []
        for slide in powerpoint_data.slides:
            slide_builder = SlideBuilder(layout_manager)
            slide_builder.set_title(slide.content.title)
            for point in slide.content.bullet_points:
                slide_builder.add_bullet_point(point)
            if slide.content.image_path:
                slide_builder.set_image(slide.content.image_path)
            new_slide = slide_builder.finalize()
            new_slides.append(new_slide)
        
        # 更新 PowerPoint 数据
        powerpoint_data.slides = new_slides
        
        # 生成输出路径
        output_dir = os.path.join(os.getcwd(), 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{presentation_title}.pptx")
        
        # 生成 PowerPoint
        generate_presentation(powerpoint_data, template_path, output_path)
        
        return output_path, f"✅ PowerPoint 文件已生成：{presentation_title}.pptx"
    except Exception as e:
        LOG.error(f"生成 PowerPoint 失败: {str(e)}")
        return "", f"❌ 生成失败：{str(e)}"


def chat_with_bot(user_message: str, history: list, chatbot: ChatBot, config: Config) -> tuple[list, str, str]:
    """
    与 ChatBot 对话并生成 PowerPoint
    
    Args:
        user_message: 用户消息
        history: 对话历史
        chatbot: ChatBot 实例
        config: 配置对象
        
    Returns:
        tuple: (更新后的历史, 清空的输入框, 生成的 Markdown 文本)
    """
    if not user_message.strip():
        return history, "", ""
    
    try:
        # 转换为 Markdown
        markdown_text = chatbot.format_to_markdown(user_message)
        
        # 生成 PowerPoint
        output_path, status_msg = generate_ppt_from_markdown(markdown_text, config)
        
        # 更新历史
        history.append((user_message, f"{status_msg}\n\n**生成的 Markdown：**\n```markdown\n{markdown_text}\n```"))
        
        return history, "", markdown_text
    except Exception as e:
        error_msg = f"❌ 错误：{str(e)}"
        history.append((user_message, error_msg))
        return history, "", ""


def create_gradio_interface():
    """创建 Gradio 界面"""
    # 加载配置
    config = Config()
    
    # 初始化 ChatBot
    system_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'formatter.txt')
    chatbot = ChatBot(system_prompt_path)
    
    # 创建 Gradio 界面
    with gr.Blocks(title="ChatPPT - AI PowerPoint Generator", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🎨 ChatPPT - AI PowerPoint Generator
        
        使用自然语言描述你的演示文稿内容，AI 将自动生成 PowerPoint 文件！
        
        **功能特点：**
        - 💬 自然语言输入
        - 📝 自动转换为 Markdown 格式
        - 🎯 自动布局分配
        - 📊 支持文本、图片、表格和图表
        - ⚡ 一键生成 PowerPoint
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                chatbot_interface = gr.Chatbot(
                    label="对话",
                    height=400,
                    show_copy_button=True
                )
                user_input = gr.Textbox(
                    label="输入你的演示文稿内容",
                    placeholder="例如：创建一个关于人工智能的演示文稿，包含3张幻灯片：1. 标题页 2. AI简介 3. 应用场景",
                    lines=3
                )
                submit_btn = gr.Button("生成 PowerPoint", variant="primary", size="lg")
            
            with gr.Column(scale=1):
                gr.Markdown("### 📋 使用说明")
                gr.Markdown("""
                1. 在输入框中描述你的演示文稿内容
                2. 可以包含：
                   - 标题和主题
                   - 幻灯片数量
                   - 每张幻灯片的内容
                   - 图片需求
                3. 点击"生成 PowerPoint"按钮
                4. 系统会自动生成 Markdown 并创建 PPT 文件
                """)
                
                markdown_output = gr.Textbox(
                    label="生成的 Markdown",
                    lines=10,
                    interactive=False
                )
        
        # 绑定事件
        submit_btn.click(
            chat_with_bot,
            inputs=[user_input, chatbot_interface, gr.State(chatbot), gr.State(config)],
            outputs=[chatbot_interface, user_input, markdown_output]
        )
        
        user_input.submit(
            chat_with_bot,
            inputs=[user_input, chatbot_interface, gr.State(chatbot), gr.State(config)],
            outputs=[chatbot_interface, user_input, markdown_output]
        )
    
    return app


if __name__ == "__main__":
    # 创建并启动界面
    app = create_gradio_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )

