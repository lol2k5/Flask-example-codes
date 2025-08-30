# Tính năng template render template thực chất trả về 1 xâu 
# với dữ liệu lấy từ 1 hoặc các file trong thư mục templates
# sử dụng thư viện Jinja template
from flask import Flask, render_template


app: Flask = Flask(__name__)


# Như đã nói từ trước, ta có render 1 file html thông qua hàm
# render_template, ở đây file html là 1 template
@app.route("/")
def index() -> str:
    return render_template("index.html")


# Thư viện Jinja template còn cho ta chỉnh sửa các template thông 
# qua các tham số trong template, cho phép template có thể được
# render dưới nhiều dạng khác nhau 
@app.route("/example1/<n>")
def example_1(n: str) -> str:
    return render_template("example1.html", name=n)
    # Ta truyền giá trị của n cho tham số name của template
    # Xem file example1.html


# Ngoài ra, ta còn có thể kế thừa các template với nhau, tức là thay 
# vì ta phải viết nhiều template giống nhay thì ta có thể lấy 1 
# template chung và các template phụ chỉ cần dùng lại, giúp tiếp 
# kiệm thời gian và công sức
@app.route("/example2")
def example_2() -> str:
    return render_template("example2.html")

@app.route("/example3")
def example_3() -> str:
    return render_template("example3.html") 


# Jinja còn cung cấp các dạng block hoạt động như vòng lặp hay if-else
@app.route("/example4/<pas>")
def example_4(pas: str) -> str:
    return render_template("example4.html", password=pas)

@app.route("/example5")
def example_5() -> str:
    pages_list: list[str]=["/", "/example2", "/example3", ]
    return render_template("example5.html", pages=pages_list) 


# Ngoài lề 1 chút, ta có thể thêm các trang từ các thư mục khác mà cùng
# nằm chung thư mục với ứng dụng, thường thì ta đặt cho các file như vậy
# trong thư mục static
@app.route("/staticExample")
def static_example() -> str:
    return render_template("staticExample.html")


if __name__ == "__main__":
    app.run(debug=True)