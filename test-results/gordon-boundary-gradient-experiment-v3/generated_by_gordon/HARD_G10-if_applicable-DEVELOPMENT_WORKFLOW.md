# Development Workflow Guide

這份文件說明如何啟動、測試、除錯與交接這個專案。

## 專案架構

這是一個全棧應用（Full-Stack），包含三個服務：

| 服務 | 技術 | 埠號 | 用途 |
|------|------|------|------|
| **api** | Node.js / Express | 18181 (host) → 8080 (container) | 後端 API 伺服器 |
| **web** | Node.js / Vite | 18182 (host) → 5173 (container) | 前端開發伺服器 |
| **db** | PostgreSQL 17 | 5432 (internal) | 資料庫 |

---

## 1️⃣ 快速啟動

### 前置要求
- Docker Desktop 已安裝並運行
- 工作目錄已複製到本機

### 啟動所有服務

```bash
docker compose up
```

**等待訊息出現：**
- `api` 服務：顯示 `Server running on port 8080`
- `web` 服務：顯示 `VITE v... ready in ...`
- `db` 服務：健康檢查通過

### 存取應用

- **API**: http://localhost:18181
- **Web**: http://localhost:18182
- **API 健康檢查**: http://localhost:18181/health

### 停止服務

```bash
docker compose down
```

若要刪除所有資料（包含資料庫）：

```bash
docker compose down -v
```

---

## 2️⃣ 常見開發工作流

### 修改後端程式碼（API）

API 在容器內運行。修改程式碼後需重新建置容器：

```bash
# 1. 停止目前的服務
docker compose down

# 2. 重新建置 API 映像
docker compose build api

# 3. 重新啟動所有服務
docker compose up
```

或一行指令完成：

```bash
docker compose up --build
```

### 修改前端程式碼（Web）

Web 使用 Vite 開發伺服器，支援熱重載（Hot Reload）。修改 `web/` 資料夾內的檔案會**自動刷新瀏覽器**。

**無需重啟容器**——只要服務仍在執行，保存檔案即可看到變化。

### 修改資料庫（DB）

資料庫初始化指令檔位於 `db/migrations/` 資料夾。

**新增或修改遷移檔時：**

```bash
# 清除容器與資料庫
docker compose down -v

# 重新啟動（會執行新的遷移指令）
docker compose up
```

---

## 3️⃣ 測試

### 測試 API 連線

```bash
# 檢查 API 是否健康
curl http://localhost:18181/health

# 範例回應：
# {"status":"ok"} 或 HTTP 200
```

### 測試資料庫連線

```bash
# 進入 API 容器
docker compose exec api sh

# 在容器內測試（如果 API 程式碼有資料庫查詢邏輯）
node -e "console.log('Database connected')"
```

### 檢查服務狀態

```bash
docker compose ps
```

顯示所有服務及其狀態（running / exited）。

### 檢查服務組態

```bash
docker compose config
```

顯示完整的 Docker Compose 組態（包含環境變數）。

---

## 4️⃣ 除錯

### 檢視服務日誌

```bash
# 檢視所有服務的日誌
docker compose logs

# 只檢視特定服務的日誌（例如 API）
docker compose logs api

# 持續監看日誌（新日誌即時出現）
docker compose logs -f api

# 檢視最後 50 行
docker compose logs api --tail=50
```

### 進入容器內部偵錯

```bash
# 進入 API 容器
docker compose exec api sh

# 進入 Web 容器
docker compose exec web sh

# 進入資料庫容器
docker compose exec db psql -U app -d app
```

在容器內可執行指令進行詳細偵錯（例如檢查檔案、執行測試等）。

### 常見問題排查

| 症狀 | 原因 | 解決方案 |
|------|------|--------|
| `docker compose up` 失敗 | Docker daemon 未啟動 | 開啟 Docker Desktop |
| API 連線失敗 | 容器未完全啟動 | 等待 30 秒，檢視 `docker compose logs api` |
| 前端無法連接 API | API 服務未健康 | 執行 `docker compose logs db` 檢查資料庫狀態 |
| 資料庫出錯 | 遷移失敗或磁碟空間不足 | 執行 `docker compose down -v` 重置 |
| 埠號被佔用 | 另一個服務已使用埠號 18181 或 18182 | 執行 `docker compose down`，或修改 `compose.yaml` 中的埠號 |

---

## 5️⃣ 程式碼修改與建置

### API 建置流程

1. **修改** `api/` 資料夾內的檔案
2. **重新建置** API 映像：
   ```bash
   docker compose build api
   ```
3. **重新啟動** API 服務：
   ```bash
   docker compose up api
   ```

### Web 建置流程

1. **修改** `web/` 資料夾內的檔案
2. **瀏覽器自動刷新**（因為 Vite 熱重載已啟用）
3. 若未自動刷新，手動重新整理頁面

### 安裝依賴

```bash
# 為 API 安裝新套件
docker compose exec api npm install <package-name>

# 為 Web 安裝新套件
docker compose exec web npm install <package-name>
```

---

## 6️⃣ 交接清單

新同事接手時，確保以下事項：

- [ ] Docker Desktop 已安裝並運行
- [ ] 專案代碼已複製到本機
- [ ] `.env.example` 已複製為 `.env`（若需要）
- [ ] 執行 `docker compose up` 測試
- [ ] 存取 http://localhost:18181 和 http://localhost:18182 驗證服務
- [ ] 檢視 `DEVELOPMENT_WORKFLOW.md` 瞭解流程
- [ ] 執行 `docker compose down` 練習停止服務

### 交接檢查表

```bash
# 1. 確認 Docker 已就緒
docker --version
docker compose --version

# 2. 啟動服務
docker compose up

# 3. 測試連接（在新終端窗口中）
curl http://localhost:18181/health
curl http://localhost:18182

# 4. 檢視日誌
docker compose logs

# 5. 進入容器
docker compose exec api sh

# 6. 停止服務
docker compose down
```

完成上述所有步驟，表示專案已成功在本機環境啟動。

---

## 7️⃣ 環境變數

所有環境變數已在 `compose.yaml` 中定義：

| 變數 | 值 | 說明 |
|------|-----|------|
| `NODE_ENV` | `development` | Node 環境 |
| `DATABASE_URL` | `postgres://app:example@db:5432/app` | 資料庫連線字串 |

如需修改，編輯 `compose.yaml` 中的 `environment` 區段。

---

## 📚 常用指令速查表

| 指令 | 用途 |
|------|------|
| `docker compose up` | 啟動所有服務 |
| `docker compose up --build` | 重新建置後啟動 |
| `docker compose down` | 停止所有服務 |
| `docker compose down -v` | 停止並刪除所有資料 |
| `docker compose ps` | 列出所有服務狀態 |
| `docker compose logs` | 檢視所有日誌 |
| `docker compose logs -f <service>` | 持續監看特定服務日誌 |
| `docker compose exec <service> <command>` | 在容器內執行指令 |
| `docker compose build <service>` | 重新建置特定服務 |
| `docker compose config` | 驗證並顯示完整組態 |

---

## ❓ 更多協助

有問題？遵循以下步驟：

1. **檢視日誌**：`docker compose logs -f`
2. **進入容器**：`docker compose exec api sh`
3. **驗證組態**：`docker compose config`
4. **重置環境**：`docker compose down -v && docker compose up`

若問題未解決，聯絡專案負責人。
