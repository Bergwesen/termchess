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

ALL_PIECES = [Turm, Pferd, Laeufer, Dame, Koenig, Bauer]

# corner, opposite corner, edge, centre
SAMPLE_SQUARES = [(0, 7), (7, 0), (0, 4), (4, 4)]


def squares(piece):
    """possible_moves() as a set of (x, y) — Position is unhashable."""
    return {(m.x, m.y) for m in piece.possible_moves()}


# --------------------------------------------------------------------------
# exact sets: small enough to write out in full
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "x,y,expected",
    [
        pytest.param(0, 7, {(1, 5), (2, 6)}, id="a1_corner"),
        pytest.param(7, 0, {(5, 1), (6, 2)}, id="h8_corner"),
        pytest.param(0, 4, {(1, 2), (1, 6), (2, 3), (2, 5)}, id="a4_edge"),
        pytest.param(
            4, 3,
            {(3, 1), (5, 1), (2, 2), (6, 2), (2, 4), (6, 4), (3, 5), (5, 5)},
            id="e5_centre",
        ),
    ],
)
def test_pferd_moves(x, y, expected):
    knight = Pferd(Color.WHITE, x, y, [])
    moves = knight.possible_moves()
    assert squares(knight) == expected
    assert len(moves) == len(expected), "duplicate squares emitted"


@pytest.mark.parametrize(
    "x,y,expected",
    [
        pytest.param(0, 7, {(0, 6), (1, 6), (1, 7)}, id="a1_corner"),
        pytest.param(7, 0, {(6, 0), (6, 1), (7, 1)}, id="h8_corner"),
        pytest.param(0, 4, {(0, 3), (0, 5), (1, 3), (1, 4), (1, 5)}, id="a4_edge"),
        pytest.param(
            4, 4,
            {(3, 3), (4, 3), (5, 3), (3, 4), (5, 4), (3, 5), (4, 5), (5, 5)},
            id="e4_centre",
        ),
    ],
)
def test_koenig_moves(x, y, expected):
    king = Koenig(Color.WHITE, x, y, [])
    moves = king.possible_moves()
    assert squares(king) == expected
    assert len(moves) == len(expected), "duplicate squares emitted"


# --------------------------------------------------------------------------
# sliders: count + diagnostic members (full sets are 14-27 squares)
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "x,y,must_contain",
    [
        # a rook reaches its whole rank and file from anywhere: 7 + 7
        pytest.param(0, 7, {(7, 7), (0, 0)}, id="a1_corner"),
        pytest.param(7, 0, {(0, 0), (7, 7)}, id="h8_corner"),
        pytest.param(4, 4, {(0, 4), (7, 4), (4, 0), (4, 7)}, id="e4_centre"),
    ],
)
def test_turm_moves(x, y, must_contain):
    rook = Turm(Color.WHITE, x, y, [])
    moves = squares(rook)
    assert len(moves) == 14
    assert must_contain <= moves


@pytest.mark.parametrize(
    "x,y,count,must_contain",
    [
        # (3,4) / (4,3) are middle squares: they catch a ray that skips
        pytest.param(0, 7, 7, {(7, 0), (3, 4)}, id="a1_corner"),
        pytest.param(7, 0, 7, {(0, 7), (4, 3)}, id="h8_corner"),
        pytest.param(0, 4, 7, {(4, 0), (3, 7)}, id="a4_edge"),
        pytest.param(4, 4, 13, {(7, 7), (0, 0), (1, 7), (7, 1)}, id="e4_centre"),
    ],
)
def test_laeufer_moves(x, y, count, must_contain):
    bishop = Laeufer(Color.WHITE, x, y, [])
    moves = squares(bishop)
    assert len(moves) == count
    assert must_contain <= moves


@pytest.mark.parametrize(
    "x,y,count",
    [
        pytest.param(0, 7, 21, id="a1_corner"),
        pytest.param(7, 0, 21, id="h8_corner"),
        pytest.param(0, 4, 21, id="a4_edge"),
        pytest.param(4, 4, 27, id="e4_centre"),
    ],
)
def test_dame_move_count(x, y, count):
    assert len(squares(Dame(Color.WHITE, x, y, []))) == count


@pytest.mark.parametrize("x,y", SAMPLE_SQUARES)
def test_dame_is_turm_plus_laeufer(x, y):
    """The queen's spec is literally the union of the other two sliders."""
    queen = squares(Dame(Color.WHITE, x, y, []))
    rook = squares(Turm(Color.WHITE, x, y, []))
    bishop = squares(Laeufer(Color.WHITE, x, y, []))
    assert queen == rook | bishop


# --------------------------------------------------------------------------
# pawns: direction depends on colour, double step on extended_moves()
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "color,x,y,expected",
    [
        # white advances toward y=0, black toward y=7
        pytest.param(Color.WHITE, 4, 6, {(4, 5), (3, 5), (5, 5), (4, 4)}, id="white_e2"),
        pytest.param(Color.BLACK, 4, 1, {(4, 2), (3, 2), (5, 2), (4, 3)}, id="black_e7"),
        # on the a-file one diagonal falls off the board
        pytest.param(Color.WHITE, 0, 6, {(0, 5), (1, 5), (0, 4)}, id="white_a2_edge"),
        pytest.param(Color.BLACK, 7, 1, {(7, 2), (6, 2), (7, 3)}, id="black_h7_edge"),
    ],
)
def test_bauer_possible_moves(color, x, y, expected):
    """Both diagonals are always present: occupancy is filtered downstream."""
    assert squares(Bauer(color, x, y, [])) == expected


@pytest.mark.parametrize(
    "color,x,y,double_step",
    [
        pytest.param(Color.WHITE, 4, 6, (4, 4), id="white_e2_e4"),
        pytest.param(Color.BLACK, 4, 1, (4, 3), id="black_e7_e5"),
    ],
)
def test_bauer_double_step_only_while_unmoved(color, x, y, double_step):
    pawn = Bauer(color, x, y, [])

    assert pawn.moved is False
    extended = {(m.x, m.y) for m in pawn.extended_moves()}
    assert extended == squares(pawn) | {double_step}

    pawn.moved = True
    assert {(m.x, m.y) for m in pawn.extended_moves()} == squares(pawn)


@pytest.mark.parametrize(
    "color,x,y",
    [
        pytest.param(Color.WHITE, 4, 0, id="white_on_rank8"),
        pytest.param(Color.BLACK, 4, 7, id="black_on_rank1"),
    ],
)
def test_bauer_on_promotion_rank_has_no_moves(color, x, y):
    """A pawn that reached the far rank can only promote, never step again."""
    assert squares(Bauer(color, x, y, [])) == set()



def test_bauer_no_double_step_off_home_rank():
    pawn = Bauer(Color.WHITE, 4, 4, [])  # white pawn on e4, never flagged
    assert (4, 2) not in {(m.x, m.y) for m in pawn.extended_moves()}


# --------------------------------------------------------------------------
# invariants that hold for every piece on every square
# --------------------------------------------------------------------------


@pytest.mark.parametrize("piece_cls", ALL_PIECES, ids=lambda c: c.__name__)
@pytest.mark.parametrize("x,y", SAMPLE_SQUARES)
def test_moves_stay_on_the_board(piece_cls, x, y):
    for mx, my in squares(piece_cls(Color.WHITE, x, y, [])):
        assert 0 <= mx <= 7 and 0 <= my <= 7


@pytest.mark.parametrize("piece_cls", ALL_PIECES, ids=lambda c: c.__name__)
@pytest.mark.parametrize("x,y", SAMPLE_SQUARES)
def test_own_square_is_not_a_move(piece_cls, x, y):
    assert (x, y) not in squares(piece_cls(Color.WHITE, x, y, []))


@pytest.mark.parametrize("piece_cls", ALL_PIECES, ids=lambda c: c.__name__)
@pytest.mark.parametrize("x,y", SAMPLE_SQUARES)
def test_no_duplicate_squares(piece_cls, x, y):
    piece = piece_cls(Color.WHITE, x, y, [])
    moves = piece.possible_moves()
    assert len(moves) == len(squares(piece))
