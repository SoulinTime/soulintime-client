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
Spec: [../SPEC-statement-v0.1.md](../SPEC-statement-v0.1.md).
