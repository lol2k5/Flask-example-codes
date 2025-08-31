# Đôi khi ta sẽ cần cấu hình ứng dụng của chúng ta để 
# nó có thể hoạt động theo ý muốn
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ


app: Flask = Flask(__name__)

# Các cấu hình trong ứng dụng có thể được truy cập qua
# thuộc tính config, syntax như ví dụ sau:
# app.config["tên_tùy_chỉnh"] = giá_trị

# Tất nhiên là ta có thể thực hiện thêm tùy chỉnh thông
# qua 1 file khác trong trường hợp cần giấu gì đó:
app.config.from_file("config.py")

# Hoặc là lấy trực tiếp giá trị từ các biến môi trường 
# trong hệ điều hành
app.config["ENV"] = environ.get('default_key')


# Có rất nhiều tùy chỉnh theo điều khiển nhiều thứ khác 
# nhau trong 1 ứng dụng và chúng có thể bao gồm:
# Bảo mật, như là secret key và quản lý phiên
app.config['SECRET_KEY'] = "key"
app.config['SESSION_TYPE'] = "filesystem"
app.config['PERMANENT_SESSION_LEFT_TIME'] = timedelta(days = 1)

# Liên quan đến cơ sở dữ liệu
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Với postgresql
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://username:password@localhost/tên_csdl"

# Liên quan đến Debug
app.config["DEBUG"] = True

# Liên quan đến vấn đề lưu trữ file
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024 # 5 MB