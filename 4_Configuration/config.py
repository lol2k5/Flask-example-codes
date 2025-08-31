

# Ta có thể dựa vào việc khai báo các lớp để thêm
# đặt các giá trị cho các tùy chỉnh
class Config:
    SECRET_KEY = "test"


class Development(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    DEBUG = True


class Prodution(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost/database.db"
    DEBUG = False

# Sau đó ta có thể dùng phương thức from_object để 
# đặt các config cần thiết
# Trong trường hợp có ta cần có nhiều phương thức
# tùy chỉnh khác nhau, như là khi phát triển và khi
# thử nghiệm thành quả thì ta cũng có thể ép ứng dụng
# sử dụng tùy chỉnh nhất định tùy trường hợp

if app.config["ENV"] == "development":
    app.config.from_object("config.Development")
elif app.config["ENV"] == "Prodution":
    app.config.from_object("config.Prodution")
    # app.config.from_object("tên_file.tên_lớp")