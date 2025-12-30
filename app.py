from flask import Flask, request, redirect, session, jsonify
import requests
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 配置
TARGET_URL = os.getenv('TARGET_URL', 'https://example.com')
ALLOWED_EMAILS = set(os.getenv('ALLOWED_EMAILS', '').split(','))

# 简单的密码验证（比OAuth简单）
PASSWORD = "grandma123"  # 您可以改成自己喜欢的密码

def check_auth(email, password):
    """检查邮箱和密码"""
    return email in ALLOWED_EMAILS and password == PASSWORD

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    """重定向到目标网站"""
    return redirect(TARGET_URL)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        if check_auth(email, password):
            session['logged_in'] = True
            session['email'] = email
            return redirect('/')
        else:
            return "登录失败，请检查邮箱和密码", 401
    
    # 显示登录表单
    return '''
    <html>
    <head>
        <title>数据库访问登录</title>
        <style>
            body { font-family: Arial; padding: 50px; max-width: 400px; margin: auto; }
            input { width: 100%; padding: 10px; margin: 10px 0; }
            button { background: blue; color: white; padding: 10px 20px; border: none; }
        </style>
    </head>
    <body>
        <h2>🔒 数据库访问登录</h2>
        <form method="POST">
            <input type="email" name="email" placeholder="您的邮箱" required><br>
            <input type="password" name="password" placeholder="密码" required><br>
            <button type="submit">登录</button>
        </form>
        <p><small>密码：grandma123（请告诉同事）</small></p>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    return redirect('/login')

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({"status": "healthy", "service": "db-proxy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
