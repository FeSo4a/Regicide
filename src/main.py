from cli import set_main_parser
from game import game_loop
from config import setup_dual_logging
import argparse
import sys


def main() -> None:
    """
    程序入口和主函数。

    :return: None
    """
    parser: argparse.ArgumentParser = set_main_parser()
    parser.parse_args()

    if len(sys.argv) == 1:
        game_loop()


if __name__ == '__main__':
    main()
