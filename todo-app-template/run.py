#!/usr/bin/env python3
"""
BMAD Todo List 應用啟動腳本
簡化的應用程式入口點
"""

from app import create_app
import os

if __name__ == '__main__':
    # 確保資料庫目錄存在
    if not os.path.exists('database'):
        os.makedirs('database')
    
    # 創建應用程式實例
    app = create_app()
    
    # 運行應用程式
    print("🚀 BMAD Todo List 應用正在啟動...")
    print("📱 請在瀏覽器中開啟: http://localhost:5000")
    print("📋 基於 BMAD 方法論的待辦清單應用")
    print("⚙️  按 Ctrl+C 停止服務")
    
    app.run(debug=True, host='0.0.0.0', port=5000)