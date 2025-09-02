# Bản thân Flask không có các tính năng hỗ trợ nó để
# tương tác với csdl nên nó dựa nhiều phần vào SQLAlchemy,
# framework này cung cấp cơ chế ORM cho phép tương tác
# với các csdl như SQLite, PostgreSQL, MongoDB, ...

# Ta lấy mã nguồn từ thư mục 2_Flask_models để demo cũng
# như nói sâu hơn về cách ta sẽ tương tác với SQLAlchemy
from pydoc import text
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Select, and_, or_, func, text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timedelta


app: Flask = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db: SQLAlchemy = SQLAlchemy(app)


# Phần tạo model khác với ứng dụng ở Flask models, tuy 
# nhiên theo doc thì đây là cách khai báo đúng
class Note(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    info: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Note {self.id}>"
# Ngoài các kiểu được viết ở đây ra thì ta còn có các kiểu dữ 
# liệu tương ứng với cơ sở dữ liệu SQL, tất cả các kiểu đó đều 
# được biểu diễn dưới dạng Camel case, tức interger(SQL) tương 
# ứng với Interger (SQLAlchemy), float với Float, text với Text ...


# Phần tạo và xóa thì ta không cần nói nhiều do nó đã
# khá rõ ràng rồi, ta thêm 1 phần tử hoặc xóa 1 phần
# tử được chỉ định
def add_note(note_information: str) -> None:
    new_note: Note = Note(info=note_information)
    db.session.add(new_note)
    db.session.commit()


# Để chọn chính sác vật thể, ta có thể sử dụng phương 
# thức get, tuy nhiên thì ta sẽ chỉ có thể chọn dựa trên
# khóa chính với phương thức này, đổi lại ta biết là có
# thể chọn chính sác vật thể nào. 
def delete_note(id: int) -> None:
    note_need_to_delete: Note = db.session.get(Note, id)
    db.session.delete(note_need_to_delete)
    db.session.commit()
# Ta cũng đã biết thì nếu gọi phương thức add hay delete
# thì nó sẽ chưa xóa ngay mà nó sẽ dồn các truy vấn lại
# và chờ đến khi phương thức commit được gọi thì chúng
# mới thực hiện truy vấn


@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note_api(id: int) -> str:
    if(request.method == "DELETE"):
        delete_note(id)
        return f"Note {id} has been deleted!"
    
    return "Nothing happened"


# Khác với các truy vấn thêm, bớt, với các truy vấn 
# chỉ lấy thông tin thì ta không cần commit
@app.route("/", methods=["GET", "POST"]) 
def index() -> str:
    if(request.method == "POST"):
        note_info: str = request.form["content"]
        add_note(note_info)
        return redirect(url_for("index"))
    
    query: Select = db.select(Note).order_by(Note.date)
    query_result: iter[Note] = db.session.execute(query).scalars()
    # Như ở đây thì ta hiểu được là ta đang lấy toàn bộ cột liên
    # quan đến bảng Note, tuy nhiên thì sẽ có trường hợp ta chỉ
    # cần lấy 1 số cột nhất định, để làm vậy ta thự hiện như sau:
    #
    # query: Select = db.select(Note.id, Note.info).order_by(Note.date)
    # query_result: iter[Result] = db.session.execute(query)
    #
    # Ở trường hợp này thì ta chỉ lấy 2 cột của bảng note ra, lúc ấy
    # ta chỉ cần bỏ phương thức scalars do tác dụng của nó chỉ là lấy
    # cột đầu (Vật thể Note) và tách chúng ra, còn đây là ta đã chỉ rõ
    # được các cột nên ta chỉ cần sử dụng luôn

    return render_template("index.html", notes=query_result)


# Dưới đây sẽ trình bày 1 số ví dụ truy vấn sử dụng SQLAlchemy
# Chạy lệnh sau để xem các truy vấn:
# flask --app app_SQLAlchemy.py demo
@app.cli.command("demo")
def query_demo() -> None:
    # Lấy toàn bộ cột trong 1 bảng
    query1: Select = db.select(Note)
    print("Truy van 1:")
    print(query1, '\n')

    # Lấy chính sách từng cột
    query2: Select = db.select(Note.id, Note.date)
    print("Truy van 2:")
    print(query2, '\n')

    # Lấy theo điều kiện
    query3: Select = \
        db.select(Note).where(
            and_(
                Note.id > 1, 
                Note.info.like("% cache %")
            )
        )
    # Nếu bạn thấy điều kiện truy vấn nhì hơi lạ thì thực ra là
    # framework đang gán giá trị thôi, như truy vấn trên có dạng:
    #
    # SELECT note.id, note.info, note.date
    # FROM note
    # WHERE note.id > :id_1 AND note.info LIKE :info_1
    #
    # Nhưng thật ra thì id_1 được gán cho 1 còn info_1 thì được
    # gán cho "% cache %"
    print("Truy van 3:")
    print(query3, '\n')

    query4: Select = \
        db.select(Note).where(
            or_(
                Note.id < 4, 
                Note.date >= datetime.utcnow() - timedelta(days=7)
            )
        )
    print("Truy van 4:")
    print(query4, '\n')

    # Sử dụng Aggregate Func
    query5: Select = \
        db.select(func.count(Note.id).label("notes")).select_from(Note)
    print("Truy van 5:")
    print(query5, '\n')

    query6: Select = \
        db.select(
            Note.date,      # lưu ý: func.date() hợp với SQLite/MySQL; Postgres có thể dùng date_trunc
            func.count(Note.id).label("n_notes")
        ) \
        .group_by(Note.date) \
        .order_by(Note.date.desc())
    print("Truy van 6:")
    print(query6, '\n')

    query7: Select = \
        db.select(
        Note.date,
        func.count(Note.id).label("n_notes")
    ) \
    .group_by(Note.date) \
    .having(func.count(Note.id) >= 5) \
    .order_by(Note.date.desc())
    print("Truy van 7:")
    print(query7, '\n')
    # Đây là ví dụ thôi

    # Ta cũng có thể tự tạo truy vấn và thực thi thay vì
    # phải dựa vào các hàm có sẵn như trên
    query8: str = "SELECT id, info, date FROM note;"
    print("Truy van 8:")
    print(query8, end = "\n\n")

    # Nhớ là lúc thực hiện truy vấn thì ta phải đưa nó vào
    # hàm text
    result: iter[Result] = db.session.execute(text(query8))
    
    print("Ket qua:")
    for note in result:
        print("Note" + str(note.id) + ':')
        print(note.info)
        print("Datetime :", note.date)
        print()



@app.cli.command("init-db")
def init_db() -> None:
    with app.app_context():
        db.create_all()

# flask --app app_SQLAlchemy.py init-db
# flask --app app_SQLAlchemy.py run --host=địa_chỉ_ip --port=cổng_ảo
# Lệnh đầu tiên là dùng để tạo cơ sở dữ liệu, lệnh sau để chạy 
# ứng dụng

# Nhớ chỉnh script.js, đoạn chứa địa chỉ ip và cổng để gọi api
# theo host và port
