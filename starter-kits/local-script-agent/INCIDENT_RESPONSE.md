# Incident Response Runbook — Local Script Agent

## Overview

This runbook covers the five phases of incident response for the local Python script agent.

---

## 1. Detect

Signals that indicate a potential incident:

- `PermissionError` in logs from `safe_read()` (path traversal attempt).
- Summary output contains content from outside `./sandbox/` (sandbox bypass).
- Summary output reproduces apparent API keys, tokens, or other secrets.
- Summary output contains PII or PHI that should have been omitted.
- Unexpected cost spike in the OpenAI usage dashboard.
- Cron job running when `OPERATOR_APPROVED_TO_RUN` was not explicitly set.
- Log file shows the script executing at an unexpected time or frequency.

Monitoring:
- [ ] Alert on `PermissionError` in the script's log file.
- [ ] Alert on OpenAI spend > 2x the 30-day average per day.
- [ ] Review log file after every run when first deployed.
- [ ] Alert if the script runs outside its scheduled window (if cron is enabled).

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Revoke the `OPENAI_API_KEY` in the OpenAI dashboard (https://platform.openai.com/api-keys).
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all environments.
   c. If a cron job is running: comment out or remove the crontab entry immediately. The entry in `script.py` is labeled "manual-only example" — do not re-enable without completing the full launch checklist.
   d. Kill any running script processes.
   e. Issue a new API key and store in the secrets manager.
2. Quarantine `./sandbox/output/summary.md` if it contains sensitive content.
3. If PII or PHI was exposed in output: restrict access and notify the data-protection officer.
4. Preserve log files from the incident window.

---

## 3. Investigate

Questions to answer:

- What notes file content triggered the incident?
- Was it a prompt injection from a note, or a code/logic bug in `script.py`?
- Did `safe_read()` fire? If not, was the sandbox check bypassed?
- Was `OPERATOR_APPROVED_TO_RUN=1` set by a human following the checklist?
- Was the cron job enabled without authorization?
- Is the attack class in `RED_TEAM_CASES.jsonl`? If not, add it.
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Patch `script.py` (sandbox enforcement, PII detection, or error handling).
- Update `PROMPT.md` if the system prompt had a gap.
- Add a new eval and red-team case for the attack class.
- Re-run the full eval suite and confirm all cases pass.
- Run `pip audit` to check for new vulnerabilities.
- Re-issue `OPENAI_API_KEY` after rotation.
- If cron was the issue: document the authorization change required before re-enabling.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If PII or PHI was exposed: follow your organization's breach notification policy.
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agent-builder-field-guide/
