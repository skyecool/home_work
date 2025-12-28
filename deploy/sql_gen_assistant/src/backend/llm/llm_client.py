from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMClient(ABC):
    """LLM客户端抽象基类，定义统一的接口"""
    
    @abstractmethod
    def generate_sql(self, natural_language: str, table_schema: str) -> Dict[str, Any]:
        """
        将自然语言转换为SQL查询
        
        Args:
            natural_language: 用户的自然语言查询
            table_schema: 数据库表结构信息
            
        Returns:
            包含生成的SQL语句和其他相关信息的字典
        """
        pass
    
    @abstractmethod
    def fix_sql(self, sql: str, error_message: str, table_schema: str) -> Dict[str, Any]:
        """
        修复错误的SQL语句
        
        Args:
            sql: 错误的SQL语句
            error_message: 错误信息
            table_schema: 数据库表结构信息
            
        Returns:
            包含修复后的SQL语句和其他相关信息的字典
        """
        pass
