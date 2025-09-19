"""
BMAD Todo List 應用主程式
Big Model: 應用架構與配置
Agent: Flask 應用初始化與路由註冊
Design: API 端點設計
"""

from flask import Flask, render_template
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    """應用工廠函數 - Big Model 架構決策"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bmad-todo-secret-key'
    
    # 啟用 CORS 支援前端呼叫
    CORS(app)
    
    # 註冊 API 藍圖 - Agent 模組整合
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 主頁路由 - Design 界面入口
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)