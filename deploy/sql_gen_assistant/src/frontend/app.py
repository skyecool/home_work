#!/usr/bin/env python3
"""
基于大模型的自然语言转SQL查询工具 - Streamlit应用
"""

import streamlit as st
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.sql_execution_service import SQLExecutionService
from backend.er_diagram_service import ERDiagramService
from backend.sql_generator_service import SQLGeneratorService


# 初始化服务
sql_execution_service = SQLExecutionService()
er_diagram_service = ERDiagramService()
sql_generator_service = SQLGeneratorService()


def main():
    # 设置页面配置
    st.set_page_config(
        page_title="基于大模型的自然语言转SQL查询工具",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 页面标题
    st.title("基于大模型的自然语言转SQL查询工具")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("系统功能")
        
        # 功能选择
        feature = st.radio(
            "选择功能",
            ["自然语言查询", "图书录入", "E-R图可视化", "数据库结构"]
        )
        
        # 模型选择
        model_option = st.selectbox(
            "选择LLM模型",
            ["llama3:8b", "deepseek-coder", "deepseek-chat", "glm-4", "glm-3-turbo"]
        )
        
        # API密钥配置
        if model_option.startswith("deepseek-"):
            deepseek_api_key = st.text_input(
                "DeepSeek API密钥",
                type="password",
                help="请输入您的DeepSeek API密钥"
            )
            # 将API密钥保存到会话状态
            if deepseek_api_key:
                st.session_state["deepseek_api_key"] = deepseek_api_key
            else:
                st.session_state["deepseek_api_key"] = None
        elif model_option.startswith("glm-"):
            zhipu_api_key = st.text_input(
                "智谱AI API密钥",
                type="password",
                help="请输入您的智谱AI API密钥"
            )
            # 将API密钥保存到会话状态
            if zhipu_api_key:
                st.session_state["zhipu_api_key"] = zhipu_api_key
            else:
                st.session_state["zhipu_api_key"] = None
        
        # 将选中的模型保存到会话状态
        st.session_state["selected_model"] = model_option
        
        st.markdown("---")
        
        # 关于系统
        st.header("关于系统")
        st.write("本系统是一个基于大模型的自然语言转SQL查询工具，支持:")
        st.write("✅ 自然语言到SQL的自动转换")
        st.write("✅ SQL执行和结果展示")
        st.write("✅ 自动错误修正")
        st.write("✅ E-R图可视化")
        st.write("✅ 数据库结构查看")
        st.write("✅ 示例数据展示")
    
    # 主内容区
    if feature == "自然语言查询":
        show_natural_language_query()
    elif feature == "图书录入":
        show_book_entry()
    elif feature == "E-R图可视化":
        show_er_diagram()
    elif feature == "数据库结构":
        show_database_structure()


def show_natural_language_query():
    """显示自然语言查询功能"""
    st.subheader("自然语言查询")
    
    # 查询输入区
    col1, col2 = st.columns([3, 1])
    with col1:
        natural_language = st.text_area(
            "请输入您的自然语言查询",
            placeholder="例如: 查询所有图书的标题和价格",
            height=100
        )
    
    with col2:
        max_retries = st.slider(
            "最大重试次数",
            min_value=1,
            max_value=3,
            value=2,
            help="当生成的SQL执行失败时，系统会自动尝试修正的次数"
        )
        
        submit_button = st.button(
            "执行查询",
            type="primary",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # 结果展示区
    if submit_button and natural_language:
        with st.spinner("正在处理您的查询..."):
            # 根据用户选择的模型动态创建LLM客户端
            from backend.llm.llm_factory import LLMFactory
            from backend.config import config
            
            selected_model = st.session_state.get("selected_model", "llama3:8b")
            api_key = None
            
            if selected_model.startswith("deepseek-"):
                api_key = st.session_state.get("deepseek_api_key", None)
            elif selected_model.startswith("glm-"):
                api_key = st.session_state.get("zhipu_api_key", None)
            
            # 重新初始化SQL生成服务，使用选定的模型
            from backend.sql_generator_service import SQLGeneratorService
            from backend.sql_execution_service import SQLExecutionService
            
            # 创建新的SQL生成服务实例，使用选定的模型
            custom_sql_generator = SQLGeneratorService()
            custom_sql_generator.llm_client = LLMFactory.create_client(model_name=selected_model, api_key=api_key)
            
            # 创建新的SQL执行服务实例
            custom_sql_execution_service = SQLExecutionService()
            custom_sql_execution_service.sql_generator = custom_sql_generator
            
            # 执行自然语言查询
            result = custom_sql_execution_service.execute_natural_language_query(natural_language, max_retries)
        
        # 显示处理步骤
        st.subheader("处理步骤")
        
        for i, step in enumerate(result["steps"]):
            if step["step"] == "generate":
                with st.expander(f"步骤 {i+1}: 生成SQL"):
                    if step["result"]["success"]:
                        st.code(step["result"]["sql"], language="sql")
                    else:
                        st.error(f"生成SQL失败: {step['result']['error']}")
            
            elif step["step"] == "execute":
                with st.expander(f"步骤 {i+1}: 执行SQL (尝试 {step['attempt']})"):
                    st.code(step["sql"], language="sql")
                    if step["result"]["success"]:
                        st.success("SQL执行成功")
                    else:
                        st.error(f"SQL执行失败: {step['result']['error']}")
            
            elif step["step"] == "fix":
                with st.expander(f"步骤 {i+1}: 修正SQL (尝试 {step['attempt']})"):
                    if step["result"]["success"]:
                        st.code(step["result"]["sql"], language="sql")
                    else:
                        st.error(f"修正SQL失败: {step['result']['error']}")
        
        st.markdown("---")
        
        # 显示最终结果
        st.subheader("最终结果")
        
        if result["success"]:
            st.success("查询成功")
            
            # 显示最终SQL
            st.markdown("### 最终生成的SQL")
            st.code(result["final_sql"], language="sql")
            
            # 显示查询结果
            st.markdown("### 查询结果")
            if result["data"]:
                st.dataframe(result["data"])
                st.write(f"共返回 {len(result['data'])} 条记录")
            else:
                st.info("查询结果为空")
        else:
            st.error(f"查询失败: {result['error']}")
    
    elif submit_button:
        st.warning("请输入查询内容")


def show_er_diagram():
    """显示E-R图可视化功能"""
    st.subheader("E-R图可视化")
    
    with st.spinner("正在生成E-R图..."):
        svg_content = er_diagram_service.get_er_diagram_svg()
    
    # 显示E-R图
    st.markdown("### 数据库实体关系图")
    st.markdown("下图展示了数据库中所有表之间的关系:")
    st.components.v1.html(svg_content, height=800)


def show_book_entry():
    """显示图书录入功能"""
    st.subheader("图书录入")
    
    from backend.database_manager import db_manager
    
    # 获取现有数据用于下拉选择
    def get_publishers():
        result = db_manager.execute_query("SELECT publisher_id, publisher_name FROM publishers")
        if result['success']:
            return {p['publisher_name']: p['publisher_id'] for p in result['data']}
        return {}
    
    def get_authors():
        result = db_manager.execute_query("SELECT author_id, author_name FROM authors")
        if result['success']:
            return {a['author_name']: a['author_id'] for a in result['data']}
        return {}
    
    def get_categories():
        result = db_manager.execute_query("SELECT category_id, category_name FROM categories")
        if result['success']:
            return {c['category_name']: c['category_id'] for c in result['data']}
        return {}
    
    # 获取或创建出版社
    def get_or_create_publisher(publisher_name):
        result = db_manager.execute_query("SELECT publisher_id FROM publishers WHERE publisher_name = ?", (publisher_name,))
        if result['success'] and result['data']:
            return result['data'][0]['publisher_id']
        # 创建新出版社
        insert_result = db_manager.execute_query("INSERT INTO publishers (publisher_name, country) VALUES (?, ?)", (publisher_name, "中国"))
        if insert_result['success']:
            return insert_result['data']['last_id']
        return None
    
    # 获取或创建作者
    def get_or_create_author(author_name):
        result = db_manager.execute_query("SELECT author_id FROM authors WHERE author_name = ?", (author_name,))
        if result['success'] and result['data']:
            return result['data'][0]['author_id']
        # 创建新作者
        insert_result = db_manager.execute_query("INSERT INTO authors (author_name) VALUES (?)", (author_name,))
        if insert_result['success']:
            return insert_result['data']['last_id']
        return None
    
    # 获取或创建分类
    def get_or_create_category(category_name):
        result = db_manager.execute_query("SELECT category_id FROM categories WHERE category_name = ?", (category_name,))
        if result['success'] and result['data']:
            return result['data'][0]['category_id']
        # 创建新分类
        insert_result = db_manager.execute_query("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
        if insert_result['success']:
            return insert_result['data']['last_id']
        return None
    
    publishers = get_publishers()
    authors = get_authors()
    categories = get_categories()
    
    # 图书录入表单
    with st.form("book_entry_form"):
        st.markdown("### 图书基本信息")
        
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("书名")
            isbn = st.text_input("ISBN")
            
            # 出版社选择或手动录入
            st.markdown("#### 出版社")
            publisher_option = st.radio("出版社录入方式", ["从现有列表选择", "手动录入新出版社"], key="publisher_option", horizontal=True)
            if publisher_option == "从现有列表选择":
                publisher = st.selectbox("选择出版社", list(publishers.keys()), index=None, placeholder="请选择出版社", key="publisher_select")
                manual_publisher = None
            else:
                manual_publisher = st.text_input("手动输入出版社名称", key="manual_publisher")
                publisher = None
        
        with col2:
            publication_year = st.number_input("出版年份", min_value=1900, max_value=2100, value=2025)
            price = st.number_input("价格", min_value=0.01, step=0.01, value=0.01)
            stock = st.number_input("库存", min_value=0, step=1, value=0)
        
        # 作者选择或手动录入
        st.markdown("### 图书作者")
        author_option = st.radio("作者录入方式", ["从现有列表选择", "手动录入新作者"], key="author_option", horizontal=True)
        if author_option == "从现有列表选择":
            selected_authors = st.multiselect("选择作者（可多选）", list(authors.keys()), placeholder="请选择作者", key="authors_select")
            manual_authors = None
        else:
            manual_authors_input = st.text_input("手动输入作者名称，多个作者用逗号分隔", key="manual_authors")
            manual_authors = [author.strip() for author in manual_authors_input.split(",") if author.strip()]
            selected_authors = None
        
        # 分类选择或手动录入
        st.markdown("### 图书分类")
        category_option = st.radio("分类录入方式", ["从现有列表选择", "手动录入新分类"], key="category_option", horizontal=True)
        if category_option == "从现有列表选择":
            selected_categories = st.multiselect("选择分类（可多选）", list(categories.keys()), placeholder="请选择分类", key="categories_select")
            manual_categories = None
        else:
            manual_categories_input = st.text_input("手动输入分类名称，多个分类用逗号分隔", key="manual_categories")
            manual_categories = [category.strip() for category in manual_categories_input.split(",") if category.strip()]
            selected_categories = None
        
        # 提交按钮
        submit_button = st.form_submit_button("录入图书", type="primary")
    
    # 处理表单提交
    if submit_button:
        # 验证必填字段
        if not title:
            st.error("请填写书名")
        elif not isbn:
            st.error("请填写ISBN")
        # 验证出版社
        elif publisher_option == "从现有列表选择" and not publisher:
            st.error("请选择出版社")
        elif publisher_option == "手动录入新出版社" and not manual_publisher:
            st.error("请输入出版社名称")
        # 验证作者
        elif author_option == "从现有列表选择" and not selected_authors:
            st.error("请选择至少一位作者")
        elif author_option == "手动录入新作者" and not manual_authors:
            st.error("请输入至少一位作者")
        # 验证分类
        elif category_option == "从现有列表选择" and not selected_categories:
            st.error("请选择至少一个分类")
        elif category_option == "手动录入新分类" and not manual_categories:
            st.error("请输入至少一个分类")
        else:
            # 处理出版社
            if publisher_option == "从现有列表选择":
                publisher_id = publishers[publisher]
                final_publisher = publisher
            else:
                publisher_id = get_or_create_publisher(manual_publisher)
                final_publisher = manual_publisher
            
            # 处理作者
            if author_option == "从现有列表选择":
                author_ids = [authors[author] for author in selected_authors]
                final_authors = selected_authors
            else:
                author_ids = []
                final_authors = []
                for author_name in manual_authors:
                    author_id = get_or_create_author(author_name)
                    if author_id:
                        author_ids.append(author_id)
                        final_authors.append(author_name)
            
            # 处理分类
            if category_option == "从现有列表选择":
                category_ids = [categories[category] for category in selected_categories]
                final_categories = selected_categories
            else:
                category_ids = []
                final_categories = []
                for category_name in manual_categories:
                    category_id = get_or_create_category(category_name)
                    if category_id:
                        category_ids.append(category_id)
                        final_categories.append(category_name)
            
            # 插入图书基本信息
            book_query = """
            INSERT INTO books (title, isbn, publisher_id, publication_year, price, stock)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            book_params = (title, isbn, publisher_id, publication_year, price, stock)
            
            result = db_manager.execute_query(book_query, book_params)
            
            if result['success']:
                # 获取刚插入的图书ID
                book_id = result['data']['last_id']
                
                # 插入图书-作者关系
                author_success = True
                for author_id in author_ids:
                    author_query = "INSERT INTO book_authors (book_id, author_id) VALUES (?, ?)"
                    author_result = db_manager.execute_query(author_query, (book_id, author_id))
                    if not author_result['success']:
                        author_success = False
                        break
                
                # 插入图书-分类关系
                category_success = True
                for category_id in category_ids:
                    category_query = "INSERT INTO book_categories (book_id, category_id) VALUES (?, ?)"
                    category_result = db_manager.execute_query(category_query, (book_id, category_id))
                    if not category_result['success']:
                        category_success = False
                        break
                
                if author_success and category_success:
                    st.success("图书录入成功！")
                    
                    # 显示录入的图书信息
                    st.markdown("### 录入成功的图书信息")
                    st.write(f"书名: {title}")
                    st.write(f"ISBN: {isbn}")
                    st.write(f"出版社: {final_publisher}")
                    st.write(f"出版年份: {publication_year}")
                    st.write(f"价格: {price}")
                    st.write(f"库存: {stock}")
                    st.write(f"作者: {', '.join(final_authors)}")
                    st.write(f"分类: {', '.join(final_categories)}")
                else:
                    st.error("图书基本信息录入成功，但关联关系录入失败，请联系管理员。")
            else:
                st.error(f"图书录入失败: {result['error']}")
    
    # 显示当前图书列表
    st.markdown("---")
    st.markdown("### 当前图书列表")
    
    books_result = db_manager.execute_query("""
    SELECT b.book_id, b.title, b.isbn, p.publisher_name, b.publication_year, b.price, b.stock
    FROM books b
    LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
    ORDER BY b.book_id DESC
    LIMIT 10
    """)
    
    if books_result['success'] and books_result['data']:
        st.dataframe(books_result['data'])
    else:
        st.info("当前没有图书数据")


def show_database_structure():
    """显示数据库结构功能"""
    st.subheader("数据库结构")
    
    # 获取数据库信息
    db_info = sql_generator_service.get_database_info()
    
    # 显示表名列表
    st.markdown("### 表列表")
    table_names = db_info["table_names"]
    selected_table = st.selectbox("选择一个表查看详情", table_names)
    
    st.markdown("---")
    
    # 显示选定表的结构
    st.markdown(f"### 表 {selected_table} 结构")
    
    # 获取表结构信息
    from backend.database_manager import db_manager
    schema_info = db_manager.get_table_schema()
    table_info = schema_info[selected_table]
    
    # 显示列信息
    st.markdown("#### 列信息")
    columns_data = []
    for column in table_info['columns']:
        column_name = column[1]
        column_type = column[2]
        is_nullable = "否" if column[3] == 0 else "是"
        is_primary = "是" if column[5] == 1 else "否"
        is_foreign = "是" if any(fk[3] == column_name for fk in table_info['foreign_keys']) else "否"
        
        columns_data.append({
            "列名": column_name,
            "数据类型": column_type,
            "是否为空": is_nullable,
            "是否为主键": is_primary,
            "是否为外键": is_foreign
        })
    
    st.dataframe(columns_data)
    
    # 显示外键关系
    if table_info['foreign_keys']:
        st.markdown("#### 外键关系")
        fk_data = []
        for fk in table_info['foreign_keys']:
            fk_data.append({
                "外键列": fk[3],
                "引用表": fk[2],
                "引用列": fk[4]
            })
        
        st.dataframe(fk_data)
    
    # 显示示例数据
    st.markdown("#### 示例数据")
    sample_data = db_info["sample_data"][selected_table]
    if sample_data:
        st.dataframe(sample_data)
        st.write(f"显示前 {len(sample_data)} 条记录")
    else:
        st.info("该表没有示例数据")


if __name__ == "__main__":
    main()
