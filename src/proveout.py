# Proveout / what-if mode
from src.banker import Banker

CASES_PER_ROUND = [6, 5, 4, 3, 2, 1, 1, 1, 1]


class Proveout:
    """
    Simulates what would have happened if the player had said NO DEAL.

    Only valid for deals accepted on offers 1-8. The proveout auto-plays
    the remaining rounds, opening cases in ascending case-number order
    (deterministic — no player choice) and computing hypothetical banker
    offers using the correct per-round scaling factors.
    """

    def __init__(self, deal_amount, player_case, remaining_board_cases, deal_round):
        """
        Args:
            deal_amount: The dollar amount the player accepted.
            player_case: The player's Briefcase.
            remaining_board_cases: Dict mapping case number → Briefcase for
                                   all cases still on the board at deal time.
            deal_round: Round number (1-8) when the deal was accepted.

        Raises:
            ValueError: If deal_round is None or greater than 8.
        """
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
        """
        Auto-play all remaining rounds and return a list of round summaries.

        Each entry (except the last) is a dict with keys:
            - 'round_number': int
            - 'cases_opened': list of Briefcase
            - 'banker_offer': int (hypothetical offer)

        The final entry has round_number=None and banker_offer=None, and
        cases_opened contains any remaining board cases plus the player's case.

        Returns:
            List of round summary dicts.
        """
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
        """
        Compare the accepted deal to the player's case value.

        Returns:
            'GOOD DEAL' if deal_amount >= player_case.amount, else 'BAD DEAL'.
        """
        if self.deal_amount >= self.player_case.amount:
            return "GOOD DEAL"
        return "BAD DEAL"
