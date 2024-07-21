import streamlit as st
import yfinance as yf
import pandas as pd
import mibian as mi
from datetime import date, datetime, timedelta

footer_html = """<div style='text-align: center;'>
  <p>©️ by Roman Eisenbarth (eisi82 on GitHub), July 2024</p>
  <p>See more on <a href="https://github.com/eisi82/CSP-Finder">https://github.com/eisi82/CSP-Finder</a></p>

</div>"""




@st.cache_resource
def get_sp500():
    # Read and print the stock tickers that make up S&P500
    sp500_list = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    print(sp500_list.head())

    sp500 = sp500_list[['Symbol', 'Security']]
    sp500['Full'] = sp500_list['Symbol'] + " - " + sp500_list['Security']
    sp500.sort_values(by=['Full'],inplace=True)
    print(sp500.head())
    return sp500

def create_ticker_obj(stock):
    ticker_obj = yf.Ticker(stock)
    return ticker_obj

def get_puts(ticker_obj, stockprice, min_days, max_days, min_cagr, max_cagr):
    # Dataframe initialisieren
    putlist = pd.DataFrame()
    puts = pd.DataFrame()

    # Datum für Minimum und Maximum Days to Expiration berechnen
    min_expiry = datetime.now() + timedelta(days=min_days)
    max_expiry = datetime.now() + timedelta(days=max_days)
    #print("Min, Max: ", min_expiry, max_expiry)

    # Laden der Expiration-Dates für Stock
    expirations = ticker_obj.options # Laden der einzelnen Expirations
    # Aktuellen Stock-Price ermitteln
    #stockprice = get_price(ticker_obj)

    # Expirationdates in Datetime umwandeln und Filter für Puts innerhalb des Zeitbereichs
    for exp in expirations:
        # Expiration-Datum von String ind Datetime-Objekt umwandeln
        date_object = datetime.strptime(exp, '%Y-%m-%d') 
        # Nur Chain die zwischen der ausgewählten Datums-Range liegt
        if date_object >= min_expiry and date_object <= max_expiry:
            # Chain zur jweiligen Expiration laden
            puts = ticker_obj.option_chain(date=exp).puts
            
            # weitere Datenfelder generieren
            puts['expiration'] = date_object 
            puts['dte'] = (date_object - datetime.strptime(str(date.today()),'%Y-%m-%d')).days
            puts['Symbol'] = stock
            puts['CAGR'] = puts.apply(lambda row: calc_put_cagr(row['lastPrice'], row['strike'], row['dte']), axis=1)
            puts['P/L'] = puts.apply(lambda row: calc_put_pnl(row['lastPrice'], row['strike']), axis=1)
            puts['Moneyness'] = puts.apply(lambda row: round((row['strike'] / stockprice), 2), axis=1)
            puts['Puffer'] = puts.apply(lambda row: row['strike'] - row['lastPrice'], axis=1)
            puts['Abstand%'] = puts.apply(lambda row: ((stockprice / row['Puffer']) - 1) * 100, axis=1)
            puts['Faktor'] = puts.apply(lambda row: ((row['Abstand%'] / 100) * row['CAGR']), axis=1)
            
            # alle Put-Expirations zusammenfügen
            putlist = pd.concat([putlist, puts], ignore_index=True)
    
    # Nach Voragbe CAGR filtern
    filtered_puts = putlist[(putlist['CAGR'] >= min_cagr) & (putlist['CAGR'] <= max_cagr)]
    
    # Delta berechnen (hier beispielhaft als Dummy-Wert, da yFinance das Delta nicht direkt liefert)
    filtered_puts['delta'] = filtered_puts.apply(lambda x: get_greeks('p', stockprice, x['strike'], x['dte'], 0.0455, x['lastPrice']).putDelta, axis=1)

    # Ergebnis nach Factor sortieren
    filtered_puts_sorted = filtered_puts.sort_values(by='Faktor', ascending=False)

    return filtered_puts_sorted

def get_price(ticker_obj):
    # 31.01.2023
    # .info funktioniert nicht mehr, fast_info verwenden
    # p = get_stock(ticker).info['regularMarketPrice'] # Aktuellen Kurs auswerten
    p = ticker_obj.fast_info['last_price'] # Aktuellen Kurs auswerten
    return p

# Ermittlung CAGR für Cash Secured Put
def calc_put_cagr(p, s, dte):
    # p: Put Preis
    # s: Strike
    # dte: Days To Expiration
    cagr = (p / s) * (365 / dte) * 100
    return cagr

# Ermittlung P&L Cash Secured Put
def calc_put_pnl(p, s):
    pnl = (p / s) * 100
    return pnl

# Funktion zur Errechnung der Greeks
def get_greeks(cp, ul, s, dte, rf, o):
    # cp = put oder call
    # ul = Preis UL
    # s = Strike
    # dte = Days to Expiration
    # rf = Risk-free rate
    # o = Preis der Option
    if cp == 'c':
        # code call
        opt = mi.BS([ul, s, rf, dte], callPrice = o)        
    elif cp == 'p':
        # code put
        opt = mi.BS([ul, s, rf, dte], putPrice = o)       
    else:
        iv = 0
    iv = opt.impliedVolatility
    d = mi.BS([ul, s, rf, dte], volatility = iv)
    return d


if __name__ == "__main__":

    # Liste der S&P 500 Aktien (hier beispielhaft einige wenige)
    #sp500_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'BRK.B', 'JPM', 'JNJ', 'V']
    sp500_stocks = get_sp500()

    # Benutzeroberfläche
    st.title("S&P 500 Cash-Secured-Put Finder")

    st.sidebar.write("Select Ranges")

    # Auswahl der Aktien
    selected_stocks = st.multiselect("Please select up to three stocks...", sp500_stocks['Full'], max_selections=3)

    # Slider für Voreinstellungen
    min_days, max_days = st.sidebar.slider("Range Days to Expiration", 1, 365, (30,90))
    min_cagr, max_cagr = st.sidebar.slider("Range CAGR for CSP", 1, 120, (10, 40))

    # Button um die Abfrage zu starten
    if st.button("Go"):
        if selected_stocks:
            for stock in selected_stocks:
                # erstelle Ticker-Object
                stocksymbol = stock.split("-")[0].strip()
                ticker_obj = create_ticker_obj(stocksymbol)
                stockprice = get_price(ticker_obj)
                st.write(f"**{stock}, Last: {round(stockprice, 2)}**")            
                try:
                    st.write(get_puts(ticker_obj, stockprice, min_days, max_days, min_cagr, max_cagr)[['Symbol', 'lastPrice', 'strike', 'expiration', 'dte', 'Moneyness', 'Faktor','CAGR', 'P/L', 'delta']])
                except Exception as e:
                    st.write(f"No Data found for {stock}. Please make new selection.")
        else:
            st.write("Please select at least one stock.")

    # Footer
   
    st.markdown(footer_html, unsafe_allow_html=True)
   
