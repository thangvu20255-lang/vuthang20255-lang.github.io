from flask import Flask, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_123"
DATABASE = "users.db"

# ====== GAME ROOMS ======
rooms = [
    {"id": 1, "players": ["thangvu", "user2"], "max": 4},
    {"id": 2, "players": ["user3"], "max": 4},
    {"id": 3, "players": [], "max": 4},
]

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            locked INTEGER DEFAULT 0
        )
    """)

    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        admin_pass = generate_password_hash("admin123")
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", admin_pass, "admin")
        )

    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user


def get_all_users():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, username, role, locked FROM users")
    users = c.fetchall()
    conn.close()
    return users


def create_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    hashed = generate_password_hash(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              (username, hashed))
    conn.commit()
    conn.close()


def toggle_lock(user_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute(
        "UPDATE users SET locked = CASE locked WHEN 0 THEN 1 ELSE 0 END WHERE id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if user:
            if user[4] == 1:
                error = "Tài khoản đã bị khoá!"
            elif check_password_hash(user[2], password):
                session["user"] = username
                session["role"] = user[3]
                return redirect(url_for("dashboard"))
            else:
                error = "Sai mật khẩu!"
        else:
            error = "Tài khoản không tồn tại!"

    return render_login(error)

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    # ADMIN PAGE
    if session["role"] == "admin":
        users = get_all_users()

        rows = ""
        for u in users:
            action = "🔒 Khoá" if u[3] == 0 else "🔓 Mở"
            status = "Hoạt động" if u[3] == 0 else "Bị khoá"

            rows += f"""
            <tr>
                <td>{u[1]}</td>
                <td>{u[2]}</td>
                <td>{status}</td>
                <td><a href='/toggle/{u[0]}'>{action}</a></td>
            </tr>
            """

        return f"""
        <h2 style='text-align:center;'>Trang Admin 👑</h2>
        <table border='1' cellpadding='10' style='margin:auto;'>
            <tr>
                <th>Username</th>
                <th>Role</th>
                <th>Trạng thái</th>
                <th>Hành động</th>
            </tr>
            {rows}
        </table>
        <br><div style='text-align:center;'><a href='/logout'>Đăng xuất</a></div>
        """

    # USER PAGE (SẢNH CHỜ)
    room_html = ""
    for room in rooms:
        room_html += f"""
        <div style='border:1px solid #444;padding:15px;margin:10px'>
            <h3>Room {room['id']}</h3>
            <p>Người chơi: {len(room['players'])}/{room['max']}</p>
            <p>Danh sách: {room['players']}</p>
            <a href='/join/{room['id']}'>Vào phòng</a>
        </div>
        """

    return f"""
    <h2 style='text-align:center;'>Xin chào {session['user']} 👋</h2>
    <div style='text-align:center;'>
    <h3>🎮 SẢNH CHỜ</h3>
    {room_html}
    <br><a href='/logout'>Đăng xuất</a>
    </div>
    """

# ================= JOIN ROOM =================
@app.route("/join/<int:room_id>")
def join_room(room_id):
    if "user" not in session:
        return redirect(url_for("login"))

    for room in rooms:
        if room["id"] == room_id:
            if session["user"] not in room["players"] and len(room["players"]) < room["max"]:
                room["players"].append(session["user"])
            break

    return redirect(url_for("dashboard"))

# ================= TOGGLE LOCK =================
@app.route("/toggle/<int:user_id>")
def toggle(user_id):
    if "role" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    toggle_lock(user_id)
    return redirect(url_for("dashboard"))

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if get_user(username):
            error = "Tài khoản đã tồn tại!"
        else:
            create_user(username, password)
            return redirect(url_for("login"))

    return render_login(error).replace("Đăng nhập", "Đăng ký")

# ================= SIMPLE LOGIN UI =================
def render_login(error):
    return f"""
    <h2>Đăng nhập</h2>
    <div style='color:red'>{error}</div>
    <form method="POST">
        <input name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <input type="submit" value="Login">
    </form>
    <a href="/register">Đăng ký</a>
    """

# ================= RUN =================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
