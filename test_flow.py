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

print()
if failures:
    print("结果: %d 项失败 -> %s" % (len(failures), failures))
    sys.exit(1)
print("结果: 全部通过 ✔")
