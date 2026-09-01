import argparse
import random
import sys
from itertools import chain, combinations
from operator import gt, lt
from typing import Callable

Game = tuple[list[int], list[int], list[int], list[int]]
Move = tuple[int, int]
Strategy = Callable[[Game, list[int]], Move]


def simulate_game(num_players: int, strategy: Strategy) -> int:
    """
    Simulates a game and returns the number of playable cards.

    :param num_players: the number of players to simulate the game for.
    :param strategy: the strategy to apply.
    :return: the number of cards that could be played.
    """

    if num_players < 1 or num_players > 7:
        raise ValueError(f"Can't play a game with {num_players} players.")

    # Initialize the game
    game = ([1], [1], [100], [100])
    deck = list(range(2, 100))
    random.shuffle(deck)

    # Initialize the player decks
    if num_players == 1:
        num_cards = 8
    elif num_players == 2:
        num_cards = 7
    else:
        num_cards = 6

    player_hands = [[] for _ in range(num_players)]
    for _ in range(num_cards):
        for hand in player_hands:
            hand.append(deck.pop())

    # Start playing the game
    cards_played = 0
    game_running = True

    # The game is running so long as there are cards in the deck or player hands
    while len(deck) and len(list(chain.from_iterable(player_hands))) and game_running:
        for hand in player_hands:
            # Choose the deck and card to play using the strategy
            deck_to_play, card_to_play = strategy(
                game,
                hand
            )

            # Draw the card
            card = hand.pop(card_to_play)

            # Check if it is valid for the selected deck
            comparator = gt if deck_to_play < 2 else lt
            if comparator(card, game[deck_to_play][-1]):
                game[deck_to_play].append(card)
                cards_played += 1

                if len(deck):
                    hand.append(deck.pop())
            else:
                game_running = False
                break

    return cards_played


def random_strategy(game: Game, hand: list[int]) -> Move:
    """
    Picks any valid card at random and puts it on a random (but allowed) pile.
    """
    valid_cards = []
    for index, g in enumerate(game):
        comparator = gt if index < 2 else lt
        for index_card, card in enumerate(hand):
            if comparator(card, g[-1]):
                valid_cards.append((index, index_card))

    if len(valid_cards):
        deck_to_play, card_to_play = random.choice(valid_cards)
        return deck_to_play, card_to_play
    else:
        return 0, 0


def minimal_distance_strategy(game: Game, hand: list[int]) -> Move:
    """
    Picks the card with the least distance to any of the piles and puts it on that pile.
    """
    ascending_values = [game[0][-1], game[1][-1]]
    min_ascending = min(ascending_values)
    descending_values = [game[2][-1], game[3][-1]]
    max_descending = max(descending_values)

    sorted_hand = sorted(hand)
    if abs(min_ascending - sorted_hand[0]) < abs(max_descending - sorted_hand[-1]):
        card_to_play = hand.index(sorted_hand[0])
        if game[0][-1] == min_ascending:
            return 0, card_to_play
        else:
            return 1, card_to_play
    else:
        card_to_play = hand.index(sorted_hand[-1])
        if game[2][-1] == max_descending:
            return 2, card_to_play
        else:
            return 3, card_to_play


def trick_strategy(game: Game, hand: list[int]) -> Move:
    """
    Tries to play cards such that in a consecutive move we can use a jump 10 (as specified in the tricks section).
    """
    possible_cards = []

    for game_index, g in enumerate(game):
        for card_deck in g:
            for card_index, card in enumerate(hand):
                if abs(card_deck - card) == 10:
                    possible_cards.append((game_index, card_index))

    if len(possible_cards):
        return random.choice(possible_cards)

    for card1, card2 in combinations(hand, 2):
        if abs(card1 - card2) == 10:
            for index in range(3):
                comparator = gt if index < 2 else lt
                if comparator(card1, game[index][-1]):
                    possible_cards.append((index, hand.index(card1)))

    if len(possible_cards):
        return random.choice(possible_cards)
    else:
        return random_strategy(game, hand)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_players", type=int)
    parser.add_argument("--strategy", type=str, default="random", choices=["random", "minimal", "trick"], nargs="?")
    args = parser.parse_args()

    match args.strategy:
        case "random":
            player_strategy = random_strategy
        case "minimal":
            player_strategy = minimal_distance_strategy
        case "trick":
            player_strategy = trick_strategy
        case _:
            player_strategy = random_strategy

    cards_played_total = simulate_game(args.num_players, player_strategy)
    print(
        f"Simulated game with {args.num_players} players and {args.strategy} strategy. Played {cards_played_total}.",
        file=sys.stderr
    )
