/**
 * BMAD Todo List 前端應用
 * Big Model: 前端架構與狀態管理設計
 * Agent: DOM 操作與 API 通訊實現
 * Design: 使用者互動邏輯與視覺回饋
 */

class TodoApp {
    constructor() {
        // Big Model: 應用狀態初始化
        this.todos = [];
        this.currentDeleteId = null;
        
        // Agent: DOM 元素引用
        this.elements = {
            todoInput: document.getElementById('todoInput'),
            addBtn: document.getElementById('addBtn'),
            todoList: document.getElementById('todoList'),
            emptyState: document.getElementById('emptyState'),
            loadingState: document.getElementById('loadingState'),
            totalCount: document.getElementById('totalCount'),
            completedCount: document.getElementById('completedCount'),
            pendingCount: document.getElementById('pendingCount'),
            confirmModal: document.getElementById('confirmModal'),
            confirmDelete: document.getElementById('confirmDelete'),
            cancelDelete: document.getElementById('cancelDelete')
        };
        
        this.init();
    }
    
    // Big Model: 應用初始化流程
    init() {
        this.bindEvents();
        this.loadTodos();
    }
    
    // Agent: 事件綁定
    bindEvents() {
        // 新增待辦事項
        this.elements.addBtn.addEventListener('click', () => this.addTodo());
        this.elements.todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });
        
        // 確認對話框事件
        this.elements.confirmDelete.addEventListener('click', () => this.confirmDeleteTodo());
        this.elements.cancelDelete.addEventListener('click', () => this.hideConfirmModal());
        
        // 點擊遮罩關閉對話框
        this.elements.confirmModal.addEventListener('click', (e) => {
            if (e.target === this.elements.confirmModal) {
                this.hideConfirmModal();
            }
        });
    }
    
    // Agent: API 請求 - 載入所有待辦事項
    async loadTodos() {
        try {
            this.showLoading(true);
            const response = await fetch('/api/todos');
            const data = await response.json();
            
            if (data.success) {
                this.todos = data.data;
                this.renderTodos();
                this.updateStats();
            } else {
                this.showError('載入待辦事項失敗：' + data.message);
            }
        } catch (error) {
            this.showError('網路錯誤：無法載入待辦事項');
        } finally {
            this.showLoading(false);
        }
    }
    
    // Agent: API 請求 - 新增待辦事項
    async addTodo() {
        const title = this.elements.todoInput.value.trim();
        
        if (!title) {
            this.elements.todoInput.focus();
            return;
        }
        
        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.todos.unshift(data.data);
                this.elements.todoInput.value = '';
                this.renderTodos();
                this.updateStats();
                this.showSuccess('成功新增待辦事項');
            } else {
                this.showError('新增失敗：' + data.message);
            }
        } catch (error) {
            this.showError('網路錯誤：無法新增待辦事項');
        }
    }
    
    // Agent: API 請求 - 更新待辦事項
    async updateTodo(id, updates) {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updates)
            });
            
            const data = await response.json();
            
            if (data.success) {
                const index = this.todos.findIndex(todo => todo.id === id);
                if (index !== -1) {
                    this.todos[index] = data.data;
                    this.renderTodos();
                    this.updateStats();
                }
            } else {
                this.showError('更新失敗：' + data.message);
            }
        } catch (error) {
            this.showError('網路錯誤：無法更新待辦事項');
        }
    }
    
    // Agent: API 請求 - 刪除待辦事項
    async deleteTodo(id) {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.todos = this.todos.filter(todo => todo.id !== id);
                this.renderTodos();
                this.updateStats();
                this.showSuccess('成功刪除待辦事項');
            } else {
                this.showError('刪除失敗：' + data.message);
            }
        } catch (error) {
            this.showError('網路錯誤：無法刪除待辦事項');
        }
    }
    
    // Design: 渲染待辦清單
    renderTodos() {
        if (this.todos.length === 0) {
            this.elements.todoList.style.display = 'none';
            this.elements.emptyState.style.display = 'block';
            return;
        }
        
        this.elements.todoList.style.display = 'block';
        this.elements.emptyState.style.display = 'none';
        
        this.elements.todoList.innerHTML = this.todos.map(todo => `
            <div class="todo-item" data-id="${todo.id}">
                <input 
                    type="checkbox" 
                    class="todo-checkbox" 
                    ${todo.completed ? 'checked' : ''} 
                    onchange="app.toggleTodo(${todo.id})"
                >
                <div class="todo-content ${todo.completed ? 'completed' : ''}">
                    ${this.escapeHtml(todo.title)}
                    <div class="todo-meta">
                        建立時間：${this.formatDate(todo.created_at)}
                        ${todo.updated_at !== todo.created_at ? 
                            ` | 更新時間：${this.formatDate(todo.updated_at)}` : ''
                        }
                    </div>
                </div>
                <div class="todo-actions">
                    <button 
                        class="btn btn-danger" 
                        onclick="app.showDeleteConfirm(${todo.id})"
                    >
                        刪除
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    // Agent: 切換待辦事項完成狀態
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            this.updateTodo(id, { completed: !todo.completed });
        }
    }
    
    // Design: 顯示刪除確認對話框
    showDeleteConfirm(id) {
        this.currentDeleteId = id;
        this.elements.confirmModal.style.display = 'flex';
    }
    
    // Design: 隱藏確認對話框
    hideConfirmModal() {
        this.elements.confirmModal.style.display = 'none';
        this.currentDeleteId = null;
    }
    
    // Agent: 確認刪除操作
    confirmDeleteTodo() {
        if (this.currentDeleteId) {
            this.deleteTodo(this.currentDeleteId);
            this.hideConfirmModal();
        }
    }
    
    // Design: 更新統計資訊
    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(todo => todo.completed).length;
        const pending = total - completed;
        
        this.elements.totalCount.textContent = total;
        this.elements.completedCount.textContent = completed;
        this.elements.pendingCount.textContent = pending;
    }
    
    // Design: 顯示/隱藏載入狀態
    showLoading(show) {
        this.elements.loadingState.style.display = show ? 'block' : 'none';
    }
    
    // Design: 顯示成功訊息
    showSuccess(message) {
        this.showNotification(message, 'success');
    }
    
    // Design: 顯示錯誤訊息
    showError(message) {
        this.showNotification(message, 'error');
    }
    
    // Design: 通用通知顯示
    showNotification(message, type = 'info') {
        // 創建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">
                    ${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}
                </span>
                <span class="notification-message">${message}</span>
            </div>
        `;
        
        // 添加樣式
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            zIndex: '9999',
            backgroundColor: type === 'success' ? '#7ed321' : 
                           type === 'error' ? '#d0021b' : '#4a90e2',
            color: 'white',
            padding: '12px 20px',
            borderRadius: '8px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });
        
        document.body.appendChild(notification);
        
        // 顯示動畫
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // 自動隱藏
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // 工具函數：HTML 轉義
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // 工具函數：日期格式化
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('zh-TW', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Big Model: 應用程式入口點
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TodoApp();
});