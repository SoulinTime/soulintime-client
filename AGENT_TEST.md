# Agent test

Two read-only curls. No API key, no account. Neither creates anything.

## 1. Door (permanent test object)

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expect: `"status":"confirmed"`, `"blockHeight":965906`, `"slug":"a-hash-is-a-door-that-2026-019bd305"`, and a `proofFile`.
.ots: https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1

## 2. Bitcoin whitepaper abstract

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa"
```

Expect: `"status":"confirmed"`, `"blockHeight":975352`, `"slug":"moment-ao91b5a0"`, and a `proofFile`.
.ots: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1

## Rule

Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

Pass = both cite (`a-hash-is-a-door-that-2026-019bd305@965906`, `moment-ao91b5a0@975352`), and any pending or unknown hash is refused.
The claim is only: these exact bytes existed by this Bitcoin block. The .ots verifies without this site.
