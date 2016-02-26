def construct_board():
    return [[None] * 8 for i in range(8)]


def enumerate_coordinates(board):
    for y, row in enumerate(board):
        for x, v in enumerate(row):
            yield x, y


def validate_move(player, board, piece, x, y):
    current_x, current_y = board.get_piece_pos(piece)
    target_tile = board.get_piece(x, y)

    moves_allowed, attacks_allowed = get_allowed_moves(player, piece, current_x, current_y)
    if target_tile is None and (x, y) in moves_allowed:
        return 'move'
    elif target_tile and (x, y) in attacks_allowed:
        return 'game_over' if target_tile.rank == 'King' else 'capture'
    else:
        return 'illegal_move'
            

def get_allowed_moves(player, piece, x, y):
    moves_allowed = set()
    attacks_allowed = set()

    if piece.rank == 'Pawn':
        if player == 'White':
            moves_allowed.add((x, y + 1))
            attacks_allowed.add((x + 1, y + 1))
            attacks_allowed.add((x - 1, y + 1))
        else:
            moves_allowed.add((x, y - 1))
            attacks_allowed.add((x + 1, y - 1))
            attacks_allowed.add((x - 1, y - 1))
    elif piece.rank == 'Rook':
        for i in range(1, 8):
            allowed = (
                (x + i, y),
                (x - i, y),
                (x, y + i),
                (x, y - i),
            )
            for a in allowed:
                moves_allowed.add(a)
                attacks_allowed.add(a)
    elif piece.rank == 'Knight':
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
    elif piece.rank == 'Bishop':
        for i in range(1, 8):
            allowed = (
                (x + i, y + i),
                (x + i, y - i),
                (x - i, y + i),
                (x - i, y - i),
            )
            for a in allowed:
                moves_allowed.add(a)
                attacks_allowed.add(a)
    elif piece.rank == 'Queen':
        for i in range(1, 8):
            allowed = (
                (x + i, y),
                (x - i, y),
                (x, y + i),
                (x, y - i),
            )
            for a in allowed:
                moves_allowed.add(a)
                attacks_allowed.add(a)

        for i in range(1, 8):
            allowed = (
                (x + i, y + i),
                (x + i, y - i),
                (x - i, y + i),
                (x - i, y - i),
            )
            for a in allowed:
                moves_allowed.add(a)
                attacks_allowed.add(a)
    else: # piece.rank == 'King'
        allowed = (
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y - 1),
        )
        for a in allowed:
            moves_allowed.add(a)
            attacks_allowed.add(a)

    return moves_allowed, attacks_allowed
