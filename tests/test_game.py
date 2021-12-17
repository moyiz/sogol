import pytest

from sogol.game import BoardBuilder, GameOfLife


@pytest.mark.parametrize(
    "max_column,max_row,max_cells", ((10, 10, 5), (1, 10, 5), (10, 1, 5), (10, 10, 0))
)
def test_generate_random_board(max_column, max_row, max_cells):
    board = BoardBuilder.generate_random_board(
        max_column=max_column, max_row=max_row, max_cells=max_cells
    )
    assert isinstance(board, tuple)
    assert len(board) <= max_cells
    assert all(isinstance(cell, tuple) for cell in board)
    assert all((0, 0) <= cell <= (max_column, max_row) for cell in board)


@pytest.mark.parametrize(
    "lexicon,expected_board",
    (
        ("..O\n..O\n..O", ((2, 0), (2, 1), (2, 2))),
        ("   ..O   \n..O \n    ..O", ((2, 0), (2, 1), (2, 2))),
        ("\t..O   \n    ..O \n    ..O", ((2, 0), (2, 1), (2, 2))),
    ),
)
def test_from_lexicon(lexicon, expected_board):
    board = BoardBuilder.from_lexicon(lexicon)
    assert board == expected_board


@pytest.mark.parametrize(
    "board,turns,result",
    (
        # - to |
        (((0, 0), (1, 0), (2, 0)), 1, ((1, 0), (1, -1), (1, 1))),
        # - to -
        (((0, 0), (1, 0), (2, 0)), 2, ((0, 0), (1, 0), (2, 0))),
        # Stale
        (
            ((1, 0), (0, 1), (2, 1), (0, 2), (2, 2), (1, 3)),
            1,
            ((1, 0), (0, 1), (2, 1), (0, 2), (2, 2), (1, 3)),
        ),
        # Aircraft carrier
        (
            ((2, 0), (3, 0), (0, 1), (3, 1), (0, 2), (1, 2)),
            1,
            ((2, 0), (3, 0), (0, 1), (3, 1), (0, 2), (1, 2)),
        ),
    ),
)
def test_game_of_life(board, turns, result):
    for _ in range(turns):
        board = GameOfLife.do_turn(board)
    assert sorted(board) == sorted(result)
