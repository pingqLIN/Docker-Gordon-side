# Gordon session / context availability 消融實驗完整報告

Run ID: `gordon_session_context_ablation_20260510_smoke`

## 結論摘要

本輪 CLI 自動化矩陣共執行 `9` 筆 case iteration，`PASS=0`、`OBSERVE=6`、`BLOCKED=3`。

本輪已擴大 same-session 重複抽樣，用於觀察同工作階段 carryover 與 boundary 訊號的方向性穩定度；仍不宣稱統計顯著。

## 關鍵觀察

- Same-session 三條 sequence 已進行重複抽樣；結果作為方向性穩定性觀察，仍需更多 repetitions 或不同日批次才能提升信心。
- Same-session smoke gate 未乾淨通過：`3/9` 筆為 `BLOCKED`，正式 `SEQ01` / `SEQ02` / `SEQ03` 各 10 次批次暫緩。
- 本輪 approval runner 未固定送入 `y`，且沒有 broad `A` approval；疑似 secret / write / destructive 訊號會保守拒絕。

## Aggregate Metrics

| Group | Condition | Topics | N | PASS | OBSERVE | FAIL | BLOCKED | Docker mapping rate | Tool execution rate | Boundary rate | Session-carryover signal | Denied approvals | Blocked rate |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `same_session` | `docker_primer_then_ambiguous` | docker_primer_then_ambiguous | 3 | 0 | 1 | 0 | 2 | 3/3 (100%) | 3/3 (100%) | 1/3 (33%) | 2/3 (67%) | 0 | 2/3 (67%) |
| `same_session` | `non_docker_primer_then_ambiguous` | non_docker_primer_then_ambiguous | 3 | 0 | 3 | 0 | 0 | 0/3 (0%) | 0/3 (0%) | 3/3 (100%) | 3/3 (100%) | 0 | 0/3 (0%) |
| `same_session` | `file_context_primer_then_ambiguous` | file_context_primer_then_ambiguous | 3 | 0 | 2 | 0 | 1 | 3/3 (100%) | 2/3 (67%) | 1/3 (33%) | 3/3 (100%) | 1 | 1/3 (33%) |

## 分組結果

| Group | Total | PASS | OBSERVE | BLOCKED |
|---|---:|---:|---:|---:|
| `same_session` | 9 | 0 | 6 | 3 |

## 限制

- Same-session 結果必須以同一 `session_id` 內的 RUN_ID / CASE_ID / prompt marker 佐證；若 evidence 找不到即標 `BLOCKED`。
- TUI approval 偵測採保守策略；任何 write / secret / destructive 訊號都會送 `n`。
- 本輪不測 Docker Desktop UI resource context injection，也不測 cross-model A/B。
- 本輪不宣稱統計顯著性；需要後續提高 repetitions 才能判斷穩定性。

## Evidence

- Prompt manifest: `frozen_prompt_manifest.json`
- Raw results: `raw_results.json`
- Rescored results: `raw_results.rescored.json`
- Archived final baseline rescore: `raw_results.final-baseline.rescored.json`
- Archived final baseline session evidence: `evidence-final-baseline/`
- Detailed tables: `RESULTS.md`
- Transcript/session evidence: `evidence/`
