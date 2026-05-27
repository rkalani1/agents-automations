#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const failures = [];

function fail(message) {
  failures.push(message);
}

function walk(dir, predicate, found = []) {
  if (!fs.existsSync(dir)) return found;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, predicate, found);
    else if (predicate(full)) found.push(full);
  }
  return found;
}

function run(command, args, options = {}) {
  const result = spawnSync(command, args, {
    cwd: options.cwd || repoRoot,
    env: process.env,
    encoding: "utf8",
    stdio: "pipe",
  });
  if (result.status !== 0) {
    const output = `${result.stdout || ""}${result.stderr || ""}`.trim();
    fail(`${options.label || [command, ...args].join(" ")} failed${output ? `:\n${output}` : ""}`);
  }
}

function validateJsonl(file) {
  const rel = path.relative(repoRoot, file);
  const lines = fs.readFileSync(file, "utf8").split(/\r?\n/);
  let records = 0;

  lines.forEach((line, index) => {
    if (!line.trim()) return;
    records += 1;
    try {
      const parsed = JSON.parse(line);
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
        fail(`${rel}:${index + 1}: JSONL record must be an object`);
      }
    } catch (error) {
      fail(`${rel}:${index + 1}: invalid JSON (${error.message})`);
    }
  });

  if (records === 0) fail(`${rel}: contains no JSONL records`);
  return records;
}

function pythonCommand() {
  for (const candidate of ["python3", "python"]) {
    const result = spawnSync(candidate, ["--version"], { encoding: "utf8", stdio: "pipe" });
    if (result.status === 0) return candidate;
  }
  return null;
}

let jsonlRecords = 0;
for (const file of walk(repoRoot, (candidate) => candidate.endsWith(".jsonl"))) {
  jsonlRecords += validateJsonl(file);
}

const pythonFiles = walk(path.join(repoRoot, "starter-kits"), (candidate) => candidate.endsWith(".py"));
const py = pythonCommand();
if (!py) {
  fail("python3/python not found; cannot compile Python starter kits");
} else if (pythonFiles.length > 0) {
  run(py, ["-m", "py_compile", ...pythonFiles], { label: "Python starter-kit compilation" });
}

for (const relativeDir of [
  "starter-kits/mcp-server-typescript",
  "starter-kits/openai-agents-sdk-typescript",
]) {
  const cwd = path.join(repoRoot, relativeDir);
  run("npm", ["install", "--silent", "--no-audit", "--no-fund", "--package-lock=false", "--ignore-scripts"], {
    cwd,
    label: `${relativeDir}: npm install`,
  });
  run("npm", ["run", "typecheck", "--silent"], {
    cwd,
    label: `${relativeDir}: npm run typecheck`,
  });
}

if (failures.length > 0) {
  console.error(`Starter-kit validation failed with ${failures.length} issue(s):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Starter-kit validation passed (${jsonlRecords} JSONL records, ${pythonFiles.length} Python files, 2 TypeScript kits).`);
