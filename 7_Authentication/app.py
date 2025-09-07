# Xác thực người dùng là 1 chức năng thường xuất hiện và
# và được sử dụng tại các trang web, ta sẽ sử dụng 
# flask_login để có thể thêm chức năng này vào
from typing import Any, Optional
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.engine import row
from email_validator import ValidatedEmail, validate_email, EmailNotValidError
from re import match
from flask_bcrypt import check_password_hash, generate_password_hash


# Tạo app
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

# Tạo database và quản lý đăng nhập
db: SQLAlchemy = SQLAlchemy(app)
login_manager: LoginManager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Tạo model người dùng
class Users(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    # Hàm kiểm tra email
    @validates("email")
    def validate_email(self, id: int, email: str) -> str:
        try:
            v: ValidatedEmail = validate_email(email)
        except EmailNotValidError as e:
            raise ValueError("Invalid Email!") from e
        return v.email

    # Hàm kiểm tra mật khẩu đầu vào
    def validate_input_password(password: str) -> bool:
        # Nó phải thỏa mãn các điều kiện:
        # Dài ít nhất 12 kí tự
        # Có ít nhất 1 chữ cái hoa, 1 chữ cái thường
        # Có ít nhất 1 số
        # Có ít nhất 1 kí tự đặc biệtbiệt
        pattern: str = r"^(?=.{12,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).*$"
        return bool(match(pattern, password))


# Midderware để kiểm tra người dùng đã đăng nhập chưa
@app.before_request
def check_login() -> str | None:
    # Nếu đăng nhập rồi thì cho qua
    if(current_user.is_authenticated):
       return None

    # Nếu chưa nhưng đang cố gắng đến trang đăng nhâp hoặc
    # đăng kí thì cho qua
    if(request.endpoint in {"login", "register"}):
        return None

    # Các trường hợp còn lại thì đều chuyển hớp về trang 
    # đăng nhập
    return redirect(url_for("login"))


# Trước khi thêm chức năng xác thực, ta cần tạo 1 hàm
# để flask_login có thể lấy người dùng thông qua id
@login_manager.user_loader
def load_user(user_id: Any) -> None:
    return db.session.get(Users, int(user_id))


# Hàm xử lý yêu cầu đăng kí 
@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if(request.method == "POST"):
        try:
            # Lấy các thông tin cần thiết
            username: str = request.form.get("username")
            email: str = request.form.get("email")
            password: str = request.form.get("password")

            # Khai báo truy vấn
            query_check_username: str = "SELECT id FROM users where username=:username;"
            query_check_email: str = "SELECT id FROM users where email=:email;"

            # Sử dụng truy vấn để tìm tên người dùng trùng
            # Nếu tìm thấy thì ép đăng nhập lại
            if(db.session.execute(text(query_check_username).params(username=username)).first()):
                return render_template("register.html", error="Username already taken!")

            # Tương tự với trường hợp tìm thấy email trùng
            if(db.session.execute(text(query_check_email).params(email=email)).first()):
                return render_template("register.html", error="Email already taken!")

            # Trường hợp người dùng có thông qua proxy để chỉnh sửa yêu cầu
            if(not Users.validate_input_password(password)):
                raise ValueError("Invalid Password!")

            # Nếu không thấy cái gì trùng, ta băm mật khẩu và
            # lưu dữ liệu vào bảng thể hiện đây là người dùng mới
            hashed_password: str = generate_password_hash(password).decode("utf-8")
            new_user: Users = Users(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
        except ValueError as v:
            return render_template("register.html", error=v.args[0])

        return redirect(url_for("login"))

    return render_template("register.html")


# Hàm sử lý yêu cầu đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if(request.method == "POST"):
        try:
            # Lấy các thông tin cần thiết
            username: str = request.form.get("username")
            password: str = request.form.get("password")

            # Trường hợp người dùng có thông qua proxy để chỉnh sửa yêu cầu
            if(not username or not password):
                raise ValueError("Username and password cannot be blank")

            # Khai báo truy vấn tìm người dùng
            query_search_user: str = "SELECT * FROM users WHERE username=:username;"

            # Ta phải truy vấn tất cả các cột vì cần phải
            # lấy 1 instance của người dùng đó, sau đó mới
            # có thể truyền vào hàm login_user được
            user: Optional[Users] = db.session.query(Users).from_statement(
                                       text(query_search_user)
                                    ).params(username=username).one_or_none()

            # Nếu tìm thấy user và mã băm của mật khẩu đầu vào
            # khớp với trong cldl thì cho vào
            if(user and check_password_hash(user.password, password)):
                login_user(user)
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Invalid username or password")
        except ValueError as v:
            return render_template("login.html", error=v.args[0])

    return render_template("login.html")


# Trang của người dùng
@app.route("/")
@login_required
def index() -> str:
    return render_template("home.html")


# Đăng xuất
@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("login"))


# Thay đổi email của 1 người
@app.route("/change_email", methods=["POST"])
@login_required
def change_email() -> str:
    try:
        # Đầu tiên lấy email mới từ form
        new_email: str = request.form.get("email")

        # Sau đó lấy instance người dùng tương ứng
        user_to_update: Users = db.session.get(Users, current_user.id)

        # Gán giá trị email mới cho người dùng đó
        user_to_update.email = new_email

        # Gửi truy vấn cập nhật lên máy chủ
        db.session.commit()
    except ValueError as v:
        return render_template("home.html", mess=v.args[0])
    
    return render_template("home.html", mess="Email has been changed successfully!")


# Lệnh tạo csdl
@app.cli.command("init-db")
def init_db() -> None:
    with app.app_context():
        db.create_all()


@app.cli.command("test")
def test() -> None:
    pass

# flask --app app.py init-db
# flask --app app.py run
# Lệnh đầu tiên là dùng để tạo cơ sở dữ liệu, lệnh sau để chạy 
# ứng dụng