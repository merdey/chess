import pygame

from constants import tile_size, piece_inset

class Piece:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        self.state = 'normal'

    def draw(self, screen, x, y):
        color_map = {
            'Pawn': (128, 128, 128),
            'Rook': (255, 0, 0),
            'Knight': (0, 0, 255),
            'Bishop': (0, 255, 0),
            'Queen': (255, 0, 255),
            'King': (255, 255, 255)
        }
        color = color_map.get(self.rank)

        border = (
            x * tile_size + piece_inset - 1,
            y * tile_size + piece_inset - 1,
            tile_size - 2 * piece_inset + 2,
            tile_size - 2 * piece_inset + 2,
        )
        border_color = (255, 255, 0) if self.state == 'selected' else (0, 0, 0)
        piece = (
            x * tile_size + piece_inset,
            y * tile_size + piece_inset,
            tile_size - 2 * piece_inset,
            tile_size - 2 * piece_inset,
        )

        pygame.draw.rect(screen, border_color, border)
        pygame.draw.rect(screen, color, piece)