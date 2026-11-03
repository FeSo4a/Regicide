"""dual_log.py

一行启用：所有 print / stderr 输出同时写入终端和日志文件。

用法：
    from dual_log import setup_dual_logging
    setup_dual_logging("logs")   # 只需传一个文件夹路径
"""

import atexit
import os
import sys
from datetime import datetime

__all__ = ["setup_dual_logging"]

_installed = False
_log_file = None
_original_stdout = None
_original_stderr = None


class _Tee:
    """把写操作转发给多个流；属性访问代理到第一个流（终端）。"""

    def __init__(self, *streams):
        self._streams = streams

    def write(self, data):
        for s in self._streams:
            try:
                s.write(data)
            except Exception:
                pass
        return len(data)  # 遵循 TextIOBase.write 的约定

    def flush(self):
        for s in self._streams:
            try:
                s.flush()
            except Exception:
                pass

    def close(self):
        for s in self._streams:
            try:
                s.close()
            except Exception:
                pass

    def __getattr__(self, name):
        # 让 isatty / fileno / encoding / buffer 等查询走终端
        return getattr(self._streams[0], name)


def setup_dual_logging(log_dir, *, filename=None, encoding="utf-8", mirror_stderr=True):
    """把 sys.stdout（和 sys.stderr）同时镜像到 log_dir 下的日志文件。

    :param log_dir: 日志文件夹，不存在会自动创建。
    :param filename: 可选，日志文件名；默认按时间生成，如 app_2026-11-03_12-30-00.log。
    :param encoding: 文件编码，默认 utf-8。
    :param mirror_stderr: 是否把 stderr（包括 traceback）也写进日志，默认 True。
    :return: 实际打开的日志文件路径。
    """
    global _installed, _log_file, _original_stdout, _original_stderr

    if _installed:  # 幂等，重复调用返回已有路径
        return _log_file.name if _log_file else None

    os.makedirs(log_dir, exist_ok=True)
    if filename is None:
        filename = f"app_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
    path = os.path.join(log_dir, filename)

    # buffering=1 → 文本模式行缓冲：遇到 \n 立即落盘，崩溃也不易丢日志
    log_file = open(path, "a", encoding=encoding, buffering=1)

    # 保存当前流（也就是终端），避免以后恢复时用错对象
    _original_stdout = sys.stdout
    _original_stderr = sys.stderr

    sys.stdout = _Tee(_original_stdout, log_file)
    if mirror_stderr:
        sys.stderr = _Tee(_original_stderr, log_file)

    _installed = True
    _log_file = log_file
    atexit.register(_cleanup)

    return path


def _cleanup():
    """进程正常退出时恢复 stdout/stderr 并关闭文件。"""
    global _installed, _log_file, _original_stdout, _original_stderr
    if not _installed:
        return
    if _original_stdout is not None:
        sys.stdout = _original_stdout
    if _original_stderr is not None:
        sys.stderr = _original_stderr
    if _log_file is not None:
        try:
            _log_file.flush()
            _log_file.close()
        except Exception:
            pass
        _log_file = None
    _installed = False
