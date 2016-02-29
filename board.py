from constants import tile_size
from piece import Piece
from utils import construct_board, enumerate_coordinates

class Board:
    def __init__(self):
        self.board = construct_board()
        self.move_history = []

    def set_pieces(self):
        for x, y in enumerate_coordinates(self.board):
            # Determine color
            if y == 0 or y == 1:
                color = 'White'
            elif y == 6 or y == 7:
                color = 'Black'
            else:
                 continue

            # Determine rank
            if y == 1 or y == 6:
                rank = 'Pawn'
            elif x == 0 or x == 7:
                rank = 'Rook'
            elif x == 1 or x == 6:
                rank = 'Knight'
            elif x == 2 or x == 5:
                rank = 'Bishop'
            elif x == 3:
                rank = 'Queen'
            else:
                rank = 'King'

            self.board[y][x] = Piece(color, rank)

    def move_piece(self, piece, new_x, new_y):
        old_x, old_y = self.get_piece_pos(piece)
        self.board[new_y][new_x] = piece
        self.board[old_y][old_x] = None

        self.move_history.append((
            piece,
            (old_x, old_y),
            (new_x, new_y),
        ))

    def castle(self, piece, x, y):
        if x == 2:
            rook = self.get_piece(0, y)
            rook_x = 3
        else:
            rook = self.get_piece(7, y)
            rook_x = 5

        self.move_piece(piece, x, y)
        self.move_piece(rook, rook_x, y)


    def has_piece_moved(self, piece):
        for move in self.move_history:
            if move[0] == piece:
                return True
        return False


    def get_piece_pos(self, piece):
        for x, y in enumerate_coordinates(self.board):
            if piece == self.board[y][x]:
                return x, y

    def get_piece(self, x, y):
        return self.board[y][x]

    def enumerate_coordinates(self):
        for x, y in enumerate_coordinates(self.board):
            yield x, y
