"""Streamlit UI composition for CSP Finder."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import streamlit as st

from csp_finder.config import AppConfig
from csp_finder.models import OptionFilterCriteria, StockSelection
from csp_finder.services.csp_analyzer import CashSecuredPutAnalyzer
from csp_finder.services.market_data import MarketDataService


@dataclass
class StreamlitCSPApp:
    """Orchestrates Streamlit rendering and service coordination.

    Args:
        market_data: Market data provider service.
        analyzer: Option analyzer service.

    Returns:
        StreamlitCSPApp: UI facade used by the entrypoint to render pages.
    """

    market_data: MarketDataService
    analyzer: CashSecuredPutAnalyzer

    def run(self) -> None:
        """Render and run the Streamlit application.

        Args:
            None.

        Returns:
            None: The method writes directly to Streamlit runtime state.
        """

        st.title("S&P 500 Cash-Secured-Put Finder")
        st.sidebar.write("Select Ranges")

        sp500 = self._get_sp500_cached()
        selected_labels = st.multiselect(
            "Please select up to three stocks...",
            sp500["Full"],
            max_selections=3,
        )

        min_days, max_days = st.sidebar.slider("Range Days to Expiration", 1, 365, (30, 90))
        min_cagr, max_cagr = st.sidebar.slider("Range CAGR for CSP", 1, 120, (10, 40))

        if st.button("Go"):
            self._render_results(
                selected_labels,
                OptionFilterCriteria(
                    min_days=min_days,
                    max_days=max_days,
                    min_cagr=min_cagr,
                    max_cagr=max_cagr,
                ),
            )

        st.markdown(self._footer_html(), unsafe_allow_html=True)

    @st.cache_resource
    def _get_sp500_cached(self) -> pd.DataFrame:
        """Load S&P 500 data with Streamlit resource caching.

        Args:
            None.

        Returns:
            pd.DataFrame: Cached DataFrame for symbol selection widgets.
        """

        return self.market_data.get_sp500()

    def _render_results(self, selected_labels: list[str], criteria: OptionFilterCriteria) -> None:
        """Render analysis tables for selected labels.

        Args:
            selected_labels: Selected labels from multiselect input.
            criteria: User-filter criteria object.

        Returns:
            None: Writes status and tables to Streamlit output.
        """

        if not selected_labels:
            st.write("Please select at least one stock.")
            return

        for label in selected_labels:
            selection = StockSelection.from_label(label)
            ticker = self.market_data.create_ticker(selection.symbol)
            stock_price = self.market_data.get_price(ticker)
            st.write(f"**{selection.symbol} - {selection.name}, Last: {stock_price}**")

            try:
                results = self.analyzer.analyze_symbol(
                    ticker=ticker,
                    symbol=selection.symbol,
                    stock_price=float(stock_price) if stock_price else 0.0,
                    criteria=criteria,
                )
                st.write(
                    results[
                        [
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
                    ]
                )
            except Exception:
                st.write(f"No Data found for {selection.symbol}. Please make new selection.")

    def _footer_html(self) -> str:
        """Return static footer HTML.

        Args:
            None.

        Returns:
            str: Footer HTML snippet with project attribution links.
        """

        return """<div style='text-align: center;'>
  <p>©️ by Roman Eisenbarth (eisi82 on GitHub), July 2024</p>
  <p>See more on <a href='https://github.com/eisi82/CSP-Finder'>https://github.com/eisi82/CSP-Finder</a></p>
</div>"""


def create_app() -> StreamlitCSPApp:
    """Build the application graph and return a runnable app object.

    Args:
        None.

    Returns:
        StreamlitCSPApp: Fully configured Streamlit app object.
    """

    config = AppConfig()
    market_data = MarketDataService(config=config)
    analyzer = CashSecuredPutAnalyzer(market_data=market_data, config=config)
    return StreamlitCSPApp(market_data=market_data, analyzer=analyzer)
