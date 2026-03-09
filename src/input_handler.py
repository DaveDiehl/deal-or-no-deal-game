# InputHandler — console input with retry logic


class InputHandler:
    """Handles all console input prompts with retry loops for invalid entries."""

    def prompt_case_number(self, prompt: str, valid_numbers: set) -> int:
        """
        Prompt the player to enter a case number, retrying on invalid input.

        Args:
            prompt: The prompt string to display.
            valid_numbers: Set of integers representing available case numbers.

        Returns:
            A valid case number from valid_numbers.
        """
        while True:
            raw = input(prompt).strip()
            try:
                number = int(raw)
            except ValueError:
                print(f"  Please enter a whole number.")
                continue
            if number not in valid_numbers:
                print(f"  Case #{number} is not available. Try again.")
                continue
            return number

    def prompt_deal_or_no_deal(self) -> str:
        """
        Prompt the player to accept or reject the Banker's offer.

        Returns:
            'deal' or 'no deal' (lowercase).
        """
        while True:
            raw = input('  Your answer (DEAL / NO DEAL): ').strip().lower()
            if raw in ("deal", "no deal"):
                return raw
            print("  Please type DEAL or NO DEAL.")

    def prompt_swap_or_keep(self) -> str:
        """
        Prompt the player to keep their case or swap for the remaining board case.

        Returns:
            'keep' or 'swap' (lowercase).
        """
        while True:
            raw = input('  Your choice (KEEP / SWAP): ').strip().lower()
            if raw in ("keep", "swap"):
                return raw
            print("  Please type KEEP or SWAP.")
