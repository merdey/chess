from ai import ChessAi
from board import Board
from utils import validate_move


class Game:
    '''Manages game state'''

    def __init__(self):
        self.board = Board()

        self.players = {
            'White': 'human',
            'Black': 'ai'
        }
        self.active_player = 'White'
        self.ai = ChessAi()

    def move_piece(self, piece, x, y):
        res = validate_move(self.board, self.active_player, piece, x, y)
        if res == 'move' or res == 'capture':
            self.board.move_piece(piece, x, y)
            self.toggle_active_player()
        elif res == 'castle':
            self.board.castle(piece, x, y)
            self.toggle_active_player()
        elif res == 'en_passant':
            raise NotImplemented('En passant not implemented')

        return res

    def active_player_is_ai(self):
        return self.players[self.active_player] == 'ai'

    def toggle_active_player(self):
        self.active_player = 'Black' if self.active_player == 'White' else 'White'

    def enumerate_board_coordinates(self):
        return self.board.enumerate_coordinates()

    def get_piece(self, x, y):
        return self.board.get_piece(x, y)

    def make_ai_move(self):
        assert self.active_player_is_ai()
        piece, pos = self.ai.pick_move(self.board, self.active_player)
        x, y = pos
        self.move_piece(piece, x, y)
