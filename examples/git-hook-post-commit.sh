#!/bin/sh
# Example git hook (not installed anywhere): request a statement for each new commit's tree listing.
# Copy to .git/hooks/post-commit and chmod +x. It sends only a SHA-256, never your code.
# Same request as the canonical signed-out curl (see the repo README). One fresh hash per network per hour is free;
# a 429 (rate_limited or already_stamped) is not a statement, so the hook just prints it and never retries.
set -eu
H=$(git ls-tree -r HEAD | sha256sum | cut -c1-64)
curl -s -X POST https://soulintime.com/functions/createMoment \
  -H "Content-Type: application/json" -H "X-SoulInTime-Client: git-hook-example" \
  -d "{\"sha256Hash\":\"$H\"}" || true
echo
echo "Later: curl -s \"https://soulintime.com/functions/v1Statement?hash=$H\"  (export: https://soulintime.com/statement?hash=$H)"
