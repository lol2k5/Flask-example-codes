from flask import Blueprint, jsonify
from .services import UserService


# Khởi tạo Blueprint cùng đường dẫn api
users_bp = Blueprint('users', __name__, url_prefix='/api/users')

# Định nghĩa Controller
class UserController:
    def __init__(self, blueprint: Blueprint):
        self.service = UserService()
        
        # Dùng add_url_rule để gắn phương thức của class vào Blueprint
        blueprint.add_url_rule('/', view_func=self.get_users, methods=['GET'])
        blueprint.add_url_rule('/<int:user_id>', view_func=self.get_user_by_id, methods=['GET'])

    def get_users(self) -> str:
        data = self.service.get_all()
        return jsonify(data), 200

    def get_user_by_id(self, user_id: int) -> str:
        return jsonify({"message": f"Find user with id: {user_id}"}), 200

# Khởi tạo Controller và truyền Blueprint vào để nó tự động đăng ký các route
UserController(users_bp)