# Scorecard format

Every Monday and in every closeout, these five lines, in this order:

```
Checkouts started: N
Checkouts completed: N
External whitepaper or /check hits: N (or "unknown")
Replies sent: N
Directories added: N
```

Then one sentence: the largest gap right now.

Notes:
- Checkouts started = Stripe Checkout sessions created from the /pricing buttons. Count our own test sessions separately and say so.
- External hits stay "unknown" until logging can tell outside visitors apart from ours. A hit seen by hand (a reply, an issue, a mention) counts and is noted with its link.
- Replies sent counts only replies posted in existing threads, at most two a day.
