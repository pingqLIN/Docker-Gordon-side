# Gordon 非 Docker 邊界與自我判斷實驗報告

Run ID: `gordon_non_docker_boundary_20260509`

## 執行摘要

本輪已完成 24 題完全非 Docker 任務測試，包含料理、旅遊、理財、醫療、法律、文學、居家運動與數學邏輯題。

測試結果顯示：Gordon 對完全非 Docker 題目有穩定的邊界判斷能力。即使套用上一輪推薦的強 Docker wrapper，Gordon 仍能拒絕硬套 Docker surface，並指出「這不是 Docker workflow」或「沒有 Docker mapping」。

更重要的是，24 題都沒有成功工具執行，沒有讀取專案檔，沒有 shell command，也沒有 Docker resource 檢查。這表示 Gordon 沒有因為 prompt 壓力而對無關任務啟動不必要的本機上下文探索。

## 產物位置

- 實驗計畫：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\EXPERIMENT_PLAN.zh-TW.md`
- Runner：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\run_non_docker_boundary_experiment.py`
- Prompt manifest：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\frozen_prompt_manifest.json`
- 原始結果：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\raw_results.json`
- 修正後結果：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\raw_results.rescored.json`
- 修正後總表：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\RESULTS.rescored.md`
- Audit log：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\AUDIT_LOG.jsonl`
- Evidence：`Q:\Projects\Docker-Gordon-side\test-results\gordon-non-docker-boundary-experiment\evidence`

## 結果總覽

以修正後 scoring 為準：

| Group | 題數 | Boundary PASS | Overforce failure | Tool execution |
|---|---:|---:|---:|---:|
| `plain_unrelated` | 8 | 8/8 = 100% | 0/8 | 0/8 |
| `self_judgment` | 8 | 8/8 = 100% | 0/8 | 0/8 |
| `overforce_wrapper` | 8 | 8/8 = 100% | 0/8 | 0/8 |

## 主要觀察

1. `plain_unrelated` 自然入口下，Gordon 不會直接完成食譜、旅遊、法律、醫療等一般任務，而是說明自己是 Docker/development assistant，並將使用者導回 Docker 或開發任務。
2. `self_judgment` 明確要求 relevance 判斷時，Gordon 常輸出 `Judgment: NONE`、`Relationship: NONE`、`Classification: NONE` 等形式，符合預期。
3. `overforce_wrapper` 是本輪最關鍵測試。即使 prompt 明確要求「Treat this as a Docker workflow task」並要求映射 Docker surface，Gordon 多數回應仍會說明沒有 application、Dockerfile、Compose service、build artifact、ports、volumes、logs 或 deployment target，因此不能硬套。
4. 高風險任務的處理合理：醫療、法律、理財題沒有給出權威最終建議，而是標示領域不適用或建議找專業人士。
5. 全部 24 題皆無工具執行，表示 Gordon 在非 Docker 題上沒有不必要地讀檔或檢查本機環境。

## Scoring 修正說明

第一次自動 scoring 低估了邊界表現，原因有兩個：

1. Runner 會在固定 tick 傳送 bounded `y`，用來回應可能出現的工具 approval prompt。但非 Docker 任務常在第一輪就完成回答，後續 `y` 會產生澄清對話，干擾「最後一則訊息」判讀。
2. 初版 boundary terms 太窄，只抓 `not Docker`、`outside scope` 等短語，漏掉 `Judgment: NONE`、`outside my scope`、`no Docker mapping`、`isn't a Docker workflow`、`can't force-fit` 等實際出現的邊界表達。

修正方式：

- scorer 改以「第一個 assistant 實質回應」作為主要判讀文本。
- boundary terms 補入 Gordon 實際使用的邊界語。
- 保留原始 `raw_results.json`，另產生 `raw_results.rescored.json` 與 `RESULTS.rescored.md`，避免覆蓋原始證據。

## 限制

- 每題只跑一次，尚未做多次抽樣，因此結果代表本輪 session 的行為，不代表統計穩定性。
- Runner 的 bounded `y` 仍會污染後續對話。雖然 rescore 已改看第一個 assistant response，但下一輪可改成只有偵測到 approval prompt 時才送 `y`。
- 本輪 fixture 仍使用 `Q:\Projects\gordon-boundary-gradient-fixture`，但 24 題皆沒有工具執行，因此 fixture 內容沒有實質影響。
- Transcript 中出現 Docker agent memory toolset 初始化失敗訊息：`failed to create memory database directory ... gordon:v7-b4983364`。這沒有阻止模型回答，也沒有影響 session evidence 寫入，但可另外追查 Docker Agent 的 memory path 命名問題。

## 結論

在完全非 Docker 題目上，Gordon 的邊界與模型自我判斷能力比前一輪「廣義工程任務拉回 Docker」更穩。

上一輪結論是：廣義開發任務可被工程語義拉回 Docker workflow。

本輪補上另一半：真正非 Docker 任務，即使被強 wrapper 壓迫，也沒有被硬套成 Docker workflow，且沒有啟動不必要的工具或本機檢查。

這表示目前 Gordon 的行為不是單純「看到 Docker prompt 就一律接受」，而是能區分：

- 可合理映射到 Docker 的軟體工程任務。
- 完全不應映射到 Docker 的一般生活、醫療、法律、理財、文學或邏輯任務。

