# Display, video wall, narrative
from src.briefcase import Briefcase


class Display:

    # --- Board ---

    def show_board(
        self,
        cases: dict,
        player_case: "Briefcase | None",
        opened: list | None = None,
    ) -> str:
        opened_numbers = {b.number for b in (opened or [])}
        lines = ["", "=" * 44, " " * 14 + "CASE BOARD", "=" * 44]
        all_numbers = sorted(
            list(cases.keys()) +
            ([player_case.number] if player_case else []) +
            list(opened_numbers)
        )
        row = []
        for n in range(1, 27):
            if n in opened_numbers:
                row.append(" XX ")
            else:
                row.append(f"[{n:2d}]")
            if len(row) == 6:
                lines.append("  " + "  ".join(row))
                row = []
        if row:
            lines.append("  " + "  ".join(row))
        if player_case:
            lines.append(f"\n  Your case: [{player_case.number:2d}]")
        lines.append("=" * 44)
        return "\n".join(lines)

    # --- Amounts ---

    def show_amounts(self, amounts: list, eliminated: list) -> str:
        eliminated_set = set(eliminated)
        all_amounts = [
            0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500,
            750, 1000, 5000, 10000, 25000, 50000, 75000, 100000,
            200000, 300000, 400000, 500000, 750000, 1000000,
        ]
        left = all_amounts[:13]
        right = all_amounts[13:]
        lines = ["", "=" * 44, " " * 12 + "DOLLAR AMOUNTS", "=" * 44]
        for l, r in zip(left, right):
            l_str = self._fmt_amount(l, l in eliminated_set)
            r_str = self._fmt_amount(r, r in eliminated_set)
            lines.append(f"  {l_str:<20}  {r_str}")
        lines.append("=" * 44)
        return "\n".join(lines)

    def _fmt_amount(self, amount: float, eliminated: bool) -> str:
        if amount == 0.01:
            formatted = "$0.01"
        else:
            formatted = f"${int(amount):,}"
        if eliminated:
            return f"[{formatted}]"
        return formatted

    # --- Offer ---

    def show_offer(self, offer: int) -> str:
        return (
            "\n" + "=" * 44 +
            "\n  THE BANKER'S OFFER" +
            f"\n\n  ${offer:,}" +
            "\n\n  DEAL or NO DEAL?" +
            "\n" + "=" * 44
        )

    # --- Player case ---

    def show_player_case(self, case: "Briefcase") -> str:
        return (
            f"\n  You have chosen Case #{case.number}.\n"
            f"  It will stay with you until the end!"
        )

    # --- Welcome ---

    def show_welcome(self) -> str:
        return (
            "\n" + "=" * 44 +
            "\n   Welcome to DEAL OR NO DEAL!" +
            "\n" + "=" * 44 +
            "\n\n  26 briefcases. 26 dollar amounts." +
            "\n  One is yours — choose wisely." +
            "\n\n  Each round, open cases to eliminate" +
            "\n  amounts. After each round, the Banker" +
            "\n  will make you an offer." +
            "\n\n  DEAL to take the money." +
            "\n  NO DEAL to keep playing." +
            "\n\n  Good luck!\n"
        )

    # --- Final result ---

    def show_final_result(self, winnings: float) -> str:
        if winnings == int(winnings):
            amount_str = f"${int(winnings):,}"
        else:
            amount_str = f"${winnings:,.2f}"
        return (
            "\n" + "=" * 44 +
            "\n  CONGRATULATIONS!" +
            f"\n\n  You won {amount_str}!" +
            "\n" + "=" * 44
        )

    # --- Swap or keep ---

    def show_swap_or_keep_prompt(
        self, player_case: "Briefcase", other_case: "Briefcase"
    ) -> str:
        return (
            "\n" + "=" * 44 +
            "\n  ONE CASE REMAINS!" +
            f"\n\n  Your case:  Case #{player_case.number}" +
            f"\n  Other case: Case #{other_case.number}" +
            "\n\n  Do you want to KEEP your case" +
            "\n  or SWAP for the other one?" +
            "\n" + "=" * 44
        )

    # --- Swap result ---

    def show_swap_result(
        self,
        player_case: "Briefcase",
        other_case: "Briefcase",
        swapped: bool,
    ) -> str:
        p_amt = player_case.amount
        o_amt = other_case.amount
        p_str = f"${p_amt:,}" if p_amt == int(p_amt) else f"${p_amt}"
        o_str = f"${o_amt:,}" if o_amt == int(o_amt) else f"${o_amt}"
        action = "swapped" if swapped else "kept"
        winning_amt = o_amt if swapped else p_amt
        w_str = f"${winning_amt:,}" if winning_amt == int(winning_amt) else f"${winning_amt}"
        return (
            "\n" + "=" * 44 +
            f"\n  Case #{player_case.number} contained: {p_str}" +
            f"\n  Case #{other_case.number} contained: {o_str}" +
            f"\n\n  You {action} — you win {w_str}!" +
            "\n" + "=" * 44
        )

    # --- Proveout ---

    def show_proveout_header(self) -> str:
        return (
            "\n" + "=" * 44 +
            "\n  PROVEOUT — What would have happened?" +
            "\n" + "=" * 44 +
            "\n  Let's see what the rest of the game" +
            "\n  would have looked like if you had" +
            "\n  said NO DEAL...\n"
        )

    def show_proveout_round(
        self,
        round_number: int,
        cases_opened: list,
        banker_offer: int,
    ) -> str:
        opened_strs = ", ".join(
            f"Case #{c.number} (${c.amount:,})" if c.amount == int(c.amount)
            else f"Case #{c.number} (${c.amount})"
            for c in cases_opened
        )
        return (
            f"\n  Round {round_number}:" +
            f"\n    Opened: {opened_strs}" +
            f"\n    Banker offer: ${banker_offer:,}"
        )

    def show_proveout_final(self, deal_amount: float, case_value: float) -> str:
        d_str = f"${int(deal_amount):,}" if deal_amount == int(deal_amount) else f"${deal_amount}"
        c_str = f"${int(case_value):,}" if case_value == int(case_value) else f"${case_value}"
        if case_value > deal_amount:
            verdict = f"Your case was worth {c_str} — the deal was worth less. You missed out!"
        elif case_value < deal_amount:
            verdict = f"Your case was only worth {c_str} — the deal was better!"
        else:
            verdict = f"Your case was worth exactly {c_str} — perfect deal!"
        return (
            "\n" + "=" * 44 +
            "\n  PROVEOUT RESULT" +
            f"\n\n  You took the deal for: {d_str}" +
            f"\n  Your case contained:   {c_str}" +
            f"\n\n  {verdict}" +
            "\n" + "=" * 44
        )
