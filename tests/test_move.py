
"""
Coordinate convention (from Board.__init__): y=0 is rank 8, y=7 is rank 1.
So a1 == (0,7), a8 == (0,0), e4 == (4,4).
"""

import pytest

from modules.pieces import Bauer, Color, Dame, Koenig, Laeufer, Pferd, Turm, Position, Figure
from modules.board import Board
from modules.move import move, m_type, is_checkmate,is_stalemate

# move() refuses to run without a king of each colour. a1/h8 share no rank,
# file or diagonal with e4, so the kings never block the piece under test.
WHITE_KING = Position(x=0, y=7)
BLACK_KING = Position(x=7, y=0)


def p(x: int, y: int) -> Position:
    """Short constructor to keep the tables below readable."""
    return Position(x=x, y=y)


def board_init(
    figure_positions: list[Position],
    figure_type: list[type[Figure]],
    figure_color: list[Color],
    acting:Color|None = None
) -> Board:
    if acting is None :
        board = Board(board_list=[[None] * 8 for _ in range(8)], runde=1, color=Color.WHITE)
    else :
        board = Board(board_list=[[None] * 8 for _ in range(8)], runde=1, color=acting)
    board.set(WHITE_KING, Koenig(color=Color.WHITE, x=WHITE_KING.x, y=WHITE_KING.y, move_list=[]))
    board.set(BLACK_KING, Koenig(color=Color.BLACK, x=BLACK_KING.x, y=BLACK_KING.y, move_list=[]))
    for x in range(len(figure_positions)):
        position = figure_positions[x]
        board.set(
            position,
            figure_type[x](color=figure_color[x], x=position.x, y=position.y, move_list=[]),
        )
    return board


@pytest.mark.parametrize("slider_position,slider_type,figure_positions,figure_type,figure_color,blocked_positions",

                         [
                            # Rook on e4, own pawns on c4 / h4 / e6 / e2. Their squares are
                            # own-colour targets, everything behind them is unreachable.
                            # Free: d4, f4, g4, e5, e3.
                            pytest.param(
                                p(4, 4), Turm,
                                [p(4, 4), p(2, 4), p(7, 4), p(4, 2), p(4, 6)],
                                [Turm, Bauer, Bauer, Bauer, Bauer],
                                [Color.WHITE] * 5,
                                [
                                    p(2, 4), p(1, 4), p(0, 4),   # c4 own pawn + b4, a4 behind it
                                    p(7, 4),                     # h4 own pawn (nothing behind)
                                    p(4, 2), p(4, 1), p(4, 0),   # e6 own pawn + e7, e8 behind it
                                    p(4, 6), p(4, 7),            # e2 own pawn + e1 behind it
                                ],
                                id="rook_own_pawns",
                            ),
                            # Same four pawns, now black: each pawn square is a legal
                            # capture, only the squares behind them are blocked.
                            pytest.param(
                                p(4, 4), Turm,
                                [p(4, 4), p(2, 4), p(7, 4), p(4, 2), p(4, 6)],
                                [Turm, Bauer, Bauer, Bauer, Bauer],
                                [Color.WHITE] + [Color.BLACK] * 4,
                                [
                                    p(1, 4), p(0, 4),            # behind the c4 capture
                                    p(4, 1), p(4, 0),            # behind the e6 capture
                                    p(4, 7),                     # behind the e2 capture
                                ],
                                id="rook_enemy_pawns",
                            ),
                            # Rook walled in by its own pawns on all four sides: every one
                            # of its 14 pseudo-legal squares is blocked.
                            pytest.param(
                                p(4, 4), Turm,
                                [p(4, 4), p(3, 4), p(5, 4), p(4, 3), p(4, 5)],
                                [Turm, Bauer, Bauer, Bauer, Bauer],
                                [Color.WHITE] * 5,
                                [
                                    p(3, 4), p(2, 4), p(1, 4), p(0, 4),
                                    p(5, 4), p(6, 4), p(7, 4),
                                    p(4, 3), p(4, 2), p(4, 1), p(4, 0),
                                    p(4, 5), p(4, 6), p(4, 7),
                                ],
                                id="rook_boxed_in",
                            ),
                            # Bishop on e4. Own pawns g2 and f5 shut two diagonals
                            # down, the black pawn on c6 is capturable. The d3/c2/b1
                            # diagonal stays completely free.
                            pytest.param(
                                p(4, 4), Laeufer,
                                [p(4, 4), p(6, 6), p(5, 3), p(2, 2)],
                                [Laeufer, Bauer, Bauer, Bauer],
                                [Color.WHITE, Color.WHITE, Color.WHITE, Color.BLACK],
                                [
                                    p(6, 6), p(7, 7),            # own pawn g2 + h1 behind it
                                    p(5, 3), p(6, 2), p(7, 1),   # own pawn f5 + g6, h7 behind it
                                    p(1, 1), p(0, 0),            # behind the c6 capture
                                ],
                                id="bishop_mixed",
                            ),
                            # Queen on e4: one blocked ray per direction kind. Own pawn e5
                            # and own pawn f3 block, black c4 and black d5 are captures.
                            # Free: f4-h4, e3-e1, d3/c2/b1, f5/g6/h7.
                            pytest.param(
                                p(4, 4), Dame,
                                [p(4, 4), p(4, 3), p(5, 5), p(2, 4), p(3, 3)],
                                [Dame, Bauer, Bauer, Bauer, Bauer],
                                [Color.WHITE, Color.WHITE, Color.WHITE, Color.BLACK, Color.BLACK],
                                [
                                    p(4, 3), p(4, 2), p(4, 1), p(4, 0),   # own pawn e5 + e6-e8
                                    p(5, 5), p(6, 6), p(7, 7),            # own pawn f3 + g2, h1
                                    p(1, 4), p(0, 4),                     # behind the c4 capture
                                    p(2, 2), p(1, 1), p(0, 0),            # behind the d5 capture
                                ],

                                id="queen_mixed",
                            ),
                         ],
                         )
def test_move_slider(slider_position:Position,slider_type:type[Figure],figure_positions:list[Position],figure_type:list[type[Figure]],figure_color:list[Color],blocked_positions:list[Position]):
    """
    Alle Figuren, deren Typen und deren Farben muessen in figure_positions, figure_type und
    figure_color stehen. Mit slider_position und slider_type bestimmt man nur welche Figur
    getestest wird. Die 2 Koenige setzt board_init selbst.

    Geprueft wird nur die eine Richtung: jedes Feld in blocked_positions muss abgelehnt
    werden. Ob die uebrigen Felder erlaubt bleiben, prueft dieser Test nicht.
    """
    board = board_init(figure_positions=figure_positions,figure_type=figure_type,figure_color=figure_color)
    slider = board.at(slider_position)
    if slider == None:
        raise ValueError("Slider must point to a figure")
    assert isinstance(slider, slider_type), "slider_type does not match the board"
    board.color = slider.color  # move() reads board.color as the side to move
    for  x in slider.possible_moves():
        if  x in blocked_positions:
            assert  move(board=board,s_pos=slider_position,e_pos=x) == m_type.INVALID_MOVE, f"{x} should be blocked"



def board_init_raw(
    figure_positions: list[Position],
    figure_type: list[type[Figure]],
    figure_color: list[Color],
    acting:Color|None = None
) -> Board:
    if acting is None :
        board = Board(board_list=[[None] * 8 for _ in range(8)], runde=1, color=Color.WHITE)
    else :
        board = Board(board_list=[[None] * 8 for _ in range(8)], runde=1, color=acting)
    for x in range(len(figure_positions)):
        position = figure_positions[x]
        board.set(
            position,
            figure_type[x](color=figure_color[x], x=position.x, y=position.y, move_list=[]),
        )
    return board




@pytest.mark.parametrize("figure_positions,figure_type,figure_color,checking_color",

                         [
                            pytest.param(
                                [p(0, 1), p(0, 2), p(0, 0)],
                                [Dame, Koenig, Koenig],
                                [Color.WHITE,Color.WHITE,Color.BLACK],
                                Color.WHITE
                                ,
                                id="simple_mate",
                            ),],)
 
def test_move_checkmate(figure_positions:list[Position],figure_type:list[type[Figure]],figure_color:list[Color],checking_color:Color):
    board = board_init_raw(figure_positions=figure_positions,figure_type=figure_type,figure_color=figure_color,acting=checking_color)
    assert  is_checkmate(board=board,by=checking_color)  == True



@pytest.mark.parametrize("figure_positions,figure_type,figure_color,checking_color",

                         [
                            pytest.param(
                                [p(1, 0), p(1, 1), p(1, 2)],
                                [Koenig, Bauer, Koenig],
                                [Color.BLACK,Color.WHITE,Color.WHITE],
                                Color.WHITE
                                ,
                                id="simple_stalemate",
                            ),],)
 
def test_move_stalemate(figure_positions:list[Position],figure_type:list[type[Figure]],figure_color:list[Color],checking_color:Color):
    board = board_init_raw(figure_positions=figure_positions,figure_type=figure_type,figure_color=figure_color,acting=checking_color)
    assert  is_stalemate(board=board,by=checking_color)  == True








    
