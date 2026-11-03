from .summon_card_list import _set_random_deck, _summon_card, _summon_boss
from .player_input import _draw_card, _play_card, _discard_pile_to_deck, _check_if_can_fold, _fold_cards
from .screen import _print_screen, _clear_screen, _print_player_deck, _show_win_screen, _show_lose_screen


def game_loop() -> None:
    """
    游戏主循环接口，供main调用

    :return: None
    """
    # 随机生成卡组
    deck, boss_deck = _summon_card()
    deck, boss_deck = _set_random_deck(deck, boss_deck)
    # 初始化弃牌堆、boss牌和玩家手牌
    discard_pile: list = []
    player_deck: list = []
    _draw_card(deck, player_deck, 8)
    boss_list: None | list = None
    # 初始化玩家底牌数量和护甲
    joker_count: int = 2
    armor: int = 0

    # 游戏主循环
    while True:
        _clear_screen()  # 清屏
        if boss_list is None and len(boss_deck) > 0:
            boss_list: None | list = _summon_boss(boss_deck)  # 如果当前Boss没了就抽一张
        elif boss_list is None and len(boss_deck) == 0:  # 如果所有Boss都没了则胜利
            _show_win_screen(joker_count, player_deck)
            return

        # noinspection bad-argument-type
        # 出牌阶段
        _print_screen(boss_deck, boss_list, player_deck, discard_pile, deck, joker_count, armor)
        user_input = input('请输入要出牌的序列号，如果要出多张牌请勿分割：\n')
        result = _play_card(player_deck, user_input, discard_pile)

        if result is None:  # 输入不合法
            continue

        elif result == 'joker':
            # TODO: 小丑牌逻辑
            _clear_screen()
            print('你出了小丑牌')
            input()

        # 发动技能阶段
        _clear_screen()
        suit, rank = result
        print(f'你出了{rank}点数！')
        double_attack = False  # 两倍攻击标记，留给攻击阶段

        # 如果攻击者的花色和boss一样，那么该技能不会被发动。
        suit = suit.replace(boss_list[0], '')
        print(f'你发动了{suit}花色技能！')

        if '♠' in suit:
            armor += rank  # 增加防御，一个Boss死亡才会重置
            print(f'你增加了{rank}点防御！现在是{armor}点防御。')
        if '♥' in suit:
            _discard_pile_to_deck(deck, discard_pile, rank)
            print(f'已将弃牌区中的{rank}张牌加入牌库！')
        if '♦' in suit:
            if len(player_deck) + rank > 8:  # 如果抽牌到上限则抽到上限
                add_card_count = 8 - len(player_deck)
            else:
                add_card_count = rank
            _draw_card(deck, player_deck, add_card_count)
            print(f'你抽取了{add_card_count}张卡牌！')
        if '♣' in suit:
            double_attack = True  # 两倍攻击标记
            print(f'攻击力增强成功！')
        input('回车确认')

        # 攻击Boss阶段
        _clear_screen()
        if double_attack:
            boss_list[2] = boss_list[2] - rank * 2
            print(f'双倍伤害！你对Boss造成了{rank * 2}点伤害！')
        else:
            boss_list[2] = boss_list[2] - rank
            print(f'你对Boss造成了{rank}点伤害！')
        # 校验Boss是否死亡
        if boss_list[2] < 0:
            print(f'Boss死亡！')
            discard_pile.append(f'{boss_list[0]}{boss_list[1]}')  # 存入弃牌区
            # 重置护甲和boss栏
            boss_list: None | list = None
            armor: int = 0
            input('回车确认')
            continue
        elif boss_list[2] == 0:
            print(f'Boss血量恰为0，你感化了Boss！')
            deck.insert(0, f'{boss_list[0]}{boss_list[1]}')  # 放在牌库头，下一回合就能抽到
            # 重置护甲和boss栏
            boss_list: None | list = None
            armor: int = 0
            input('回车确认')
            continue
        input('回车确认')

        # Boss反击阶段
        _clear_screen()
        damage: int = boss_list[3] - armor
        if damage < 0:
            damage = 0
        print(f'Boss对你造成了{damage}点伤害！')
        if damage == 0:
            continue
        # 从手牌中弃掉比damage大的手牌
        can_fold = _check_if_can_fold(player_deck, damage)
        if not can_fold:
            _show_lose_screen(boss_deck)
            return
        # 输出手牌并让用户输入
        _print_player_deck(player_deck)
        true_input = False
        while not true_input:
            fold_input = input('请弃掉比伤害数量大的牌，可弃多张：\n')
            true_input, fold_input_num = _fold_cards(player_deck, damage, fold_input)  # 检测弃牌合法性
        # 弃牌
        for i in fold_input_num:
            discard_pile.append(player_deck.pop(i - 1))
        input('回车确认')
