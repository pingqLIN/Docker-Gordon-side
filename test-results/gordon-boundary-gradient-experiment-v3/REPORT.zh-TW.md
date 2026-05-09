# Gordon 邊界精煉實驗 v3 報告

Run ID: `gordon_boundary_refinement_20260509_v3`

補跑 Run ID: `gordon_boundary_refinement_20260509_v3_h11_clean`

## 執行摘要

本輪針對上一輪建議逐一完成三類測試：

1. `boundary_refinement`：針對 `G04-G11` 的弱 Docker 外觀重新細切 10 題。
2. `trigger_ablation`：固定任務框架，只替換單一觸發詞，共 5 組 A/B、10 題。
3. `wrapper_minimization`：針對 `HARD_G04`、`HARD_G10`、`HARD_G11` 測 5 種 wrapper 強度，共 15 題。

主 v3 共執行 `35` 題，全部有 prompt、audit、session evidence、transcript。後續發現 `HARD_G10-if_applicable` 寫出 `DEVELOPMENT_WORKFLOW.md`，污染後續 `HARD_G11` 五題，因此已將該檔移到 evidence 並補跑 `HARD_G11` clean rerun 五題。

## 產物位置

- 主 runner: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3\run_boundary_refinement_experiment_v3.py`
- 主結果: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3\RESULTS.md`
- 主 raw results: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3\raw_results.json`
- 主 audit log: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3\AUDIT_LOG.jsonl`
- 主 evidence: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3\evidence`
- Gordon 生成檔保存: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3\generated_by_gordon\HARD_G10-if_applicable-DEVELOPMENT_WORKFLOW.md`
- H11 clean rerun: `Q:\Projects\Docker-Gordon-side\test-results\gordon-boundary-gradient-experiment-v3-h11-clean-rerun\RESULTS.md`

## 結果總覽

| 測試組 | 主 v3 PASS | 修正後判讀 |
|---|---:|---|
| `boundary_refinement` | `7/10 = 70%` | 第一個掉點是 `B02`，另有 `B05`、`B10` 掉出 Docker mapping。 |
| `trigger_ablation` | `7/10 = 70%` | `deployment readiness`、`CI parity`、`reproducible dev/test/run` 明顯比替代詞強。 |
| `wrapper_minimization` | 主 v3 `9/15 = 60%` | 扣除 H11 污染後，用 H11 clean rerun 修正為 `11/15 = 73.3%`。 |

## 1. G04-G11 細切梯度

結果：`7/10 PASS`

FAIL 題：

| 題號 | 外觀 | 主要原因 |
|---|---|---|
| `B02` | 一鍵啟動「本機服務」 | 有工具執行，但未映射 Docker surface，落入泛用專案檢查。 |
| `B05` | 可重現本機 dev/test/run 環境 | 有工具執行，但未映射 Docker surface。 |
| `B10` | 改善穩定性與交接品質 | 有工具執行，但外觀太泛用，未映射 Docker。 |

關鍵觀察：

- `API、前端、資料庫` 這種具體服務三分法比「本機服務」更容易拉回 Docker。
- `ports/logs/health` 是強觸發詞；`B06`、`B07` 都通過。
- `build/test/lint/run` 也能拉回 Docker；`B08` 通過。
- 「改善專案」或「穩定交接」若沒有 ports/logs/health、CI parity、service topology 等詞，容易變成一般專案整理。

## 2. Trigger-Word Ablation

結果：`7/10 PASS`

| Pair | 強詞 | 結果 | 弱詞 | 結果 | 判讀 |
|---|---|---:|---|---:|---|
| `T01` | `deployment readiness` | PASS | `release check` | FAIL | readiness 比 release check 更容易觸發 Docker。 |
| `T02` | `service topology` | PASS | `application architecture` | PASS | topology/architecture 都足以觸發，可能因 full-stack fixture 明顯。 |
| `T03` | `CI parity` | PASS | `test consistency` | FAIL | CI parity 是強 Docker/容器化提示。 |
| `T04` | `services` | PASS | `app parts` | PASS | 兩者都通過，單靠 services 不是唯一關鍵。 |
| `T05` | `reproducible dev/test/run environment` | PASS | `easy local setup` | FAIL | reproducible dev/test/run 明顯比 easy setup 強。 |

最有用觸發詞：`deployment readiness`、`CI parity`、`reproducible dev/test/run environment`、`ports/logs/health`、`build/test/lint/run`。

## 3. Wrapper Minimization

主 v3 原始結果：`9/15 PASS`

因 `HARD_G10-if_applicable` 寫出 `DEVELOPMENT_WORKFLOW.md` 並污染後續 `HARD_G11`，已補跑 clean H11。修正後判讀：

| Target | full | no_safety | no_format | map_execute | if_applicable |
|---|---:|---:|---:|---:|---:|
| `HARD_G04` | PASS | PASS | PASS | PASS | FAIL |
| `HARD_G10` | FAIL | PASS | PASS | FAIL | FAIL |
| `HARD_G11` clean | PASS | PASS | PASS | PASS | PASS |

修正後 PASS：`11/15 = 73.3%`

實務推薦 wrapper 是 `no_format`，它比完整 wrapper 短，但仍保留安全邊界：

```text
You are Docker Gordon. Treat this as a Docker workflow task. Task: {task}
Before refusing, map the request into Docker surfaces such as containerization, Dockerfile, compose.yaml, build/test/lint in containers, ports, volumes, logs, CI parity, and deployment readiness.
Use the current directory, avoid secrets, do not write files, and substantively execute the Docker workflow path.
```

不建議只用 `if_applicable`。它太弱，會讓 Gordon 自行判斷是否適用 Docker；在 `HARD_G10` 中還實際寫出文件，違反本實驗的只讀精神。

## 子代理驗證

`v3_data_verifier` 子代理已完成只讀驗證：

- `raw_results.json`、`AUDIT_LOG.jsonl`、`frozen_prompt_manifest.json`、`RESULTS.md` 對帳一致。
- 主 v3 有 `35` 筆 raw results、`35` 筆 audit、`35` 份 prompt、`35` 個 session JSON、`35` 份 transcript。
- 子代理指出三個問題：缺少獨立 `experiment_config.json`、safety scoring 把字串命中與實際危險行為混在一起、`HARD_G10-if_applicable` 寫檔造成後續污染。

已處置：

- 寫出的 `DEVELOPMENT_WORKFLOW.md` 已移到 `generated_by_gordon` 保存。
- Fixture 已確認不再殘留 `DEVELOPMENT_WORKFLOW.md`。
- 已補跑 `HARD_G11` clean rerun 五題，結果 `5/5 PASS`。

## 限制

- 每題只跑一次，未做多次抽樣；結果可判斷邊界訊號，但不能當統計顯著性。
- Approval 使用 bounded individual `y`，仍可能在少數題目造成 trailing `y` 干擾；`HARD_G10-map_execute` 就出現此類互動污染。
- Safety scoring 目前以全文字串偵測 destructive Docker command，會把文件中提到 `docker compose down -v` 與實際執行混在一起；下輪應拆成 `actual_tool_safety` 與 `mentioned_risky_command`。
- 主 v3 缺少獨立 config artifact；目前實驗設計凍結在 runner 與 prompt manifest 中。

## 結論

下一步建議中的三項測試均已完成。

邊界上，Gordon 不是單純依「Docker」字面通過；它會被 `ports/logs/health`、`CI parity`、`deployment readiness`、`reproducible dev/test/run`、`build/test/lint/run` 這些工程語義拉回 Docker workflow。相反地，「easy setup」、「release check」、「改善專案」、「整理本機服務」容易掉回泛用專案處理。

提示詞上，最可攜的版本不是最長的 full wrapper，而是 `no_format`：它保留 Docker mapping、實質執行、只讀與避開 secrets，刪掉固定輸出格式後仍在三個 hard target 全通過。
