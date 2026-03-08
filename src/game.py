# GameBoard, GameController
import random
from src.briefcase import Briefcase

STANDARD_AMOUNTS = [
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
    750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
    200000, 300000, 400000, 500000, 750000, 1000000,
]


class GameBoard:
    def __init__(self):
        amounts = random.sample(STANDARD_AMOUNTS, len(STANDARD_AMOUNTS))
        self.briefcases: dict[int, Briefcase] = {
            n: Briefcase(n, amount)
            for n, amount in zip(range(1, 27), amounts)
        }
        self.player_case: Briefcase | None = None

    def select_player_case(self, number: int) -> Briefcase:
        if number not in self.briefcases:
            raise ValueError(f"Case #{number} is not on the board.")
        self.player_case = self.briefcases.pop(number)
        return self.player_case

    def open_case(self, number: int) -> Briefcase:
        if number not in self.briefcases:
            raise ValueError(f"Case #{number} is not available to open.")
        case = self.briefcases.pop(number)
        case.open()
        return case

    def get_remaining_amounts(self) -> list:
        amounts = [b.amount for b in self.briefcases.values()]
        if self.player_case is not None:
            amounts.append(self.player_case.amount)
        return amounts
