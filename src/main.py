from cli import set_main_parser
from game import game_loop
from config import setup_dual_logging, read_config, show_config, set_config
import argparse
import sys
import os
from typing import Final

DEFAULT_CONFIG_PATH: Final[str] = 'config.json'


def main() -> None:
    """
    程序入口和主函数。

    :return: None
    """
    log_path, open_log = read_config(DEFAULT_CONFIG_PATH)
    if open_log:
        setup_dual_logging(log_path)

    parser: argparse.ArgumentParser = set_main_parser()
    arg = parser.parse_args()

    if arg.command == 'config':
        if arg.show:
            show_config(log_path, open_log)

        match arg.open_log:
            case 'y':
                open_log_ = True
            case 'n':
                open_log_ = False
            case _:
                open_log_ = None

        config = {'log_path': log_path, 'open_log': open_log}
        set_config(DEFAULT_CONFIG_PATH, arg.log_path, open_log_, config)

    elif len(sys.argv) == 1:
        game_loop()


if __name__ == '__main__':
    main()
