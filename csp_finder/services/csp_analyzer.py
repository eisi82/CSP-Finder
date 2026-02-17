"""Option analytics service for cash-secured put scanning."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

import pandas as pd
import yfinance as yf

from csp_finder.config import AppConfig
from csp_finder.math_utils import get_greek_delta
from csp_finder.models import OptionFilterCriteria
from csp_finder.services.market_data import MarketDataService


@dataclass
class CashSecuredPutAnalyzer:
    """Analyze CSP opportunities for a given ticker.

    Args:
        market_data: Service for market data retrieval.
        config: Static application configuration.

    Returns:
        CashSecuredPutAnalyzer: Analyzer capable of scanning puts and ranking output.
    """

    market_data: MarketDataService
    config: AppConfig

    def analyze_symbol(
        self,
        ticker: yf.Ticker,
        symbol: str,
        stock_price: float,
        criteria: OptionFilterCriteria,
    ) -> pd.DataFrame:
        """Compute filtered and ranked put opportunities for one symbol.

        Args:
            ticker: yfinance ticker object.
            symbol: Ticker symbol used for labeling output rows.
            stock_price: Current stock price.
            criteria: User-selected day/CAGR filter criteria.

        Returns:
            pd.DataFrame: Ranked CSP opportunities with computed metrics.
        """

        expirations = self.market_data.get_filtered_expirations(
            ticker,
            criteria.min_days,
            criteria.max_days,
        )
        if not expirations or not stock_price or stock_price <= 0:
            return self._empty_result()

        frames: list[pd.DataFrame] = []
        for exp in expirations:
            frame = self._load_and_enrich_put_chain(ticker=ticker, symbol=symbol, stock_price=stock_price, expiration=exp)
            if not frame.empty:
                frames.append(frame)

        if not frames:
            return self._empty_result()

        putlist = pd.concat(frames, ignore_index=True)
        filtered = putlist[
            (putlist["CAGR"] >= criteria.min_cagr)
            & (putlist["CAGR"] <= criteria.max_cagr)
        ].copy()
        if filtered.empty:
            return self._empty_result()

        filtered["delta"] = filtered.apply(
            lambda row: get_greek_delta(
                option_type="p",
                underlying_price=stock_price,
                strike=row["strike"],
                dte=int(row["dte"]),
                risk_free_rate=self.config.default_risk_free_rate,
                option_price=row["lastPrice"],
            ),
            axis=1,
        )
        return filtered.sort_values(by="CAGR", ascending=False, kind="mergesort").reset_index(drop=True)

    def _load_and_enrich_put_chain(
        self,
        ticker: yf.Ticker,
        symbol: str,
        stock_price: float,
        expiration: str,
    ) -> pd.DataFrame:
        """Load one expiration put chain and compute derived metrics.

        Args:
            ticker: yfinance ticker object.
            symbol: Ticker symbol for output labels.
            stock_price: Current stock price.
            expiration: Expiration date in 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: Enriched put-chain data for the given expiration.
        """

        expiration_dt = datetime.strptime(expiration, "%Y-%m-%d")
        dte = (expiration_dt - datetime.strptime(str(date.today()), "%Y-%m-%d")).days

        chain = ticker.option_chain(date=expiration).puts.copy()
        if chain.empty:
            return pd.DataFrame()

        chain["expiration"] = expiration_dt
        chain["dte"] = dte
        chain["Symbol"] = symbol

        strikes = chain["strike"].astype(float)
        last_prices = chain["lastPrice"].astype(float)

        if dte > 0:
            chain["CAGR"] = (last_prices / strikes) * (365 / dte) * 100
        else:
            chain["CAGR"] = 0.0

        chain["P/L"] = (last_prices / strikes) * 100
        chain["MoneynessRatio"] = (strikes / stock_price).round(2)
        chain["Buffer"] = stock_price - strikes
        chain["DistancePct"] = (chain["Buffer"] / stock_price) * 100
        chain["DistanceWeightedCAGR"] = (chain["DistancePct"] / 100) * chain["CAGR"]

        return chain

    def _empty_result(self) -> pd.DataFrame:
        """Return a schema-stable empty result DataFrame.

        Args:
            None.

        Returns:
            pd.DataFrame: Empty DataFrame with expected result columns.
        """

        return pd.DataFrame(
            columns=[
                "Symbol",
                "lastPrice",
                "strike",
                "expiration",
                "dte",
                "MoneynessRatio",
                "DistanceWeightedCAGR",
                "CAGR",
                "P/L",
                "delta",
            ]
        )
