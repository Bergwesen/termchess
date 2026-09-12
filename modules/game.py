from .sequence import Sequence
from .inputs import validate_input, notation_to_coordinate, input_processing, code_feedback
from .move import move, m_type, apply_move,is_checkmate,is_stalemate
from .board import Board, square_color
from .pieces import Color, Position,Koenig,Dame,Pferd,Laeufer,Bauer,Turm
from .fen_processing import  fen_out,fen_in
from collections import Counter


class LogikLeak(Exception):
    pass



def player_materials(board:Board , of:Color) -> list:
        player_pieces = []
        for x in range(8):
            for y in range(8):
                temp_piece = board.at(Position(x=x,y=y))
                if not(temp_piece is None): 
                    if temp_piece.color == of :
                        if isinstance(temp_piece,Koenig):
                            player_pieces.append('K')
                        elif isinstance(temp_piece,Bauer):
                            player_pieces.append('B')
                        elif isinstance(temp_piece,Laeufer):
                            if square_color(Position(x=temp_piece.x,y=temp_piece.y)) == Color.WHITE:
                                player_pieces.append('B0')
                            else :
                                player_pieces.append('B1')
                        elif isinstance(temp_piece,Pferd):
                            player_pieces.append('N')
                        elif isinstance(temp_piece,Dame):
                            player_pieces.append('D')
                        elif isinstance(temp_piece,Turm):
                            player_pieces.append('T')

        player_pieces.sort()
        return player_pieces

DRAWN = [
    [["K"], ["K"]],
    [["K"], ["B0", "K"]],
    [["K"], ["B1", "K"]],
    [["K"], ["K", "N"]],
    [["B0", "K"], ["B0", "K"]],
    [["B1", "K"], ["B1", "K"]],
]


class Game:

    def __init__(self):
        self.game_sequence: Sequence = Sequence(None)
        self.current = 0


    def scroll_back(self):
        if self.current <= -1 :
            raise ValueError("Shouldnt have happened")
        if self.current > self.game_sequence.rounds() -1:
            raise ValueError("Shouldnt have happened")
        elif self.current <= self.game_sequence.rounds() -1 :
            self.current = self.current -1
            print(self.game_sequence[self.current])
        else :
            raise ValueError("Weird")


    def input_routing(self) -> bool:  
        first_input = input().strip()
        match first_input :
            case "q":
                return True
            case "exit":
                return True
            case "forward":
                self.scroll_forward()
                return False
            case "backwards":
                self.scroll_back() 
                return False
            case "load":
                fen_input_string = input("give the fen string")
                self.fen_to_board(fen_input_string)
                return False
            case "export" : 
                print(self.board_to_fen())
                return False 
            case _ :
                try :
                    self.one_move(first_input)
                    return False
                except :
                    code_feedback("Wrong Input ? It should be q/exit/forward/backwards/load/export  or a  valid cooridnate like a4")
                    return False


    def scroll_forward(self):
        if self.current >= self.game_sequence.rounds():
            raise ValueError("Shouldnt have happened")
        if self.game_sequence.rounds() == self.current +1 :
           #input_continue = self.one_move()
            code_feedback("You cant  move forward. You are already at the current state")
        elif self.current < self.game_sequence.rounds() -1 :
            self.current += 1
            print(self.game_sequence[self.current])
        else :
            #shouldnt be reachable 
            raise ValueError("Weird")
            #self.current += 1
            #print(self.game_sequence[self.current])



    def game_loop(self):
        end = False
        while end == False:
            #self.one_move()
            end = self.input_routing()
            #a = input("Moechtest du  aufhoeren  y/n ")
            #if "y" in a.lower():
            #    end = True

    def game_loop_preset(self, preset_list: list[tuple[str, str]]):
        end = False
        for counter in range(len(preset_list)):
            self.one_move(
                s_input=preset_list[counter][0], e_input=preset_list[counter][1]
            )
        return True

    def is_finished_game(self):
        if  self.game_sequence.blocked != -1  or self.current < self.game_sequence.blocked :
            return  False 
        return True

    def fen_to_board(self,fen_string):
        """this  reset the sequence"""
        board = fen_in(fen_string)
        self.game_sequence = Sequence(board)
        self.current = 0
        print(self.game_sequence[self.current])
        

    def board_to_fen(self) -> str:
        return fen_out(self.game_sequence[self.current])

        

    #def next_board_info(self, board: Board) -> tuple[int, Color]:
    #    if self.current != board.round - 1:
    #        raise ValueError("Sequence is messed up")
    #    next_color = Color.WHITE if board.color == Color.BLACK else Color.BLACK
    #    self.current = self.current + 1
    #    return self.current + 1, next_color

    def one_move(self, s_input: str | None = None, e_input: str | None = None,promotion_figure: str|None = None):
        current_board = self.game_sequence[self.current]
        preset_flag = False
        if not (s_input is None) and not (e_input is None) :
            preset_flag = True 
        s_pos, e_pos = input_processing(s_input=s_input, e_input=e_input)
        #print(f"done processing first move is {s_pos} and second one is {e_pos}")
        move_validation = move(board=current_board, s_pos=s_pos, e_pos=e_pos,promotion_figure=promotion_figure)
        #I NEED TO CHECK WETHER THIS FAILS SO THAT THE PRESET ONE_MOVE CALL DOESNT CALL INPUT LOGIC
        while move_validation == m_type.INVALID_MOVE:
            if preset_flag:
                raise ValueError("preset input made a wrong move")
            code_feedback("The move was invalid")
            s_pos, e_pos = input_processing()
            move_validation = move(board=current_board, s_pos=s_pos, e_pos=e_pos)
        #print(move_validation)
        if isinstance(move_validation, m_type):
            raise ValueError(
                "m_type return should indicate an error and should only be m_type.INVALID_MOVE"
            )


        self.game_sequence.cache_board(apply_move(current_board, move_validation))
        self.current += 1
        new_board = self.game_sequence[self.current]
        print(self.game_sequence[self.current])

        if m_type.CHECKMATE in move_validation.notes:
            self.game_sequence.blocked = self.current 
            code_feedback("CHECKMATE ITS OVER")
        elif is_stalemate(self.game_sequence[self.current],by=self.game_sequence[self.current-1].color):
            self.game_sequence.blocked = self.current
            code_feedback("STALEMATE ITS OVER")

        if new_board.half_move_counter >= 100:
            self.game_sequence.blocked = self.current
            code_feedback("Draw because of the Fifty-move rule")
        w_pieces = player_materials(new_board,Color.WHITE)
        b_pieces = player_materials(new_board,Color.BLACK)
        case = [w_pieces , b_pieces ]
        case.sort()
        for x in DRAWN:
            x.sort()
            if  case  == x:
                self.game_sequence.blocked = self.current
                code_feedback("Draw because of insuffiecient materials")

        fen_set  = Counter()
        repetition = 0 
        for x in self.game_sequence.games_fens:
            fen_part = x.split(' ')
            fen_part = " ".join(fen_part[0:4])
            fen_set[fen_part] += 1
            if fen_set[fen_part] >= 3 :
                repetition +=1
        if repetition == 1 :
            self.game_sequence.blocked = self.current
            code_feedback("The Game is drawn  a position has been repeated 3 times")
        elif repetition > 1 :
            raise LogikLeak("A Repition wasnt caught either the  game sequence is valid or there is a logikleak")
        





def main():
    #fen_board = fen_in("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") 
    #print(fen_board)
    live_game = Game()
    print(live_game.game_sequence[live_game.current])
    #print(fen_out(live_game.game_sequence[live_game.current]))
    live_game.game_loop()
    #live_game.game_loop_preset([("a7", "a6")])



if __name__ == "__main__":
    main()
