# Ngoài middleware cơ bản mà flask cung cấp, ta còn
# có các thư việ như flask_cors, flask_limiter, 
# flask_talisman, ... 
# Ở đây ta lấy ví dụ về flask_cors

# CORS là 1 cơ chế bảo mật được sử dụng bởi các trình
# duyệt với mục đích ngăn chặn các tài nguyên mạng của
# 1 miền truy cập bởi 1 miền khác nếu không có sự
# cho phép
from flask import Flask
from flask_cors import CORS

app: Flask = Flask(__name__)

# Thiết lập các miền được phép truy cập với trang,
# ở đây nghĩa là ta chỉ có thể vào trang này thông
# qua chính nó chứ không thể được gọi từ các trang khác
CORS(app, origins = ["http://192.168.2.3:5000"])
# Bạn có thể thêm các miền vào theo 1 danh sách và các
# miền đó cũng có thể gửi yêu cầu, có thể là thông qua
# hàm fetch đến trang này

@app.route("/")
def index() -> str:
    return "Hello"

# flask --app app2.py run --host=địa_chỉ_ip
# Bạn có thể thử sử dụng lệnh để tạo 1 trang web tại
# 1 cổng khác để thử dùng hàm fetch tại console