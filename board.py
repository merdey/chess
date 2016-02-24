import pygame

from constants import tile_size
from piece import Piece

class Board:
    def __init__(self):
        self.board = _construct_board()
        self.selected_piece = None

    def set_pieces(self):
        for x, y in _enumerate_coordinates(self.board):
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

    def handle_click(self, mouse_pos, player):
        '''Return True if move was made'''
        click_x, click_y = self.get_tile_pos(mouse_pos[0], mouse_pos[1])
        clicked_piece = self.board[click_y][click_x]

        # If a piece is already selected, try to move to clicked tile
        if self.selected_piece:
            if self.can_move(self.selected_piece, click_x, click_y):
                self._move_piece(self.selected_piece, click_x, click_y)
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

        #TODO: handle castling
        if target and target.color == piece.color:
            return False

        return self.selected_piece.is_valid_move(piece_x, piece_y, new_x, new_y)

    def draw(self, screen):
        self._draw_tiling(screen)
        self._draw_pieces(screen)

    def _draw_tiling(self, screen):
        for x, y in _enumerate_coordinates(self.board):
            if x % 2 == y % 2:
                color = (255, 255, 255)
            else:
                color = (102, 51, 0)

            rect = (x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, color, rect)

    def _draw_pieces(self, screen):
        for x, y in _enumerate_coordinates(self.board):
            piece = self.board[y][x]
            if piece is not None:
                piece.draw(screen, x, y)

    def get_tile_pos(self, pix_x, pix_y):
        # convert from pixel x/y to tile x/y
        return int(pix_x / tile_size), int(pix_y / tile_size)

    def get_piece_pos(self, piece):
        for x, y in _enumerate_coordinates(self.board):
            if piece == self.board[y][x]:
                return x, y


def _construct_board():
    return [[None] * 8 for i in range(8)]


def _enumerate_coordinates(board):
    for y, row in enumerate(board):
        for x, v in enumerate(row):
            yield x, y