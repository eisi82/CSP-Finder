"""Mathematical helper functions for CSP analytics."""

from __future__ import annotations

import mibian as mi


def calc_put_cagr(option_price: float, strike: float, dte: int) -> float:
    """Calculate annualized return (CAGR proxy) for a CSP.

    Args:
        option_price: Latest put premium.
        strike: Option strike price.
        dte: Days to expiration.

    Returns:
        float: Annualized return in percent; 0.0 for invalid inputs.
    """

    if dte <= 0 or strike <= 0:
        return 0.0
    return (option_price / strike) * (365 / dte) * 100


def calc_put_pnl(option_price: float, strike: float) -> float:
    """Calculate raw premium-to-strike return in percent.

    Args:
        option_price: Latest put premium.
        strike: Option strike price.

    Returns:
        float: Percentage return over secured strike not annualized.
    """

    if strike <= 0:
        return 0.0
    return (option_price / strike) * 100


def get_greek_delta(
    option_type: str,
    underlying_price: float,
    strike: float,
    dte: int,
    risk_free_rate: float,
    option_price: float,
) -> float:
    """Estimate option delta using implied volatility from Mibian.

    Args:
        option_type: 'p' for put or 'c' for call.
        underlying_price: Current underlying asset price.
        strike: Option strike price.
        dte: Days to expiration.
        risk_free_rate: Annualized risk-free interest rate.
        option_price: Option market premium used to infer implied volatility.

    Returns:
        float: Estimated option delta value or 0.0 if estimation fails.
    """

    if dte <= 0 or underlying_price <= 0 or strike <= 0 or option_price <= 0:
        return 0.0

    try:
        if option_type == "c":
            pricing = mi.BS([underlying_price, strike, risk_free_rate, dte], callPrice=option_price)
        elif option_type == "p":
            pricing = mi.BS([underlying_price, strike, risk_free_rate, dte], putPrice=option_price)
        else:
            return 0.0

        volatility = pricing.impliedVolatility
        greeks = mi.BS([underlying_price, strike, risk_free_rate, dte], volatility=volatility)
        return float(greeks.callDelta if option_type == "c" else greeks.putDelta)
    except Exception:
        return 0.0
