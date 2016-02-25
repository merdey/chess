from constants import tile_size
from piece import Piece
from utils import construct_board, enumerate_coordinates

class Board:
    def __init__(self):
        self.board = construct_board()
        self.selected_piece = None

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

    def handle_click(self, player, x, y):
        '''Return True if move was made'''
        clicked_piece = self.board[y][x]
        print(x, y, clicked_piece)

        # If a piece is already selected, try to move to clicked tile
        if self.selected_piece:
            if self.can_move(self.selected_piece, x, y):
                self._move_piece(self.selected_piece, x, y)
                self._clear_selection()
                return True
            else:
                self._clear_selection()
                return False

        # Select piece if user clicked a piece of their color
        if clicked_piece and clicked_piece.color == player:
            self._select_piece(clicked_piece)

    def _select_piece(self, clicked_piece):
        clicked_piece.state = 'selected'
        self.selected_piece = clicked_piece

    def _clear_selection(self):
        self.selected_piece.state = 'normal'
        self.selected_piece = None

    def _move_piece(self, piece, new_x, new_y):
        old_x, old_y = self.get_piece_pos(piece)
        self.board[new_y][new_x] = piece
        self.board[old_y][old_x] = None
        print('moved from (%s, %s) to (%s, %s)' % (old_x, old_y, new_x, new_y))

    def can_move(self, piece, new_x, new_y):
        piece_x, piece_y = self.get_piece_pos(piece)
        target = self.board[new_y][new_x]

        if target and target.color == piece.color:
            return False

        return self.selected_piece.is_valid_move(piece_x, piece_y, new_x, new_y)

    def get_piece_pos(self, piece):
        for x, y in enumerate_coordinates(self.board):
            if piece == self.board[y][x]:
                return x, y

    def get_piece(self, x, y):
        return self.board[y][x]

    def enumerate_coordinates(self):
        for x, y in enumerate_coordinates(self.board):
            yield x, y
