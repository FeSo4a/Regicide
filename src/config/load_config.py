import json
from typing import Final, Tuple
import os

DEFAULT_CONFIG: Final[dict] = {
    'log_path': os.path.join('log'),
    'open_log': False
}


def _new_config(config_path: str) -> None:
    """
    新建一个config文件

    :param config_path: config文件的位置
    :return: None
    """
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)


def read_config(config_path: str) -> Tuple[str, bool]:
    """
    读取config文件

    :param config_path: config文件路径
    :return: log_path (str), open_log (bool)
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config: dict = json.load(f)
            log_path: str = config['log_path']
            open_log: bool = config['open_log']
            return log_path, open_log
    except Exception:
        _new_config(config_path)
        log_path: str = DEFAULT_CONFIG['log_path']
        open_log: bool = DEFAULT_CONFIG['open_log']
        return log_path, open_log


def show_config(log_path: str, open_log: bool) -> None:
    """
    显示config设置

    :param log_path: log路径
    :param open_log: 是否记录log
    :return: None
    """
    print(f'log_path | log文件夹路径： {log_path}')
    print(f'open_log | 是否记录日志： {open_log}')


def set_config(config_path: str, log_path: str | None, open_log: bool | None, config: dict) -> None:
    """
    设置设置文件

    :param config_path: config文件路径
    :param log_path: log文件夹路径
    :param open_log: 是否记录日志
    :param config: 当前config设置
    :return: None
    """
    if log_path is not None:
        config['log_path'] = log_path
    if open_log is not None:
        config['open_log'] = open_log
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
