# DeepSeek Harness 安装器（Python 版）· 作者：Mr.Chen

一个 Python 桌面程序：打开后自动检查 Node.js（要求 **≥ v24.0.0**）→ 缺失或版本过低时在界面内询问用户是否安装/更新 → 选择「是」后自动执行安装指令 → 随后自动执行 `npx @deepseek-ai/dsh web` 下载并启动 DeepSeek Harness → 服务就绪后在**同一个窗口**内打开 Harness 页面（窗口封装）。

## 功能

1. **可视化界面**：打开程序即显示图形界面，并自动检查 Node.js 版本；
2. **询问机制**：未安装或版本 < v24.0.0 时，界面弹出询问框：
   - 选择「否，退出」→ 程序直接退出；
   - 选择「是」→ 自动执行安装/更新指令；
3. **自动安装/更新 Node.js**：
   - Windows：优先 `winget install OpenJS.NodeJS.LTS`，失败时自动回退为下载官方最新 v24.x MSI 并静默安装（`msiexec`）；
   - macOS：`brew install node`；Linux：`sudo apt-get install -y nodejs`；
4. **一键启动 Harness**：自动执行 `npx --yes @deepseek-ai/dsh web`（首次运行自动下载组件），并在同一窗口打开 `http://127.0.0.1:3080`；
5. **进度条 + 内嵌终端**：安装/启动全程显示进度条与实时命令输出（界面内嵌 Terminal 面板，与真实终端体验一致），界面标注作者 **Mr.Chen**；
6. **同一窗口**：安装界面与最终 Harness 页面为同一个窗口，全程无缝衔接。

## 使用方式

- **双击 `启动.bat`**，或
- 命令行运行：

```bash
python dsh_app.py
```

> 首次运行会自动通过 `pip` 安装依赖 `pywebview`（也可手动执行 `pip install -r requirements.txt`）。
> 需要 Python 3.8+。

## 界面说明

| 元素 | 说明 |
| ---- | ---- |
| 标题 / 作者 | DeepSeek Harness 安装器 · **Mr.Chen** |
| 状态行 | 当前阶段文字提示 |
| 进度条 | 阶段百分比进度；忙碌时（下载/安装中）自动进入流动动画 |
| Terminal 面板 | 内嵌终端，实时显示执行的命令与输出（含 npx 下载日志） |
| 询问框 | 是否安装/更新 Node.js、是否重试等交互 |

## 测试

```bash
python test_flow.py        # 无界面全流程测试(8 个场景: 版本检查/询问/安装/重试/退出等)
```

## 打包成 exe（Nuitka）

已验证可用的**最终打包命令**（在 `D:\dev\dsh` 目录下执行，产物为 `dist\dsh.dist\dsh.exe`，约 13 MB）：

```bat
".venv\Scripts\python.exe" -m nuitka --standalone --windows-console-mode=disable --output-filename=dsh.exe --windows-icon-from-ico=installer.ico --output-dir=dist --product-name="dsh" --company-name="Mr.Chen" --file-description="dsh - DeepSeek Harness 一键启动器 (Mr.Chen)" --file-version=1.0.0 --product-version=1.0.0 --copyright="Mr.Chen" --enable-plugin=pywebview --include-package-data=webview --include-package=pythonnet --include-package-data=pythonnet --include-module=clr --nofollow-import-to=tkinter,idlelib,test,unittest,pydoc,curses,lib2to3 --msvc=latest dsh_app.py
```

> `build_exe.bat` 内为同一命令的多行版，**双击即可打包**（需已安装 Nuitka：`pip install nuitka`）。
> 打包后 `build_exe.bat` 会把产物目录整理为 `dist\dsh.dist\dsh.exe`；若手动执行上述命令，产物在 `dist\dsh_app.dist\dsh.exe`。

### 前置补丁（重要！）

打包前需对 venv 里 Nuitka 的两个源文件打补丁。**重装 Nuitka 或重建虚拟环境后必须重新打**：

**① `venv\Lib\site-packages\nuitka\plugins\standard\PywebViewPlugin.py`**
Nuitka 的 pywebview 插件在 Windows 允许列表里漏了 `webview.platforms.win32`（pywebview ≥ 6 的 winforms 依赖它做屏幕缩放），不补会报：
`Module 'webview.platforms.win32' was actively excluded from Nuitka compilation`。在第 41-47 行的元组中加入：

```python
"webview.platforms.win32",  # pywebview>=6 winforms 依赖此模块(屏幕缩放)
```

**② `venv\Lib\site-packages\nuitka\build\inline_copy\clcache\clcache\caching.py`**
clcache 用系统 ANSI 代码页（mbcs）解码 cl.exe 的 UTF-8 输出，中文 Windows 上必然报 `UnicodeDecodeError: 'mbcs' codec can't decode`。把第 65 行改为：

```python
CL_DEFAULT_CODEC = "utf-8"   # 原为 "mbcs"
```

**③ `venv\Lib\site-packages\webview\util.py`**（pywebview 补丁）
`js_bridge_call` 的 `_call` 里最后投递 JS 回调的 `window.evaluate_js(...)` 没有异常保护——页面导航后旧文档回调失效，拖拽/缩放等高频调用在跳转瞬间会抛 `JavascriptException: ... is not a function`。把这段包上 try/except：

```python
try:
    window.evaluate_js(
        f'window.pywebview._returnValuesCallbacks["{func_name}"]["{value_id}"]({retval})'
    )
except Exception:
    pass  # dsh patch: 页面已导航, 回调丢失, 静默忽略
```

### 打包注意事项

- 使用 **`--msvc=latest`**（需要 Visual Studio Build Tools）；**不要覆盖 TEMP 环境变量**（会导致 `c1: fatal error C1083` 无法创建中间文件）；
- 分发时把整个 `.dist` 文件夹压缩成 zip（standalone 需要同目录的 DLL/资源），**不要只发单个 exe**；
- exe 图标自动使用黑色鲸鱼（`installer.ico`，由 DSH 官方 favicon.svg 生成）；
- 目标机器要求 Win10/11（自带 WebView2 Runtime）；Node.js 由程序自动安装；
- 分发前建议上传 VirusTotal 自查误报（无签名 exe 可能触发启发式引擎）。

## 常见问题

- **Windows 弹出 UAC 授权**：安装 Node.js 时属正常现象（需要管理员权限），点「是」即可；若静默安装失败，请右键「以管理员身份运行」本程序。
- **端口 3080 已被占用**：若 Harness 服务已在运行，程序会检测到并直接打开已有页面，不会重复启动。
- **国内网络下载慢**：可先配置 npm 镜像后重试，例如 `npm config set registry https://registry.npmmirror.com`。
- **界面无法打开**：Windows 需安装 WebView2 Runtime（Win10/11 一般自带）：https://developer.microsoft.com/microsoft-edge/webview2/
- **关闭程序即停止 DSH 服务**：关闭窗口时程序会自动结束由它启动的 `dsh web` 服务进程。

## 目录结构

```
dsh/
├── dsh_app.py                       # 入口（薄封装，实际代码在 dshapp/ 包内）
├── dshapp/                          # 功能模块包（由原单文件 dsh_app.py 重构拆分）
│   ├── __init__.py                  # 包说明 + 公共 API 再导出
│   ├── assets.py                    # 静态资源与常量（图标/界面HTML/注入JS）
│   ├── utils.py                     # 通用工具（进程/命令/服务探测/日志转发）
│   ├── node_install.py              # Node.js 安装（winget/MSI/brew/apt）
│   ├── launcher.py                  # DeepSeek Harness 启动（npx @deepseek-ai/dsh web）
│   ├── api.py                       # JS <-> Python 桥（pywebview js_api）
│   ├── flow.py                      # 安装/启动主流程 run_install
│   └── gui.py                       # 窗口创建与入口 main
├── dsh_app.original.py              # 重构前单文件备份（可删除）
├── 启动.bat                        # 双击启动脚本
├── build_exe.bat                   # Nuitka 打包脚本（多行版打包命令）
├── requirements.txt                # 依赖清单（pywebview）
├── test_flow.py                    # 无界面全流程回归测试
├── installer.ico                   # 黑色鲸鱼图标（exe 图标 / 任务栏图标）
├── dist/                           # 打包产物（Nuitka 输出）
├── .venv/                          # Python 虚拟环境（含打包所需的 nuitka 补丁）
└── README.md
```

## 作者

👨‍💻 **Mr.Chen**
