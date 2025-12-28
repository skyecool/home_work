import sqlite3
import os
from .config import config

class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self):
        self.db_path = config.database_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库，创建表结构并填充示例数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建出版社表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            publisher_name TEXT NOT NULL,
            country TEXT NOT NULL
        )
        ''')
        
        # 创建作者表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            author_id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT NOT NULL,
            birth_year INTEGER
        )
        ''')
        
        # 创建图书分类表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL
        )
        ''')
        
        # 创建图书表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            isbn TEXT NOT NULL UNIQUE,
            publisher_id INTEGER,
            publication_year INTEGER,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
        )
        ''')
        
        # 创建图书-作者关系表（多对多）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_authors (
            book_id INTEGER,
            author_id INTEGER,
            PRIMARY KEY (book_id, author_id),
            FOREIGN KEY (book_id) REFERENCES books (book_id),
            FOREIGN KEY (author_id) REFERENCES authors (author_id)
        )
        ''')
        
        # 创建图书-分类关系表（多对多）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_categories (
            book_id INTEGER,
            category_id INTEGER,
            PRIMARY KEY (book_id, category_id),
            FOREIGN KEY (book_id) REFERENCES books (book_id),
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
        ''')
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'reader'
        )
        ''')
        
        # 创建借阅记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS borrow_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            borrow_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (book_id) REFERENCES books (book_id)
        )
        ''')
        
        # 检查是否已有数据
        cursor.execute('SELECT COUNT(*) FROM publishers')
        if cursor.fetchone()[0] == 0:
            # 填充出版社数据
            publishers = [
                ('清华大学出版社', '中国'),
                ('机械工业出版社', '中国'),
                ('人民邮电出版社', '中国'),
                ('电子工业出版社', '中国'),
                ('北京大学出版社', '中国')
            ]
            cursor.executemany('INSERT INTO publishers (publisher_name, country) VALUES (?, ?)', publishers)
            
            # 填充作者数据
            authors = [
                ('张三', 1970),
                ('李四', 1985),
                ('王五', 1990),
                ('赵六', 1978),
                ('孙七', 1982)
            ]
            cursor.executemany('INSERT INTO authors (author_name, birth_year) VALUES (?, ?)', authors)
            
            # 填充分类数据
            categories = [
                ('计算机科学',),
                ('文学',),
                ('历史',),
                ('经济',),
                ('教育',)
            ]
            cursor.executemany('INSERT INTO categories (category_name) VALUES (?)', categories)
            
            # 填充图书数据
            books = [
                ('Python编程从入门到精通', '9787115523028', 1, 2023, 89.00, 10),
                ('Java核心技术', '9787111641247', 2, 2022, 128.00, 8),
                ('数据结构与算法分析', '9787111640905', 2, 2021, 99.00, 5),
                ('数据库系统概论', '9787302551637', 1, 2020, 79.00, 12),
                ('机器学习实战', '9787115523035', 1, 2023, 88.00, 7)
            ]
            cursor.executemany('INSERT INTO books (title, isbn, publisher_id, publication_year, price, stock) VALUES (?, ?, ?, ?, ?, ?)', books)
            
            # 填充图书-作者关系
            book_authors = [
                (1, 1),  # 图书1的作者是作者1
                (1, 2),  # 图书1的作者是作者2
                (2, 3),  # 图书2的作者是作者3
                (3, 4),  # 图书3的作者是作者4
                (4, 5),  # 图书4的作者是作者5
                (5, 1),  # 图书5的作者是作者1
                (5, 3)   # 图书5的作者是作者3
            ]
            cursor.executemany('INSERT INTO book_authors (book_id, author_id) VALUES (?, ?)', book_authors)
            
            # 填充图书-分类关系
            book_categories = [
                (1, 1),  # 图书1属于分类1
                (2, 1),  # 图书2属于分类1
                (3, 1),  # 图书3属于分类1
                (4, 1),  # 图书4属于分类1
                (5, 1),  # 图书5属于分类1
                (5, 4)   # 图书5属于分类4
            ]
            cursor.executemany('INSERT INTO book_categories (book_id, category_id) VALUES (?, ?)', book_categories)
            
            # 填充用户数据
            users = [
                ('读者1', 'reader1@example.com', 'reader'),
                ('读者2', 'reader2@example.com', 'reader'),
                ('管理员', 'admin@example.com', 'admin')
            ]
            cursor.executemany('INSERT INTO users (user_name, email, role) VALUES (?, ?, ?)', users)
            
            # 填充借阅记录数据
            borrow_records = [
                (1, 1, '2024-01-15', '2024-02-15'),  # 用户1借阅图书1
                (1, 2, '2024-03-01', None),  # 用户1借阅图书2（未归还）
                (2, 3, '2024-02-20', '2024-03-20'),  # 用户2借阅图书3
                (2, 5, '2024-04-01', None)   # 用户2借阅图书5（未归还）
            ]
            cursor.executemany('INSERT INTO borrow_records (user_id, book_id, borrow_date, return_date) VALUES (?, ?, ?, ?)', borrow_records)
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """执行SQL查询并返回结果"""
        # 确保数据库路径使用平台无关的格式
        db_path = os.path.normpath(self.db_path)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # 使用字典形式返回结果
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # 如果是查询语句，返回结果
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
                return {'success': True, 'data': results}
            else:
                conn.commit()
                # 对于INSERT语句，返回最后插入的ID
                if query.strip().upper().startswith('INSERT'):
                    last_id = cursor.lastrowid
                    return {'success': True, 'data': {'last_id': last_id}}
                return {'success': True, 'data': None}
        except sqlite3.Error as e:
            return {'success': False, 'error': str(e)}
        finally:
            conn.close()
    
    def get_table_schema(self):
        """获取数据库表结构信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [table[0] for table in cursor.fetchall()]
        
        schema_info = {}
        for table in tables:
            # 获取表的列信息
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            
            # 获取表的外键信息
            cursor.execute(f"PRAGMA foreign_key_list({table})")
            foreign_keys = cursor.fetchall()
            
            schema_info[table] = {
                'columns': columns,
                'foreign_keys': foreign_keys
            }
        
        conn.close()
        return schema_info
    
    def get_table_names(self):
        """获取所有表名"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [table[0] for table in cursor.fetchall()]
        conn.close()
        return tables
    
    def get_sample_data(self, table_name, limit=5):
        """获取表的示例数据"""
        query = f"SELECT * FROM {table_name} LIMIT ?"
        result = self.execute_query(query, (limit,))
        return result

# 创建数据库管理器实例
db_manager = DatabaseManager()
