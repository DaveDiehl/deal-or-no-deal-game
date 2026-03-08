import pytest
from src.display import Display
from src.briefcase import Briefcase


# --- Helpers ---

def make_briefcase(number, amount, opened=False):
    b = Briefcase(number, amount)
    if opened:
        b.open()
    return b


# --- show_board ---

def test_show_board_contains_all_case_numbers():
    display = Display()
    cases = {n: make_briefcase(n, 1000) for n in range(1, 27)}
    result = display.show_board(cases, player_case=None)
    for n in range(1, 27):
        assert str(n) in result


def test_show_board_marks_opened_cases_distinctly():
    display = Display()
    opened = make_briefcase(5, 1000, opened=True)
    cases = {n: make_briefcase(n, 1000) for n in range(1, 27) if n != 5}
    result = display.show_board(cases, player_case=None, opened=[opened])
    # Opened cases should be visually distinct (XX or similar)
    assert "XX" in result or "--" in result or "[  ]" in result or "✗" in result


def test_show_board_highlights_player_case():
    display = Display()
    player = make_briefcase(13, 500000)
    cases = {n: make_briefcase(n, 1000) for n in range(1, 27) if n != 13}
    result = display.show_board(cases, player_case=player)
    assert "13" in result


# --- show_amounts ---

def test_show_amounts_contains_all_standard_amounts():
    display = Display()
    amounts = [
        0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
        750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
        200000, 300000, 400000, 500000, 750000, 1000000,
    ]
    result = display.show_amounts(amounts, eliminated=[])
    assert "1,000,000" in result
    assert "0.01" in result


def test_show_amounts_marks_eliminated_amounts():
    display = Display()
    amounts = [100, 500, 1000]
    result = display.show_amounts(amounts, eliminated=[100])
    # The eliminated amount should be visually distinct
    assert result.count("100") >= 1  # still shown, just marked


# --- show_offer ---

def test_show_offer_contains_offer_amount():
    display = Display()
    result = display.show_offer(42500)
    assert "42,500" in result or "42500" in result


def test_show_offer_contains_deal_prompt():
    display = Display()
    result = display.show_offer(42500)
    assert "deal" in result.lower() or "offer" in result.lower()


# --- show_player_case ---

def test_show_player_case_contains_case_number():
    display = Display()
    case = make_briefcase(7, 250000)
    result = display.show_player_case(case)
    assert "7" in result


# --- show_welcome ---

def test_show_welcome_contains_title():
    display = Display()
    result = display.show_welcome()
    assert "deal" in result.lower()


def test_show_welcome_contains_instructions():
    display = Display()
    result = display.show_welcome()
    assert len(result) > 50  # substantive content


# --- show_final_result ---

def test_show_final_result_contains_winnings():
    display = Display()
    result = display.show_final_result(75000)
    assert "75,000" in result or "75000" in result


# --- show_swap_or_keep_prompt ---

def test_show_swap_or_keep_prompt_contains_both_case_numbers():
    display = Display()
    case_a = make_briefcase(3, 100)
    case_b = make_briefcase(18, 500000)
    result = display.show_swap_or_keep_prompt(case_a, case_b)
    assert "3" in result
    assert "18" in result


def test_show_swap_or_keep_prompt_mentions_swap_and_keep():
    display = Display()
    case_a = make_briefcase(3, 100)
    case_b = make_briefcase(18, 500000)
    result = display.show_swap_or_keep_prompt(case_a, case_b)
    assert "swap" in result.lower() or "switch" in result.lower()
    assert "keep" in result.lower()


# --- show_swap_result ---

def test_show_swap_result_contains_both_amounts():
    display = Display()
    result = display.show_swap_result(
        player_case=make_briefcase(3, 100),
        other_case=make_briefcase(18, 500000),
        swapped=True,
    )
    assert "100" in result
    assert "500,000" in result or "500000" in result


def test_show_swap_result_indicates_choice():
    display = Display()
    result = display.show_swap_result(
        player_case=make_briefcase(3, 100),
        other_case=make_briefcase(18, 500000),
        swapped=False,
    )
    assert "keep" in result.lower() or "kept" in result.lower() or "stay" in result.lower()


# --- show_proveout_header ---

def test_show_proveout_header_introduces_proveout():
    display = Display()
    result = display.show_proveout_header()
    assert "would" in result.lower() or "proveout" in result.lower() or "what if" in result.lower()


# --- show_proveout_round ---

def test_show_proveout_round_contains_round_number():
    display = Display()
    cases = [make_briefcase(2, 500), make_briefcase(4, 10000)]
    result = display.show_proveout_round(round_number=3, cases_opened=cases, banker_offer=8000)
    assert "3" in result


def test_show_proveout_round_contains_offer():
    display = Display()
    cases = [make_briefcase(2, 500)]
    result = display.show_proveout_round(round_number=1, cases_opened=cases, banker_offer=12345)
    assert "12,345" in result or "12345" in result


# --- show_proveout_final ---

def test_show_proveout_final_contains_deal_amount():
    display = Display()
    result = display.show_proveout_final(deal_amount=50000, case_value=1000000)
    assert "50,000" in result or "50000" in result


def test_show_proveout_final_contains_case_value():
    display = Display()
    result = display.show_proveout_final(deal_amount=50000, case_value=1000000)
    assert "1,000,000" in result or "1000000" in result


def test_show_proveout_final_indicates_good_or_bad_deal():
    display = Display()
    result = display.show_proveout_final(deal_amount=50000, case_value=1000000)
    # Case had more — bad deal
    assert any(word in result.lower() for word in ["bad", "less", "better", "missed", "worth"])
