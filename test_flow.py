# -*- coding: utf-8 -*-
"""
无界面全流程测试: 用 MockApi 驱动 dshapp.flow.run_install,
覆盖主要分支并断言结果。运行: python test_flow.py

说明: dsh_app.py 已重构拆分为 dshapp/ 包, monkeypatch 目标为
dshapp.utils / dshapp.node_install / dshapp.launcher 的模块级函数
(flow.run_install 一律通过模块引用调用这些函数)。
"""
import sys

import dshapp as m
from dshapp import launcher, node_install, utils


class MockWindow:
    def __init__(self):
        self.title = None
        self.urls = []

    def load_url(self, url):
        self.urls.append(url)


class MockApi:
    """模拟真实 Api(不触碰任何 GUI), 记录所有 UI 调用。"""

    def __init__(self, answers=None):
        self._window = MockWindow()
        self._closed = False
        self.calls = []
        self.ask_calls = []
        self._answers = list(answers or [])

    def ui_status(self, t):
        self.calls.append(("status", t))

    def ui_stage(self, t):
        self.calls.append(("stage", t))

    def ui_progress(self, v):
        self.calls.append(("progress", v))

    def ui_log(self, t, cls=""):
        self.calls.append(("log", t, cls))

    def eval_js(self, code):
        self.calls.append(("eval_js", code))

    def ask(self, text, timeout=3600):
        self.ask_calls.append(text)
        return self._answers.pop(0) if self._answers else False

    def exit_soon(self, delay=1.2):
        self.calls.append(("exit", None))
        self._closed = True

    # 供 start_dsh 等读取
    @property
    def closed(self):
        return self._closed


# 测试会 monkeypatch 的模块级函数(与 flow.run_install 的调用点一一对应)
_PATCHED = (utils.find_node, utils.run_capture, node_install.install_node,
            utils.server_up, launcher.start_dsh)


def scenario(name, api, setup=None):
    """运行一个场景, 返回 (加载的URL, ask次数, 是否退出, 最后状态)。"""
    orig = _PATCHED
    try:
        if setup:
            setup()
        m.run_install(api)
        loaded = list(api._window.urls)
        asks = len(api.ask_calls)
        exited = any(c[0] == "exit" for c in api.calls)
        statuses = [c[1] for c in api.calls if c[0] == "status"]
        return name, loaded, asks, exited, (statuses[-1] if statuses else None)
    finally:
        utils.find_node, utils.run_capture, node_install.install_node, \
            utils.server_up, launcher.start_dsh = orig


REAL_NODE = utils.find_node()
failures = []


def check(name, result, exp_loaded, exp_asks, exp_exited):
    _name, loaded, asks, exited, last_status = result
    ok = (loaded == exp_loaded and asks == exp_asks and exited == exp_exited)
    tag = "PASS" if ok else "FAIL"
    if not ok:
        failures.append(name)
    print(f"[{tag}] {name}")
    print(f"      loaded={loaded}  asks={asks}  exited={exited}  last_status={last_status!r}")
    return ok


# A: Node 已装(本机 v24) + 服务已在运行 -> 直接打开页面, 不询问
r = scenario("A-node-ok-server-up", MockApi())
check("A-node-ok-server-up", r, [m.DSH_URL], 0, False)

# B: Node 缺失 + 用户选择退出 -> 程序退出, 不打开页面
def setup_b():
    utils.find_node = lambda: None
r = scenario("B-node-missing-decline", MockApi(answers=[False]), setup_b)
check("B-node-missing-decline", r, [], 1, True)

# C: Node 缺失 + 用户同意安装 + 安装成功 -> 打开页面
def setup_c():
    seq = iter([None, REAL_NODE])
    utils.find_node = lambda: next(seq)
    node_install.install_node = lambda api: True
r = scenario("C-node-missing-accept", MockApi(answers=[True]), setup_c)
check("C-node-missing-accept", r, [m.DSH_URL], 1, False)

# D: Node 版本过低(v22) + 同意更新 + 更新成功(v24) -> 打开页面
def setup_d():
    seq = iter([(0, "v22.1.0\n"), (0, "v24.3.0\n")])
    utils.run_capture = lambda cmd, timeout=20: next(seq)
    node_install.install_node = lambda api: True
r = scenario("D-node-old-accept", MockApi(answers=[True]), setup_d)
check("D-node-old-accept", r, [m.DSH_URL], 1, False)

# E: Node 缺失 + 安装失败 + 重试也失败 -> 退出
def setup_e():
    utils.find_node = lambda: None
    node_install.install_node = lambda api: False
r = scenario("E-install-fail-exit", MockApi(answers=[True, False]), setup_e)
check("E-install-fail-exit", r, [], 2, True)

# F: DSH 首次启动失败 + 重试成功 -> 打开页面
def setup_f():
    utils.run_capture = lambda cmd, timeout=20: (0, "v24.1.0\n")
    utils.server_up = lambda *a, **k: False
    seq = iter([False, True])
    launcher.start_dsh = lambda api: next(seq)
r = scenario("F-dsh-fail-retry-ok", MockApi(answers=[True]), setup_f)
check("F-dsh-fail-retry-ok", r, [m.DSH_URL], 1, False)

# G: DSH 启动失败 + 重试也失败 -> 退出(首次启动自动进行, 仅失败后询问 1 次重试)
def setup_g():
    utils.run_capture = lambda cmd, timeout=20: (0, "v24.1.0\n")
    utils.server_up = lambda *a, **k: False
    launcher.start_dsh = lambda api: False
r = scenario("G-dsh-fail-exit", MockApi(answers=[True, False]), setup_g)
check("G-dsh-fail-exit", r, [], 1, True)

# H: 再次确认 js_api 无公开可递归属性(防止 pywebview 递归刷屏问题回归)
import inspect
api = m.Api()
bad = [n for n in dir(api) if not n.startswith("_")
       and not (inspect.ismethod(getattr(api, n)) or inspect.isfunction(getattr(api, n)))]
ok_h = (bad == [])
print(f"[{'PASS' if ok_h else 'FAIL'}] H-jsapi-introspection-safe  public_non_method={bad}")
if not ok_h:
    failures.append("H-jsapi-introspection-safe")

# I: Api.start_worker 必须解析到 flow.run_install(回归: 拆分后曾因缺 import 报 NameError)
import dshapp.api as api_mod
import dshapp.flow as flow_mod

captured = {}


class _FakeThread:
    def __init__(self, **kw):
        captured.update(kw)

    def start(self):
        pass

    def is_alive(self):
        return False


_orig_thread = api_mod.threading.Thread
api_mod.threading.Thread = _FakeThread
try:
    api2 = m.Api()
    api2.start_worker()
    ok_i = (captured.get("target") is flow_mod.run_install) and api2._started
finally:
    api_mod.threading.Thread = _orig_thread
print(f"[{'PASS' if ok_i else 'FAIL'}] I-start-worker-resolves-run-install  target={captured.get('target')!r}")
if not ok_i:
    failures.append("I-start-worker-resolves-run-install")

# J: 标题栏增强 API(动态任务栏标题/置顶/数据目录/返回安装器)
import time as _time
import dshapp.utils as _utils_mod


class _FakeWin:
    def __init__(self):
        self.title = None
        self.on_top = False
        self.loads = []
        self.urls = []

    def load_html(self, h):
        self.loads.append(h)

    def load_url(self, u):
        self.urls.append(u)

    def destroy(self):
        pass

    def evaluate_js(self, code):
        pass


_fw = _FakeWin()
_api3 = m.Api()
_api3._window = _fw
ok_j = True
_api3.ui_stage("检查环境")
if _fw.title != "dsh · 检查环境":
    ok_j = False
r_j1 = _api3.toggleOnTop()
r_j2 = _api3.toggleOnTop()
if not (r_j1.get("ok") and r_j1.get("on_top") is True and r_j2.get("on_top") is False):
    ok_j = False
_orig_sf = getattr(_utils_mod.os, "startfile", None)
if _orig_sf is not None:
    _utils_mod.os.startfile = lambda p: None
try:
    if _api3.openDataDir() is not True:
        ok_j = False
finally:
    if _orig_sf is not None:
        _utils_mod.os.startfile = _orig_sf
if _api3.backToInstaller() is not True or len(_fw.loads) != 1:
    ok_j = False
_time.sleep(1.3)  # 等 backToInstaller 的定时器触发(非守护线程)
print(f"[{'PASS' if ok_j else 'FAIL'}] J-titlebar-apis  title={_fw.title!r} loads={len(_fw.loads)}")
if not ok_j:
    failures.append("J-titlebar-apis")

# K: toggleOnTop 的 UI 线程封送路径(回归: js_api 桥在后台线程, 直写 WinForms TopMost
#    会触发 .NET 跨线程未处理异常崩溃 0xCFFFFFFF; 修复后经 form.Invoke 封送到 UI 线程)
class _FakeNative:
    def __init__(self):
        self.TopMost = False
        self.invoked = 0

    def Invoke(self, action):
        self.invoked += 1
        action()


class _FakeWin2:
    def __init__(self):
        self.title = None
        self.on_top = False
        self.native = _FakeNative()

    def load_html(self, h):
        pass

    def evaluate_js(self, code):
        pass


try:
    from System import Action  # noqa: F401  (pythonnet 可用性探测)
    _sys_ok = True
except Exception:
    _sys_ok = False

if _sys_ok:
    _fw2 = _FakeWin2()
    _api4 = m.Api()
    _api4._window = _fw2
    _r1 = _api4.toggleOnTop()
    _r2 = _api4.toggleOnTop()
    ok_k = (_r1.get("ok") and _r1.get("on_top") is True
            and _r2.get("ok") and _r2.get("on_top") is False
            and _fw2.native.TopMost is False and _fw2.native.invoked == 2)
    print(f"[{'PASS' if ok_k else 'FAIL'}] K-toggleOnTop-UI-thread-marshal  "
          f"r1={_r1} r2={_r2} invoked={_fw2.native.invoked}")
    if not ok_k:
        failures.append("K-toggleOnTop-UI-thread-marshal")
else:
    print("[SKIP] K-toggleOnTop-UI-thread-marshal  (pythonnet 不可用, 跳过 Invoke 路径验证)")

# T: _scan_usage 的 mtime 预过滤与 zstd 流式解压(旧文件跳过/新文件正确统计)
# 注: 沙箱环境下只能在项目根目录建临时文件(新建子目录写入会被拒), 用完即删。
import datetime as _dt3
import json as _json3
import os as _os3

_TROOT = _os3.path.dirname(_os3.path.abspath(__file__))
_old_p = _os3.path.join(_TROOT, "_usage_test_old.jsonl")
_new_p = _os3.path.join(_TROOT, "_usage_test_new.jsonl")
_z_p = _os3.path.join(_TROOT, "_usage_test_newz.jsonl.zstd")
try:
    _today_ms = _dt3.datetime.combine(_dt3.date.today(), _dt3.time.min).timestamp() * 1000
    _ev = {"type": "assistant/message", "time": _today_ms + 5000,
           "data": {"usage": {"inputTokens": 100, "outputTokens": 200}}}
    # old.jsonl: 文件 mtime 两天前, 但事件时间戳是今天 -> 应被 mtime 过滤跳过
    with open(_old_p, "w", encoding="utf-8") as f:
        f.write(_json3.dumps(_ev) + "\n")
    _yesterday = (_dt3.datetime.now() - _dt3.timedelta(days=2)).timestamp()
    _os3.utime(_old_p, (_yesterday, _yesterday))
    # new.jsonl + newz.jsonl.zstd: mtime 今天 -> 应被统计
    with open(_new_p, "w", encoding="utf-8") as f:
        f.write(_json3.dumps(_ev) + "\n")
    import zstandard as _zstd3
    _comp = _zstd3.ZstdCompressor().compress(_json3.dumps(_ev).encode("utf-8") + b"\n")
    with open(_z_p, "wb") as f:
        f.write(_comp)
    _now_ts = _time.time()
    _os3.utime(_new_p, (_now_ts, _now_ts))
    _os3.utime(_z_p, (_now_ts, _now_ts))

    _usage_res = m.Api()._scan_usage(_TROOT, _today_ms)
    _u_tokens = _usage_res["data"]["today"]["tokens"]
    _u_reqs = _usage_res["data"]["today"]["requests"]
    # 期望: new.jsonl(300/1) + newz.jsonl.zstd(300/1) = 600 tokens / 2 reqs; old 被过滤
    ok_t = (_u_tokens == 600 and _u_reqs == 2)
    print(f"[{'PASS' if ok_t else 'FAIL'}] T-usage-scan-mtime-filter  tokens={_u_tokens} reqs={_u_reqs}")
    if not ok_t:
        failures.append("T-usage-scan-mtime-filter")
finally:
    for _p in (_old_p, _new_p, _z_p):
        try:
            _os3.remove(_p)
        except OSError:
            pass

print()
if failures:
    print("结果: %d 项失败 -> %s" % (len(failures), failures))
    sys.exit(1)
print("结果: 全部通过 ✔")
