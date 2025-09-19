"""
BMAD Todo 資料模型
Big Model: 資料結構設計決策
Agent: 資料庫操作與業務邏輯實現
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class TodoModel:
    """Todo 資料模型類 - Agent 負責資料持久化"""
    
    def __init__(self, db_path: str = "database/todos.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化資料庫表結構 - Big Model 架構決策"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def create_todo(self, title: str) -> Dict:
        """新增待辦事項 - Agent 實現"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO todos (title) VALUES (?)", (title,)
            )
            todo_id = cursor.lastrowid
            conn.commit()
            
            return self.get_todo(todo_id)
    
    def get_todo(self, todo_id: int) -> Optional[Dict]:
        """取得單一待辦事項 - Agent 實現"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM todos WHERE id = ?", (todo_id,)
            )
            row = cursor.fetchone()
            
            if row:
                todo = dict(row)
                # 轉換布林值
                todo['completed'] = bool(todo['completed'])
                return todo
            return None
    
    def get_all_todos(self) -> List[Dict]:
        """取得所有待辦事項 - Agent 實現"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM todos ORDER BY id DESC"
            )
            rows = cursor.fetchall()
            
            todos = []
            for row in rows:
                todo = dict(row)
                # 轉換布林值
                todo['completed'] = bool(todo['completed'])
                todos.append(todo)
            
            return todos
    
    def update_todo(self, todo_id: int, **kwargs) -> Optional[Dict]:
        """更新待辦事項 - Agent 實現"""
        allowed_fields = ['title', 'completed']
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not update_fields:
            return self.get_todo(todo_id)
        
        update_fields['updated_at'] = datetime.now().isoformat()
        
        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values()) + [todo_id]
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"UPDATE todos SET {set_clause} WHERE id = ?", values
            )
            conn.commit()
            
            return self.get_todo(todo_id)
    
    def delete_todo(self, todo_id: int) -> bool:
        """刪除待辦事項 - Agent 實現"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            
            return cursor.rowcount > 0