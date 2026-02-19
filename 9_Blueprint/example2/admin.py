from flask import Blueprint, render_template

# Xét 1 số các tham số khác  
admin_bp = Blueprint(
    'admin',                              # Tên blueprint
    __name__,                             # Vị trí module hiện tại
    url_prefix='/dashboard',              # Mọi URL sẽ bắt đầu bằng /dashboard
    # subdomain='manager',                # Chỉ chạy trên subdomain "manager", sẽ chạy local nên tạm bỏ
    template_folder='admin_templates',    # Thư mục chứa HTML riêng: ./admin_templates
    static_folder='admin_static',         # Thư mục vật lý chứa CSS/JS: ./admin_static
    static_url_path='/files_admin'        # URL trên web để truy cập file tĩnh
)


@admin_bp.route('/')
def dashboard():
    # Sẽ load file HTML từ thư mục 'admin_templates'
    # Truy cập thực tế tr http://manager.yourdomain.com/dashboard/
    return render_template('index.html')


@admin_bp.route('/settings')
def settings():
    # URL thực tế: http://manager.yourdomain.com/dashboard/settings
    return "Trang cài đặt"