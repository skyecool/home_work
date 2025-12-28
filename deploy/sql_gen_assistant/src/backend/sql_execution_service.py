from typing import Dict, Any
from .sql_generator_service import SQLGeneratorService


class SQLExecutionService:
    """SQL执行服务，负责执行SQL查询并处理错误修正"""
    
    def __init__(self):
        self.sql_generator = SQLGeneratorService()
    
    def execute_natural_language_query(self, natural_language: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        执行自然语言查询，包括SQL生成、执行和自动错误修正
        
        Args:
            natural_language: 用户的自然语言查询
            max_retries: 最大重试次数，包括原始尝试
            
        Returns:
            包含最终结果的字典
        """
        results = {
            "steps": [],
            "final_result": None
        }
        
        # 步骤1: 生成SQL
        generate_result = self.sql_generator.generate_sql(natural_language)
        results["steps"].append({
            "step": "generate",
            "result": generate_result
        })
        
        if not generate_result["success"]:
            return {
                "success": False,
                "error": generate_result["error"],
                **results
            }
        
        sql = generate_result["sql"]
        
        # 步骤2: 执行SQL并处理错误
        for attempt in range(max_retries):
            execute_result = self.sql_generator.execute_sql(sql)
            results["steps"].append({
                "step": "execute",
                "attempt": attempt + 1,
                "sql": sql,
                "result": execute_result
            })
            
            if execute_result["success"]:
                # SQL执行成功，返回结果
                return {
                    "success": True,
                    "data": execute_result["data"],
                    "final_sql": sql,
                    **results
                }
            
            # SQL执行失败，需要修正
            if attempt < max_retries - 1:  # 还有重试机会
                # 步骤3: 修正SQL
                fix_result = self.sql_generator.fix_sql(sql, execute_result["error"])
                results["steps"].append({
                    "step": "fix",
                    "attempt": attempt + 1,
                    "result": fix_result
                })
                
                if not fix_result["success"]:
                    # 无法修正，返回错误
                    return {
                        "success": False,
                        "error": f"无法修正SQL: {fix_result['error']}",
                        **results
                    }
                
                # 使用修正后的SQL进行下一次尝试
                sql = fix_result["sql"]
        
        # 所有重试都失败
        return {
            "success": False,
            "error": f"经过{max_retries}次尝试仍无法执行SQL，最后的错误信息: {execute_result['error']}",
            "final_sql": sql,
            **results
        }
