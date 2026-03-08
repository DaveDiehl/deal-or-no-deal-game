"""Deal or No Deal — console entry point."""
from src.game import GameController
from src.input_handler import InputHandler


def run():
    gc = GameController()
    handler = InputHandler()
    opened_cases = []
    eliminated_amounts = []

    print(gc.display.show_welcome())

    try:
        # --- SELECT PLAYER CASE ---
        print(gc.display.show_board(gc.board.briefcases, player_case=None))
        player_number = handler.prompt_case_number(
            "  Choose your briefcase (1-26): ",
            valid_numbers=set(gc.board.briefcases.keys()),
        )
        gc.select_player_case(player_number)
        print(gc.display.show_player_case(gc.board.player_case))

        # --- MAIN GAME LOOP ---
        while not gc.game_over:

            if gc.state == "OPEN_CASES":
                to_open = gc.get_cases_to_open_this_round()
                print(gc.display.show_board(gc.board.briefcases, gc.board.player_case, opened_cases))
                print(gc.display.show_amounts([], eliminated_amounts))
                print(f"\n  Open {to_open} case(s) this round.")

                for _ in range(to_open):
                    case_number = handler.prompt_case_number(
                        "  Choose a case to open: ",
                        valid_numbers=set(gc.board.briefcases.keys()),
                    )
                    case = gc.board.briefcases[case_number]
                    eliminated_amounts.append(case.amount)
                    opened_cases.append(case)
                    gc.open_case(case_number)
                    print(f"\n  Case #{case_number} contained: ${case.amount:,}" if case.amount == int(case.amount) else f"\n  Case #{case_number} contained: ${case.amount}")

            elif gc.state == "DEAL_OR_NO_DEAL":
                print(gc.display.show_offer(gc.current_offer))
                answer = handler.prompt_deal_or_no_deal()
                if answer == "deal":
                    gc.deal()
                else:
                    gc.no_deal()

            elif gc.state == "SWAP_OR_KEEP":
                other_case = list(gc.board.briefcases.values())[0]
                print(gc.display.show_swap_or_keep_prompt(gc.board.player_case, other_case))
                choice = handler.prompt_swap_or_keep()
                if choice == "keep":
                    winnings = gc.board.player_case.amount
                    print(gc.display.show_swap_result(gc.board.player_case, other_case, swapped=False))
                    gc.keep()
                else:
                    winnings = other_case.amount
                    print(gc.display.show_swap_result(gc.board.player_case, other_case, swapped=True))
                    gc.swap()

        # --- GAME OVER ---
        print(gc.display.show_final_result(gc.winnings))

        # --- PROVEOUT STUB (full implementation in feature/proveout) ---
        if gc.state == "DEAL_ACCEPTED":
            print(gc.display.show_proveout_header())
            print("  (Proveout mode coming soon...)\n")

    except KeyboardInterrupt:
        print("\n\n  Thanks for playing Deal or No Deal. Goodbye!\n")


if __name__ == "__main__":
    run()
