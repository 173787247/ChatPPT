import json
import os

class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        # 检查 config 文件是否存在
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' not found.")

        with open(self.config_file, 'r') as f:
            config = json.load(f)
            
            # 加载 ChatPPT 运行模式（默认文本模态）
            self.input_mode = config.get('input_mode', "text")
            
            # 加载 PPT 默认模板
            self.ppt_template = config.get('ppt_template', "templates/MasterTemplate.pptx")
            
            # 加载布局映射
            self.layout_mapping = config.get('layout_mapping', {})
            
            # 加载图像生成配置
            self.image_generator = config.get('image_generator', {})
            
            # 加载反思机制配置
            self.reflection = config.get('reflection', {})