@echo off

REM 基于大模型的自然语言转SQL查询工具 - 一键部署脚本（Windows）

echo ==================================================
echo 基于大模型的自然语言转SQL查询工具 - 一键部署
echo ==================================================

REM 创建应用目录
set APP_DIR=%~dp0\sql_gen_assistant
echo 创建应用目录: %APP_DIR%
mkdir "%APP_DIR%" 2>nul

REM 复制项目文件
echo 复制项目文件...
xcopy "..\src" "%APP_DIR%\src" /E /Y
xcopy "..\docs" "%APP_DIR%\docs" /E /Y
copy "..\seed_books.py" "%APP_DIR%" /Y
copy "..\requirements.txt" "%APP_DIR%" /Y
copy "..\.env.example" "%APP_DIR%" /Y
copy "..\.gitignore" "%APP_DIR%" /Y

REM 进入应用目录
cd "%APP_DIR%"

REM 检查Python版本
echo 检查Python版本...
python --version

REM 验证Python版本是否符合要求
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
set PYTHON_MAJOR_MINOR=%PYTHON_VERSION:~0,3%
set MIN_VERSION=3.9

REM 比较Python版本
if "%PYTHON_MAJOR_MINOR%" LSS "%MIN_VERSION%" (
    echo 警告：Python版本 %PYTHON_VERSION% 低于推荐版本 %MIN_VERSION%
    echo 某些依赖可能无法正常安装或运行
    echo 按任意键继续，或关闭窗口取消
    pause >nul
)

REM 创建虚拟环境
echo 创建虚拟环境...
python -m venv venv

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 升级pip
echo 升级pip...
pip install --upgrade pip

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 创建.env文件
echo 创建环境变量配置文件...
copy .env.example .env /Y

REM 执行预录入脚本
echo 执行预录入脚本，录入100本经典高中、大学图书...
python seed_books.py

REM 退出虚拟环境
deactivate

echo ==================================================
echo 部署完成！
echo ==================================================
echo 下一步：
echo 1. 编辑环境变量配置文件: %APP_DIR%\.env
echo 2. 运行启动脚本: run.bat
echo 3. 通过浏览器访问: http://localhost:8505
echo.
echo 如果需要配置API密钥，请编辑.env文件：
echo - DeepSeek API: DEEPSEEK_API_KEY=your_deepseek_api_key
echo - 智谱AI API: ZHIPU_API_KEY=your_zhipu_api_key
echo.
echo ==================================================
pause