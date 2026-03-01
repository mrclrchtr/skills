import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import test from "node:test";
import { createServer } from "node:http";
import { fileURLToPath } from "node:url";

function runFetchmd(url) {
  return new Promise((resolve) => {
    const cwd = fileURLToPath(new URL("..", import.meta.url));
    const child = spawn(
      process.execPath,
      ["--import", "tsx", "./src/fetchmd.ts", url],
      { cwd, stdio: ["ignore", "pipe", "pipe"] },
    );

    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (d) => (stdout += d));
    child.stderr.on("data", (d) => (stderr += d));
    child.on("close", (code) => resolve({ code, stdout, stderr }));
    child.on("error", (err) => resolve({ code: 1, stdout, stderr: String(err) }));
  });
}

test("fences non-Markdown text/plain (toml) instead of running Readability", async () => {
  const server = createServer((req, res) => {
    if (req.url === "/mise.toml") {
      res.statusCode = 200;
      res.setHeader("Content-Type", "text/plain; charset=utf-8");
      res.end('foo = "bar"\n');
      return;
    }
    res.statusCode = 404;
    res.end("not found");
  });

  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const { port } = server.address();
  const url = `http://127.0.0.1:${port}/mise.toml`;

  try {
    const { code, stdout, stderr } = await runFetchmd(url);
    assert.equal(code, 0, stderr);
    assert.match(stdout, /^```toml\n/m);
    assert.match(stdout, /foo = "bar"/);
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
});
