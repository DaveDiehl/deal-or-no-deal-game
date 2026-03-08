# InputHandler — console input with retry logic


class InputHandler:

    def prompt_case_number(self, prompt: str, valid_numbers: set) -> int:
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
        while True:
            raw = input('  Your answer (DEAL / NO DEAL): ').strip().lower()
            if raw in ("deal", "no deal"):
                return raw
            print("  Please type DEAL or NO DEAL.")

    def prompt_swap_or_keep(self) -> str:
        while True:
            raw = input('  Your choice (KEEP / SWAP): ').strip().lower()
            if raw in ("keep", "swap"):
                return raw
            print("  Please type KEEP or SWAP.")
