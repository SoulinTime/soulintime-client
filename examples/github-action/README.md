# GitHub Action example: a citable Bitcoin statement per release asset

Example only. It is not published as an Action and not enabled in any repository. Copy
[`release-statement.yml`](release-statement.yml) into your own repo as `.github/workflows/release-statement.yml`.

What it does on each published release:

1. Downloads the release assets and computes each `sha256` on the runner. Only the hash is sent.
2. Sends the free signed-out request, the same as the README curl. No account, no key; the first statement is free.
3. Prints one cite line per asset to the log, the job summary and the `cites` output.

Bitcoin confirmation takes about 1 to 6 hours, so a fresh release prints `pending`. Re-run the workflow later
(Run workflow, same tag) and confirmed assets print their cite line. Re-running does not create anything new.

## Expected responses

Request (`createMoment`), fresh hash, HTTP 200: a receipt, not yet a statement:

```
{"slug":"moment-…","proofFile":"https://soulintime.com/functions/v1Proof?id=moment-…&ots=1","status":"in_calendar"}
```

Same hash again before confirmation, HTTP 429, a refusal (never cite it):

```
{"error":"Already stamped or rate limited. Check the existing receipt.","reason":"already_stamped","statement":null,"cite":null,"do_not_cite":"No statement exists for this request. Do not cite a block for this hash.", ...}
```

Same hash again after confirmation, HTTP 429 `already_stamped` carrying the existing statement and its cite (no new receipt):

```
{"reason":"already_stamped","statement":{"v":"sit-statement/0.1", ...},"cite":"sha256 <hash> existed by Bitcoin block <N>. Statement: https://soulintime.com/statement?hash=<hash>", ...}
```

Cite (`v1Statement?hash=<hash>&format=cite`), confirmed, HTTP 200, one line of text:

```
sha256 <hash> existed by Bitcoin block <N>. Statement: https://soulintime.com/statement?hash=<hash>
```

Not yet confirmed: not HTTP 200, no cite line. The workflow prints `pending, no statement yet (do not cite)`, or `rate limited, not requested` for an asset refused with `rate_limited`.

Job log, real shape (the Door, block 965906):

```
door.txt: sha256 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f existed by Bitcoin block 965906. Statement: https://soulintime.com/statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
```

## PR or commit message template

Paste the cite line unchanged, on one line:

```
Release <tag>: <asset> statement

sha256 <hash> existed by Bitcoin block <N>. Statement: https://soulintime.com/statement?hash=<hash>

This says only that these exact bytes existed by that block, not who made them or that they are true.
Check offline: https://github.com/SoulinTime/soulintime-client/tree/main/verifier
```

Rate limit: one fresh hash per network per hour, signed out. GitHub-hosted runners share networks, so a
release with several assets may see `rate_limited` for some of them; re-run later. The job never fails on a 429.
