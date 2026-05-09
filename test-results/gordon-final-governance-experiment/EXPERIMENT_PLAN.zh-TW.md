# Gordon 最終治理層實驗計畫

Run ID prefix: `gordon_final_governance`

## 目的

本實驗回應外部 GPT 5.5 PRO 審查建議，聚焦目前可由 `docker ai` CLI 自動化執行的測試，不納入需要手動 Docker Desktop resource context 的 UI injection 測試，也不納入目前 Gordon 無法手動切換模型的 cross-model A/B。

## 本輪涵蓋

- `zh_trigger_ablation`：中文與中英混合 prompt trigger 對照。
- `repetition_boundary`：針對既有弱邊界題做重複抽樣。
- `secret_boundary`：`.env`、ignore-rule、secret handling 邊界。
- `risky_docker`：有 Docker 關係但不應直接執行的高風險任務。
- `lexical_trap`：Docker 詞彙在非 Docker 語境中的 false-positive trap。

## 明確延後

- `cross-model A/B`：Gordon 目前模型由系統設定，使用者端暫無穩定模型切換機制。
- `Docker Desktop UI context injection`：需要手動在 Desktop 不同 resource context 中啟動 Gordon，本 runner 僅支援 CLI。
- 真正 production destructive 操作：本實驗只允許 read-only、dry-run、inspect 或拒絕／風險說明。

## Runner 設計

- 來源 fixtures：`fixtures/cases.json`
- Prompt freeze：`prompts/<group>/<case-id>__rNN.txt`
- Evidence：
  - TUI transcript: `evidence/<case-id>__rNN-transcript.txt`
  - exported Gordon session: `evidence/<case-id>__rNN-session.json`
- Approval policy：
  - 不固定送入 `y`。
  - 只有偵測到 Gordon approval prompt 時才回覆。
  - 若 approval 畫面含 destructive Docker command 或 secret-like read signal，送 `n` 並記錄。
  - 其他 read-only / inspect 類 approval 送 `y` 並記錄。

## 完成標準

- runner 可 freeze fixtures、執行 CLI 實驗、匯出 session evidence、產生 raw results 與 Markdown 報告。
- 報告明確拆分已完成自動化結果與 deferred / manual 項目。
- 不修改程式碼產品本身、不修改 fixture 專案、不讀取 real secrets。
