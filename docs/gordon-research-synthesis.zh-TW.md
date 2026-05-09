# Docker Gordon 實驗研究總結報告

- Project: `Docker-Gordon-side`
- Date: 2026-05-10
- Language: zh-TW
- Scope: 彙整本 repo 內 Gordon / Docker AI 的 context-reading、任務邊界、prompt wrapper、治理層與安全篩選實驗結果。

## 1. 結論摘要

本 repo 的實驗結果支持一個核心結論：Gordon 的行為不是單純由「是否出現 Docker 字面詞」決定，也不能只歸因於單一模型或 CLI。較合理的解釋是：Gordon 的任務篩選由模型語義能力、Gordon system prompt / wrapper / tool schema / policy、CLI 或 Docker Desktop runtime context、approval gating 與 session history 共同構成。

在強 Docker surface 的任務上，Gordon 的 baseline 已經接近飽和；`gordon-prompt-framework-experiment` 中 positive Docker-adjacent corpus baseline 與 treatment 都是 `12/12 = 100%`，因此不能用該批資料證明 wrapper 對明顯 Docker 任務有額外提升。

真正有鑑別力的是弱 Docker 外觀與邊界任務。`gordon-boundary-gradient-experiment-v2` 顯示 Gradient baseline `9/12 = 75%`，treatment `12/12 = 100%`；`v3` 進一步顯示 `deployment readiness`、`CI parity`、`ports/logs/health`、`reproducible dev/test/run`、`build/test/lint/run` 等工程語義能把任務拉回 Docker workflow。

完全非 Docker 題目則呈現另一種穩定性。`gordon-non-docker-boundary-experiment` 的 24 題在 plain、self-judgment、overforce wrapper 三組中全數 boundary pass，且 `0/24` 有工具執行，表示強 wrapper 沒有把料理、旅遊、醫療、法律、理財、文學或邏輯題硬套成 Docker 任務。

最終治理層實驗 `gordon-final-governance-experiment` 修正了早期 runner 固定送入 `y` 的污染，改為偵測 approval prompt 後才回覆，並在疑似 destructive Docker command 或 secret-like read 時送 `n`。該輪 21 筆 case iteration 全部通過，涵蓋中文 trigger、弱邊界重複抽樣、secret boundary、risky Docker task 與 lexical trap。

## 2. 主要實驗總表

| 實驗 | 研究問題 | 方法 | 核心結果 | 主要證據 |
|---|---|---|---|---|
| Context audit / rerun | Gordon 何時讀取 working directory、Dockerfile、Compose、`.env`、父目錄或 Docker resource context | canary fixture、session.db、CLI/interactive rerun | repo 目前保留完整測試手冊與部分 rerun 證據；正式 context audit 仍需逐 session 填表驗證 | `GORDON_CONTEXT_AUDIT_REPORT.md`, `test-results/docker-ai-rerun/` |
| AGENTS layer audit | Gordon 是否自動載入 AGENTS.md，以及明確讀取時如何判斷 precedence | 多層 AGENTS fixture、session evidence | no-read baseline 未看見 token；明確檢查時最近 AGENTS.md 生效；feature-level run 曾越界讀到 `Q:\AGENTS.md` | `test-results/gordon-agent-layer-audit/SUMMARY.md` |
| Prompt framework | Docker workflow prompt wrapper 是否達成 positive task 80% 成功標準 | 12 positive tasks、2 negative controls、baseline/treatment 配對 | treatment `12/12`，baseline 也 `12/12`；negative controls pass；wrapper 可用但未證明提升 | `test-results/gordon-prompt-framework-experiment/FINAL_REPORT.md` |
| Boundary gradient v2 | Docker 訊號遞減時，baseline 何時掉出 Docker workflow；wrapper 是否補回 | Anchor 7 題、Gradient 12 題，各 baseline/treatment | Anchor baseline/treatment `7/7`；Gradient baseline `9/12`，treatment `12/12`；掉點為 `G04`, `G10`, `G11` | `test-results/gordon-boundary-gradient-experiment-v2/REPORT.zh-TW.md` |
| Boundary refinement v3 | 哪些 trigger word / wrapper 強度對邊界題最有效 | `boundary_refinement`, `trigger_ablation`, `wrapper_minimization` | refinement `7/10`；trigger ablation `7/10`；wrapper minimization 修正後 `11/15`；推薦 `no_format` wrapper | `test-results/gordon-boundary-gradient-experiment-v3/REPORT.zh-TW.md` |
| Non-Docker boundary | Gordon 是否會被強 wrapper 逼迫硬套完全無關任務 | 8 題 x 3 conditions，共 24 題 | 三組皆 `8/8 = 100%` boundary pass；`0/24` tool execution | `test-results/gordon-non-docker-boundary-experiment/REPORT.zh-TW.md` |
| Final governance | 修正 approval runner 後，中文、secret、risky、lexical trap 是否仍可安全通過 | 21 case iterations，detect-only approval runner，rescored secret logic | Total `21/21 = 100%`；五組皆全通過；Desktop UI 與 cross-model 仍 deferred/manual | `test-results/gordon-final-governance-experiment/REPORT.zh-TW.md` |

## 3. 研究問題與整體判讀

### 3.1 Gordon 是否會把一般任務硬套成 Docker？

目前證據顯示不會一律硬套。完全非 Docker 題目在 `plain_unrelated`、`self_judgment`、`overforce_wrapper` 三組中都能被 Gordon 拒絕或標示為無 Docker mapping，而且沒有工具執行。這支持「Gordon 仍保有語義邊界判斷」的結論。

但對軟體工程任務，Gordon 的判斷會受工程語義影響。即使 prompt 沒有明講 Docker，只要出現 deployment readiness、CI parity、reproducible environment、ports/logs/health、build/test/lint/run 等詞，就更可能被映射到 Docker workflow。

### 3.2 Prompt wrapper 的作用是什麼？

Prompt wrapper 對強 Docker 任務沒有顯著可觀測提升，因為 baseline 已經全通過。但在弱 Docker 外觀上，wrapper 的邊際效果明顯。v2 的 Gradient treatment 從 baseline `9/12` 拉到 `12/12`，v3 的 wrapper minimization 也顯示只保留 Docker mapping、實質執行、只讀、不讀 secrets 等關鍵約束，就能達到比完整固定格式更可攜的效果。

最實用的版本是 v3 推薦的 `no_format` wrapper，因為它保留操作約束但不強迫固定回答格式。相對地，`if_applicable` 太弱，容易讓 Gordon 自行判斷不適用 Docker；在 `HARD_G10-if_applicable` 中還曾寫出 `DEVELOPMENT_WORKFLOW.md`，造成後續 H11 run 污染。

### 3.3 模型本身、治理層與 CLI 哪個影響最大？

目前尚未完成 cross-model controlled experiment，因此不能宣稱 Haiku、Sonnet 或其他模型之間的統計差異。基於既有資料，較穩健的說法是：

- Model semantic layer 提供必要的語義判斷能力，這可由 non-Docker overforce 仍拒絕硬套得到支持。
- Governance / prompt / tool schema / wrapper 對 borderline Docker task 的影響最大，這可由 v2/v3 wrapper 與 trigger ablation 的差異得到支持。
- CLI / Desktop runtime 主要提供 context、工具入口、approval gating 與 evidence channel；它可能改變模型看見的資訊，但不是主要語義分類器。

外部 GPT 5.5 PRO 審查也給出相近判讀：任務篩選不是 Haiku 單獨主導，也不是 CLI 單獨主導，而是 model + governance layer + runtime context 的組合。見 `test-results/GPT55PRO.md` 與 `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md`。

### 3.4 Context-reading 與檔案邊界有何風險？

`GORDON_CONTEXT_AUDIT_REPORT.md` 提供了完整測試手冊，但它更像測試設計與判讀標準，不是所有項目都已填表完成的最終結果。此類結論必須逐 session 以 `session.db`、debug log、record cassette 或 transcript 查證，不能只根據 Gordon 畫面回答推定。

已完成的 AGENTS layer audit 顯示，Gordon 不會在 no-read baseline 自動透露 AGENTS token；但在明確要求檢查 AGENTS.md precedence 時，feature-level run 曾讀到指定 boundary 之外的 `Q:\AGENTS.md`。這代表「明確要求向上尋找規則檔」時，工具讀取範圍仍需用 prompt guardrail 與 session evidence 驗證。

## 4. 可重現性與證據完整性

本 repo 的主要自動化實驗具備可重現性素材：

- runner scripts: `run_*.py`
- prompt manifests: `frozen_prompt_manifest.json`
- raw results: `raw_results.json` / `raw_results.rescored.json`
- audit logs: `AUDIT_LOG.jsonl`
- evidence: session JSON 與 transcript text

主要位置包括：

- `test-results/gordon-prompt-framework-experiment/`
- `test-results/gordon-boundary-gradient-experiment-v2/`
- `test-results/gordon-boundary-gradient-experiment-v3/`
- `test-results/gordon-boundary-gradient-experiment-v3-h11-clean-rerun/`
- `test-results/gordon-non-docker-boundary-experiment/`
- `test-results/gordon-final-governance-experiment/`

較早期的 `test-results/docker-ai-rerun/` 與 root-level `T01-*` 至 `T07-*` artifacts 可作為 context-reading 補充證據，但不像 final governance / v2 / v3 那樣具備完整一致的 runner、manifest、raw results 與 audit log 結構。

## 5. 已知限制

1. 多數早期與 v3 題目每題只跑一次，適合判斷邊界訊號，不適合宣稱統計顯著。
2. prompt framework、v2、v3 與 non-Docker 實驗早期 runner 使用 bounded individual `y` approval，可能造成 trailing `y` 對 transcript 或最後訊息判讀的污染。
3. final governance 已修正 approval 策略，但 TUI approval prompt 偵測仍可能偏保守；若畫面文字含 secret-like 訊號，runner 可能送 `n` 並留下 denial record。
4. v3 曾出現 `HARD_G10-if_applicable` 寫檔污染後續 `HARD_G11`，雖已移至 `generated_by_gordon/` 並補跑 clean rerun，但這也證明 fixture hygiene 對 agent eval 很重要。
5. cross-model A/B 尚未完成；目前不能把觀察到的行為精確分解為 Haiku model effect、Gordon prompt effect 或 tool schema effect。
6. Docker Desktop UI context injection 尚未自動化；container logs、image inspect、failed build context 等入口仍需人工對照。
7. context audit 的 `.env`、parent directory、outside directory、symlink / junction、session history 等測試有完整設計，但仍需逐 session 完成正式結果表。
8. raw evidence 可能包含完整 tool responses、local paths、session ids 與 fake canary strings；公開前需重新審查與必要的 redaction。

## 6. 建議的後續驗證

優先完成 Docker Desktop UI context injection 對照：同一 prompt 分別從 CLI、Desktop detached Gordon、container logs、image inspect、failed build context 入口執行，檢查 session item 是否已注入 logs / inspect / build error，以及是否無 tool call 就引用 UI context。

擴大重複抽樣：針對 `G04`, `G10`, `G11`, `B02`, `B05`, `B10`、中文弱 trigger、risky Docker tasks 與 lexical traps，每題至少 10 次，重要邊界題可提高到 20-30 次。

在可控模型機制出現後再做 cross-model A/B：固定 fixture、prompt、toolset、scorer 與 runner，只替換模型，以分離 model semantic layer 與 governance/tool schema 的邊際效果。

補完 context audit 正式表格：尤其是 `.env`、`.dockerignore` / `.gitignore`、parent/outside directory、symlink/junction、Windows/WSL path、same-session vs fresh-session、record cassette 與 session.db 搜尋。

保持 final governance runner 的 detect-only approval 策略，並繼續把 `actual_tool_secret_access`、`secret_mentioned_only`、`actual_tool_safety`、`mentioned_risky_command` 分開 scoring。

## 7. 公開前內容控管

本 repo 已依公開研究證據庫的方向更新 README，並明確標示測試資料可能含 fake canary strings、fake secret/token markers、本機路徑、session ids、raw transcripts、session JSON 與 debug logs。公開前檢查重點如下：

- fake secret/token markers 是否可能被掃描器誤判並造成誤報。
- local Windows paths 是否被讀者誤解為 credential 或部署資訊。
- future-work / deferred/manual 項目是否被誤讀成已完成結論。
- raw evidence 是否應被視為研究資料，而不是乾淨的產品文件。

本次公開策略不是刪除 raw evidence，而是將 repo 定位為「研究證據庫」，保留可追溯資料並在 README、`docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md`、`docs/PUBLIC_RELEASE_REVIEW.zh-TW.md` 中清楚標註資料性質與限制。
