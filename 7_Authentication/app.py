# Xác thực người dùng là 1 chức năng thường xuất hiện và
# và được sử dụng tại các trang web, ta sẽ sử dụng 
# flask_login để có thể thêm chức năng này vào
from typing import Any, Optional
from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy.engine import row
from email_validator import ValidatedEmail, validate_email, EmailNotValidError
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
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    # Hàm kiểm tra email
    @validates("email")
    def validate_email(self, id: int, email: str) -> str:
        try:
            v: ValidatedEmail = validate_email(email)
        except EmailNotValidError as e:
            raise ValueError("Invalid Email!") from e
        return v.email


# Trước khi thêm chức năng xác thực, ta cần tạo 1 hàm
# để flask_login có thể lấy người dùng thông qua id
@login_manager.user_loader
def load_user(user_id: Any) -> None:
    return db.session.get(Users, int(user_id))


# Hàm xử lý yêu cầu đăng kí 
@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if(request.method == "POST"):
        username: str = request.form.get("username")
        email: str = request.form.get("email")
        password: str = request.form.get("password")

        query_check_username: str = f"SELECT id FROM users where username='{username}';"
        query_check_email: str = f"SELECT id FROM users where email='{email}';"

        if(db.session.execute(text(query_check_username)).first()):
            return render_template("register.html", error="Username already taken!")
        
        if(db.session.execute(text(query_check_email)).first()):
            return render_template("register.html", error="Email already taken!")

        hashed_password: str = generate_password_hash(password).decode("utf-8")
        new_user: Users = Users(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


# Hàm sử lý yêu cầu đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if(request.method == "POST"):
        username: str = request.form.get("username")
        password: str = request.form.get("password")

        query_search_user: str = "SELECT * FROM users WHERE username=:username;"
        user: Optional[Users] = db.session.query(Users).from_statement(
                                   text(query_search_user)
                                ).params(username=username).one_or_none()

        if(user and check_password_hash(user.password, password)):
            login_user(user)
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")
        
    return render_template("login.html")


# Trang của người dùng
@app.route("/")
def index() -> str:
    return render_template("home.html")


# Đăng xuất
@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("login"))


@app.cli.command("init-db")
def init_db() -> None:
    with app.app_context():
        db.create_all()


@app.cli.command("test")
def test() -> None:
    from sqlalchemy import inspect
    print(inspect(db.engine).get_table_names())

# flask --app app.py init-db
# flask --app app.py run
# Lệnh đầu tiên là dùng để tạo cơ sở dữ liệu, lệnh sau để chạy 
# ứng dụng