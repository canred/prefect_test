# Prefect Redis File Processing Flow

這是一個使用 Prefect 建立的檔案處理流程，主要功能是掃描磁碟上的 ZIP 檔案並將資訊儲存到 Redis 中。

## 環境變量
    $env:PREFECT_API_URL="http://127.0.0.1:8888/api"
## 專案結構

```
PrefectFlow/
├── flows/                    # Prefect 流程定義
│   ├── __init__.py
│   ├── my_flow.py.bak           # 原始流程檔案
│   └── my_flow.py # 重構後的流程檔案
├── tasks/                    # Prefect 任務模組
│   ├── __init__.py
│   ├── redis_tasks.py       # Redis 相關任務
│   └── file_tasks.py        # 檔案處理任務
├── utils/                    # 工具函數
│   ├── __init__.py
│   ├── config.py            # 配置檔案
│   └── helpers.py           # 輔助函數
├── tests/                    # 測試檔案
│   ├── __init__.py
│   └── test_flows.py        # 流程測試
├── scripts/                  # 執行腳本
│   ├── deploy.py            # 部署腳本
│   ├── run_flow.py          # 本地執行腳本
│   └── setup_variables.py   # 環境變數設定
├── prefect.yaml             # Prefect 專案配置
├── requirements.txt         # Python 依賴套件
├── .env.example            # 環境變數範例
└── README.md               # 專案說明
```

## 安裝與設定

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定環境變數

複製 `.env.example` 為 `.env` 並修改相關設定：

```bash
copy .env.example .env
```

### 3. 設定 Redis

確保 Redis 服務正在運行，預設連接設定：
- Host: localhost
- Port: 6379
- DB: 0

## 使用方法

### 本地執行

```bash
python scripts/run_flow.py
```

### 部署到 Prefect Cloud/Server

```bash
python scripts/deploy.py
```

或使用 Prefect CLI：

```bash
prefect deploy flows/my_flow.py:my_flow --name redis-file-processing
```

### 執行測試

```bash
python -m pytest tests/
```

## 功能說明

### 主要功能

1. **檔案掃描**: 遞迴掃描指定目錄中的 ZIP 檔案
2. **Redis 儲存**: 將檔案資訊儲存到 Redis 資料庫
3. **重複檢查**: 避免重複處理相同檔案
4. **日誌記錄**: 詳細的執行日誌

### 環境變數說明

- `REDIS_HOST`: Redis 伺服器位址
- `REDIS_PORT`: Redis 連接埠
- `REDIS_DB`: Redis 資料庫編號
- `DISK_PATH`: 要掃描的磁碟路徑
- `FILTER_RULE`: 檔案過濾規則（如 .zip）
- `SOURCE_SERVER`: 來源伺服器名稱
- `TARGET_SERVER`: 目標伺服器名稱
- `TARGET_FOLDER`: 目標資料夾路徑

## 開發指南

### 新增任務

1. 在 `tasks/` 目錄下建立新的模組
2. 使用 `@task` 裝飾器定義任務函數
3. 在流程中匯入並使用

### 修改流程

1. 編輯 `flows/my_flow.py`
2. 使用模組化的任務組合流程
3. 測試後重新部署

### 執行測試

在專案根目錄執行：

```bash
python -m unittest tests.test_flows
```

## 故障排除

### 常見問題

1. **Redis 連接失敗**: 確認 Redis 服務正在運行且網路連接正常
2. **檔案路徑錯誤**: 檢查 `DISK_PATH` 環境變數設定
3. **權限問題**: 確保程式有讀取指定目錄的權限

### 日誌查看

流程執行時會產生詳細的日誌，可透過 Prefect UI 或終端機查看。
