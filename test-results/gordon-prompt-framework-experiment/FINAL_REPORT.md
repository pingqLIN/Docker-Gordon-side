# Gordon Prompt Framework Experiment Final Report

Date: 2026-05-07
Run ID: `gordon_prompt_arch_20260507_v1`

## Verdict

The target prompt architecture met the operational 80% success criterion on the positive task corpus:

```text
treatment positive pass rate = 12 / 12 = 100%
target threshold = >= 80%
```

However, the paired baseline also passed:

```text
baseline positive pass rate = 12 / 12 = 100%
observed lift = 0 percentage points
```

Conclusion:

- The architecture can be used as a robust Gordon prompt wrapper for Docker-adjacent development tasks.
- This experiment does not prove the architecture improves Gordon over baseline on this fixture, because baseline already succeeded on all positive tasks.
- The architecture did correctly preserve boundary behavior on negative controls: Gordon refused artificial Docker mapping for non-Docker requests.

## Artifacts

- Plan: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\EXPERIMENT_PLAN.md`
- External audit report: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\EXTERNAL_AUDIT_REPORT.md`
- Result summary: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\RESULTS_SUMMARY_FOR_VERIFICATION.md`
- Frozen prompt manifest: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\frozen_prompt_manifest.json`
- Raw results: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\raw_results.json`
- Audit log: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\AUDIT_LOG.jsonl`
- Evidence directory: `Q:\Projects\Docker-Gordon-side\test-results\gordon-prompt-framework-experiment\evidence`
- Fixture: `Q:\Projects\gordon-prompt-framework-fixture`

## Method

Official Gordon entrypoint:

```powershell
docker ai -C Q:\Projects\gordon-prompt-framework-fixture "<prompt>"
```

Experiment design after audit correction:

- 12 positive Docker-adjacent task intents.
- 2 negative controls.
- Each task ran in two conditions:
  - `baseline`: task intent without the architecture.
  - `treatment`: same task intent embedded in the Docker workflow prompt architecture.
- Each run used a fresh `docker ai` invocation.
- The runner sent individual `y` approvals only; it did not send `A` and did not enable YOLO.
- Session evidence came from `C:\Users\miles\.cagent\session.db`.

## Positive Task Results

| Test | Type | Baseline | Treatment |
|---|---|---:|---:|
| T01 | frontend/dev-server | PASS | PASS |
| T02 | backend/runtime | PASS | PASS |
| T03 | database/backend | PASS | PASS |
| T04 | test/CI | PASS | PASS |
| T05 | image-optimization | PASS | PASS |
| T06 | logs/debugging | PASS | PASS |
| T07 | security/config | PASS | PASS |
| T08 | documentation | PASS | PASS |
| T09 | architecture | PASS | PASS |
| T10 | build-cache | PASS | PASS |
| T11 | local-dev-parity | PASS | PASS |
| T12 | deployment-readiness | PASS | PASS |

Treatment success rate:

```text
12 / 12 = 100%
```

Baseline success rate:

```text
12 / 12 = 100%
```

Diagnostic note:

With only 12 positive tasks, the point estimate is 100%, but the confidence interval remains wide. Treat this as a pilot result, not a statistical guarantee that future tasks will exceed 80%.

## Negative Controls

| Test | Condition | Outcome |
|---|---|---|
| N01 | treatment | PASS as boundary check: Gordon refused to force a capital-city question into Docker. |
| N02 | treatment | PASS as boundary check: Gordon refused to force a birthday greeting into Docker before later approval-artifact messages. |

## Prompt Architecture That Passed

Use this wrapper when a task has a plausible Docker workflow mapping:

```text
You are Docker Gordon. Treat the following request as a Docker workflow task, not as a general chat request.

Task:
[TASK]

Docker workflow mapping requirement:
Before refusing, map the request into one or more Docker surfaces:
- containerization
- Dockerfile
- compose.yaml
- .dockerignore
- local dev container
- build/test/lint inside a container
- runtime logs
- image layers and cache
- ports, volumes, networks
- env var handling without reading secrets
- CI build parity
- deployment readiness

Execution requirement:
You must substantively execute the Docker workflow path. A valid execution can include read-only file inspection, Docker resource inspection, Docker documentation lookup, or a safe Docker command. Merely saying this is not Docker-related, giving generic advice, or solving it without the Docker workflow mapping is a failure.

Safety boundaries:
- Use the current working directory as the default scope.
- Do not read secret files such as .env, pem files, credentials, or private keys.
- Do not write files unless explicitly requested.
- Do not run destructive Docker commands.
- If a command requires approval, propose only the minimum safe command.

Required answer format:
1. Accepted? yes/no
2. Docker workflow surface used
3. Concrete execution performed
4. Files/resources inspected
5. Result
6. Any refusal or boundary note
```

## Important Caveats

- Baseline also achieved 100%, so this experiment does not show a measured improvement over ordinary Gordon prompting for Docker-adjacent tasks.
- The fixture was already Docker-rich. A harder future corpus should include more ambiguous real-world tasks and more non-Docker distractors.
- The runner sent blind individual `y` approvals three times per run. Some sessions include trailing `y` user messages after Gordon had already completed. Evidence and scoring used the earlier task-relevant tool calls and assistant outputs, but this artifact should be removed in a future runner.
- Raw evidence may contain full tool responses and should be treated as potentially sensitive local audit data.
- `docker ai` internally launches `docker agent run ... docker/gordon:v7`; this was still the official `docker ai` entrypoint, not a direct `docker agent` substitution.

## External Audit Disposition

Three review roles were attempted under `external-audit-orchestrator` same-provider mode. Substantive audit findings were obtained for:

- methodology/statistical design
- Gordon boundary fairness
- safety/evidence handling

The plan was revised before execution to address the warning-or-higher findings:

- paired baseline/treatment corpus
- prompt manifest and hashes
- deterministic session evidence export
- command allowlist
- no YOLO and no session-wide approval
- secret preflight
- negative controls
- raw evidence retention caveat

The final result-verifier subagent did not return a substantive verification report despite follow-up; therefore the final consistency check was performed directly against `raw_results.json`, `AUDIT_LOG.jsonl`, and session evidence exports.

## Final Recommendation

Use the prompt architecture as a practical Gordon wrapper when the user task has a real Docker workflow surface. Do not claim it universally improves Gordon acceptance rate yet. The next experiment should use a harder held-out corpus of tasks that Gordon historically rejected, because this fixture's baseline was already too favorable.

