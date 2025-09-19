"""
BMAD Todo 模型測試
Agent: 資料層測試實現
"""

import pytest
import tempfile
import os
from models.todo import TodoModel

class TestTodoModel:
    """Todo 模型測試類 - Agent 測試職責"""
    
    @pytest.fixture
    def todo_model(self):
        """測試用的 Todo 模型實例"""
        # 創建臨時資料庫文件
        db_fd, db_path = tempfile.mkstemp()
        model = TodoModel(db_path)
        yield model
        # 清理
        os.close(db_fd)
        os.unlink(db_path)
    
    def test_create_todo(self, todo_model):
        """測試新增待辦事項 - Agent 功能驗證"""
        todo = todo_model.create_todo("測試待辦事項")
        
        assert todo is not None
        assert todo['title'] == "測試待辦事項"
        assert todo['completed'] is False
        assert 'id' in todo
        assert 'created_at' in todo
    
    def test_get_all_todos(self, todo_model):
        """測試取得所有待辦事項 - Agent 功能驗證"""
        # 新增幾個測試項目
        todo1 = todo_model.create_todo("待辦事項 1")
        todo2 = todo_model.create_todo("待辦事項 2")
        
        todos = todo_model.get_all_todos()
        
        assert len(todos) == 2
        assert todos[0]['title'] == "待辦事項 2"  # 最新的在前面
        assert todos[1]['title'] == "待辦事項 1"
    
    def test_update_todo(self, todo_model):
        """測試更新待辦事項 - Agent 功能驗證"""
        todo = todo_model.create_todo("原始標題")
        
        # 更新標題
        updated = todo_model.update_todo(todo['id'], title="更新後標題")
        assert updated['title'] == "更新後標題"
        
        # 更新完成狀態
        updated = todo_model.update_todo(todo['id'], completed=True)
        assert updated['completed'] is True
    
    def test_delete_todo(self, todo_model):
        """測試刪除待辦事項 - Agent 功能驗證"""
        todo = todo_model.create_todo("要刪除的事項")
        
        # 確認刪除成功
        success = todo_model.delete_todo(todo['id'])
        assert success is True
        
        # 確認已被刪除
        deleted_todo = todo_model.get_todo(todo['id'])
        assert deleted_todo is None
    
    def test_get_nonexistent_todo(self, todo_model):
        """測試取得不存在的待辦事項 - Agent 邊界測試"""
        todo = todo_model.get_todo(99999)
        assert todo is None
    
    def test_delete_nonexistent_todo(self, todo_model):
        """測試刪除不存在的待辦事項 - Agent 邊界測試"""
        success = todo_model.delete_todo(99999)
        assert success is False