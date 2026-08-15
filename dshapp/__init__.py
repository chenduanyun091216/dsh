"""
DeepSeek Harness 安装器 / 启动器 (包)
=====================================
由单文件 dsh_app.py 重构拆分而来, 按功能划分模块:

  assets        静态资源与配置常量 (图标 / 界面 HTML / 注入 JS)
  utils         通用工具函数 (进程 / 命令 / 服务探测)
  node_install  Node.js 安装 (winget / MSI / brew / apt)
  launcher      DeepSeek Harness 启动 (npx @deepseek-ai/dsh web)
  api           JS <-> Python 桥 (pywebview js_api)
  flow          安装/启动主流程 run_install
  gui           窗口与入口 main

入口仍为 dsh_app.py:  python dsh_app.py   (或双击 启动.bat)
"""

from .assets import (APP_NAME, AUTHOR, DSH_ACTUAL_URL, DSH_URL, DS_PRICE_DEFAULT,
                     DS_PRICES, INJECT_TITLEBAR_JS, NODE_MIN, NOFLASH_SCRIPT,
                     NPROC, PAGE_HTML, WHALE_ICO_B64, WHALE_SVG_URI)
from .utils import (drain, find_node, fmt_elapsed, js_str, kill_tree, no_window,
                    parse_version, run_capture, server_up, smart_decode,
                    start_pulse, stream_cmd)
from .node_install import install_node, install_node_msi
from .launcher import start_dsh
from .api import Api
from .flow import run_install
from .gui import ensure_pywebview, main

__version__ = "1.0.0"
__author__ = "Mr.Chen"

