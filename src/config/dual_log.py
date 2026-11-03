"""dual_log.py — 所有 print/stderr 同时写终端和日志文件。"""

import atexit
import os
import sys
import threading
from datetime import datetime

__all__ = ["setup_dual_logging"]

_installed = False
_log_file = None
_original_stdout = None
_original_stderr = None
_lock = threading.RLock()
_error_reported = False


class _Tee:
    def __init__(self, primary, secondary, on_error=None):
        self._primary = primary  # 终端（可能为 None）
        self._secondary = secondary  # 日志文件
        self._on_error = on_error
        self._closed = False

    def write(self, data):
        with _lock:
            n = 0
            for stream in (self._primary, self._secondary):
                if stream is None:
                    continue
                try:
                    n = stream.write(data)
                except Exception as e:
                    self._report(e, stream)
            return len(data)

    def flush(self):
        with _lock:
            for stream in (self._primary, self._secondary):
                if stream is None:
                    continue
                try:
                    stream.flush()
                except Exception as e:
                    self._report(e, stream)

    def close(self):
        # 只关日志文件，绝不动终端
        with _lock:
            if self._closed:
                return
            self._closed = True
            try:
                if self._secondary is not None:
                    self._secondary.close()
            except Exception:
                pass

    def _report(self, exc, stream):
        global _error_reported
        if _error_reported:
            return
        _error_reported = True
        try:
            name = "stdout" if stream is self._primary else "log file"
            # 直接写原始 stderr，绕开 _Tee，避免递归
            msg = f"\n[dual_log] 写入 {name} 失败: {exc!r}\n"
            orig = _original_stderr or sys.__stderr__
            if orig is not None:
                orig.write(msg)
                orig.flush()
        except Exception:
            pass

    def __getattr__(self, name):
        # 只代理到终端；终端为 None 时给出合理默认
        primary = object.__getattribute__(self, "_primary")
        if primary is None:
            if name in ("isatty",):
                return lambda: False
            if name in ("fileno",):
                return lambda: (_ for _ in ()).throw(OSError("no fileno"))
            raise AttributeError(name)
        return getattr(primary, name)


def setup_dual_logging(log_dir, *, filename=None, encoding="utf-8",
                       mirror_stderr=True, errors="backslashreplace"):
    """把 sys.stdout（和 stderr）同时镜像到 log_dir 下的日志文件。

    :param log_dir: 日志文件夹，自动创建。
    :param filename: 可选，默认 app_YYYY-MM-DD_HH-MM-SS.log。
    :param encoding: 文件编码，默认 utf-8。
    :param mirror_stderr: 是否镜像 stderr（含 traceback），默认 True。
    :param errors: 文件编码错误策略，默认 backslashreplace（不会因编码崩）。
    :return: 日志文件绝对路径。
    :raises OSError: 目录或文件无法创建时抛出，让调用方知道。
    """
    global _installed, _log_file, _original_stdout, _original_stderr

    with _lock:
        if _installed:
            return os.path.abspath(_log_file.name) if _log_file else None

        os.makedirs(log_dir, exist_ok=True)
        if filename is None:
            filename = f"app_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
        path = os.path.abspath(os.path.join(log_dir, filename))

        # 行缓冲 + 编码兜底，避免 UnicodeEncodeError 静默丢日志
        log_file = open(path, "a", encoding=encoding,
                        errors=errors, buffering=1)

        _original_stdout = sys.stdout
        _original_stderr = sys.stderr

        sys.stdout = _Tee(_original_stdout, log_file)
        if mirror_stderr:
            sys.stderr = _Tee(_original_stderr, log_file)

        # 显式接管未捕获异常，保证 flush
        sys.excepthook = _make_excepthook(_original_stderr)
        try:
            import threading as _t
            if hasattr(_t, "excepthook"):
                _t.excepthook = _make_excepthook(_original_stderr,
                                                 thread=True)
        except Exception:
            pass

        _installed = True
        _log_file = log_file
        atexit.register(_cleanup)

        return path


def _make_excepthook(base_stream, thread=False):
    def hook(exc_type, exc_value, tb):
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:
            pass
        # 交给原始 hook，它写原始 stderr；由于 sys.stderr 已被 Tee 替换，
        # traceback 会同时进终端和文件
        import traceback
        text = "".join(traceback.format_exception(exc_type, exc_value, tb))
        try:
            sys.stderr.write(text)
            sys.stderr.flush()
        except Exception:
            if base_stream is not None:
                base_stream.write(text)

    if thread:
        def thread_hook(args):
            hook(args.exc_type, args.exc_value, args.exc_traceback)

        return thread_hook
    return hook


def _cleanup():
    global _installed, _log_file, _original_stdout, _original_stderr
    with _lock:
        if not _installed:
            return
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:
            pass
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
