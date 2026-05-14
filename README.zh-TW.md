[![Docker Gordon Side Experiments banner](RADI0380.jpeg)](RADI0380.jpeg)

# Docker Gordon Side Experiments

> **[English](README.md)**

Docker Gordon / Docker AI 邊界、提示詞包裝、上下文讀取與治理層行為的研究證據庫。

![Status](https://img.shields.io/badge/status-research%20archive-blue) ![Platform](https://img.shields.io/badge/platform-Docker%20AI%20%2F%20Windows-informational) ![License](https://img.shields.io/badge/license-MIT-green)

[正式網站](https://docker-gordon-side.colorgeek.co/) · [總報告](docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md) · [公開檢查](docs/PUBLIC_RELEASE_REVIEW.zh-TW.md) · [上下文稽核](GORDON_CONTEXT_AUDIT_REPORT.md) · [English](README.md)

---

## 背景

這個儲存庫保存一系列針對 Docker Desktop Gordon / `docker ai` 的實驗：Gordon 何時會把任務映射到 Docker 工作流程、提示詞包裝是否能改善弱 Docker 外觀任務、完全非 Docker 任務是否會被錯誤硬套，以及機密資料 / 高風險 Docker 任務是否能被治理層安全處理。

研究重點不是「讓一個應用程式跑起來」，而是保存提示詞、執行器、原始結果、稽核日誌、工作階段證據與人工整理報告。

> 注意：儲存庫內有假金絲雀字串、假機密 / 權杖 / 金鑰標記。它們是測試資料，不是真實憑證。

---

## 重點結論

| 主題 | 結論 |
|---|---|
| 明確 Docker 任務 | Docker-rich 測試夾具下，基準組與處理組都可穩定通過 |
| 弱 Docker 外觀 | 提示詞包裝可把部分泛用工程任務拉回 Docker 工作流程 |
| 強觸發語義 | `deployment readiness`[部署準備程度]、`CI parity`[持續整合一致性]、`ports/logs/health`[連接埠 / 日誌 / 健康檢查]、`reproducible dev/test/run`[可重現開發 / 測試 / 執行] 特別有效 |
| 非 Docker 邊界 | 完全無關任務即使套用強提示詞包裝，仍未啟動工具或硬套 Docker |
| 機密與高風險任務 | 最終治理層執行器將「實際讀取機密」與「文字提到機密」分開評分 |
| 仍待補完 | Docker Desktop 使用者介面上下文注入，以及跨模型 A/B 測試仍需人工補完 |

---

## 如何閱讀

| 目的 | 入口 |
|---|---|
| 互動式邊界地圖 | `index.html`（可直接本機開啟，或用 `npx serve .` 服務整個資料夾） |
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
| `test-results/gordon-prompt-framework-experiment/` | 提示詞架構基準組 / 處理組實驗 |
| `test-results/gordon-boundary-gradient-experiment-v2/` | 錨點組 + 梯度組邊界遞減實驗 |
| `test-results/gordon-boundary-gradient-experiment-v3/` | 弱邊界細切、觸發詞消融、提示詞包裝最小化 |
| `test-results/gordon-boundary-gradient-experiment-v3-h11-clean-rerun/` | H11 乾淨重跑，修正污染 |
| `test-results/gordon-non-docker-boundary-experiment/` | 完全非 Docker 任務與過度強制提示詞包裝 |
| `test-results/gordon-final-governance-experiment/` | 中文觸發、機密邊界、高風險 Docker、詞彙陷阱 |
| `test-results/gordon-session-context-ablation-experiment/` | fresh-session、same-session 與 CLI context/tool availability 消融 |
| `test-results/gordon-desktop-ui-context-injection-experiment/` | Docker Desktop UI context injection 人工證據模板 |
| `test-results/docker-ai-rerun/` | Docker AI 上下文 / 重跑證據 |
| `test-results/gordon-agent-layer-audit/` | AGENTS 優先序與代理層行為觀察 |

---

## 重現與驗證

多數執行器是 Python 腳本，並依賴本機 Docker Desktop / `docker ai`、Windows 路徑，以及 Docker Agent 工作階段資料庫。重跑前請先確認測試夾具中沒有真實機密檔案。

```powershell
# 範例：檢查可用的實驗執行器
Get-ChildItem -Recurse -Filter run_*.py test-results

# 範例：讀取最終治理層結果表
Get-Content test-results\gordon-final-governance-experiment\RESULTS.md
```

> 安全建議：不要把真 `.env`、私鑰、憑證或正式環境權杖放入測試夾具。

---

## 關鍵檔案

| 檔案 | 說明 |
|---|---|
| `index.html` | 互動式邊界地圖，整合防護線、實驗紀錄、提示詞範本、觸發語義與結論 |
| `CNAME` | GitHub Pages 自訂網域：`docker-gordon-side.colorgeek.co` |
| `gordon-boundary-map.json` | 儀表板資料源，包含防護線、實驗與提示詞資料 |
| `gordon-boundary-map.js` | 由 JSON 產生的本機 `file://` fallback |
| `RADI0380.jpeg` | README 橫幅圖，直接引用原始檔案，不轉檔 |
| `docs/assets/blue-whale-cutout.png` | 互動式邊界地圖使用的描圖紙藍鯨剪紙 |
| `docs/PROJECT_EXPERIMENT_REPORT.zh-TW.md` | 完整專案實驗總報告 |
| `docs/gordon-research-synthesis.zh-TW.md` | 實驗目標、證據與限制的單元統整報告 |
| `docs/PUBLIC_RELEASE_REVIEW.zh-TW.md` | GitHub 公開前檢查與外部稽核標準化報告 |
| `GORDON_CONTEXT_AUDIT_REPORT.md` | Gordon 上下文讀取範圍測試報告與執行手冊 |
| `README.md` | 英文專案入口 |
| `README.zh-TW.md` | 繁體中文專案入口 |
| `LICENSE` | MIT 授權 |

---

## AI 輔助開發

本專案是在 AI 輔助下開發與整理。

| 模型 | 角色 |
|---|---|
| OpenAI Codex | 文件統整、README 改寫、發布審查、儲存庫檢查 |
| GPT 5.5 PRO | 外部研究審查產物，保存於 `test-results/GPT55PRO.md` |

### 人工監督

- 實驗資料以既有原始結果、稽核日誌、報告與逐字稿為來源。
- README 與總報告保留限制，不將小樣本結果誇大成統計保證。
- 公開發布前掃描假機密、規劃內容與本機路徑風險。
- 對外呈現的變更限於文件、互動式邊界地圖、由 JSON 產生的儀表板資料、橫幅素材與授權檔。
- README 橫幅直接引用原始 `RADI0380.jpeg`，屬於裝飾素材，後續可替換，不影響實驗證據與結論。

> 免責聲明：作者已盡力審查與驗證 AI 生成的程式碼與文件，但不保證其正確性、安全性或適用於任何特定目的。請自行承擔使用風險。

---

## 授權

[MIT License](LICENSE)
