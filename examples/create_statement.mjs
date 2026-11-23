// createStatement (JavaScript, Node 18+, no dependencies). Example, not a package.
// Same request as the canonical signed-out curl:
//   curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" \
//        -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
// Usage: node create_statement.mjs FILE [--wait | --watch]   (--watch: create nothing, only poll an existing receipt)
// Input: a file path (only its SHA-256 is sent). Output: the receipt now; with --wait, the signed statement once Bitcoin confirms.
// A 429 (rate_limited or already_stamped) is not a statement and is not retried. Run by you, this produces an external statement.
import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";

const API = "https://soulintime.com/functions";
const headers = { "Content-Type": "application/json", "X-SoulInTime-Client": "create_statement.mjs" };

export async function createStatement(path, { wait = false, watch = false } = {}) {
  const sha256Hash = createHash("sha256").update(await readFile(path)).digest("hex");
  if (watch) return poll(path, sha256Hash);
  const r = await fetch(`${API}/createMoment`, { method: "POST", headers, body: JSON.stringify({ sha256Hash }) });
  const receipt = await r.json().catch(() => null);
  console.log(JSON.stringify({ http: r.status, request_id: r.headers.get("X-SoulInTime-Request-Id"), receipt }));
  if (r.status === 429 || !wait) return null; // 429 is never a statement
  return poll(path, sha256Hash);
}

async function poll(path, sha256Hash) {
  const deadline = Date.now() + 12 * 3600e3;
  while (Date.now() < deadline) {
    const s = await fetch(`${API}/v1Statement?hash=${sha256Hash}`);
    const st = await s.json().catch(() => null);
    if (s.status === 200 && st?.status === "confirmed") {
      await writeFile(`${path}.statement.json`, JSON.stringify(st));
      console.log("statement:", JSON.stringify(st));
      const c = await fetch(`${API}/v1Statement?hash=${sha256Hash}&format=cite`);
      if (c.status === 200) console.log("cite:", (await c.text()).trim()); // paste as-is, on one line
      console.log(`statement_url: https://soulintime.com/statement?hash=${sha256Hash}`);
      return st;
    }
    await new Promise((res) => setTimeout(res, 600e3)); // pending is not a statement
  }
  return null;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  if (!process.argv[2]) { console.error("usage: node create_statement.mjs FILE [--wait | --watch]"); process.exit(2); }
  await createStatement(process.argv[2], { wait: process.argv.includes("--wait"), watch: process.argv.includes("--watch") });
}
