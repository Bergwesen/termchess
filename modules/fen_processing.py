from .board import Board
from .pieces import Koenig,Dame,Bauer,Turm,Laeufer,Pferd,Color,Figure,Position


class InvalidFEN(Exception):
    pass





def algebraic_notation(piece:Figure) -> str:
    letter = ""
    if isinstance(piece,Turm):
        letter = 'r' 
    if isinstance(piece,Koenig):
        letter = 'k' 
    if isinstance(piece,Dame):
        letter = 'q' 
    if isinstance(piece,Bauer):
        letter = 'p' 
    if isinstance(piece,Pferd):
        letter = 'n' 
    if isinstance(piece,Laeufer):
        letter = 'b' 
    if piece.color == Color.WHITE :
        return letter.capitalize()
    else :
        return letter

def algebraic_to_piece(notation:str,x:int,y:int) -> Figure|None:
    color = Color.BLACK if  notation.islower() else  Color.WHITE
    if notation.isnumeric():
        return None
    match notation.lower():
        case 'r' :
            piece =  Turm(color=color,x=x,y=y)
        case 'k':
            piece =  Koenig(color=color,x=x,y=y)
        case 'q':
            piece =  Dame(color=color,x=x,y=y)
        case 'p':
            piece =  Bauer(color=color,x=x,y=y)
        case 'n' :
            piece =  Pferd(color=color,x=x,y=y)
        case 'b' : 
            piece =  Laeufer(color=color,x=x,y=y)
        case _ :
            raise ValueError("Invalid call of the function notation to be r,k,q,p,n or b")
    return  piece






def fen_to_coordinate(notation: str) -> Position:
    """in a FEN the rank 8 is the row y=0"""
    if len(notation) != 2 :
        raise InvalidFEN("A FEN square has to look like e3")
    x = -1
    match notation[0]:
        case "a":
            x = 0
        case "b":
            x = 1
        case "c":
            x = 2
        case "d":
            x = 3
        case "e":
            x = 4
        case "f":
            x = 5
        case "g":
            x = 6
        case "h":
            x = 7
        case _:
            raise InvalidFEN("This value cant be processed")

    if not notation[1] in "12345678" :
        raise InvalidFEN("This value cant be processed")

    return Position(x=x, y=8 - int(notation[1]))


def coordinate_to_fen(position: Position) -> str:
    """FEN square like e3 , the row y=0 is the rank 8"""
    file_letter = ""
    match position.x:
        case 0:
            file_letter = "a"
        case 1:
            file_letter = "b"
        case 2:
            file_letter = "c"
        case 3:
            file_letter = "d"
        case 4:
            file_letter = "e"
        case 5:
            file_letter = "f"
        case 6:
            file_letter = "g"
        case 7:
            file_letter = "h"
        case _:
            raise InvalidFEN("This value cant be processed")

    if position.y < 0 or position.y > 7 :
        raise InvalidFEN("This value cant be processed")

    return file_letter + str(8 - position.y)


def fen_out(board:Board) -> str :
    output_string = []

    board_placement = []
    for y in range(8):       
        empty_square = 0
        for x in range(8):
            piece = board.at(Position(x=x,y=y))
            if not( piece is None):
                if empty_square > 0 :
                    board_placement.append(str(empty_square))
                    empty_square = 0 
                board_placement.append(algebraic_notation(piece))
            else :
                empty_square  += 1
        if empty_square > 0 :
            board_placement.append(str(empty_square))

        if y != 7 :
            board_placement.append("/")

    output_string.append(board_placement)
    player = [] 
    if board.color == Color.WHITE :
        player.append('w')
    else :
        player.append('b')
    
    castle_right = []
    if board.w_k_castle:
        castle_right.append("K")
    if board.w_q_castle:
        castle_right.append("Q")
    if board.b_k_castle:
        castle_right.append("k")
    if board.b_q_castle:
        castle_right.append("q")
    if len(castle_right) == 0 :
        castle_right.append("-")
    
    en_passant_target_square = []
    if (board.en_passant is None) or len(board.en_passant) == 0 :
        en_passant_target_square.append("-")
    else :
        en_passant_target_square.append(coordinate_to_fen(board.en_passant[0]))

    halfmove_clock = [str(board.half_move_counter)]

    fullmove_counter = [str(board.full_move_counter)]
    buffer = [" "]
    output_string = board_placement +buffer+player+ buffer + castle_right +buffer+ en_passant_target_square + buffer + halfmove_clock +buffer+ fullmove_counter
    return "".join(output_string)
    







        










               





def fen_in(fen_string:str) -> Board :
    board_list = []
    fen_parts = fen_string.split(' ')
    board_parts = fen_parts[0].split('/')
    for y,row in enumerate(board_parts):
        new_row  = []
        file = 0 
        for x,square in enumerate(row):
            if square.isnumeric():
                for c in range(int(square)):
                    new_row.append(algebraic_to_piece(square,file,y))
                    file = file + 1
            else:
                new_row.append(algebraic_to_piece(square,file,y))
                file = file  + 1 
        board_list.append(new_row)

    if fen_parts[1] == 'w' :
        board_color = Color.WHITE
    elif fen_parts[1] == 'b' :
        board_color = Color.BLACK
    else :
        raise InvalidFEN("The FEN String must contain the 'side-to-move'")
    board_castle_rights = [False,False,False,False]
    if fen_parts[2] != '-':
        for castle_case in fen_parts[2]:
            if castle_case == 'K':
                board_castle_rights[1] = True
            elif castle_case == 'Q':
                board_castle_rights[0] = True
            elif castle_case == 'k':
                board_castle_rights[3] = True
            elif castle_case == 'q':
                board_castle_rights[2] = True
            else :
                InvalidFEN("The FEN Strint for castling must be K,Q,k or q")
    board_en_passant = None
    if fen_parts[3] != '-':
        board_en_passant = [fen_to_coordinate(fen_parts[3])]


    board_half_move_counter = int(fen_parts[4])
    board_full_move_counter = int(fen_parts[5])

    return Board(board_list=board_list,runde=1,color=board_color,en_passant=board_en_passant,half_move_counter=board_half_move_counter,full_move_counter=board_full_move_counter,castle_right=board_castle_rights)








    pass
    
