import os
from dotenv import load_dotenv

class Config:
    """配置管理类"""
    
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        
        # 大模型API配置
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
        self.zhipu_api_key = os.getenv("ZHIPU_API_KEY", "")
        
        # 默认模型配置
        self.default_model = os.getenv("DEFAULT_MODEL", "llama3:8b")
        
        # 数据库配置
        self.database_path = os.getenv("DATABASE_PATH", "./src/data/library.db")
        
        # 确保数据库路径使用平台无关的格式
        self.database_path = os.path.normpath(self.database_path)
        # 确保数据库目录存在
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
    
    def get_api_key_for_model(self, model_name: str) -> str:
        """
        根据模型名称获取对应的API密钥
        
        Args:
            model_name: 模型名称
            
        Returns:
            对应的API密钥，如果没有则返回空字符串
        """
        if model_name.startswith("deepseek-"):
            return self.deepseek_api_key
        elif model_name.startswith("gpt-"):
            return self.openai_api_key
        elif model_name.startswith("glm-"):
            return self.zhipu_api_key
        else:
            return ""

# 创建全局配置实例
config = Config()
