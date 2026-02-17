"""Market data services for symbols, quotes, and option chains."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import requests
import yfinance as yf

from csp_finder.config import AppConfig


@dataclass
class MarketDataService:
    """Service for loading and normalizing market data.

    Args:
        config: Application configuration object.

    Returns:
        MarketDataService: Service with helper methods to fetch external data.
    """

    config: AppConfig

    def get_sp500(self) -> pd.DataFrame:
        """Load and normalize S&P 500 symbols from Wikipedia.

        Args:
            None.

        Returns:
            pd.DataFrame: DataFrame with columns ['Symbol', 'Security', 'Full'].
        """

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

        for url in self.config.sp500_urls:
            try:
                response = requests.get(url, headers=headers, timeout=self.config.http_timeout_seconds)
                response.raise_for_status()
                source_table = pd.read_html(response.text)[0]
                sp500 = source_table[["Symbol", "Security"]].copy()
                sp500["Full"] = sp500["Symbol"] + " - " + sp500["Security"]
                return sp500.sort_values(by="Full", kind="mergesort").reset_index(drop=True)
            except Exception:
                continue

        raise RuntimeError(
            "S&P 500 list could not be loaded (HTTP 403 / network issue). "
            "Please try again later or check your internet/proxy settings."
        )

    def create_ticker(self, symbol: str) -> yf.Ticker:
        """Instantiate a yfinance ticker object.

        Args:
            symbol: Ticker symbol.

        Returns:
            yf.Ticker: Ticker object for downstream quote and options requests.
        """

        return yf.Ticker(symbol)

    def get_price(self, ticker: yf.Ticker) -> float | None:
        """Fetch current regular market price.

        Args:
            ticker: yfinance ticker object.

        Returns:
            float | None: Last regular market price if available.
        """

        return ticker.info.get("regularMarketPrice")

    def get_filtered_expirations(self, ticker: yf.Ticker, min_days: int, max_days: int) -> list[str]:
        """Filter expiration dates by day-range window.

        Args:
            ticker: yfinance ticker object.
            min_days: Minimum days to expiration (inclusive).
            max_days: Maximum days to expiration (inclusive).

        Returns:
            list[str]: Matching expiration dates in 'YYYY-MM-DD' format.
        """

        now = datetime.now()
        lower = now.timestamp() + min_days * 86400
        upper = now.timestamp() + max_days * 86400

        selected: list[str] = []
        for exp in ticker.options:
            ts = datetime.strptime(exp, "%Y-%m-%d").timestamp()
            if lower <= ts <= upper:
                selected.append(exp)
        return selected
