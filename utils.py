import itertools

from constants import tile_size


def construct_board():
    return [[None] * 8 for i in range(8)]


def enumerate_coordinates(board):
    for y, row in enumerate(board):
        for x, v in enumerate(row):
            yield x, y


def validate_move(board, player, piece, x, y):
    if piece.color != player:
        return 'illegal_move'

    target_tile = board.get_piece(x, y)
    moves_allowed, attacks_allowed = get_allowed_moves(board, piece)
    if target_tile is None and (x, y) in moves_allowed:
        return 'move'
    elif target_tile and (x, y) in attacks_allowed:
        return 'capture' if target_tile.rank != 'King' else 'game_over'
    elif is_valid_castling(board, piece, x, y):
        return 'castle'


    return 'illegal_move'
            

def get_allowed_moves(board, piece):
    rule_mapping = {
        'Pawn': get_pawn_moves,
        'Rook': get_rook_moves,
        'Knight': get_knight_moves,
        'Bishop': get_bishop_moves,
        'Queen': get_queen_moves,
        'King': get_king_moves,
    }

    moves_allowed, attacks_allowed = rule_mapping[piece.rank](board, piece)
    return moves_allowed, attacks_allowed


def get_pawn_moves(board, piece):
    x, y = board.get_piece_pos(piece)
    moves_allowed = set()
    attacks_allowed = set()
    if piece.color == 'White':
        moves_allowed.add((x, y + 1))
        if not board.has_piece_moved(piece):
            moves_allowed.add((x, y + 2))
        attacks_allowed.add((x + 1, y + 1))
        attacks_allowed.add((x - 1, y + 1))
    else:
        moves_allowed.add((x, y - 1))
        if not board.has_piece_moved(piece):
            moves_allowed.add((x, y - 2))
        attacks_allowed.add((x + 1, y - 1))
        attacks_allowed.add((x - 1, y - 1))
    return moves_allowed, attacks_allowed


def get_rook_moves(board, piece):
    x, y = board.get_piece_pos(piece)
    moves_allowed, attacks_allowed = set(), set()
    for move in itertools.chain(get_horizontal_moves(board, x, y),
                                get_vertical_moves(board, x, y)):
        moves_allowed.add(move)
        attacks_allowed.add(move)
    return moves_allowed, attacks_allowed


def get_knight_moves(board, piece):
    x, y = board.get_piece_pos(piece)
    moves_allowed = set()
    attacks_allowed = set()
    allowed = (
            (x + 2, y + 1),
            (x + 2, y - 1),
            (x + 1, y + 2),
            (x + 1, y - 2),
            (x - 1, y + 2),
            (x - 1, y - 2),
            (x - 2, y + 1),
            (x - 2, y - 1),
        )
    for a in allowed:
        moves_allowed.add(a)
        attacks_allowed.add(a)
    return moves_allowed, attacks_allowed


def get_bishop_moves(board, piece):
    x, y = board.get_piece_pos(piece)
    moves_allowed, attacks_allowed = set(), set()
    for move in get_diagonal_moves(board, x, y):
        moves_allowed.add(move)
        attacks_allowed.add(move)
    return moves_allowed, attacks_allowed
            
            
def get_queen_moves(board, piece):
    x, y = board.get_piece_pos(piece)
    moves_allowed, attacks_allowed = set(), set()
    for move in itertools.chain(get_horizontal_moves(board, x, y),
                                get_vertical_moves(board, x, y),
                                get_diagonal_moves(board, x, y)):
        moves_allowed.add(move)
        attacks_allowed.add(move)
    return moves_allowed, attacks_allowed


def get_king_moves(board, piece):
    x, y = board.get_piece_pos(piece)
    moves_allowed, attacks_allowed = set(), set()
    for move in itertools.chain(get_horizontal_moves(board, x, y, length=1),
                                get_vertical_moves(board, x, y, length=1),
                                get_diagonal_moves(board, x, y, length=1)):
        moves_allowed.add(move)
        attacks_allowed.add(move)
    return moves_allowed, attacks_allowed


def is_valid_castling(board, piece, x, y):
    if x == 2:
        x = 0
    elif x == 6:
        x = 7
    else:
        return False

    target_tile = board.get_piece(x, y)
    if not target_tile or target_tile.rank != 'Rook' or piece.rank != 'King':
        return False
    if board.has_piece_moved(piece) or board.has_piece_moved(target_tile):
        return False

    piece_x, _ = board.get_piece_pos(piece)
    start = min(piece_x, x)
    end = max(piece_x, x)
    for i in range(start + 1, end):
        if board.get_piece(i, y):
            return False

    return True



def get_horizontal_moves(board, x, y, length=8):
    for allowed in itertools.chain(line_generator(board, x, y, 1, 0, length),
                                   line_generator(board, x, y, -1, 0, length)):
        yield allowed


def get_vertical_moves(board, x, y, length=8):
    for allowed in itertools.chain(
        line_generator(board, x, y, 0, 1, length),
        line_generator(board, x, y, 0, -1, length),
    ):
        yield allowed


def get_diagonal_moves(board, x, y, length=8):
    for allowed in itertools.chain(
        line_generator(board, x, y, 1, 1, length),
        line_generator(board, x, y, 1, -1, length),
        line_generator(board, x, y, -1, 1, length),
        line_generator(board, x, y, -1, -1, length),
    ):
        yield allowed


def line_generator(board, x, y, x_diff, y_diff, length):
    piece = board.get_piece(x, y)
    for i in range(1, length + 1):
        current_x = x + i*x_diff
        current_y = y + i*y_diff

        if current_x < 0 or current_x > 7 or current_y < 0 or current_y > 7:
            break

        current_tile = board.get_piece(current_x, current_y)
        if current_tile is None or piece.color != current_tile.color:
            yield (current_x, current_y)

        if current_tile:
            break


def get_tile_pos(pix_x, pix_y):
    # convert from pixel x/y to tile x/y
    return int(pix_x / tile_size), int(pix_y / tile_size)
