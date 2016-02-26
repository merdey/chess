import pygame
import sys

from board import Board
from constants import tile_size, piece_inset


class Client:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Game of Life")
        self.fps_clock = pygame.time.Clock()
        self.state = 'main menu'
        self.buttons = []

    def start_game(self):
        self.board = Board()
        self.board.set_pieces()
        self.state = 'game running'
        self.active_player = 'White'

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button.was_clicked(mouse_pos):
                button.perform_actions()
                return

        if self.state == 'game running':
            x, y = self.get_tile_pos(*mouse_pos)
            res = self.board.handle_click(self.active_player, x, y)
            if res in ('move', 'capture', 'castle', 'en_passant'):
                self.swap_active_player()
            elif res == 'game_over':
                self.state = 'game over'
            print('Active Player', self.active_player)

    def get_tile_pos(self, pix_x, pix_y):
        # convert from pixel x/y to tile x/y
        return int(pix_x / tile_size), int(pix_y / tile_size)

    def swap_active_player(self):
        self.active_player = 'Black' if self.active_player == 'White' else 'White'

    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.state == 'main menu':
            self.buttons = [Button(200, 200, 200, 200, 'Start', self.start_game)]
        elif self.state == 'game running':
            self.buttons = []
            self.screen.fill((0, 255, 0))
            self.draw_board()
        elif self.state == 'game over':
            self.buttons = [Button(200, 200, 200, 200, 'Start Again', self.start_game)]

        for button in self.buttons: button.draw(self.screen)

        pygame.display.update()

    def draw_board(self):
        self._draw_tiling()
        self._draw_pieces()

    def _draw_tiling(self):
        for x, y in self.board.enumerate_coordinates():
            if x % 2 == y % 2:
                color = (255, 255, 255)
            else:
                color = (102, 51, 0)

            rect = (x * tile_size, y * tile_size, tile_size, tile_size)
            pygame.draw.rect(self.screen, color, rect)

    def _draw_pieces(self):
        for x, y in self.board.enumerate_coordinates():
            piece = self.board.get_piece(x, y)
            if piece is not None:
                self._draw_piece(piece, x, y)
        pygame.display.flip()

    def _draw_piece(self, piece, x, y):
        if piece.state == 'selected':
            pygame.draw.rect(
                self.screen,
                (255, 255, 0),
                (x * tile_size, y * tile_size, tile_size, tile_size)
            )

        piece_offset = (x * tile_size + piece_inset, y * tile_size + piece_inset)
        self.screen.blit(piece.sprite, piece_offset)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    res = self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw()

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


if __name__ == '__main__':
    client = Client()
    client.run()