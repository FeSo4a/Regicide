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
    print(f'玩家剩余底牌：{joker_count} （出牌阶段输入joker即可使用）')
    for i in range(len(player_deck)):
        print(f'[{i + 1}] {player_deck[i]}', end=' ')
    print()


def _print_player_deck(player_deck: list) -> None:
    """
    显示手牌信息

    :param player_deck: 玩家手牌情况
    :return: None
    """
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


def _show_win_screen(joker_count: int, player_deck: list) -> None:
    """
    显示胜利屏幕

    :param joker_count: 剩余底牌数量
    :param player_deck: 玩家胜利时的手牌
    :return: None
    """
    last_deck: int = len(player_deck)
    deck_str: str = ''.join(player_deck)
    print('胜利！！！')
    print('击败Boss: 12/12')
    print(f'已用底牌张数：{2 - joker_count} / 2')
    print(f'结束时还剩下的手牌：{last_deck} / 8')
    if joker_count == 0:
        print('评分：B | 下次争取使用更少的底牌！')
    elif joker_count == 1:
        print('评分：A | 干的漂亮，下次争取使用更少的底牌！')
    else:
        if last_deck == 8 and '♠' in deck_str and '♥' in deck_str and '♦' in deck_str and '♣' in deck_str and (
                'J' in deck_str or 'K' in deck_str or 'Q' in deck_str):
            print(f'评分：U | 完美无瑕！！！卡牌之神诞生了！')
        elif last_deck == 8:
            print(f'评分：X | 完美！！下次试试结束时凑齐花色并尽可能感化Boss吧！')
        elif last_deck == 7:
            print(f'评分：SSS | 完美！！你是怎么办到的？')
        elif last_deck == 6:
            print(f'评分：SS | 完美！你是怎么办到的？')
        else:
            print('评分：S | 干的漂亮，下次争取最后尽可能多地留下手牌。')


def _show_lose_screen(boss_deck: list) -> None:
    """
    显示失败屏幕

    :param boss_deck: 剩余Boss卡池
    :return: None
    """
    killed_boss: int = 12 - len(boss_deck) - 1
    print('失败......')
    print(f'击败Boss: {killed_boss} / 12')
    if killed_boss == 11:
        print('评级：C | 就差一点！')
    elif killed_boss >= 8:
        print('评级：C | 已经步入K级了，胜利就在眼前！')
    elif killed_boss >= 4:
        print('评级：D | 多试几次，下次说不定就能把Q级给过了！')
    else:
        print('评级：F')
