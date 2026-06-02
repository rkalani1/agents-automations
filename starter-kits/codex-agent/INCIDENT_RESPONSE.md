# Incident Response Runbook — Codex CLI Coding Agent

## Overview

This runbook covers the five phases of incident response for the Codex CLI coding agent. Keep it accessible to all engineers who use the agent.

---

## 1. Detect

Signals that indicate a potential incident:

- Agent applied edits to files outside the permitted scope (check git diff).
- Agent ran a shell command not in the permitted list (check session transcript).
- Agent reproduced or logged content from a secret-matching file.
- Agent initiated a network call without human confirmation.
- CI/CD pipeline triggered or modified without human request.
- Unexpected API cost spike in the OpenAI billing dashboard.
- Session transcript contains instructions the agent should have refused.

Monitoring:
- [ ] Alert on git changes to files outside `src/`, `tests/`, `docs/`.
- [ ] Alert on changes to CI/CD or infrastructure files.
- [ ] Alert on API spend > 2x the 30-day daily average.
- [ ] Review `shell_commands_run` at end of every session.

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Revoke the OpenAI API key in the OpenAI dashboard (https://platform.openai.com/api-keys).
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all environments.
   c. Terminate any active Codex CLI sessions.
   d. Issue a replacement key and store in the secrets manager.
2. If unintended edits were applied: do not push. Run `git diff HEAD`, then `git checkout .` to discard uncommitted changes or `git revert` for committed changes.
3. If CI/CD was triggered: disable the pipeline and review any deployments.
4. If secrets were exposed in output: treat the secret as compromised and rotate it immediately.
5. Preserve session transcripts and logs from the incident window.

---

## 3. Investigate

Questions to answer:

- What exact input or file content triggered the behavior?
- Was it a prompt injection from a source file or a direct human instruction?
- Which `AGENTS.md` rule was violated or absent?
- Is the attack class documented in `RED_TEAM_CASES.jsonl`? If not, add it.
- Were all four HITL gates functioning at the time?
- Which eval or red-team case would have caught this?

---

## 4. Remediate

- Update `AGENTS.md` to close the gap.
- Update `PROMPT.md` if the system prompt was insufficiently restrictive.
- Add a new eval and red-team case for the incident's attack class.
- Re-run the full eval and red-team suite on a scratch repository.
- Re-issue API credentials after rotation.
- If CI/CD was affected, harden pipeline permissions.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to stakeholders.
- If secrets or PII were exposed: follow your organization's breach notification policy.
- After remediation: publish a post-mortem and file it alongside this document.

Field Guide:  /agents-automations/
Reference: https://developers.openai.com/codex/cli
