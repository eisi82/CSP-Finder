"""Configuration objects for the CSP Finder application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Application-level constants.

    Args:
        sp500_urls: Candidate URLs for loading the S&P 500 component list.
        http_timeout_seconds: Timeout for HTTP requests in seconds.
        default_risk_free_rate: Annualized risk-free rate used by greek calculations.

    Returns:
        AppConfig: Immutable configuration values for app services.
    """

    sp500_urls: tuple[str, ...] = (
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies?output=1",
    )
    http_timeout_seconds: int = 15
    default_risk_free_rate: float = 0.0455
