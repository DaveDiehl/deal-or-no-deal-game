import pytest
from src.game import GameBoard, GameController

STANDARD_AMOUNTS = {
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
    750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
    200000, 300000, 400000, 500000, 750000, 1000000,
}

# ---------------------------------------------------------------------------
# GameBoard tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# GameController tests
# ---------------------------------------------------------------------------

# --- Helpers ---

CASES_PER_ROUND = [6, 5, 4, 3, 2, 1, 1, 1, 1]


def make_controller():
    """Return a fresh GameController."""
    return GameController()


def advance_to_open_cases(gc):
    """Select player case to move past SELECT_CASE state."""
    board_numbers = list(gc.board.briefcases.keys())
    gc.select_player_case(board_numbers[0])


def open_round(gc, n):
    """Open n cases from whatever is available on the board."""
    opened = 0
    for number in list(gc.board.briefcases.keys()):
        if opened >= n:
            break
        gc.open_case(number)
        opened += 1


def play_through_rounds(gc, rounds):
    """Play through the given number of complete rounds (open + no deal)."""
    for r in range(rounds):
        open_round(gc, CASES_PER_ROUND[r])
        gc.no_deal()


# --- State machine ---

def test_controller_starts_in_select_case():
    gc = make_controller()
    assert gc.state == "SELECT_CASE"


def test_controller_moves_to_open_cases_after_selection():
    gc = make_controller()
    advance_to_open_cases(gc)
    assert gc.state == "OPEN_CASES"


def test_controller_moves_to_deal_or_no_deal_after_round():
    gc = make_controller()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])  # round 1: open 6
    assert gc.state == "DEAL_OR_NO_DEAL"


def test_controller_no_deal_returns_to_open_cases():
    gc = make_controller()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])
    gc.no_deal()
    assert gc.state == "OPEN_CASES"


def test_controller_deal_sets_deal_accepted():
    gc = make_controller()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])
    gc.deal()
    assert gc.state == "DEAL_ACCEPTED"


def test_controller_deal_sets_winnings_to_offer():
    gc = make_controller()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])
    offer = gc.current_offer
    gc.deal()
    assert gc.winnings == offer


def test_controller_game_over_false_during_play():
    gc = make_controller()
    advance_to_open_cases(gc)
    assert gc.game_over is False


def test_controller_game_over_true_after_deal():
    gc = make_controller()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])
    gc.deal()
    assert gc.game_over is True


# --- Round structure ---

def test_controller_cases_to_open_round_1():
    gc = make_controller()
    advance_to_open_cases(gc)
    assert gc.get_cases_to_open_this_round() == 6


def test_controller_cases_to_open_round_2():
    gc = make_controller()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])
    gc.no_deal()
    assert gc.get_cases_to_open_this_round() == 5


def test_controller_cases_to_open_all_rounds():
    gc = make_controller()
    advance_to_open_cases(gc)
    for i, expected in enumerate(CASES_PER_ROUND):
        assert gc.get_cases_to_open_this_round() == expected
        open_round(gc, expected)
        if i < len(CASES_PER_ROUND) - 1:
            gc.no_deal()


# --- State enforcement ---

def test_controller_cannot_open_case_in_wrong_state():
    gc = make_controller()  # SELECT_CASE state
    board_numbers = list(gc.board.briefcases.keys())
    with pytest.raises(ValueError):
        gc.open_case(board_numbers[0])


def test_controller_cannot_deal_in_wrong_state():
    gc = make_controller()
    advance_to_open_cases(gc)  # OPEN_CASES state
    with pytest.raises(ValueError):
        gc.deal()


def test_controller_cannot_no_deal_in_wrong_state():
    gc = make_controller()
    advance_to_open_cases(gc)  # OPEN_CASES state
    with pytest.raises(ValueError):
        gc.no_deal()


# --- Swap-or-keep finale ---

def test_controller_reaches_swap_or_keep_after_9_no_deals():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 9)
    assert gc.state == "SWAP_OR_KEEP"


def test_controller_keep_wins_player_case_amount():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 9)
    player_amount = gc.board.player_case.amount
    gc.keep()
    assert gc.winnings == player_amount
    assert gc.state == "GAME_OVER"


def test_controller_swap_wins_other_case_amount():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 9)
    other_number = list(gc.board.briefcases.keys())[0]
    other_amount = gc.board.briefcases[other_number].amount
    gc.swap()
    assert gc.winnings == other_amount
    assert gc.state == "GAME_OVER"


def test_controller_game_over_true_after_keep():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 9)
    gc.keep()
    assert gc.game_over is True


def test_controller_game_over_true_after_swap():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 9)
    gc.swap()
    assert gc.game_over is True


def test_controller_cannot_reach_swap_without_9_no_deals():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 8)  # only 8 rounds
    assert gc.state != "SWAP_OR_KEEP"


def test_controller_both_case_values_available_at_swap():
    gc = make_controller()
    advance_to_open_cases(gc)
    play_through_rounds(gc, 9)
    assert gc.board.player_case is not None
    assert len(gc.board.briefcases) == 1
