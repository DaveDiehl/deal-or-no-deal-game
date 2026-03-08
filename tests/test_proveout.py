import pytest
from src.game import GameController
from src.proveout import Proveout
from src.briefcase import Briefcase

CASES_PER_ROUND = [6, 5, 4, 3, 2, 1, 1, 1, 1]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def advance_to_open_cases(gc):
    number = list(gc.board.briefcases.keys())[0]
    gc.select_player_case(number)


def open_round(gc, n):
    opened = 0
    for number in list(gc.board.briefcases.keys()):
        if opened >= n:
            break
        gc.open_case(number)
        opened += 1


def make_proveout_at_round(deal_round):
    """Play a game to deal_round, accept deal, return Proveout."""
    gc = GameController()
    advance_to_open_cases(gc)
    for r in range(deal_round - 1):
        open_round(gc, CASES_PER_ROUND[r])
        gc.no_deal()
    open_round(gc, CASES_PER_ROUND[deal_round - 1])
    remaining = dict(gc.board.briefcases)
    player_case = gc.board.player_case
    offer = gc.current_offer
    gc.deal()
    return Proveout(
        deal_amount=offer,
        player_case=player_case,
        remaining_board_cases=remaining,
        deal_round=deal_round,
    ), gc


# ---------------------------------------------------------------------------
# Round count
# ---------------------------------------------------------------------------

def test_proveout_round_count_deal_round_1():
    # 8 proveout rounds (2-9) + 1 final entry = 9
    proveout, _ = make_proveout_at_round(1)
    assert len(proveout.get_proveout_rounds()) == 9


def test_proveout_round_count_deal_round_4():
    # 5 proveout rounds (5-9) + 1 final entry = 6
    proveout, _ = make_proveout_at_round(4)
    assert len(proveout.get_proveout_rounds()) == 6


def test_proveout_round_count_deal_round_8():
    # 1 proveout round (9) + 1 final entry = 2
    proveout, _ = make_proveout_at_round(8)
    assert len(proveout.get_proveout_rounds()) == 2


# ---------------------------------------------------------------------------
# Round structure
# ---------------------------------------------------------------------------

def test_proveout_round_numbers_are_correct():
    proveout, _ = make_proveout_at_round(5)
    rounds = proveout.get_proveout_rounds()
    expected = [6, 7, 8, 9]
    actual = [r["round_number"] for r in rounds[:-1]]
    assert actual == expected


def test_proveout_round_has_required_keys():
    proveout, _ = make_proveout_at_round(2)
    for r in proveout.get_proveout_rounds()[:-1]:
        assert "round_number" in r
        assert "cases_opened" in r
        assert "banker_offer" in r


def test_proveout_banker_offer_is_integer_in_each_round():
    proveout, _ = make_proveout_at_round(3)
    for r in proveout.get_proveout_rounds()[:-1]:
        assert isinstance(r["banker_offer"], int)


def test_proveout_opens_correct_number_of_cases_per_round():
    proveout, _ = make_proveout_at_round(4)
    rounds = proveout.get_proveout_rounds()
    # deal_round=4, proveout rounds 5-9: CASES_PER_ROUND[4:] = [2,1,1,1,1]
    expected_counts = [2, 1, 1, 1, 1]
    for i, r in enumerate(rounds[:-1]):
        assert len(r["cases_opened"]) == expected_counts[i]


# ---------------------------------------------------------------------------
# Final entry
# ---------------------------------------------------------------------------

def test_proveout_final_entry_round_number_is_none():
    proveout, _ = make_proveout_at_round(1)
    final = proveout.get_proveout_rounds()[-1]
    assert final["round_number"] is None


def test_proveout_final_entry_banker_offer_is_none():
    proveout, _ = make_proveout_at_round(1)
    final = proveout.get_proveout_rounds()[-1]
    assert final["banker_offer"] is None


def test_proveout_final_entry_contains_player_case():
    proveout, _ = make_proveout_at_round(2)
    final = proveout.get_proveout_rounds()[-1]
    assert proveout.player_case in final["cases_opened"]


# ---------------------------------------------------------------------------
# Deterministic ordering
# ---------------------------------------------------------------------------

def test_proveout_cases_opened_in_ascending_order():
    proveout, _ = make_proveout_at_round(2)
    for r in proveout.get_proveout_rounds()[:-1]:
        numbers = [c.number for c in r["cases_opened"]]
        assert numbers == sorted(numbers)


# ---------------------------------------------------------------------------
# All board cases accounted for
# ---------------------------------------------------------------------------

def test_proveout_all_board_cases_opened():
    proveout, _ = make_proveout_at_round(3)
    expected_numbers = set(proveout._remaining.keys())
    rounds = proveout.get_proveout_rounds()
    opened_numbers = set()
    for r in rounds:
        for c in r["cases_opened"]:
            if c.number != proveout.player_case.number:
                opened_numbers.add(c.number)
    assert opened_numbers == expected_numbers


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------

def test_proveout_verdict_good_deal():
    # deal_amount >= player_case.amount → GOOD DEAL
    player_case = Briefcase(1, 100)
    remaining = {2: Briefcase(2, 500), 3: Briefcase(3, 1000)}
    proveout = Proveout(
        deal_amount=500,
        player_case=player_case,
        remaining_board_cases=remaining,
        deal_round=8,
    )
    assert proveout.get_verdict() == "GOOD DEAL"


def test_proveout_verdict_exact_match_is_good_deal():
    player_case = Briefcase(1, 500)
    remaining = {2: Briefcase(2, 1000), 3: Briefcase(3, 200)}
    proveout = Proveout(
        deal_amount=500,
        player_case=player_case,
        remaining_board_cases=remaining,
        deal_round=8,
    )
    assert proveout.get_verdict() == "GOOD DEAL"


def test_proveout_verdict_bad_deal():
    # deal_amount < player_case.amount → BAD DEAL
    player_case = Briefcase(1, 1000000)
    remaining = {2: Briefcase(2, 500), 3: Briefcase(3, 200)}
    proveout = Proveout(
        deal_amount=50000,
        player_case=player_case,
        remaining_board_cases=remaining,
        deal_round=8,
    )
    assert proveout.get_verdict() == "BAD DEAL"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_proveout_raises_for_deal_round_9():
    with pytest.raises(ValueError):
        Proveout(
            deal_amount=500,
            player_case=Briefcase(1, 100),
            remaining_board_cases={2: Briefcase(2, 1000)},
            deal_round=9,
        )


def test_proveout_raises_for_all_deals_rejected():
    # Represents swap-or-keep path — no deal was taken
    with pytest.raises(ValueError):
        Proveout(
            deal_amount=0,
            player_case=Briefcase(1, 100),
            remaining_board_cases={2: Briefcase(2, 1000)},
            deal_round=10,
        )


# ---------------------------------------------------------------------------
# GameController integration
# ---------------------------------------------------------------------------

def test_controller_create_proveout_after_deal():
    gc = GameController()
    advance_to_open_cases(gc)
    open_round(gc, CASES_PER_ROUND[0])
    gc.deal()
    proveout = gc.create_proveout()
    assert isinstance(proveout, Proveout)


def test_controller_create_proveout_raises_before_deal():
    gc = GameController()
    advance_to_open_cases(gc)
    with pytest.raises(ValueError):
        gc.create_proveout()


def test_controller_deal_round_9_raises_for_proveout():
    gc = GameController()
    advance_to_open_cases(gc)
    for r in range(8):
        open_round(gc, CASES_PER_ROUND[r])
        gc.no_deal()
    open_round(gc, CASES_PER_ROUND[8])
    gc.deal()
    # Deal accepted at round 9 — proveout not valid
    with pytest.raises(ValueError):
        gc.create_proveout()


# ---------------------------------------------------------------------------
# Edge cases — explicit round 1 and round 8 boundaries
# ---------------------------------------------------------------------------

def test_proveout_edge_round_1_plays_8_proveout_rounds():
    """Deal at round 1 → 8 proveout rounds (2-9) + final entry = 9 total."""
    proveout, _ = make_proveout_at_round(1)
    rounds = proveout.get_proveout_rounds()
    proveout_rounds = [r for r in rounds if r["round_number"] is not None]
    assert len(proveout_rounds) == 8
    assert [r["round_number"] for r in proveout_rounds] == list(range(2, 10))


def test_proveout_edge_round_8_plays_1_proveout_round():
    """Deal at round 8 → 1 proveout round (9) + final entry = 2 total."""
    proveout, _ = make_proveout_at_round(8)
    rounds = proveout.get_proveout_rounds()
    proveout_rounds = [r for r in rounds if r["round_number"] is not None]
    assert len(proveout_rounds) == 1
    assert proveout_rounds[0]["round_number"] == 9


def test_proveout_verdict_bad_deal_explicit():
    """BAD DEAL: deal amount is much less than player's case value."""
    player_case = Briefcase(13, 1000000)
    remaining = {2: Briefcase(2, 500), 3: Briefcase(3, 100)}
    proveout = Proveout(
        deal_amount=100,
        player_case=player_case,
        remaining_board_cases=remaining,
        deal_round=8,
    )
    assert proveout.get_verdict() == "BAD DEAL"
