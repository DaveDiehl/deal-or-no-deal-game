import pytest
from src.game import GameBoard

STANDARD_AMOUNTS = {
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
    750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
    200000, 300000, 400000, 500000, 750000, 1000000,
}


def test_gameboard_initializes_with_26_briefcases():
    board = GameBoard()
    assert len(board.briefcases) == 26


def test_gameboard_briefcases_numbered_1_to_26():
    board = GameBoard()
    numbers = {b.number for b in board.briefcases.values()}
    assert numbers == set(range(1, 27))


def test_gameboard_contains_standard_dollar_values():
    board = GameBoard()
    amounts = {b.amount for b in board.briefcases.values()}
    assert amounts == STANDARD_AMOUNTS


def test_gameboard_amounts_randomly_assigned(monkeypatch):
    # Run two boards and confirm the assignment order differs at least once
    # across many attempts (probability of always matching is 1/26! ≈ 0)
    seen_orders = set()
    for _ in range(10):
        board = GameBoard()
        order = tuple(board.briefcases[n].amount for n in range(1, 27))
        seen_orders.add(order)
    assert len(seen_orders) > 1


def test_gameboard_select_player_case_removes_from_board():
    board = GameBoard()
    board.select_player_case(5)
    assert 5 not in board.briefcases


def test_gameboard_select_player_case_stores_player_case():
    board = GameBoard()
    board.select_player_case(5)
    assert board.player_case is not None
    assert board.player_case.number == 5


def test_gameboard_select_invalid_case_raises():
    board = GameBoard()
    with pytest.raises(ValueError):
        board.select_player_case(0)
    with pytest.raises(ValueError):
        board.select_player_case(27)


def test_gameboard_25_cases_remain_after_selection():
    board = GameBoard()
    board.select_player_case(1)
    assert len(board.briefcases) == 25


def test_gameboard_open_case_removes_from_board():
    board = GameBoard()
    board.select_player_case(1)
    board.open_case(2)
    assert 2 not in board.briefcases


def test_gameboard_open_case_not_on_board_raises():
    board = GameBoard()
    board.select_player_case(1)
    board.open_case(2)
    with pytest.raises(ValueError):
        board.open_case(2)


def test_gameboard_open_player_case_raises():
    board = GameBoard()
    board.select_player_case(3)
    with pytest.raises(ValueError):
        board.open_case(3)


def test_get_remaining_amounts_includes_all_unopened():
    board = GameBoard()
    board.select_player_case(1)
    board.open_case(2)
    remaining = board.get_remaining_amounts()
    assert len(remaining) == 25  # 24 on board + player's case


def test_get_remaining_amounts_excludes_opened_cases():
    board = GameBoard()
    board.select_player_case(1)
    opened_amount = board.briefcases[2].amount
    board.open_case(2)
    remaining = board.get_remaining_amounts()
    assert opened_amount not in remaining
