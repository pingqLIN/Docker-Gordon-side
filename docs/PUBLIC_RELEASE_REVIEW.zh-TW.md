# GitHub 公開發布檢查報告

日期：2026-05-11
範圍：準備公開推送的已追蹤儲存庫內容、本次新增 / 修改文件，以及 curated evidence package。

## 結論

本次可推送公開，但需附帶資料性質說明：儲存庫中包含大量 Docker Gordon / Docker AI 測試逐字稿、工作階段證據、本機路徑與假金絲雀 / 假機密字串。README 已加入警示，總報告也明確標註限制。

本次採用 curated evidence 策略：公開可驗證的報告、prompt、fixtures、raw / rescored results、session evidence 與 transcript evidence；排除 `__pycache__/` 與 `run-smoke-*.out.log` / `run-smoke-*.err.log` transient logs。

## 檢查項目

| 項目 | 狀態 | 說明 |
|---|---|---|
| README 入口 | PASS | 已改為研究儲存庫說明，新增英文 README 與繁中 companion[對應版本] |
| 橫幅圖 | PASS | 新增 `docs/assets/gordon-research-banner.svg` |
| 授權 | PASS | 新增 MIT `LICENSE` |
| AI 輔助開發揭露 | PASS | README 與 README.zh-TW 均加入 |
| 新增 evidence 路徑 | PASS | README / 總報告引用的 session/context 消融與 Desktop UI context injection 資料夾已納入 curated evidence |
| 機密衛生 | WARNING | 掃描會命中假金絲雀、提示詞、逐字稿中的機密 / 權杖 / 金鑰字樣；這些是實驗資料，但公開前仍需保留警示 |
| 規劃詞彙 | WARNING | `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md` 含後續研究方向；因本儲存庫目標是公開研究脈絡，本次保留 |
| 本機路徑暴露 | WARNING | 多份既有報告與證據含 `Q:\Projects\...`、`C:\Users\miles\...` 等本機路徑；屬可重現性證據，但也是環境資訊 |
| 原始證據體積 | WARNING | `test-results/` 包含大量工作階段 / 逐字稿，公開後儲存庫可讀性與體積成本較高 |
| Session/context 消融 | WARNING | `gordon-session-context-ablation-experiment` 包含 `OBSERVE=6`, `BLOCKED=3` 的 smoke matrix；不可升格為正式 10x 結論 |
| Desktop UI context injection | WARNING | `gordon-desktop-ui-context-injection-experiment` 目前是 manual / semi-manual 測試計畫與模板，不是已完成自動化結果 |

## 命中內容判讀

| 類型 | 判讀 |
|---|---|
| `secret`, `token`, `key`, `.env` | 多為假金絲雀、測試限制、提示詞文字或模型回覆；README 已標示不應提交真實機密 |
| `roadmap`, `timeline`, `開發計畫`, `開發時程` | 未發現要保密的產品開發時程；既有文件含後續工作 / 後續測試方向，視為研究報告內容 |
| 本機 Windows 路徑 | 有，且大量存在於既有證據；公開風險是暴露作者本機資料夾命名，不是憑證 |
| `BLOCKED` / `OBSERVE` | session/context 消融仍是方向性 evidence；`BLOCKED` rows 表示 prompt/session evidence gate 不完整，不是模型行為失敗 |
| Desktop UI template | 只代表人工測試入口與判讀規則已建立；尚未提供 Docker Desktop UI context injection 的實測結論 |

## 公開前規則處置

依全域 GitHub 公開前檢查規則：

- 已掃描規劃相關詞：`roadmap`, `development priorities`, `timeline`, `開發計畫`, `開發時程`。
- 已掃描機密相關詞：`secret`, `token`, `api_key`, `password`, `credential`, private key pattern。
- 未刪除既有已追蹤證據，因使用者要求整理完整專案實驗報告並公開推送；這些證據是研究儲存庫的主要內容。
- 本次新增 evidence 採 curated evidence：納入 session/context 消融與 Desktop UI context injection 測試資料，排除 transient run-smoke logs 與 Python cache。
- 已在 README 與總報告中揭露假金絲雀、本機路徑、原始證據與統計限制。

## 外部稽核標準化報告

### 稽核模式

same-provider-subagent

### Scope

本次 documentation/publication change：`README.md`, `README.zh-TW.md`, `.gitignore`, `LICENSE`, `docs/assets/gordon-research-banner.svg`, `docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md`, `docs/gordon-research-synthesis.zh-TW.md`, `docs/PUBLIC_RELEASE_REVIEW.zh-TW.md`，以及 curated evidence paths `test-results/gordon-session-context-ablation-experiment/`、`test-results/gordon-desktop-ui-context-injection-experiment/`。

### 參考輸入

- `local-skill`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\SKILL.md` - 用於稽核模式、來源標註與標準化報告格式。
- `local-skill`: `C:\Users\miles\.codex\skills\readme-quality\SKILL.md` - 用於 README 結構、雙語對應版本、AI 輔助開發揭露與發布檢查期望。
- `local-repo`: `Q:\Projects\Docker-Gordon-side\test-results\...` - 用於既有實驗報告與原始結果摘要，以建立專案總報告。

### Findings

1. Warning：原始證據包含本機路徑與假類機密字串。
   位置或範圍：`test-results/`, `GORDON_CONTEXT_AUDIT_REPORT.md`
   風險：公開讀者可能把假金絲雀字串誤讀為外洩機密，或把本機路徑視為敏感中繼資料。
   建議行動：保留 README 警示，不宣稱儲存庫已完全移除所有環境中繼資料。

2. Warning：後續工作文件已被追蹤。
   位置或範圍：`docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md`
   風險：公開研究優先順序與未來實驗方向。
   建議行動：因使用者要求產出公開研究報告，本次可接受；若不是公開研究脈絡，應改放本機且忽略追蹤的筆記。

3. Suggestion：README 沒有執行期快速開始，因為本儲存庫是研究證據，不是可執行應用程式。
   位置或範圍：`README.md`
   風險：讀者可能期待標準安裝指令。
   建議行動：保留「How to Read」與「Reproduce」章節，不虛構安裝流程。

4. Warning：session/context 消融 evidence 尚未形成正式穩定性結論。
   位置或範圍：`test-results/gordon-session-context-ablation-experiment/`
   風險：讀者可能把 `OBSERVE` rows 或 3x smoke matrix 誤讀為統計結論。
   建議行動：保留 `BLOCKED` / `OBSERVE` 標示，並在總報告中維持「正式 10x 暫緩」限制。

5. Warning：Desktop UI context injection 目前是人工 / 半人工模板。
   位置或範圍：`test-results/gordon-desktop-ui-context-injection-experiment/`
   風險：讀者可能把測試計畫誤讀為已完成的 Desktop UI evidence。
   建議行動：維持 manual / semi-manual 標示，不以 CLI 結果替代 Desktop UI 結果。

### Assumptions

- 使用者意圖是公開研究證據與 curated evidence，不只公開新的摘要文件。
- 假金絲雀 / 假機密標記是刻意設計的測試資料。
- 遠端 `origin` 是預定公開的 GitHub 儲存庫。

### Disposition

accept

### Post-push Verification

發布 commit：`d50c177 docs: publish curated Gordon evidence`

推送狀態：已推送至 `origin/main`，本機 `HEAD` 與 `origin/main` 相同。

推送前後已確認：

- README / README.zh-TW 相對連結存在。
- `origin/main..HEAD` 未納入 `__pycache__`、`run-smoke-*.out.log` / `run-smoke-*.err.log`、`.env`、private key 或 credential 類路徑。
- 高信度 private key / token pattern 未命中。
- `OBSERVE` / `BLOCKED` 與 Desktop UI template 限制已保留，不升格為完成結論。

### Next Action

下一輪優先補 Docker Desktop UI context injection 人工實測表；其次修 same-session smoke 的 prompt/session evidence gate，再評估是否重跑正式 10x。
