from typing import Dict, Any
from .config import config
from .database_manager import db_manager
from .llm.llm_factory import LLMFactory


class SQLGeneratorService:
    """SQL生成服务，负责将自然语言转换为SQL查询"""
    
    def __init__(self):
        api_key = config.get_api_key_for_model(config.default_model)
        self.llm_client = LLMFactory.create_client(model_name=config.default_model, api_key=api_key)
    
    def _format_table_schema(self) -> str:
        """
        格式化数据库表结构，使其适合大模型理解
        
        Returns:
            格式化后的表结构字符串
        """
        schema_info = db_manager.get_table_schema()
        formatted_schema = []
        
        for table_name, table_info in schema_info.items():
            formatted_schema.append(f"表名: {table_name}")
            formatted_schema.append("列信息:")
            
            for column in table_info['columns']:
                column_name = column[1]  # name
                column_type = column[2]  # type
                is_nullable = "NOT NULL" if column[3] == 0 else "NULL"  # notnull
                is_primary = "PRIMARY KEY" if column[5] == 1 else ""
                
                column_desc = f"  - {column_name} {column_type} {is_nullable}"
                if is_primary:
                    column_desc += f" {is_primary}"
                formatted_schema.append(column_desc)
            
            if table_info['foreign_keys']:
                formatted_schema.append("外键关系:")
                for fk in table_info['foreign_keys']:
                    fk_column = fk[3]  # from
                    ref_table = fk[2]  # table
                    ref_column = fk[4]  # to
                    formatted_schema.append(f"  - {fk_column} REFERENCES {ref_table}({ref_column})")
            
            formatted_schema.append("")
        
        return "\n".join(formatted_schema)
    
    def generate_sql(self, natural_language: str) -> Dict[str, Any]:
        """
        将自然语言转换为SQL查询
        
        Args:
            natural_language: 用户的自然语言查询
            
        Returns:
            包含生成的SQL语句和其他相关信息的字典
        """
        # 获取格式化的表结构
        table_schema = self._format_table_schema()
        
        # 调用LLM生成SQL
        result = self.llm_client.generate_sql(natural_language, table_schema)
        
        return result
    
    def fix_sql(self, sql: str, error_message: str) -> Dict[str, Any]:
        """
        修复错误的SQL语句
        
        Args:
            sql: 错误的SQL语句
            error_message: 错误信息
            
        Returns:
            包含修复后的SQL语句和其他相关信息的字典
        """
        # 获取格式化的表结构
        table_schema = self._format_table_schema()
        
        # 调用LLM修复SQL
        result = self.llm_client.fix_sql(sql, error_message, table_schema)
        
        return result
    
    def execute_sql(self, sql: str) -> Dict[str, Any]:
        """
        执行SQL查询并返回结果
        
        Args:
            sql: 要执行的SQL语句
            
        Returns:
            包含查询结果的字典
        """
        return db_manager.execute_query(sql)
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        获取数据库信息，包括表名和示例数据
        
        Returns:
            包含数据库信息的字典
        """
        table_names = db_manager.get_table_names()
        sample_data = {}
        
        for table_name in table_names:
            sample = db_manager.get_sample_data(table_name, limit=3)
            if sample['success']:
                sample_data[table_name] = sample['data']
        
        return {
            'table_names': table_names,
            'sample_data': sample_data
        }
