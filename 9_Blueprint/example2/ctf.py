from flask import Blueprint, render_template


ctf_bp = Blueprint(
    'ctf', 
    __name__, 
    url_prefix='/ctf',
    template_folder='ctf_templates',
    static_folder='ctf_static',
    static_url_path='/files_ctf'
)


@ctf_bp.route('/')
def challenges():
    return render_template('index.html')