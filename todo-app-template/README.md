# BMAD Todo List 應用模板

基於 BMAD 方法論開發的 Todo List 應用模板。

## 快速開始

1. 複製此模板到您的開發目錄
2. 安裝依賴：`pip install -r requirements.txt`
3. 運行應用：`python app.py`
4. 在瀏覽器中開啟：`http://localhost:5000`

## 專案結構

請參考 [BMAD 專案規劃文檔](../BMAD-TodoList-Project-Plan.md) 了解完整的架構說明。

## BMAD 三要素實現

- **Big Model**：需求分析與架構決策已在專案規劃中完成
- **Agent**：程式碼生成按照模塊化設計，便於 AI 協作開發
- **Design**：UI/UX 設計遵循簡潔直觀的原則

## 下一步

1. 實現後端 API（`api/routes.py`）
2. 建立資料模型（`models/todo.py`）
3. 開發前端介面（`templates/index.html`, `static/js/app.js`）
4. 撰寫測試（`tests/`）