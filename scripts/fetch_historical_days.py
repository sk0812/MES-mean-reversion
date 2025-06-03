from ib_insync import *
import pandas as pd
import os
from datetime import datetime, timedelta

ib = IB()
ib.connect("127.0.0.1", 7497, clientId=5)

contracts = ib.reqContractDetails(Future(symbol="MES", exchange="CME"))
mes = contracts[0].contract

# Generate last n weekdays (excluding weekends)
def get_past_trading_days(n):
    today = datetime.now()
    dates = []
    while len(dates) < n:
        today -= timedelta(days=1)
        if today.weekday() < 5:
            dates.append(today.strftime("%Y%m%d"))
    return dates

dates = get_past_trading_days(100)

os.makedirs("data", exist_ok=True)

for date in dates:
    file_path = f"data/MES_{date}.csv"
    if os.path.exists(file_path):
        print(f"⚠️ Already exists: MES_{date}.csv, skipping.")
        continue

    bars = ib.reqHistoricalData(
        mes,
        endDateTime=f"{date} 23:59:59",
        durationStr="1 D",
        barSizeSetting="1 min",
        whatToShow="TRADES",
        useRTH=False,
        formatDate=1
    )

    if not bars:
        print(f"❌ No data for {date}, skipping.")
        continue

    df = util.df(bars)
    df.to_csv(file_path, index=False)
    print(f"✅ Saved: MES_{date}.csv")

ib.disconnect()