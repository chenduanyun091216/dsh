@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title DeepSeek Harness 安装器 (Mr.Chen)

rem 优先使用项目虚拟环境, 其次 PATH 中的 python / py
set "PY="
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    where py >nul 2>nul && set "PY=py -3"
)
if not defined PY (
    echo [错误] 未检测到 Python, 请先安装 Python 3.8+ : https://www.python.org/downloads/
    echo        安装时请勾选 "Add Python to PATH"。
    pause
    exit /b 1
)

%PY% dsh_app.py
if %errorlevel% neq 0 (
    echo.
    echo [提示] 程序异常退出, 请查看上方错误信息。
    pause
)
endlocal
