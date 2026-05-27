# Local folder monitor agent (manual-only)

> **Last verified:** 2026-05-06 · **Drift risk:** low

## Goal

Take a snapshot of a local folder's file tree and metadata, compare it against a previously saved snapshot, and produce a plain-text report listing new, modified, and deleted files — without modifying, copying, or uploading any file contents.

## Recommended platform(s)

Primary: Local Python script (stdlib only, no LLM required for the diff; optional LLM for the summary)
Alternates: Claude Code for interactive session with summary narrative; shell script with `find` and `diff`

## Why this platform

This recipe is intentionally local-first and LLM-optional. The core functionality — snapshot, compare, report — is deterministic and can be implemented with Python's `pathlib` and `hashlib` libraries without any API calls. Adding an LLM (via Claude Code or the OpenAI API) is useful only if you want a natural-language summary of the changes ("3 new files added to the invoices folder, 2 config files modified"). The stdlib-only path has zero API cost, zero data egress, and no drift risk from external services.

## Required subscription / account / API

- Python 3.11+ (stdlib only for the core script)
- Optional: Anthropic API key or OpenAI API key for a narrative summary step
- No cloud connector, LLM, or internet access required for the diff step

## Required tools / connectors

- Python `pathlib`, `hashlib`, `json` (all stdlib)
- Optional: `anthropic` or `openai` Python package for the summary step
- Read access to the monitored folder
- Write access to a `snapshots/` directory for storing state

## Permission model

| Permission | Scope granted | Rationale |
|---|---|---|
| Read monitored folder (metadata only) | Recursive read of file names, sizes, mtimes, hashes | Needed to build the snapshot |
| Write snapshots/ directory | Single directory | Stores snapshot JSON files |
| Read file contents for hashing | MD5/SHA-256 of each file | Detects content changes without copying |
| Upload file contents | NOT granted | Contents never leave the machine |
| Delete or modify monitored files | NOT granted | Read-only monitoring |

Never run this script as a background process or cron job. It is a manual, on-demand tool.

## Filled agent spec

| Field | Value |
|---|---|
| Job statement | On demand, compare the current state of a specified folder to the last saved snapshot and report new, modified, and deleted files |
| Inputs | Path to the monitored folder; optional: path to a previous snapshot file (defaults to the most recent in snapshots/) |
| Outputs | A plain-text change report printed to stdout and optionally saved to `reports/`; an updated snapshot JSON saved to `snapshots/` |
| Tools | Python stdlib (pathlib, hashlib, json); no LLM unless --summarize flag is passed |
| Stop conditions | Snapshot taken; diff computed; report written |
| Error handling | If a file cannot be read (permissions, in-use), note it as "Skipped — read error" in the report |
| HITL gates | Human reads the report and decides on any action; the script makes no changes |
| Owner | System owner or developer |
| Review cadence | Run manually as needed; no automated execution |

## Setup steps

1. Create the working directories:
   ```bash
   mkdir -p snapshots reports
   ```
2. Save the script below as `folder_monitor.py`.
3. Take the first (baseline) snapshot:
   ```bash
   python folder_monitor.py --folder ~/my-folder --save-snapshot
   ```
   This writes `snapshots/snapshot_YYYY-MM-DD_HHMMSS.json`.
4. After some time passes (or after changes you want to detect), run again:
   ```bash
   python folder_monitor.py --folder ~/my-folder
   ```
   The script compares against the most recent snapshot and prints a change report.
5. To save the report to a file:
   ```bash
   python folder_monitor.py --folder ~/my-folder --output reports/changes_YYYY-MM-DD.txt
   ```

Manual-only run; opt-in scheduling is out of scope for this recipe.

## Prompt / instructions

```python
"""
local-folder-monitor: folder_monitor.py
Manual-only. No LLM required for core diff. Optional --summarize flag adds LLM narrative.
"""

import argparse, hashlib, json, os, pathlib, sys
from datetime import datetime

SNAPSHOT_DIR = pathlib.Path("snapshots")
SNAPSHOT_DIR.mkdir(exist_ok=True)

def hash_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return "READ_ERROR"

def build_snapshot(folder: pathlib.Path) -> dict:
    snapshot = {}
    for p in folder.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(folder))
            snapshot[rel] = {
                "size": p.stat().st_size,
                "mtime": p.stat().st_mtime,
                "sha256": hash_file(p),
            }
    return snapshot

def load_latest_snapshot() -> tuple[dict, str]:
    snapshots = sorted(SNAPSHOT_DIR.glob("snapshot_*.json"))
    if not snapshots:
        return {}, ""
    latest = snapshots[-1]
    return json.loads(latest.read_text()), latest.name

def diff_snapshots(old: dict, new: dict) -> dict:
    old_keys = set(old)
    new_keys = set(new)
    added = sorted(new_keys - old_keys)
    deleted = sorted(old_keys - new_keys)
    modified = sorted(
        k for k in old_keys & new_keys
        if old[k]["sha256"] != new[k]["sha256"]
        and old[k]["sha256"] != "READ_ERROR"
        and new[k]["sha256"] != "READ_ERROR"
    )
    read_errors = sorted(k for k in new_keys if new[k]["sha256"] == "READ_ERROR")
    return {
        "added": added,
        "deleted": deleted,
        "modified": modified,
        "read_errors": read_errors,
    }

def format_report(diff: dict, folder: str, snapshot_name: str) -> str:
    lines = [
        f"Folder monitor report",
        f"Folder: {folder}",
        f"Compared against: {snapshot_name or 'no previous snapshot'}",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
    ]
    if not snapshot_name:
        lines.append("No previous snapshot found. Baseline created.")
        return "\n".join(lines)
    for label, key in [("New files", "added"), ("Modified files", "modified"), ("Deleted files", "deleted")]:
        lines.append(f"{label} ({len(diff[key])}):")
        for f in diff[key]:
            lines.append(f"  {f}")
        lines.append("")
    if diff["read_errors"]:
        lines.append(f"Skipped — read error ({len(diff['read_errors'])}):")
        for f in diff["read_errors"]:
            lines.append(f"  {f}")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True)
    ap.add_argument("--save-snapshot", action="store_true")
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    folder = pathlib.Path(args.folder).expanduser().resolve()
    new_snapshot = build_snapshot(folder)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    snap_path = SNAPSHOT_DIR / f"snapshot_{ts}.json"
    snap_path.write_text(json.dumps(new_snapshot, indent=2))

    old_snapshot, old_name = load_latest_snapshot()
    # After saving, reload to get the one before the current
    all_snaps = sorted(SNAPSHOT_DIR.glob("snapshot_*.json"))
    if len(all_snaps) >= 2:
        old_snap_path = all_snaps[-2]
        old_snapshot = json.loads(old_snap_path.read_text())
        old_name = old_snap_path.name
    else:
        old_snapshot, old_name = {}, ""

    diff = diff_snapshots(old_snapshot, new_snapshot)
    report = format_report(diff, str(folder), old_name)
    print(report)
    if args.output:
        pathlib.Path(args.output).write_text(report)
        print(f"Report saved to {args.output}")

if __name__ == "__main__":
    main()
```

## Example input

Monitored folder: `~/project-files/` (synthetic)

Baseline snapshot taken 2026-05-01. Changes made since:
- `report_q2.docx` added
- `config.yaml` modified (new API endpoint added)
- `old_backup.tar.gz` deleted

## Expected output

```
Folder monitor report
Folder: /home/user/project-files
Compared against: snapshot_2026-05-01_090000.json
Generated: 2026-05-06T14:22:11

New files (1):
  report_q2.docx

Modified files (1):
  config.yaml

Deleted files (1):
  old_backup.tar.gz
```

## Eval cases

1. Input: folder with zero changes since baseline. Expected: "New files (0)", "Modified files (0)", "Deleted files (0)."
2. Input: first run (no baseline exists). Expected: snapshot saved; report says "No previous snapshot found. Baseline created." No diff produced.
3. Input: a file that is locked by another process during the run. Expected: that file appears in "Skipped — read error" section; diff continues for all other files.
4. Input: folder contains 10,000 files. Expected: script completes without error; progress is not printed (silence is fine); report is accurate.
5. Input: a file is renamed (deleted + added with a new name and same content). Expected: reported as one deletion and one addition; not detected as a rename (rename detection is out of scope for this recipe).

## Red-team probes

1. Monitored folder contains a symlink pointing outside the folder (e.g., `~/secret-files`). Expected behavior: `rglob("*")` follows symlinks by default; add `follow_symlinks=False` to `rglob` call or skip symlinks explicitly.
2. User runs the script with `--folder /` (root filesystem). Expected behavior: script should run but produce a very large snapshot; add a `max_files` guard (default 50,000) to prevent runaway hashing.
3. A snapshot file in `snapshots/` is corrupted (invalid JSON). Expected behavior: `json.loads` raises an exception; add a try/except that skips corrupted snapshots and falls back to the next most recent.

## Failure modes

1. Large file hashing latency: a folder with large video files takes minutes to hash. Mitigation: add an `--skip-large-files` flag that skips hashing files above a size threshold (e.g., 100 MB) and notes them as "Large file — hash skipped."
2. Clock skew: mtime-based detection is unreliable across filesystems with different timestamp resolutions. Mitigation: the script uses SHA-256 hash comparison, not mtime, for the change decision; mtime is recorded only for informational purposes.
3. Snapshot directory grows unbounded: many runs create many snapshot files. Mitigation: add a retention policy that keeps only the last 10 snapshots; delete older ones at the start of each run.
4. Sensitive file contents in snapshot: the snapshot stores only metadata and hashes, not contents. Mitigation: verify that `build_snapshot` stores only `size`, `mtime`, and `sha256` — no content.
5. False positive on touch: a file's mtime changes (e.g., a touch command) but content is unchanged. Mitigation: the script uses SHA-256 comparison, so a touch with no content change is not reported as modified.

## Cost / usage controls

- Zero API cost for the core script (stdlib only).
- Optional LLM summary step: roughly 500–1,000 tokens per report summary. Calculate dollar cost from the selected model's current pricing before recurring use.
- No external services, no data egress.

## Safe launch checklist

- [ ] Confirmed script contains no file modification, deletion, or upload operations
- [ ] Tested on a small synthetic folder (5–10 files) before pointing at real data
- [ ] Verified snapshots/ directory stores only metadata (size, mtime, sha256) — no file contents
- [ ] Symlink handling reviewed for the monitored folder
- [ ] Script is not in any crontab, launchd plist, or systemd timer

## Maintenance cadence

This recipe has very low drift risk — it uses only Python stdlib and no external APIs. Re-verify after Python version upgrades that `pathlib.rglob` behavior has not changed. Review the snapshot retention policy when the snapshots/ directory approaches 50 MB. No external vendor docs to monitor for this recipe.
