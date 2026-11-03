from .summon_card_list import _set_random_deck, _summon_card, _summon_boss
from .player_input import _draw_card, _play_card
from .screen import _print_screen, _clear_screen


def game_loop() -> None:
    deck, boss_deck = _summon_card()
    deck, boss_deck = _set_random_deck(deck, boss_deck)
    joker_count: int = 2

    discard_pile: list = []
    player_deck: list = []
    _draw_card(deck, player_deck, 8)
    boss_list: None | list = None
    armor: int = 0

    while True:
        _clear_screen()
        if boss_list is None and len(boss_deck) > 0:
            boss_list: None | list = _summon_boss(boss_deck)
        elif boss_list is None and len(boss_deck) == 0:
            # TODO: 胜利界面
            pass

        # noinspection bad-argument-type
        _print_screen(boss_deck, boss_list, player_deck, discard_pile, deck, joker_count, armor)
        user_input = input('请输入要出牌的序列号，如果要出多张牌请勿分割：\n')
        result = _play_card(player_deck, user_input)

        if result is None:
            continue

        elif result == 'joker':
            # TODO: 小丑牌逻辑
            print('你出了小丑牌')
            input()

        suit, rank = result
        print(f'你出了{rank}点数！')
        print(f'你发动了{suit}花色技能！')
        input(f'回车确认')
