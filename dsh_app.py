#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek Harness 安装器 / 启动器
================================
作者: Mr.Chen

功能:
  1. 启动可视化界面, 自动检查 Node.js (要求 >= 24.0.0)
  2. 未安装或版本过低 -> 在界面内询问用户是否安装/更新
     - 选择"否, 退出" -> 程序直接退出
     - 选择"是"       -> 自动打开终端面板并执行安装/更新指令
  3. 安装完成后, 自动执行 `npx @deepseek-ai/dsh web` 下载并启动 DeepSeek Harness
  4. 服务就绪后, 在同一个窗口内打开 DeepSeek Harness 页面 (窗口封装)
  5. 安装/启动全程显示进度条 + 实时终端输出, 界面标注作者 Mr.Chen

说明:
  - 代码已按功能拆分为 dshapp/ 包 (assets / utils / node_install / launcher /
    api / flow / gui), 本文件仅为入口, 模块清单见 dshapp/__init__.py。
  - 依赖 pywebview(首次运行会自动通过 pip 安装)。
  - Windows 10/11 自带 WebView2 Runtime, 无需额外安装。

运行方式:
  python dsh_app.py   (或双击 启动.bat)
"""

from dshapp.gui import main


if __name__ == "__main__":
    main()

