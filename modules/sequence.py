from .board import Board
from .pieces import Color
from .fen_processing import fen_out

class Sequence:

    def __init__(self, computed_games: list[Board] | Board | None):
        if isinstance(computed_games, list):
            self.games: list[Board] = computed_games
            self.games_fens: list[str] = []
            for x in computed_games:
                self.games_fens.append(fen_out(x))
        elif isinstance(computed_games, Board):
            self.games: list[Board] = [computed_games]
            self.games_fens = [fen_out(computed_games)]
        else:
            self.games: list[Board] = [
                Board(board_list=None, runde=1, color=Color.WHITE)
            ]
            self.games_fens = [fen_out(self.games[0])]
        self.blocked = -1

    def move_forward(self):
        pass

    def move_backwards(self):
        pass

    def __getitem__(self, index) -> Board:
        return self.games[index]

    def rounds(self) -> int:
        return len(self.games)

    def cache_board(self, board: Board):
        self.games.append(board)
        self.games_fens.append(fen_out(board))
