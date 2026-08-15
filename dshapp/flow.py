#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装/启动主流程 (从原 dsh_app.py 拆分)
====================================
run_install: 检查 Node.js -> 安装/更新 -> 启动 DSH -> 同一窗口打开页面。

注意: 函数一律通过模块引用调用 (utils.find_node / node_install.install_node /
launcher.start_dsh ...), 以便 test_flow.py 按模块 monkeypatch。
"""

import time

from . import launcher
from . import node_install
from . import utils
from .assets import DSH_ACTUAL_URL, DSH_URL, NODE_MIN

# ============================================================
# 主流程
# ============================================================

def run_install(api):
    """后台安装线程: 检查 Node.js -> 安装/更新 -> 启动 DSH -> 打开页面。"""
    try:
        api.ui_log("DeepSeek Harness 安装器 v1.0   (作者: Mr.Chen)", "dim")
        api.ui_log("> 正在检查运行环境 ...", "cmd")
        api.ui_stage("检查环境")
        api.ui_status("正在检查 Node.js ...")
        api.ui_progress(3)

        node_exe = utils.find_node()
        ver = None
        if node_exe:
            _code, out = utils.run_capture([node_exe, "--version"])
            ver = utils.parse_version(out)

        if ver and ver >= NODE_MIN:
            vstr = ".".join(map(str, ver))
            api.ui_log(f"Node.js 检查通过: v{vstr}  (要求 >= 24.0.0)", "ok")
            api.ui_status(f"Node.js 检查通过 (v{vstr})")
            api.ui_progress(20)
        else:
            if ver:
                vstr = ".".join(map(str, ver))
                msg = f"检测到 Node.js v{vstr}, 但需要 >= 24.0.0"
            else:
                msg = "未检测到 Node.js"
            api.ui_log(msg, "err")
            api.ui_status("需要安装/更新 Node.js")
            api.ui_progress(5)
            if not api.ask(msg + "\n是否现在安装/更新 Node.js 24+?"):
                api.ui_log("用户选择不安装, 程序退出。", "dim")
                api.ui_status("已取消, 即将退出 ...")
                api.exit_soon()
                return
            api.ui_stage("安装 / 更新 Node.js")
            api.ui_status("正在安装/更新 Node.js, 可能需要几分钟, 请勿关闭窗口 ...")
            api.ui_log("首次安装 Node.js 可能需要几分钟, 期间进度条/终端仍在活动即属正常。", "dim")
            api.ui_progress(10)
            ok = node_install.install_node(api)
            if not ok:
                api.ui_log("安装失败, 询问是否重试 ...", "err")
                if api.ask("Node.js 安装/更新失败。\n是否重试?\n"
                           "(若多次失败, 建议右键以管理员身份运行本程序)"):
                    ok = node_install.install_node(api)
            if not ok:
                api.ui_log("Node.js 安装失败, 程序退出。", "err")
                api.ui_status("安装失败, 即将退出 ...")
                api.exit_soon()
                return
            api.ui_progress(45)
            node_exe = utils.find_node()
            _code, out = utils.run_capture([node_exe, "--version"]) if node_exe else (-1, "")
            ver = utils.parse_version(out)
            if ver:
                vstr = ".".join(map(str, ver))
                api.ui_log(f"Node.js 就绪: v{vstr}", "ok")
                api.ui_status(f"Node.js 就绪 (v{vstr})")
            else:
                api.ui_log("Node.js 已安装, 但版本验证失败, 继续尝试启动 ...", "err")

        # ---- 下载并启动 DeepSeek Harness ----
        api.ui_stage("下载并启动 DeepSeek Harness")
        api.ui_progress(50)
        if utils.server_up(DSH_URL):
            api.ui_log(f"检测到 DeepSeek Harness 服务已在运行: {DSH_URL}", "ok")
            # 渐进式进度动画(约2.5s): 即使一切就绪, 也让进度条分段走完再进入页面
            for _p, _s in ((60, "正在连接服务 ..."),
                           (72, "正在载入工作区 ..."),
                           (85, "正在准备界面 ..."),
                           (94, "即将打开界面 ...")):
                api.ui_progress(_p)
                api.ui_status(_s)
                time.sleep(0.6)
        else:
            api.ui_status("正在下载并启动 DeepSeek Harness, 首次运行需下载, 视网络可能需要几分钟, 请耐心等待 ...")
            api.ui_log("首次运行需下载 DeepSeek Harness, 下载完成后会自动启动; 等待期间请勿关闭窗口。", "dim")
            api.ui_log("> npx --yes @deepseek-ai/dsh web", "cmd")
            ok = launcher.start_dsh(api)
            if not ok:
                api.ui_log("启动失败, 询问是否重试 ...", "err")
                if api.ask("DeepSeek Harness 下载/启动失败。\n是否重试?"):
                    ok = launcher.start_dsh(api)
            if not ok:
                api.ui_log("DeepSeek Harness 启动失败, 程序退出。请检查网络后重试。", "err")
                api.ui_status("启动失败, 即将退出 ...")
                api.exit_soon()
                return

        # ---- 同一窗口打开 Harness 页面(load_url 跳转, 加载后自动注入跟随主题的自绘标题栏) ----
        api.ui_progress(100)
        api.ui_stage("完成")
        api.ui_log("DeepSeek Harness 已启动, 正在打开界面 ...", "ok")
        api.ui_status("正在打开 DeepSeek Harness 界面 ...")
        try:
            api._window.title = "dsh · " + DSH_ACTUAL_URL[0].replace("http://", "").replace("https://", "")
        except Exception:
            pass
        time.sleep(0.6)
        api._window.load_url(DSH_ACTUAL_URL[0])

    except Exception as exc:
        import traceback
        traceback.print_exc()
        try:
            api.ui_log("发生错误: " + str(exc), "err")
            api.ui_status("发生错误, 即将退出 ...")
            api.exit_soon()
        except Exception:
            pass
