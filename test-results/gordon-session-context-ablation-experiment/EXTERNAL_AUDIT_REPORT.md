# External Audit Report

## Audit Mode

same-provider-subagent

## Scope

- `test-results/gordon-session-context-ablation-experiment/EXPERIMENT_PLAN.zh-TW.md`
- `test-results/gordon-session-context-ablation-experiment/run_session_context_ablation_experiment.py`
- `test-results/gordon-session-context-ablation-experiment/REPORT.zh-TW.md`
- `test-results/gordon-session-context-ablation-experiment/RESULTS.md`
- README / synthesis index updates that reference this experiment

## Reference Inputs

- `local-project`: `Q:\Projects\Docker-Gordon-side` - current Gordon experiment repository and existing runner/report patterns.
- `local-skill`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\SKILL.md` - audit procedure requested by the user.
- `local-skill`: `C:\Users\miles\.codex\skills\project-development-loop\SKILL.md` - execution loop requested by the user.

## Latest Implementation Snapshot

- Current rescored run: `gordon_session_context_ablation_20260510_smoke`
- Current totals: `OBSERVE=6`, `BLOCKED=3`, total `9`
- Archived baseline rescore: `raw_results.final-baseline.rescored.json`
- Archived baseline session evidence: `evidence-final-baseline/`
- Archived baseline totals: `PASS=2`, `OBSERVE=4`, `BLOCKED=5`, total `11`
- Formal 10x same-session batch: not executed because the 3x smoke expansion produced blocked rows.
- Desktop UI context injection: manual / semi-manual evidence package only, stored in `test-results/gordon-desktop-ui-context-injection-experiment/`.

## Findings

### Warning: two-agent external review did not complete

- Severity: Warning
- Location or scope: audit orchestration
- Risk: The requested two-agent external/subagent review gate was attempted but did not produce usable reviewer findings. The first reviewer pair returned only instruction acknowledgements. The second reviewer pair remained running without findings until closed after timeout. Earlier `codex review --uncommitted` also failed with API authentication / network errors before completion.
- Recommended action: Treat this experiment as locally verified but not externally reviewed. Re-run two independent reviewers when the subagent or external review path is healthy.

### Warning: context-ablation flags are unavailable in the current CLI entrypoint

- Severity: Warning
- Location or scope: `context_ablation`
- Risk: The planned `--send-files` / `--write-files` style ablation could not be executed because the current `docker ai` entrypoint rejected those flags. These cases are correctly marked `BLOCKED`, but they do not provide model-behavior evidence.
- Recommended action: Keep the blocked classification and revisit when Docker exposes stable CLI controls for context/tool availability.

### Suggestion: increase repetitions before treating same-session observations as stable

- Severity: Suggestion
- Location or scope: `same_session`
- Risk: Same-session smoke expansion ran three iterations per sequence, but `3/9` rows were blocked because interactive prompt/session evidence was incomplete. The result is directional only and the formal 10x batch was correctly not executed.
- Recommended action: Fix or widen the interactive TUI prompt/session evidence gate, then rerun the 3x smoke expansion before attempting 10 iterations per condition.

## Assumptions

- Local Docker Desktop / Gordon state was acceptable for CLI experiments after unsandboxed Docker pipe access was allowed.
- The evidence root `test-results/gordon-session-context-ablation-experiment/` is intended to be committed as part of the research archive.
- No real secrets were present in the fixture preflight.

## Disposition

blocked

## Next Action

The local implementation and evidence are internally consistent for the current blocked/smoke status, but the external review requirement remains blocked. The next operational step is to rerun two read-only external/subagent reviewers when that tool path is healthy, then update this report with their actual findings before calling the phase complete.
