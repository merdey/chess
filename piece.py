import pygame

from constants import tile_size, piece_inset

class Piece:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        self.state = 'normal'

    def is_valid_move(self, current_x, current_y, target_x, target_y):
        return True