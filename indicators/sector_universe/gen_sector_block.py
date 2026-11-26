# Generates the Pine "SECTOR TABLE" block for FO_Sector_Screener and FO_Sector_Check from the universe CSV.
# Usage: python3 gen_sector_block.py FO_Sector_Universe_2026-11.csv > block.pine
import csv, sys
from collections import OrderedDict

rows = list(csv.DictReader(open(sys.argv[1])))
secs = OrderedDict()
for r in rows:
    k = int(r["sector_code"])
    secs.setdefault(k, {"name": r["sector"], "m": []})["m"].append((r["ticker"], r["ref_price"]))

def g(p):  # keep prices compact: 980 not 980.0
    return p.rstrip("0").rstrip(".") if "." in p else p

out = []
out.append("// ── SECTOR TABLE: generated from " + sys.argv[1].split("/")[-1] + " by gen_sector_block.py. Edit the CSV, not this block. ──")
out.append('const string SEC_NAMES = "' + "|".join(["Not in list"] + [s["name"] for s in secs.values()]) + '"')
out.append('const string LEADERS   = ",' + ",".join(s["m"][0][0] for s in secs.values()) + ',"')
for k, s in secs.items():
    out.append(f'const string M_{k:02d} = ",' + ",".join(t for t, _ in s["m"]) + ',"')
for k, s in secs.items():
    out.append(f'const string OI_{k:02d} = "' + "+".join(f"NSE:{t}1!_OI*{g(p)}+NSE:{t}2!_OI*{g(p)}" for t, p in s["m"]) + '"')
for k, s in secs.items():
    out.append(f'const string PX_{k:02d} = "' + "+".join(f"NSE:{t}/{g(p)}" for t, p in s["m"]) + '"')
ks = list(secs.keys())
out.append("f_secOf(string tk) =>")
out.append("    string w = \",\" + tk + \",\"")
out.append("    " + " : ".join(f"str.contains(M_{k:02d}, w) ? {k}" for k in ks) + " : 0")
out.append("f_oiF(int s) =>")
out.append("    " + " : ".join(f"s == {k} ? OI_{k:02d}" for k in ks) + " : NOSYM")
out.append("f_pxF(int s) =>")
out.append("    " + " : ".join(f"s == {k} ? PX_{k:02d}" for k in ks) + " : NOSYM")
out.append("f_memF(int s) =>")
out.append("    " + " : ".join(f"s == {k} ? M_{k:02d}" for k in ks) + ' : ""')
out.append(f"const int SEC_N = {len(ks)}")
out.append("// ── END SECTOR TABLE ──")
print("\n".join(out))
sys.stderr.write("sectors=%d stocks=%d max_members=%d max_oi_symbols=%d\n" % (len(ks), len(rows), max(len(s["m"]) for s in secs.values()), 2 * max(len(s["m"]) for s in secs.values())))
