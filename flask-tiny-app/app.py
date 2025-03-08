from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  

# File paths 
USERS_FILE = "users.json"
POSTS_FILE = "posts.json"

#functions
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding users.json: {e}")
            flash("Lỗi khi tải dữ liệu người dùng. Vui lòng kiểm tra file users.json.", "error")
            return []
    return []

def save_users(users):
    with open(USERS_FILE, "w", encoding='utf-8') as f:
        json.dump(users, f, indent=4)

def load_posts():
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding posts.json: {e}")
            flash("Lỗi khi tải dữ liệu bài viết. Vui lòng kiểm tra file posts.json.", "error")
            return []
    return []

def save_posts(posts):
    with open(POSTS_FILE, "w", encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

# Routes
@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = next((u for u in load_users() if u['id'] == session['user_id']), None)
    if not user:
        flash("Người dùng không tồn tại. Vui lòng đăng nhập lại.", "error")
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if user['is_blocked']:
        flash("Tài khoản của bạn đã bị khóa.", "error")
        session.pop('user_id', None)
        return redirect(url_for('login'))
    
    # Load all users and create a mapping of author to user_id
    users = load_users()
    author_to_user_id = {u['email']: u['id'] for u in users}

    # Load all posts
    all_posts_data = load_posts()
    if not all_posts_data:
        flash("Không thể tải bài viết. File posts.json có thể bị lỗi.", "error")
        user_posts = []
        all_posts = []
    else:
        user_posts = [post for post in all_posts_data if 'author' in post and post['author'] == user['email']]
        user_posts.sort(key=lambda x: x['id'], reverse=True)
        all_posts = all_posts_data.copy()
        all_posts.sort(key=lambda x: x['id'], reverse=True)
    
    # Pagination
    per_page = 10
    total_user_posts = len(user_posts)
    total_user_pages = (total_user_posts + per_page - 1) // per_page
    start_user = (page - 1) * per_page
    end_user = start_user + per_page
    paginated_user_posts = user_posts[start_user:end_user]
    
    #all posts
    total_all_posts = len(all_posts)
    total_all_pages = (total_all_posts + per_page - 1) // per_page
    start_all = (page - 1) * per_page
    end_all = start_all + per_page
    paginated_all_posts = all_posts[start_all:end_all]
    
    # Debugging
    print(f"User: {user['email']}, Total user posts: {total_user_posts}, Total user pages: {total_user_pages}, Paginated user posts: {len(paginated_user_posts)}")
    print(f"Total all posts: {total_all_posts}, Total all pages: {total_all_pages}, Paginated all posts: {len(paginated_all_posts)}")
    
    return render_template(
        'index.html',
        user=user,
        user_posts=paginated_user_posts,
        total_user_pages=total_user_pages,
        all_posts=paginated_all_posts,
        total_all_pages=total_all_pages,
        page=page
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            if user['is_blocked']:
                flash("Tài khoản của bạn đã bị khóa.", "error")
                return redirect(url_for('login'))
            session['user_id'] = user['id']
            session['user_email'] = user['email']  # Lưu email vào session
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('index'))
        else:
            flash("Email hoặc mật khẩu không đúng.", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if any(u['email'] == email for u in users):
            flash("Email đã tồn tại.", "error")
            return redirect(url_for('register'))
        new_user = {
            "id": len(users) + 1,
            "email": email,
            "password": password,
            "role": "user",
            "is_blocked": False
        }
        users.append(new_user)
        save_users(users)
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash("Đăng xuất thành công.", "success")
    return redirect(url_for('login'))


#..