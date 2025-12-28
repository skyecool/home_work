@echo off

REM 基于大模型的自然语言转SQL查询工具 - 启动脚本（Windows）

set APP_DIR=%~dp0\sql_gen_assistant

REM 检查应用目录是否存在
if not exist "%APP_DIR%" (
    echo 错误：应用目录 %APP_DIR% 不存在！
    echo 请先运行部署脚本：setup.bat
    pause
    exit /b 1
)

echo ==================================================
echo 基于大模型的自然语言转SQL查询工具 - 启动脚本
echo ==================================================

REM 进入应用目录
cd "%APP_DIR%"

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 获取本机IP地址
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4 Address"') do (
    for /f "tokens=1 delims= " %%j in ("%%i") do (
        set IP=%%j
    )
)

REM 启动应用
echo 启动应用...
echo 本地访问地址: http://localhost:8505
echo 网络访问地址: http://%IP%:8505
echo 按 Ctrl+C 停止应用
echo ==================================================

streamlit run src/frontend/app.py --server.port 8505 --server.address 0.0.0.0

REM 退出虚拟环境
deactivate