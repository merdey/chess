import itertools
import random
from collections import defaultdict

from utils import get_allowed_moves

class ChessAi():
    def pick_move(self, board, color):
        piece_moves = self.get_all_moves(board, color)

        # pick a random piece
        piece = random.choice(list(piece_moves.keys()))

        # pick a random move
        allowed_moves = piece_moves[piece]
        move = random.choice(allowed_moves)

        return piece, move

    def evaluate_board(self, board):
        pass

    def get_all_moves(self, board, color):
        pieces = []
        for x, y in board.enumerate_coordinates():
            piece = board.get_piece(x, y)
            if piece and piece.color == color:
                pieces.append(piece)

        moves = defaultdict(list)
        for piece in pieces:
            moves_allowed, attacks_allowed = get_allowed_moves(board, piece)
            for move in itertools.chain(moves_allowed, attacks_allowed):
                moves[piece].append(move)

        return moves