#!/usr/bin/env python3
"""SoulInTime statement verifier, sit-statement/0.1. One file, standard library only. Works offline.

  python3 verify_statement.py statement.json [--file FILE | --hash SHA256] [--ots proof.ots] [--key KEY.json]

Checks: (1) the statement shape; (2) sha256 of your file (or the hash you pass) equals statement.sha256;
(3) the Ed25519 signature over the RFC 8785 (JCS) canonical JSON of every field except sig, against the
published key (kid 0a64aa45b8ce17a7, below; or --key); (4) with --ots, sha256 of the .ots equals ots_sha256
and the .ots commits to statement.sha256. Then it prints the OpenTimestamps command that checks the block.
Exit 0 only when every check that ran passed. Pure-Python Ed25519 (RFC 8032) is used; if PyNaCl or
cryptography is installed it is used instead (faster, same answer).
"""
import argparse, base64, hashlib, json, sys

PUBLISHED_KEYS = {  # kid -> raw Ed25519 public key, base64url. Also at https://soulintime.com/protocol#statements and keys/ in the repo.
    "0a64aa45b8ce17a7": "GrcQ1ZzlNQAtU8GyezaWCmyFjzjP2NEknvkAd5CQXxc",
}
BASE = ["v", "sha256", "status", "block_height", "block_hash", "ots_sha256", "issued_at", "issuer", "kid", "sig"]

def b64u(s): return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))

def jcs(v):
    """RFC 8785 for the value types a statement uses (strings, integers, null, booleans, flat objects)."""
    if v is None: return "null"
    if v is True: return "true"
    if v is False: return "false"
    if isinstance(v, int): return str(v)
    if isinstance(v, str): return json.dumps(v, ensure_ascii=False)
    if isinstance(v, dict):
        keys = sorted(v, key=lambda k: k.encode("utf-16-be"))
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + jcs(v[k]) for k in keys) + "}"
    raise ValueError("unsupported JSON value in statement: %r" % (v,))

# ---- Ed25519 verify, RFC 8032 section 5.1.7 (pure Python, slow but small) ----
_p = 2**255 - 19; _L = 2**252 + 27742317777372353535851937790883648493
_d = -121665 * pow(121666, _p - 2, _p) % _p; _I = pow(2, (_p - 1) // 4, _p)
def _inv(x): return pow(x, _p - 2, _p)
def _xrecover(y):
    xx = (y * y - 1) * _inv(_d * y * y + 1); x = pow(xx, (_p + 3) // 8, _p)
    if (x * x - xx) % _p: x = x * _I % _p
    if (x * x - xx) % _p: raise ValueError("not a point")
    return x
_By = 4 * _inv(5) % _p; _B = (_xrecover(_By) % _p, _By)
if _B[0] & 1: _B = (_p - _B[0], _By)
def _ext(P): return (P[0], P[1], 1, P[0] * P[1] % _p)
def _add(P, Q):
    A = (P[1] - P[0]) * (Q[1] - Q[0]) % _p; B = (P[1] + P[0]) * (Q[1] + Q[0]) % _p
    C = 2 * P[3] * Q[3] * _d % _p; D = 2 * P[2] * Q[2] % _p; E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _p, G * H % _p, F * G % _p, E * H % _p)
def _mul(s, P):
    Q = (0, 1, 1, 0)
    while s:
        if s & 1: Q = _add(Q, P)
        P = _add(P, P); s >>= 1
    return Q
def _eq(P, Q): return (P[0] * Q[2] - Q[0] * P[2]) % _p == 0 and (P[1] * Q[2] - Q[1] * P[2]) % _p == 0
def _decode(b):
    if len(b) != 32: raise ValueError("bad point")
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    if y >= _p: raise ValueError("bad point")
    x = _xrecover(y)
    if (x & 1) != (b[31] >> 7): x = _p - x
    if x == 0 and (b[31] >> 7): raise ValueError("bad point")
    return (x, y, 1, x * y % _p)
def _pure_verify(pub, msg, sig):
    if len(sig) != 64: return False
    try: A = _decode(pub); R = _decode(sig[:32])
    except ValueError: return False
    S = int.from_bytes(sig[32:], "little")
    if S >= _L: return False
    h = int.from_bytes(hashlib.sha512(sig[:32] + pub + msg).digest(), "little") % _L
    return _eq(_mul(8 * S, _ext(_B)), _add(_mul(8, R), _mul(8 * h, A)))

def ed25519_verify(pub, msg, sig):
    try:
        from nacl.signing import VerifyKey  # optional: pip install pynacl
        VerifyKey(pub).verify(msg, sig); return True
    except ImportError: pass
    except Exception: return False
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        Ed25519PublicKey.from_public_bytes(pub).verify(sig, msg); return True
    except ImportError: pass
    except Exception: return False
    return _pure_verify(pub, msg, sig)

def shape_ok(st):
    if not isinstance(st, dict): return "not an object"
    want = BASE + (["reason"] if st.get("status") == "refused" else ["priority"] if st.get("priority") is True else [])
    if sorted(st) != sorted(want): return "fields are %s, expected %s" % (sorted(st), sorted(want))
    if st["v"] != "sit-statement/0.1": return "unknown version"
    hexok = lambda s: isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdef" for c in s)
    if not hexok(st["sha256"]) or not hexok(st["block_hash"]): return "sha256/block_hash must be 64 lowercase hex"
    if not isinstance(st["block_height"], int) or isinstance(st["block_height"], bool) or st["block_height"] <= 0: return "bad block_height"
    if st["status"] == "confirmed" and not hexok(st["ots_sha256"]): return "confirmed needs ots_sha256"
    if st["status"] == "refused" and (st["ots_sha256"] is not None or st.get("reason") not in ("not_found", "not_confirmed")): return "bad refusal"
    if st["status"] not in ("confirmed", "refused"): return "status must be confirmed or refused (pending is never a statement)"
    return None

def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("statement"); g = ap.add_mutually_exclusive_group()
    g.add_argument("--file"); g.add_argument("--hash"); ap.add_argument("--ots"); ap.add_argument("--key", help="JSON file {kid, public_key_b64u} to use instead of the built-in key")
    a = ap.parse_args()
    st = json.load(open(a.statement, encoding="utf-8"))
    if isinstance(st, dict) and isinstance(st.get("statement"), dict): st = st["statement"]
    ok = True
    def res(cond, msg):
        nonlocal ok; ok = ok and cond; print(("PASS " if cond else "FAIL ") + msg)
    err = shape_ok(st); res(err is None, "shape sit-statement/0.1" + ("" if err is None else ": " + err))
    if err: return 1
    if a.file:
        h = hashlib.sha256(open(a.file, "rb").read()).hexdigest(); res(h == st["sha256"], "sha256(file) = %s" % h)
    elif a.hash:
        res(a.hash.strip().lower() == st["sha256"], "given hash equals statement sha256")
    keys = dict(PUBLISHED_KEYS)
    if a.key:
        k = json.load(open(a.key)); keys = {k["kid"]: k["public_key_b64u"]}
    pub = b64u(keys[st["kid"]]) if st["kid"] in keys else None
    res(pub is not None, "key id %s is a published key" % st["kid"])
    if pub is not None:
        res(hashlib.sha256(pub).hexdigest()[:16] == st["kid"], "kid = first 16 hex of sha256(public key)")
        body = {k: v for k, v in st.items() if k != "sig"}
        res(ed25519_verify(pub, jcs(body).encode("utf-8"), b64u(st["sig"])), "Ed25519 signature over JCS(all fields but sig)")
    if a.ots:
        ob = open(a.ots, "rb").read()
        if st["status"] == "confirmed": res(hashlib.sha256(ob).hexdigest() == st["ots_sha256"], "sha256(.ots) = ots_sha256")
        res(len(ob) >= 65 and ob[33:65].hex() == st["sha256"], ".ots commits to statement sha256")
    if st["status"] == "confirmed":
        print("Block check (OpenTimestamps, needs a Bitcoin node or compare the merkle root by hand):")
        print("  ots verify -d %s %s" % (st["sha256"], a.ots or "proof.ots"))
        print("  expected: block %d, whose hash on any explorer is %s" % (st["block_height"], st["block_hash"]))
    else:
        print("Signed refusal: not confirmed (%s) as of block %d. Do not cite a block." % (st["reason"], st["block_height"]))
    print("RESULT: " + ("all checks passed" if ok else "FAILED"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
