# Fingerprint stamp

`keys/fingerprint.txt` (the kid, public key and fingerprint of signing key `0a64aa45b8ce17a7`) was dated to Bitcoin on 22 Nov 2026.

- sha256 of `keys/fingerprint.txt`: `8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25`
- Receipt: https://soulintime.com/moment/moment-sl6wqxcz (unlisted), submitted to the OpenTimestamps calendars 22 Nov 2026 16:37 UTC.
- Status when this file was written: in_calendar (pending). Pending is not a statement. Check it yourself:
  `curl -s "https://soulintime.com/functions/v1Verify?hash=8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25"`
  Once it is confirmed: `sha256sum keys/fingerprint.txt`, download the `.ots` (`proofFile` in that answer) and run
  `ots verify -d 8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25 proof.ots`.
