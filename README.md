# 記帳小工具 (Expense Tracker)

一個簡單易用的記帳工具，使用 Python 和 Tkinter 開發的圖形化介面應用程式。

## 功能特點

- 📝 記錄收入和支出
- 📊 自動計算總收入、總支出和結餘
- 📈 支出分類統計圖表
- 💾 自動保存數據
- 🗑️ 支持刪除記錄
- 📱 響應式界面設計

## 系統需求

- Python 3.6 或更高版本
- macOS 系統（已測試）
- 以下 Python 套件：
  - tkinter
  - matplotlib
  - json

## 安裝步驟

1. 克隆專案：
```bash
git clone https://github.com/你的用戶名/expense-tracker.git
cd expense-tracker
```

2. 安裝依賴套件：
```bash
pip3 install matplotlib
```

## 使用方法

1. 執行程式：
```bash
python3 expense_tracker.py
```

2. 新增記錄：
   - 選擇日期
   - 選擇類型（收入/支出）
   - 選擇分類
   - 輸入金額
   - 輸入備註（可選）
   - 點擊「新增記錄」按鈕

3. 查看統計：
   - 總收入、總支出和結餘會自動計算
   - 支出分類統計圖表會自動更新

4. 刪除記錄：
   - 在記錄列表中選擇要刪除的記錄
   - 按下 Delete 鍵
   - 確認刪除

## 數據存儲

- 所有數據保存在 `expense_data.json` 文件中
- 數據格式為 JSON
- 支持 UTF-8 編碼，可以正確顯示中文

## 貢獻指南

歡迎提交 Pull Request 或開 Issue 來改進這個專案！

## 授權協議

MIT License

## 作者

鼠鼠

## 致謝

- Python Tkinter 團隊
- Matplotlib 團隊 