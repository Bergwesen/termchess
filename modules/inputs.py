# from .pieces import Position,KOENIG_LETTER,DAME_LETTER,LAEUFER_LETTER,TURM_LETTER,SPRINGER_LETTER,Figure,Dame,Koenig,Laeufer,Bauer,Turm,Pferd
from .pieces import (
    Position,
    KOENIG_LETTER,
    DAME_LETTER,
    LAEUFER_LETTER,
    TURM_LETTER,
    SPRINGER_LETTER,
    Figure,
    Dame,
    Koenig,
    Laeufer,
    Bauer,
    Turm,
    Pferd,
    Color,
)
import typing
from enum import Enum
import re


class IncorrectInput(Exception):
    pass


class m_type(Enum):
    """This Enum class should be used for debugging purposes or the make the processing of SAN inputs faster"""

    DISAMBIGUATION = (
        -1
    )  # minus one because this should be the only move type where we would need bord knowledge to know which piece we from to which sqaure
    CHECK = 1
    CHECKMATE = 2
    PAWN_MOVE = 13
    PIECE_MOVE = 4
    PROMOTION = 5
    EN_PASSANT = 6
    CAPTURE = 9
    CASTLE_KING = 10
    CASTLE_QUEEN = 11
    INVALID_MOVE = 12
    EN_PASSANT_MOVE = 14
    STALE_MATE = 7
    PROMOTION_QUENN = 15
    PROMOTION_ROCK  = 16
    PROMOTION_BISHOP = 17
    PROMOTION_KNIGHT = 18



def notation_to_coordinate(notation: str) -> Position:
    """A general function that derives the coordiantes of a input of type  a-h1-8 or a-h or 1-8"""
    notation_len = len(notation)
    match notation_len:
        case 1:
            if notation.isalpha():
                match notation:
                    case "a":
                        return Position(x=0, y=-1)
                    case "b":
                        return Position(x=1, y=-1)
                    case "c":
                        return Position(x=2, y=-1)
                    case "d":
                        return Position(x=3, y=-1)
                    case "e":
                        return Position(x=4, y=-1)
                    case "f":
                        return Position(x=5, y=-1)
                    case "g":
                        return Position(x=6, y=-1)
                    case "h":
                        return Position(x=7, y=-1)
                    case _:
                        raise ValueError("This value cant be processed")

            else:
                match notation:
                    case "1":
                        return Position(x=-1, y=0)
                    case "2":
                        return Position(x=-1, y=1)
                    case "3":
                        return Position(x=-1, y=2)
                    case "4":
                        return Position(x=-1, y=3)
                    case "5":
                        return Position(x=-1, y=4)
                    case "6":
                        return Position(x=-1, y=5)
                    case "7":
                        return Position(x=-1, y=6)
                    case "8":
                        return Position(x=-1, y=7)
                    case _:
                        raise ValueError("This value cant be processed")
        case 2:
            x = -1
            y = -1
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
                    raise ValueError("This value cant be processed")

            match notation[1]:
                case "1":
                    y = 0
                case "2":
                    y = 1
                case "3":
                    y = 2
                case "4":
                    y = 3
                case "5":
                    y = 4
                case "6":
                    y = 5
                case "7":
                    y = 6
                case "8":
                    y = 7
                case _:
                    raise ValueError("This value cant be processed")

            return Position(x=x, y=y)

        case _:
            raise ValueError("This function should only receive a string of size 2")


def validate_input(input: str) -> bool:
    piece_move = re.compile("[a-h][1-8]")
    if piece_move.match(input) is None:
        return False
    else:
        return True

def  non_game_inputs(input:str) -> bool :
    match input.strip() :
        case "exit" :
            return True
        case "quit" :
            return True
        case "back" :
            return True
        case "forward" :
            return True
        case _ :
            return False






def input_processing(
    s_input: str | None = None, e_input: str | None = None
) -> tuple[Position, Position]:

    
    one_preset = False
    preset = False
    if isinstance(s_input,str) and e_input is None :
        one_preset = True
        raw_s_pos = s_input 
    elif isinstance(s_input, str) and isinstance(e_input, str):
        raw_s_pos = s_input
        raw_e_pos = e_input
        preset = True
    elif (s_input is None and  not (e_input is None))   :
        raise IncorrectInput(
            "To use the presetting start position and end position need to be set"
        )
    else :
        raw_s_pos = input()
        

    processable_input_one = False
    processable_input_two = False
    #if not preset or not one_preset:
    #    raw_s_pos = input()
    

    first_pass_one = validate_input(raw_s_pos)
    
    if first_pass_one:
        s_pos = notation_to_coordinate(raw_s_pos)
        processable_input_one = True
    else:
        if preset or one_preset:
            raise IncorrectInput("Preset input must be correctly formatted")

        while not processable_input_one:
            print("Welche Figure moechtest du bewegen")
            raw_s_pos = input()
            first_pass_one = validate_input(raw_s_pos)
            if first_pass_one:
                s_pos = notation_to_coordinate(raw_s_pos)
                processable_input_one = True

    print("Auf welches Feld moechteste du die Figure bewegen")
    if not preset:
        raw_e_pos = input()
    first_pass_two = validate_input(raw_e_pos)
    if first_pass_two:
        e_pos = notation_to_coordinate(raw_e_pos)
        processable_input_two = True
    else:
        if preset:
            raise IncorrectInput("Preset input must be correctly formatted")
        while not processable_input_two:
            print("Auf welches Feld moechteste du die Figure bewegen")
            raw_e_pos = input()
            first_pass_two = validate_input(raw_e_pos)
            if first_pass_two:
                e_pos = notation_to_coordinate(raw_e_pos)
                processable_input_two = True

    return s_pos, e_pos  # shouldnt be unbounded


def promotion_input(
    piece_x: int, piece_y: int, piece_color: Color
):  # should return a figure object
    pass


def free_move() -> list[Position]:
    """Allows the user to freely move pieces with a-h1-8 string inputs"""
    print("Which figure do you want to move")
    pre_position = input()
    input_result = validate_input(pre_position)

    while input_result:
        print("Which figure do you want to move")
        pre_position = input()
        input_result = validate_input(pre_position)

    pre_coords = notation_to_coordinate(pre_position)

    print("Where you want to move it")
    post_position = input()
    input_result_two = validate_input(post_position)
    while not input_result_two:
        print("Where you want to move it")
        post_position = input()
        input_result_two = validate_input(post_position)
    post_coords = notation_to_coordinate(post_position)
    return [pre_coords, post_coords]

def piece_selection(override:str|None = None) -> m_type:
    """" Parses/translates inputs into the promoted figure type"""
    valid_inputs = ["king","k","queen","q","rock","r","bishop","b","knight","k"]
    if override is None :
        line_input = input("Choose a figure").strip()    
        while not any( x in line_input for x in valid_inputs):
            line_input = input("Choose a figure").strip()
    else :
        line_input = override 
        if  line_input not in  valid_inputs :
            raise IncorrectInput(f"You must preset/use the following inputs for a promotion case {valid_inputs}")
    match line_input:
        case "queen":
            return m_type.PROMOTION_QUENN
        case "q":
            return m_type.PROMOTION_QUENN
        case "bishop":
            return m_type.PROMOTION_BISHOP
        case "b":
            return m_type.PROMOTION_BISHOP
        case "rock":
            return m_type.PROMOTION_ROCK
        case "r":
            return m_type.PROMOTION_ROCK
        case "knight":
            return m_type.PROMOTION_KNIGHT
        case "k":
            return m_type.PROMOTION_KNIGHT
        case _ :
            raise  ValueError("shoudlnt happen")


def code_feedback(text:str):
    """Prints one piece of player facing feedback inside an ascii box."""
    lines = text.splitlines() or [""]
    width = max(len(line) for line in lines)
    print("+" + "-" * (width + 2) + "+")
    for line in lines:
        print("| " + line.ljust(width) + " |")
    print("+" + "-" * (width + 2) + "+")
        












