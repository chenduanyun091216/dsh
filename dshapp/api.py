#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JS <-> Python 桥 (从原 dsh_app.py 拆分)
======================================
pywebview 的 js_api 对象: 内容缩放、窗口控制、DeepSeek 余额/今日用量统计、
主题切换、UI 转发(状态/进度/日志/询问)。

重要: 所有实例属性必须以 "_" 开头! pywebview 的 inject_pywebview() 会递归遍历
js_api 的公开属性并暴露给 JS, 若持有 window 等公开属性, 会从非 UI 线程访问 COM
控件导致 "CoreWebView2 can only be accessed from the UI thread" 刷屏/卡死。
"""

import json
import os
import sys
import tempfile
import threading
import urllib.request

from .assets import DSH_ACTUAL_URL, DSH_URL, DS_PRICE_DEFAULT, DS_PRICES, PAGE_HTML
from .flow import run_install
from .utils import js_str, open_folder

# ============================================================
# JS <-> Python 桥
# ============================================================

class Api:
    def __init__(self):
        # 重要: js_api 对象的所有属性必须以 "_" 开头!
        # pywebview 的 inject_pywebview() 会递归遍历 js_api 的公开属性并暴露给 JS,
        # 若持有 window 等公开属性, 会一路递归进入 WinForms/WebView2 COM 控件,
        # 从非 UI 线程访问 COM 属性导致 "CoreWebView2 can only be accessed from
        # the UI thread" 刷屏以及 AccessibilityObject 无限递归, 界面卡死。
        self._window = None
        self._closed = False
        self._lock = threading.Lock()
        self._started = False
        self._ev = threading.Event()
        self._ans = None
        self._worker = None
        self._zoom = self._load_zoom()
        self._usage_cache = None      # (日志指纹, 统计结果) 缓存, 避免每次刷新全量解压日志
        self._usage_lock = threading.Lock()
        # 终端输出批量合并: 高频输出时合并为每 ~50ms 一次桥调用, 降低 UI 线程压力
        self._log_lock = threading.Lock()
        self._log_buf = []
        self._log_timer = None
        self._pinned = None        # 置顶状态(懒初始化; js_api 桥回调在后台线程, 不走 pywebview 内部状态)

    # ---- 缩放(类似浏览器缩放, 基于 WebView2 ZoomFactor, 持久化) ----
    def _zoom_file(self):
        d = os.environ.get("APPDATA") or tempfile.gettempdir()
        d = os.path.join(d, "dsh")
        try:
            os.makedirs(d, exist_ok=True)
        except Exception:
            pass
        return os.path.join(d, "zoom.txt")

    def _load_zoom(self):
        try:
            with open(self._zoom_file(), encoding="utf-8") as f:
                z = float(f.read().strip())
            return round(min(2.0, max(0.5, z)), 2)
        except Exception:
            return 1.0

    def _save_zoom(self, z):
        try:
            with open(self._zoom_file(), "w", encoding="utf-8") as f:
                f.write(str(z))
        except Exception:
            pass

    def _apply_zoom(self, z):
        z = round(min(2.0, max(0.5, z)), 2)
        self._zoom = z
        self._save_zoom(z)
        # CSS zoom 只作用于页面内容, 标题栏不缩放(不用 WebView2 ZoomFactor, 它会连标题栏一起缩放)
        self.eval_js("applyZoom(" + str(z) + ")")

    def zoomBy(self, delta):
        """标题栏缩放按钮: delta 为 -0.1 / +0.1。"""
        try:
            self._apply_zoom(self._zoom + float(delta))
        except Exception:
            pass
        return True

    def zoomReset(self):
        self._apply_zoom(1.0)
        return True

    def getZoom(self):
        return self._zoom

    # ---- DeepSeek 账户信息(宠物面板) ----
    def _config(self):
        d = os.environ.get("APPDATA") or tempfile.gettempdir()
        try:
            with open(os.path.join(d, "dsh", "config.json"), encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_config(self, cfg):
        try:
            d = os.path.join(os.environ.get("APPDATA") or tempfile.gettempdir(), "dsh")
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "config.json"), "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _dsh_credentials_path(self):
        return os.path.join(os.path.expanduser("~"), ".dsh", ".credentials.yaml")

    def _read_dsh_key(self):
        """从 DSH 自身配置(~/.dsh/.credentials.yaml)读取 DEEPSEEK_API_KEY。"""
        try:
            with open(self._dsh_credentials_path(), encoding="utf-8") as f:
                for line in f:
                    if line.lstrip().startswith("DEEPSEEK_API_KEY"):
                        _, _, v = line.partition(":")
                        v = v.strip().strip('"').strip("'")
                        if v:
                            return v
        except Exception:
            pass
        return ""

    def getApiKey(self):
        return self._config().get("api_key") or self._read_dsh_key() or ""

    def saveApiKey(self, key):
        cfg = self._config()
        cfg["api_key"] = (key or "").strip()
        self._save_config(cfg)
        return True

    def getBalance(self):
        """查询 DeepSeek 官方余额接口; 优先用本地 Key, 否则自动用 DSH 配置的 Key。"""
        key = (self._config().get("api_key") or self._read_dsh_key() or "").strip()
        if not key:
            return {"ok": False, "error": "no_key"}
        try:
            req = urllib.request.Request(
                "https://api.deepseek.com/user/balance",
                headers={"Authorization": "Bearer " + key,
                         "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            return {"ok": True, "data": data}
        except Exception as e:
            code = getattr(e, "code", None)
            if code == 401:
                return {"ok": False, "error": "key_invalid"}
            if code == 402:
                return {"ok": False, "error": "insufficient"}
            return {"ok": False, "error": str(e)[:100]}

    def _usage_signature(self, root):
        """会话日志指纹: (路径, mtime_ns, 大小) 列表; 任一文件变化则指纹不同。"""
        sig = []
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                if not (name.endswith(".jsonl.zstd") or name.endswith(".jsonl")):
                    continue
                p = os.path.join(dirpath, name)
                try:
                    st = os.stat(p)
                    sig.append((p, st.st_mtime_ns, st.st_size))
                except Exception:
                    pass
        sig.sort()
        return sig

    def _scan_usage(self, root, today_start):
        """扫描会话日志, 统计 今日 的 token/cost/requests。

        usage 口径与官网一致: 输入(缓存未命中) + 缓存命中 + 输出
        (含 reasoningTokens 思考 token, 官方按输出价格计费)。
        消费为按官方价目的本地估算(≈)。

        性能优化:
          - mtime 预过滤: 会话日志按时间追加, 今天之前未修改过的文件不可能
            含今日事件, 直接跳过, 避免解压扫描全部历史日志(宠物面板刷新的
            主要开销);
          - 流式解压: zstd 用 decompressobj 增量解压并按行切分, 普通 jsonl
            逐行读取, 内存占用有界, 不再整文件读入。
        """
        import zstandard as _zstd
        agg = {"tokens": 0, "cost": 0.0, "requests": 0}

        def _consume(raw, state):
            """解析一行事件并累加(与官网计费口径一致)。"""
            try:
                ev = json.loads(raw)
            except Exception:
                return
            if not isinstance(ev, dict):
                return
            t = ev.get("type")
            if t == "request/context":
                m = ((ev.get("data") or {}).get("model") or "").strip()
                if m:
                    state["model"] = m
            elif t == "request/header":
                cfg = ((ev.get("data") or {}).get("header") or {}).get("config") or {}
                m = (cfg.get("model") or "").strip()
                if m:
                    state["model"] = m
            elif t == "assistant/message":
                ev_time = ev.get("time")
                if not isinstance(ev_time, (int, float)):
                    return
                usage = ((ev.get("data") or {}).get("usage") or {})
                if not isinstance(usage, dict):
                    return
                inp = usage.get("inputTokens") or 0
                out = usage.get("outputTokens") or 0
                cr = usage.get("cacheReadTokens") or 0
                cw = usage.get("cacheWriteTokens") or 0
                rt = usage.get("reasoningTokens") or 0
                if inp <= 0 and out <= 0 and cr <= 0 and cw <= 0 and rt <= 0:
                    return
                # 思考/推理 token(reasoningTokens)官方按输出价格计费,
                # 且不计入 outputTokens, 须并入输出后计费/计数。
                out += rt
                miss, hit, outp = DS_PRICES.get((state["model"] or "").lower(), DS_PRICE_DEFAULT)
                c = (inp * miss + (cr + cw) * hit + out * outp) / 1e6
                n = inp + out + cr + cw
                if ev_time >= today_start:
                    agg["tokens"] += n
                    agg["cost"] += c
                    agg["requests"] += 1

        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                if not (name.endswith(".jsonl.zstd") or name.endswith(".jsonl")):
                    continue
                path = os.path.join(dirpath, name)
                try:
                    st = os.stat(path)
                    # mtime 预过滤: 今天之前未修改过的文件直接跳过
                    if st.st_mtime * 1000 < today_start:
                        continue
                except Exception:
                    continue
                state = {"model": None}
                try:
                    if name.endswith(".zstd"):
                        # 重要: DSH 会话日志是"每写一次追加一个新 zstd 帧"(单文件可达
                        # 上万帧)。decompressobj 只能解第一帧(继续喂数据会抛
                        # "cannot use a decompressobj multiple times"), 必须用
                        # stream_reader + read_across_frames=True 跨帧读取;
                        # 分块 read(1 MiB)保持内存有界, 逐行切分。
                        reader = _zstd.ZstdDecompressor().stream_reader(
                            open(path, "rb"), read_across_frames=True)
                        try:
                            buf = b""
                            while True:
                                chunk = reader.read(1 << 20)
                                if not chunk:
                                    break
                                buf += chunk
                                while True:
                                    nl = buf.find(b"\n")
                                    if nl < 0:
                                        break
                                    raw = buf[:nl]
                                    buf = buf[nl + 1:]
                                    if raw.strip():
                                        _consume(raw.decode("utf-8", "replace"), state)
                            if buf.strip():
                                _consume(buf.decode("utf-8", "replace"), state)
                        finally:
                            reader.close()
                    else:
                        with open(path, "r", encoding="utf-8", errors="replace") as f:
                            for line in f:
                                if line.strip():
                                    _consume(line, state)
                except Exception:
                    continue
        return {"ok": True,
                "data": {"today": {"tokens": int(agg["tokens"]),
                                   "cost": round(agg["cost"], 4),
                                   "requests": int(agg["requests"])}},
                "estimated": True}

    def getUsage(self):
        """统计 DSH 会话日志中的今日用量与消费(消费按官方价目估算≈)。

        官方公开 API 不提供用量/账单(api.deepseek.com/user/usage 不存在),
        因此从本机 DSH 会话日志 (~/.dsh/sessions) 汇总今日数据:
        assistant/message 事件携带 usage(input/output/缓存/推理 tokens),
        模型取同会话最近的 request/context / request/header 记录。
        推理 token(reasoningTokens)按输出价格并入统计, 与官网计费口径一致。
        首次刷新需全量解压扫描一次(可能耗时数秒), 之后以文件
        mtime/大小 指纹 + 日期缓存结果, 仅当日志变化或跨天时才重新扫描。
        """
        import datetime as _dt
        try:
            import zstandard as _zstd  # noqa: F401
        except Exception:
            return {"ok": False, "error": "no_zstd"}
        root = os.path.join(os.path.expanduser("~"), ".dsh", "sessions")
        if not os.path.isdir(root):
            return {"ok": False, "error": "no_logs"}
        today_start = _dt.datetime.combine(_dt.date.today(), _dt.time.min).timestamp() * 1000
        day_key = _dt.date.today().isoformat()   # 缓存有效期到当天结束
        try:
            sig = self._usage_signature(root)
            with self._usage_lock:
                if (self._usage_cache and self._usage_cache[0] == sig
                        and self._usage_cache[2] == day_key):
                    return self._usage_cache[1]
                result = self._scan_usage(root, today_start)
                self._usage_cache = (sig, result, day_key)
                return result
        except Exception as e:
            return {"ok": False, "error": str(e)[:100]}

    # ---- 主题切换(直写 ~/.dsh/settings.yaml, 由 DSH 热重载应用) ----
    def _settings_path(self):
        return os.path.join(os.path.expanduser("~"), ".dsh", "settings.yaml")

    def setTheme(self, pref, force=False):
        """切换 DSH 主题偏好(light/dark/system)。

        直接改写 ~/.dsh/settings.yaml 的 ui-theme.preference: DSH 的
        settings-file 提供者(chokidar)监听到外部编辑后热重载文档并广播
        settings/document-updated, 客户端 ThemeRuntime.adopt() 随即发布
        theme/change, 界面实时应用新主题 —— 不再依赖模拟点击设置面板,
        不受 DSH 界面结构/类名变化影响。文件其余内容与注释原样保留。

        force=True 时即使文件已是目标值也重写一次(文件监听偶尔漏事件的
        自愈手段: 重写会再次触发 chokidar, 让 DSH 重新应用)。
        """
        if pref not in ("light", "dark", "system"):
            return {"ok": False, "error": "bad_pref"}
        path = self._settings_path()
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            lines = []
        except Exception as e:
            return {"ok": False, "error": str(e)[:100]}
        out = []
        in_theme = False
        pref_idx = None       # ui-theme 段内已有的 preference 行位置
        theme_idx = None      # ui-theme: 顶层键行位置
        last_child = None     # ui-theme 段最后一个子键行位置
        modified = False
        for content in lines:
            if not content.strip():
                out.append(content)
                continue
            indent = len(content) - len(content.lstrip())
            if indent == 0:
                in_theme = content.rstrip().endswith(":") and content.strip().startswith("ui-theme:")
                if in_theme:
                    theme_idx = len(out)
            elif in_theme:
                if content.strip().startswith("preference:"):
                    pref_idx = len(out)
                    key = content.partition(":")[0]
                    val = content.partition(":")[2].strip().strip('"').strip("'")
                    if val != pref:
                        out.append(key + ": " + pref)
                        modified = True
                    else:
                        out.append(content)
                    continue
                last_child = len(out)
            out.append(content)
        if pref_idx is not None and not modified and not force:
            return {"ok": True, "preference": pref}   # 已是目标值, 无需写盘
        if pref_idx is None:
            if theme_idx is not None:
                insert_at = (last_child + 1) if last_child is not None else (theme_idx + 1)
                out.insert(insert_at, "  preference: " + pref)
            else:
                if out and out[-1].strip() != "":
                    out.append("")
                out.append("ui-theme:")
                out.append("  preference: " + pref)
            modified = True
        if not modified and not force:
            return {"ok": True, "preference": pref}
        try:
            new_text = "\n".join(out) + "\n"
            try:
                tmp = path + ".tmp"
                with open(tmp, "w", encoding="utf-8", newline="") as f:
                    f.write(new_text)
                os.replace(tmp, path)
            except OSError:
                # 兜底: tmp+rename 被占用/拦截(如杀软)时直接写原文件,
                # DSH 的文件监听同样能感知变更。
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_text)
        except Exception as e:
            return {"ok": False, "error": str(e)[:100]}
        return {"ok": True, "preference": pref}

    def getTheme(self):
        """读取当前 DSH 主题偏好(light/dark/system)。

        来源为 ~/.dsh/settings.yaml(唯一事实来源), 供标题栏主题按钮判定
        当前主题 —— 不再依赖 CSS 样式计算(colorScheme 在部分 WebView2
        版本返回 "light dark" 等值, 样式检测可能误判导致切换成无操作)。
        """
        try:
            path = self._settings_path()
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if line.lstrip().startswith("preference:"):
                        v = line.partition(":")[2].strip().strip('"').strip("'")
                        if v in ("light", "dark", "system"):
                            return {"ok": True, "theme": v}
            return {"ok": False, "error": "no_preference"}
        except Exception as e:
            return {"ok": False, "error": str(e)[:100]}

    def openDeepSeekSite(self):
        """一键跳转 DeepSeek 官网(默认浏览器)。"""
        url = "https://platform.deepseek.com"
        try:
            os.startfile(url)
        except Exception:
            try:
                import webbrowser
                webbrowser.open(url)
            except Exception:
                return False
        return True

    # ---- JS 调用 Python ----
    def onLoad(self):
        self.start_worker()
        return True

    def start_worker(self):
        """启动后台安装线程(一次性; JS 桥与 Python loaded 事件均可触发)。"""
        with self._lock:
            if self._started:
                return
            self._started = True
            if self._worker is not None and self._worker.is_alive():
                return
            self._worker = threading.Thread(target=run_install, args=(self,), daemon=True)
            self._worker.start()

    def answer(self, yes):
        self._ans = bool(yes)
        self._ev.set()
        return True

    def closeWindow(self):
        self._closed = True
        try:
            if self._window:
                self._window.destroy()
        except Exception:
            pass
        return True

    def windowControl(self, action):
        """自绘标题栏按钮: min / max / restore / close。"""
        if self._window is None:
            return True
        try:
            if action == "min":
                self._window.minimize()
            elif action == "max":
                self._window.maximize()
            elif action == "restore":
                self._window.restore()
            elif action == "close":
                self.closeWindow()
        except Exception as e:
            print("[win]", e, file=sys.stderr)
        return True

    def resizeWindow(self, w, h, edge):
        """无边框窗口拖拽缩放: w/h 为逻辑像素, edge 为 n/s/e/w/ne/nw/se/sw。"""
        if self._window is None:
            return True
        try:
            from webview.window import FixPoint
            _fix = {
                "e":  FixPoint.NORTH | FixPoint.WEST,
                "w":  FixPoint.NORTH | FixPoint.EAST,
                "s":  FixPoint.NORTH | FixPoint.WEST,
                "n":  FixPoint.SOUTH | FixPoint.WEST,
                "se": FixPoint.NORTH | FixPoint.WEST,
                "sw": FixPoint.NORTH | FixPoint.EAST,
                "ne": FixPoint.SOUTH | FixPoint.WEST,
                "nw": FixPoint.SOUTH | FixPoint.EAST,
            }
            fp = _fix.get(edge, FixPoint.NORTH | FixPoint.WEST)
            self._window.resize(max(int(w), 640), max(int(h), 360), fp)
        except Exception as e:
            print("[win]", e, file=sys.stderr)
        return True

    def moveWindowTo(self, x, y):
        """自绘拖拽(兜底): 把窗口移动到 (x, y)(逻辑像素)。修复缩放后 pywebview 内置拖拽错位。"""
        if self._window is None:
            return True
        try:
            self._window.move(int(x), int(y))
        except Exception as e:
            print("[win]", e, file=sys.stderr)
        return True

    # ---- 原生窗口拖拽/缩放(推荐路径) ----
    # 旧实现每帧走一次 JS→Python 桥调用(mousemove→rAF→pywebview 桥→SetWindowPos),
    # 桥延迟 + 跨线程往返使窗口跟不上光标, 产生"不顺滑/顿挫"感。
    # 这里改为一次性把 WM_NCLBUTTONDOWN + 命中码发给顶层窗体, 由操作系统接管
    # 整个移动/缩放模态循环: 拖动期间零桥调用, 光标与窗口完全同步, 顺滑度与
    # 系统标题栏一致; 缩放时最小尺寸由 WinForms MinimumSize(WM_GETMINMAXINFO)自动生效。
    # 物理像素坐标由系统处理, 不再受 devicePixelRatio/缩放影响, 也不会错位。
    WM_NCLBUTTONDOWN = 0x00A1
    HT_CAPTION = 2
    HT_LEFT, HT_RIGHT, HT_TOP = 10, 11, 12
    HT_TOPLEFT, HT_TOPRIGHT = 13, 14
    HT_BOTTOM, HT_BOTTOMLEFT, HT_BOTTOMRIGHT = 15, 16, 17
    HT_MAP = {
        "n": HT_TOP, "s": HT_BOTTOM, "e": HT_RIGHT, "w": HT_LEFT,
        "ne": HT_TOPRIGHT, "nw": HT_TOPLEFT,
        "se": HT_BOTTOMRIGHT, "sw": HT_BOTTOMLEFT,
    }

    def _native_hwnd(self):
        """顶层窗体 HWND(用于 Win32 消息)。"""
        if self._window is None:
            return None
        try:
            return int(self._window.native.Handle)
        except Exception:
            return None

    def _native_drag(self, ht_code):
        """启动一次系统原生窗口移动/缩放循环(WM_NCLBUTTONDOWN + 命中码)。

        必须在 UI 线程上发送该消息: 系统根据目标线程的输入状态(GetKeyState)决定
        是否进入模态移动循环, 而 pywebview 的 JS 桥在后台线程执行 Python 方法,
        直接 SendMessage 时状态读不到"左键按下", 循环不启动 → 窗口拖不动。
        因此用 form.Invoke 封送到 UI 线程执行; 模态循环期间 UI 线程在内部泵消息,
        直到松开鼠标按键才返回(桥调用线程同步阻塞, 属预期)。
        """
        hwnd = self._native_hwnd()
        if not hwnd:
            return True
        try:
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32

            def _do():
                try:
                    user32.ReleaseCapture()
                    pt = wintypes.POINT()
                    user32.GetCursorPos(ctypes.byref(pt))
                    lparam = (pt.y << 16) | (pt.x & 0xFFFF)
                    user32.SendMessageW(hwnd, self.WM_NCLBUTTONDOWN, ht_code, lparam)
                except Exception as e2:
                    print("[win]", e2, file=sys.stderr)

            form = self._window.native
            if getattr(form, "InvokeRequired", False):
                from System import Action
                form.Invoke(Action(_do))
            else:
                _do()
        except Exception as e:
            print("[win]", e, file=sys.stderr)
        return True

    def startNativeDrag(self):
        """自绘标题栏拖拽(推荐): HTCAPTION, 系统原生移动循环。
        窗口最大化时按住拖动会自动还原并继续移动(与系统标题栏行为一致)。"""
        return self._native_drag(self.HT_CAPTION)

    def startNativeResize(self, edge):
        """无边框边缘缩放(推荐): n/s/e/w/ne/nw/se/sw → 对应 HT 命中码。"""
        ht = self.HT_MAP.get(edge)
        if ht is None:
            return True
        return self._native_drag(ht)

    # ---- Python 调用 JS ----
    def eval_js(self, code):
        if self._window is None or self._closed:
            return
        try:
            self._window.evaluate_js(code)
        except Exception as e:
            print("[ui]", e, file=sys.stderr)

    def ui_status(self, text):
        self.eval_js("setStatus(" + js_str(text) + ")")

    def ui_stage(self, text):
        self.eval_js("setStage(" + js_str(text) + ")")
        # 动态任务栏标题: 最小化/Alt-Tab 也能看到当前阶段
        self._set_window_title("dsh · " + text)

    def _set_window_title(self, title):
        if self._window is None or self._closed:
            return
        try:
            self._window.title = title
        except Exception:
            pass

    def ui_progress(self, v):
        self.eval_js("setProgress(" + str(v) + ")")

    def ui_log(self, text, cls=""):
        # 性能: 终端输出可能高频(如 npx 下载进度), 逐行桥调用会压垮 UI 线程。
        # 先入缓冲区, 由 50ms 定时器合并为一次 appendLogs 调用(顺序保持)。
        with self._log_lock:
            self._log_buf.append({"text": text, "cls": cls})
            if self._log_timer is None:
                self._log_timer = threading.Timer(0.05, self._flush_logs)
                self._log_timer.daemon = True
                self._log_timer.start()

    def _flush_logs(self):
        with self._log_lock:
            batch = self._log_buf
            self._log_buf = []
            self._log_timer = None
        if batch:
            self.eval_js("appendLogs(" + json.dumps(batch, ensure_ascii=False) + ")")

    def flush_logs_now(self):
        """立即冲刷日志缓冲(用于退出/跳页前, 避免丢行)。"""
        with self._log_lock:
            batch = self._log_buf
            self._log_buf = []
            if self._log_timer is not None:
                self._log_timer.cancel()
                self._log_timer = None
        if batch:
            self.eval_js("appendLogs(" + json.dumps(batch, ensure_ascii=False) + ")")

    def ask(self, text, timeout=3600):
        """弹出 是/否 询问框, 阻塞等待用户选择; 返回 bool。"""
        self._ev.clear()
        self._ans = None
        self.eval_js("showQuestion(" + js_str(text) + ")")
        waited = 0.0
        while not self._ev.wait(0.2):
            waited += 0.2
            if self._closed:
                return False
            if waited > timeout:
                return False
        return bool(self._ans)

    def exit_soon(self, delay=1.2):
        threading.Timer(delay, self.closeWindow).start()

    # ---- 标题栏增强(置顶 / 数据目录 / 返回安装器) ----
    def toggleOnTop(self):
        """切换窗口置顶; 返回 {ok, on_top}。

        注意: pywebview 的 js_api 回调在【后台线程】执行(util.js_bridge_call 明确
        注释 "executed in a separate thread"), 而 winforms 的 set_on_top 直接写
        控件 TopMost 未做封送 —— 从后台线程访问 WinForms 控件会触发 .NET 跨线程
        未处理异常, 进程以 0xCFFFFFFF 崩溃。
        因此 Windows 上通过 form.Invoke 封送到 UI 线程执行; 其它平台回退到
        pywebview 的 on_top 属性。置顶状态由本对象自行维护(_pinned)。
        """
        if self._window is None:
            return {"ok": False, "error": "no_window"}
        try:
            if self._pinned is None:
                try:
                    self._pinned = bool(getattr(self._window, "on_top", False))
                except Exception:
                    self._pinned = False
            new = not self._pinned
            form = None
            if os.name == "nt":
                try:
                    form = self._window.native
                except Exception:
                    form = None
            if form is not None:
                from System import Action
                ok = [False]

                def _apply():
                    try:
                        form.TopMost = new
                        ok[0] = True
                    except Exception:
                        pass

                try:
                    form.Invoke(Action(_apply))
                except Exception:
                    pass
                if not ok[0]:
                    return {"ok": False, "error": "set_on_top failed"}
            else:
                # 非 Windows 或无 native(如测试桩): 直接走 pywebview 属性
                self._window.on_top = new
            self._pinned = new
            return {"ok": True, "on_top": new}
        except Exception as e:
            return {"ok": False, "error": str(e)[:100]}

    def openDataDir(self):
        """打开 DSH 数据目录(~/.dsh)。"""
        return open_folder(os.path.expanduser("~/.dsh"))

    def openUrl(self, url):
        """在默认浏览器中打开指定地址(标题栏服务地址点击)。"""
        url = (url or "").strip()
        if not url:
            return False
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        try:
            if os.name == "nt":
                os.startfile(url)
            else:
                import webbrowser
                webbrowser.open(url)
            return True
        except Exception:
            try:
                import webbrowser
                webbrowser.open(url)
                return True
            except Exception:
                return False

    def backToInstaller(self):
        """从 Harness 页面返回安装器首页, 并自动重新检查环境。

        页面加载完成后自动执行 run_install(与首次安装同一流程): Node.js 缺失
        会询问并安装、服务未运行会尝试启动; 一切正常后自动 load_url 回到工作页面。
        """
        if self._window is None or self._closed:
            return False
        try:
            self._window.load_html(PAGE_HTML)
        except Exception:
            return False

        t = threading.Timer(1.0, self._recheck_and_return)  # 等页面加载 + JS 桥就绪
        t.daemon = True
        t.start()
        return True

    def _recheck_and_return(self):
        """返回安装器后的自动重检: 走 run_install, 正常则自动回到工作页面。"""
        try:
            run_install(self)
        except Exception:
            pass
