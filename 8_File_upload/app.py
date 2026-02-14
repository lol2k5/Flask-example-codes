from flask import Flask, render_template, request, abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from os import getcwd, path, remove
from string import ascii_letters, digits
from filetype import guess
from random import randint, choice


app = Flask(__name__)
app.config["UPLOAD_PATH"] = getcwd() + r"\storage"
# getcwd để lấy thư mục hiện tại, quy định nơi chứa các file


@app.route("/type1", methods=["GET", "POST"])
def type1() -> str:
    """
    Loại 1, cơ bản nhất, chỉ lấy 1 file nào đó và đưa lên máy chủ
    chỉ sử dụng hàm secure_filename để bảo vệ.
 
    :return: Phản hồi
    :rtype: str
    """

    if request.method == "GET":
        return render_template("type1.html")
    else:
        if "file" in request.files:
            upload_file: FileStorage = request.files["file"]
            if upload_file.name != '':
                upload_file.save(path.join(app.config["UPLOAD_PATH"], secure_filename(upload_file.filename)))
        
        return render_template("type1.html")


@app.route("/type2", methods=["GET", "POST"])
def type2() -> str:
    """
    Loại có sử dung thư viện ngoài tại frontend
    
    :return: Phản hồi
    :rtype: str
    """

    if request.method == "GET":
        return render_template("type2.html")
    else:
        if "file" in request.files:
            upload_file: FileStorage = request.files["file"]
            if upload_file.name != '':
                upload_file.save(path.join(app.config["UPLOAD_PATH"], secure_filename(upload_file.filename)))
        
        return render_template("type2.html")


# Cấu hình độ lớn cao nhất của 1 file, ở đây nghĩa là không quá 1 MB
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
# 1 loạt các đuôi file mà sẽ dùng để làm whitelist
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.gif']
# Phần thư mục phụ, đây là file được kiểm tra
app.config["TEMP_DIR"] = getcwd() + r"\temp"
# Phần kí tự cho việc tạo xâu ngẫu nhiên
app.config["WORDLIST"] = ascii_letters + digits


def validate_image(filepath: str) -> bool:
    """
    Kiểm tra xem có phải file ảnh thông qua nội dung
    
    :param filepath: Description
    :type filepath: str
    :return: Description
    :rtype: bool
    """

    # Đoán loại
    file_type = guess(filepath)

    # Nếu không thuộc loại mine thì không cho lưu file
    if file_type == None or not file_type.is_mime:
        return False
    
    # Kiểm tra loại file
    mine_type: str = file_type.mime

    # Nếu là ảnh thì cho vào
    if mine_type.startswith("image/"):
        return True
    else:
        return False


@app.route("/type3", methods=["GET", "POST"])
def type3() -> str:
    """
    Y chang type 1 nhưng thêm 1 số chức năng bảo vệ.
    
    :return: Phản hồi
    :rtype: str
    """

    # Chỉ khi là POST và có ảnh trong yêu cầu
    if request.method == "POST" and "file" in request.files:
        upload_file: FileStorage = request.files["file"]
        
        # Lấy tập các đuôi file
        file_exts = upload_file.filename.split()[1:]

        # Chỉ cần có đuôi không hợp lệ
        if any(ext not in app.config["UPLOAD_EXTENSIONS"] for ext in file_exts):
            abort(400)
        
        # Cho lọc tên file
        secured_filename = secure_filename(upload_file.filename)

        # Chỉ cần 2 tên file sau lọc không trống
        if upload_file.name and secured_filename:
            # Tạo 1 đường dẫn file ngẫu nhiên gồm kí tự và chữ số, dài từ 10 đến 15 ký tự
            random_len = randint(10, 15)
            random_filename = ''.join(choice(app.config["WORDLIST"]) for _ in range(random_len))
            random_path = path.join(app.config["TEMP_DIR"], random_filename)
            
            # Lựu tạm file vào đường dẫn ngẫu nhiên
            upload_file.save(random_path)

            # Kiểm tra lại qua nội dung, nếu được mới cho lưu
            if validate_image(random_path):
                upload_file.save(path.join(app.config["UPLOAD_PATH"], secured_filename))
            
            # Sau đó xóa file tạm
            remove(random_path)
        
        # Như bình thường thì trả về 
        return render_template("type3.html")


# flask --app app.py run --host '192.168.69.69' --port 8000
# hoặc
# set FLASK_APP=app.py
# flask run --host 192.168.69.69 --port 8000