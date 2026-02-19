from flask import Flask
from modules.users import users_bp


app = Flask(__name__)


# Đăng ký Blueprint 
app.register_blueprint(users_bp)


# Ví dụ về sử dụng OOP trong Flask
# flask --app app.py run