import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

symbols = ["360ONE.NS","ABB.NS","ABCAPITAL.NS","ABFRL.NS","ACC.NS","ADANIENSOL.NS","ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS","ADANIPOWER.NS","ALKEM.NS","AMBUJACEM.NS","ANGELONE.NS","APLAPOLLO.NS","APOLLOHOSP.NS","ASHOKLEY.NS","ASIANPAINT.NS","ASTRAL.NS","ATUL.NS","AUBANK.NS","AUROPHARMA.NS","AXISBANK.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BAJFINANCE.NS","BALKRISIND.NS","BANDHANBNK.NS","BANKBARODA.NS","BATAINDIA.NS","BEL.NS","BERGEPAINT.NS","BHARATFORG.NS","BHARTIARTL.NS","BHEL.NS","BIOCON.NS","BOSCHLTD.NS","BPCL.NS","BRITANNIA.NS","BSOFT.NS","CAMS.NS","CANBK.NS","CANFINHOME.NS","CDSL.NS","CEATLTD.NS","CHAMBLFERT.NS","CHOLAFIN.NS","CIPLA.NS","COALINDIA.NS","COFORGE.NS","COLPAL.NS","CONCOR.NS","COROMANDEL.NS","CROMPTON.NS","CUB.NS","CUMMINSIND.NS","CYIENT.NS","DABUR.NS","DALBHARAT.NS","DEEPAKNTR.NS","DELTACORP.NS","DIVISLAB.NS","DIXON.NS","DLF.NS","DMART.NS","DRREDDY.NS","EICHERMOT.NS","ESCORTS.NS","EXIDEIND.NS","FEDERALBNK.NS","GAIL.NS","GLENMARK.NS","GMRINFRA.NS","GNFC.NS","GODREJCP.NS","GODREJPROP.NS","GRANULES.NS","GRASIM.NS","GUJGASLTD.NS","HAL.NS","HAVELLS.NS","HCLTECH.NS","HDFCAMC.NS","HDFCBANK.NS","HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDCOPPER.NS","HINDPETRO.NS","HINDUNILVR.NS","HINDZINC.NS","HONASA.NS","ICICIBANK.NS","ICICIGI.NS","ICICIPRULI.NS","IDFCFIRSTB.NS","IEX.NS","IGL.NS","INDHOTEL.NS","INDIAMART.NS","INDIGO.NS","INDUSINDBK.NS","INDUSTOWER.NS","INFY.NS","IOC.NS","IPCALAB.NS","IRCTC.NS","IRFC.NS","ITC.NS","JINDALSTEL.NS","JKCEMENT.NS","JSWENERGY.NS","JSWSTEEL.NS","JUBLFOOD.NS","KAYNES.NS","KEI.NS","KOTAKBANK.NS","KPITTECH.NS","LAURUSLABS.NS","LICHSGFIN.NS","LICI.NS","LT.NS","LTF.NS","LTIM.NS","LUPIN.NS","M&M.NS","M&MFIN.NS","MANAPPURAM.NS","MARICO.NS","MARUTI.NS","MAXHEALTH.NS","MCX.NS","METROPOLIS.NS","MFSL.NS","MGL.NS","MOTHERSON.NS","MPHASIS.NS","MRF.NS","MUTHOOTFIN.NS","NATIONALUM.NS","NAUKRI.NS","NBCC.NS","NESTLEIND.NS","NHPC.NS","NMDC.NS","NTPC.NS","OBEROIRLTY.NS","OFSS.NS","OIL.NS","ONGC.NS","PAGEIND.NS","PATANJALI.NS","PEL.NS","PERSISTENT.NS","PETRONET.NS","PFC.NS","PIDILITIND.NS","PIIND.NS","PNB.NS","POLICYBZR.NS","POLYCAB.NS","POWERGRID.NS","POWERINDIA.NS","PRAJIND.NS","PRESTIGE.NS","PVRINOX.NS","RAMCOCEM.NS","RBLBANK.NS","RECLTD.NS","RELIANCE.NS","SAIL.NS","SBICARD.NS","SBILIFE.NS","SBIN.NS","SHREECEM.NS","SHRIRAMFIN.NS","SIEMENS.NS","SRF.NS","SUNPHARMA.NS","SUNTV.NS","SYNGENE.NS","TATACHEM.NS","TATACOMM.NS","TATACONSUM.NS","TATAMOTORS.NS","TATAPOWER.NS","TATASTEEL.NS","TCS.NS","TECHM.NS","TITAN.NS","TORNTPHARM.NS","TORNTPOWER.NS","TRENT.NS","TVSMOTOR.NS","UBL.NS","ULTRACEMCO.NS","UNIONBANK.NS","UNITDSPR.NS","UPL.NS","VEDL.NS","VOLTAS.NS","WIPRO.NS","YESBANK.NS","ZEE.NS","ZYDUSLIFE.NS"]

def get_renko_signal(df):
    # ATR se Brick Size
    high = df['High'].values.flatten()
    low = df['Low'].values.flatten()
    close = df['Close'].values.flatten()
    tr = np.maximum(high[1:]-low[1:], np.abs(high[1:]-close[:-1]), np.abs(low[1:]-close[:-1]))
    atr = np.mean(tr[-14:]) if len(tr)>=14 else np.mean(tr)
    brick = max(atr*0.5, close[-1]*0.005)
    # Last 2 Renko Bricks
    last_close = close[-1]
    prev_close = close[-2]
    # Simple Renko Logic: Price ne Brick Size se zyada move kiya?
    diff = last_close - prev_close
    if diff >= brick:
        return "BUY", "GREEN", round(last_close,2), round(brick,2)
    elif diff <= -brick:
        return "SELL", "RED", round(last_close,2), round(brick,2)
    else:
        # Trend continue
        if last_close > close[-5]:
            return "HOLD-BULLISH", "GREEN", round(last_close,2), round(brick,2)
        else:
            return "HOLD-BEARISH", "RED", round(last_close,2), round(brick,2)

results = []
for sym in symbols:
    try:
        df = yf.download(sym, period="3mo", interval="1d", progress=False, auto_adjust=True)
        if len(df) < 20:
            continue
        signal, color, price, brick = get_renko_signal(df)
        name = sym.replace(".NS","")
        results.append({"Stock": name, "Price": price, "Signal": signal, "Brick_Color": color, "Brick_Size": brick})
        print(f"{name} - {signal} - {price}")
    except Exception as e:
        print(f"{sym} Error {e}")

df_out = pd.DataFrame(results)
# BUY pehle, SELL baad me
order = {"BUY":0, "SELL":1, "HOLD-BULLISH":2, "HOLD-BEARISH":3}
df_out['sort'] = df_out['Signal'].map(order)
df_out = df_out.sort_values('sort').drop(columns=['sort'])
df_out.to_csv("signals.csv", index=False)
print(f"Done - {len(df_out)} Signals Saved - Date {datetime.now()}")
