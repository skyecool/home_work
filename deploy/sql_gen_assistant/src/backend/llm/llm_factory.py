from typing import Optional
from .llm_client import LLMClient
from .ollama_client import OllamaClient
from .deepseek_client import DeepSeekClient
from .zhipu_client import ZhipuClient


class LLMFactory:
    """LLM客户端工厂类，用于创建不同类型的LLM客户端实例"""
    
    @staticmethod
    def create_client(model_name: str = "llama3:8b", api_key: Optional[str] = None) -> LLMClient:
        """
        根据模型名称创建相应的LLM客户端实例
        
        Args:
            model_name: 模型名称，如"llama3:8b", "gpt-3.5-turbo", "deepseek-coder", "glm-4"
            api_key: API密钥，对于本地模型如Ollama不需要
            
        Returns:
            LLMClient实例
        """
        if model_name.startswith("deepseek-"):
            return DeepSeekClient(model=model_name, api_key=api_key)
        elif model_name.startswith("glm-"):
            return ZhipuClient(model=model_name, api_key=api_key)
        else:
            return OllamaClient(model=model_name)
