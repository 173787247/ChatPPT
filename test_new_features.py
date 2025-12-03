"""
测试新功能：图像生成、LangGraph 反思机制、Streamlit 集成
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.config import Config
from src.gradio_server import generate_ppt_from_markdown
from src.langgraph_reflection_agent import LangGraphReflectionAgent
from logger import LOG


def test_image_generation():
    """测试图像生成功能"""
    print("\n" + "="*50)
    print("测试 1: 图像生成功能")
    print("="*50)
    
    try:
        from src.image_generator import ImageGenerator
        
        config = Config()
        image_gen = ImageGenerator(config.__dict__)
        
        # 测试生成图像
        test_prompt = "Professional business presentation about artificial intelligence"
        image_path = image_gen.generate_image(test_prompt, "AI Technology")
        
        if image_path:
            print(f"✅ 图像生成成功: {image_path}")
            return True
        else:
            print("❌ 图像生成失败")
            return False
    except Exception as e:
        print(f"❌ 图像生成测试失败: {str(e)}")
        return False


def test_reflection_agent():
    """测试 LangGraph 反思机制"""
    print("\n" + "="*50)
    print("测试 2: LangGraph 反思机制")
    print("="*50)
    
    try:
        system_prompt_path = os.path.join("prompts", "formatter.txt")
        agent = LangGraphReflectionAgent(system_prompt_path, max_iterations=3)
        
        test_input = "创建一个关于机器学习的演示文稿，包含3张幻灯片：1. 标题页 2. 机器学习简介 3. 应用场景"
        
        print("正在使用反思机制生成内容（最多3轮）...")
        result = agent.generate_with_reflection(test_input)
        
        if result:
            print(f"✅ 反思机制测试成功")
            print(f"生成内容长度: {len(result)} 字符")
            return True
        else:
            print("❌ 反思机制测试失败：未生成内容")
            return False
    except Exception as e:
        print(f"❌ 反思机制测试失败: {str(e)}")
        return False


def test_ppt_with_image_gen():
    """测试带图像生成的 PPT 生成"""
    print("\n" + "="*50)
    print("测试 3: PPT 生成（启用图像生成）")
    print("="*50)
    
    try:
        config = Config()
        markdown_text = """
# 人工智能技术
## 机器学习基础
- 监督学习
- 无监督学习
## 深度学习应用
- 图像识别
- 自然语言处理
"""
        
        output_path, status = generate_ppt_from_markdown(
            markdown_text,
            config,
            enable_image_generation=True
        )
        
        if output_path and os.path.exists(output_path):
            print(f"✅ PPT 生成成功（带图像生成）: {output_path}")
            return True
        else:
            print(f"❌ PPT 生成失败: {status}")
            return False
    except Exception as e:
        print(f"❌ PPT 生成测试失败: {str(e)}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*50)
    print("ChatPPT 新功能测试")
    print("="*50)
    
    results = []
    
    # 测试 1: 图像生成
    results.append(("图像生成", test_image_generation()))
    
    # 测试 2: 反思机制
    results.append(("LangGraph 反思机制", test_reflection_agent()))
    
    # 测试 3: PPT 生成（带图像生成）
    results.append(("PPT 生成（图像生成）", test_ppt_with_image_gen()))
    
    # 输出测试结果
    print("\n" + "="*50)
    print("测试结果汇总")
    print("="*50)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, result in results if result)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查配置和依赖")


if __name__ == "__main__":
    main()

