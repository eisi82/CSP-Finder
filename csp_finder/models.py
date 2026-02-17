"""Domain models for option analytics and filtering."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OptionFilterCriteria:
    """Filter criteria selected by the user.

    Args:
        min_days: Minimum days to expiration (inclusive).
        max_days: Maximum days to expiration (inclusive).
        min_cagr: Minimum CAGR value in percent (inclusive).
        max_cagr: Maximum CAGR value in percent (inclusive).

    Returns:
        OptionFilterCriteria: Immutable criteria used by analytics services.
    """

    min_days: int
    max_days: int
    min_cagr: float
    max_cagr: float


@dataclass(frozen=True)
class StockSelection:
    """Represents a single selected stock from the UI.

    Args:
        symbol: Stock ticker symbol.
        name: Human-readable company name.

    Returns:
        StockSelection: Parsed and validated stock selection.
    """

    symbol: str
    name: str

    @classmethod
    def from_label(cls, label: str) -> "StockSelection":
        """Create a stock selection object from a combined UI label.

        Args:
            label: String label in the format '<SYMBOL> - <COMPANY NAME>'.

        Returns:
            StockSelection: Parsed symbol and company name.
        """

        symbol, _, name = label.partition(" - ")
        return cls(symbol=symbol.strip(), name=name.strip())
