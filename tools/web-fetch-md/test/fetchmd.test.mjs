import test from "node:test";
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { once } from "node:events";
import { spawn } from "node:child_process";
import { cp, mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(testDir, "..", "..", "..");
const packageJsonPath = path.join(repoRoot, "tools/web-fetch-md/package.json");
const shippedSkillDir = path.join(repoRoot, "skills/web-fetch-to-markdown");
const shippedSkillScript = path.join(shippedSkillDir, "scripts/fetchmd.js");
const launchers = [
  ".agents/skills/web-fetch-to-markdown/scripts/fetchmd.js",
  "skills/web-fetch-to-markdown/scripts/fetchmd.js",
];

async function withServer(handler, run) {
  const server = createServer(handler);
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address();
  if (!address || typeof address === "string") {
    throw new Error("Expected TCP server address");
  }
  const origin = `http://127.0.0.1:${address.port}`;
  try {
    await run(origin);
  } finally {
    server.close();
    await once(server, "close");
  }
}

async function runCli(launcherPath, url, cwd = repoRoot) {
  const cliPath = path.isAbsolute(launcherPath) ? launcherPath : path.join(repoRoot, launcherPath);
  const child = spawn(process.execPath, [cliPath, url], {
    cwd,
    stdio: ["ignore", "pipe", "pipe"],
  });

  let stdout = "";
  let stderr = "";
  child.stdout.setEncoding("utf8");
  child.stderr.setEncoding("utf8");
  child.stdout.on("data", (chunk) => {
    stdout += chunk;
  });
  child.stderr.on("data", (chunk) => {
    stderr += chunk;
  });

  const [code] = await once(child, "close");
  return { code, stdout, stderr };
}

test("package declares a Node runtime compatible with jsdom 29", async () => {
  const pkg = JSON.parse(await readFile(packageJsonPath, "utf8"));
  assert.equal(pkg.engines.node, ">=20.19.0");
});

test("shipped skill runtime is self-contained", async () => {
  const script = await readFile(shippedSkillScript, "utf8");
  assert.match(script, /Usage:|#!/);
  // The bundle must not reach back into the build source tree at runtime —
  // any reference would break installs that only copy `skills/web-fetch-to-markdown/`.
  assert.doesNotMatch(script, /tools\/web-fetch-md\//);
});

test("isolated installed skill prints help via plugin-root path", async () => {
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), "web-fetch-skill-"));
  const installedSkillDir = path.join(tempRoot, "web-fetch-to-markdown");

  try {
    await cp(shippedSkillDir, installedSkillDir, { recursive: true });
    const child = spawn(
      "bash",
      ["-c", 'bash "${CLAUDE_PLUGIN_ROOT}/scripts/fetchmd" --help'],
      {
        cwd: tempRoot,
        env: { ...process.env, CLAUDE_PLUGIN_ROOT: installedSkillDir },
        stdio: ["ignore", "pipe", "pipe"],
      },
    );

    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });

    const [code] = await once(child, "close");
    assert.equal(code, 0, `stderr:\n${stderr}`);
    assert.match(stdout, /Usage:/);
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});

test("fetchmd converts HTML pages containing tables without crashing", async (t) => {
  await withServer((_req, res) => {
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(`<!doctype html>
      <html>
        <head><title>Table Test</title></head>
        <body>
          <main>
            <article>
              <h1>Example Table</h1>
              <p>A simple table for regression coverage.</p>
              <table>
                <tr><th>Name</th><th>Value</th></tr>
                <tr><td>alpha</td><td>1</td></tr>
              </table>
            </article>
          </main>
        </body>
      </html>`);
  }, async (origin) => {
    for (const launcherPath of launchers) {
      await t.test(launcherPath, async () => {
        const { code, stdout, stderr } = await runCli(launcherPath, `${origin}/table`);
        assert.equal(code, 0, `stderr:\n${stderr}`);
        assert.match(stdout, /Example Table/);
        assert.match(stdout, /Name/);
        assert.match(stdout, /alpha/);
      });
    }
  });
});

test("fetchmd does not leak jsdom CSS parse warnings to stderr", async (t) => {
  await withServer((_req, res) => {
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(`<!doctype html>
      <html>
        <head>
          <title>Broken CSS</title>
          <style>body { color: red; } }</style>
        </head>
        <body>
          <main><p>Styled content</p></main>
        </body>
      </html>`);
  }, async (origin) => {
    for (const launcherPath of launchers) {
      await t.test(launcherPath, async () => {
        const { code, stdout, stderr } = await runCli(launcherPath, `${origin}/css`);
        assert.equal(code, 0, `stderr:\n${stderr}`);
        assert.match(stdout, /Styled content/);
        assert.equal(stderr.trim(), "");
      });
    }
  });
});
