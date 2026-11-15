"""V16 model-free adjacent-window reversal test. Do not alter after lock.

Usage:
  python3 v16_locked.py --data DATA_DIR --out OUT_DIR --preflight   # inventory + signal-group counts; never reads targets
  python3 v16_locked.py --data DATA_DIR --out OUT_DIR               # full locked analysis
DATA_DIR holds <MARKET>.csv files with columns Date, Close (frozen by v16_fetch_data.py).
"""
import argparse
import hashlib
import json
import os
from datetime import date

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

H = 20
SIGNALS = ["200DMA", "Persistence", "Momentum60"]  # 200DMA is the sole primary signal
SAMPLE_A = ["FTSE100", "DAX", "HANGSENG", "TSX", "ASX200", "TAIEX"]          # markets new to the study
SAMPLE_B = ["SP500", "NASDAQ100", "NIKKEI225", "EUROSTOXX50", "KOSPI200"]    # study markets, pre-2010 only
BLOCKS = [(1998 + 2 * k, 1999 + 2 * k) for k in range(12)]                   # B1=1998-99 ... B12=2020-21
PAIRS = [(2 * k, 2 * k + 1) for k in range(6)]                               # P1=(B1,B2) ... P6=(B11,B12)
SAMPLE_B_MAX_BLOCK = 6                                                       # B1..B6 only (ends 2009)
MIN_GROUP = 20
MAX_GAP_DAYS = 15
N_PERM = 10000
SEED = 20261116


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load(path):
    df = pd.read_csv(path, usecols=["Date", "Close"])
    df["Date"] = pd.to_datetime(df["Date"]).dt.normalize()
    df = df.dropna(subset=["Close"])
    df = df[df["Close"] > 0].sort_values("Date").drop_duplicates("Date", keep="first").reset_index(drop=True)
    return df


def block_status(df, y0, y1):
    """Eligibility of a calendar block, decided from dates only (no target outcomes)."""
    d = df["Date"]
    inside = df.index[(d >= pd.Timestamp(y0, 1, 1)) & (d <= pd.Timestamp(y1, 12, 31))]
    if len(inside) == 0:
        return False, "no sessions"
    first, last = inside[0], inside[-1]
    if first < 200:
        return False, "fewer than 200 sessions before block"
    if d[first] > pd.Timestamp(y0, 1, 15) or d[last] < pd.Timestamp(y1, 12, 15):
        return False, "block not fully covered"
    gaps = d[first:last + 1].diff().dt.days.max()
    if gaps > MAX_GAP_DAYS:
        return False, f"gap of {int(gaps)} calendar days"
    return True, "ok"


def eligible_rows(df, y0, y1, with_target):
    """Forecast dates t in the block whose t+20 session also lies in the block. Signals use t-1 (common cutoff)."""
    C = df["Close"].to_numpy()
    d = df["Date"]
    end = pd.Timestamp(y1, 12, 31)
    out = []
    idx = df.index[(d >= pd.Timestamp(y0, 1, 1)) & (d <= end)]
    for t in idx:
        prev = t - 1
        if prev - 199 < 0 or t + H >= len(df) or d[t + H] > end:
            continue
        rec = {"Date": d[t].date().isoformat(),
               "Persistence": int(C[prev] > C[prev - 20]),
               "200DMA": int(C[prev] > np.mean(C[prev - 199:prev + 1])),
               "Momentum60": int(C[prev] > C[prev - 60])}
        if with_target:
            rec["y"] = int(C[t + H] > C[t])
        out.append(rec)
    return pd.DataFrame(out)


def effect(rows, s):
    g0, g1 = rows[rows[s] == 0], rows[rows[s] == 1]
    if len(g0) < MIN_GROUP or len(g1) < MIN_GROUP:
        return float("nan"), len(g0), len(g1)
    return float(g1["y"].mean() - g0["y"].mean()), len(g0), len(g1)


def markets_blocks():
    for m in SAMPLE_A:
        yield m, "A", list(range(12))
    for m in SAMPLE_B:
        yield m, "B", list(range(SAMPLE_B_MAX_BLOCK))


def rho(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return float("nan"), int(ok.sum())
    return float(spearmanr(x[ok], y[ok])[0]), int(ok.sum())


def perm_p(pairs, s, obs):
    """One-sided (negative) within-market permutation: shuffle second-block E among a market's defined pairs."""
    rng = np.random.default_rng(SEED)
    sub = pairs.dropna(subset=[f"{s}_E1", f"{s}_E2"]).reset_index(drop=True)
    groups = [g.index.to_numpy() for _, g in sub.groupby("Market")]
    e1, e2 = sub[f"{s}_E1"].to_numpy(), sub[f"{s}_E2"].to_numpy()
    hits = 0
    for _ in range(N_PERM):
        z = e2.copy()
        for g in groups:
            z[g] = e2[rng.permutation(g)]
        hits += spearmanr(e1, z)[0] <= obs
    return (1 + hits) / (N_PERM + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--preflight", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    inv, blocks = [], []
    for m, sample, bl in markets_blocks():
        path = os.path.join(a.data, f"{m}.csv")
        if not os.path.exists(path):
            inv.append({"Market": m, "Sample": sample, "status": "file missing"})
            continue
        df = load(path)
        inv.append({"Market": m, "Sample": sample, "sha256": sha256(path), "rows": len(df),
                    "first": df["Date"].iloc[0].date().isoformat(), "last": df["Date"].iloc[-1].date().isoformat()})
        for b in bl:
            y0, y1 = BLOCKS[b]
            ok, why = block_status(df, y0, y1)
            rec = {"Market": m, "Sample": sample, "Block": f"B{b + 1}", "Years": f"{y0}-{y1}", "Eligible": ok, "Reason": why}
            if ok:
                rows = eligible_rows(df, y0, y1, with_target=not a.preflight)
                rec["N"] = len(rows)
                for s in SIGNALS:
                    rec[f"{s}_N0"] = int((rows[s] == 0).sum())
                    rec[f"{s}_N1"] = int((rows[s] == 1).sum())
                    if not a.preflight:
                        rec[f"{s}_E"] = effect(rows, s)[0]
            blocks.append(rec)
    B = pd.DataFrame(blocks)
    json.dump(inv, open(os.path.join(a.out, "v16_inventory.json"), "w"), indent=2)
    if a.preflight:
        B.to_csv(os.path.join(a.out, "v16_preflight_block_counts.csv"), index=False)
        print("PREFLIGHT ONLY: dates and signal-group counts; no target labels computed.")
        return
    B.to_csv(os.path.join(a.out, "v16_block_effects.csv"), index=False)

    pr = []
    for m, sample, bl in markets_blocks():
        for k, (i, j) in enumerate(PAIRS):
            if j not in bl:
                continue
            r = {"Market": m, "Sample": sample, "Pair": f"P{k + 1}", "First": f"B{i + 1}", "Second": f"B{j + 1}"}
            for s in SIGNALS:
                for tag, b in (("E1", i), ("E2", j)):
                    row = B[(B.Market == m) & (B.Block == f"B{b + 1}")]
                    r[f"{s}_{tag}"] = float(row[f"{s}_E"].iloc[0]) if len(row) and f"{s}_E" in row and row["Eligible"].iloc[0] else float("nan")
            pr.append(r)
    P = pd.DataFrame(pr)

    # calendar-demeaned E: subtract the cross-market mean E of the same block (common-shock control)
    for s in SIGNALS:
        cm = B[B.Eligible].groupby("Block")[f"{s}_E"].mean()
        P[f"{s}_E1_cd"] = P[f"{s}_E1"] - P["First"].map(cm)
        P[f"{s}_E2_cd"] = P[f"{s}_E2"] - P["Second"].map(cm)
    P.to_csv(os.path.join(a.out, "v16_pairs.csv"), index=False)

    res = {"protocol": "V16", "run_date_utc": date.today().isoformat(), "n_perm": N_PERM, "seed": SEED}
    for s in SIGNALS:
        obs, n = rho(P[f"{s}_E1"], P[f"{s}_E2"])
        h = {"rho": obs, "N_pairs": n, "nominal_p": perm_p(P, s, obs) if np.isfinite(obs) else float("nan")}
        d = P.dropna(subset=[f"{s}_E1", f"{s}_E2"])
        h["sign_flip_fraction"] = float((np.sign(d[f"{s}_E1"]) != np.sign(d[f"{s}_E2"])).mean()) if len(d) else float("nan")
        h["calendar_demeaned_rho"] = rho(P[f"{s}_E1_cd"], P[f"{s}_E2_cd"])[0]
        c1 = d[f"{s}_E1"] - d.groupby("Market")[f"{s}_E1"].transform("mean")
        c2 = d[f"{s}_E2"] - d.groupby("Market")[f"{s}_E2"].transform("mean")
        h["market_centered_rho"] = rho(c1, c2)[0]
        h["sample_A_rho"] = rho(*[P[P.Sample == "A"][f"{s}_{t}"] for t in ("E1", "E2")])
        h["sample_B_rho"] = rho(*[P[P.Sample == "B"][f"{s}_{t}"] for t in ("E1", "E2")])
        h["leave_one_market_out"] = {m: rho(*[P[P.Market != m][f"{s}_{t}"] for t in ("E1", "E2")])[0] for m in P.Market.unique()}
        h["leave_one_pair_out"] = {p: rho(*[P[P.Pair != p][f"{s}_{t}"] for t in ("E1", "E2")])[0] for p in P.Pair.unique()}
        wm = {}
        for m, g in d.groupby("Market"):
            if len(g) >= 4:
                wm[m] = rho(g[f"{s}_E1"], g[f"{s}_E2"])[0]
        h["within_market_rho_markets_with_4plus_pairs"] = wm
        h["within_market_negative_count"] = [int(sum(v < 0 for v in wm.values())), len(wm)]
        res[s] = h

    p1 = res["200DMA"]
    if not np.isfinite(p1["rho"]):
        lab = "Not evaluable"
    elif p1["rho"] < 0 and p1["nominal_p"] < .05:
        lab = "Nominally supported under a non-exact permutation diagnostic"
    elif p1["rho"] < 0:
        lab = "Directionally consistent, nominally non-significant"
    else:
        lab = "Not supported in direction"
    res["H1_label"] = lab
    res["H1_complete_case_note"] = f"evaluated on {p1['N_pairs']} of {len(P)} planned pairs"
    p2 = sorted([(res[s]["nominal_p"], s) for s in ("Persistence", "Momentum60")])
    res["H2_Holm2"] = {p2[0][1]: min(1.0, 2 * p2[0][0]), p2[1][1]: min(1.0, max(2 * p2[0][0], p2[1][0]))}
    json.dump(res, open(os.path.join(a.out, "v16_results.json"), "w"), indent=2, default=float)
    print(json.dumps({"H1": res["H1_label"], "rho": p1["rho"], "p": p1["nominal_p"], "N": p1["N_pairs"]}, default=float))


if __name__ == "__main__":
    main()
