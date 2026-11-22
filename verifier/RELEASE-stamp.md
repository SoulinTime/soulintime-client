# Verifier release 0.1.0 — dated to Bitcoin

`sha256sum RELEASE.md` = `4e6987c64becdd4676c5d4e91c5a3ca2fb2a01ead7568524dbe952e0db0069a6` (RELEASE.md lists the hashes of both verifiers).

Requested 23 Nov 2026 with the canonical curl (house request, unlisted receipt `moment-urpa1fic`). Pending until Bitcoin confirms; then:

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=4e6987c64becdd4676c5d4e91c5a3ca2fb2a01ead7568524dbe952e0db0069a6"
```

returns the signed statement, and https://soulintime.com/statement?hash=4e6987c64becdd4676c5d4e91c5a3ca2fb2a01ead7568524dbe952e0db0069a6 is its export. Until then it is a receipt, not a statement.
