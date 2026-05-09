# GitHub 公開發布檢查報告

日期：2026-05-10
範圍：準備公開 push 的 tracked repository content 與本次新增/修改文件。

## 結論

本次可推送公開，但需附帶資料性質說明：repo 中包含大量 Docker Gordon / Docker AI 測試 transcript、session evidence、本機路徑與 fake canary / fake secret 字串。README 已加入警示，總報告也明確標註限制。

## 檢查項目

| 項目 | 狀態 | 說明 |
|---|---|---|
| README 入口 | PASS | 已改為研究 repo 說明，新增英文 README 與繁中 companion |
| Banner | PASS | 新增 `docs/assets/gordon-research-banner.svg` |
| License | PASS | 新增 MIT `LICENSE` |
| AI-assisted disclosure | PASS | README 與 README.zh-TW 均加入 |
| Secret hygiene | WARNING | 掃描會命中 fake canary、prompt、transcript 中的 secret/token/key 字樣；這些是實驗資料，但公開前仍需保留警示 |
| Planning terms | WARNING | `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md` 含後續研究方向；因本 repo 目標是公開研究脈絡，本次保留 |
| Local path exposure | WARNING | 多份既有報告與 evidence 含 `Q:\Projects\...`、`C:\Users\miles\...` 等本機路徑；屬可重現性證據，但也是環境資訊 |
| Raw evidence volume | WARNING | `test-results/` 包含大量 session/transcript，公開後 repo 可讀性與體積成本較高 |

## 命中內容判讀

| 類型 | 判讀 |
|---|---|
| `secret`, `token`, `key`, `.env` | 多為假 canary、測試限制、prompt 文字或模型回覆；README 已標示「No real secrets should be committed」 |
| `roadmap`, `timeline`, `開發計畫`, `開發時程` | 未發現要保密的產品開發時程；既有文件含 future work / 後續測試方向，視為研究報告內容 |
| Local Windows paths | 有，且大量存在於既有 evidence；公開風險是暴露作者本機資料夾命名，不是 credential |

## 公開前規則處置

依全域 GitHub 公開前檢查規則：

- 已掃描 planning 相關詞：`roadmap`, `development priorities`, `timeline`, `開發計畫`, `開發時程`。
- 已掃描 secret 相關詞：`secret`, `token`, `api_key`, `password`, `credential`, private key pattern。
- 未刪除既有 tracked evidence，因使用者要求整理完整專案實驗報告並公開 push；這些 evidence 是研究 repo 的主要內容。
- 已在 README 與總報告中揭露 fake canary、local path、raw evidence 與統計限制。

## External Audit Normalized Report

### Audit Mode

same-provider-subagent

### Scope

本次 documentation/publication change：`README.md`, `README.zh-TW.md`, `LICENSE`, `docs/assets/gordon-research-banner.svg`, `docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md`, `docs/gordon-research-synthesis.zh-TW.md`, `docs/PUBLIC_RELEASE_REVIEW.zh-TW.md`。

### Reference Inputs

- `local-skill`: `C:\Users\miles\.codex\skills\external-audit-orchestrator\SKILL.md` - used audit mode, attribution, and normalized report contract.
- `local-skill`: `C:\Users\miles\.codex\skills\readme-quality\SKILL.md` - used README structure, bilingual companion, AI-assisted disclosure, and release checklist expectations.
- `local-repo`: `Q:\Projects\Docker-Gordon-side\test-results\...` - used existing experiment reports and raw result summaries to build the total project report.

### Findings

1. Warning: raw evidence includes local paths and fake secret-like strings.
   Location or scope: `test-results/`, `GORDON_CONTEXT_AUDIT_REPORT.md`
   Risk: public readers may misread fake canary strings as leaked secrets, or local paths as sensitive metadata.
   Recommended action: keep README warnings and do not claim the repo is scrubbed of all environment metadata.

2. Warning: future-work document is tracked.
   Location or scope: `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md`
   Risk: publishes research priorities and future experiment directions.
   Recommended action: acceptable only because the requested output is a public research report; otherwise move to a local-only ignored note.

3. Suggestion: README has no runtime quick-start because the repo is research evidence, not a runnable app.
   Location or scope: `README.md`
   Risk: users may expect a standard install command.
   Recommended action: keep "How to Read" and "Reproduce" sections instead of inventing a fake install flow.

### Assumptions

- The user intends to publish the research evidence and existing tracked experiment files, not only the new summary documents.
- Fake canary / fake secret markers are intentional test data.
- The remote `origin` is the intended public GitHub repository.

### Disposition

accept

### Next Action

Commit the documentation/publication updates and push to `origin/main` after final diff review and Git status check.
