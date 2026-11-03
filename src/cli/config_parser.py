import argparse
from random import choice


def _set_config_parser(sub_parser: argparse._SubParsersAction) -> None:
    """
    设置CLI控制

    :param sub_parser: 传入的子parser
    :return: None
    """
    config_parser = sub_parser.add_parser('config')
    config_parser.add_argument('-l', '--log-path', type=str, help='设置日志输出路径')
    config_parser.add_argument('-o', '--open-log', choices=['y', 'n'], help='设置是否要记录日志')
    config_parser.add_argument('-s', '--show', action='store_true', help='查看当前设置')
