from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

# ====== DATABASE GIẢ LẬP ======
users = {
    "admin": {"password": "123456", "role": "admin"},
    "mod": {"password": "123456", "role": "mod"},
    "user": {"password": "123456", "role": "user"}
}

# ================= LOGIN UI =================
def render_login(error=""):
    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
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
<a href="/register">Chưa có tài khoản? Đăng ký</a>
</div>
</div>
</div>
</body>
</html>
"""
    return render_template_string(html, error=error)


# ================= REGISTER UI =================
def render_register(error=""):
    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Đăng ký</title>
<style>
body{display:flex;justify-content:center;align-items:center;height:100vh;background:#111;color:white;font-family:Tahoma;}
.box{background:#1f2937;padding:30px;border-radius:15px;width:320px;}
input{width:100%;padding:10px;margin:10px 0;border:none;border-radius:8px;}
button{width:100%;padding:10px;background:#10b981;border:none;border-radius:8px;color:white;font-weight:bold;}
.error{color:#ef4444;text-align:center;}
a{color:#7adaa5;text-decoration:none;}
</style>
</head>
<body>
<div class="box">
<h2 style="text-align:center;">Đăng ký</h2>
<div class="error">{{ error }}</div>

<form method="POST">
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Tạo tài khoản</button>
</form>

<p style="text-align:center;margin-top:10px;">
<a href="/">Quay lại đăng nhập</a>
</p>
</div>
</body>
</html>
"""
    return render_template_string(html, error=error)


# ================= LOGIN =================
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


# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_register("Tài khoản đã tồn tại")

        users[username] = {
            "password": password,
            "role": "user"  # mặc định user
        }

        return redirect("/")

    return render_register()


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    role = session.get("role")
    username = session.get("user")

    return f"""
    <h1>Xin chào {username}</h1>
    <h2>Role: {role}</h2>
    <a href='/logout'>Logout</a>
    """


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
