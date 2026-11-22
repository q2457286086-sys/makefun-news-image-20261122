import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

// Entrypoint: write the finished front page to the scoring output dir.
const root = new URL(".", import.meta.url).pathname;
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(destination, { recursive: true });

const source = path.join(root, "entry.png");
let bytes;
try {
  bytes = readFileSync(source);
} catch {
  throw new Error("entry.png missing: run draw_frontpage.py first");
}
const target = path.join(destination, "entry.png");
writeFileSync(target, bytes);

// Integrity check: the delivered copy must be byte-identical in size.
const delivered = readFileSync(target);
if (delivered.length !== bytes.length) {
  throw new Error("entry.png copy size mismatch");
}
console.log(`wrote ${target} (${bytes.length} bytes)`);
