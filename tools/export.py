"""Build data/offers.json and data/history.json from an ArtifactData export.

Usage: python3 tools/export.py <export_dir>
<export_dir> holds offers/<id>.json and (optionally) history/<id>.json,
as written by ArtifactData list with out_dir.
"""
import glob, json, os, sys

src = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def docs(coll):
    out = {}
    for f in sorted(glob.glob(os.path.join(src, coll, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        out[os.path.basename(f)[:-5]] = d.get("data", d) if isinstance(d, dict) else d
    return out

offers = []
for key, v in docs("offers").items():
    if not isinstance(v, dict) or not v.get("kind") or not v.get("cls"):
        continue
    v = dict(v); v["_key"] = key
    offers.append(v)
if len(offers) < 20:
    sys.exit("too few offers (%d), not writing" % len(offers))
history = {k: v["points"] for k, v in docs("history").items() if isinstance(v, dict) and v.get("points")}

def write(name, obj):
    with open(os.path.join(root, "data", name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))

write("offers.json", offers)
write("history.json", history)
print("offers:", len(offers), "history:", len(history))
