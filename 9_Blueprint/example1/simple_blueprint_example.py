from flask import Blueprint


# Cấu tạo 1 blueprint cơ bản
simple_example = Blueprint("simple_example", __name__, template_folder="templates", url_prefix="/pages")
# Có khai báo đường dẫn template, đó chính là thư mục mà nó sẽ dùng để 
# lấy templates, ngoài ra còn tham số url prefix, mọi đường dẫn được 
# tạo trong blueprint đều có đầu là nó
#
# Tham số đầu tiên là tham số tên, cái này sẽ xác định tên của blueprint,
# được sự dụng có các hàm như url_for
# Cái tiếp theo là tên của module chứa Blueprint này, nó khá phức tạp để
# giải thích cho người mới nên hiện tại, hãy hiểu là hầu như ta sẽ dùng giá trị 
# __name__


# Tạo đường dẫn cho blue print
@simple_example.route("/")
@simple_example.route("/<page>")
def show_page(page : str = "index") -> str:
    return f"This is {page} page!"