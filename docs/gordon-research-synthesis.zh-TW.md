# Docker Gordon 實驗研究總結報告

- Project: `Docker-Gordon-side`
- Date: 2026-05-10
- Language: zh-TW
- Scope: 彙整本儲存庫內 Gordon / Docker AI 的上下文讀取、任務邊界、提示詞包裝、治理層與安全篩選實驗結果。

## 1. 結論摘要

本儲存庫的實驗結果支持一個核心結論：Gordon 的行為不是單純由「是否出現 Docker 字面詞」決定，也不能只歸因於單一模型或 CLI。較合理的解釋是：Gordon 的任務篩選由模型語義能力、Gordon 系統提示詞 / 提示詞包裝 / 工具結構描述 / 政策、CLI 或 Docker Desktop 執行期上下文、批准閘門與工作階段歷史共同構成。

在強 Docker surface[表層訊號] 的任務上，Gordon 的基準組已經接近飽和；`gordon-prompt-framework-experiment` 中正向 Docker-adjacent[鄰近 Docker] 語料的基準組與處理組都是 `12/12 = 100%`，因此不能用該批資料證明提示詞包裝對明顯 Docker 任務有額外提升。

真正有鑑別力的是弱 Docker 外觀與邊界任務。`gordon-boundary-gradient-experiment-v2` 顯示梯度組基準組 `9/12 = 75%`，處理組 `12/12 = 100%`；`v3` 進一步顯示 `deployment readiness`[部署準備程度]、`CI parity`[持續整合一致性]、`ports/logs/health`[連接埠 / 日誌 / 健康檢查]、`reproducible dev/test/run`[可重現開發 / 測試 / 執行]、`build/test/lint/run`[建置 / 測試 / 檢查 / 執行] 等工程語義能把任務拉回 Docker 工作流程。

完全非 Docker 題目則呈現另一種穩定性。`gordon-non-docker-boundary-experiment` 的 24 題在一般入口、自我判斷、過度強制提示詞包裝三組中全數邊界通過，且 `0/24` 有工具執行，表示強提示詞包裝沒有把料理、旅遊、醫療、法律、理財、文學或邏輯題硬套成 Docker 任務。

最終治理層實驗 `gordon-final-governance-experiment` 修正了早期執行器固定送入 `y` 的污染，改為偵測批准提示後才回覆，並在疑似破壞性 Docker 指令或類機密讀取時送 `n`。該輪 21 筆案例迭代全部通過，涵蓋中文觸發、弱邊界重複抽樣、機密邊界、高風險 Docker 任務與詞彙陷阱。

## 2. 主要實驗總表

| 實驗 | 研究問題 | 方法 | 核心結果 | 主要證據 |
|---|---|---|---|---|
| 上下文稽核 / 重跑 | Gordon 何時讀取工作目錄、Dockerfile、Compose、`.env`、父目錄或 Docker 資源上下文 | 金絲雀測試夾具、`session.db`、CLI / 互動式重跑 | 儲存庫目前保留完整測試手冊與部分重跑證據；正式上下文稽核仍需逐工作階段填表驗證 | `GORDON_CONTEXT_AUDIT_REPORT.md`, `test-results/docker-ai-rerun/` |
| AGENTS 層稽核 | Gordon 是否自動載入 AGENTS.md，以及明確讀取時如何判斷優先序 | 多層 AGENTS 測試夾具、工作階段證據 | 不讀取基準組未看見權杖；明確檢查時最近的 AGENTS.md 生效；功能層級 run 曾越界讀到 `Q:\AGENTS.md` | `test-results/gordon-agent-layer-audit/SUMMARY.md` |
| 提示詞框架 | Docker 工作流程提示詞包裝是否達成正向任務 80% 成功標準 | 12 個正向任務、2 個負向對照、基準組 / 處理組配對 | 處理組 `12/12`，基準組也 `12/12`；負向對照通過；提示詞包裝可用但未證明提升 | `test-results/gordon-prompt-framework-experiment/FINAL_REPORT.md` |
| 邊界梯度 v2 | Docker 訊號遞減時，基準組何時掉出 Docker 工作流程；提示詞包裝是否補回 | 錨點組 7 題、梯度組 12 題，各有基準組 / 處理組 | 錨點組基準組 / 處理組 `7/7`；梯度組基準組 `9/12`，處理組 `12/12`；掉點為 `G04`, `G10`, `G11` | `test-results/gordon-boundary-gradient-experiment-v2/REPORT.zh-TW.md` |
| 邊界精煉 v3 | 哪些觸發詞 / 提示詞包裝強度對邊界題最有效 | `boundary_refinement`, `trigger_ablation`, `wrapper_minimization` | 精煉組 `7/10`；觸發詞消融 `7/10`；提示詞包裝最小化修正後 `11/15`；推薦 `no_format` 提示詞包裝 | `test-results/gordon-boundary-gradient-experiment-v3/REPORT.zh-TW.md` |
| 非 Docker 邊界 | Gordon 是否會被強提示詞包裝逼迫硬套完全無關任務 | 8 題 x 3 條件，共 24 題 | 三組皆 `8/8 = 100%` 邊界通過；`0/24` 工具執行 | `test-results/gordon-non-docker-boundary-experiment/REPORT.zh-TW.md` |
| 最終治理層 | 修正批准執行器後，中文、機密、高風險、詞彙陷阱是否仍可安全通過 | 21 筆案例迭代，只偵測批准執行器，重新評分機密邏輯 | 總計 `21/21 = 100%`；五組皆全通過；Desktop 使用者介面與跨模型仍需人工補完 | `test-results/gordon-final-governance-experiment/REPORT.zh-TW.md` |

## 3. 研究問題與整體判讀

### 3.1 Gordon 是否會把一般任務硬套成 Docker？

目前證據顯示不會一律硬套。完全非 Docker 題目在 `plain_unrelated`、`self_judgment`、`overforce_wrapper` 三組中都能被 Gordon 拒絕或標示為無 Docker 映射，而且沒有工具執行。這支持「Gordon 仍保有語義邊界判斷」的結論。

但對軟體工程任務，Gordon 的判斷會受工程語義影響。即使提示詞沒有明講 Docker，只要出現 `deployment readiness`[部署準備程度]、`CI parity`[持續整合一致性]、可重現環境、`ports/logs/health`[連接埠 / 日誌 / 健康檢查]、`build/test/lint/run`[建置 / 測試 / 檢查 / 執行] 等詞，就更可能被映射到 Docker 工作流程。

### 3.2 提示詞包裝的作用是什麼？

提示詞包裝對強 Docker 任務沒有顯著可觀測提升，因為基準組已經全通過。但在弱 Docker 外觀上，提示詞包裝的邊際效果明顯。v2 的梯度組處理組從基準組 `9/12` 拉到 `12/12`，v3 的提示詞包裝最小化也顯示只保留 Docker 映射、實質執行、只讀、不讀機密等關鍵約束，就能達到比完整固定格式更可攜的效果。

最實用的版本是 v3 推薦的 `no_format` 提示詞包裝，因為它保留操作約束但不強迫固定回答格式。相對地，`if_applicable` 太弱，容易讓 Gordon 自行判斷不適用 Docker；在 `HARD_G10-if_applicable` 中還曾寫出 `DEVELOPMENT_WORKFLOW.md`，造成後續 H11 run 污染。

### 3.3 模型本身、治理層與 CLI 哪個影響最大？

目前尚未完成 cross-model controlled experiment，因此不能宣稱 Haiku、Sonnet 或其他模型之間的統計差異。基於既有資料，較穩健的說法是：

- 模型語義層提供必要的語義判斷能力，這可由非 Docker 過度強制情境仍拒絕硬套得到支持。
- 治理層 / 提示詞 / 工具結構描述 / 提示詞包裝對邊界 Docker 任務的影響最大，這可由 v2 / v3 提示詞包裝與觸發詞消融的差異得到支持。
- CLI / Desktop 執行期主要提供上下文、工具入口、批准閘門與證據通道；它可能改變模型看見的資訊，但不是主要語義分類器。

外部 GPT 5.5 PRO 審查也給出相近判讀：任務篩選不是 Haiku 單獨主導，也不是 CLI 單獨主導，而是模型 + 治理層 + 執行期上下文的組合。見 `test-results/GPT55PRO.md` 與 `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md`。

### 3.4 上下文讀取與檔案邊界有何風險？

`GORDON_CONTEXT_AUDIT_REPORT.md` 提供了完整測試手冊，但它更像測試設計與判讀標準，不是所有項目都已填表完成的最終結果。此類結論必須逐工作階段以 `session.db`、除錯日誌、錄製紀錄或逐字稿查證，不能只根據 Gordon 畫面回答推定。

已完成的 AGENTS 層稽核顯示，Gordon 不會在不讀取基準組自動透露 AGENTS 權杖；但在明確要求檢查 AGENTS.md 優先序時，功能層級 run 曾讀到指定邊界之外的 `Q:\AGENTS.md`。這代表「明確要求向上尋找規則檔」時，工具讀取範圍仍需用提示詞護欄與工作階段證據驗證。

## 4. 可重現性與證據完整性

本儲存庫的主要自動化實驗具備可重現性素材：

- 執行器腳本：`run_*.py`
- 提示詞清單：`frozen_prompt_manifest.json`
- 原始結果：`raw_results.json` / `raw_results.rescored.json`
- 稽核日誌：`AUDIT_LOG.jsonl`
- 證據：工作階段 JSON 與逐字稿文字

主要位置包括：

- `test-results/gordon-prompt-framework-experiment/`
- `test-results/gordon-boundary-gradient-experiment-v2/`
- `test-results/gordon-boundary-gradient-experiment-v3/`
- `test-results/gordon-boundary-gradient-experiment-v3-h11-clean-rerun/`
- `test-results/gordon-non-docker-boundary-experiment/`
- `test-results/gordon-final-governance-experiment/`

較早期的 `test-results/docker-ai-rerun/` 與根目錄層級 `T01-*` 至 `T07-*` 產物可作為上下文讀取補充證據，但不像最終治理層 / v2 / v3 那樣具備完整一致的執行器、清單、原始結果與稽核日誌結構。

## 5. 已知限制

1. 多數早期與 v3 題目每題只跑一次，適合判斷邊界訊號，不適合宣稱統計顯著。
2. 提示詞框架、v2、v3 與非 Docker 實驗的早期執行器使用固定節奏個別 `y` 批准，可能造成尾端 `y` 對逐字稿或最後訊息判讀的污染。
3. 最終治理層已修正批准策略，但 TUI 批准提示偵測仍可能偏保守；若畫面文字含類機密訊號，執行器可能送 `n` 並留下拒絕紀錄。
4. v3 曾出現 `HARD_G10-if_applicable` 寫檔污染後續 `HARD_G11`，雖已移至 `generated_by_gordon/` 並補跑乾淨重跑，但這也證明測試夾具衛生對代理評測很重要。
5. 跨模型 A/B 尚未完成；目前不能把觀察到的行為精確分解為 Haiku 模型效果、Gordon 提示詞效果或工具結構描述效果。
6. Docker Desktop 使用者介面上下文注入尚未自動化；容器日誌、映像檢查、建置失敗上下文等入口仍需人工對照。
7. 上下文稽核的 `.env`、父目錄、外部目錄、符號連結 / junction、工作階段歷史等測試有完整設計，但仍需逐工作階段完成正式結果表。
8. 原始證據可能包含完整工具回應、本機路徑、工作階段 ID 與假金絲雀字串；公開前需重新審查與必要的遮蔽。

## 6. 建議的後續驗證

優先完成 Docker Desktop 使用者介面上下文注入對照：同一提示詞分別從 CLI、Desktop detached Gordon、容器日誌、映像檢查、建置失敗上下文入口執行，檢查工作階段項目是否已注入日誌 / 檢查 / 建置錯誤，以及是否無工具呼叫就引用使用者介面上下文。

擴大重複抽樣：針對 `G04`, `G10`, `G11`, `B02`, `B05`, `B10`、中文弱觸發、高風險 Docker 任務與詞彙陷阱，每題至少 10 次，重要邊界題可提高到 20-30 次。

在可控模型機制出現後再做跨模型 A/B：固定測試夾具、提示詞、工具集、評分器與執行器，只替換模型，以分離模型語義層與治理層 / 工具結構描述的邊際效果。

補完上下文稽核正式表格：尤其是 `.env`、`.dockerignore` / `.gitignore`、父目錄 / 外部目錄、符號連結 / junction、Windows / WSL 路徑、同工作階段與新工作階段、錄製紀錄與 `session.db` 搜尋。

保持最終治理層執行器的只偵測批准策略，並繼續把 `actual_tool_secret_access`、`secret_mentioned_only`、`actual_tool_safety`、`mentioned_risky_command` 分開評分。

## 7. 公開前內容控管

本儲存庫已依公開研究證據庫的方向更新 README，並明確標示測試資料可能含假金絲雀字串、假機密 / 權杖標記、本機路徑、工作階段 ID、原始逐字稿、工作階段 JSON 與除錯日誌。公開前檢查重點如下：

- 假機密 / 權杖標記是否可能被掃描器誤判並造成誤報。
- 本機 Windows 路徑是否被讀者誤解為憑證或部署資訊。
- 後續工作 / 仍需人工補完項目是否被誤讀成已完成結論。
- 原始證據是否應被視為研究資料，而不是乾淨的產品文件。

本次公開策略不是刪除原始證據，而是將儲存庫定位為「研究證據庫」，保留可追溯資料並在 README、`docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md`、`docs/PUBLIC_RELEASE_REVIEW.zh-TW.md` 中清楚標註資料性質與限制。
