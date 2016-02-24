import pygame
import sys

from board import Board


class Client:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        pygame.display.set_caption("Game of Life")
        self.fps_clock = pygame.time.Clock()
        self.state = 'main menu'
        self.buttons = [
            Button(0, 0, 100, 50, 'Start', self.start_game)
        ]

    def start_game(self):
        self.buttons = []
        self.board = Board()
        self.board.set_pieces()
        self.state = 'game running'

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if button.was_clicked(mouse_pos):
                button.perform_actions()
                return

        if self.state == 'game running':
            self.board.handle_click(mouse_pos)

    def draw(self):
        self.screen.fill((255, 255, 255))

        if self.state == 'main menu':
            pass
        elif self.state == 'game running':
            self.screen.fill((0, 255, 0))
            self.board.draw(self.screen)

        for button in self.buttons: button.draw(self.screen)

        pygame.display.update()

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.draw()

        self.fps_clock.tick(50)
        self.run()


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