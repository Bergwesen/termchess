from .pieces import (
    Position,
    Bauer,
    Koenig,
    Color,
    Turm,
    Dame,
    Laeufer,
    Pferd,
    color_inverse,
)
from .pieces import Figure
from .board import Board
from .inputs import m_type, piece_selection
from enum import Enum
from dataclasses import dataclass
import copy

BLACK_KING_Y = 0
BLACK_KING_X = 4
WHITE_KING_Y = 7
WHITE_KING_X = 4

PROMOTION_BLACK = 7
PROMOTION_WHITE = 0

BLACK_JUMP_FROM = 1
WHITE_JUMP_FROM = 6


WHITE_TOWER_QUEEN = Position(x=0, y=7)
WHITE_TOWER_KING = Position(x=7, y=7)
BLACK_TOWER_QUEEN = Position(x=0, y=0)
BLACK_TOWER_KING = Position(x=7, y=0)


class PromotionError(Exception):
    pass


class WrongKingCount(Exception):
    pass


class CheckMissingCase(Exception):
    pass


class InvalidSquare(Exception):
    pass


class WrongCheckBreak(Exception):
    pass


class NotaKing(Exception):
    pass


class NoKingFound(Exception):
    pass


class failedInvariant(Exception):
    pass

class Logicleak(Exception):
    pass

class Dir(Enum):
    DIAGONAL = 0
    STRAIGHT = 1
    BOTH = 2


@dataclass
class Move:
    s_position: Position
    e_position: Position
    notes: list[m_type]


class Square_status(Enum):
    OPPONENT_SQUARE = 0
    MY_SQUARE = 1
    NO_PIECE = -1


def inboundary(position: Position) -> bool:
    if not (position.x >= 0 and position.x <= 7):
        return False
    if not (position.y >= 0 and position.y <= 7):
        return False
    return True


def king_range(square: Position) -> list[Position]:
    res_list = []
    for y in range(square.y - 1, square.y + 2):
        for x in range(square.x - 1, square.x + 2):
            if y == square.y and x == square.x:
                continue
            if inboundary(Position(x=x, y=y)):
                res_list.append(Position(x=x, y=y))
    return res_list


def in_check(board: Board, color: Color) -> bool:
    for y in range(8):
        for x in range(8):
            current_pos = Position(x=x, y=y)
            if not (board.at(current_pos) is None):
                if square_status(
                    board, current_pos, color
                ) == Square_status.MY_SQUARE and isinstance(
                    board.at(current_pos), Koenig
                ):
                    opposite_color = (
                        Color.WHITE if color == Color.BLACK else Color.BLACK
                    )
                    return is_attacked(board, current_pos, opposite_color)

    raise NoKingFound("The board doesnt contain a King of the given color")


def is_attacked(board: Board, square: Position, by: Color) -> bool:
    """This function returns True if the square is attacked by the given color"""
    # diagnoals

    directions = [
        Position(x=1, y=1),
        Position(x=1, y=-1),
        Position(x=-1, y=-1),
        Position(x=-1, y=1),
    ]
    for dir in directions:
        starting_point = square + dir
        while inboundary(starting_point):
            if square_status(board, starting_point, by) == Square_status.MY_SQUARE:
                if isinstance(board.at(starting_point), Laeufer) or isinstance(
                    board.at(starting_point), Dame
                ):
                    return True
                else:
                    break

            elif not (
                square_status(board, starting_point, by) == Square_status.NO_PIECE
            ):
                break
            starting_point = starting_point + dir

    directions = [
        Position(x=0, y=1),
        Position(x=0, y=-1),
        Position(x=-1, y=0),
        Position(x=1, y=0),
    ]
    for dir in directions:
        starting_point = square + dir
        while inboundary(starting_point):
            if square_status(board, starting_point, by) == Square_status.MY_SQUARE:
                if isinstance(board.at(starting_point), Turm) or isinstance(
                    board.at(starting_point), Dame
                ):
                    return True
                else:
                    break

            elif not (
                square_status(board, starting_point, by) == Square_status.NO_PIECE
            ):
                break
            starting_point = starting_point + dir

    directions = [
        Position(x=square.x - 1, y=square.y + 2),
        Position(x=square.x + 1, y=square.y + 2),
        Position(x=square.x - 1, y=square.y - 2),
        Position(x=square.x + 1, y=square.y - 2),
        Position(x=square.x + 2, y=square.y + 1),
        Position(x=square.x + 2, y=square.y - 1),
        Position(x=square.x - 2, y=square.y + 1),
        Position(x=square.x - 2, y=square.y - 1),
    ]
    for dir in directions:
        if inboundary(dir):
            if square_status(board, dir, by) == Square_status.MY_SQUARE:
                if isinstance(board.at(dir), Pferd):
                    return True

    if by == Color.WHITE:
        offset = 1
    else:
        offset = -1
    directions = [
        Position(x=square.x - 1, y=square.y + offset),
        Position(x=square.x + 1, y=square.y + offset),
    ]
    for dir in directions:
        if inboundary(dir):
            if square_status(board, dir, by) == Square_status.MY_SQUARE:
                if isinstance(board.at(dir), Bauer):
                    return True

    enemy_king_attack = king_range(square=square)
    for x in enemy_king_attack:
        if not (board.at(x) is None):
            if square_status(board, x, by) == Square_status.MY_SQUARE and isinstance(
                board.at(x), Koenig
            ):
                return True
    return False




def square_status(board: Board, square: Position, color: Color) -> Square_status:
    """ " This function assumes that the color of the Board is the color of the current player."""
    #print("square status call")
    opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
    square_piece = board.at(square)
    if square_piece is None:
        return Square_status.NO_PIECE
    elif square_piece.color == color:
        return Square_status.MY_SQUARE
    elif square_piece.color == opponent_color:
        return Square_status.OPPONENT_SQUARE
    else:
        raise InvalidSquare


def is_blocked(board: Board, s_pos: Position, e_pos: Position) -> bool:
    """This function  checks that the  squares between the start and end position are free. For pieces where this doesnt make sense the output is false"""
    piece = board.at(s_pos)
    passed = False
    if piece is None:
        return False

    if isinstance(piece, Turm):
        direction = Dir.STRAIGHT
    elif isinstance(piece, Laeufer):
        direction = Dir.DIAGONAL
    elif isinstance(piece, Dame):
        dx = piece.x - e_pos.x
        dy = piece.y - e_pos.y
        if dx == 0 or dy == 0 :
            direction = Dir.STRAIGHT
        elif (abs(dx) - abs(dy)) == 0:
            direction = Dir.DIAGONAL
        else : 
            raise failedInvariant()
    elif isinstance(piece, Pferd):
        return False
    elif isinstance(piece, Bauer):
        if abs(s_pos.y - e_pos.y) == 2 :
            if piece.color == Color.WHITE :
                    if square_status(board=board,square=(Position(x=s_pos.x,y=s_pos.y-1)),color=piece.color) != Square_status.NO_PIECE:
                        return True
            else :
                    if square_status(board=board,square=(Position(x=s_pos.x,y=s_pos.y+1)),color=piece.color) != Square_status.NO_PIECE:
                        return True
        return False
    elif isinstance(piece, Koenig):
        return False
    else:
        raise failedInvariant()

    if direction == Dir.DIAGONAL or direction == Dir.BOTH:
        up_left = Position(x=-1, y=1)
        up_right = Position(x=1, y=1)
        down_right = Position(x=1, y=-1)
        down_left = Position(x=-1, y=-1)

        if e_pos.x - s_pos.x < 0 and e_pos.y - s_pos.y < 0:
            chosen_dir = down_left
        elif e_pos.x - s_pos.x > 0 and e_pos.y - s_pos.y < 0:
            chosen_dir = down_right
        elif e_pos.x - s_pos.x > 0 and e_pos.y - s_pos.y > 0:
            chosen_dir = up_right
        elif e_pos.x - s_pos.x < 0 and e_pos.y - s_pos.y > 0:
            chosen_dir = up_left
        else:
            raise failedInvariant("These case should have been caught earlier")

        starting_point = s_pos + chosen_dir
        starting_color = board.at(s_pos).color

        while inboundary(starting_point) and starting_point != e_pos:
            if (
                square_status(board, starting_point, starting_color)
                != Square_status.NO_PIECE
            ):

                return True

            starting_point = starting_point + chosen_dir

    if direction == Dir.STRAIGHT or direction == Dir.BOTH:
        left = Position(x=-1, y=0)
        right = Position(x=1, y=0)
        up = Position(x=0, y=1)
        down = Position(x=0, y=-1)

        if e_pos.x > s_pos.x:
            chosen_dir = right
        elif e_pos.x < s_pos.x:
            chosen_dir = left
        elif e_pos.y < s_pos.y:
            chosen_dir = down
        elif e_pos.y > s_pos.y:
            chosen_dir = up
        else:
            raise failedInvariant("These case should have been caught earlier")
        starting_point = s_pos + chosen_dir
        starting_color = board.at(s_pos).color
        while inboundary(starting_point) and starting_point != e_pos:
            if (
                square_status(board, starting_point, starting_color)
                != Square_status.NO_PIECE
            ):
                return True
            starting_point = starting_point + chosen_dir

    return False


def move_classification(board: Board, s_pos: Position, e_pos: Position) -> list[m_type]:
    """ " By classifying the move , debugging becomes easier and the code more readabel"""

    m_types: list[m_type] = []
    if square_status(board, e_pos, board.color) == Square_status.NO_PIECE:
        if isinstance(board.at(s_pos), Bauer):
            m_types.append(m_type.PAWN_MOVE)
            if board.color == Color.BLACK:
                if e_pos.y == PROMOTION_BLACK:
                    m_types.append(m_type.PROMOTION)
            elif board.color == Color.WHITE:
                if e_pos.y == PROMOTION_WHITE:
                    m_types.append(m_type.PROMOTION)
        elif isinstance(board.at(s_pos), Koenig):
            if board.color == Color.WHITE:
                if s_pos.x == WHITE_KING_X and s_pos.y == WHITE_KING_Y:
                    if e_pos.y == s_pos.y and e_pos.x == s_pos.x - 2:
                        m_types.append(m_type.CASTLE_QUEEN)
                    elif e_pos.y == s_pos.y and e_pos.x == s_pos.x + 2:
                        m_types.append(m_type.CASTLE_KING)
                    else:
                        m_types.append(m_type.PIECE_MOVE)

                else:
                    m_types.append(m_type.PIECE_MOVE)
            elif board.color == Color.BLACK:
                if s_pos.x == BLACK_KING_X and s_pos.y == BLACK_KING_Y:
                    if e_pos.y == s_pos.y and e_pos.x == s_pos.x - 2:
                        m_types.append(m_type.CASTLE_QUEEN)
                    elif e_pos.y == s_pos.y and e_pos.x == s_pos.x + 2:
                        m_types.append(m_type.CASTLE_KING)
                    else:
                        m_types.append(m_type.PIECE_MOVE)
                else:
                    m_types.append(m_type.PIECE_MOVE)
        else:
            m_types.append(m_type.PIECE_MOVE)

    elif square_status(board, e_pos, board.color) == Square_status.OPPONENT_SQUARE:
        m_types.append(m_type.CAPTURE)
        if isinstance(board.at(s_pos), Bauer):
            if board.color == Color.BLACK:
                if e_pos.y == PROMOTION_BLACK:
                    m_types.append(m_type.PROMOTION)
            elif board.color == Color.WHITE:
                if e_pos.y == PROMOTION_WHITE:
                    m_types.append(m_type.PROMOTION)
    elif square_status(board, e_pos, board.color) == Square_status.MY_SQUARE:
        return [m_type.INVALID_MOVE]

    # for the SAN PARSER IT WOULD BE HELPFUL TOO ADD CHECK OR CHECKMATE classification

    return m_types

def create_promotion_figure(notes:list[m_type],pawn:Bauer,new_position:Position) -> Figure:
    if m_type.PROMOTION_ROCK in notes :
        piece_type = Turm(color=pawn.color,x=new_position.x,y=new_position.y,move_list=[])
    elif m_type.PROMOTION_BISHOP in notes :
        piece_type = Laeufer(color=pawn.color,x=new_position.x,y=new_position.y,move_list=[])
    elif m_type.PROMOTION_KNIGHT in notes :
        piece_type = Pferd(color=pawn.color,x=new_position.x,y=new_position.y,move_list=[])
    elif m_type.PROMOTION_QUENN in notes :
        piece_type = Dame(color=pawn.color,x=new_position.x,y=new_position.y,move_list=[])
    else :
        raise Logicleak("Shouldnt happen because m_type.PROMOTION_X is assured to be in the notes by other functions")

    return piece_type

def apply_move(board: Board, move: Move) -> Board:
    """apply_move is used in two cases: to create the next validated Board
    and to create the temporary Board for the check test. It also has to
    handle certain specific moves and make sure to give the subsequent
    Board the necessary information.
    """
    #print(f"current color {board.color} and round {board.round}")
    move_case = move.notes
    king = board.find_king(board.color)
    netxt_board = copy.deepcopy(board.board_list)

    e_position = move.e_position
    s_position = move.s_position
    en_passant = None

    if board.color == Color.BLACK:
        next_full_move_counter = board.full_move_counter + 1
    else:
        next_full_move_counter = board.full_move_counter

    if any(
        full_move in [m_type.PAWN_MOVE, m_type.CAPTURE, m_type.EN_PASSANT]
        for full_move in move_case
    ):
        next_half_move = 0
    else:
        next_half_move = board.half_move_counter + 1

    if m_type.CASTLE_KING in move_case:
        king_s = Position(x=4, y=king.y)
        king_e = Position(x=6, y=king.y)
        tower_s = Position(x=7, y=king.y)
        tower_e = Position(x=5, y=king.y)

        netxt_board = piece_move(
            netxt_board=netxt_board, s_position=king_s, e_position=king_e
        )
        netxt_board = piece_move(
            netxt_board=netxt_board, s_position=tower_s, e_position=tower_e
        )

    elif m_type.CASTLE_QUEEN in move_case:
        king_s = Position(x=4, y=king.y)
        king_e = Position(x=2, y=king.y)
        tower_s = Position(x=0, y=king.y)
        tower_e = Position(x=3, y=king.y)

        netxt_board = piece_move(
            netxt_board=netxt_board, s_position=king_s, e_position=king_e
        )
        netxt_board = piece_move(
            netxt_board=netxt_board, s_position=tower_s, e_position=tower_e
        )



    elif m_type.EN_PASSANT in move_case:
        if board.color == Color.WHITE:
            netxt_board[e_position.y + 1][e_position.x] = None
            netxt_board = piece_move(
                netxt_board=netxt_board, s_position=s_position, e_position=e_position
            )
        else:
            netxt_board = piece_move(
                netxt_board=netxt_board, s_position=s_position, e_position=e_position
            )
            netxt_board[e_position.y - 1][e_position.x] = None

    elif m_type.PROMOTION in move_case:
        pawn = board.at(s_position)
        netxt_board[e_position.y][e_position.x] = create_promotion_figure(move_case,pawn,e_position)
        netxt_board[s_position.y][s_position.x] = None


   
    else:
        netxt_board = piece_move(
            netxt_board=netxt_board, s_position=s_position, e_position=e_position
        )
     
    if m_type.EN_PASSANT_MOVE in move_case :
        en_passant = [Position(x=e_position.x, y=(s_position.y + e_position.y) // 2)]

    castle_rights  = [board.w_q_castle,board.w_k_castle,board.b_q_castle,board.b_k_castle]
    moved_piece = board.at(s_position)
    if isinstance(moved_piece,Koenig):
        if moved_piece.color == Color.WHITE:
            castle_rights[0] = False
            castle_rights[1] = False
        else :
            castle_rights[2] = False
            castle_rights[3] = False

    for sq, idx in ((Position(x=0, y=WHITE_KING_Y), 0), (Position(x=7, y=WHITE_KING_Y), 1),
                (Position(x=0, y=BLACK_KING_Y), 2), (Position(x=7, y=BLACK_KING_Y), 3)):
        if s_position == sq or e_position == sq:
            castle_rights[idx] = False
    

    


    return Board(
        board_list=netxt_board,
        runde=board.round + 1,
        color=color_inverse(board.color),
        en_passant=en_passant,
        half_move_counter=next_half_move,
        full_move_counter=next_full_move_counter,
        castle_right=castle_rights
    )


def post_check_invariant(board: Board, move: Move, king_square: Position) -> Move|m_type:
    """This function checks that we do not check ourself with the move, which would be an invalid move, this function therefore detects pins"""
    post_board = apply_move(board=board, move=move)
    king_square = post_board.find_king(board.color)
    if is_attacked(
        board=post_board, square=king_square, by=color_inverse(board.color)
    ):
        return m_type.INVALID_MOVE
    return move

def one_move_open(board:Board,for_player:Color) -> bool :
    for x in range(8):
        for y in range(8):
            current_square = board.at(Position(x=x,y=y))
            if current_square != None:
                if current_square.color == for_player:
                    #print("found " + str(current_square) + str(current_square.x) + str(current_square.y) + str(current_square.color))
                    for move_choice  in current_square.possible_moves():
                        #print("asdf " + str(move_choice))
                        if move(board=board,s_pos=Position(x=current_square.x,y=current_square.y),e_pos=move_choice) != m_type.INVALID_MOVE:
                            return True

    return False

def is_stalemate(board:Board,by:Color) -> bool :
    if is_attacked(board=board,square=board.find_king(Color.WHITE),by=Color.BLACK) or is_attacked(board=board,square=board.find_king(Color.BLACK),by=Color.WHITE):
        return False
    original_color = board.color
    player_to_move = color_inverse(by)
    try:
        board.color = player_to_move
        return not one_move_open(board=board, for_player=player_to_move)
    finally:
        board.color = original_color

def is_checkmate(board:Board,by:Color) -> bool: 
    original_color = board.color
    player_to_move = color_inverse(by)
    try:
        board.color = player_to_move
        return (
            is_attacked(
                board=board,
                square=board.find_king(player_to_move),
                by=by,
            )
            and not one_move_open(board=board, for_player=player_to_move)
        )
    finally:
        board.color = original_color
    #return     True if one_move_open(board=board,for_player=color_inverse(color=by))  ==  False  and is_attacked(board=board,square=board.find_king(color_inverse(by)),by=by) == True else  False




def move(board: Board, s_pos: Position, e_pos: Position,promotion_figure:str|None = None) -> Move | m_type:
    """
    This should be  a pure function, we are not changing or touching the state of the  board.
    move() only does the validation and creation of the move object, to store the  move and its information.

    Only Stuff that has to be validated :
    - Player ends a check state
    - Castle
    - En passant

    """
    # invariants
    for k in range(8):
        if isinstance(board.board_list[7][k], Bauer):
            raise PromotionError
        if isinstance(board.board_list[0][k], Bauer):
            raise PromotionError
    king_count_b = 0
    king_count_w = 0
    king_w_position = None
    king_b_position = None
    for x in range(8):
        for y in range(8):
            square = board.at(Position(x=x, y=y))
            if isinstance(square, Koenig):
                if square.color == Color.BLACK:
                    king_b_position = Position(x=x, y=y)
                elif square.color == Color.WHITE:
                    king_w_position = Position(x=x, y=y)

    if king_w_position is None or king_b_position is None:
        raise WrongKingCount

    # Piece exists
    if square_status(board, s_pos, board.color) == Square_status.OPPONENT_SQUARE:
        #print("This is not your square")
        return m_type.INVALID_MOVE
    elif square_status(board, s_pos, board.color) == Square_status.NO_PIECE:
        #print("There is  no piece on that square")
        return m_type.INVALID_MOVE

    # pseude legal move check
    temp_square = board.at(s_pos)
    #print(f"                                                    Pass : {temp_square} Piece exists")
    if temp_square is None:
        return m_type.INVALID_MOVE

    if isinstance(temp_square, Bauer) or isinstance(temp_square,Koenig):
        if not (e_pos in temp_square.extended_moves()):
            #print("This piece cant move like this")
            #print(board.at(s_pos).possible_moves())
            return m_type.INVALID_MOVE
    else:
        if not (e_pos in temp_square.possible_moves()):
            #print("This piece cant move like this")
            #print(board.at(s_pos).possible_moves())
            return m_type.INVALID_MOVE

    #print("Pass : its a legal move")

    # Now the possible move type
    opposite_color = color_inverse(board.color)
    m_types = move_classification(board, s_pos, e_pos)
    #print("MOOOOOVE TYPE  " + str(m_types))
    if m_type.INVALID_MOVE in m_types:
        return m_type.INVALID_MOVE
    move_return_flag = True
    if m_type.PROMOTION in m_types:
        promoted_piece = piece_selection(promotion_figure)  
        notes_with_promotion = [m_type.PROMOTION,promoted_piece]
        if not move_return_flag:
            raise Logicleak()
        move_return = post_check_invariant(board=board,move=Move(s_position=s_pos, e_position=e_pos, notes=notes_with_promotion),king_square=board.find_king(color=board.color))
        move_return_flag = False
    elif m_type.CAPTURE in m_types:
        if is_blocked(board, s_pos, e_pos):
            return m_type.INVALID_MOVE
        if (isinstance(temp_square,Bauer)):
            if (abs(s_pos.x - e_pos.x)) != 1 :
                return m_type.INVALID_MOVE
        if isinstance(temp_square,Koenig):
            if is_attacked(board,e_pos,opposite_color):
                return m_type.INVALID_MOVE
        if square_status(board, e_pos, board.color) != Square_status.OPPONENT_SQUARE:
            return m_type.INVALID_MOVE
        else:
            if not move_return_flag:
                raise Logicleak()
            move_return = post_check_invariant( board=board, move=Move(s_position=s_pos, e_position=e_pos, notes=[m_type.CAPTURE]), king_square=board.find_king(color=board.color))
            #return Move(s_position=s_pos, e_position=e_pos, notes=[m_type.CAPTURE])
            move_return_flag = False

    elif m_type.PAWN_MOVE in m_types:
        move_return = None
        if is_blocked(board, s_pos, e_pos):
            return m_type.INVALID_MOVE
        if square_status(
            board, e_pos, board.color
        ) != Square_status.NO_PIECE or not isinstance(board.at(s_pos), Bauer):
            return m_type.INVALID_MOVE
        else:
            if board.color == Color.BLACK:
                if s_pos.y == BLACK_JUMP_FROM and abs(s_pos.y - e_pos.y) == 2:
                    if e_pos in board.at(s_pos).possible_moves():
                        if (abs(e_pos.x - s_pos.x) == 1):
                            return m_type.INVALID_MOVE
                        if not move_return_flag:
                            raise Logicleak()
                        move_return = post_check_invariant(board=board,move=Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE,m_type.EN_PASSANT_MOVE]) ,king_square=board.find_king(color=board.color))
                        #return Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE])
                        move_return_flag = False
                    else:
                        return m_type.INVALID_MOVE
                elif ( (e_pos.y - s_pos.y) == 1 and abs(e_pos.x - s_pos.x) == 1):
                    if (square_status(board=board,square=Position(x=e_pos.x,y=s_pos.y),color=temp_square.color) != Square_status.OPPONENT_SQUARE):
                        return m_type.INVALID_MOVE
                    if board.en_passant is None :
                        return m_type.INVALID_MOVE
                    else :

                        if not (e_pos  in board.en_passant):
                            return m_type.INVALID_MOVE

                    if e_pos in board.at(s_pos).possible_moves():
                        if not move_return_flag:
                            raise Logicleak()
                        move_return = post_check_invariant(board=board,move=Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE,m_type.EN_PASSANT]) ,king_square=board.find_king(color=board.color))
                        #return Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE])
                        move_return_flag = False
                    else:
                        return m_type.INVALID_MOVE
            elif board.color == Color.WHITE:
                if s_pos.y == WHITE_JUMP_FROM and abs(s_pos.y - e_pos.y) == 2:
                    if e_pos in board.at(s_pos).possible_moves():
                        if (abs(e_pos.x - s_pos.x) == 1):
                            return m_type.INVALID_MOVE
                        if not move_return_flag:
                            raise Logicleak()
                        move_return = post_check_invariant(board=board,move=Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE,m_type.EN_PASSANT_MOVE]),king_square=board.find_king(color=board.color))
                        move_return_flag = False

                        #return Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE])
                    else:
                        return m_type.INVALID_MOVE
                elif ((e_pos.y - s_pos.y) == -1 and abs(e_pos.x - s_pos.x) == 1):
                    if (square_status(board=board,square=Position(x=e_pos.x,y=s_pos.y),color=temp_square.color) != Square_status.OPPONENT_SQUARE):
                        return m_type.INVALID_MOVE
                    if board.en_passant is None :
                        return m_type.INVALID_MOVE
                    else :

                        if not (e_pos  in board.en_passant):
                            return m_type.INVALID_MOVE

                    if e_pos in board.at(s_pos).possible_moves():
 
                        if not move_return_flag:
                            raise Logicleak()
                        move_return = post_check_invariant(board=board,move=Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE,m_type.EN_PASSANT]) ,king_square=board.find_king(color=board.color))
                        #return Move( s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE])
                        move_return_flag = False
                    else:
                        return m_type.INVALID_MOVE
         
            if move_return is None :
                move_return = post_check_invariant(board=board,move=Move(s_position=s_pos, e_position=e_pos, notes=[m_type.PAWN_MOVE]),king_square=board.find_king(color=board.color))
            #return move_return

    elif m_type.PIECE_MOVE in m_types:
        if is_blocked(board, s_pos, e_pos):
            return m_type.INVALID_MOVE

        if isinstance(board.at(s_pos),Koenig):
            if is_attacked(board=board,square=e_pos,by=color_inverse(board.at(s_pos).color)):
                return m_type.INVALID_MOVE

        if square_status(
            board, e_pos, board.color
        ) != Square_status.NO_PIECE or isinstance(board.at(s_pos), Bauer):
            return m_type.INVALID_MOVE
        else:
            if not move_return_flag:
                raise Logicleak()
            move_return = post_check_invariant(board=board,move=Move(s_position=s_pos, e_position=e_pos, notes=[m_type.PIECE_MOVE]) ,king_square=board.find_king(color=board.color))
            move_return_flag = False
            #return Move(s_position=s_pos, e_position=e_pos, notes=[m_type.PIECE_MOVE])
    elif m_type.CASTLE_KING in m_types:
        if is_attacked(board,s_pos,color_inverse(board.color)):
            return m_type.INVALID_MOVE

        if board.color == Color.BLACK:
            if board.b_k_castle== False :
                return m_type.INVALID_MOVE
            matching_y = BLACK_KING_Y
            matching_x = BLACK_KING_X
        elif board.color == Color.WHITE:
            if board.w_k_castle== False :
                return m_type.INVALID_MOVE
            matching_y = WHITE_KING_Y
            matching_x = WHITE_KING_X

        for x in [
            Position(x=matching_x + 1, y=matching_y),
            Position(x=matching_x + 2, y=matching_y),
        ]:
            if square_status(
                board, x, board.color
            ) != Square_status.NO_PIECE or is_attacked(board, x, opposite_color):
                return m_type.INVALID_MOVE

        if isinstance(board.at(s_pos), Koenig):
            if (
                s_pos.y == matching_y
                and s_pos.x == matching_x
                and e_pos.y == matching_y
                and e_pos.x == s_pos.x + 2
            ):  # cant be unbopunded because board.color is either white or black

                if not move_return_flag:
                    raise Logicleak()
                move_return = post_check_invariant(board=board,move=Move( s_position=s_pos, e_position=e_pos, notes=[m_type.CASTLE_KING]) ,king_square=board.find_king(color=board.color))
                move_return_flag = False

                #return Move( s_position=s_pos, e_position=e_pos, notes=[m_type.CASTLE_KING])
            #return m_type.INVALID_MOVE

    elif m_type.CASTLE_QUEEN in m_types:
        if is_attacked(board,s_pos,color_inverse(board.color)):
            return m_type.INVALID_MOVE
        if board.color == Color.BLACK:
            if board.b_q_castle == False :
                return m_type.INVALID_MOVE
            matching_y = BLACK_KING_Y
            matching_x = BLACK_KING_X
        elif board.color == Color.WHITE:
            if board.w_q_castle== False :
                return m_type.INVALID_MOVE
            matching_y = WHITE_KING_Y
            matching_x = WHITE_KING_X

        for x in [
            Position(x=matching_x - 1, y=matching_y),
            Position(x=matching_x - 2, y=matching_y),
        ]:
            if square_status(
                board, x, board.color
            ) != Square_status.NO_PIECE or is_attacked(board, x, opposite_color):
                return m_type.INVALID_MOVE

        if square_status(board,Position(x=matching_x - 3, y=matching_y),board.color) != Square_status.NO_PIECE :
            return m_type.INVALID_MOVE

        if isinstance(board.at(s_pos), Koenig):
            if (
                s_pos.y == matching_y
                and s_pos.x == matching_x
                and e_pos.y == matching_y
                and e_pos.x == s_pos.x-2
            ):  # cant be unbopunded because board.color is either white or black
                    if not move_return_flag:
                        raise Logicleak()
                    move_return = post_check_invariant(board=board,move=Move( s_position=s_pos, e_position=e_pos, notes=[m_type.CASTLE_QUEEN]),king_square=board.find_king(color=board.color))
                    move_return_flag = False

                    #return Move( s_position=s_pos, e_position=e_pos, notes=[m_type.CASTLE_KING])
            #return m_type.INVALID_MOVE
    
    if is_checkmate(board=board,by=board.color):
        if isinstance(move_return,Move):
            move_return.notes.append(m_type.CHECKMATE)
        else :
            raise Logicleak()
    #if is_stalemate(board=board,by=board.color):
    #    if isinstance(move_return,Move):
    #        move_return.notes.append(m_type.STALE_MATE)
    #    else :
    #        raise Logicleak()

    return move_return


def piece_move(
    netxt_board: list[list[Figure | None]], s_position: Position, e_position: Position
):
    netxt_board[e_position.y][e_position.x] = netxt_board[s_position.y][s_position.x]
    netxt_board[s_position.y][s_position.x] = None
    netxt_board[e_position.y][e_position.x].moved = True
    netxt_board[e_position.y][e_position.x].y = e_position.y
    netxt_board[e_position.y][e_position.x].x = e_position.x
    return netxt_board
