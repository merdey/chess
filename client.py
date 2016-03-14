import os
import pygame
import sys
import time

from constants import tile_size, piece_inset, piece_size, piece_ranks
from game import Game
from utils import get_tile_pos


class Client:
    '''Handles drawing to screen and accepting user interaction'''

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Chess")
        self.fps_clock = pygame.time.Clock()
        self.state = 'main menu'
        self.buttons = []
        self._load_sprites()
        self.selected_piece = None

    def _load_sprites(self):
        self.sprites = {}
        for color in ('Black', 'White'):
            for rank in piece_ranks:
                key = color + rank
                path_to_sprite = 'sprites/%s.png' % key
                sprite = pygame.image.load(os.path.join(path_to_sprite))
                self.sprites[key] = pygame.transform.scale(sprite, (piece_size, piece_size))

    def start_game(self):
        self.game = Game()
        self.state = 'game running'

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button.was_clicked(mouse_pos):
                button.perform_actions()
                return

        if self.state == 'game running':
            x, y = get_tile_pos(*mouse_pos)
            clicked_piece = self.game.get_piece(x, y)
            if self.selected_piece:
                res = self.game.move_piece(self.selected_piece, x, y)
            elif clicked_piece and clicked_piece.color == self.game.active_player:
                self._select_piece(clicked_piece)
                res = 'select_piece'
            else:
                res = 'invalid'

            if res in ('move', 'capture', 'castle', 'en_passant'):
                self._clear_selection()
            elif res == 'game_over':
                self.state = 'game over'

    def _select_piece(self, piece):
        self.selected_piece = piece

    def _clear_selection(self):
        self.selected_piece = None

    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.state == 'main menu':
            self.buttons = [Button(200, 200, 200, 200, 'Start New Game', self.start_game)]
        elif self.state == 'game running':
            self.buttons = []
            self.screen.fill((0, 255, 0))
            self._draw_board()
        elif self.state == 'game over':
            self.buttons = [Button(200, 200, 200, 200, 'Start Again', self.start_game)]

        for button in self.buttons: button.draw(self.screen)
        pygame.display.update()

    def _draw_board(self):
        self._draw_tiling()
        self._draw_pieces()

    def _draw_tiling(self):
        for x, y in self.game.enumerate_board_coordinates():
            if x % 2 == y % 2:
                color = (255, 255, 255)
            else:
                color = (102, 51, 0)

            rect = (x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(self.screen, color, rect)

    def _draw_pieces(self):
        for x, y in self.game.enumerate_board_coordinates():
            piece = self.game.get_piece(x, y)
            if piece is not None:
                self._draw_piece(piece, x, y)
        pygame.display.flip()

    def _draw_piece(self, piece, x, y):
        if piece == self.selected_piece:
            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                (x * tile_size, y * tile_size, tile_size, tile_size)
            )

        piece_offset = (x * tile_size + piece_inset, y * tile_size + piece_inset)
        k = piece.color + piece.rank
        self.screen.blit(self.sprites[k], piece_offset)

    def run(self):
        while True:
            self.handle_events(pygame.event.get())
            self.draw()

            if self.state == 'game running' and self.game.active_player_is_ai():
                self.game.make_ai_move()
                time.sleep(1)

            self.fps_clock.tick(50)


class Button:
    def __init__(self, x, y, width, height, text, *actions):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.actions = actions

        self.fontObj = pygame.font.Font('freesansbold.ttf', 24)
        self.textSurfaceObj = self.fontObj.render(text, True, (0, 0, 0))
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (x+width/2, y+height/2)

    def was_clicked(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)

    def perform_actions(self):
        for a in self.actions: a()

    def draw(self, screen):
        screen.blit(self.textSurfaceObj, self.textRectObj)
