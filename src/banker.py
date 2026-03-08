# Banker

SCALING_FACTORS = {
    1: 0.10, 2: 0.20, 3: 0.30, 4: 0.40,
    5: 0.55, 6: 0.70, 7: 0.85, 8: 1.00, 9: 1.10,
}


class Banker:
    """
    Calculates the Banker's offer each round.

    The offer is computed as:  round(average_of_remaining_amounts * scaling_factor)

    Scaling factors increase each round and can exceed 1.0 in round 9,
    meaning the offer can exceed the simple average of remaining amounts.
    """

    def __init__(self):
        self._round = 1

    @property
    def round(self) -> int:
        """The current round number (1-9)."""
        return self._round

    def make_offer(self, remaining_amounts: list) -> int:
        """
        Calculate and return the Banker's offer for the current round.

        Increments the internal round counter after computing the offer.

        Args:
            remaining_amounts: List of dollar amounts still in play
                               (board cases + player's case).

        Returns:
            The offer as a whole dollar integer.
        """
        average = sum(remaining_amounts) / len(remaining_amounts)
        factor = SCALING_FACTORS.get(self._round, 1.10)
        offer = round(average * factor)
        self._round += 1
        return offer
