"""
BMAD Todo API 路由
Big Model: RESTful API 設計決策
Agent: HTTP 請求處理與回應邏輯
Design: API 介面規格定義
"""

from flask import Blueprint, request, jsonify
from models.todo import TodoModel

# 建立 API 藍圖 - Big Model 模組化架構
api_bp = Blueprint('api', __name__)

# 初始化 Todo 模型 - Agent 資料層整合
todo_model = TodoModel()

@api_bp.route('/todos', methods=['GET'])
def get_todos():
    """取得所有待辦事項 - Agent 實現"""
    try:
        todos = todo_model.get_all_todos()
        return jsonify({
            'success': True,
            'data': todos,
            'message': '成功取得待辦清單'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '取得待辦清單失敗'
        }), 500

@api_bp.route('/todos', methods=['POST'])
def create_todo():
    """新增待辦事項 - Agent 實現"""
    try:
        data = request.get_json()
        
        if not data or not data.get('title'):
            return jsonify({
                'success': False,
                'message': '待辦事項標題不能為空'
            }), 400
        
        todo = todo_model.create_todo(data['title'])
        return jsonify({
            'success': True,
            'data': todo,
            'message': '成功新增待辦事項'
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '新增待辦事項失敗'
        }), 500

@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """更新待辦事項 - Agent 實現"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': '請提供更新資料'
            }), 400
        
        todo = todo_model.update_todo(todo_id, **data)
        
        if not todo:
            return jsonify({
                'success': False,
                'message': '找不到指定的待辦事項'
            }), 404
        
        return jsonify({
            'success': True,
            'data': todo,
            'message': '成功更新待辦事項'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '更新待辦事項失敗'
        }), 500

@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """刪除待辦事項 - Agent 實現"""
    try:
        success = todo_model.delete_todo(todo_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': '找不到指定的待辦事項'
            }), 404
        
        return jsonify({
            'success': True,
            'message': '成功刪除待辦事項'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '刪除待辦事項失敗'
        }), 500

@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """取得單一待辦事項 - Agent 實現"""
    try:
        todo = todo_model.get_todo(todo_id)
        
        if not todo:
            return jsonify({
                'success': False,
                'message': '找不到指定的待辦事項'
            }), 404
        
        return jsonify({
            'success': True,
            'data': todo,
            'message': '成功取得待辦事項'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '取得待辦事項失敗'
        }), 500