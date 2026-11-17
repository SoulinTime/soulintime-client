# Spec: browser extension "Date this" — second insertion point, spec only

Status: spec. Not built in this pass (the Telegram bot spec comes first).

- **Where:** a "Date this" item on a download or share (context menu on a link or a downloaded file).
- **Hash on device:** the extension computes SHA-256 locally with WebCrypto. Only the hash is sent.
- **Check stays free:** "Check this" calls `https://soulintime.com/functions/v1Verify?hash=<sha256>` and shows a block only when status is confirmed with a proofFile; otherwise "Not confirmed. Do not cite."
- **Create spends a stamp** from the signed-in account's balance (existing create path). Reply: the receipt link, shown as pending.
- **No stamps:** open https://soulintime.com/pricing.
- No tracking, no history upload, no page-content reading beyond the item the user picked.
