// Todo List App JavaScript
class TodoApp {
    constructor() {
        this.todos = [];
        this.nextId = 1;
        
        // Get DOM elements
        this.todoInput = document.getElementById('todoInput');
        this.addTodoBtn = document.getElementById('addTodoBtn');
        this.todoList = document.getElementById('todoList');
        
        // Bind methods to maintain context
        this.addTodo = this.addTodo.bind(this);
        this.toggleTodo = this.toggleTodo.bind(this);
        this.handleInputKeyPress = this.handleInputKeyPress.bind(this);
        
        // Set up event listeners
        this.initEventListeners();
        
        // Show empty state initially
        this.renderTodos();
    }
    
    initEventListeners() {
        this.addTodoBtn.addEventListener('click', this.addTodo);
        this.todoInput.addEventListener('keypress', this.handleInputKeyPress);
    }
    
    handleInputKeyPress(event) {
        if (event.key === 'Enter') {
            this.addTodo();
        }
    }
    
    addTodo() {
        const text = this.todoInput.value.trim();
        
        if (text === '') {
            alert('請輸入待辦事項內容');
            return;
        }
        
        const newTodo = {
            id: this.nextId++,
            text: text,
            completed: false
        };
        
        this.todos.push(newTodo);
        this.todoInput.value = '';
        this.renderTodos();
    }
    
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.renderTodos();
        }
    }
    
    renderTodos() {
        // Clear the current list
        this.todoList.innerHTML = '';
        
        if (this.todos.length === 0) {
            this.renderEmptyState();
            return;
        }
        
        // Render each todo item
        this.todos.forEach(todo => {
            const todoItem = this.createTodoElement(todo);
            this.todoList.appendChild(todoItem);
        });
    }
    
    renderEmptyState() {
        const emptyElement = document.createElement('li');
        emptyElement.className = 'empty-state';
        emptyElement.textContent = '還沒有待辦事項，開始新增一些吧！';
        this.todoList.appendChild(emptyElement);
    }
    
    createTodoElement(todo) {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'todo-checkbox';
        checkbox.checked = todo.completed;
        checkbox.addEventListener('change', () => this.toggleTodo(todo.id));
        
        const span = document.createElement('span');
        span.className = 'todo-text';
        span.textContent = todo.text;
        
        li.appendChild(checkbox);
        li.appendChild(span);
        
        return li;
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});