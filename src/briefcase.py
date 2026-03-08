# Briefcase, Model


class Briefcase:
    """Represents a single numbered briefcase containing a hidden dollar amount."""

    def __init__(self, number: int, amount: int):
        """
        Args:
            number: Case number (1-26).
            amount: Dollar amount hidden inside the case.
        """
        self._number = number
        self._amount = amount
        self._opened = False

    @property
    def number(self) -> int:
        """The case number (1-26)."""
        return self._number

    @property
    def amount(self) -> int:
        """The dollar amount hidden inside the case."""
        return self._amount

    @property
    def is_opened(self) -> bool:
        """True if the case has been opened."""
        return self._opened

    def open(self) -> int:
        """
        Open the case, revealing its dollar amount.

        Returns:
            The dollar amount inside.

        Raises:
            ValueError: If the case has already been opened.
        """
        if self._opened:
            raise ValueError(f"Case #{self._number} has already been opened.")
        self._opened = True
        return self._amount

    def __str__(self) -> str:
        """Return 'Case #N' when closed, 'Case #N ($X)' when opened."""
        if self._opened:
            return f"Case #{self._number} (${self._amount:,})"
        return f"Case #{self._number}"

    def __eq__(self, other) -> bool:
        """Equality is based on case number."""
        if not isinstance(other, Briefcase):
            return NotImplemented
        return self._number == other._number

    def __hash__(self):
        return hash(self._number)
