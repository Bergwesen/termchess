from enum import Enum
import typing

# from .pieces import Koenig,Dame,Bauer,Turm,Pferd,Laeufer,Color,Figure,Position
from .pieces import (
    Koenig,
    Dame,
    Bauer,
    Turm,
    Pferd,
    Laeufer,
    Color,
    Figure,
    Position,
    color_inverse,
)

# from .move import Move,m_type,NoKingFound
from .inputs import m_type
from .inputs import promotion_input
import copy

BLACK_KING_BASE = Position(x=5, y=0)
WHITE_KING_BASE = Position(x=5, y=7)
WHITE_TOWER_QUEEN = Position(x=0, y=7)
WHITE_TOWER_KING = Position(x=7, y=7)
BLACK_TOWER_QUEEN = Position(x=0, y=0)
BLACK_TOWER_KING = Position(x=7, y=0)


class NoKingFound(Exception):
    pass


def square_color(pos:Position) -> Color:
    return Color.WHITE

class Board:
    def __init__(
        self,
        board_list: list[list[Figure | None]] | None,
        runde: int,
        color: Color,
        en_passant: list[Position] | None = None,
        half_move_counter: int = 0,
        full_move_counter: int = 1,
        castle_right:list[bool]|None = None
    ):
        if board_list is None:
            self.board_list = []
            for y in range(8):
                match y:
                    case 0:
                        row_color = Color.BLACK
                        self.board_list.append(
                            [
                                Turm(color=row_color, x=0, y=y, move_list=[]),
                                Pferd(color=row_color, x=1, y=y, move_list=[]),
                                Laeufer(color=row_color, x=2, y=y, move_list=[]),
                                Dame(color=row_color, x=3, y=y, move_list=[]),
                                Koenig(color=row_color, x=4, y=y, move_list=[]),
                                Laeufer(color=row_color, x=5, y=y, move_list=[]),
                                Pferd(color=row_color, x=6, y=y, move_list=[]),
                                Turm(color=row_color, x=7, y=y, move_list=[]),
                            ]
                        )

                    case 1:
                        row_color = Color.BLACK
                        self.board_list.append(
                            [
                                Bauer(color=row_color, x=x, y=y, move_list=[])
                                for x in range(8)
                            ]
                        )
                    case 6:
                        row_color = Color.WHITE
                        self.board_list.append(
                            [
                                Bauer(color=row_color, x=x, y=y, move_list=[])
                                for x in range(8)
                            ]
                        )
                    case 7:
                        row_color = Color.WHITE
                        self.board_list.append(
                            [
                                Turm(color=row_color, x=0, y=y, move_list=[]),
                                Pferd(color=row_color, x=1, y=y, move_list=[]),
                                Laeufer(color=row_color, x=2, y=y, move_list=[]),
                                Dame(color=row_color, x=3, y=y, move_list=[]),
                                Koenig(color=row_color, x=4, y=y, move_list=[]),
                                Laeufer(color=row_color, x=5, y=y, move_list=[]),
                                Pferd(color=row_color, x=6, y=y, move_list=[]),
                                Turm(color=row_color, x=7, y=y, move_list=[]),
                            ]
                        )
                    case _:
                        self.board_list.append(
                            [None, None, None, None, None, None, None, None]
                        )

        else:
            self.board_list = board_list

        self.round = runde
        self.color: Color = color
        self.en_passant = en_passant
        self.half_move_counter = half_move_counter
        self.full_move_counter = full_move_counter

        #self.white_castle_right_queen = True
        #self.black_castle_right_queen = True
        #self.white_castle_right_king = True
        #self.black_castle_right_king = True

        if castle_right is None :
            self.w_q_castle = True
            self.w_k_castle = True
            self.b_q_castle = True
            self.b_k_castle = True
        else :
            if len(castle_right) != 4 :
                raise ValueError("Always set the castle right with the function ")
            self.w_q_castle = castle_right[0]
            self.w_k_castle = castle_right[1]
            self.b_q_castle = castle_right[2]
            self.b_k_castle = castle_right[3]


   




    def castle_right_check(self) -> bool:
        """function might have to go """

        if self.color == Color.WHITE:
            king_position = WHITE_KING_BASE
            queen_side = WHITE_TOWER_QUEEN
            king_side = WHITE_TOWER_KING
        else:
            king_position = BLACK_KING_BASE
            queen_side = BLACK_TOWER_QUEEN
            king_side = BLACK_TOWER_KING

        if self.at(king_position) is None:
            return False
        board_king = self.at(king_position)
        if not isinstance(board_king, Koenig):
            return False

        if isinstance(board_king, Koenig):
            if board_king.moved == True:
                return False

        for tower in [queen_side, king_side]:
            if self.at(tower) is None:
                return False
            board_tower = self.at(king_position)
            if not isinstance(board_tower, Turm):
                return False

            if isinstance(board_tower, Turm):
                if board_tower.moved == True:
                    return False
        return True

    #def move(self, s_position, e_position) -> list[list[Figure | None]]:

    #    netxt_board = copy.deepcopy(self.board_list)
    #    print(self.board_list[s_position.y][s_position.x])
    #    print(self.board_list[e_position.y][e_position.x])
    #    print(e_position)
    #    print(s_position)
        #            self.board_list[e_position.y][e_position.x] = self.board_list[s_position.y][s_position.x]
    #    netxt_board[e_position.y][e_position.x] = netxt_board[s_position.y][
    #        s_position.x
    #    ]
    #    print(self.board_list[e_position.y][e_position.x])
    #    netxt_board[s_position.y][s_position.x] = None
    #    netxt_board[e_position.y][e_position.x].moved = True
    #    netxt_board[e_position.y][e_position.x].y = e_position.y
    #    netxt_board[e_position.y][e_position.x].x = e_position.x
    #    return netxt_board

    def at(self, pos: Position) -> Figure | None:
        return self.board_list[pos.y][pos.x]

    def set(self,pos:Position,figure:Figure):
        self.board_list[pos.y][pos.x] = figure

    def find_king(self, color: Color) -> Position:
        for x in range(8):
            for y in range(8):
                temp_position = Position(x=x, y=y)
                if not (self.at(temp_position) is None):
                    if (
                        isinstance(self.at(temp_position), Koenig)
                        and self.at(temp_position).color == color
                    ):
                        return temp_position
        raise NoKingFound("No king on the board")

    def __str__(self) -> str:

        multiline_string = ""
        for y in range(8):
            seperator = "------------------\n"
            multiline_string = multiline_string + seperator
            for x in range(8):
                #                    print( str(x) + " "  + str(y ))
                # print("|" + self.board_list[y][x],end="")
                if self.board_list[y][x] is not None:
                    multiline_string += "|" + str(self.board_list[y][x])
                else:
                    multiline_string += "|" + " "

            # print("|")
            multiline_string += "|" + str(y + 1) + "\n"
        return multiline_string


def move_loop():

    pass
