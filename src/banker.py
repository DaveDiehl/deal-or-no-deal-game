# Banker

SCALING_FACTORS = {
    1: 0.10, 2: 0.20, 3: 0.30, 4: 0.40,
    5: 0.55, 6: 0.70, 7: 0.85, 8: 1.00, 9: 1.10,
}


class Banker:
    def __init__(self):
        self._round = 1

    @property
    def round(self) -> int:
        return self._round

    def make_offer(self, remaining_amounts: list) -> int:
        average = sum(remaining_amounts) / len(remaining_amounts)
        factor = SCALING_FACTORS.get(self._round, 1.10)
        offer = round(average * factor)
        self._round += 1
        return offer
