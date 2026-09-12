from enum import Enum
from typing import override
from  dataclasses import dataclass

class Color(Enum):
    BLACK = 0
    WHITE = 1

def color_inverse(color:Color) -> Color:
    return Color.BLACK if color == Color.WHITE else Color.WHITE


BLACK_KING_Y = 0
BLACK_KING_X = 4
WHITE_KING_Y = 7
WHITE_KING_X = 4



@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self,other:Position) -> Position:
        return Position(x=self.x+other.x , y = self.y+other.y)

    def to_algebraic(self)-> str:
        algebraic_notation = ""
        match self.x :
            case 1 :
                algebraic_notation = algebraic_notation + 'a'
            case 2 :

                algebraic_notation = algebraic_notation + 'b'
            case 3 :
                algebraic_notation = algebraic_notation + 'c'
            case 4 :
                algebraic_notation = algebraic_notation + 'd'
            case 5 :
                algebraic_notation = algebraic_notation + 'e'
            case 6 :
                algebraic_notation = algebraic_notation + 'f'
            case 7 :
                algebraic_notation = algebraic_notation + 'g'
            case 8 :
                algebraic_notation = algebraic_notation + 'h'
        return algebraic_notation + str(8-self.y)


        

KOENIG_SIGN_W    = "\u2654"  # ♔
DAME_SIGN_W      = "\u2655"  # ♕
TURM_SIGN_W      = "\u2656"  # ♖
LAEUFER_SIGN_W   = "\u2657"  # ♗
SPRINGER_SIGN_W  = "\u2658"  # ♘
BAUER_SIGN_W     = "\u2659"  # ♙

KOENIG_SIGN_B    = "\u265A"  # ♚
DAME_SIGN_B      = "\u265B"  # ♛
TURM_SIGN_B      = "\u265C"  # ♜
LAEUFER_SIGN_B   = "\u265D"  # ♝
SPRINGER_SIGN_B  = "\u265E"  # ♞
BAUER_SIGN_B     = "\u265F"  # ♟

BAUER_LETTER = "B"
DAME_LETTER = "Q"
KOENIG_LETTER  = "K"
LAEUFER_LETTER = "B"
TURM_LETTER  = "R"
SPRINGER_LETTER = "N"



BLACK_JUMP_FROM = 1 
WHITE_JUMP_FROM = 6


class Figure():

    
    def __init__(self,color:Color,x:int,y:int,move_list:list[Position]):
        self.moved:bool = False  # has to be extended so that when loadin a game in the middle its not false
        self.color = color
        self.x = x 
        self.y = y
        self.sign = ""
        #self.move_list = move_list
    


    #REMEBER THAT WE ALSO STORE THE CURRENT POSIRTION AS POSSIBLE 
    def possible_moves(self) -> list[Position]:
        return []
    
    def inboundary(self,position:Position) -> bool :
        if not (position.x >= 0 and position.x <= 7) :
            return False
        if not (position.y >= 0 and position.y <= 7) :
            return False
        return True

    def __str__(self) -> str:
        return self.sign






class Bauer(Figure):
    def __init__(self,color,x,y,move_list=None):
        super().__init__(color,x,y,move_list)
        self.sign = BAUER_SIGN_W if self.color == Color.WHITE else BAUER_SIGN_B

    @override
    def possible_moves(self) -> list[Position]: 
        #self.move_list = []
        move_list = []
               
        
        up_down =  1 if self.color == Color.BLACK else -1
        up = Position(x=self.x,y=self.y+up_down)
        up_right = Position(x=self.x+1,y=self.y+up_down)
        up_left = Position(x=self.x-1,y=self.y+up_down)
        if self.inboundary(up):
            #self.move_list.append(up)
            move_list.append(up)
        if self.inboundary(up_right):
            #self.move_list.append(up_right)
            move_list.append(up_right)
        if self.inboundary(up_left):
            #self.move_list.append(up_left)
            move_list.append(up_left)

        if self.color == Color.BLACK     and self.y == BLACK_JUMP_FROM and self.moved == False: 
            #self.move_list.append(Position(x=self.x,y=self.y+2))
            move_list.append(Position(x=self.x,y=self.y+2))
        elif self.color == Color.WHITE and self.y == WHITE_JUMP_FROM and self.moved == False:
            #self.move_list.append(Position(x=self.x,y=self.y-2))
            move_list.append(Position(x=self.x,y=self.y-2))
     

        return move_list
    
    def extended_moves(self) -> list[Position]:
        move_list = self.possible_moves()
       # if self.color == Color.BLACK     and not self.moved  : 
       #     #self.move_list.append(Position(x=self.x,y=self.y+2))
       #     move_list.append(Position(x=self.x,y=self.y+2))
       # elif self.color == Color.WHITE and not self.moved:
            #self.move_list.append(Position(x=self.x,y=self.y-2))
      #      move_list.append(Position(x=self.x,y=self.y-2))
     
        return move_list

        


class Turm(Figure):

    def __init__(self,color,x,y,move_list=None):

        super().__init__(color,x,y,move_list)
        self.sign = TURM_SIGN_W if self.color == Color.WHITE else TURM_SIGN_B

    @override
    def possible_moves(self) -> list[Position]:
        #self.move_list = []
        move_list = []
        for x in range(8):
            new_move = Position(x=x,y=self.y)
            if self.inboundary(new_move) :
                if ( new_move.x != self.x):
                    #self.move_list.append(new_move)
                    move_list.append(new_move)

            else : 
                continue

        for y in range(8):
            new_move = Position(x=self.x,y=y)
            if self.inboundary(new_move):
                if (new_move.y != self.y):
                    #self.move_list.append(new_move)
                    move_list.append(new_move)
            else : 
                continue
            
        return move_list



class Koenig(Figure):
    def __init__(self,color,x,y,move_list=None):

        super().__init__(color,x,y,move_list)
        self.sign =  KOENIG_SIGN_W if self.color == Color.WHITE else KOENIG_SIGN_B

    
    @override
    def possible_moves(self) -> list[Position]: 
        #self.move_list = []
        move_list = []
        for direction in [[1,0],[1,1],[1,-1],[0,1],[0,-1],[-1,0],[-1,1],[-1,-1]] : 
            new_move = Position(x=self.x + direction[0],y=self.y + direction[1])
            if self.inboundary(new_move) : 
                #self.move_list.append(new_move)
                move_list.append(new_move)
            else : 
               continue 
        return move_list

    def extended_moves(self) -> list[Position]:
        move_list = self.possible_moves() 
        for case  in [2,-2]:
            castle_move = Position(x=self.x+case,y=self.y)
            if self.inboundary(castle_move):
                if self.color == Color.WHITE:
                    if self.y ==  WHITE_KING_Y and self.x == WHITE_KING_X:
                        move_list.append(castle_move)
                else :
                    if self.y ==  BLACK_KING_Y  and self.x == BLACK_KING_X:
                        move_list.append(castle_move)


        return move_list



class Dame(Figure):
    def __init__(self,color,x,y,move_list=None):


        super().__init__(color,x,y,move_list)
        self.sign = DAME_SIGN_W  if self.color == Color.WHITE else DAME_SIGN_B


    @override
    def possible_moves(self) -> list[Position]:
        #self.move_list = []
        move_list = []
        for x in range(8):
            new_move = Position(x=x,y=self.y)
            if self.inboundary(new_move):
                if (new_move.x != self.x):
                    #self.move_list.append(new_move)
                    move_list.append(new_move)
        for y in range(8):
            new_move = Position(x=self.x,y=y)
            if self.inboundary(new_move):
                if ( new_move.y != self.y):
                    #self.move_list.append(new_move)
                    move_list.append(new_move)
        for line in [(1,1),(-1,1),(-1,-1),(1,-1)] :
            diagonal = Position(x=line[0],y=line[1])
            for k in range(8):
                new_move = Position(x=self.x+ diagonal.x,y=self.y+diagonal.y)
                if self.inboundary(new_move):
                    #self.move_list.append(new_move)
                    move_list.append(new_move)
                else : 
                    break
                #diagonal.x += line[0] 
                #diagonal.y += line[1]
                diagonal = diagonal + Position(x=line[0],y=line[1])
        return move_list




class Laeufer(Figure):

    def __init__(self,color,x,y,move_list=None):
        super().__init__(color,x,y,move_list)
        self.sign = LAEUFER_SIGN_W if self.color == Color.WHITE else LAEUFER_SIGN_B 


    @override
    def possible_moves(self) -> list[Position]:
        #self.move_list = []
        move_list = []
        for line in [(1,1),(-1,1),(-1,-1),(1,-1)] :
            diagonal = Position(x=line[0],y=line[1])
            for k in range(8):
                new_move = Position(x=self.x+ diagonal.x,y=self.y+diagonal.y)
                if self.inboundary(new_move):
                    #self.move_list.append(new_move)
                    move_list.append(new_move)
                else : 
                    break
                #diagonal.x += line[0]
                #diagonal.y += line[1]
                diagonal = diagonal + Position(x=line[0],y=line[1])
        return move_list





class Pferd(Figure):
    def __init__(self,color,x,y,move_list=None):

        super().__init__(color,x,y,move_list)
        self.sign =  SPRINGER_SIGN_W if self.color == Color.WHITE else SPRINGER_SIGN_B 

    @override
    def possible_moves(self) -> list[Position]:
        #self.move_list = []
        move_list = []
        for line in [(-2,1),(-2,-1),(2,1),(2,-1),(1,2),(-1,2),(-1,-2),(1,-2)] :
            diagonal = Position(x=line[0],y=line[1])
            new_move = Position(x=self.x+ diagonal.x,y=self.y+diagonal.y)
            if self.inboundary(new_move):
        #        self.move_list.append(new_move)
                move_list.append(new_move)
            #diagonal.x += diagonal.x
            #diagonal.y += diagonal.y
            diagonal = diagonal + Position(x=line[0],y=line[1])
        return move_list 









