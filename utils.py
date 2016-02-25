def construct_board():
    return [[None] * 8 for i in range(8)]


def enumerate_coordinates(board):
    for y, row in enumerate(board):
        for x, v in enumerate(row):
            yield x, y