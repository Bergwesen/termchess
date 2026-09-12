from .pieces import Position,KOENIG_LETTER,DAME_LETTER,LAEUFER_LETTER,TURM_LETTER,SPRINGER_LETTER,Figure,Dame,Koenig,Laeufer,Bauer,Turm,Pferd
import typing
from enum import Enum
import re
from .inputs import m_type,notation_to_coordinate














def piece_type(cli_input:str) -> type[Figure] :
    """ This function returns the type of a figure based of the SAN input"""
    if  "Q" in cli_input :
        return Dame
    elif "R" in cli_input:
        return Turm
    elif "K" in cli_input:
        return Koenig
    elif "N" in cli_input:
        return  Pferd
    elif "B" in cli_input:
        return  Laeufer
    else:
        return Bauer

def check_or_checkmate(cli_input:str) -> m_type|None:
    """This function returns wether or not the SAN  notation marks it as  check or checkmate or none of both"""
    if "#" in cli_input :
        return m_type.CHECKMATE
    elif "+" in cli_input:
        return m_type.CHECK
    else : 
        return None

def validate_input_san(cli_input:str) -> tuple[m_type , type[Figure] | None] | tuple[m_type , m_type ,type[Figure] | None] | None:
    """ This  function should check that the move sent via the cli  is correctly  written and then return its move type
        The following has to bee checked : 
            castle == ,check ==,checkmate ==,pawn move == 3  , piece move == 4, promotion , en passant, disambiguation,promotion with capture
    """
    


    piece_move = re.compile("[QKRBN]?[a-h]{1}[1-8]{1}")

    piece_capture = re.compile("[a-h]{1}|[QKRBN]{1}x[a-h]{1}[1-8]{1}")

    castle_queen = re.compile("0-0-0")
    castle_king = re.compile("0-0")

    check = re.compile("[QKBNR]?[a-h]{1}[1-8]{1}+")

    checkmate =  re.compile("[QKBNR]?[a-h]{1}[1-8]{1}#")

    promotion = re.compile("[a-h]{1}[1-8]{1}=[QKBNR]{1}")

    disambiguation = re.compile("[QKBNR]{1}[a-h]{1}|[1-8]{1}[a-h]{1}[1-8]{1}")
    capture_check =re.compile("[QKBRN]{1}|[a-h]{1}x[a-h]{1}[1-8]{1}+")
    capture_mate_pawn = re.compile("[a-h]{1}|[QKBRN]{1}x[a-h]{1}[1-8]{1}#")


    
    piece = piece_type(cli_input)
    if   not  (piece_move.match(cli_input) is None):
            return (m_type.PIECE_MOVE,piece)
    elif not  (piece_capture.match(cli_input) is None):
            extra_move = check_or_checkmate(cli_input)
            if extra_move is None :
                return (m_type.CAPTURE,piece)
            else :
                return (m_type.CAPTURE,extra_move,piece) 
    elif not  (castle_queen.match(cli_input) is None):
            return (m_type.CASTLE_QUEEN,None)

    elif not  (castle_king.match(cli_input) is None):
            return (m_type.CASTLE_King,None)

    elif not  (check.match(cli_input) is None):
            return (m_type.CHECK,m_type.PIECE_MOVE,piece)

    elif not  (checkmate.match(cli_input) is None):
            return (m_type.CHECKMATE,m_type.PIECE_MOVE,piece)

    elif not  (promotion.match(cli_input) is None):
        promotion_check = re.compile("*+")
        promotion_checkmate = re.compile("*#")

        if promotion_check.match(cli_input):
            return (m_type.PROMOTION,m_type.CHECK,piece)
        elif promotion_checkmate.match(cli_input): 
            return (m_type.PROMOTION,m_type.CHECKMATE,piece)
        else : 
            return (m_type.PROMOTION,piece_type(cli_input[-2:]))

    elif not  (disambiguation.match(cli_input) is None):
            return (m_type.DISAMBIGUATION,piece)
    else :
        return None

def extract_coordinates_san(cli_input:str,move_type: m_type |tuple[m_type,m_type],is_pawn:bool)-> Position:
    """Unfinished function,which allos us to derive the coordinates based on the SAN input"""
    match move_type :
        case m_type.PIECE_MOVE :
            if is_pawn :
                return notation_to_coordinate(cli_input) 
            else : 
                return notation_to_coordinate(cli_input[1:]) 
        case m_type.CAPTURE :
            return notation_to_coordinate(cli_input[1:]) 
        case _ :
            raise ValueError("this move type hasnt been implemented until now")




def free_move_input_san() -> list[Position]:

    print("Which figure do you want to move")
    pre_position = input()
    input_result = validate_input_san(pre_position)

    while  input_result is None :
        print("Which figure do you want to move")
        pre_position = input()
        input_result = validate_input_san(pre_position)    

    #move_type_one,piece_type_one =  input_result[0],input_result[1] if len(input_result) == 2 else input_result[0:2],input_result[2]

    move_type_one  = None
    piece_type_one = None
    if len(input_result) == 2 :
        move_type_one = input_result[0]
        piece_type_one= input_result[1]

    elif len(input_result) == 3 :
        move_type_one = input_result[0:2]
        piece_type_one= input_result[2]
    else :
        raise ValueError("????")





    is_pawn =  True if piece_type_one == Bauer else False
    if  input_result is  None :
        raise ValueError("Wrong input")
    else :
        pre_coords =  extract_coordinates_san(pre_position,move_type_one,is_pawn)
   

    print("Where you want to move it")
    post_position = input()
    input_result_two= validate_input_san(post_position)
    while  input_result_two is None :
        print("Where you want to move it")
        post_position = input()
        input_result_two= validate_input_san(post_position)

    
#    move_type_two =  input_result_two[0] if len(input_result_two) == 2  else input_result_two[0:2]
#    is_pawn_two = False

    move_type_two  = None
    piece_type_two = None
    if len(input_result_two) == 2 :
        move_type_two = input_result_two[0]
        piece_type_two= input_result_two[1]

    elif len(input_result_two) == 3 :
        move_type_two = input_result_two[0:2]
        piece_type_two = input_result_two[2]
    else :
        raise ValueError("????")

    is_pawn_two =  True if piece_type_two == Bauer else False



    


    if input_result_two is  None :
        raise ValueError("Wrong input")
    else :
        post_coords =  extract_coordinates_san(post_position,move_type_two,is_pawn_two)

    return  [pre_coords,post_coords]

















