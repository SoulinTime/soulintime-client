# The receipt survives us

`index.html` is one self-contained page (no build, no dependencies, no request to soulintime.com). Open it from disk,
block soulintime.com, and press "Verify the built-in Door statement", or pick your own statement JSON, its `.ots`
and optionally the original file. It checks the sit-statement/0.1 shape, the Ed25519 signature over JCS against the
built-in key `0a64aa45b8ce17a7`, the `.ots` digest, and replays the `.ots` to the Bitcoin attestation. It prints the
merkle root that block must have; compare it with any block explorer or your own node.

Tested 24 Nov 2026 with soulintime.com blocked (headless Chrome, `file://`): `RESULT: all checks passed`, zero requests
to soulintime.com; block 965906 merkle root `741974c490b6cc6b0b89f2d82cc676b5a0a0fce9ad1e95b8640f82f2f6a7e9d7`, the same
as `ots --no-bitcoin verify` and mempool.space. A changed block height, signature or `.ots` byte prints `RESULT: FAILED`.

Spec: [../../SPEC-statement-v0.1.md](../../SPEC-statement-v0.1.md) (hosted copy: https://soulintime.com/sit-statement-0.1.md).
Hosted copy of this page: https://soulintime.com/survives.html
