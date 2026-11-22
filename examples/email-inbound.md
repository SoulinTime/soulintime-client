# Email inbound: sketch only (not built, no address exists)

Idea: hash in, statement out, by email. Nothing here is live; there is no inbound address.

1. A sender mails a message whose subject is a 64-hex SHA-256 (or attaches a file; only its SHA-256 would be kept).
2. A mail worker makes the same request as the canonical curl:
   `curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" -d "{\"sha256Hash\":\"<sha256>\"}"`
3. It replies at once with the receipt (pending is not a statement) and the export link `https://soulintime.com/statement?hash=<sha256>`.
4. A second reply goes out when `GET /functions/v1Statement?hash=<sha256>` returns `"status":"confirmed"`, with the statement JSON attached.

Open questions before building: abuse limits per sender, whether to keep the sender address at all (default: no), and attachment size.
Required input: one SHA-256 per message. It would produce an external statement for each sender.
