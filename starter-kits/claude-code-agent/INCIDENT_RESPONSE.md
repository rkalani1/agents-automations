# Incident Response Runbook — Claude Code Coding Agent

## Overview

This runbook covers the five phases of incident response for the Claude Code coding agent. Review it before the first production session and keep it accessible to all engineers who use the agent.

---

## 1. Detect

Signals that indicate a potential incident:

- Agent applied edits to files outside the permitted scope (visible in git diff or file modification timestamps).
- Agent ran a shell command that is not in the permitted list (visible in `shell_commands_run` log).
- Agent read or reproduced content from a secret-matching file.
- Agent initiated a network call without human confirmation.
- A CI/CD pipeline was triggered or modified without the human requesting it.
- Session transcript contains instructions the agent should have refused but did not.
- Unexpected API cost spike in the Anthropic billing dashboard.

Monitoring checklist:
- [ ] Alert on git changes to files outside `src/`, `tests/`, `docs/`.
- [ ] Alert on changes to `.github/workflows/` or infrastructure files.
- [ ] Alert on API spend > 2x the 30-day daily average.
- [ ] Review `shell_commands_run` at the end of every session.

---

## 2. Contain

Immediate steps when an incident is confirmed:

1. Kill switch:
   a. Revoke the Anthropic API key immediately in the Anthropic console.
   b. Set `OPERATOR_APPROVED_TO_RUN=0` in all environments where the agent is running.
   c. Terminate any active Claude Code sessions.
   d. Issue a new API key and store it in the secrets manager.
2. If unintended code changes were applied: do not push them. Run `git diff HEAD` to review, then `git checkout .` to discard uncommitted changes, or `git revert` for committed changes.
3. If a CI/CD pipeline was triggered: disable the pipeline at the CI provider and review any deployments it may have initiated.
4. If secrets were exposed in output: treat the secret as compromised. Rotate it immediately regardless of where it was sent.
5. Preserve session transcripts and logs from the incident window.

---

## 3. Investigate

Questions to answer:

- What exact session input or file content triggered the behavior?
- Was it a prompt injection from a source file or a direct instruction from a human?
- Which `CLAUDE.md` rule was violated or absent?
- Was the attack class one of the documented red-team scenarios? If not, add it to `RED_TEAM_CASES.jsonl`.
- Were all HITL gates functioning? Did the agent skip a gate?
- Which eval or red-team case would have caught this if run before the incident?

---

## 4. Remediate

- Update `CLAUDE.md` to close the gap that allowed the incident.
- Update `PROMPT.md` if the system prompt was insufficiently restrictive.
- Add a new eval or red-team case covering the incident's attack class.
- Re-run the full eval and red-team suite against a scratch repository.
- Re-issue API credentials after rotation.
- If CI/CD was affected, review and harden pipeline permissions.

---

## 5. Communicate

- Within 1 hour: Notify the owner in `AGENT_SPEC.md` and the security team.
- Within 4 hours: Send an internal incident summary to all stakeholders.
- If secrets or PII were exposed: follow your organization's breach notification policy.
- If CI/CD or production systems were affected: notify the engineering leadership and document the blast radius.
- After remediation: publish a post-mortem. File a copy alongside this document.

Field Guide:  /agents-automations/
Reference: https://code.claude.com/docs/en/setup
