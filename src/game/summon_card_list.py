from typing import Tuple, Final
import random

SUIT: Final[list] = ['♠', '♥', '♦', '♣']
COMMON_RANK: Final[list] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']


def _summon_card() -> Tuple[list, list]:
    """
    快速生成有序的初始牌堆

    :return: player_deck用于给玩家抽牌，boss_deck用于随机生成Boss
    """
    player_deck: list = [f'{s}{r}' for s in SUIT for r in COMMON_RANK]

    boss_deck: list = [
        [f'{s}J' for s in SUIT],
        [f'{s}Q' for s in SUIT],
        [f'{s}K' for s in SUIT]
    ]

    return player_deck, boss_deck


def _set_random_deck(player_deck: list, boss_deck: list) -> Tuple[list, list]:
    """
    随机打乱牌堆。

    :param player_deck: 用于给玩家抽牌的牌堆
    :param boss_deck: 用于随机生成Boss的牌堆
    :return: player_deck, boss_deck，同上，已打乱。
    """
    random.shuffle(player_deck)  # 打乱玩家牌堆
    temp_boss_deck: list = boss_deck
    boss_deck: list = []  # 创建临时列表装boss牌堆

    for i in temp_boss_deck:
        random.shuffle(i)  # 分层打乱保证永远先刷J再是Q最后是K
    for i in temp_boss_deck:
        for j in i:
            boss_deck.append(j)  # 打乱好后将嵌套删去

    return player_deck, boss_deck


def _summon_boss(boss_deck: list) -> list:
    """
    抽牌，定义Boss信息

    :param boss_deck: Boss牌堆
    :return: 一个存有Boss信息的列表
    """
    boss: str = boss_deck.pop(0)  # 翻开第一张

    match boss[1]:  # 根据信息生成boss
        case 'J':
            boss_health = 20
            boss_attack = 10
        case 'Q':
            boss_health = 30
            boss_attack = 15
        case 'K':
            boss_health = 40
            boss_attack = 20

    # noinspection unbound-local-variable
    boss_list: list = [boss[0], boss[1], boss_health, boss_attack]

    return boss_list
