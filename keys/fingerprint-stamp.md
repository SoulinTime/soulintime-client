# Fingerprint stamp

`keys/fingerprint.txt` (the kid, public key and fingerprint of signing key `0a64aa45b8ce17a7`) was dated to Bitcoin on 22 Nov 2026.

- sha256 of `keys/fingerprint.txt`: `8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25`
- Receipt: https://soulintime.com/moment/moment-sl6wqxcz (unlisted), submitted to the OpenTimestamps calendars 22 Nov 2026 16:37 UTC.
- Confirmed at Bitcoin block 977076 (block hash `000000000000000000016405e083d74defc2c21a5bd228ab6bf4d14976436b09`); signed statement issued on confirmation, 22 Nov 2026 17:40 UTC:
  `curl -s "https://soulintime.com/functions/v1Statement?hash=8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25"`
- Check it yourself:
  `curl -s "https://soulintime.com/functions/v1Verify?hash=8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25"`
  Then: `sha256sum keys/fingerprint.txt`, download the `.ots` (`proofFile` in that answer) and run
  `ots verify -d 8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25 proof.ots`.
