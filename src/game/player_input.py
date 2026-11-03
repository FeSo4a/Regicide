import random
from typing import Tuple


def _draw_card(deck: list, player_deck: list, count: int) -> None:
    """
    抽牌逻辑

    :param deck: 一个牌组
    :param player_deck: 玩家手牌
    :param count: 抽牌数量
    :return: None
    """
    for _ in range(count):
        if len(player_deck) > 7:
            return
        elif len(deck) == 0:
            return
        player_deck.append(deck.pop(0))


def _check_card(card: list) -> tuple:
    """
    检查用户输入传来的卡片列表是否合法。

    :param card: 一个列表，每一项是一个字符串，如：['♠5']
    :return: 一个元组，分别是花色（字符串）、数字总和
    """
    # 生成两个列表，一个装花色，一个装数字
    suit: list = []
    rank: list = []

    # 把card里面的str分割成花色和列表两个
    for i in card:
        suit.append(i[0])
        rank.append(i[1:])
    suit: list = list(set(suit))
    suit: str = ''.join(suit)  # 去除重复花色（不会计算在内），并整理成一个字符串
    temp_rank: list = rank[:]  # 拷贝一个临时装数字的

    # A是“宠物牌”，跟在所有牌后都合法
    while 'A' in temp_rank:
        temp_rank.remove('A')  # 所以校验合法性先去除它，同时也是为了后面转为int
    # 将其余牌也转换
    while 'J' in temp_rank:
        temp_rank.remove('J')
        temp_rank.append('10')
    while 'Q' in temp_rank:
        temp_rank.remove('Q')
        temp_rank.append('15')
    while 'K' in temp_rank:
        temp_rank.remove('K')
        temp_rank.append('20')

    temp_rank: list = [int(i) for i in temp_rank]
    if sum(temp_rank) > 10:  # 第一个条件：除了A外所有数字总和都要小于等于10
        raise ValueError('SumError')
    elif len(list(set(temp_rank))) > 1:  # 第二个条件：除了A外不能有散牌
        raise ValueError('RankError')

    # 将rank里面的字符换成对应数字，为了转成整数
    while 'A' in rank:
        rank.remove('A')
        rank.append('1')
    while 'J' in rank:
        rank.remove('J')
        rank.append('10')
    while 'Q' in rank:
        rank.remove('Q')
        rank.append('15')
    while 'K' in rank:
        rank.remove('K')
        rank.append('20')

    rank: list = [int(i) for i in rank]
    rank: int = sum(rank)  # 最后只需返回花色+总和就足够进行剩下操作了

    return suit, rank


def _play_card(player_deck: list, player_input: str, discard_pile: list) -> tuple | None | str:
    """
    获取并处理玩家输入

    :param player_deck: 玩家手牌
    :param player_input: 玩家输入的序列号，可能为数字组合、joker、或者其他
    :param discard_pile: 弃牌区
    :return: 为joker的时候直接返回字符串、有误时返回None、正常状况返回元组，装有suit花色和rank数字的
    """
    if player_input == '':  # 输入为空时
        input('输入有误，请按回车再试一次')
        return None

    # 统一去除空白内容转小写，并验证是否是joker
    player_input: str = player_input.replace(' ', '')
    player_input: str = player_input.lower()
    if player_input == 'joker':
        return 'joker'

    input_list: list = list(player_input)
    input_list = list(set(input_list))  # 将输入转为列表，并去除重复元素

    # noinspection broad-exception
    # 尝试将输入列表中所有项都转为int
    try:
        input_number: list = [int(i) for i in input_list]
    except Exception:
        input('输入有误，请按回车再确认一次。')
        return None

    return_card: list = []  # 现在根据输入从手牌中提取卡片存入它
    # noinspection broad-exception
    try:
        for i in input_number:
            return_card.append(player_deck[i - 1])
    except Exception:
        input('输入有误，请按回车再确认一次。')
        return None

    try:
        suit, rank = _check_card(return_card)  # 送入比较函数校验并得出花色及总值。
        for i in input_number:
            discard_pile.append(player_deck.pop(i - 1))
        return suit, rank
    except ValueError:
        input('出牌有误，请按回车再确认一次')
        return None


def _discard_pile_to_deck(deck: list, discard_pile: list, count: int) -> None:
    """
    将弃牌区的牌打乱后随机选出上面的几个牌放回牌库底端

    :param deck: 牌库
    :param discard_pile: 弃牌区
    :param count: 要选几个牌
    :return: None
    """
    random.shuffle(discard_pile)
    if count > len(discard_pile):
        count = len(discard_pile)
    for _ in range(count):
        deck.append(discard_pile.pop(0))


def _check_if_can_fold(player_deck: list, damage: int) -> bool:
    """
    校验玩家是否死亡的函数

    :param player_deck: 玩家的手牌
    :param damage: Boss的伤害
    :return: True/False
    """
    rank: list = [i[1] for i in player_deck]

    while 'A' in rank:
        rank.remove('A')
        rank.append('1')
    while 'J' in rank:
        rank.remove('J')
        rank.append('10')
    while 'Q' in rank:
        rank.remove('Q')
        rank.append('15')
    while 'K' in rank:
        rank.remove('K')
        rank.append('20')

    rank: list = [int(i) for i in rank]
    sum_rank: int = sum(rank)
    return sum_rank > damage


def _fold_cards(player_deck: list, damage: int, fold_input: str) -> Tuple(bool, list | None):
    """
    检测玩家弃牌合法性的函数

    :param player_deck: 玩家手牌
    :param damage: Boss造成的伤害
    :param fold_input: 玩家的输入
    :return: True/False | 提取到的输入
    """
    if fold_input == '':  # 输入为空时
        input('输入有误，请按回车再试一次')
        return False, None

    # 统一去除空白内容转小写
    fold_input: str = fold_input.replace(' ', '')
    fold_input: str = fold_input.lower()

    input_list: list = list(fold_input)
    input_list = list(set(input_list))  # 将输入转为列表，并去除重复元素

    # noinspection broad-exception
    # 尝试将输入列表中所有项都转为int
    try:
        input_number: list = [int(i) for i in input_list]
    except Exception:
        input('输入有误，请按回车再确认一次。')
        return False, None

    return_card: list = []
    # noinspection broad-exception
    try:
        for i in input_number:
            return_card.append(player_deck[i - 1])
    except Exception:
        input('输入有误，请按回车再确认一次。')
        return False, None

    rank: list = [i[1:] for i in return_card]

    while 'A' in rank:
        rank.remove('A')
        rank.append('1')
    while 'J' in rank:
        rank.remove('J')
        rank.append('10')
    while 'Q' in rank:
        rank.remove('Q')
        rank.append('15')
    while 'K' in rank:
        rank.remove('K')
        rank.append('20')

    rank: list = [int(i) for i in rank]
    if sum(rank) < damage:
        input('输入有误，请按回车再确认一次。')
        return False, None
    return True, input_number
