# Trong flask, khuân mẫu (model) thể hiện cấu trúc dữ liệu 
# và quản lý tương tác với database
# Tức là cho phép tương tác với database thông qua OOP và ORM

# ORM (Object Relational Mapping) là kĩ thuật mà các model sử
# dụng để tương tác với database dễ hơn, thay vì dùng sql, ta 
# dùng các phương thức của lớp
# Ta có thể sử dụng thư viện SQLAlchemy để tương tác, đầu tiên 
# ta import thư viện vào và setup 1 số thứ
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app: Flask = Flask(__name__)

# Tiếp theo thì ta cấu hình cơ sở dữ liệu
# Ở đây là tên file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# File này sẽ được lưu tại thư mục Instance, thư mục này sẽ được 
# tạo tại đường dẫn nơi ta chạy úng dụng

# Tắt tự động kiểm tra thay đổi database không cần thiết
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Tạo vật thể database
db: SQLAlchemy = SQLAlchemy(app)

# Tạo 1 lớp model, ở đây ta sẽ tạo 1 app ghi chú đơn giản, mỗi 
# ghi chú sẽ có 2 thuộc tính là thông tin và thời gian, thông 
# tin do người dùng nhập vào còn thời gian sẽ là lúc người dùng 
# nhập thông tin ghi chú đó.
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# Để có thể thêm dữ liệu vào bảng, ta cần tạo 1 vật Note,
# sau đó thêm nó vào database thông qua phương thức commit
def add_note(note_information: str) -> None:
    # Tạo 1 vật thể Note thêm thông tin được thêm vàovào
    new_note: Note = Note(info=note_information)

    # Thêm vật thể vào session nhưng chưa gửi đi để lưu 
    # vào database
    db.session.add(new_note)

    # Lưu vật thể được đánh dấu thông qua phương thức add 
    # vào database
    db.session.commit()


# Xóa 1 ghi chú khỏi database
def delete_note(id: int) -> None:
    # Tìm ghi chú cần xóa
    note_need_to_delete: Note = db.session.get(Note, id)

    # Thêm nó vào danh sách xóa
    db.session.delete(note_need_to_delete)

    # Xóa nó đi
    db.session.commit()


# API lấy toàn bộ các ghi chú
@app.route("/notes")
def show_note_api() -> str:
    # Lấy toàn bộ các ghi chú trong cơ sở dữ liệu
    # Phương thức select và order by dùng để tạo truy vấn
    # execute dùng để thực hiện truy vấn đó và trả về vật thể Result
    # scalars chuyển cột đầu tiên lấy được từ kết quả trong vật 
    # thể Result thành các Note instance và chuyển chúng thành 1 iter
    # all thực hiện chuyển iter thành list
    query_result: list[Note] = db.session.execute(db.select(Note).order_by(Note.date)).scalars().all()

    # Trả về kết quả dưới dạng JSON
    # Vì là instance nên ta phải có bước chuyển đổi sang vật thể
    return jsonify([{
        "id": note.id,
        "info": note.info,
        "date": note.date
    } for note in query_result])


# API xóa 1 note dựa trên id
@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note_api(id: int) -> str:
    if(request.method == "DELETE"):
        delete_note(id)
        return f"Note {id} has been deleted!"
    
    return "Nothing happened"


# Trang chính
@app.route("/", methods=["GET", "POST"]) 
def index() -> str:
    # Nếu là yêu cầu POST, ta cập nhật ghi chú vào database 
    # và chuyển hướng quay lại trang chính.
    if(request.method == "POST"):
        note_info: str = request.form["content"]
        add_note(note_info)
        return redirect(url_for("index"))
    
    # Nếu là yêu cầu GET thông thường thì trả về trang chính
    return render_template("index.html")


# Hàm tạo bảng
# vì nếu chạy với flask thay vì python3 dòng lệnh dưới
# if __name__ == __main__: sẽ không bao giờ được chạychạy
@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()

# flask --app app.py init-db
# flask --app app.py run --host=địa_chỉ_ip --port=cổng_ảo
# Lệnh đầu tiên là dùng để tạo cơ sở dữ liệu, lệnh sau để chạy 
# ứng dụng
# Nhớ chỉnh script.js, đoạn chứa địa chỉ ip và cổng để gọi api
# theo host và port