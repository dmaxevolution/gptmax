import json
import os
from datetime import datetime
import pandas as pd
import yfinance as yf

# Daftar Emiten IDX Pilihan Swing Trader (150+ Ticker)
TICKERS = [
    # Bluechip / Big Cap
    {"ticker": "BBCA", "category": "Bluechip"}, {"ticker": "BBRI", "category": "Bluechip"},
    {"ticker": "BMRI", "category": "Bluechip"}, {"ticker": "BBNI", "category": "Bluechip"},
    {"ticker": "TLKM", "category": "Bluechip"}, {"ticker": "ASII", "category": "Bluechip"},
    {"ticker": "UNVR", "category": "Bluechip"}, {"ticker": "ICBP", "category": "Bluechip"},
    {"ticker": "INDF", "category": "Bluechip"}, {"ticker": "AMRT", "category": "Bluechip"},
    {"ticker": "TPIA", "category": "Bluechip"}, {"ticker": "BREN", "category": "Bluechip"},
    {"ticker": "BYAN", "category": "Bluechip"}, {"ticker": "CPIN", "category": "Bluechip"},
    {"ticker": "KLBF", "category": "Bluechip"},

    # Energy, Mining & Metals
    {"ticker": "ADRO", "category": "IDX"}, {"ticker": "PTBA", "category": "IDX"},
    {"ticker": "ITMG", "category": "IDX"}, {"ticker": "MEDC", "category": "IDX"},
    {"ticker": "ANTM", "category": "IDX"}, {"ticker": "INCO", "category": "IDX"},
    {"ticker": "PGAS", "category": "IDX"}, {"ticker": "AKRA", "category": "IDX"},
    {"ticker": "HRUM", "category": "IDX"}, {"ticker": "MBMA", "category": "IDX"},
    {"ticker": "NCKL", "category": "IDX"}, {"ticker": "AMMN", "category": "IDX"},
    {"ticker": "CUAN", "category": "IDX"}, {"ticker": "DOID", "category": "IDX"},
    {"ticker": "INDY", "category": "IDX"}, {"ticker": "ELSA", "category": "IDX"},
    {"ticker": "ENRG", "category": "IDX"}, {"ticker": "BUMI", "category": "IDX"},
    {"ticker": "DEWA", "category": "IDX"}, {"ticker": "BRMS", "category": "IDX"},
    {"ticker": "HUMI", "category": "IDX"}, {"ticker": "BNBR", "category": "IDX"},
    {"ticker": "TINS", "category": "IDX"}, {"ticker": "PSAB", "category": "IDX"},

    # Banking & Financials
    {"ticker": "BRIS", "category": "IDX"}, {"ticker": "BBTN", "category": "IDX"},
    {"ticker": "BDMN", "category": "IDX"}, {"ticker": "BNGA", "category": "IDX"},
    {"ticker": "NISP", "category": "IDX"}, {"ticker": "PNBN", "category": "IDX"},
    {"ticker": "ARTO", "category": "IDX"}, {"ticker": "BBYB", "category": "IDX"},
    {"ticker": "BANK", "category": "IDX"}, {"ticker": "AGRO", "category": "IDX"},
    {"ticker": "BSIM", "category": "IDX"}, {"ticker": "MAYA", "category": "IDX"},

    # Telecom, Tech & Infrastructure
    {"ticker": "EXCL", "category": "IDX"}, {"ticker": "ISAT", "category": "IDX"},
    {"ticker": "TOWR", "category": "IDX"}, {"ticker": "TBIG", "category": "IDX"},
    {"ticker": "MTEL", "category": "IDX"}, {"ticker": "EMTK", "category": "IDX"},
    {"ticker": "SCMA", "category": "IDX"}, {"ticker": "BUKA", "category": "IDX"},
    {"ticker": "WIFI", "category": "IDX"}, {"ticker": "CENT", "category": "IDX"},
    {"ticker": "MLPT", "category": "IDX"}, {"ticker": "MTDL", "category": "IDX"},

    # Consumer & Healthcare
    {"ticker": "MYOR", "category": "IDX"}, {"ticker": "CMRY", "category": "IDX"},
    {"ticker": "ACES", "category": "IDX"}, {"ticker": "MAPI", "category": "IDX"},
    {"ticker": "MAPA", "category": "IDX"}, {"ticker": "RALS", "category": "IDX"},
    {"ticker": "LPPF", "category": "IDX"}, {"ticker": "ERAA", "category": "IDX"},
    {"ticker": "MIKA", "category": "IDX"}, {"ticker": "HEAL", "category": "IDX"},
    {"ticker": "SILO", "category": "IDX"}, {"ticker": "SIDO", "category": "IDX"},
    {"ticker": "TSPC", "category": "IDX"}, {"ticker": "KAEF", "category": "IDX"},
    {"ticker": "CLEO", "category": "IDX"}, {"ticker": "ULTJ", "category": "IDX"},
    {"ticker": "MEDS", "category": "IDX"}, 

    # Property & Construction
    {"ticker": "BSDE", "category": "IDX"}, {"ticker": "CTRA", "category": "IDX"},
    {"ticker": "PWON", "category": "IDX"}, {"ticker": "SMRA", "category": "IDX"},
    {"ticker": "ASRI", "category": "IDX"}, {"ticker": "ADHI", "category": "IDX"},
    {"ticker": "PTPP", "category": "IDX"}, {"ticker": "WIKA", "category": "IDX"},
    {"ticker": "TOTL", "category": "IDX"}, {"ticker": "DILD", "category": "IDX"},

    # Industrial & Agro
    {"ticker": "SMGR", "category": "IDX"}, {"ticker": "INTP", "category": "IDX"},
    {"ticker": "UNTR", "category": "IDX"}, {"ticker": "AUTO", "category": "IDX"},
    {"ticker": "GJTL", "category": "IDX"}, {"ticker": "SMSM", "category": "IDX"},
    {"ticker": "MAIN", "category": "IDX"}, {"ticker": "JPFA", "category": "IDX"},
    {"ticker": "TAPG", "category": "IDX"}, {"ticker": "DSNG", "category": "IDX"},
    {"ticker": "SSMS", "category": "IDX"}, {"ticker": "LSIP", "category": "IDX"},
    {"ticker": "AALI", "category": "IDX"}, {"ticker": "ASSA", "category": "IDX"},
    {"ticker": "CDIA", "category": "IDX"}, {"ticker": "JGLE", "category": "IDX"},
    {"ticker": "KOTA", "category": "IDX"}, {"ticker": "SIDO", "category": "IDX"}
]

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_swing_strategy(close, ema20, ema50, rsi):
    score = 0
    
    if close > ema20:
        ema20_status = "strong_buy" if close >= ema20 * 1.02 else "buy"
        score += 2 if ema20_status == "strong_buy" else 1
    elif close < ema20:
        ema20_status = "strong_sell" if close <= ema20 * 0.98 else "sell"
        score -= 2 if ema20_status == "strong_sell" else 1
    else:
        ema20_status = "neutral"

    if ema20 > ema50:
        ema50_status = "strong_buy" if close > ema50 else "buy"
        score += 2 if ema50_status == "strong_buy" else 1
    elif ema20 < ema50:
        ema50_status = "strong_sell" if close < ema50 else "sell"
        score -= 2 if ema50_status == "strong_sell" else 1
    else:
        ema50_status = "neutral"

    if rsi >= 65:
        rsi_status = "strong_buy"
        score += 2
    elif 50 <= rsi < 65:
        rsi_status = "buy"
        score += 1
    elif 30 <= rsi <= 40:
        rsi_status = "sell"
        score -= 1
    elif rsi < 30:
        rsi_status = "strong_sell"
        score -= 2
    else:
        rsi_status = "neutral"

    if score >= 4:
        signal = "STRONG_BULLISH"
    elif score >= 1:
        signal = "BULLISH"
    elif score <= -4:
        signal = "STRONG_BEARISH"
    elif score <= -1:
        signal = "BEARISH"
    else:
        signal = "NEUTRAL"

    power_score = min(10, max(1, round(((score + 5) / 10) * 10)))

    return {
        "ema20_status": ema20_status,
        "ema50_status": ema50_status,
        "rsi_status": rsi_status,
        "signal": signal,
        "power_score": power_score
    }

def fetch_real_data():
    symbol_map = {f"{item['ticker']}.JK": item for item in TICKERS}
    ticker_symbols = list(symbol_map.keys())
    all_download_tickers = ticker_symbols + ["^JKSE"]

    print("⚡ Mengunduh data emiten dan IHSG (^JKSE)...")
    download_data = yf.download(all_download_tickers, period="100d", interval="1d", group_by="ticker", progress=False)

    ihsg_data = {
        "name": "IHSG", "open": 0, "high": 0, "low": 0, "close": 0, "prev_close": 0, "change_pct": 0.0
    }

    try:
        if "^JKSE" in download_data and not download_data["^JKSE"].dropna().empty:
            df_ihsg = download_data["^JKSE"].dropna().copy()
            if len(df_ihsg) >= 2:
                latest_ihsg = df_ihsg.iloc[-1]
                prev_ihsg = df_ihsg.iloc[-2]
                c_val, p_val = float(latest_ihsg['Close']), float(prev_ihsg['Close'])
                chg = round(((c_val - p_val) / p_val) * 100, 2) if p_val > 0 else 0.0
                ihsg_data = {
                    "name": "IHSG",
                    "open": round(float(latest_ihsg['Open']), 2),
                    "high": round(float(latest_ihsg['High']), 2),
                    "low": round(float(latest_ihsg['Low']), 2),
                    "close": round(c_val, 2),
                    "prev_close": round(p_val, 2),
                    "change_pct": chg
                }
    except Exception as e:
        print(f"Gagal memuat IHSG: {e}")

    all_stocks = []
    for symbol, stock in symbol_map.items():
        try:
            if symbol in download_data and not download_data[symbol].dropna().empty:
                df = download_data[symbol].dropna().copy()
            else:
                continue

            if len(df) < 30:
                continue

            df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['RSI'] = calculate_rsi(df['Close'], 14)

            latest, previous = df.iloc[-1], df.iloc[-2]
            close, prev_close = float(latest['Close']), float(previous['Close'])
            
            if close <= 0 or prev_close <= 0:
                continue

            change_pct = round(((close - prev_close) / prev_close) * 100, 2)
            ema20, ema50 = float(latest['EMA20']), float(latest['EMA50'])
            rsi = round(float(latest['RSI']), 1) if not pd.isna(latest['RSI']) else 50.0

            swing_res = calculate_swing_strategy(close, ema20, ema50, rsi)

            # Hitung TP 2 Level dan Stop Loss
            stop_loss = round(close * 0.95, 2)
            tp1 = round(close * 1.05, 2)
            tp2 = round(close * 1.10, 2)

            # Status Sentuh TP/CL
            tp1_hit = close >= tp1
            tp2_hit = close >= tp2
            cl_hit = close <= stop_loss

            item = {
                "ticker": stock["ticker"],
                "close": round(close, 2),
                "change_pct": change_pct,
                "category": stock["category"],
                "ema20": round(ema20, 2),
                "ema20_status": swing_res["ema20_status"],
                "ema50": round(ema50, 2),
                "ema50_status": swing_res["ema50_status"],
                "rsi": rsi,
                "rsi_status": swing_res["rsi_status"],
                "signal": swing_res["signal"],
                "power_score": swing_res["power_score"],
                "stop_loss": stop_loss,
                "take_profit_1": tp1,
                "take_profit_2": tp2,
                "tp1_hit": tp1_hit,
                "tp2_hit": tp2_hit,
                "cl_hit": cl_hit
            }
            all_stocks.append(item)
        except Exception:
            continue

    # Mengurutkan berdasarkan Power Ranking Terbesar secara default
    all_stocks = sorted(all_stocks, key=lambda x: (x["power_score"], x["change_pct"]), reverse=True)

    top_bearish = sorted(all_stocks, key=lambda x: (x["power_score"], x["change_pct"]))[:20]
    top_10_entry = [s for s in all_stocks if s["signal"] in ["STRONG_BULLISH", "BULLISH"]][:10]

    swing_setup = [s for s in all_stocks if s["signal"] in ["BULLISH", "STRONG_BULLISH"]]
    top_gainers = sorted(all_stocks, key=lambda x: x["change_pct"], reverse=True)[:20]
    top_movers = sorted(all_stocks, key=lambda x: abs(x["change_pct"]), reverse=True)[:20]
    bluechips = [s for s in all_stocks if s["category"] == "Bluechip"]

    output = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "total_scanned": len(all_stocks),
        "ihsg": ihsg_data,
        "top_10_entry": top_10_entry,
        "swing_setup": swing_setup,
        "top_gainers": top_gainers,
        "top_movers": top_movers,
        "bluechips": bluechips,
        "top_bearish": top_bearish,
        "all_stocks": all_stocks
    }

    temp_filename, final_filename = "data.json.tmp", "data.json"
    with open(temp_filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    os.replace(temp_filename, final_filename)
    print(f"🚀 Berhasil! {len(all_stocks)} emiten tersimpan.")

if __name__ == "__main__":
    fetch_real_data()
