# GameBoard, GameController
import random
from src.briefcase import Briefcase
from src.banker import Banker
from src.display import Display
from src.proveout import Proveout

STANDARD_AMOUNTS = [
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
    750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
    200000, 300000, 400000, 500000, 750000, 1000000,
]


class GameBoard:
    """
    Holds the 26 briefcases and tracks which cases are still in play.

    Dollar amounts are randomly shuffled across case numbers at start-up.
    """

    def __init__(self):
        amounts = random.sample(STANDARD_AMOUNTS, len(STANDARD_AMOUNTS))
        self.briefcases: dict[int, Briefcase] = {
            n: Briefcase(n, amount)
            for n, amount in zip(range(1, 27), amounts)
        }
        self.player_case: Briefcase | None = None

    def select_player_case(self, number: int) -> Briefcase:
        """
        Remove a case from the board and designate it as the player's case.

        Args:
            number: Case number to select (must be on the board).

        Returns:
            The selected Briefcase.

        Raises:
            ValueError: If the number is not on the board.
        """
        if number not in self.briefcases:
            raise ValueError(f"Case #{number} is not on the board.")
        self.player_case = self.briefcases.pop(number)
        return self.player_case

    def open_case(self, number: int) -> Briefcase:
        """
        Open a case, removing it from the board and revealing its amount.

        Args:
            number: Case number to open (must be on the board).

        Returns:
            The opened Briefcase.

        Raises:
            ValueError: If the number is not on the board.
        """
        if number not in self.briefcases:
            raise ValueError(f"Case #{number} is not available to open.")
        case = self.briefcases.pop(number)
        case.open()
        return case

    def get_remaining_amounts(self) -> list:
        """
        Return all dollar amounts still in play (board cases + player's case).
        """
        amounts = [b.amount for b in self.briefcases.values()]
        if self.player_case is not None:
            amounts.append(self.player_case.amount)
        return amounts


CASES_PER_ROUND = [6, 5, 4, 3, 2, 1, 1, 1, 1]


class GameController:
    """
    Orchestrates the full game flow, composing GameBoard, Banker, and Display.

    State machine:
        SELECT_CASE → OPEN_CASES ↔ DEAL_OR_NO_DEAL (×9) → SWAP_OR_KEEP → GAME_OVER
        or DEAL_OR_NO_DEAL → DEAL_ACCEPTED (at any round 1-9)

    Cases to open per round: 6, 5, 4, 3, 2, 1, 1, 1, 1.
    """

    def __init__(self):
        self.board = GameBoard()
        self.banker = Banker()
        self.display = Display()
        self.state = "SELECT_CASE"
        self._round = 1
        self._cases_opened_this_round = 0
        self.current_offer: int | None = None
        self.winnings: float | None = None
        self._deal_round: int | None = None

    @property
    def game_over(self) -> bool:
        """True when the game has ended (deal accepted or swap/keep complete)."""
        return self.state in ("DEAL_ACCEPTED", "GAME_OVER")

    def get_cases_to_open_this_round(self) -> int:
        """Return the number of cases the player must open in the current round."""
        return CASES_PER_ROUND[self._round - 1]

    def select_player_case(self, number: int) -> None:
        """
        Select the player's personal briefcase to start the game.

        Raises:
            ValueError: If not in SELECT_CASE state or number is invalid.
        """
        if self.state != "SELECT_CASE":
            raise ValueError("Cannot select player case in current state.")
        self.board.select_player_case(number)
        self.state = "OPEN_CASES"

    def open_case(self, number: int) -> None:
        """
        Open a case from the board during the OPEN_CASES phase.

        Automatically transitions to DEAL_OR_NO_DEAL when enough cases
        have been opened for the current round.

        Raises:
            ValueError: If not in OPEN_CASES state or case is unavailable.
        """
        if self.state != "OPEN_CASES":
            raise ValueError("Cannot open a case in current state.")
        self.board.open_case(number)
        self._cases_opened_this_round += 1
        if self._cases_opened_this_round >= self.get_cases_to_open_this_round():
            self.current_offer = self.banker.make_offer(self.board.get_remaining_amounts())
            self.state = "DEAL_OR_NO_DEAL"

    def deal(self) -> None:
        """
        Accept the Banker's offer, ending the game.

        Sets winnings to the current offer and transitions to DEAL_ACCEPTED.

        Raises:
            ValueError: If not in DEAL_OR_NO_DEAL state.
        """
        if self.state != "DEAL_OR_NO_DEAL":
            raise ValueError("Cannot take a deal in current state.")
        self._deal_round = self._round
        self.winnings = self.current_offer
        self.state = "DEAL_ACCEPTED"

    def create_proveout(self) -> "Proveout":
        """
        Create a Proveout simulation after a deal has been accepted.

        Only valid for deals accepted on offers 1-8.

        Returns:
            A Proveout instance ready to simulate remaining rounds.

        Raises:
            ValueError: If state is not DEAL_ACCEPTED or deal was on round 9.
        """
        if self.state != "DEAL_ACCEPTED":
            raise ValueError("Proveout is only available after a deal has been accepted.")
        return Proveout(
            deal_amount=self.winnings,
            player_case=self.board.player_case,
            remaining_board_cases=self.board.briefcases,
            deal_round=self._deal_round,
        )

    def no_deal(self) -> None:
        """
        Reject the Banker's offer and advance to the next round.

        After round 9 is rejected, transitions to SWAP_OR_KEEP.

        Raises:
            ValueError: If not in DEAL_OR_NO_DEAL state.
        """
        if self.state != "DEAL_OR_NO_DEAL":
            raise ValueError("Cannot reject a deal in current state.")
        self._round += 1
        self._cases_opened_this_round = 0
        if self._round > len(CASES_PER_ROUND):
            self.state = "SWAP_OR_KEEP"
        else:
            self.state = "OPEN_CASES"

    def keep(self) -> None:
        """
        Keep the player's original case in the swap-or-keep finale.

        Sets winnings to the player's case amount.

        Raises:
            ValueError: If not in SWAP_OR_KEEP state.
        """
        if self.state != "SWAP_OR_KEEP":
            raise ValueError("Cannot keep in current state.")
        self.winnings = self.board.player_case.amount
        self.state = "GAME_OVER"

    def swap(self) -> None:
        """
        Swap the player's case for the remaining board case.

        Sets winnings to the amount in the other case.

        Raises:
            ValueError: If not in SWAP_OR_KEEP state.
        """
        if self.state != "SWAP_OR_KEEP":
            raise ValueError("Cannot swap in current state.")
        other_case = list(self.board.briefcases.values())[0]
        self.winnings = other_case.amount
        self.state = "GAME_OVER"
