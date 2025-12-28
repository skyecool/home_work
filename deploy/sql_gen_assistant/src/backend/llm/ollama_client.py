from typing import Dict, Any
from .llm_client import LLMClient
import ollama


class OllamaClient(LLMClient):
    """Ollama客户端实现，用于本地运行的大模型"""
    
    def __init__(self, model: str = "llama3:8b"):
        """
        初始化Ollama客户端
        
        Args:
            model: 要使用的Ollama模型名称，默认为llama3:8b
        """
        self.model = model
    
    def generate_sql(self, natural_language: str, table_schema: str) -> Dict[str, Any]:
        """
        使用Ollama模型将自然语言转换为SQL查询
        """
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
            # 调用Ollama API生成SQL
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={"temperature": 0.1}
            )
            
            sql = response["response"].strip()
            
            return {
                "success": True,
                "sql": sql,
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
        使用Ollama模型修复错误的SQL语句
        """
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
            # 调用Ollama API修复SQL
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={"temperature": 0.1}
            )
            
            fixed_sql = response["response"].strip()
            
            return {
                "success": True,
                "sql": fixed_sql,
                "model": self.model
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
