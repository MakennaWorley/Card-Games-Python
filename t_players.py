from texas_holdem import TexasHoldemGame
from player import RandomPlayer
from ai_player import MinimaxPlayer, AlphaBetaPlayer


class TPlayers():
    def __init__(self, number_of_games, verbose=False, testing=True):
        self.number_of_games = number_of_games
        self.verbose = verbose
        self.testing = testing

    def t_minimax_random(self, verbose=False, testing=True):
        wins = {
            "random": 0,
            "minimax": 0
        }

        for _ in range(self.number_of_games):
            players = [
                RandomPlayer("Random1", 1000),
                RandomPlayer("Random2", 1000),
                MinimaxPlayer("Minimax1", 1000),
                MinimaxPlayer("Minimax2", 1000),
            ]
            game = TexasHoldemGame(players, verbose=verbose, testing=testing)
            game.play_round()

            max_chips = max(p.chips for p in players)
            winners = [p for p in players if p.chips == max_chips]

            for winner in winners:
                if isinstance(winner, RandomPlayer):
                    wins["random"] += 1 / len(winners)
                else:
                    wins["minimax"] += 1 / len(winners)

        print(f"Out of {self.number_of_games} games:")
        print(f"  Random Players won {wins['random']:.1f} games")
        print(f"  Minimax Players won {wins['minimax']:.1f} games")

    def t_alphabeta_random(self, verbose=False, testing=True):
        wins = {
            "random": 0,
            "alphabeta": 0
        }

        for _ in range(self.number_of_games):
            players = [
                RandomPlayer("Random1", 1000),
                RandomPlayer("Random2", 1000),
                AlphaBetaPlayer("AlphaBeta1", 1000),
                AlphaBetaPlayer("AlphaBeta2", 1000),
            ]
            game = TexasHoldemGame(players, verbose=verbose, testing=testing)
            game.play_round()

            max_chips = max(p.chips for p in players)
            winners = [p for p in players if p.chips == max_chips]

            for winner in winners:
                if isinstance(winner, RandomPlayer):
                    wins["random"] += 1 / len(winners)
                else:
                    wins["alphabeta"] += 1 / len(winners)

        print(f"Out of {self.number_of_games} games:")
        print(f"  Random Players won {wins['random']:.1f} games")
        print(f"  AlphaBeta Players won {wins['alphabeta']:.1f} games")

    def t_alphabeta_minimax(self, verbose=False, testing=True):
        wins = {
            "alphabeta": 0,
            "minimax": 0
        }

        for _ in range(self.number_of_games):
            players = [
                AlphaBetaPlayer("AlphaBeta1", 1000),
                AlphaBetaPlayer("AlphaBeta2", 1000),
                MinimaxPlayer("Minimax1", 1000),
                MinimaxPlayer("Minimax2", 1000),
            ]
            game = TexasHoldemGame(players, verbose=verbose, testing=testing)
            game.play_round()

            max_chips = max(p.chips for p in players)
            winners = [p for p in players if p.chips == max_chips]

            for winner in winners:
                if isinstance(winner, AlphaBetaPlayer):
                    wins["alphabeta"] += 1 / len(winners)
                else:
                    wins["minimax"] += 1 / len(winners)

        print(f"Out of {self.number_of_games} games:")
        print(f"  AlphaBeta Players won {wins['alphabeta']:.1f} games")
        print(f"  Minimax Players won {wins['minimax']:.1f} games")


if __name__ == "__main__":
    t = TPlayers(1_000, verbose=False, testing=True)

    t.t_minimax_random()
    t.t_alphabeta_random()
    t.t_alphabeta_minimax()
