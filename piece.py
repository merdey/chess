import pygame

from constants import tile_size, piece_inset

class Piece:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        self.state = 'normal'
