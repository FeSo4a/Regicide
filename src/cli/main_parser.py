import argparse
from .config_parser import _set_config_parser


def set_main_parser() -> argparse.ArgumentParser:
    """
    添加CLI命令行主parser

    :return: 一个parser类，供main调用
    """
    main_parser = argparse.ArgumentParser(
        description='''
        弑君者 | 改编自桌游 | By FeSo4a
        '''
    )
    sub_parser = main_parser.add_subparsers(dest='command')
    _set_config_parser(sub_parser)

    main_parser.add_argument('-v', '--version', action='version', version='1.0')

    return main_parser
