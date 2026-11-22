#!/usr/bin/env python3
"""createStatement (Python, standard library only). Example, not a package.

Same request as the canonical signed-out curl:
  curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" \
       -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"

Usage: python3 create_statement.py FILE [--wait]
Input: a file path (only its SHA-256 is sent, never the file).
Output: the receipt JSON now; with --wait, polls (every 10 minutes, at most 12 hours) until the signed statement exists
and writes it to FILE.statement.json. A 429 (rate_limited or already_stamped) is not a statement and is not retried.
Run by you, from your network, this produces an external statement once Bitcoin confirms.
"""
import hashlib, json, sys, time, urllib.request, urllib.error

API = "https://soulintime.com/functions"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def request(url, body=None, client="create_statement.py"):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="POST" if body is not None else "GET",
                                 headers={"Content-Type": "application/json", "X-SoulInTime-Client": client})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b"null"), r.headers
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null"), e.headers

def create_statement(path, wait=False):
    digest = sha256_file(path)
    status, body, headers = request(API + "/createMoment", {"sha256Hash": digest})
    print(json.dumps({"http": status, "request_id": headers.get("X-SoulInTime-Request-Id"), "receipt": body}))
    if status == 429:
        return None  # rate_limited or already_stamped: never a statement; do not retry in a loop
    if not wait:
        return None
    deadline = time.time() + 12 * 3600
    while time.time() < deadline:
        s, st, _ = request(API + "/v1Statement?hash=" + digest)
        if s == 200 and isinstance(st, dict) and st.get("status") == "confirmed":
            with open(path + ".statement.json", "w") as f:
                json.dump(st, f, separators=(",", ":"))
            print("statement:", json.dumps(st))
            print("export: https://soulintime.com/statement?hash=" + digest)
            return st
        time.sleep(600)  # pending is not a statement; check again in 10 minutes
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    create_statement(sys.argv[1], "--wait" in sys.argv)
