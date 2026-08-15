#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用工具函数 (从原 dsh_app.py 拆分)
==================================
子进程/命令执行、Node 定位、服务探测、进度脉冲、终端输出转发等。
api 参数为鸭子类型(提供 ui_log/ui_status/ui_progress/_closed)。
"""

import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request

from .assets import DSH_URL

# ============================================================
# 工具函数
# ============================================================

def no_window():
    """Windows 下隐藏子进程的黑窗口。"""
    if os.name == "nt":
        try:
            return subprocess.CREATE_NO_WINDOW
        except AttributeError:
            return 0
    return 0


def js_str(s):
    return json.dumps(str(s), ensure_ascii=False)


def fmt_elapsed(sec):
    """秒 -> mm:ss。"""
    sec = int(max(0, sec))
    m, s = divmod(sec, 60)
    return f"{m:02d}:{s:02d}"


def smart_decode(data: bytes) -> str:
    """兼容 winget 重定向输出为 UTF-16 的情况。"""
    if b"\x00" in data[:4096]:
        try:
            return data.decode("utf-16")
        except Exception:
            pass
    return data.decode("utf-8", errors="replace")


def parse_version(text):
    """从 'v24.3.1' 之类的文本中解析 (24, 3, 1)。"""
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", text or "")
    if not m:
        return None
    return tuple(int(g) for g in m.groups())


def run_capture(cmd, timeout=20):
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            creationflags=no_window(),
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return -1, str(e)


def find_node():
    """定位 node 可执行文件(考虑安装后 PATH 未刷新的情况)。"""
    exe = shutil.which("node")
    if exe:
        return exe
    if os.name == "nt":
        for d in (r"C:\Program Files\nodejs",
                  os.path.expandvars(r"%LOCALAPPDATA%\Programs\nodejs")):
            p = os.path.join(d, "node.exe")
            if os.path.exists(p):
                return p
    return None


def server_up(url=DSH_URL, timeout=2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status < 500
    except Exception:
        return False


def kill_tree(proc):
    """结束进程树(Windows 用 taskkill /T)。"""
    if proc is None:
        return
    try:
        if proc.poll() is not None:
            return
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/pid", str(proc.pid), "/T", "/F"],
                capture_output=True, creationflags=no_window(),
            )
        else:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
    except Exception:
        pass


def start_pulse(api):
    """进度条不定式动画(忙碌状态)。返回停止信号。"""
    stop = threading.Event()

    def loop():
        while not stop.wait(1.5):
            api.ui_progress(-1)

    threading.Thread(target=loop, daemon=True).start()
    return stop


def drain(q, api):
    try:
        while True:
            line = q.get(timeout=0.3)
            if line:
                api.ui_log(line)
    except queue.Empty:
        pass


def stream_cmd(cmd, api, timeout=1800, pulse=True, label=None):
    """执行命令并把输出实时写入界面终端; 返回是否成功(退出码为 0)。
    label 用于长耗时无输出阶段的"心跳"提示, 防止用户误以为卡死。"""
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            bufsize=0, creationflags=no_window(),
        )
    except Exception as e:
        api.ui_log("无法启动命令: " + str(e), "err")
        return False

    stop = start_pulse(api) if pulse else None
    q = queue.Queue()

    def reader():
        try:
            for raw in iter(proc.stdout.readline, b""):
                q.put(smart_decode(raw).rstrip("\r\n"))
        except Exception:
            pass

    threading.Thread(target=reader, daemon=True).start()
    deadline = time.time() + timeout
    started = time.time()
    last_output = started
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
                api.ui_log(line)
                last_output = time.time()
            now = time.time()
            # 长时间无输出时的心跳提示(每 30s 一次), 附带已用时
            if now - last_output >= 30:
                name = label or "命令"
                used = fmt_elapsed(now - started)
                api.ui_log(f"⏳ {name} 仍在进行中(已用时 {used}), 请耐心等待, 界面未卡死 ...", "dim")
                api.ui_status(f"{name} 进行中 ... 已用时 {used}")
                last_output = now
            rc = proc.poll()
            if rc is not None:
                drain(q, api)
                return rc == 0
    finally:
        if stop:
            stop.set()
    kill_tree(proc)
    api.ui_log("命令执行超时。", "err")
    return False


def open_folder(path):
    """跨平台打开文件夹(资源管理器 / Finder / xdg-open); 不存在则先创建。"""
    try:
        os.makedirs(path, exist_ok=True)
        if os.name == "nt":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception:
        return False
