# Spec: Telegram bot (first insertion point) — spec only, not built

Status: spec. Not live. Building it needs a bot token from Telegram's BotFather, which needs a Telegram account; we do not have one yet.

Why Telegram first: a bot can be made without a phone business account or app review, and forwarding a file or a line to a bot is one step for the user.

## What it does
1. **Check (free).** The user sends a SHA-256, a file, or a line. The bot hashes on its side if it received bytes, then calls the existing read-only verify:
   `curl -s "https://soulintime.com/functions/v1Verify?hash=<sha256>"`
   - `status` confirmed with a `proofFile`: reply "These exact bytes existed by Bitcoin block N" + the receipt link + the .ots link.
   - Anything else (pending, in_calendar, not_found, 429): reply "Not confirmed. Do not cite a height for this hash." No height is ever shown before confirmed.
2. **Create (spends one stamp).** `/date` on a forwarded file or line calls the existing create path for the linked account. Reply: the receipt link and "Pending until a calendar attests it in a Bitcoin block, which takes minutes to hours."
3. **No stamps left:** reply with https://soulintime.com/pricing only.

## The file
Telegram delivers forwarded files to the bot, so the bot receives the bytes. The bot says so in one plain sentence on first use: "To hash a file, this bot receives it from Telegram, hashes it, and does not keep it." Sending a SHA-256 or using `/check <hash>` avoids sending the file at all.

## Account link (simplest)
A one-time code: the signed-in user opens https://soulintime.com/account, gets a short code, and sends `/link <code>` to the bot. No new account system, no passwords in chat. Check needs no link.

## Never
- Never claims the content is true, who made it, or where anyone was.
- Never shows a height before status is confirmed with a proofFile.
- No background folder watcher. No Gmail, WhatsApp or Drive in the same app.

## Readiness
Insertion point: spec. Bot: NEED (BotFather token).
