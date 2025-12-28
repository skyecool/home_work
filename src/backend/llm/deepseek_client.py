from typing import Dict, Any
from .llm_client import LLMClient
import requests


class DeepSeekClient(LLMClient):
    """DeepSeek客户端实现，用于调用DeepSeek API"""
    
    def __init__(self, model: str = "deepseek-coder", api_key: str = None):
        """
        初始化DeepSeek客户端
        
        Args:
            model: 要使用的DeepSeek模型名称，默认为deepseek-coder
            api_key: DeepSeek API密钥
        """
        self.model = model
        self.api_key = api_key
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
    
    def generate_sql(self, natural_language: str, table_schema: str) -> Dict[str, Any]:
        """
        使用DeepSeek模型将自然语言转换为SQL查询
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "DeepSeek API密钥未设置",
                "model": self.model
            }
        
        # 构建提示词
        prompt = f"""
        你是一个专业的SQL查询生成器。请根据用户的自然语言描述和提供的数据库表结构，生成准确的SQL查询语句。
        
        数据库表结构如下：
        {table_schema}
        
        请严格按照以下要求生成SQL查询：
        1. 只生成SQL查询语句，不要包含任何解释或其他文本
        2. 确保SQL语法正确，能够在SQLite数据库中执行
        3. 使用正确的表名和列名，注意大小写敏感
        4. 对于多表查询，确保正确使用JOIN语句和关联条件
        5. 只返回最终的SQL查询结果，不要包含任何多余的内容
        
        用户的自然语言查询：{natural_language}
        """
        
        try:
            # 调用DeepSeek API生成SQL
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            sql = result["choices"][0]["message"]["content"].strip()
            
            return {
                "success": True,
                "sql": sql,
                "model": self.model
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API调用失败: {str(e)}",
                "model": self.model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
    
    def fix_sql(self, sql: str, error_message: str, table_schema: str) -> Dict[str, Any]:
        """
        使用DeepSeek模型修复错误的SQL语句
        """
        if not self.api_key:
            return {
                "success": False,
                "error": "DeepSeek API密钥未设置",
                "model": self.model
            }
        
        # 构建提示词
        prompt = f"""
        你是一个专业的SQL查询修复专家。请根据提供的错误信息和数据库表结构，修复给定的SQL查询语句。
        
        数据库表结构如下：
        {table_schema}
        
        错误的SQL查询：
        {sql}
        
        错误信息：
        {error_message}
        
        请严格按照以下要求修复SQL查询：
        1. 只生成修复后的SQL查询语句，不要包含任何解释或其他文本
        2. 确保SQL语法正确，能够在SQLite数据库中执行
        3. 使用正确的表名和列名，注意大小写敏感
        4. 对于多表查询，确保正确使用JOIN语句和关联条件
        5. 只返回最终的SQL查询结果，不要包含任何多余的内容
        """
        
        try:
            # 调用DeepSeek API修复SQL
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            fixed_sql = result["choices"][0]["message"]["content"].strip()
            
            return {
                "success": True,
                "sql": fixed_sql,
                "model": self.model
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API调用失败: {str(e)}",
                "model": self.model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
