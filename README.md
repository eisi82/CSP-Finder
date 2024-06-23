# CSP-Finder 🎯
Find Cash-Secured Puts for stocks from the S&P 500 Index at the push of a button that best match your strategy.

## Overview
The **CSP Finder** is an application developed in Python and Streamlit that helps users find the best Cash Secured Puts (CSPs) for up to three selected stocks from the S&P 500 Index. Using user-defined selection criteria such as remaining expiration days and a preset range for Compound Annual Growth Rate (CAGR), the optimal CSPs are determined and presented in clear tables.

## Features
- Selection of up to three stocks from the S&P 500 Index
- Definition of user-defined selection criteria (e.g., term in days)
- Display of the best CSPs based on the CAGR
- Presentation of results in clear tables
- Export results to CSV or Excel

## Anforderungen
- Python 3.x
- Streamlit
- Pandas
- Additional dependencies can be found in the requirements.txt file

## Installation
1. **Clone Repository:**
    ```sh
    git clone https://github.com/eisi82/CSP-Finder.git
    cd CSP-Finder
    ```

2. **Create and activate virtual environment:**
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows: .\env\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Start Streamlit application:**
    ```sh
    streamlit run app.py
    ```

2. **Select stocks and set criteria::**
    - Select up to three stocks from the S&P 500 Index.
    - Use the sliders in the sidebar to set the desired selection criteria (e.g., term in days).
    - Click on "Go"
    -     

3. **Display results:**
    - The best CSPs based on CAGR are presented in clear tables.

## Example
Here is an example of using the application:

1. Start the application with:
    ```sh
    streamlit run app.py
    ```

2. Select stocks like Apple (AAPL), Microsoft (MSFT), and Amazon (AMZN) and click on "Go".
![Auswahl von drei Aktien](images/screenshot1.png)


3. Set ranges for expiration and CAGR and let the application find the best CSPs for you.
![Ergebnis](images/screenshot2.png)

## Contributions
Contributions are welcome! If you have ideas or find any bugs, please open an issue or create a pull request.

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more details.

## IMPORTANT LEGAL NOTICE
This app uses the yfinance package. Therefore, please note the following:

Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc.

yfinance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes.

You should refer to Yahoo!'s terms of use ([here](https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm), [here](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html), and [here](https://policies.yahoo.com/us/en/yahoo/terms/index.htm)) for details on your rights to use the actual data downloaded. Remember - the Yahoo! finance API is intended for personal use only.

Therefore, please use the app exclusively for personal, non-commercial purposes in accordance with Yahoo!'s terms of service!

## Authors
- Roman Eisenbarth - eisi82(https://github.com/eisi82)

---

Thank you for trying out the CSP-Finder! We look forward to your feedback.

