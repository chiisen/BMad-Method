"""
BMAD Todo API 測試
Agent: API 層測試實現
"""

import pytest
import json
import tempfile
import os
from app import create_app
from models.todo import TodoModel

class TestTodoAPI:
    """Todo API 測試類 - Agent 測試職責"""
    
    @pytest.fixture
    def client(self):
        """測試客戶端"""
        # 創建臨時資料庫
        db_fd, db_path = tempfile.mkstemp()
        
        app = create_app()
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            # 在每個測試中使用新的模型實例
            global todo_model
            from api.routes import api_bp
            # 更新 API 路由中的模型
            import api.routes
            api.routes.todo_model = TodoModel(db_path)
            yield client
        
        # 清理
        os.close(db_fd)
        os.unlink(db_path)
    
    def test_get_empty_todos(self, client):
        """測試取得空的待辦清單 - Agent API 測試"""
        response = client.get('/api/todos')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['data'] == []
    
    def test_create_todo(self, client):
        """測試新增待辦事項 API - Agent API 測試"""
        todo_data = {'title': '測試待辦事項'}
        
        response = client.post('/api/todos', 
                             json=todo_data,
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 201
        assert data['success'] is True
        assert data['data']['title'] == '測試待辦事項'
        assert data['data']['completed'] is False
    
    def test_create_todo_without_title(self, client):
        """測試沒有標題的新增請求 - Agent 邊界測試"""
        response = client.post('/api/todos', 
                             json={},
                             content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert data['success'] is False
        assert '標題不能為空' in data['message']
    
    def test_get_todos_after_creation(self, client):
        """測試新增後取得待辦清單 - Agent 整合測試"""
        # 新增一個待辦事項
        todo_data = {'title': '測試事項'}
        client.post('/api/todos', json=todo_data, content_type='application/json')
        
        # 取得清單
        response = client.get('/api/todos')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert len(data['data']) == 1
        assert data['data'][0]['title'] == '測試事項'
    
    def test_update_todo(self, client):
        """測試更新待辦事項 API - Agent API 測試"""
        # 先新增一個待辦事項
        todo_data = {'title': '原始標題'}
        create_response = client.post('/api/todos', json=todo_data, content_type='application/json')
        created_todo = json.loads(create_response.data)['data']
        
        # 更新待辦事項
        update_data = {'title': '更新後標題', 'completed': True}
        response = client.put(f'/api/todos/{created_todo["id"]}', 
                            json=update_data,
                            content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['data']['title'] == '更新後標題'
        assert data['data']['completed'] is True
    
    def test_delete_todo(self, client):
        """測試刪除待辦事項 API - Agent API 測試"""
        # 先新增一個待辦事項
        todo_data = {'title': '要刪除的事項'}
        create_response = client.post('/api/todos', json=todo_data, content_type='application/json')
        created_todo = json.loads(create_response.data)['data']
        
        # 刪除待辦事項
        response = client.delete(f'/api/todos/{created_todo["id"]}')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        
        # 確認已被刪除
        get_response = client.get(f'/api/todos/{created_todo["id"]}')
        assert get_response.status_code == 404
    
    def test_get_nonexistent_todo(self, client):
        """測試取得不存在的待辦事項 - Agent 邊界測試"""
        response = client.get('/api/todos/99999')
        data = json.loads(response.data)
        
        assert response.status_code == 404
        assert data['success'] is False
    
    def test_update_nonexistent_todo(self, client):
        """測試更新不存在的待辦事項 - Agent 邊界測試"""
        update_data = {'title': '更新標題'}
        response = client.put('/api/todos/99999', 
                            json=update_data,
                            content_type='application/json')
        data = json.loads(response.data)
        
        assert response.status_code == 404
        assert data['success'] is False
    
    def test_delete_nonexistent_todo(self, client):
        """測試刪除不存在的待辦事項 - Agent 邊界測試"""
        response = client.delete('/api/todos/99999')
        data = json.loads(response.data)
        
        assert response.status_code == 404
        assert data['success'] is False