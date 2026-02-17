# CSP-Finder

CSP-Finder is a Streamlit application for analyzing **Cash-Secured Put (CSP)** opportunities on S&P 500 stocks. The app loads market data, calculates key option metrics (for example CAGR, premium return, and delta), and filters results based on user-defined criteria.

## Refactoring Goals

The codebase has been fully restructured with focus on:

- **Object-oriented design** with clear responsibilities
- **Modular architecture** (services, models, UI)
- **Robustness** through stable fallbacks and safer error handling
- **Performance for larger datasets** using vectorized pandas operations
- **Maintainability** through consistent docstrings and separation of concerns

---

## Project Structure

```text
CSP-Finder/
├── app.py
├── csp_finder/
│   ├── __init__.py
│   ├── config.py
│   ├── math_utils.py
│   ├── models.py
│   ├── services/
│   │   ├── csp_analyzer.py
│   │   └── market_data.py
│   └── ui/
│       └── streamlit_app.py
├── requirements.txt
└── README.md
```

### Module Overview

- `app.py`: Thin Streamlit entrypoint.
- `csp_finder/config.py`: Central app configuration (`AppConfig`).
- `csp_finder/models.py`: Domain models for filtering and stock selection.
- `csp_finder/services/market_data.py`: S&P 500 list retrieval, quote access, expiration filtering.
- `csp_finder/services/csp_analyzer.py`: CSP analytics pipeline and metric computation.
- `csp_finder/math_utils.py`: Shared math/greeks helpers.
- `csp_finder/ui/streamlit_app.py`: Streamlit UI orchestration.

---

## Installation

### Prerequisites

- Python 3.9+
- `pip`
- Internet access (Wikipedia + Yahoo Finance data endpoints)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/eisi82/CSP-Finder.git
   cd CSP-Finder
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   On Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Running the App

```bash
streamlit run app.py
```

The Streamlit UI will open in your browser.

---

## Usage

1. Select up to three S&P 500 stocks.
2. Configure the sidebar ranges:
   - `Days to Expiration`
   - `CAGR`
3. Click **Go**.
4. Review the filtered CSP opportunities per selected stock.

### Output Columns

- `lastPrice`: Latest option premium
- `strike`: Option strike price
- `expiration`: Expiration date
- `dte`: Days to expiration
- `MoneynessRatio`: Strike / underlying ratio
- `DistanceWeightedCAGR`: Distance-adjusted CAGR score
- `CAGR`: Annualized premium return metric
- `P/L`: Premium over strike in percent (not annualized)
- `delta`: Delta estimate from implied volatility

---

## Performance and Stability Notes

- **Vectorized calculations** in option-chain processing for better scaling.
- **Schema-stable empty DataFrames** to avoid UI failures when no results exist.
- **Encapsulated service layer** for easier testing and reduced side effects.
- **Centralized configuration** for URLs, timeout values, and risk-free rate.
- **Streamlit resource caching** for repeated S&P 500 symbol loading.

---

## Important Notes

- External market data can occasionally be unavailable (network/rate-limit/provider issues).
- The app handles missing data gracefully and keeps table schemas stable.

---

## License

This project is licensed under Apache-2.0. See `LICENSE` for details.

## Market Data Disclaimer

This application uses `yfinance`, which retrieves market data from Yahoo-related endpoints (Yahoo! / Yahoo! Finance).

**Important legal note:** Yahoo!, Y!Finance, and Yahoo! Finance are trademarks of Yahoo, Inc. The Yahoo Finance API/data is generally intended for **personal use only**. Use this application only in accordance with Yahoo's terms of service and applicable data usage policies.

Useful references:
- https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm
- https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html
- https://policies.yahoo.com/us/en/yahoo/terms/index.htm
