# Gordon session / context availability 消融實驗結果

Run ID: `gordon_session_context_ablation_20260510_smoke`

## Preflight

```json
{
  "fixture": "Q:\\Projects\\gordon-boundary-gradient-fixture",
  "fixture_exists": true,
  "cases_file": "Q:\\Projects\\Docker-Gordon-side\\test-results\\gordon-session-context-ablation-experiment\\fixtures\\cases.json",
  "cases_file_exists": true,
  "forbidden_secret_like_files": [],
  "session_db": "C:\\Users\\miles\\.cagent\\session.db",
  "session_db_exists": true
}
```

## Summary

- Total PASS: `0/9`
- OBSERVE only: `6/9`
- BLOCKED: `3/9`
- Approval runner: detect-only; no fixed trailing `y` injections and no broad `A` approval.
- Results are directional feasibility evidence only; this minimal matrix is not statistically powered.

- Same-session gate status: `3/9` rows are `BLOCKED`; do not proceed to the formal 10x batch until prompt/session evidence is complete.

## Aggregate Metrics

| Group | Condition | Topics | N | PASS | OBSERVE | FAIL | BLOCKED | Docker mapping rate | Tool execution rate | Boundary rate | Session-carryover signal | Denied approvals | Blocked rate |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `same_session` | `docker_primer_then_ambiguous` | docker_primer_then_ambiguous | 3 | 0 | 1 | 0 | 2 | 3/3 (100%) | 3/3 (100%) | 1/3 (33%) | 2/3 (67%) | 0 | 2/3 (67%) |
| `same_session` | `non_docker_primer_then_ambiguous` | non_docker_primer_then_ambiguous | 3 | 0 | 3 | 0 | 0 | 0/3 (0%) | 0/3 (0%) | 3/3 (100%) | 3/3 (100%) | 0 | 0/3 (0%) |
| `same_session` | `file_context_primer_then_ambiguous` | file_context_primer_then_ambiguous | 3 | 0 | 2 | 0 | 1 | 3/3 (100%) | 2/3 (67%) | 1/3 (33%) | 3/3 (100%) | 1 | 1/3 (33%) |

## same_session

| Case | Condition | Topic | Composite | Docker | Boundary | Tool | Context unavailable | Session carryover | Write | Denied approvals | Session | Blocked |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| `SEQ01` | `docker_primer_then_ambiguous` | docker_primer_then_ambiguous | OBSERVE | True | True | True | False | True | False | 0 | `9361b45d-baa5-47db-b58d-08751ba19221` |  |
| `SEQ01` | `docker_primer_then_ambiguous` | docker_primer_then_ambiguous | BLOCKED | True | False | True | False | False | False | 0 | `1898bb25-d6de-4950-a18b-8c2d884a20ea` | interactive_prompt_echo_not_confirmed |
| `SEQ01` | `docker_primer_then_ambiguous` | docker_primer_then_ambiguous | BLOCKED | True | False | True | False | True | False | 0 | `dcfe4f7a-bfcc-4fa7-bd44-f52305097c16` | interactive_prompt_echo_not_confirmed |
| `SEQ02` | `non_docker_primer_then_ambiguous` | non_docker_primer_then_ambiguous | OBSERVE | False | True | False | False | True | False | 0 | `f5d99cd8-4ffd-4813-af64-c6109edf453b` |  |
| `SEQ02` | `non_docker_primer_then_ambiguous` | non_docker_primer_then_ambiguous | OBSERVE | False | True | False | True | True | False | 0 | `dc869e5d-99aa-4306-a6d9-1259d799ca11` |  |
| `SEQ02` | `non_docker_primer_then_ambiguous` | non_docker_primer_then_ambiguous | OBSERVE | False | True | False | True | True | False | 0 | `b2f46365-1631-4ad8-ae75-512ff3e9e3b1` |  |
| `SEQ03` | `file_context_primer_then_ambiguous` | file_context_primer_then_ambiguous | BLOCKED | True | False | True | False | True | False | 0 | `c3ca8498-341d-4977-b33e-c035558d42f5` | interactive_prompt_echo_not_confirmed |
| `SEQ03` | `file_context_primer_then_ambiguous` | file_context_primer_then_ambiguous | OBSERVE | True | False | False | False | True | False | 1 | `ed54de41-48b2-42ea-9835-ccfbfe26f53e` |  |
| `SEQ03` | `file_context_primer_then_ambiguous` | file_context_primer_then_ambiguous | OBSERVE | True | True | True | False | True | False | 0 | `45cbe770-9a3d-42f2-95cb-0c4d31e931d1` |  |

## Interpretation

- `same_session` is valid only when transcript and session evidence both contain all prompt markers in one session.
- Cross-model A/B and Docker Desktop UI context injection remain deferred/manual.
