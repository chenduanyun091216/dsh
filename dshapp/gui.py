#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
窗口与入口 (从原 dsh_app.py 拆分)
================================
ensure_pywebview + main: 单实例保护、创建 pywebview 无边框窗口、事件挂接、
任务栏图标、防白闪脚本注册、自绘标题栏注入。
"""

import base64
import os
import subprocess
import sys
import tempfile
import threading
import time

from .api import Api
from .assets import (INJECT_TITLEBAR_JS, NOFLASH_SCRIPT, NPROC, PAGE_HTML,
                     WHALE_ICO_B64)
from .utils import kill_tree, no_window

# ============================================================
# 入口
# ============================================================

def ensure_pywebview():
    """确保 pywebview 已安装(首次运行自动 pip 安装)。"""
    global webview
    try:
        import webview
    except ImportError:
        print("未检测到 pywebview, 正在自动安装 ...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--quiet",
                 "--disable-pip-version-check", "pywebview"],
                creationflags=no_window(),
            )
            import webview
        except Exception as e:
            print("pywebview 安装失败: %s" % e, file=sys.stderr)
            print("请手动执行: %s -m pip install pywebview" % sys.executable, file=sys.stderr)
            sys.exit(1)


def main():
    # 单实例保护: 防止重复启动生成多个窗口(首次安装耗时较长, 易被重复双击)。
    # 用命名互斥体; 已存在实例时, 把已有窗口调到前台并退出, 不再弹多余窗口。
    try:
        import ctypes
        MUTEX = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\dsh_single_instance")
        if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            user32 = ctypes.windll.user32
            hwnd = user32.FindWindowW(None, "dsh · Mr.chen")
            if not hwnd:
                hwnd = user32.FindWindowW(None, "dsh")
            if hwnd:
                user32.ShowWindow(hwnd, 9)        # SW_RESTORE (最小化则还原)
                user32.SetForegroundWindow(hwnd)  # 调到前台
            else:
                user32.MessageBoxW(None, "dsh 已在运行中, 请查看任务栏。", "dsh", 0x40)
            sys.exit(0)
    except Exception:
        pass

    ensure_pywebview()

    api = Api()
    window = webview.create_window(
        "dsh · Mr.chen",
        html=PAGE_HTML,
        js_api=api,
        width=1280,   # 内容区宽 1280
        height=842,   # 内容高 800(调高, 避免设置窗口被标题栏遮挡) + 自绘标题栏 42
        min_size=(1024, 618),
        frameless=True,   # 去掉系统标题栏, 使用界面内自绘标题栏
        easy_drag=False,  # 仅 .pywebview-drag-region(自绘标题栏)可拖动窗口
        text_select=True,  # 允许页面文字选择/复制(pywebview 默认禁止)
        background_color="#0b1220",
    )
    api._window = window

    def on_closing(*_args):
        api._closed = True
        kill_tree(NPROC[0])

    window.events.closing += on_closing
    # 兜底: 若 JS 桥启动回调未触发, Python 侧 loaded 事件同样会启动后台任务(一次性)
    window.events.loaded += lambda *_a: api.start_worker()
    # 每次页面加载后尝试注入自绘标题栏(仅对 Harness 页面生效, 幂等; 跟随 DSH 主题变色)
    window.events.loaded += lambda *_a: api.eval_js(INJECT_TITLEBAR_JS)
    # 每次页面加载后同步缩放(标题栏不缩放, 仅内容区)
    window.events.loaded += lambda *_a: api.eval_js("applyZoom(" + str(api._zoom) + ")")
    # 窗口显示后设置任务栏图标(黑色鲸鱼)
    # 注意: 不能用 .NET 的 System.Drawing.Icon 对象(与 WinForms 关闭时的释放顺序冲突,
    #       会导致关闭窗口时 .NET 未处理异常崩溃, 退出码 0xCFFFFFFF/1);
    #       改用 Win32 API 直接设置, 无对象生命周期问题。
    def _register_noflash():
        """在后台线程向 WebView2 注册文档创建脚本(消除跳转白闪)。
        必须在 UI 线程访问 CoreWebView2, 用 Invoke 封送; 注册本身不阻塞界面
        (不 Wait, fire-and-forget, 注册完成前 DSH 导航不会发生)。"""
        try:
            from System import Action
            form = api._window.native
            for _ in range(20):
                ok = [False]

                def _do():
                    try:
                        cwv2 = form.browser.webview.CoreWebView2
                        if cwv2 is None:
                            return
                        cwv2.AddScriptToExecuteOnDocumentCreatedAsync(NOFLASH_SCRIPT)
                        ok[0] = True
                    except Exception:
                        pass

                try:
                    form.Invoke(Action(_do))
                except Exception:
                    return
                if ok[0]:
                    return
                time.sleep(0.4)
        except Exception:
            pass

    def on_shown(*_a):
        try:
            import ctypes
            p = os.path.join(tempfile.gettempdir(), "dsh_installer_icon.ico")
            if not os.path.exists(p):
                with open(p, "wb") as f:
                    f.write(base64.b64decode(WHALE_ICO_B64))
            user32 = ctypes.windll.user32
            hwnd = int(api._window.native.Handle)
            # IMAGE_ICON=1, LR_LOADFROMFILE=0x10
            hicon = user32.LoadImageW(None, p, 1, 0, 0, 0x10)
            if hicon:
                WM_SETICON = 0x0080
                user32.SendMessageW(hwnd, WM_SETICON, 1, hicon)  # 小图标(任务栏)
                user32.SendMessageW(hwnd, WM_SETICON, 0, hicon)  # 大图标(Alt+Tab)
        except Exception:
            pass
        # 消除页面跳转白闪: 在 WebView2 文档创建瞬间注入深色背景脚本。
        # DSH 页面首个 HTML 无内联背景, 主题脚本异步加载后才变深色, 期间会白闪。
        # 注册放后台线程, 避免阻塞 UI 线程导致窗口卡死。
        threading.Thread(target=_register_noflash, daemon=True).start()
        # 应用持久化的缩放比例(类似浏览器缩放)
        api._apply_zoom(api._zoom)
    window.events.shown += on_shown

    try:
        webview.start()
    except Exception as e:
        print("启动界面失败: %s" % e, file=sys.stderr)
        print("提示: Windows 请确认已安装 WebView2 Runtime: "
              "https://developer.microsoft.com/microsoft-edge/webview2/", file=sys.stderr)
        sys.exit(1)

    kill_tree(NPROC[0])
