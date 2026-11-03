import os


def _print_screen(boss_deck: list, boss_list: list, player_deck: list, discard_pile: list, deck: list, joker_count: int,
                  armor: int) -> None:
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
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
