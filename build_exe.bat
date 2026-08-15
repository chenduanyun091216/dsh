@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title dsh 打包脚本 (Mr.Chen)

rem ============================================================
rem  dsh - DeepSeek Harness 一键安装启动器 (Nuitka 打包脚本, 已验证可用)
rem  产物: dist\dsh.dist\dsh.exe
rem ============================================================

if not exist ".venv\Scripts\python.exe" (
    echo [错误] 未找到 .venv, 请先创建虚拟环境并安装依赖:
    echo        ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    pause
    exit /b 1
)

rem ---------- 1. 检查 C 编译器 (MSVC / VS Build Tools) ----------
set "VSW=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
if exist "%VSW%" (
    "%VSW%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath >nul 2>nul
    if errorlevel 1 (
        echo [警告] 未找到 Visual Studio Build Tools 的 C++ 工具集。
        echo        打包需要 MSVC。可选:
        echo        a. 安装 VS Build Tools, 勾选 C++ 生成工具
        echo           https://visualstudio.microsoft.com/zh-hans/downloads/
        echo        b. 或把命令中的 --msvc=latest 改成 --mingw64, 首次自动下载 MinGW
        echo.
        pause
    )
) else (
    echo [警告] 未找到 vswhere, 无法确认 MSVC。若打包报找不到编译器, 请安装 VS Build Tools。
    echo.
)

rem ---------- 2. 安装 Nuitka (不要用 --upgrade, 会覆盖下方补丁) ----------
".venv\Scripts\python.exe" -c "import nuitka" >nul 2>nul
if errorlevel 1 (
    echo [1/3] 正在安装 Nuitka ...
    ".venv\Scripts\python.exe" -m pip install nuitka
    if errorlevel 1 (
        echo [错误] Nuitka 安装失败, 请检查网络。
        pause
        exit /b 1
    )
) else (
    echo [1/3] Nuitka 已安装, 跳过。
)

rem ---------- 3. 检查 Nuitka 补丁 (重装/升级 Nuitka 后需重新打) ----------
set "PATCH1=.venv\Lib\site-packages\nuitka\plugins\standard\PywebViewPlugin.py"
set "PATCH2=.venv\Lib\site-packages\nuitka\build\inline_copy\clcache\clcache\caching.py"
set "PATCH3=.venv\Lib\site-packages\webview\util.py"
set "MISSING="

findstr /C:"webview.platforms.win32" "%PATCH1%" >nul 2>nul || set "MISSING=1"
findstr /C:"patched" "%PATCH2%" >nul 2>nul || set "MISSING=1"
findstr /C:"dsh patch" "%PATCH3%" >nul 2>nul || set "MISSING=1"

if defined MISSING (
    echo.
    echo [警告] 检测到 Nuitka 补丁缺失, 不打补丁将打包失败。请按 README 打包章节打补丁:
    echo.
    echo   %PATCH1%
    echo     在 Windows 允许列表元组中加入:  "webview.platforms.win32",
    echo.
    echo   %PATCH2%
    echo     把  CL_DEFAULT_CODEC = "mbcs"  改为  CL_DEFAULT_CODEC = "utf-8"
    echo.
    echo   %PATCH3%
    echo     把 js_bridge_call 里最后的 window.evaluate_js 调用包上 try/except(回调丢失静默忽略)
    echo.
    echo   提示: 若刚才 pip 升级过 Nuitka/pywebview, 补丁会被覆盖, 需要重新打。
    echo.
    pause
)

rem ---------- 4. 开始打包 ----------
echo.
echo [2/3] 开始打包, MSVC 编译约 10~30 分钟, 请耐心等待。
echo       注意: 请勿在其它终端覆盖 TEMP 环境变量。
echo.

set "EXTRA="
if exist installer.ico set "EXTRA=--windows-icon-from-ico=installer.ico"

".venv\Scripts\python.exe" -m nuitka ^
    --standalone ^
    --windows-console-mode=disable ^
    --output-filename=dsh.exe ^
    %EXTRA% ^
    --output-dir=dist ^
    --product-name="dsh" ^
    --company-name="Mr.Chen" ^
    --file-description="dsh - DeepSeek Harness 一键启动器 (Mr.Chen)" ^
    --file-version=1.0.0 ^
    --product-version=1.0.0 ^
    --copyright="Mr.Chen" ^
    --enable-plugin=pywebview ^
    --include-package-data=webview ^
    --include-package=pythonnet ^
    --include-package-data=pythonnet ^
    --include-module=clr ^
    --nofollow-import-to=tkinter,idlelib,test,unittest,pydoc,curses,lib2to3 ^
    --msvc=latest ^
    dsh_app.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败, 请查看上方日志。
    pause
    exit /b 1
)

rem ---------- 5. 整理产物目录 (dsh_app.dist -> dsh.dist) ----------
if exist "dist\dsh_app.dist" (
    if exist "dist\dsh.dist" rmdir /s /q "dist\dsh.dist"
    move "dist\dsh_app.dist" "dist\dsh.dist" >nul
)

rem ---------- 6. 完成 ----------
echo.
echo [3/3] 打包完成:
echo       dist\dsh.dist\dsh.exe
echo.
echo       分发: 将整个 .dist 文件夹压缩为 zip, 目标机器无需安装 Python。
echo       自查: 上传 VirusTotal 检查误报; 正式分发建议做代码签名。
echo       测试: 建议在无 Python/Node 的干净机器上完整跑一遍安装流程。
echo.
pause
endlocal
