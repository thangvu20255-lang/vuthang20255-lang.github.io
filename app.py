from flask import Flask, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, join_room, leave_room, emit
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

socketio = SocketIO(app, cors_allowed_origins="*")

DATABASE = "users.db"

# ====== GAME ROOMS ======
rooms = [
    {"id": 1, "players": [], "max": 4},
    {"id": 2, "players": [], "max": 4},
]

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    hashed = generate_password_hash(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              (username, hashed))
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
        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Sai tài khoản hoặc mật khẩu!"

    return render_login(error)

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    room_html = ""
    for room in rooms:
        room_html += f"""
        <div style='border:1px solid #444;padding:15px;margin:10px'>
            <h3>Room {room['id']}</h3>
            <p>Người chơi: {len(room['players'])}/{room['max']}</p>
            <button onclick="joinRoom({room['id']})">Vào phòng</button>
        </div>
        """

    return f"""
    <h2>Xin chào {session['user']} 👋</h2>
    <h3>🎮 SẢNH CHỜ</h3>
    {room_html}
    <br><a href='/logout'>Đăng xuất</a>

    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <script>
    const socket = io();

    function joinRoom(roomId) {{
        socket.emit("join_room", {{
            username: "{session['user']}",
            room: roomId
        }});
    }}

    socket.on("user_joined", function(data) {{
        alert(data.msg);
    }});

    socket.on("user_left", function(data) {{
        alert(data.msg);
    }});
    </script>
    """

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

# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ================= SOCKET EVENTS =================
@socketio.on("join_room")
def handle_join(data):
    username = data["username"]
    room_id = data["room"]

    room_name = f"room_{room_id}"
    join_room(room_name)

    emit("user_joined", {
        "msg": f"{username} đã vào phòng {room_id}"
    }, to=room_name)

# ================= LOGIN UI =================
def render_login(error):
    return f"""
    <h2>Đăng nhập</h2>
    <div style='color:red'>{error}</div>
    <form method="POST">
        <input name="username" required><br>
        <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    <a href="/register">Đăng ký</a>
    """

# ================= RUN =================
if __name__ == "__main__":
    init_db()
    socketio.run(app, debug=True)
