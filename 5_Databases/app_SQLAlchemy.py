# Bản thân Flask không có các tính năng hỗ trợ nó để
# tương tác với csdl nên nó dựa nhiều phần vào SQLAlchemy,
# framework này cung cấp cơ chế ORM cho phép tương tác
# với các csdl như MySQL, SQLite, PostgreSQL, ...

# Ta lấy mã nguồn từ thư mục 2_Flask_models để demo cũng
# như nói 1 chút về cách ta sẽ tương tác với SQLAlchemy
from flask import Flask, redirect, render_template, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app: Flask = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


def add_note(note_information: str) -> None:
    new_note: Note = Note(info=note_information)
    db.session.add(new_note)
    db.session.commit()


def delete_note(id: int) -> None:
    note_need_to_delete: Note = db.session.get(Note, id)
    db.session.delete(note_need_to_delete)
    db.session.commit()


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note_api(id: int) -> str:
    if(request.method == "DELETE"):
        delete_note(id)
        return f"Note {id} has been deleted!"
    
    return "Nothing happened"


@app.route("/", methods=["GET", "POST"]) 
def index() -> str:
    if(request.method == "POST"):
        note_info: str = request.form["content"]
        add_note(note_info)
        return redirect(url_for("index"))
    
    query_result: list[Note] = Note.query.all()
    return render_template("index.html", notes=query_result)


@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()

# flask --app app_SQLAlchemy.py init-db
# flask --app app_SQLAlchemy.py run --host=địa_chỉ_ip --port=cổng_ảo
# Lệnh đầu tiên là dùng để tạo cơ sở dữ liệu, lệnh sau để chạy 
# ứng dụng

# Nhớ chỉnh script.js, đoạn chứa địa chỉ ip và cổng để gọi api
# theo host và port
