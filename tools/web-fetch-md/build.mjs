#!/usr/bin/env node
import { build } from "esbuild";
import { createRequire } from "node:module";
import { chmodSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, "../..");
const shippedSkillScript = resolve(repoRoot, "skills/web-fetch-to-markdown/scripts/fetchmd.js");
const agentsLauncher = resolve(repoRoot, ".agents/skills/web-fetch-to-markdown/scripts/fetchmd.js");

function replaceOnceOrThrow(source, pattern, replacement, label) {
  if (!pattern.test(source)) {
    throw new Error(`Build patch did not match: ${label}`);
  }
  return source.replace(pattern, replacement);
}

await build({
  entryPoints: ["src/fetchmd.ts"],
  bundle: true,
  platform: "node",
  target: "node20",
  format: "cjs",
  outfile: shippedSkillScript,
  minify: true,
  legalComments: "none",
  plugins: [
    {
      name: "jsdom-fixes",
      setup(b) {
        // 1. Inline jsdom's default stylesheet CSS so the shipped bundle is self-contained.
        b.onLoad({ filter: /computed-style\.js$/, namespace: "file" }, (args) => {
          const src = readFileSync(args.path, "utf8");
          const cssPath = resolve(dirname(args.path), "../../../browser/default-stylesheet.css");
          const css = readFileSync(cssPath, "utf8");
          const contents = replaceOnceOrThrow(
            src,
            /fs\.readFileSync\(\s*path\.resolve\(__dirname,\s*["'][^"']*default-stylesheet\.css["']\s*\),\s*\{[^}]*\}\s*\)/,
            JSON.stringify(css),
            "jsdom computed-style default stylesheet",
          );
          return { contents, loader: "js" };
        });

        // 2. Stub the sync-XHR worker path — synchronous XHR is never used here.
        b.onLoad({ filter: /XMLHttpRequest-impl\.js$/, namespace: "file" }, (args) => {
          const src = readFileSync(args.path, "utf8");
          const contents = replaceOnceOrThrow(
            src,
            /require\.resolve\(["']\.\/xhr-sync-worker\.js["']\)/,
            '"__xhr_sync_worker_unavailable__"',
            "jsdom XMLHttpRequest sync worker",
          );
          return { contents, loader: "js" };
        });

        // 3. css-tree uses createRequire(import.meta.url) to load JSON data files.
        //    In CJS bundles import.meta.url is undefined, so inline the JSON at build time.
        b.onLoad({ filter: /css-tree\/lib\/(version|data|data-patch)\.js$/, namespace: "file" }, (args) => {
          const src = readFileSync(args.path, "utf8");
          const fileDir = dirname(args.path);
          const scopedRequire = createRequire(args.path);

          let contents = replaceOnceOrThrow(
            src,
            /^import \{ createRequire \} from ['"]module['"];\n/m,
            "",
            `css-tree createRequire import (${args.path})`,
          );
          contents = replaceOnceOrThrow(
            contents,
            /^const require = createRequire\(import\.meta\.url\);\n/m,
            "",
            `css-tree createRequire call (${args.path})`,
          );

          let replacedJsonReads = 0;
          contents = contents.replace(/require\(['"]([^'"]+\.json)['"]\)/g, (_match, jsonPath) => {
            replacedJsonReads += 1;
            let fullPath;
            try {
              fullPath = jsonPath.startsWith(".")
                ? resolve(fileDir, jsonPath)
                : scopedRequire.resolve(jsonPath);
            } catch {
              fullPath = resolve(fileDir, jsonPath);
            }
            return readFileSync(fullPath, "utf8").trim();
          });

          if (replacedJsonReads === 0) {
            throw new Error(`Build patch did not inline css-tree JSON for: ${args.path}`);
          }

          return { contents, loader: "js" };
        });
      },
    },
  ],
});

// Rewrite the internal `.agents/` launcher as a thin shim that delegates to
// the shipped skill bundle. The launcher is only used by agents running inside
// this repo; it is not part of the distributed skill.
mkdirSync(dirname(agentsLauncher), { recursive: true });
writeFileSync(
  agentsLauncher,
  [
    "#!/usr/bin/env node",
    "const path = require('node:path');",
    "require(path.resolve(__dirname, '../../../../skills/web-fetch-to-markdown/scripts/fetchmd.js'));",
    "",
  ].join("\n"),
  "utf8",
);

chmodSync(shippedSkillScript, 0o755);
chmodSync(agentsLauncher, 0o755);
