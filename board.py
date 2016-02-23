import pygame

from constants import tile_size
from piece import Piece

class Board:
    def __init__(self):
        self.board = _construct_board()

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


def _construct_board():
    return [[None] * 8 for i in range(8)]


def _enumerate_coordinates(board):
    for y, row in enumerate(board):
        for x, v in enumerate(row):
            yield x, y