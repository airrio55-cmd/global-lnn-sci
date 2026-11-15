"""V16 one-time data freeze. Run ONCE, after the protocol lock commit and before any analysis.

Downloads daily index closes from Yahoo Finance (unadjusted 'Close', 1996-01-01 to 2022-01-31), writes
DATA_DIR/<MARKET>.csv with columns Date, Close, and writes DATA_DIR/v16_data_manifest.json with SHA-256 values.
It never computes targets, signals or effects. Commit DATA_DIR before running v16_locked.py.
Usage: pip install yfinance==<record version>; python3 v16_fetch_data.py --out data_v16
"""
import argparse
import hashlib
import json
import os
import platform
from datetime import datetime, timezone

import pandas as pd
import yfinance as yf

TICKERS = {
    # Sample A: markets new to the study
    "FTSE100": "^FTSE", "DAX": "^GDAXI", "HANGSENG": "^HSI", "TSX": "^GSPTSE", "ASX200": "^AXJO", "TAIEX": "^TWII",
    # Sample B: study markets, used only for 1998-2009 blocks
    "SP500": "^GSPC", "NASDAQ100": "^NDX", "NIKKEI225": "^N225", "EUROSTOXX50": "^STOXX50E", "KOSPI200": "^KS200",
}
START, END = "1996-01-01", "2022-01-31"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    man = {"retrieved_utc": datetime.now(timezone.utc).isoformat(), "source": "Yahoo Finance via yfinance",
           "yfinance": yf.__version__, "pandas": pd.__version__, "python": platform.python_version(),
           "start": START, "end_exclusive": END, "field": "Close (auto_adjust=False)", "files": {}}
    for m, tk in TICKERS.items():
        raw = yf.download(tk, start=START, end=END, auto_adjust=False, progress=False, actions=False)
        if raw is None or raw.empty:
            man["files"][m] = {"ticker": tk, "status": "no data returned"}
            continue
        close = raw["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        df = pd.DataFrame({"Date": pd.to_datetime(close.index).strftime("%Y-%m-%d"), "Close": close.to_numpy()})
        path = os.path.join(a.out, f"{m}.csv")
        df.to_csv(path, index=False)
        man["files"][m] = {"ticker": tk, "rows": len(df), "first": df.Date.iloc[0], "last": df.Date.iloc[-1],
                           "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()}
    json.dump(man, open(os.path.join(a.out, "v16_data_manifest.json"), "w"), indent=2)
    print(json.dumps({m: v.get("rows", v.get("status")) for m, v in man["files"].items()}))


if __name__ == "__main__":
    main()
