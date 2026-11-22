# Example texts to date and check

Three short, made-up texts that show what people date with SoulInTime: a contract clause, a letter, and an AI output.

**First, see how checking works:** open https://soulintime.com/check and check a real receipt (the Bitcoin whitepaper abstract, block 975352) in 60 seconds. No account, nothing to install.

| File | Who might date something like it | Why |
|---|---|---|
| [contract-clause.txt](contract-clause.txt) | A lawyer or small firm sending a draft | Show which exact version of a clause existed by the time it was sent |
| [letter.txt](letter.txt) | A person in a dispute | Show the letter existed by a certain time and has not changed since |
| [ai-output.txt](ai-output.txt) | A small AI team | Show a model answer was not edited after it was published |

## How to date your own version

1. Open https://soulintime.com/try and pick the file. Your browser makes its fingerprint (SHA-256); the file never leaves your device.
2. Keep the file and the proof file (`.ots`) together.
3. Send the receipt link to anyone. They check it for free, with no account, on the receipt page itself or with any OpenTimestamps client. To see a check first, open https://soulintime.com/check.

What a confirmed receipt shows, exactly: these exact bytes existed by this Bitcoin block. It does not show who wrote the text, that it is true, or any legal conclusion. Change one character and it no longer matches.

These example files have **not** been dated by us, so there is no receipt for them. Edit one, then date your own copy.

## Code examples (statements)

Every example makes the same request as the canonical signed-out curl and comments point back to it:

```sh
curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
```

| Example | Required input | Status | Produces an external statement? |
|---|---|---|---|
| [create_statement.py](create_statement.py) | a file path | runnable (Python 3, stdlib) | yes, when you run it |
| [create_statement.mjs](create_statement.mjs) | a file path | runnable (Node 18+) | yes, when you run it |
| [git-hook-post-commit.sh](git-hook-post-commit.sh) | a git repo with a commit | runnable if you install it | yes, one per commit (free: one per network per hour) |
| [github-action/release-statement.yml](github-action/release-statement.yml) | a published release with assets | valid YAML, **not enabled**, not published as an Action | yes, one per asset |
| [email-inbound.md](email-inbound.md) | one SHA-256 per message | sketch, not built | would, per sender |
| [share-target.md](share-target.md) | selected text or a shared file | sketch (bookmarklet runnable) | yes, when you run it |

A statement exists only after Bitcoin confirms (usually 1 to 6 hours). Pending is not a statement; a 429 is not a statement.
Check any statement offline with [../verifier](../verifier). Spec: [../SPEC-statement-v0.1.md](../SPEC-statement-v0.1.md).
