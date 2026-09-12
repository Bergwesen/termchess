"""Move-generation tables for modules.pieces.

Coordinate convention (from Board.__init__): y=0 is rank 8, y=7 is rank 1.
So a1 == (0,7), a8 == (0,0), e4 == (4,4).

These tests cover *geometry only*. possible_moves() knows nothing about the
board, so it does not filter blocked paths, own-colour occupancy, or pawn
diagonals that have no piece to capture. That filtering belongs to
pseudo_legal(board, pos), which does not exist yet.
"""

import pytest

from modules.pieces import Bauer, Color, Dame, Koenig, Laeufer, Pferd, Turm

import modules.game

ALL_PIECES = [Turm, Pferd, Laeufer, Dame, Koenig, Bauer]


@pytest.mark.parametrize(
    "listt",
    [
        pytest.param([("a7", "a6"), ("a2", "a4")],id="first"),
        pytest.param([("a7", "a5"), ("a2", "a4"), ("a8", "a6")],id="second"),
    ],
)
def test_game_loop_preset(listt):
    test_game = modules.game.Game()
    print(test_game.game_sequence[test_game.current])
    assert test_game.game_loop_preset(preset_list=listt) == True


def test_game_loop_preset_keeps_alternating_turns():
    test_game = modules.game.Game()

    test_game.game_loop_preset([("a7", "a5"), ("a2", "a4"), ("a8", "a6")])

    assert test_game.current == 3
    assert test_game.game_sequence[test_game.current].color == Color.BLACK
