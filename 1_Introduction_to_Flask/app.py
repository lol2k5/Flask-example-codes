# Đưa thư viện vào
from nt import abort
from flask import Flask, Response, make_response, redirect, render_template, request, url_for, abort

# Tạo app
app = Flask(__name__)

# Sử dụng decorator để xác định đường dẫn mong muốn
# Đây chính là routing
@app.route("/hello")
# Tạo hàm xử lý tương ứng với đường dẫn gắn với nó
def hello() -> str:
    return "Hello flask!"
# Đây chính là routing
# Khi người dùng truy cập đường dẫn tương ứng,
# hàm được gắn với nó sẽ chạy


# Biến tại flask, syntax:
# Lấy input dạng xâu
@app.route("/hello/<name>")
def hello_with_name(name: str) -> str:
    return "Hello %s!" % name

# Lấy input dạng số nguyên
@app.route("/int/<int:number>")
def show_int(number: int) -> str:
    return "Your number is %s" % number

# Lấy input dạng số thực
@app.route("/float/<float:number>")
def show_float(number: float) -> str:
    return "Your number is %s" % number
# Ngoài ra còn path, any và UUID


# redirect
@app.route("/admin")
def hello_admin() -> str:
    return "Hello Admin"

@app.route("/guest/<guest>")
def hello_guest(guest: str) -> str:
    return "Hello %s as Guest" % guest

@app.route("/user/<name>")
def hello_user(name: str) -> str:
    if name.lower() == "admin":
        return redirect(url_for("hello_admin"))
    else:
        return redirect(url_for("hello_guest", guest=name))
    # url_for lấy tên hàm và lấy các tham số
    # hoặc lấy tên thư mục và lấy file trong đó thông qua tham số filename
# Ngoài ra còn tham số status code và Response, mặc định thì giá trị của
# code là 302 còn Response thì tùy thuộc vào code được đưa ra, ta hoàn 
# toàn có thể điều chỉnh theo ý mình thông qua 2 tham số đó


# Báo lỗi thông qua abort
# Khi có lỗi xảy ra, ta có thể dùng hàm abort để tạo ra 1 trang lỗi riêng rẽ
@app.route("/usernameCheck/<name>")
def username_check(name: str) -> str:
    if name[0].isdigit():
        abort(400)
    return "Usable username"
# Gồm 2 tham số chính là mã code và tin nhắn trả về, nếu tin nhắn trả về để 
# trống thì sẽ tùy theo mã code được đưa


# Sử dụng html, css, js
@app.route("/")
# Ta sử dụng hàm render_template
# Có tác dụng lấy file tương ứng trong thưc mục templates
# và trả về như mẫu
def index() -> str:
    return render_template("index.html")
    # file được lấy sẽ được chuyển thành 1 xâu và được xử lý
    # Các template bên trong (xem file index.html)


# Cookies
# Xem file cookie.html và script.js
@app.route("/cookie")
def cookie() -> str:
    return render_template('cookie.html')

# Tham số methods xác định các phương thức cho phép (mặc định chỉ có GET)
@app.route("/setcookie", methods=["POST", "GET"])
def set_cookie() -> str:
    if request.method == "POST":
        # Nhận yêu cầu post từ form
        # Lấy giá trị input theo tên thuộc tính "name"
        cookie: str = request.form["cookie"]

        # Tạo 1 phàn hồi để có thể sử dụng phương thức
        # set_cookie nhằm đặt cookie cho lần phản hồi này
        resq: Response = make_response(render_template("cookie.html"))
        resq.set_cookie("tmp", cookie)

        return resq
    else:
        # Chuyển hướng về /cookie nếu là yêu cầu GET
        return redirect(url_for("cookie"))

@app.route("/getcookie")
def get_cookie() -> str:
    try:
        # Lấy cookie qua cookies.get
        return "Your cookie is: " + request.cookies.get("tmp")
    except:
        return "There is no cookie!"


# Ngoài ra còn nhiều các phương thức khác như là PUT, PATCH,..
# Về cơ bản, ta quy định
# GET dùng để lây dữ liệu từ máy chủ
# POST dùng để thêm dữ liệu vào máy chủ
# PUT ghi đè dữ liệu
# PATCH cập nhật 1 phần dữ liệu
# DELETE xóa dữ liệu 

# Để lấy giá trị tham số trên query string
# ta dùng phương thức args.get của request
@app.route("/querystringExample")
def querystring_example() -> str:
    num: str | None = request.args.get('input')

    if num:
        return f"Your input is {num}"
    else:
        return "There is no input"


if __name__ == "__main__":
    # Chạy app
    app.run(debug=True, port=8000)
    # debug=True để mỗi khi có thay đổi trong file py
    # app sẽ tự reset
    # python.exe app.py


    # Ta có thể chỉnh cổng qua tham số port (mặc định là 5000)
    # app.run(port=8000)

    # Chỉnh ip thông qua host (mặc định là "127.0.0.1")
    # app.run(host="192.168.69.69")

    # Hoặc là chạy thông qua câu lệnh như sau (Không cần đặt trước host và port)
    # flask --app app.py run --host=192.168.69.69 --port=8000
    # hoặc
    # set FLASK_APP=app.py
    # flask run --host=192.168.69.69 --port=8000