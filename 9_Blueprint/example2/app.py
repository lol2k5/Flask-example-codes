from flask import Flask
from admin import admin_bp
from ctf import ctf_bp

app = Flask(__name__)

# 1 app có thể được đăng kí nhiều blueprint
app.register_blueprint(admin_bp)
app.register_blueprint(ctf_bp)


# flask --app app.py run
# Khi chạy, để ý log sẽ thấy dù truy cập ctf
# nhưng lại lấy css tại đường dẫn của admin
# và nội dung của file css đó vẫn giống với 
# của ctf, nên là thường họ sẽ gom hết mọi thứ
# vào 1 thư mục templates và static thôi
