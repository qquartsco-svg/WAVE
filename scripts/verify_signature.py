#!/usr/bin/env python3
import hashlib, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
SIG = ROOT / "SIGNATURE.sha256"
if not SIG.exists():
    print("SIGNATURE.sha256 not found"); sys.exit(1)
ok = fail = 0
for line in SIG.read_text().splitlines():
    if not line.strip(): continue
    expected, relpath = line.split("  ", 1)
    fp = ROOT / relpath
    if not fp.exists():
        print(f"MISSING  {relpath}"); fail += 1; continue
    h = hashlib.sha256(); h.update(fp.read_bytes())
    if h.hexdigest() == expected:
        print(f"OK       {relpath}"); ok += 1
    else:
        print(f"FAIL     {relpath}"); fail += 1
print(f"\n{ok} ok, {fail} fail")
sys.exit(1 if fail else 0)
