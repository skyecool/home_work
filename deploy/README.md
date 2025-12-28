# 基于大模型的自然语言转SQL查询工具 - 一键部署工具包

## 项目简介

本工具包提供了基于大模型的自然语言转SQL查询工具的一键部署解决方案，支持Windows、macOS和Linux系统。

## 功能特性

- ✅ 自然语言转SQL查询
- ✅ 多模型支持（Ollama、DeepSeek API、智谱AI API）
- ✅ 自动错误修正
- ✅ E-R图可视化
- ✅ 图书录入功能
- ✅ 数据库可视化
- ✅ 预录入100本经典高中、大学图书

## 系统要求

- Python 3.10+
- 支持Windows、macOS、Linux系统

## 部署步骤

### 1. 解压部署包

将部署包解压到任意目录，例如：
```
/opt/sql_gen_assistant
```

### 2. 运行一键部署脚本

#### Windows系统
```cmd
setup.bat
```

#### macOS/Linux系统
```bash
chmod +x setup.sh
./setup.sh
```

### 3. 配置环境变量

部署完成后，根据提示编辑`.env`文件，配置API密钥（可选，仅当使用DeepSeek或智谱AI时需要）：

```
# DeepSeek API配置（可选）
DEEPSEEK_API_KEY=your_deepseek_api_key

# 智谱AI API配置（可选）
ZHIPU_API_KEY=your_zhipu_api_key
```

### 4. 启动应用

#### Windows系统
```cmd
run.bat
```

#### macOS/Linux系统
```bash
./run.sh
```

### 5. 访问应用

应用启动后，通过浏览器访问以下地址：
- 本地访问：http://localhost:8505
- 网络访问：http://<your_ip>:8505

## 目录结构

```
deploy/
├── README.md              # 部署说明文档
├── setup.sh               # macOS/Linux部署脚本
├── setup.bat              # Windows部署脚本
├── run.sh                 # macOS/Linux启动脚本
├── run.bat                # Windows启动脚本
├── .env.example           # 环境变量示例文件
└── sql_gen_assistant/     # 应用程序目录
    ├── src/               # 源代码
    ├── seed_books.py      # 预录入脚本
    ├── requirements.txt   # 依赖列表
    └── .gitignore         # Git忽略文件
```

## 功能使用

### 自然语言查询
1. 在左侧边栏选择"自然语言查询"功能
2. 选择要使用的大模型
3. 输入自然语言问题，如"查询所有文学类图书"
4. 点击"执行查询"按钮
5. 查看生成的SQL和执行结果

### 图书录入
1. 在左侧边栏选择"图书录入"功能
2. 填写图书基本信息
3. 选择或手动录入出版社、作者和分类
4. 点击"录入图书"按钮

### E-R图可视化
1. 在左侧边栏选择"E-R图可视化"功能
2. 查看自动生成的数据库实体关系图

### 数据库结构
1. 在左侧边栏选择"数据库结构"功能
2. 选择要查看的表
3. 查看表结构和示例数据

## 预录入图书数据

系统已预录入100本经典高中、大学图书，包括：
- 文学经典（《百年孤独》、《活着》等）
- 哲学思想（《理想国》、《资本论》等）
- 科学经典（《时间简史》、《物种起源》等）

## 技术支持

如遇到问题，请参考以下解决方案：

1. **端口被占用**：修改`run.sh`或`run.bat`中的端口号
2. **依赖安装失败**：确保Python版本≥3.10，或尝试手动安装依赖
3. **模型调用失败**：检查API密钥配置是否正确
4. **E-R图生成失败**：确保已安装Graphviz

## 更新日志

- v1.0.0 (2025-12-28)
  - 首次发布
  - 支持Ollama、DeepSeek API、智谱AI API
  - 实现自然语言转SQL、自动错误修正、E-R图可视化等功能
  - 预录入100本经典高中、大学图书

## 许可证

MIT License
