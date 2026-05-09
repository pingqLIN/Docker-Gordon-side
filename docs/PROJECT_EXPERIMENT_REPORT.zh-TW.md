# Docker Gordon Side Experiments 專案實驗總報告

日期：2026-05-10
Repository：`Docker-Gordon-side`
語言：繁體中文
範圍：Gordon / Docker AI 的上下文讀取、Docker 工作流程邊界、提示詞包裝、非 Docker 邊界、機密資料 / 高風險任務治理與公開發布整理。

## 1. 研究問題

本專案不是一般應用程式，而是一組針對 Docker Desktop Gordon / `docker ai` 行為的實驗證據庫。核心問題如下：

| 編號 | 研究問題 | 對應資料 |
|---|---|---|
| RQ1 | Gordon 是否會在未要求時讀取工作目錄、父目錄或敏感檔案？ | `GORDON_CONTEXT_AUDIT_REPORT.md`, `test-results/docker-ai-rerun/` |
| RQ2 | 明確 Docker 任務是否能穩定進入 Docker 工作流程？ | `test-results/gordon-prompt-framework-experiment/`, `test-results/gordon-boundary-gradient-experiment-v2/` |
| RQ3 | 當 Docker 外觀逐步變弱時，Gordon 的接受邊界在哪裡？ | `test-results/gordon-boundary-gradient-experiment-v2/`, `test-results/gordon-boundary-gradient-experiment-v3/` |
| RQ4 | 強提示詞包裝是否會把完全非 Docker 任務錯誤硬套到 Docker？ | `test-results/gordon-non-docker-boundary-experiment/` |
| RQ5 | 中文 / 中英混合語義、機密邊界與高風險 Docker 任務是否能被治理層處理？ | `test-results/gordon-final-governance-experiment/` |

## 2. 實驗方法總覽

| 實驗單元 | 方法 | 證據形式 |
|---|---|---|
| 上下文稽核 | 以金絲雀檔案、`.env` 假機密、工作階段資料庫檢查上下文讀取範圍 | 手冊、CLI 輸出、工作階段證據 |
| 提示詞框架 | 12 個 Docker-adjacent[鄰近 Docker] 正例、2 個負例，基準組 / 處理組配對 | `FINAL_REPORT.md`, `raw_results.json`, 逐字稿 |
| 邊界梯度 v2 | 錨點組 + 梯度組，逐步降低 Docker 顯性訊號 | `RESULTS.md`, `REPORT.zh-TW.md`, 提示詞清單 |
| 邊界精煉 v3 | 弱邊界題細切、觸發詞消融、提示詞包裝最小化 | `RESULTS.md`, `REPORT.zh-TW.md`, 乾淨重跑 |
| 非 Docker 邊界 | 料理、旅遊、理財、醫療、法律、文學、運動、邏輯題 | `RESULTS.rescored.md`, `REPORT.zh-TW.md` |
| 最終治理層 | 中文觸發、重複抽樣、機密邊界、高風險 Docker、詞彙陷阱 | `RESULTS.md`, `REPORT.zh-TW.md`, 重新評分後的原始結果 |

## 3. 單元報告

### 3.1 上下文稽核

`GORDON_CONTEXT_AUDIT_REPORT.md` 提供完整測試手冊，目標是檢查 Gordon 是否會在不同入口下讀取檔案、Docker 資源或使用者介面上下文。它設計了工作目錄金絲雀字串、Dockerfile / Compose 金絲雀字串、父目錄金絲雀字串、外部目錄金絲雀字串，以及 `.env` 假機密金絲雀字串。

主要價值是建立安全測試邊界：所有類機密資料必須是假資料；測試報告不得記錄真機密。此文件偏向執行手冊與假設整理，而不是所有項目都已完成的正式結果表。

### 3.2 提示詞框架實驗

位置：`test-results/gordon-prompt-framework-experiment/FINAL_REPORT.md`

| 指標 | 結果 |
|---|---:|
| 處理組正例通過率 | `12/12 = 100%` |
| 基準組正例通過率 | `12/12 = 100%` |
| 觀察到的提升 | `0 percentage points` |
| 負向對照 | 2 題皆維持非 Docker 邊界 |

判讀：提示詞架構可作為實務提示詞包裝，但這一輪不能證明它比基準組更好，因為測試夾具已經足夠 Docker-rich，基準組也全通過。

### 3.3 Boundary Gradient v2

位置：`test-results/gordon-boundary-gradient-experiment-v2/REPORT.zh-TW.md`

| 測試組 | Baseline | Treatment | 結論 |
|---|---:|---:|---|
| 錨點組 | `7/7 = 100%` | `7/7 = 100%` | 明確 Docker surface[表層訊號] 任務可穩定通過 |
| 梯度組 | `9/12 = 75%` | `12/12 = 100%` | 提示詞包裝在弱 Docker 外觀下有明顯幫助 |

關鍵掉點是 `G04`, `G10`, `G11`。這些題目仍可能是工程任務，但題面缺少 Docker surface[表層訊號]、`ports/logs/health`[連接埠 / 日誌 / 健康檢查]、`CI parity`[持續整合一致性]、`deployment readiness`[部署準備程度] 等訊號時，Gordon 容易轉成泛用專案檢查。

### 3.4 Boundary Refinement v3

位置：`test-results/gordon-boundary-gradient-experiment-v3/REPORT.zh-TW.md`

| 測試組 | 結果 | 修正後判讀 |
|---|---:|---|
| `boundary_refinement` | `7/10 = 70%` | `B02`, `B05`, `B10` 掉出 Docker 映射 |
| `trigger_ablation` | `7/10 = 70%` | `deployment readiness`[部署準備程度]、`CI parity`[持續整合一致性]、`reproducible dev/test/run`[可重現開發 / 測試 / 執行] 是強觸發 |
| `wrapper_minimization` | 主 v3 `9/15 = 60%` | H11 乾淨重跑後修正為 `11/15 = 73.3%` |

最實用的提示詞包裝是 `no_format` 版本：保留 Docker 映射、實質執行、只讀與避開機密，但移除固定輸出格式。`if_applicable` 太弱，不建議單獨使用。

### 3.5 Non-Docker Boundary

位置：`test-results/gordon-non-docker-boundary-experiment/REPORT.zh-TW.md`

| Group | Boundary PASS | Tool execution | Overforce failure |
|---|---:|---:|---:|
| `plain_unrelated` | `8/8 = 100%` | `0/8` | `0/8` |
| `self_judgment` | `8/8 = 100%` | `0/8` | `0/8` |
| `overforce_wrapper` | `8/8 = 100%` | `0/8` | `0/8` |

判讀：Gordon 不是單純看到提示詞包裝就接受所有任務。即使提示詞明確要求 Docker 工作流程，完全無關的生活、醫療、法律、理財、文學與邏輯題仍能維持非 Docker 邊界，且沒有啟動工具或本機檢查。

### 3.6 Final Governance

位置：`test-results/gordon-final-governance-experiment/REPORT.zh-TW.md`

| Group | Pass | 主要用途 |
|---|---:|---|
| `zh_trigger_ablation` | `6/6 = 100%` | 中文與中英混合提示詞觸發 |
| `repetition_boundary` | `6/6 = 100%` | 弱邊界題重複抽樣 |
| `secret_boundary` | `3/3 = 100%` | `.env` / 忽略規則 / 機密處理 |
| `risky_docker` | `3/3 = 100%` | 高風險 Docker 任務篩選 |
| `lexical_trap` | `3/3 = 100%` | 非 Docker 語境誤判陷阱 |

本輪最重要的修正是批准執行器改成只偵測模式，不再固定注入尾端 `y`。機密評分也拆分成「文字提到機密」與「工具實際讀取類機密檔案」，降低誤判。

## 4. 跨實驗結論

1. 明確 Docker 任務與 Docker-rich 測試夾具下，Gordon 基本可穩定進入 Docker 工作流程。
2. 提示詞包裝對弱 Docker 外觀有效，但不能用早期提示詞框架結果宣稱統計上的通用改善。
3. Gordon 的邊界不是單純字面規則。`ports/logs/health`[連接埠 / 日誌 / 健康檢查]、`CI parity`[持續整合一致性]、`deployment readiness`[部署準備程度]、`reproducible dev/test/run`[可重現開發 / 測試 / 執行]、`build/test/lint/run`[建置 / 測試 / 檢查 / 執行] 這些工程語義能明顯拉回 Docker 工作流程。
4. 完全非 Docker 任務在強提示詞包裝下仍能維持邊界，且沒有不必要工具執行。
5. 機密與高風險 Docker 任務應以工具實際行為為準，不應只靠文字命中評分。
6. CLI 自動化結果不能替代 Docker Desktop 使用者介面上下文注入測試，後者仍需要人工或瀏覽器 / 桌面層證據補完。

## 5. 限制

| 限制 | 影響 | 處置 |
|---|---|---|
| 多數早期題目每題只跑一次 | 不能宣稱統計顯著性 | Final governance 補部分重複抽樣，但仍有限 |
| 早期固定節奏 `y` 批准污染 | 可能干擾最後訊息判讀 | 後續評分器改看第一個實質回應；最終執行器改為只偵測模式 |
| Docker Desktop 使用者介面上下文注入未完整自動化 | CLI 結論不可直接外推到 Desktop 資源畫面 | 在 README 與報告標註仍需人工補完 |
| 原始證據可能包含本機路徑、工作階段逐字稿與假金絲雀字串 | 公開時需標註資料性質 | README 與公開發布審查明確警示 |
| 專案包含大量證據逐字稿 | GitHub 儲存庫體積與可讀性成本較高 | README 提供索引，總報告保留摘要 |

## 6. 公開發布摘要

本儲存庫適合以「研究證據庫」形式公開，但需要保留以下公開說明：

- 所有機密 / 權杖 / 金鑰字樣均為測試用假金絲雀字串或模型文字回覆，不應包含真機密。
- 原始證據可能包含本機 Windows 路徑與 Docker Agent 工作階段中繼資料。
- 結論主要描述本批測試夾具與執行器的觀察，不代表 Docker Gordon 在所有版本、所有模型或所有 Desktop 使用者介面上下文下的保證行為。
- `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md` 含有後續研究方向，屬於研究路線整理；若將儲存庫公開，視為一併公開該研究脈絡。

## 7. 建議引用順序

1. 先讀 `README.md` 或 `README.zh-TW.md`。
2. 再讀本總報告：`docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md`。
3. 需要細節時讀各實驗的 `REPORT.zh-TW.md` / `RESULTS.md`。
4. 需要驗證時查 `raw_results.json`, `raw_results.rescored.json`, `AUDIT_LOG.jsonl`, `frozen_prompt_manifest.json`, `evidence/`。
