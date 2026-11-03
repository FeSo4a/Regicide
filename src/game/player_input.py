def _draw_card(deck: list, player_deck: list, count: int) -> None:
    for _ in range(count):
        if len(player_deck) > 8:
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
    temp_rank: list = [int(i) for i in temp_rank]
    if sum(temp_rank) > 10:  # 第一个条件：除了A外所有数字总和都要小于等于10
        raise ValueError('SumError')
    elif len(list(set(temp_rank))) > 1:  # 第二个条件：除了A外不能有散牌
        raise ValueError('RankError')

    # 将rank里面的A换成1，为了转成整数
    while 'A' in rank:
        rank.remove('A')
        rank.append('1')
    rank: list = [int(i) for i in rank]
    rank: int = sum(rank)  # 最后只需返回花色+总和就足够进行剩下操作了

    return suit, rank


def _play_card(player_deck: list, player_input: str) -> tuple | None | str:
    if player_input == '':
        input('输入有误，请按回车再试一次')
        return None

    player_input: str = player_input.strip()
    player_input: str = player_input.lower()
    if player_input == 'joker':
        return 'joker'

    input_list: list = list(player_input)
    input_list = list(set(input_list))

    # noinspection broad-exception
    try:
        input_number: list = [int(i) for i in input_list]
    except Exception:
        input('输入有误，请按回车再确认一次。')
        return None

    return_card: list = []
    # noinspection broad-exception
    try:
        for i in input_number:
            return_card.append(player_deck[i - 1])
    except Exception:
        input('输入有误，请按回车再确认一次。')
        return None

    try:
        suit, rank = _check_card(return_card)
        for i in input_number:
            del player_deck[i - 1]
        return suit, rank
    except ValueError:
        input('出牌有误，请按回车再确认一次')
        return None
