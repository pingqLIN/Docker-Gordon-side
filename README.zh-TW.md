[![Docker Gordon Side Experiments banner](docs/assets/gordon-research-banner.svg)](docs/assets/gordon-research-banner.svg)

# Docker Gordon Side Experiments

> **[English](README.md)**

Docker Gordon / Docker AI 邊界、prompt wrapper、上下文讀取與治理層行為的研究證據庫。

![Status](https://img.shields.io/badge/status-research%20archive-blue) ![Platform](https://img.shields.io/badge/platform-Docker%20AI%20%2F%20Windows-informational) ![License](https://img.shields.io/badge/license-MIT-green)

[總報告](docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md) · [公開檢查](docs/PUBLIC_RELEASE_REVIEW.zh-TW.md) · [Context Audit](GORDON_CONTEXT_AUDIT_REPORT.md) · [English](README.md)

---

## 背景

這個 repo 保存一系列針對 Docker Desktop Gordon / `docker ai` 的實驗：Gordon 何時會把任務映射到 Docker workflow、prompt wrapper 是否能改善弱 Docker 外觀任務、完全非 Docker 任務是否會被錯誤硬套，以及 secret / 高風險 Docker 任務是否能被治理層安全處理。

研究重點不是「讓一個 app 跑起來」，而是保存 prompts、runner、raw results、audit logs、session evidence 與人工整理報告。

> 注意：repo 內有 fake canary、fake secret/token/key marker。它們是測試資料，不是真實 credential。

---

## 重點結論

| 主題 | 結論 |
|---|---|
| 明確 Docker 任務 | Docker-rich fixture 下 baseline 與 treatment 都可穩定通過 |
| 弱 Docker 外觀 | Prompt wrapper 可把部分泛用工程任務拉回 Docker workflow |
| 強觸發語義 | `deployment readiness`, `CI parity`, `ports/logs/health`, `reproducible dev/test/run` 特別有效 |
| 非 Docker 邊界 | 完全無關任務即使套強 wrapper，仍未啟動工具或硬套 Docker |
| Secret / risky tasks | Final governance runner 將 secret 實際讀取與文字提到 secret 分開評分 |
| 仍待補完 | Docker Desktop UI context injection 與 cross-model A/B 仍是 deferred/manual |

---

## 如何閱讀

| 目的 | 入口 |
|---|---|
| 專案總覽 | `docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md` |
| 研究單元統整 | `docs/gordon-research-synthesis.zh-TW.md` |
| 公開發布檢查 | `docs/PUBLIC_RELEASE_REVIEW.zh-TW.md` |
| 上下文讀取手冊 | `GORDON_CONTEXT_AUDIT_REPORT.md` |
| 後續研究方向 | `docs/gordon-docker-next-tests-and-governance-assessment.zh-TW.md` |
| 外部審查摘錄 | `test-results/GPT55PRO.md` |

---

## 實驗資料

| 路徑 | 內容 |
|---|---|
| `test-results/gordon-prompt-framework-experiment/` | Prompt architecture baseline/treatment 實驗 |
| `test-results/gordon-boundary-gradient-experiment-v2/` | Anchor + gradient 邊界遞減實驗 |
| `test-results/gordon-boundary-gradient-experiment-v3/` | 弱邊界細切、trigger ablation、wrapper minimization |
| `test-results/gordon-boundary-gradient-experiment-v3-h11-clean-rerun/` | H11 clean rerun 修正污染 |
| `test-results/gordon-non-docker-boundary-experiment/` | 完全非 Docker 任務與 overforce wrapper |
| `test-results/gordon-final-governance-experiment/` | 中文 trigger、secret boundary、risky Docker、lexical trap |
| `test-results/docker-ai-rerun/` | Docker AI context / rerun evidence |
| `test-results/gordon-agent-layer-audit/` | AGENTS precedence 與 agent layer 行為觀察 |

---

## 重現與驗證

多數 runner 是 Python 腳本，並依賴本機 Docker Desktop / `docker ai`、Windows path、以及 Docker Agent session database。重跑前請先確認沒有真實 secret 檔案存在於 fixture。

```powershell
# Example: inspect available experiment runners
Get-ChildItem -Recurse -Filter run_*.py test-results

# Example: read the final governance result table
Get-Content test-results\gordon-final-governance-experiment\RESULTS.md
```

> 安全建議：不要把真 `.env`、private key、credential 或 production token 放入測試 fixture。

---

## Key Files

| File | Description |
|---|---|
| `docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md` | 完整專案實驗總報告 |
| `docs/gordon-research-synthesis.zh-TW.md` | 實驗目標、證據與限制的單元統整報告 |
| `docs/PUBLIC_RELEASE_REVIEW.zh-TW.md` | GitHub 公開前檢查與 external audit normalized report |
| `GORDON_CONTEXT_AUDIT_REPORT.md` | Gordon 上下文讀取範圍測試報告與執行手冊 |
| `README.md` | English project entrypoint |
| `README.zh-TW.md` | 繁體中文 project entrypoint |
| `LICENSE` | MIT License |

---

## AI-Assisted Development

This project was developed with AI assistance.

| Model | Role |
|---|---|
| OpenAI Codex | documentation synthesis, README rewrite, release review, repository inspection |
| GPT 5.5 PRO | external research review artifact preserved in `test-results/GPT55PRO.md` |

### Human Oversight

- 實驗資料以既有 raw results、audit logs、reports 與 transcripts 為來源。
- README 與總報告保留 limitations，不將小樣本結果誇大成統計保證。
- 公開發布前掃描 fake secret / planning / local path 風險。
- Git 變更僅限文件、banner 與 license。

> Disclaimer: While the author has made every effort to review and validate the AI-generated code and documentation, no guarantee can be made regarding correctness, security, or fitness for any particular purpose. Use at your own risk.

---

## License

[MIT License](LICENSE)
