# Prefect Job Variables 配置說明

## 配置概述

此專案使用 Prefect 的 Job Variables 來管理配置參數。Job Variables 會以環境變數的形式傳遞給 Worker 執行環境。

## 配置參數

在 `prefect.yaml` 中的 `work_pool.job_variables` 區段定義：

```yaml
job_variables: 
  REDIS_HOST: "localhost"
  REDIS_PORT: "6379"
  REDIS_DB: "0"
  DISK_PATH: "E:/"
  FILTER_RULE: ".zip"
  SOURCE_SERVER: "pc10714"
  TARGET_SERVER: "pc10714new"
  TARGET_FOLDER: "d:/new_folder"
```

## 參數說明

| 變數名稱 | 描述 | 預設值 | 範例 |
|---------|------|--------|------|
| `REDIS_HOST` | Redis 伺服器地址 | `localhost` | `192.168.1.100` |
| `REDIS_PORT` | Redis 連接埠 | `6379` | `6380` |
| `REDIS_DB` | Redis 資料庫編號 | `0` | `1` |
| `DISK_PATH` | 要掃描的磁碟路徑 | `E:/` | `C:/data/` |
| `FILTER_RULE` | 檔案篩選規則 | `.zip` | `.rar` 或 `.tar` |
| `SOURCE_SERVER` | 來源伺服器名稱 | `pc10714` | `server01` |
| `TARGET_SERVER` | 目標伺服器名稱 | `pc10714new` | `backup-server` |
| `TARGET_FOLDER` | 目標資料夾路徑 | `d:/new_folder` | `/backup/files` |

## 使用方法

### 1. 部署 Flow
```cmd
prefect deploy
```

### 2. 創建工作池（如果不存在）
```cmd
prefect work-pool create default_work --type process
```

### 3. 啟動 Worker
```cmd
prefect worker start --pool default_work
```

### 4. 執行 Flow
```cmd
prefect deployment run "my_flow/my_flow"
```

## 修改配置

### 方法1：修改 prefect.yaml 檔案
直接編輯 `prefect.yaml` 檔案中的 `job_variables` 區段，然後重新部署：

```cmd
prefect deploy
```

### 方法2：使用 Prefect UI
1. 啟動 Prefect 服務器：`prefect server start`
2. 在瀏覽器中訪問 `http://localhost:4200`
3. 進入 Work Pools → default_work
4. 修改 Job Variables

## 程式碼中的使用

程式碼中使用 `os.getenv()` 來取得環境變數：

```python
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', '6379'))
disk_path = os.getenv('DISK_PATH', 'E:/')
```

## 優勢

- **環境隔離**: 不同的 work pool 可以有不同的配置
- **動態配置**: 可以在執行時修改而不需要重新部署程式碼
- **安全性**: 敏感資訊可以通過環境變數傳遞
- **可追蹤性**: 所有配置變更都有記錄