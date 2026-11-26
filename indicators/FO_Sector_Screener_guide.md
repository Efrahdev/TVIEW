# F&O Sector OI Screener 1.00 — how to use it (26 Nov 2026)

Files (all in `indicators/`):
- `FO_Sector_Screener_1.00.txt` — the screener indicator (put it in your Favourites, then pick it in the Pine Screener).
- `FO_Sector_Check_1.00.txt` — a chart helper that finds a bad ticker in the sector table.
- `sector_universe/FO_Sector_Universe_2026-11.csv` — the 176 stocks, 20 sectors and reference prices.
  `gen_sector_block.py` turns it into the SECTOR TABLE block inside both scripts.

**Status: NOT TESTED ON TRADINGVIEW.** The TradingView test tool hit its daily limit. The stock columns use the same
OI method as your FCOI Screener. The sector columns rely on formula symbols, which are still unconfirmed.

## First run (10 minutes, once)
1. Add `FO_Sector_Check_1.00` to any NSE 15-min chart. Every sector should read **OK** for the OI formula and then the
   price formula. For any **EMPTY** sector, switch to "One sector's stocks", enter its code, and send me the ticker
   showing **NOT FOUND**. I then fix the CSV and regenerate.
   If *every* sector is EMPTY, TradingView refuses `_OI` formulas: switch "Sector columns" off in the screener.
   The stock columns still work.
2. Add `FO_Sector_Screener_1.00` to a 15-min chart of, say, HDFCBANK. Check its table against what you see on NSE,
   especially **OI ₹ cr**. It assumes TradingView's OI is in shares.
3. In the Pine Screener: pick your F&O watchlist, 15 min, this indicator.

## The views (each is one filter and/or one sort)

| View | Filter | Sort |
|---|---|---|
| **Sector board**: one row per sector, ranked | Sector row = 1 | Sec OI % high→low |
| **Sector tree**: sectors ranked, stocks grouped under them | — | Group key high→low |
| **Open one sector** | Sector = code | OI % high→low |
| **Where OI is being added right now** | Sector row = 1 | Sec OI % last N high→low |
| **Fresh longs with conviction** | preset "Long build-up + high RVOL" | OI ₹ cr high→low |
| **Fresh shorts with conviction** | preset "Short build-up + high RVOL" | OI ₹ cr high→low |
| **Short covering** | preset "Short covering + high RVOL" | Price % high→low |
| **Quiet unwinding** | preset "Quiet OI decline" | OI % low→high |
| **Odd ones out** | preset "Against its sector" | vs Sector % |
| **Bull → bear spectrum** | — | Bias high→low |

Bias / Sec bias codes: +2 long build-up · +1 short covering · 0 neutral · −1 long unwinding · −2 short build-up.

Sector codes: 1 Private Banks · 2 PSU Banks · 3 NBFC and Lending · 4 Capital Markets and Insurance · 5 IT ·
6 Pharma and Healthcare · 7 Auto OEM · 8 Auto Components · 9 FMCG · 10 Metals and Mining · 11 Oil and Gas ·
12 Power · 13 Capital Goods and Defence · 14 Cement · 15 Realty · 16 Infra and Logistics · 17 Telecom ·
18 Consumer Durables · 19 Consumer Services · 20 Chemicals and Paints

## Rules: yours, filled gaps, and my additions
- **[YOURS]** Sector-level OI gained or lost, sector price move and sector RVOL beside each stock. Collapse into
  one row per sector, and rank the sectors with the most activity to the top.
- **[YOURS → not possible]** Sector advance/decline in a column: each row may fetch only 5 symbols, and a formula can
  add stocks up but cannot count how many rose. Use: filter Sector = code and Price % > 0, then read the row count.
- **[GAP, my default]** Measured from the previous day's close and the previous day's last OI print, as at the latest
  closed candle. RVOL is cumulative from 09:15 against the same time over 20 days (your tracker's 20 / min 5).
  Stock OI = near + next month, as in FCOI.
- **[GAP, my default]** Thresholds: stock price ±0.25%, stock OI ±1%, sector price ±0.25%, sector OI ±0.5%,
  high RVOL 150%. Last N = 3 candles. All are inputs.
- **[MINE]** The Group key (a sector → stock tree from one sort), the Sector row (collapse to one row per sector),
  Bias codes ordered from bull to bear, Sec OI % last N (is the adding happening now?), and comparisons with the
  sector and with Nifty.

## Known weak points
1. **Sector list and reference prices are from my knowledge (mid-2026), not checked against NSE today.** A renamed or
   dropped ticker empties its sector until fixed (the checker finds it). Reference prices are only weights: a
   wrong price tilts a stock's share of the sector total, but the % change stays a pure OI change.
2. **Roll morning:** the stock uses the shared contract (as FCOI). The sector total uses today's first print as the
   base (Data = 1). Expiry day itself shows OI falling by design.
3. **Sector RVOL** needs TradingView to give volume for formula symbols. If it doesn't, the column stays empty.
4. Stocks not in the table (Sector = 0) still get every stock column.
