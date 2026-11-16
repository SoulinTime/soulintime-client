# Reply template: OpenTimestamps thread (draft, not posted)

Use only on an exact fit: someone asks how to check an OTS proof or whether a hash is confirmed, and a hosted read-only check helps. Max two replies a week, as MorrisMoe. Hold if unsure.

---

If you want a read-only check without running a node, this returns the status for one hash; the .ots it points to still verifies with the stock client:

```
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected: `"status":"confirmed","blockHeight":965906` and a `proofFile`. Change one byte and it returns not_found:

```
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

That shows these exact bytes existed by that Bitcoin block, nothing more; `ots verify -d <hash> proof.ots` checks it without us.
