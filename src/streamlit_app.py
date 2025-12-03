"""
Streamlit 前端界面
集成 Whisper、MiniCPM 等模型，提供更强的交互能力
"""
import os
import streamlit as st
from typing import Optional
import tempfile
from logger import LOG

# 导入 ChatPPT 核心模块
from config import Config
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from template_manager import load_template, get_layout_mapping
from layout_manager import LayoutManager
from langgraph_reflection_agent import LangGraphReflectionAgent


# 页面配置
st.set_page_config(
    page_title="ChatPPT - AI PowerPoint Generator",
    page_icon="🎨",
    layout="wide"
)

# 初始化 session state
if "config" not in st.session_state:
    st.session_state.config = Config()
if "reflection_agent" not in st.session_state:
    try:
        system_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'formatter.txt')
        st.session_state.reflection_agent = LangGraphReflectionAgent(
            system_prompt_path,
            max_iterations=5
        )
    except Exception as e:
        st.session_state.reflection_agent = None
        st.warning(f"反思 Agent 初始化失败: {str(e)}")


def load_whisper_model():
    """加载 Whisper 模型（语音转文字）"""
    try:
        import whisper
        if "whisper_model" not in st.session_state:
            with st.spinner("正在加载 Whisper 模型..."):
                st.session_state.whisper_model = whisper.load_model("base")
        return st.session_state.whisper_model
    except ImportError:
        st.error("未安装 whisper 库，请运行: pip install openai-whisper")
        return None
    except Exception as e:
        st.error(f"加载 Whisper 模型失败: {str(e)}")
        return None


def load_minicpm_model():
    """加载 MiniCPM 模型"""
    try:
        # MiniCPM 可以通过 transformers 加载
        from transformers import AutoModelForCausalLM, AutoTokenizer
        if "minicpm_model" not in st.session_state:
            with st.spinner("正在加载 MiniCPM 模型..."):
                model_name = "openbmb/MiniCPM-2B-sft-bf16"
                st.session_state.minicpm_tokenizer = AutoTokenizer.from_pretrained(model_name)
                st.session_state.minicpm_model = AutoModelForCausalLM.from_pretrained(model_name)
        return st.session_state.minicpm_model, st.session_state.minicpm_tokenizer
    except ImportError:
        st.warning("未安装 transformers 库，MiniCPM 功能将不可用")
        return None, None
    except Exception as e:
        st.warning(f"加载 MiniCPM 模型失败: {str(e)}")
        return None, None


def transcribe_audio(audio_file) -> Optional[str]:
    """使用 Whisper 将音频转换为文字"""
    model = load_whisper_model()
    if not model:
        return None
    
    try:
        # 保存上传的音频文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        
        # 转写
        result = model.transcribe(tmp_path)
        os.unlink(tmp_path)  # 删除临时文件
        
        return result["text"]
    except Exception as e:
        st.error(f"音频转写失败: {str(e)}")
        return None


def generate_with_minicpm(prompt: str) -> Optional[str]:
    """使用 MiniCPM 生成内容"""
    model, tokenizer = load_minicpm_model()
    if not model or not tokenizer:
        return None
    
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=512)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        st.error(f"MiniCPM 生成失败: {str(e)}")
        return None


def main():
    """主函数"""
    st.title("🎨 ChatPPT - AI PowerPoint Generator")
    st.markdown("使用自然语言描述你的演示文稿内容，AI 将自动生成 PowerPoint 文件！")
    
    # 侧边栏：模型配置
    with st.sidebar:
        st.header("⚙️ 配置")
        
        # 输入模式选择
        input_mode = st.radio(
            "输入模式",
            ["文本输入", "语音输入", "混合模式"],
            help="选择输入方式"
        )
        
        # 功能开关
        use_reflection = st.checkbox(
            "启用反思机制",
            value=True,
            help="使用 LangGraph 反思机制提升生成质量（3-7轮对话）"
        )
        
        enable_image_gen = st.checkbox(
            "启用智能配图",
            value=False,
            help="使用图像生成模型为幻灯片自动配图"
        )
        
        # 模型加载选项
        st.subheader("模型选项")
        load_whisper = st.checkbox("加载 Whisper（语音转文字）", value=False)
        load_minicpm = st.checkbox("加载 MiniCPM（本地 LLM）", value=False)
        
        if load_whisper:
            load_whisper_model()
        if load_minicpm:
            load_minicpm_model()
    
    # 主界面
    tab1, tab2, tab3 = st.tabs(["📝 文本输入", "🎤 语音输入", "📊 生成结果"])
    
    with tab1:
        st.subheader("文本输入模式")
        user_input = st.text_area(
            "输入你的演示文稿内容",
            placeholder="例如：创建一个关于人工智能的演示文稿，包含3张幻灯片：1. 标题页 2. AI简介 3. 应用场景",
            height=200
        )
        
        if st.button("生成 PowerPoint", type="primary"):
            if not user_input.strip():
                st.warning("请输入演示文稿内容")
            else:
                with st.spinner("正在生成..."):
                    try:
                        # 使用反思机制（如果启用）
                        if use_reflection and st.session_state.reflection_agent:
                            markdown_text = st.session_state.reflection_agent.generate_with_reflection(user_input)
                        else:
                            # 使用普通 ChatBot
                            from gradio_server import ChatBot
                            system_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'formatter.txt')
                            chatbot = ChatBot(system_prompt_path)
                            markdown_text = chatbot.format_to_markdown(user_input)
                        
                        # 生成 PowerPoint
                        output_path, status_msg = generate_ppt_from_markdown(
                            markdown_text, 
                            st.session_state.config,
                            enable_image_generation=enable_image_gen
                        )
                        
                        if output_path:
                            st.success(status_msg)
                            st.session_state.generated_ppt = output_path
                            st.session_state.markdown_output = markdown_text
                            
                            # 显示生成的 Markdown
                            with tab3:
                                st.subheader("生成的 Markdown")
                                st.code(markdown_text, language="markdown")
                                
                                # 下载按钮
                                with open(output_path, "rb") as f:
                                    st.download_button(
                                        label="📥 下载 PowerPoint",
                                        data=f.read(),
                                        file_name=os.path.basename(output_path),
                                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                    )
                        else:
                            st.error(status_msg)
                    except Exception as e:
                        st.error(f"生成失败: {str(e)}")
                        LOG.error(f"生成失败: {str(e)}")
    
    with tab2:
        st.subheader("语音输入模式")
        st.info("上传音频文件，使用 Whisper 转换为文字后生成 PowerPoint")
        
        audio_file = st.file_uploader(
            "上传音频文件",
            type=["wav", "mp3", "m4a", "ogg"],
            help="支持 WAV, MP3, M4A, OGG 格式"
        )
        
        if audio_file:
            st.audio(audio_file, format="audio/wav")
            
            if st.button("转写并生成", type="primary"):
                with st.spinner("正在转写音频..."):
                    transcribed_text = transcribe_audio(audio_file)
                    
                    if transcribed_text:
                        st.success("转写成功！")
                        st.text_area("转写结果", transcribed_text, height=150)
                        
                        # 使用转写结果生成 PPT
                        with st.spinner("正在生成 PowerPoint..."):
                            try:
                                if use_reflection and st.session_state.reflection_agent:
                                    markdown_text = st.session_state.reflection_agent.generate_with_reflection(transcribed_text)
                                else:
                                    from gradio_server import ChatBot
                                    system_prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'formatter.txt')
                                    chatbot = ChatBot(system_prompt_path)
                                    markdown_text = chatbot.format_to_markdown(transcribed_text)
                                
                                output_path, status_msg = generate_ppt_from_markdown(
                                    markdown_text,
                                    st.session_state.config,
                                    enable_image_generation=enable_image_gen
                                )
                                
                                if output_path:
                                    st.success(status_msg)
                                    st.session_state.generated_ppt = output_path
                                    st.session_state.markdown_output = markdown_text
                                else:
                                    st.error(status_msg)
                            except Exception as e:
                                st.error(f"生成失败: {str(e)}")
                    else:
                        st.error("音频转写失败")
    
    with tab3:
        st.subheader("生成结果")
        
        if "markdown_output" in st.session_state:
            st.code(st.session_state.markdown_output, language="markdown")
        
        if "generated_ppt" in st.session_state and os.path.exists(st.session_state.generated_ppt):
            st.success(f"✅ PowerPoint 文件已生成")
            with open(st.session_state.generated_ppt, "rb") as f:
                st.download_button(
                    label="📥 下载 PowerPoint",
                    data=f.read(),
                    file_name=os.path.basename(st.session_state.generated_ppt),
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        else:
            st.info("请先使用文本或语音输入生成 PowerPoint")


if __name__ == "__main__":
    main()

