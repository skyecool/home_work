from graphviz import Digraph
from typing import Dict, Any
from .database_manager import db_manager


class ERDiagramService:
    """E-R图可视化服务，负责生成数据库的实体关系图"""
    
    def generate_er_diagram(self, output_format: str = "png", output_path: str = None) -> Dict[str, Any]:
        """
        生成数据库的E-R图
        
        Args:
            output_format: 输出格式，支持png, svg, pdf等，默认为png
            output_path: 输出路径，默认为当前目录
            
        Returns:
            包含E-R图生成结果的字典
        """
        try:
            # 获取数据库表结构
            schema_info = db_manager.get_table_schema()
            
            # 创建有向图
            dot = Digraph(name='图书管理系统E-R图', format=output_format, engine='dot')
            dot.attr(rankdir='LR', size='12,8')
            dot.attr('node', shape='rectangle', style='filled', fillcolor='lightblue2', fontname='SimHei')
            dot.attr('edge', fontname='SimHei')
            
            # 1. 添加所有实体（表）
            for table_name in schema_info.keys():
                # 获取表的列信息
                columns = schema_info[table_name]['columns']
                
                # 生成表的标签，包含列信息
                table_label = f"{table_name}\n"
                for column in columns:
                    column_name = column[1]
                    column_type = column[2]
                    is_primary = "PK" if column[5] == 1 else ""
                    is_foreign = "FK" if any(fk[3] == column_name for fk in schema_info[table_name]['foreign_keys']) else ""
                    
                    constraints = []
                    if is_primary:
                        constraints.append(is_primary)
                    if is_foreign:
                        constraints.append(is_foreign)
                    
                    constraint_str = f"({', '.join(constraints)})" if constraints else ""
                    table_label += f"{column_name} {column_type} {constraint_str}\n"
                
                # 添加实体节点
                dot.node(table_name, label=table_label.strip())
            
            # 2. 添加所有关系（外键）
            added_relations = set()
            for table_name, table_info in schema_info.items():
                for fk in table_info['foreign_keys']:
                    fk_column = fk[3]  # 外键列
                    ref_table = fk[2]  # 引用表
                    ref_column = fk[4]  # 引用列
                    
                    # 生成关系标识，避免重复添加
                    relation_key = f"{table_name}:{ref_table}"
                    if relation_key not in added_relations:
                        # 添加关系边
                        dot.edge(table_name, ref_table, label=f"{fk_column} → {ref_column}")
                        added_relations.add(relation_key)
            
            # 3. 生成并保存E-R图
            if output_path:
                # 如果提供了输出路径，使用该路径
                output_file = output_path
            else:
                # 否则使用默认路径
                output_file = "./src/data/er_diagram"
            
            # 渲染图表
            result = dot.render(output_file, view=False, cleanup=True)
            
            return {
                "success": True,
                "output_file": result,
                "format": output_format,
                "message": f"E-R图已成功生成: {result}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "生成E-R图失败"
            }
    
    def get_er_diagram_svg(self) -> str:
        """
        生成E-R图的SVG字符串，用于在网页中显示
        
        Returns:
            SVG格式的E-R图字符串
        """
        try:
            # 获取数据库表结构
            schema_info = db_manager.get_table_schema()
            
            # 创建有向图
            dot = Digraph(name='图书管理系统E-R图', format='svg', engine='dot')
            dot.attr(rankdir='LR', size='12,8')
            dot.attr('node', shape='rectangle', style='filled', fillcolor='lightblue2', fontname='SimHei')
            dot.attr('edge', fontname='SimHei')
            
            # 添加所有实体（表）
            for table_name in schema_info.keys():
                columns = schema_info[table_name]['columns']
                
                table_label = f"{table_name}\n"
                for column in columns:
                    column_name = column[1]
                    column_type = column[2]
                    is_primary = "PK" if column[5] == 1 else ""
                    is_foreign = "FK" if any(fk[3] == column_name for fk in schema_info[table_name]['foreign_keys']) else ""
                    
                    constraints = []
                    if is_primary:
                        constraints.append(is_primary)
                    if is_foreign:
                        constraints.append(is_foreign)
                    
                    constraint_str = f"({', '.join(constraints)})" if constraints else ""
                    table_label += f"{column_name} {column_type} {constraint_str}\n"
                
                dot.node(table_name, label=table_label.strip())
            
            # 添加所有关系（外键）
            added_relations = set()
            for table_name, table_info in schema_info.items():
                for fk in table_info['foreign_keys']:
                    fk_column = fk[3]
                    ref_table = fk[2]
                    ref_column = fk[4]
                    
                    relation_key = f"{table_name}:{ref_table}"
                    if relation_key not in added_relations:
                        dot.edge(table_name, ref_table, label=f"{fk_column} → {ref_column}")
                        added_relations.add(relation_key)
            
            # 生成SVG字符串
            svg_content = dot.pipe().decode('utf-8')
            return svg_content
        except Exception as e:
            return f"<p>生成E-R图失败: {str(e)}</p>"
