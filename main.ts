import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entrypoint: copy the finished front page to the scoring output dir.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png missing: run draw_frontpage.py first");
}
copyFileSync(src, join(outDir, "entry.png"));
// Integrity check: the delivered copy must be byte-identical in size.
if (statSync(join(outDir, "entry.png")).size !== statSync(src).size) {
  throw new Error("entry.png copy size mismatch");
}
console.log("wrote", join(outDir, "entry.png"));
