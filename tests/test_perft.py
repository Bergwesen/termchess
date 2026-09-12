import pytest

from modules.board import Board
from modules.move import move,m_type,apply_move
from modules.pieces import Color,Position,Bauer,Koenig
from modules.fen_processing import fen_in

PERFT_RESULTS = [20,400,8902,197281]

def move_counter(rounds:int):
    base_board_white = Board(board_list=None,runde=1,color=Color.WHITE)
    base_board_black = Board(board_list=None,runde=1,color=Color.BLACK)
    saved_result = [base_board_white]
    counted_moves = 0 
    for perft_round in range(rounds):
        next_result = []
        counted_moves = 0 
        for board in saved_result:
            for y in range(8):
                for x in range(8):
                    piece = board.at(Position(x=x,y=y))
                    if piece is None :
                        continue
                    if isinstance(piece,Bauer) or isinstance(piece,Koenig):
                        pseudo_legal_moves = piece.extended_moves()
                    else :
                        pseudo_legal_moves = piece.possible_moves()
                    for moves in pseudo_legal_moves:
                        move_result = move(board=board,s_pos=Position(x=piece.x,y=piece.y),e_pos=moves)
                        if not isinstance(move_result,m_type):
                            counted_moves = counted_moves +1 
                            print(f"We accepted move {piece} from {Position(x=piece.x,y=piece.y)} to {moves}")
                            next_result.append(apply_move(board=board,move=move_result)) 
        saved_result = next_result
    return counted_moves






def test_perft_counter():
    assert move_counter(1) == 20
    assert move_counter(2) == 400
    assert move_counter(3) == 8902
    assert move_counter(4) == 197281


















def perft_counter(board, rounds: int) -> int:
    counted_moves = 0
    for y in range(8):
        for x in range(8):
            piece = board.at(Position(x=x, y=y))
            if piece is None:
                continue
            if isinstance(piece, Bauer) or isinstance(piece, Koenig):
                pseudo_legal_moves = piece.extended_moves()
            else:
                pseudo_legal_moves = piece.possible_moves()
            for moves in pseudo_legal_moves:
                move_result = move(board=board, s_pos=Position(x=x, y=y), e_pos=moves)
                if not isinstance(move_result, m_type):
                    if rounds == 1:
                        counted_moves = counted_moves + 1
                    else:
                        counted_moves = counted_moves + perft_counter(
                            apply_move(board=board, move=move_result), rounds - 1
                        )
    return counted_moves


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
KIWIPETE_FEN = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"

START_RESULTS = [20,400,8902]
KIWIPETE_RESULTS = [48,2039,97862]


def test_perft_counter_from_fen():
    for depth, expected in enumerate(START_RESULTS, start=1):
        assert perft_counter(fen_in(START_FEN), depth) == expected
    for depth, expected in enumerate(KIWIPETE_RESULTS, start=1):
        assert perft_counter(fen_in(KIWIPETE_FEN), depth) == expected
