import os

import pygame

from constants import piece_size


class Piece:
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        self.state = 'normal'

        path_to_sprite = 'sprites/%s%s.png' % (self.color, self.rank)
        sprite = pygame.image.load(os.path.join(path_to_sprite))
        self.sprite = pygame.transform.scale(sprite, (piece_size, piece_size))