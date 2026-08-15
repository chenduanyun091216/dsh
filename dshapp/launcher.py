#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek Harness 启动 (从原 dsh_app.py 拆分)
===========================================
执行 `npx --yes @deepseek-ai/dsh web` 并等待服务就绪; 进程保持运行,
从输出中解析实际服务地址(可能非 3080)。
"""

import os
import queue
import re
import subprocess
import threading
import time

from .assets import DSH_ACTUAL_URL, DSH_URL, NPROC
from .utils import (drain, find_node, fmt_elapsed, kill_tree, no_window,
                    server_up, smart_decode, start_pulse)

# ============================================================
# 启动 DeepSeek Harness (npx @deepseek-ai/dsh web)
# ============================================================

def start_dsh(api):
    """执行 npx 下载并启动 dsh web 服务; 服务就绪返回 True(进程保持运行)。"""
    node_exe = find_node()
    node_dir = os.path.dirname(node_exe) if node_exe else ""
    env = os.environ.copy()
    if node_dir:
        env["PATH"] = node_dir + os.pathsep + env.get("PATH", "")

    if os.name == "nt":
        cmd = ["cmd", "/c", "npx", "--yes", "@deepseek-ai/dsh", "web"]
    else:
        cmd = ["npx", "--yes", "@deepseek-ai/dsh", "web"]
    api.ui_log("> " + " ".join(cmd), "cmd")

    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            bufsize=0, env=env, creationflags=no_window(),
        )
    except Exception as e:
        api.ui_log("无法启动 npx: " + str(e), "err")
        return False
    NPROC[0] = proc

    stop = start_pulse(api)
    q = queue.Queue()

    def reader():
        try:
            for raw in iter(proc.stdout.readline, b""):
                q.put(smart_decode(raw).rstrip("\r\n"))
        except Exception:
            pass

    threading.Thread(target=reader, daemon=True).start()
    deadline = time.time() + 600
    started = time.time()
    last_output = started
    found_url = None  # 从输出中解析到的服务地址(如 dsh 输出 http://127.0.0.1:xxxx)

    def check_ready():
        # 优先探测输出里声明的地址, 其次默认 3080
        if found_url and server_up(found_url):
            return found_url
        if server_up(DSH_URL):
            return DSH_URL
        return None

    try:
        while time.time() < deadline:
            if api._closed:
                kill_tree(proc)
                return False
            try:
                line = q.get(timeout=1.0)
            except queue.Empty:
                line = None
            if line:
                low = line.lower()
                cls = "err" if ("error" in low and "0 error" not in low) else ""
                api.ui_log(line, cls)
                last_output = time.time()
                # 解析输出里的 http 地址(形如 http://127.0.0.1:端口)
                m = re.search(r"https?://(?:127\.0\.0\.1|localhost):\d+", low)
                if m and found_url is None:
                    found_url = m.group(0)
            now = time.time()
            # 长时间无输出时的心跳提示(每 30s 一次), 附带已用时
            if now - last_output >= 30:
                used = fmt_elapsed(now - started)
                api.ui_log(f"⏳ 正在下载/启动 DeepSeek Harness(已用时 {used}), "
                           "首次运行需下载, 请耐心等待, 界面未卡死 ...", "dim")
                api.ui_status(f"正在下载/启动 DeepSeek Harness ... 已用时 {used}")
                last_output = now
            ready = check_ready()
            if ready:
                DSH_ACTUAL_URL[0] = ready
                api.ui_log(f"DeepSeek Harness 服务已就绪: {ready}", "ok")
                return True
            if proc.poll() is not None:
                drain(q, api)
                ready = check_ready()
                if ready:
                    DSH_ACTUAL_URL[0] = ready
                    api.ui_log(f"DeepSeek Harness 服务已就绪: {ready}", "ok")
                    return True
                api.ui_log("npx 进程已退出 (返回码 %s)。" % proc.returncode, "err")
                # 给出常见原因提示, 避免用户无从下手
                if proc.returncode == 0:
                    api.ui_log("进程无报错退出但服务未就绪, 常见原因: 首次下载超时/网络问题。", "dim")
                api.ui_log("若为网络问题, 可先设置 npm 镜像后重试: "
                           "npm config set registry https://registry.npmmirror.com", "dim")
                return False
    finally:
        stop.set()
    api.ui_log("等待 DeepSeek Harness 启动超时。", "err")
    return False
