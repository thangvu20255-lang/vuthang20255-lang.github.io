from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

# ====== DATABASE GIẢ LẬP ======
users = {
    "admin": {"password": "123456", "role": "admin"},
    "mod": {"password": "123456", "role": "mod"},
    "user": {"password": "123456", "role": "user"}
}

# ====== LOGIN UI (GIỮ NGUYÊN GIAO DIỆN CỦA BẠN) ======
def render_login(error=""):

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Đăng nhập</title>

<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Tahoma;}
body{display:flex;justify-content:center;align-items:center;min-height:100vh;background:#0f0f0f;overflow:hidden;}
.container{position:relative;width:450px;height:450px;display:flex;justify-content:center;align-items:center;}
.container i{position:absolute;inset:0;border:2px solid #fff;transition:0.5s;border-radius:20px;}
.container i:nth-child(1){ animation:animate 7s linear infinite; }
.container i:nth-child(2){ animation:animate 9s linear infinite; }
.container i:nth-child(3){ animation:animate2 12s linear infinite; }
.container:hover i{border:6px solid var(--clr);filter:drop-shadow(0 0 25px var(--clr));}
@keyframes animate{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}
@keyframes animate2{0%{transform:rotate(360deg);}100%{transform:rotate(0deg);}}
.login{position:absolute;width:320px;display:flex;flex-direction:column;gap:18px;}
.login h2{font-size:2em;color:#fff;text-align:center;}
.input-box input{width:100%;padding:12px 20px;background:rgba(255,255,255,0.05);border:2px solid #fff;border-radius:40px;font-size:1em;color:#fff;outline:none;}
.input-box input[type="submit"]{background:linear-gradient(45deg,#0078ff,#b153d7);border:none;cursor:pointer;font-weight:bold;}
.input-box input[type="submit"]:hover{background:linear-gradient(45deg,#7adaa5,#0078ff);box-shadow:0 0 20px #fff;}
.input-box input::placeholder{color:rgba(255,255,255,0.7);}
.error{color:#ff4d4d;text-align:center;font-size:14px;min-height:18px;}
.link{text-align:center;}
.link a{color:#7adaa5;text-decoration:none;font-size:14px;}
</style>
</head>

<body>
<div class="container">
<i style="--clr:#4ca0ff;"></i>
<i style="--clr:#7adaa5;"></i>
<i style="--clr:#b153d7;"></i>

<div class="login">
<h2>Đăng nhập</h2>
<div class="error">{{ error }}</div>

<form method="POST">
<div class="input-box">
<input type="text" name="username" placeholder="Username" required>
</div>

<div class="input-box">
<input type="password" name="password" placeholder="Password" required>
</div>

<div class="input-box">
<input type="submit" value="Sign In">
</div>
</form>

<div class="link">
<a href="#">Hệ thống phân quyền 3 cấp</a>
</div>
</div>
</div>
</body>
</html>
"""
    return render_template_string(html, error=error)

# ====== LOGIN ROUTE ======
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["role"] = users[username]["role"]
            return redirect("/dashboard")
        else:
            return render_login("Sai tài khoản hoặc mật khẩu")

    return render_login()

# ====== DASHBOARD THEO PHÂN QUYỀN ======
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    role = session.get("role")
    username = session.get("user")

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Dashboard</title>
<style>
body{margin:0;font-family:Tahoma;background:#f4f6f9;}
.topbar{background:#111827;color:white;padding:15px;display:flex;justify-content:space-between;}
.content{padding:30px;}
.card{background:white;padding:20px;border-radius:15px;box-shadow:0 4px 15px rgba(0,0,0,0.1);margin-bottom:20px;}
.admin{color:#ef4444;font-weight:bold;}
.mod{color:#f59e0b;font-weight:bold;}
.user{color:#10b981;font-weight:bold;}
a{color:white;text-decoration:none;background:#ef4444;padding:8px 15px;border-radius:8px;}
</style>
</head>
<body>

<div class="topbar">
<div>Xin chào {{ username }} ({{ role }})</div>
<div><a href="/logout">Logout</a></div>
</div>

<div class="content">

{% if role == "admin" %}
<div class="card admin">
<h2>ADMIN PANEL</h2>
<p>Toàn quyền quản lý hệ thống.</p>
<p>Có thể quản lý Admin / Mod / User</p>
</div>
{% elif role == "mod" %}
<div class="card mod">
<h2>MOD PANEL</h2>
<p>Quản lý user nhưng không được quản lý admin.</p>
</div>
{% else %}
<div class="card user">
<h2>USER PANEL</h2>
<p>Chỉ xem thông tin cá nhân.</p>
</div>
{% endif %}

</div>
</body>
</html>
"""
    return render_template_string(html, username=username, role=role)

# ====== LOGOUT ======
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
