import yfinance as yf
import pandas as pd
from datetime import datetime

# NIFTY 50 ke Top F&O Stocks
symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "TATAMOTORS.NS", "ITC.NS"]

print(f"Update started: {datetime.now()}")

for sym in symbols:
    try:
        df = yf.download(sym, period="1mo", interval="1d", progress=False)
        print(f"{sym} - {len(df)} rows downloaded")
    except Exception as e:
        print(f"{sym} Error: {e}")

print("Done - Renko Terminal Update Complete")
