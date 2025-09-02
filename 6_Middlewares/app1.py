# Middleware về cơ bản là 1 lớp phần mềm cho phép
# bạn xử lý yêu cầu trước khi nó được đưa cho máy
# chủ, phần logic chính xử lý và trước khi phản hồi
# được đưa đến cho người dùng

# Mục đích của chúng là sử dụng để:
# => Xử lý xác thực và phân quyền
# => Giám sát và Logging
# => Xử lý, lọc yêu cầu đầu vào
# => Xử lý yêu cầu đầu ra
# => Bảo mật 
from flask import Flask, Response, request

app = Flask(__name__)
COOKIE: str = "test_cookie"

# Cái đầu tiên ta cần quan tâm tới là 2 decorator 
# before_request và after_request, và đúng như tên
# gọi của chúng, 1 cái sẽ thực thi trước khi yêu cầu
# đến với hàm xử lý tương ứng và 1 cái thì trước khi
# phản hồi được gửi
@app.before_request
def log_request() -> None:
    print(f"Incoming request: {request.method} {request.url}")

@app.after_request
def log_response(response: Response) -> Response:
    print(f"Outgoing response: {response.status_code}")
    return response


# Có thể cùng tồn tại nhiều lớp middleware cho phép ta có 
# thể phân chia công việc giữa các hàm, ví dụ như ở trên là
# để log lại còn ở dưới đây là cho bảo mật chẳng hạn
@app.before_request
def check_pass() -> None:
    cookie: str | None = request.cookies.get("tmp")
    if(cookie != COOKIE):
        return "Goodbye!"
# Tại trình duyệt, nhấn f12 và vào mục application, ở đó
# sé có nơi giúp bạn đặt giá trị của cookie, thử đặt 1 
# cookie với tên là "tmp" và giá trị "test_cookie"


@app.route("/")
def index() -> str:
    return "Hello There"

# flask --app app1.py run
