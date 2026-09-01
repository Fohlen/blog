import argparse
from itertools import product

from simulation import simulate_game, random_strategy, minimal_distance_strategy, trick_strategy

_STRATEGY_TO_CB = {
    "random": random_strategy,
    "minimal": minimal_distance_strategy,
    "trick": trick_strategy
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", default=1000, type=int, nargs="?")
    args = parser.parse_args()

    strategies = ["random", "minimal", "trick"]
    players = list(range(1, 8))

    for i in range(args.repeats):
        for n_players, strategy in product(players, strategies):
            cards_played_total = simulate_game(n_players, _STRATEGY_TO_CB[strategy])
            print("\t".join([str(item) for item in [n_players, strategy, cards_played_total]]))
