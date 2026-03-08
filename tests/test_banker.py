import pytest
from src.banker import Banker

SCALING_FACTORS = {
    1: 0.10, 2: 0.20, 3: 0.30, 4: 0.40,
    5: 0.55, 6: 0.70, 7: 0.85, 8: 1.00, 9: 1.10,
}


def test_banker_starts_at_round_1():
    banker = Banker()
    assert banker.round == 1


def test_banker_offer_round_1():
    # average of [100, 200, 300] = 200; * 0.10 = 20
    banker = Banker()
    offer = banker.make_offer([100, 200, 300])
    assert offer == 20


def test_banker_offer_round_2():
    # average of [1000, 3000] = 2000; * 0.20 = 400
    banker = Banker()
    banker.make_offer([1000, 3000])  # consume round 1
    offer = banker.make_offer([1000, 3000])
    assert offer == 400


def test_banker_offer_rounds_up_to_nearest_dollar():
    # average of [1, 2] = 1.5; round 1: 1.5 * 0.10 = 0.15 -> rounds to 0
    # use round 3 for a cleaner rounding case
    # average of [100, 101] = 100.5; * 0.30 = 30.15 -> rounds to 30
    banker = Banker()
    banker.make_offer([100])  # round 1
    banker.make_offer([100])  # round 2
    offer = banker.make_offer([100, 101])  # round 3: 100.5 * 0.30 = 30.15
    assert offer == round(100.5 * 0.30)


def test_banker_increments_round_after_offer():
    banker = Banker()
    assert banker.round == 1
    banker.make_offer([1000])
    assert banker.round == 2
    banker.make_offer([1000])
    assert banker.round == 3


def test_banker_offer_round_9_exceeds_average():
    # average of [1000] = 1000; * 1.10 = 1100 > 1000
    banker = Banker()
    for _ in range(8):
        banker.make_offer([1000])  # advance to round 9
    offer = banker.make_offer([1000])
    assert offer == 1100
    assert offer > 1000


def test_banker_all_scaling_factors():
    amounts = [1000]
    for round_num in range(1, 10):
        banker = Banker()
        for _ in range(round_num - 1):
            banker.make_offer(amounts)
        offer = banker.make_offer(amounts)
        expected = round(1000 * SCALING_FACTORS[round_num])
        assert offer == expected, f"Round {round_num}: expected {expected}, got {offer}"


def test_banker_offer_with_one_board_case_plus_player():
    # When 1 case remains on board + player case: average of those 2
    # amounts = [500000, 1000000]; average = 750000; round 8: * 1.00 = 750000
    banker = Banker()
    for _ in range(7):
        banker.make_offer([750000])  # advance to round 8
    offer = banker.make_offer([500000, 1000000])
    assert offer == 750000


def test_banker_offer_is_integer():
    banker = Banker()
    offer = banker.make_offer([123456, 654321])
    assert isinstance(offer, int)
