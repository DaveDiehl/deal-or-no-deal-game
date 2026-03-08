# Briefcase, Model


class Briefcase:
    def __init__(self, number: int, amount: int):
        self._number = number
        self._amount = amount
        self._opened = False

    @property
    def number(self) -> int:
        return self._number

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def is_opened(self) -> bool:
        return self._opened

    def open(self) -> int:
        if self._opened:
            raise ValueError(f"Case #{self._number} has already been opened.")
        self._opened = True
        return self._amount

    def __str__(self) -> str:
        if self._opened:
            return f"Case #{self._number} (${self._amount:,})"
        return f"Case #{self._number}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Briefcase):
            return NotImplemented
        return self._number == other._number

    def __hash__(self):
        return hash(self._number)
