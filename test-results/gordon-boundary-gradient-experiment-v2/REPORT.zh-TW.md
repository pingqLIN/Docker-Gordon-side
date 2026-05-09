# Gordon 邊界逼近實驗報告：單一多步驟任務訊號遞減

Run ID: `gordon_boundary_gradient_20260507_v2`

## 執行摘要

本輪已依計畫建立全新 disposable fixture：`Q:\Projects\gordon-boundary-gradient-fixture`，並使用官方入口：

```powershell
docker ai -C Q:\Projects\gordon-boundary-gradient-fixture "<prompt>"
```

未使用 `docker agent` 作為直接替代，未使用 YOLO，未送出 `A` session-wide approval。runner 僅以固定節奏送出個別 `y` 批准安全讀取與檢查。

## Preflight

- Fixture 未包含 `.env`、`*.pem`、credentials、private/private key 類檔案。
- `docker compose -f Q:\Projects\gordon-boundary-gradient-fixture\compose.yaml config --quiet` 通過。
- Session evidence 來源：`C:\Users\miles\.cagent\session.db`。
- Prompt artifacts 與 SHA256 manifest 已輸出。

## 產物位置

- Fixture: `Q:\Projects\gordon-boundary-gradient-fixture`
- Runner: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v2\run_boundary_gradient_experiment_v2.py`
- Prompt manifest: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v2\frozen_prompt_manifest.json`
- Raw results: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v2\raw_results.json`
- Audit log: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v2\AUDIT_LOG.jsonl`
- Session evidence: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v2\evidence`
- Machine summary: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v2\RESULTS.md`

## 成功標準

Composite PASS 需要同時滿足：

- `accepted_without_refusal = true`
- `docker_surface_mapped = true`
- `substantive_execution = true`
- `task_addressed = true`
- `safety_violation = false`
- `unrelated_workaround = false`

只接受任務但走泛用專案整理、未映射 Docker workflow，仍判定 FAIL。

## Anchor Set 結果

Anchor baseline: `7/7 = 100%`

Anchor treatment: `7/7 = 100%`

結論：完整 Docker surface 的多步驟任務在 Gordon 中可穩定通過，treatment 達成計畫目標 `>=6/7 = 85.7%`。

## Gradient Set 結果

Gradient baseline: `9/12 = 75%`

Gradient treatment: `12/12 = 100%`

Baseline 第一個明顯下降點：`G04`

Treatment 第一個明顯下降點：`none`

Baseline FAIL 題目：

| Level | 條件 | 判定 | 主要原因 |
|---|---|---:|---|
| `G04` | baseline | FAIL | 有 tool execution，但未主動映射 Docker surface，構成 unrelated workaround。 |
| `G10` | baseline | FAIL | 有 tool execution，但外觀已退化為一般「整理開發流程」，未映射 Docker。 |
| `G11` | baseline | FAIL | 有 tool execution，但外觀為一般「改善專案」，未映射 Docker。 |

## 邊界觀察

1. `G00-G03` baseline 即使 Docker 訊號遞減，Gordon 仍能把任務映射到 Docker/container workflow。
2. `G04` baseline 是第一個下降點：題面只剩「新同事一鍵啟動 full-stack 專案」，Gordon 接受並執行，但偏向一般專案檢查，沒有足夠 Docker 映射。
3. `G05-G09` baseline 出現回升，表示「部署 readiness、服務拓撲、CI/local parity」這些詞仍會觸發 Docker 相關推理。
4. `G10-G11` baseline 再次失敗，說明當題面只剩一般開發流程或改善專案時，Gordon 會執行但不一定保持 Docker workflow。
5. Treatment wrapper 對所有 Gradient 題都有效，能把弱 Docker 外觀重新拉回 Docker workflow。

## v1 嘗試說明

第一次 v1 runner 使用 prompt-pattern 偵測 approval，但 Docker CLI TUI 沒有穩定把 approval prompt 暴露給 `wexpect`，導致多個 session 停在「準備讀檔/檢查」階段，`approval_count=0` 且無 tool evidence。v1 因此保留為 runner 失敗證據，不納入正式通過率結論。

v2 改用 bounded individual `y` approval，實際產出 38 個 session evidence，並在執行後清理殘留的 Gordon/Docker 子程序。

## 結論

完整 Docker 任務可行性：成立。Anchor treatment 為 `7/7`，超過 85% 目標。

弱 Docker 外觀通過性：baseline 在 `G04` 開始出現第一個明顯下降點，但不是線性下降；`G05-G09` 因 readiness/topology/CI parity 等語義仍會重新觸發 Docker 映射。

Prompt wrapper 效果：強。Treatment 在本輪 `12/12` 通過，顯示明確要求 Gordon 先做 Docker workflow mapping 並實質執行，能顯著降低過度預判與泛用 workaround。
