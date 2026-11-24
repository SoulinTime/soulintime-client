# Reference verifier (sit-statement/0.1)

One file each, no dependencies, offline.

```sh
python3 verify_statement.py examples/whitepaper.statement.json --file ../whitepaper-abstract.txt --ots whitepaper.ots
node verify_statement.mjs examples/door.statement.json --hash 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f --ots door.ots
```

Get the `.ots` files: `curl -L -o door.ots "https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1"`,
`curl -L -o whitepaper.ots "https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1"`.

It checks the statement shape, the file hash, the Ed25519 signature against the published key (built in; `--key` to use another),
and with `--ots` that the `.ots` bytes match `ots_sha256`. It then prints the `ots verify` command that checks the Bitcoin block.
Python: pure-Python Ed25519 (RFC 8032) by default; uses PyNaCl or `cryptography` automatically when installed. JS: Node 18+ WebCrypto.
Expected last line: `RESULT: all checks passed` (exit 0). A changed byte, height or signature prints `RESULT: FAILED` (exit 1).
Spec: [../SPEC-statement-v0.1.md](../SPEC-statement-v0.1.md) (hosted copy: https://soulintime.com/sit-statement-0.1.md). Both verifiers implement it with zero SoulInTime dependency: no network call, the key built in.
In a browser: [survives/index.html](survives/index.html), one self-contained page that verifies a statement with soulintime.com blocked.

## Test vectors

| file | sha256 | verifier must return |
|---|---|---|
| [vectors/valid.statement.json](vectors/valid.statement.json) | `c1d6179122a4ecffc97dbdd67bffbc5b278bd904217c17d97ef43802668181ff` | exit 0 |
| [vectors/tampered.statement.json](vectors/tampered.statement.json) | `28d6a62e26a485466e65b648fdfe8894ddd82e50e664883bff3afb2fb14e802e` | exit 1 (block_height changed) |
| [vectors/wrong-key.statement.json](vectors/wrong-key.statement.json) | `2e41bbe6a658ee81057e28a08c6ebae5d917d9a6c709bb04959ef1581e2b533e` | exit 1 (signed by a throwaway key) |
| [vectors/refused.statement.json](vectors/refused.statement.json) | `eece91ebf958efa2cb982953979d01d4a2699ff5c4064e1201a3d1a62e0f3f17` | exit 0, status refused (a signed refusal; never cite a block from it) |

```sh
for v in valid tampered wrong-key refused; do python3 verify_statement.py vectors/$v.statement.json >/dev/null; echo "$v $?"; done
```

Release hashes: [RELEASE.md](RELEASE.md). The verifier needs only the statement, the file (or its hash), the `.ots` and public Bitcoin data; it makes no network call.

## If soulintime.com disappears (tested 23 Nov 2026)

With soulintime.com blocked on the test machine (`/etc/hosts`, every request failed), both verifiers checked the Door (block 965906), the Bitcoin whitepaper abstract (975352) and the signing-key fingerprint (977076) from saved files: `RESULT: all checks passed`, exit 0, with `--hash` and `--ots`. `ots --no-bitcoin verify -d <sha256> <file>.ots` printed each block's merkle root, and all three matched a public block explorer. What you need saved: the statement JSON, the `.ots`, and the file (or its SHA-256). The signing key is built into both verifiers and in [../keys/](../keys/).
