# SoulInTime reference client — existence by Bitcoin height only. Not truth.
# Hash locally.
# POST the hash only.
# Poll until confirmed or failed, then save the .ots.
# This is sufficient for existence-by-height.
# SoulInTime reference client. Standard library only. Hash locally, POST the hash, poll until terminal, save the .ots.
# HARD RULE: a height is proven only when status == "confirmed" and proofFile exists. height_asserted is not proof.
# Unlisted receipts are excluded from Firsts and from atOrBefore results.
# On 429, respect the X-RateLimit-Reset header (Unix seconds) before retrying. Do not tight-loop.
# A 429 with reason already_stamped will not clear: do not retry; read the slug in the reply.
import argparse, hashlib, json, sys, time, urllib.error, urllib.request
F = "https://soulintime.com/functions/"
def call(url, body=None):
    req = urllib.request.Request(url, data=body and json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b"{}")
p = argparse.ArgumentParser()
p.add_argument("file", help="path, or - for raw bytes on stdin"); p.add_argument("--at-or-before", type=int); p.add_argument("--context-pack", action="store_true")
p.add_argument("--timeout", type=int, default=6 * 3600)
a = p.parse_args()
h = hashlib.sha256(sys.stdin.buffer.read() if a.file == "-" else open(a.file, "rb").read()).hexdigest()  # the file bytes never leave this machine
s, r = call(F + "createMoment", {"sha256Hash": h})
if s == 400: sys.exit("400: %s" % r.get("error"))
if s == 429: print("429: %s slug=%s" % (r.get("error"), r.get("slug")))
elif s >= 300: sys.exit("%d: %s" % (s, r))
end, wait = time.time() + a.timeout, 60
while True:
    s, v = call(F + "v1Verify?hash=" + h)
    st = v.get("status")
    if st in ("confirmed", "failed", "archived_failed") or time.time() > end: break
    print("status:", st or s, "- waiting", wait, "s"); time.sleep(wait); wait = min(wait * 2, 1800)
ok = st == "confirmed" and bool(v.get("proofFile"))
if v.get("proofFile"):
    with urllib.request.urlopen(v["proofFile"], timeout=60) as r: open((v.get("slug") or h) + ".ots", "wb").write(r.read())
    print("saved .ots")
print(json.dumps(v, indent=1))
print("CONFIRMED: these bytes existed by height %s" % v["blockHeight"] if ok else "NOT PROVEN: status %s. Do not cite a height." % st)
if a.at_or_before: print(json.dumps(call(F + "v1FirstAt?hash=%s&atOrBefore=%d" % (h, a.at_or_before))[1], indent=1))
if a.context_pack:
    rec = {k: v[k] for k in ("slug", "proofFile", "status") if v.get(k)}; rec["hash"] = h
    if ok: rec["blockHeight"] = v["blockHeight"]
    print(json.dumps({"schema": "soulintime.pack", "v": 1, "receipts": [rec]}))
