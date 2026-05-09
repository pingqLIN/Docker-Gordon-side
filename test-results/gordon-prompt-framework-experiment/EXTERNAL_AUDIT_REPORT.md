# External Audit Report

## Audit Mode

same-provider-subagent

## Scope

`manual-question: review Gordon prompt framework experiment plan`

Reviewed artifact:

`Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\EXPERIMENT_PLAN.md`

## Reference Inputs

- `local-project`: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\EXPERIMENT_PLAN.md` - experiment plan under review.
- `local-skill`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\SKILL.md` - audit orchestration procedure.
- `local-skill-support`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\references\mode-same-provider.md` - selected same-provider subagent mode.
- `local-skill-support`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\references\report-format.md` - normalized report format.
- `local-skill-support`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\references\source-attribution-policy.md` - source attribution requirements.
- `official-doc`: `https://docs.docker.com/ai-overview/` - confirmed Gordon uses `docker ai`; Docker Agent is separate.
- `official-doc`: `https://docs.docker.com/ai/gordon/` - confirmed Gordon's Docker workflow surface.
- `official-doc`: `https://docs.docker.com/ai/gordon/concepts/capabilities/` - confirmed Gordon capabilities relevant to shell/filesystem/docs/development/containerization.
- `official-doc`: `https://docs.docker.com/ai/gordon/how-to/permissions/` - informed approval/session/working-directory risk controls.

## Findings

### Critical

1. **Initial plan lacked paired baseline**
   - Scope: original `EXPERIMENT_PLAN.md`, Test Corpus / Execution Steps.
   - Risk: a 3-task baseline against 12 treatment prompts could not fairly quantify whether the architecture improved Gordon's acceptance rate.
   - Recommended action: run baseline and treatment for every frozen task intent.
   - Disposition: fixed in revised plan by adding paired baseline/treatment execution for all task intents.

2. **Failed-test-only rerun would inflate final success rate**
   - Scope: original execution step allowing only failed tests to be rerun.
   - Risk: revising after failures and rerunning only failures overfits the architecture.
   - Recommended action: treat failed-test reruns as exploratory or rerun the full corpus.
   - Disposition: fixed in revised plan.

### Warning

1. **Approval/session state could confound execution evidence**
   - Scope: Gordon permissions and CLI execution protocol.
   - Risk: YOLO or session-wide `A` approval may make treatment prompts appear more executable.
   - Recommended action: prohibit YOLO/session-wide approval and log approval events.
   - Disposition: fixed in revised plan.

2. **Session DB source must be proven**
   - Scope: evidence export.
   - Risk: Gordon and Docker Agent both use cagent-style storage, so session attribution must be verified.
   - Recommended action: add evidence-source preflight with timestamps and DB mutation check.
   - Disposition: fixed in revised plan.

3. **Command safety should use allowlist, not denylist**
   - Scope: Docker command execution.
   - Risk: destructive variants are too broad for a denylist.
   - Recommended action: add read-only and supervised command allowlists.
   - Disposition: fixed in revised plan.

4. **Working directory is context, not a security boundary**
   - Scope: file access and AGENTS/session behavior.
   - Risk: Gordon can inspect parent files unless restricted.
   - Recommended action: score out-of-scope access as boundary incident.
   - Disposition: fixed in revised plan.

5. **Composite PASS hides sub-failures**
   - Scope: scoring.
   - Risk: acceptance, Docker mapping, execution, task completion, and safety can fail independently.
   - Recommended action: record binary subfields plus composite score.
   - Disposition: fixed in revised plan.

### Suggestion

1. **Freeze corpus before execution**
   - Recommended action: save prompt files and hashes before running.
   - Disposition: adopted.

2. **Preserve raw evidence with redaction policy**
   - Recommended action: raw evidence folder, append-only audit log, summary redaction.
   - Disposition: adopted.

3. **Add negative controls**
   - Recommended action: include out-of-scope prompts to test over-forcing.
   - Disposition: adopted.

## Assumptions

- Reviewers assessed the plan, not live Gordon behavior.
- The fixture is disposable and contains no real secrets.
- This is a pilot experiment; confidence intervals are diagnostic.

## Disposition

fix-and-rerun, then proceed

## Next Action

Execute the revised paired experiment using the frozen prompt corpus, deterministic evidence export, command allowlist, and append-only audit log.

