# Proveout / what-if mode
from src.banker import Banker

CASES_PER_ROUND = [6, 5, 4, 3, 2, 1, 1, 1, 1]


class Proveout:
    """
    Simulates what would have happened if the player had said NO DEAL.
    Only valid for deals accepted on offers 1-8.
    """

    def __init__(self, deal_amount, player_case, remaining_board_cases, deal_round):
        if deal_round is None or deal_round > 8:
            raise ValueError(
                "Proveout is only available for deals accepted on offers 1-8."
            )
        self.deal_amount = deal_amount
        self.player_case = player_case
        self._remaining = dict(sorted(remaining_board_cases.items()))
        self.deal_round = deal_round
        self._rounds = None

    def get_proveout_rounds(self) -> list:
        if self._rounds is not None:
            return self._rounds

        # Advance a fresh Banker to the round after the deal was taken
        banker = Banker()
        for _ in range(self.deal_round):
            banker.make_offer([1000])  # dummy — just advances the round counter

        cases = dict(self._remaining)  # sorted copy, will be mutated
        rounds = []

        for r in range(self.deal_round + 1, 10):
            n_to_open = CASES_PER_ROUND[r - 1]
            opened = []
            for _ in range(min(n_to_open, len(cases))):
                number = min(cases.keys())
                opened.append(cases.pop(number))

            remaining_amounts = (
                [c.amount for c in cases.values()] + [self.player_case.amount]
            )
            offer = banker.make_offer(remaining_amounts)

            rounds.append({
                "round_number": r,
                "cases_opened": opened,
                "banker_offer": offer,
            })

        # Final entry: any remaining board case(s) + player's case
        final_cases = list(cases.values()) + [self.player_case]
        rounds.append({
            "round_number": None,
            "cases_opened": final_cases,
            "banker_offer": None,
        })

        self._rounds = rounds
        return rounds

    def get_verdict(self) -> str:
        if self.deal_amount >= self.player_case.amount:
            return "GOOD DEAL"
        return "BAD DEAL"
