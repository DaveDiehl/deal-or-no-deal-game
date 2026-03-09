"""
Full-game integration tests using monkeypatched input.

Board layout with FIXED_AMOUNTS (case N gets FIXED_AMOUNTS[N-1]):
  Case  1 → $0.01       Case 14 → $10,000
  Case  2 → $1          Case 15 → $25,000
  Case  3 → $5          Case 16 → $50,000
  Case  4 → $10         Case 17 → $75,000
  Case  5 → $25         Case 18 → $100,000
  Case  6 → $50         Case 19 → $200,000
  Case  7 → $75         Case 20 → $300,000
  Case  8 → $100        Case 21 → $400,000
  Case  9 → $200        Case 22 → $500,000
  Case 10 → $300        Case 23 → $750,000
  Case 11 → $400        Case 24 → $1,000
  Case 12 → $500        Case 25 → $750,000 (overlaps — exact values don't matter for flow)
  Case 13 → $750        Case 26 → $1,000,000

Player selects Case 1 ($0.01). Cases 2-26 remain on board.
"""

import random
import pytest
from src import main

FIXED_AMOUNTS = [
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
    750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
    200000, 300000, 400000, 500000, 750000, 1000000,
]

# Complete input sequence for a full no-deal game (player keeps at end)
NO_DEAL_INPUTS = [
    "1",                                      # select player case
    "2", "3", "4", "5", "6", "7",            # round 1: open 6
    "no deal",
    "8", "9", "10", "11", "12",              # round 2: open 5
    "no deal",
    "13", "14", "15", "16",                  # round 3: open 4
    "no deal",
    "17", "18", "19",                        # round 4: open 3
    "no deal",
    "20", "21",                              # round 5: open 2
    "no deal",
    "22",                                    # round 6: open 1
    "no deal",
    "23",                                    # round 7: open 1
    "no deal",
    "24",                                    # round 8: open 1
    "no deal",
    "25",                                    # round 9: open 1
    "no deal",
    "keep",                                  # swap or keep
]

# Input sequence for deal accepted at round 1
DEAL_ROUND_1_INPUTS = [
    "1",                                     # select player case
    "2", "3", "4", "5", "6", "7",           # round 1: open 6
    "deal",                                  # take the deal
]


def make_input_patch(inputs):
    it = iter(inputs)
    return lambda _="": next(it)


def test_full_game_no_deal_path_completes(monkeypatch):
    """A complete game with no deals taken reaches GAME_OVER via keep."""
    monkeypatch.setattr(random, "sample", lambda pop, k: list(FIXED_AMOUNTS))
    monkeypatch.setattr("builtins.input", make_input_patch(NO_DEAL_INPUTS))
    main.run()  # Must complete without raising


def test_full_game_no_deal_swap_path_completes(monkeypatch):
    """A complete game with no deals taken reaches GAME_OVER via swap."""
    inputs = NO_DEAL_INPUTS[:-1] + ["swap"]  # replace "keep" with "swap"
    monkeypatch.setattr(random, "sample", lambda pop, k: list(FIXED_AMOUNTS))
    monkeypatch.setattr("builtins.input", make_input_patch(inputs))
    main.run()


def test_full_game_deal_round_1_triggers_proveout(monkeypatch, capsys):
    """Deal at round 1 completes and proveout output is shown."""
    monkeypatch.setattr(random, "sample", lambda pop, k: list(FIXED_AMOUNTS))
    monkeypatch.setattr("builtins.input", make_input_patch(DEAL_ROUND_1_INPUTS))
    main.run()
    output = capsys.readouterr().out
    assert "proveout" in output.lower() or "would have happened" in output.lower()


def test_full_game_deal_round_1_shows_final_result(monkeypatch, capsys):
    """Deal at round 1 shows the final winnings."""
    monkeypatch.setattr(random, "sample", lambda pop, k: list(FIXED_AMOUNTS))
    monkeypatch.setattr("builtins.input", make_input_patch(DEAL_ROUND_1_INPUTS))
    main.run()
    output = capsys.readouterr().out
    assert "congratulations" in output.lower() or "won" in output.lower()


def test_full_game_no_deal_output_contains_winnings(monkeypatch, capsys):
    """After swap-or-keep, final result is printed."""
    monkeypatch.setattr(random, "sample", lambda pop, k: list(FIXED_AMOUNTS))
    monkeypatch.setattr("builtins.input", make_input_patch(NO_DEAL_INPUTS))
    main.run()
    output = capsys.readouterr().out
    # Player kept case 1 ($0.01)
    assert "0.01" in output or "congratulations" in output.lower()


def test_keyboard_interrupt_exits_gracefully(monkeypatch, capsys):
    """Ctrl+C produces a goodbye message instead of a traceback."""
    monkeypatch.setattr("builtins.input", lambda _="": (_ for _ in ()).throw(KeyboardInterrupt()))
    main.run()
    output = capsys.readouterr().out
    assert "goodbye" in output.lower() or "thanks" in output.lower()
