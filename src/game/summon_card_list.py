from typing import Tuple, Final
import random

SUIT: Final[list] = ['♠', '♥', '♦', '♣']
COMMON_RANK: Final[list] = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']


def _summon_card() -> Tuple[list, list]:
    player_deck: list = [f'{s}{r}' for s in SUIT for r in COMMON_RANK]

    boss_deck: list = [
        [f'{s}J' for s in SUIT],
        [f'{s}Q' for s in SUIT],
        [f'{s}K' for s in SUIT]
    ]

    return player_deck, boss_deck


def _set_random_deck(player_deck: list, boss_deck: list) -> Tuple[list, list]:
    random.shuffle(player_deck)
    temp_boss_deck: list = boss_deck
    boss_deck: list = []

    for i in temp_boss_deck:
        random.shuffle(i)

    for i in temp_boss_deck:
        for j in i:
            boss_deck.append(j)

    return player_deck, boss_deck


def _summon_boss(boss_deck: list) -> list:
    boss: str = boss_deck.pop(0)

    match boss[1]:
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
