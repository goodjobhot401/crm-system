# 👨‍💼 crm-system

 一個以 `FastAPI`、`MySQL` 建置的 CRM 系統。專案內建 `docker‑compose`，只需一行指令即可在任何支援 `Docker` 的機器上快速啟動。

## 🏗️ Built with


`FastAPI + SQLAlchemy`：使用非同步 Web Framework 與 ORM

`MySQL`：永久儲存使用者、優惠券、領取紀錄

`Docker`：使用容器化技術快速啟動所有依賴環境，自動建立資料表並寫入範例資料


## 📒 Docs Tree

```text
.
├── src
│   ├── database         --- DDL & DML 初始化
│   ├── infra            --- DB sesion 管理
│   ├── models           --- ORM DB schema
│   ├── routers          --- Fastapi 入口路由＋邏輯處理
│   ├── schemas          --- Req 結構
│   └── main.py          --- 伺服器主入口
├── .env.template        --- 環境變數樣板
├── .gitignore           --- Git 忽略設定
├── docker-compose.yml   --- 容器化設定
├── dockerfile           --- Docker 映像建置指令
├── LICENSE              --- 專案授權資訊
├── postman.json         --- Postman 測試集合
├── README.md            --- 專案說明文件
└── requirements.txt     --- Python 套件依賴清單

```

## 🚀 Getting Started

**Clone the repo**

```
git clone https://github.com/goodjobhot401/crm-system.git
cd crm-system
```


**Initialize**

```
docker compose up --build
```


**Schema**
---
`account`
| attributes    | datatype         | Nullable |
|---------------|------------------|----------|
| id            | Integer (PK)     | NO       | 
| name          | String(50)       | NO       |
| last_order_at | TIMESTAMP        | Yes      |
| created_at    | TIMESTAMP        | NO       |
| updated_at    | TIMESTAMP        | NO       |
<br>

`order`
| 欄位        | 型別                      | Nullable | 
|------------|---------------------------|----------|
| id         | Integer (PK)              | NO       |
| account_id | Integer (FK account.id)   | NO       |
| amount     | Integer                   | NO       | 
| created_at | TIMESTAMP                 | NO       |
| updated_at | TIMESTAMP                 | NO       | 
<br>

`message`
| 欄位        | 型別            | Nullable |
|------------|-----------------|----------|
| id         | Integer (PK)    | NO       | 
| title      | String(250)     | NO       | 
| template   | Text            | NO       | 
| created_at | TIMESTAMP       | No       |
| updated_at | TIMESTAMP       | NO       |
<br>

`message_log`
| 欄位        | 型別                      | Nullable |
|------------|---------------------------|----------|
| id         | Integer (PK)              | NO       | 
| account_id | Integer (FK account.id)   | NO       |
| message_id | Integer (FK message.id)   | NO       |
| content    | Text                      | NO       | 
| created_at | TIMESTAMP                 | No       |
| updated_at | TIMESTAMP                 | NO       |
<br>


## 𓇠 Seed Data & Postman
啟動容器後，系統將自動插入：
- **2** 筆 `account`
- **8** 筆 `order`
- **1** 筆 `message`

💡 可直接使用根目錄的 `postman.json` 匯入至 Postman，快速測試所有 API 功能

