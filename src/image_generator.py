"""
图像生成模块
支持使用 Stable Diffusion 或其他文生图模型为 PowerPoint 智能配图
"""
import os
import requests
from typing import Optional
from logger import LOG


class ImageGenerator:
    """
    图像生成器，支持多种图像生成模型
    """
    
    def __init__(self, config: dict):
        """
        初始化图像生成器
        
        Args:
            config: 配置字典，包含图像生成相关配置
        """
        self.config = config
        self.image_output_dir = os.path.join("images", "generated")
        os.makedirs(self.image_output_dir, exist_ok=True)
        
        # 支持的图像生成服务
        self.provider = config.get("image_generator", {}).get("provider", "openai")  # openai, stability, local_sd
        
        # 初始化对应的客户端
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "stability":
            self._init_stability()
        elif self.provider == "local_sd":
            self._init_local_sd()
        else:
            LOG.warning(f"不支持的图像生成服务: {self.provider}，将使用 OpenAI DALL-E")
            self._init_openai()
    
    def _init_openai(self):
        """初始化 OpenAI DALL-E"""
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = OpenAI(api_key=api_key)
                self.model = "dall-e-3"
                LOG.info("已初始化 OpenAI DALL-E 图像生成器")
            else:
                LOG.warning("未设置 OPENAI_API_KEY，图像生成功能将不可用")
                self.client = None
        except ImportError:
            LOG.warning("未安装 openai 库，图像生成功能将不可用")
            self.client = None
    
    def _init_stability(self):
        """初始化 Stability AI"""
        try:
            import stability_sdk.client
            api_key = self.config.get("image_generator", {}).get("stability_api_key") or os.getenv("STABILITY_API_KEY")
            if api_key:
                self.client = stability_sdk.client.StabilityInference(
                    key=api_key,
                    verbose=True
                )
                self.model = "stable-diffusion-xl-1024-v1-0"
                LOG.info("已初始化 Stability AI 图像生成器")
            else:
                LOG.warning("未设置 STABILITY_API_KEY，图像生成功能将不可用")
                self.client = None
        except ImportError:
            LOG.warning("未安装 stability-sdk 库，图像生成功能将不可用")
            self.client = None
    
    def _init_local_sd(self):
        """初始化本地 Stable Diffusion"""
        try:
            # 使用 Hugging Face Diffusers 或本地 API
            sd_url = self.config.get("image_generator", {}).get("local_sd_url", "http://localhost:7860")
            self.client = {"url": sd_url}
            self.model = "local-stable-diffusion"
            LOG.info(f"已初始化本地 Stable Diffusion: {sd_url}")
        except Exception as e:
            LOG.warning(f"初始化本地 Stable Diffusion 失败: {str(e)}")
            self.client = None
    
    def generate_image(self, prompt: str, slide_title: str = "", size: str = "1024x1024") -> Optional[str]:
        """
        根据提示词生成图像
        
        Args:
            prompt: 图像生成提示词
            slide_title: 幻灯片标题（用于上下文）
            size: 图像尺寸，默认 1024x1024
            
        Returns:
            生成的图像文件路径，如果失败返回 None
        """
        if not self.client:
            LOG.warning("图像生成器未初始化，无法生成图像")
            return None
        
        try:
            # 增强提示词（结合幻灯片标题）
            enhanced_prompt = prompt
            if slide_title:
                enhanced_prompt = f"{prompt}, related to: {slide_title}"
            
            LOG.info(f"正在生成图像: {enhanced_prompt}")
            
            # 根据不同的服务调用不同的生成方法
            if self.provider == "openai":
                image_path = self._generate_openai(enhanced_prompt, size)
            elif self.provider == "stability":
                image_path = self._generate_stability(enhanced_prompt, size)
            elif self.provider == "local_sd":
                image_path = self._generate_local_sd(enhanced_prompt, size)
            else:
                image_path = None
            
            if image_path:
                LOG.info(f"图像生成成功: {image_path}")
                return image_path
            else:
                LOG.warning("图像生成失败")
                return None
                
        except Exception as e:
            LOG.error(f"生成图像时出错: {str(e)}")
            return None
    
    def _generate_openai(self, prompt: str, size: str) -> Optional[str]:
        """使用 OpenAI DALL-E 生成图像"""
        try:
            response = self.client.images.generate(
                model=self.model,
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # 下载图像
            image_data = requests.get(image_url).content
            image_filename = f"generated_{hash(prompt) % 100000}.png"
            image_path = os.path.join(self.image_output_dir, image_filename)
            
            with open(image_path, "wb") as f:
                f.write(image_data)
            
            return image_path
        except Exception as e:
            LOG.error(f"OpenAI 图像生成失败: {str(e)}")
            return None
    
    def _generate_stability(self, prompt: str, size: str) -> Optional[str]:
        """使用 Stability AI 生成图像"""
        try:
            answers = self.client.generate(
                prompt=prompt,
                width=1024,
                height=1024,
            )
            
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == 1:  # SUCCESS
                        image_filename = f"generated_{hash(prompt) % 100000}.png"
                        image_path = os.path.join(self.image_output_dir, image_filename)
                        
                        with open(image_path, "wb") as f:
                            f.write(artifact.binary)
                        
                        return image_path
            
            return None
        except Exception as e:
            LOG.error(f"Stability AI 图像生成失败: {str(e)}")
            return None
    
    def _generate_local_sd(self, prompt: str, size: str) -> Optional[str]:
        """使用本地 Stable Diffusion 生成图像"""
        try:
            # 调用本地 SD API（如使用 Automatic1111 WebUI）
            url = f"{self.client['url']}/sdapi/v1/txt2img"
            payload = {
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, distorted",
                "steps": 20,
                "width": 1024,
                "height": 1024,
            }
            
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                import base64
                image_data = base64.b64decode(result["images"][0])
                
                image_filename = f"generated_{hash(prompt) % 100000}.png"
                image_path = os.path.join(self.image_output_dir, image_filename)
                
                with open(image_path, "wb") as f:
                    f.write(image_data)
                
                return image_path
            else:
                LOG.error(f"本地 SD API 调用失败: {response.status_code}")
                return None
        except Exception as e:
            LOG.error(f"本地 SD 图像生成失败: {str(e)}")
            return None
    
    def generate_image_for_slide(self, slide_content: str, slide_title: str = "") -> Optional[str]:
        """
        为幻灯片智能生成配图
        
        Args:
            slide_content: 幻灯片内容（要点列表）
            slide_title: 幻灯片标题
            
        Returns:
            生成的图像文件路径
        """
        # 从幻灯片内容提取图像生成提示词
        prompt = self._extract_image_prompt(slide_content, slide_title)
        
        if not prompt:
            LOG.warning("无法从幻灯片内容提取图像提示词")
            return None
        
        return self.generate_image(prompt, slide_title)
    
    def _extract_image_prompt(self, slide_content: str, slide_title: str) -> Optional[str]:
        """
        从幻灯片内容提取图像生成提示词
        
        Args:
            slide_content: 幻灯片内容
            slide_title: 幻灯片标题
            
        Returns:
            图像生成提示词
        """
        # 简单的提示词提取逻辑
        # 可以后续使用 LLM 来优化提示词生成
        
        # 结合标题和内容生成提示词
        if slide_title:
            prompt = f"Professional presentation image about {slide_title}"
        else:
            # 从内容中提取关键词
            keywords = slide_content.split()[:5]  # 取前5个词
            prompt = f"Professional presentation image: {', '.join(keywords)}"
        
        # 添加风格描述
        prompt += ", clean, modern, professional, suitable for business presentation"
        
        return prompt

