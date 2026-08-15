#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Node.js 安装 (从原 dsh_app.py 拆分)
==================================
按平台安装/更新 Node.js: Windows(winget -> 官方 MSI 回退) / macOS(brew) / Linux(apt)。
"""

import os
import platform
import re
import shutil
import tempfile
import urllib.request

from .utils import stream_cmd

# ============================================================
# Node.js 安装
# ============================================================

def install_node(api):
    """按平台安装/更新 Node.js; 成功返回 True。"""
    system = platform.system()
    if system == "Windows":
        winget = shutil.which("winget")
        if winget:
            api.ui_log(
                "> winget install --id OpenJS.NodeJS.LTS --silent "
                "--accept-package-agreements --accept-source-agreements", "cmd")
            ok = stream_cmd(
                [winget, "install", "--id", "OpenJS.NodeJS.LTS", "--silent",
                 "--accept-package-agreements", "--accept-source-agreements"],
                api, timeout=1800, label="Node.js 安装 (winget)")
            if ok:
                return True
            api.ui_log("winget 安装未成功, 尝试官方 MSI 安装包 ...", "dim")
        return install_node_msi(api)

    if system == "Darwin":
        api.ui_log("> brew install node", "cmd")
        return stream_cmd(["brew", "install", "node"], api, timeout=3600,
                          label="Node.js 安装 (brew)")

    if system == "Linux":
        api.ui_log("> sudo apt-get install -y nodejs", "cmd")
        return stream_cmd(["sudo", "apt-get", "install", "-y", "nodejs"],
                          api, timeout=3600, label="Node.js 安装 (apt)")

    api.ui_log("不支持的操作系统: " + system, "err")
    return False


def install_node_msi(api):
    """回退方案: 下载官方最新 v24.x MSI 并静默安装。"""
    try:
        base = "https://nodejs.org/dist/latest-v24.x/"
        api.ui_log("> 获取 Node.js 最新 v24.x 安装包列表 ...", "cmd")
        idx = urllib.request.urlopen(base, timeout=30).read().decode("utf-8", "replace")
        m = re.search(r'href="([^"]*-x64\.msi)"', idx)
        if not m:
            api.ui_log("未在官方源中找到 x64 MSI 安装包。", "err")
            return False
        fname = m.group(1)
        url = base + fname
        dest = os.path.join(tempfile.gettempdir(), fname)
        api.ui_log(f"> 下载 {url} ...", "cmd")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            total = int(r.headers.get("Content-Length") or 0)
            done = 0
            while True:
                chunk = r.read(65536)
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                if total:
                    api.ui_progress(10 + 30 * done / total)
        api.ui_log(f"> msiexec /i {fname} /qn /norestart (静默安装)", "cmd")
        ok = stream_cmd(["msiexec", "/i", dest, "/qn", "/norestart"],
                        api, timeout=2400, label="Node.js 安装 (MSI)")
        if not ok:
            api.ui_log("MSI 静默安装失败。可能原因: 需要管理员权限。", "err")
        return ok
    except Exception as e:
        api.ui_log("MSI 安装异常: " + str(e), "err")
        return False
