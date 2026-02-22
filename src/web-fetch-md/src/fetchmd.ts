#!/usr/bin/env node
import fs from "node:fs/promises";
import process from "node:process";
import { parseHTML } from "linkedom";
import { Readability } from "@mozilla/readability";
import TurndownService from "turndown";

const DEFAULT_ACCEPT =
  "text/markdown, text/x-markdown;q=0.99, text/plain;q=0.9, text/html;q=0.8, */*;q=0.1";
const DEFAULT_UA = "web-fetch-md/1.0";
const DEFAULT_TIMEOUT_MS = 30_000;

const HELP_TEXT = [
  "Usage:",
  "  fetchmd [--debug] [--no-abs-links] [--timeout-ms <ms>] <url> [output.md]",
  "",
  "Notes:",
  "  - Prints Markdown to stdout by default.",
  "  - Writes to output.md when provided.",
].join("\n");

function printHelp(to: "stdout" | "stderr"): void {
  const stream = to === "stdout" ? process.stdout : process.stderr;
  stream.write(`${HELP_TEXT}\n`);
}

function usageError(): never {
  printHelp("stderr");
  process.exit(2);
}

function isHttpUrl(s: string): boolean {
  try {
    const url = new URL(s);
    return url.protocol === "http:" || url.protocol === "https:";
  } catch {
    return false;
  }
}

function looksLikeHtml(s: string): boolean {
  // Keep this strict: Markdown can contain inline HTML (e.g. "<div>") and we still want
  // to treat it as Markdown if the overall payload is text-y.
  const t = (s || "").trimStart().slice(0, 2000).toLowerCase();
  if (t.startsWith("<!doctype html")) return true;
  if (t.startsWith("<html") || t.startsWith("<?xml")) return true;
  if (/<(head|body)\b/.test(t)) return true;
  if (t.startsWith("<") && /<\/(html|head|body)>/.test(t)) return true;
  return false;
}

function looksLikeMarkdown(s: string): boolean {
  const t = (s || "").slice(0, 4000);
  return (
    /^\s*#\s+\S+/m.test(t) ||
    /^\s*---\s*$/m.test(t) ||
    /```/.test(t) ||
    /^\s*[-*+]\s+\S+/m.test(t) ||
    /^\s*\d+\.\s+\S+/m.test(t) ||
    /\[[^\]]+\]\([^)]+\)/.test(t)
  );
}

function isMarkdownContentType(contentType: string | null | undefined): boolean {
  const ct = (contentType || "").toLowerCase();
  return (
    ct.includes("text/markdown") ||
    ct.includes("text/x-markdown") ||
    ct.includes("application/markdown") ||
    ct.includes("application/x-markdown")
  );
}

function isHtmlContentType(contentType: string | null | undefined): boolean {
  const ct = (contentType || "").toLowerCase();
  return ct.includes("text/html") || ct.includes("application/xhtml+xml");
}

function isTextContentType(contentType: string | null | undefined): boolean {
  const ct = (contentType || "").toLowerCase();
  return ct.startsWith("text/") || ct.includes("application/xml");
}

function debugLog(enabled: boolean, msg: string): void {
  if (!enabled) return;
  console.error(`[fetchmd] ${msg}`);
}

async function fetchWithTimeout(
  url: string,
  init: RequestInit,
  timeoutMs: number,
): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(timeout);
  }
}

async function head(url: string, headers: Record<string, string>, timeoutMs: number): Promise<Response> {
  return await fetchWithTimeout(url, { method: "HEAD", redirect: "follow", headers }, timeoutMs);
}

async function get(url: string, headers: Record<string, string>, timeoutMs: number): Promise<Response> {
  return await fetchWithTimeout(url, { method: "GET", redirect: "follow", headers }, timeoutMs);
}

async function readTextUpTo(res: Response, maxBytes: number): Promise<string> {
  const body = res.body;
  if (body && typeof (body as ReadableStream<Uint8Array>).getReader === "function") {
    const reader = (body as ReadableStream<Uint8Array>).getReader();
    const decoder = new TextDecoder("utf-8");
    let text = "";
    let bytes = 0;
    try {
      while (bytes < maxBytes) {
        const { value, done } = await reader.read();
        if (done) break;
        if (value) {
          bytes += value.byteLength;
          text += decoder.decode(value, { stream: true });
        }
        if (bytes >= maxBytes) break;
      }
    } finally {
      try {
        await reader.cancel();
      } catch {
        // ignore
      }
    }
    text += decoder.decode();
    return text.slice(0, Math.max(0, maxBytes));
  }

  const text = await res.text();
  return text.slice(0, Math.max(0, maxBytes));
}

async function sniff(
  url: string,
  headers: Record<string, string>,
  timeoutMs: number,
): Promise<{ res: Response; preview: string }> {
  const res = await get(url, { ...headers, Range: "bytes=0-8191" }, timeoutMs);
  const preview = await readTextUpTo(res, 8192);
  return { res, preview };
}

function computeMarkdownSiblingUrls(url: string): string[] {
  const u = new URL(url);
  u.hash = "";
  u.search = "";

  const candidates = new Set<string>();

  const pathName = u.pathname;
  if (pathName.endsWith("/")) {
    candidates.add(new URL("index.md", u).toString());
    candidates.add(new URL("README.md", u).toString());
  } else if (!pathName.toLowerCase().endsWith(".md")) {
    const md = new URL(u.toString());
    md.pathname = `${pathName}.md`;
    candidates.add(md.toString());
  }

  const markdown = new URL(u.toString());
  if (!pathName.toLowerCase().endsWith(".markdown")) {
    if (pathName.endsWith("/")) markdown.pathname = `${pathName}index.markdown`;
    else markdown.pathname = `${pathName}.markdown`;
    candidates.add(markdown.toString());
  }

  return [...candidates];
}

function toAbsoluteHttpUrl(urlLike: string | null, baseUrl: string): string {
  if (!urlLike) return urlLike ?? "";
  const raw = String(urlLike).trim();
  if (!raw) return raw;
  if (raw.startsWith("#")) return raw;
  if (raw.startsWith("mailto:") || raw.startsWith("tel:")) return raw;
  if (raw.startsWith("javascript:")) return "";
  try {
    const abs = new URL(raw, baseUrl);
    if (abs.protocol === "http:" || abs.protocol === "https:") return abs.toString();
    return raw;
  } catch {
    return raw;
  }
}

function absolutizeDomUrls(root: any, baseUrl: string): void {
  for (const a of root.querySelectorAll?.("a[href]") || []) {
    const href = a.getAttribute("href");
    const abs = toAbsoluteHttpUrl(href, baseUrl);
    if (abs) a.setAttribute("href", abs);
    else a.removeAttribute("href");
  }

  for (const img of root.querySelectorAll?.("img[src]") || []) {
    const src = img.getAttribute("src");
    const abs = toAbsoluteHttpUrl(src, baseUrl);
    if (abs) img.setAttribute("src", abs);
    else img.removeAttribute("src");
  }
}

async function createTurndown(): Promise<any> {
  const turndown = new TurndownService({
    codeBlockStyle: "fenced",
    headingStyle: "atx",
    hr: "---",
    bulletListMarker: "-",
    emDelimiter: "_",
  });

  try {
    const mod: any = await import("turndown-plugin-gfm");
    const plugin = mod?.default ?? mod;
    const extras: any[] = [];

    if (plugin?.gfm) extras.push(plugin.gfm);
    if (plugin?.tables) extras.push(plugin.tables);
    if (plugin?.strikethrough) extras.push(plugin.strikethrough);
    if (plugin?.taskListItems) extras.push(plugin.taskListItems);

    if (extras.length > 0) turndown.use(extras);
  } catch {
    // Optional dependency; base turndown still works.
  }

  turndown.addRule("preToFenced", {
    filter: ["pre"],
    replacement(_content: string, node: any) {
      const code = node?.textContent ?? "";
      const cleaned = String(code).replace(/\n+$/g, "");
      return `\n\n\`\`\`\n${cleaned}\n\`\`\`\n\n`;
    },
  });

  return turndown;
}

function normalizeMarkdown(md: string): string {
  return (
    String(md || "")
      .replace(/\r\n/g, "\n")
      .replace(/[ \t]+$/gm, "")
      .replace(/\n{3,}/g, "\n\n")
      .trim() + "\n"
  );
}

function stripUiNoiseMarkdown(md: string): string {
  const lines = String(md || "").replace(/\r\n/g, "\n").split("\n");
  const out: string[] = [];
  let inFence = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("```")) {
      inFence = !inFence;
      out.push(line);
      continue;
    }

    if (!inFence) {
      if (/^(copy|copy page|copied!?|copy to clipboard)$/i.test(trimmed)) continue;
      if (/^loading\.\.\.$/i.test(trimmed)) continue;
    }

    out.push(line);
  }

  return out.join("\n");
}

async function htmlToMarkdown(
  html: string,
  baseUrl: string,
  opts: { absolutizeLinks: boolean; debug: boolean },
): Promise<string> {
  const { document: doc } = parseHTML(html) as any;

  for (const selector of ["script", "style", "noscript"]) {
    doc.querySelectorAll(selector).forEach((n: any) => n.remove());
  }

  const reader = new Readability(doc as any);
  const article = reader.parse() as any;

  const turndown = await createTurndown();

  let title = (article?.title?.trim() || doc.title?.trim() || "") as string;
  let contentHtml = (article?.content || doc.body?.innerHTML || html) as string;
  title = title.replace(/\s+/g, " ").trim();

  if (article?.content) debugLog(opts.debug, "HTML → Readability → Markdown");
  else debugLog(opts.debug, "HTML → body → Markdown (Readability failed)");

  const { document: fragDoc } = parseHTML(`<html><body>${contentHtml}</body></html>`) as any;
  const fragBody = fragDoc.body;

  if (opts.absolutizeLinks) absolutizeDomUrls(fragBody, baseUrl);

  const contentMd = turndown.turndown(fragBody);
  const shouldAddTitle = title && !contentMd.trimStart().startsWith("# ");
  const md = shouldAddTitle ? `# ${title}\n\n${contentMd}` : contentMd;
  return normalizeMarkdown(stripUiNoiseMarkdown(md));
}

async function writeOutput(text: string, outPath: string | undefined): Promise<void> {
  if (outPath) {
    await fs.writeFile(outPath, text, "utf8");
    return;
  }
  process.stdout.write(text);
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  let debug = false;
  let absolutizeLinks = true;
  let timeoutMs = DEFAULT_TIMEOUT_MS;

  while (args[0]?.startsWith("-")) {
    const flag = args.shift();
    if (flag === "--help" || flag === "-h") {
      printHelp("stdout");
      process.exit(0);
    }
    if (flag === "--debug") {
      debug = true;
      continue;
    }
    if (flag === "--no-abs-links") {
      absolutizeLinks = false;
      continue;
    }
    if (flag === "--timeout-ms") {
      const raw = args.shift();
      const n = raw ? Number.parseInt(raw, 10) : Number.NaN;
      if (!Number.isFinite(n) || n <= 0) usageError();
      timeoutMs = n;
      continue;
    }
    usageError();
  }

  const url = args.shift();
  const out = args.shift();
  if (!url || args.length > 0) usageError();
  if (!isHttpUrl(url)) throw new Error(`URL must be http(s): ${url}`);

  const negotiatedHeaders: Record<string, string> = {
    Accept: DEFAULT_ACCEPT,
    "User-Agent": DEFAULT_UA,
  };

  // 1) Prefer markdown via content negotiation.
  try {
    const h = await head(url, negotiatedHeaders, timeoutMs);
    const ct = h.headers.get("content-type") || "";
    debugLog(debug, `HEAD ${h.status} content-type=${ct || "(none)"}`);
    if (h.ok && isMarkdownContentType(ct)) {
      debugLog(debug, "Negotiated Markdown (content-type)");
      const r = await get(url, negotiatedHeaders, timeoutMs);
      if (!r.ok) throw new Error(`Fetch failed: ${r.status} ${r.statusText}`);
      const body = normalizeMarkdown(await r.text());
      return await writeOutput(body, out);
    }
  } catch (err) {
    debugLog(debug, `Negotiation HEAD failed: ${String(err)}`);
  }

  // 1b) Sniff negotiated response body (handles mis-set content-type).
  try {
    const { res, preview } = await sniff(url, negotiatedHeaders, timeoutMs);
    const ct = res.headers.get("content-type") || "";
    debugLog(debug, `Sniff ${res.status} content-type=${ct || "(none)"}`);
    if (
      res.ok &&
      !looksLikeHtml(preview) &&
      (isMarkdownContentType(ct) ||
        (isTextContentType(ct) && looksLikeMarkdown(preview)) ||
        looksLikeMarkdown(preview))
    ) {
      debugLog(debug, "Negotiated Markdown (sniff)");
      const full = await get(url, negotiatedHeaders, timeoutMs);
      if (!full.ok) throw new Error(`Fetch failed: ${full.status} ${full.statusText}`);
      const body = normalizeMarkdown(await full.text());
      return await writeOutput(body, out);
    }
  } catch (err) {
    debugLog(debug, `Negotiation sniff failed: ${String(err)}`);
  }

  // 2) Try sibling *.md endpoints.
  for (const candidate of computeMarkdownSiblingUrls(url)) {
    try {
      const { res, preview } = await sniff(
        candidate,
        { "User-Agent": DEFAULT_UA, Accept: "text/markdown,text/plain;q=0.9,*/*;q=0.1" },
        timeoutMs,
      );
      const ct = res.headers.get("content-type") || "";
      debugLog(debug, `Sibling sniff ${candidate} -> ${res.status} ct=${ct || "(none)"}`);

      if (!res.ok) continue;
      if (looksLikeHtml(preview) || isHtmlContentType(ct)) continue;
      if (!looksLikeMarkdown(preview) && !isMarkdownContentType(ct)) continue;

      debugLog(debug, `Sibling Markdown: ${candidate}`);
      const full = await get(
        candidate,
        { "User-Agent": DEFAULT_UA, Accept: "text/markdown,text/plain;q=0.9,*/*;q=0.1" },
        timeoutMs,
      );
      if (!full.ok) continue;
      const body = normalizeMarkdown(await full.text());
      return await writeOutput(body, out);
    } catch {
      // keep trying
    }
  }

  // 3) Last resort: HTML → Readability → Markdown.
  const htmlRes = await get(url, { "User-Agent": DEFAULT_UA, Accept: "text/html,*/*;q=0.1" }, timeoutMs);
  if (!htmlRes.ok) throw new Error(`Fetch failed: ${htmlRes.status} ${htmlRes.statusText}`);
  const html = await htmlRes.text();
  const md = await htmlToMarkdown(html, htmlRes.url || url, { absolutizeLinks, debug });
  await writeOutput(md, out);
}

main().catch((err) => {
  console.error(String((err as any)?.stack || err));
  process.exit(1);
});
