# BMAD Todo List API 文檔

基於 BMAD 方法論設計的 RESTful API 文檔。

## Big Model 設計決策

- 採用 RESTful 架構風格
- 統一的 JSON 回應格式
- 標準的 HTTP 狀態碼
- 清晰的錯誤處理機制

## API 端點

### 基礎 URL
```
http://localhost:5000/api
```

### 1. 取得所有待辦事項

**GET** `/todos`

**回應範例：**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "title": "完成 BMAD 專案規劃",
            "completed": false,
            "created_at": "2025-01-19T10:30:00",
            "updated_at": "2025-01-19T10:30:00"
        }
    ],
    "message": "成功取得待辦清單"
}
```

### 2. 新增待辦事項

**POST** `/todos`

**請求範例：**
```json
{
    "title": "新的待辦事項"
}
```

**回應範例：**
```json
{
    "success": true,
    "data": {
        "id": 2,
        "title": "新的待辦事項",
        "completed": false,
        "created_at": "2025-01-19T11:00:00",
        "updated_at": "2025-01-19T11:00:00"
    },
    "message": "成功新增待辦事項"
}
```

### 3. 更新待辦事項

**PUT** `/todos/{id}`

**請求範例：**
```json
{
    "title": "更新後的標題",
    "completed": true
}
```

**回應範例：**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "更新後的標題",
        "completed": true,
        "created_at": "2025-01-19T10:30:00",
        "updated_at": "2025-01-19T11:15:00"
    },
    "message": "成功更新待辦事項"
}
```

### 4. 刪除待辦事項

**DELETE** `/todos/{id}`

**回應範例：**
```json
{
    "success": true,
    "message": "成功刪除待辦事項"
}
```

### 5. 取得單一待辦事項

**GET** `/todos/{id}`

**回應範例：**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "完成 BMAD 專案規劃",
        "completed": false,
        "created_at": "2025-01-19T10:30:00",
        "updated_at": "2025-01-19T10:30:00"
    },
    "message": "成功取得待辦事項"
}
```

## 錯誤處理

### 統一錯誤格式
```json
{
    "success": false,
    "error": "具體錯誤訊息",
    "message": "使用者友善的錯誤描述"
}
```

### 常見狀態碼

- `200 OK`: 請求成功
- `201 Created`: 資源建立成功
- `400 Bad Request`: 請求參數錯誤
- `404 Not Found`: 資源不存在
- `500 Internal Server Error`: 伺服器內部錯誤

## BMAD 架構體現

### Big Model（戰略規劃）
- API 設計遵循 RESTful 原則
- 統一的資料格式和錯誤處理
- 可擴展的架構設計

### Agent（任務執行）
- 模組化的路由處理
- 自動化的資料驗證
- 完整的錯誤捕捉機制

### Design（介面設計）
- 直觀的端點命名
- 清晰的回應結構
- 使用者友善的錯誤訊息

## 使用範例

### JavaScript Fetch API
```javascript
// 取得所有待辦事項
const response = await fetch('/api/todos');
const data = await response.json();

// 新增待辦事項
const newTodo = await fetch('/api/todos', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: '新的待辦事項'
    })
});

// 更新待辦事項
const updatedTodo = await fetch(`/api/todos/${id}`, {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        completed: true
    })
});

// 刪除待辦事項
await fetch(`/api/todos/${id}`, {
    method: 'DELETE'
});
```

### cURL 範例
```bash
# 取得所有待辦事項
curl -X GET http://localhost:5000/api/todos

# 新增待辦事項
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "新的待辦事項"}'

# 更新待辦事項
curl -X PUT http://localhost:5000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# 刪除待辦事項
curl -X DELETE http://localhost:5000/api/todos/1
```