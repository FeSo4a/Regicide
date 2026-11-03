import os


def _print_screen(boss_deck: list, boss_list: list, player_deck: list, discard_pile: list, deck: list, joker_count: int,
                  armor: int) -> None:
    """
    显示当前信息的函数。

    :param boss_deck: Boss卡池
    :param boss_list: 当前要打的Boss的信息的列表
    :param player_deck: 玩家手牌
    :param discard_pile: 弃牌堆
    :param deck: 抽牌堆
    :param joker_count: 剩余小丑牌数量
    :param armor: 玩家的护甲数量
    :return: None
    """
    print(f'剩余Boss：{len(boss_deck)}')
    print(f'现在的Boss: {boss_list[0]}{boss_list[1]}')
    print(f'Boss血量：{boss_list[2]}')
    print(f'Boss伤害：{boss_list[3]}')
    print()
    print(f'卡池情况：{len(deck)} 剩余卡牌 | {len(discard_pile)} 弃牌区')
    print()
    print(f'玩家护甲：{armor}')
    print(f'玩家剩余底牌：{joker_count}')
    for i in range(len(player_deck)):
        print(f'[{i + 1}] {player_deck[i]}', end=' ')
    print()


# noinspection deprecation
def _clear_screen() -> None:
    """
    用于清理屏幕。

    :return: None
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
