 def render_login(error):

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>

<style>
*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Tahoma, Geneva, Verdana, sans-serif;
}

body{
display:flex;
justify-content:center;
align-items:center;
min-height:100vh;
background:#111;
overflow:hidden;
}

.container{
position:relative;
width:450px;
height:450px;
display:flex;
justify-content:center;
align-items:center;
}

.container i{
position:absolute;
inset:0;
border:2px solid #fff;
transition:0.5s;
}

.container i:nth-child(1){ animation:animate 7s linear infinite; }
.container i:nth-child(2){ animation:animate 9s linear infinite; }
.container i:nth-child(3){ animation:animate2 12s linear infinite; }

.container:hover i{
border:6px solid var(--clr);
filter:drop-shadow(0 0 20px var(--clr));
}

@keyframes animate{
0%{ transform:rotate(0deg); }
100%{ transform:rotate(360deg); }
}

@keyframes animate2{
0%{ transform:rotate(360deg); }
100%{ transform:rotate(0deg); }
}

.login{
position:absolute;
width:300px;
display:flex;
flex-direction:column;
gap:20px;
}

.login h2{
font-size:2em;
color:#fff;
text-align:center;
}

.input-box input{
width:100%;
padding:12px 20px;
background:transparent;
border:2px solid #fff;
border-radius:40px;
font-size:1.1em;
color:#fff;
outline:none;
}

.input-box input[type="submit"]{
background:linear-gradient(45deg,#0078ff,#b153d7);
border:none;
cursor:pointer;
}

.input-box input[type="submit"]:hover{
background:linear-gradient(45deg,#7adaa5,#0078ff);
box-shadow:1px 1px 20px 1px #fff;
}

.input-box input::placeholder{
color:rgba(255,255,255,0.75);
}

.error{
color:red;
text-align:center;
}

.link{
text-align:center;
}

.link a{
color:#7adaa5;
text-decoration:none;
}
</style>
</head>

<body>

<div class="container">
<i style="--clr:#4ca0ff;"></i>
<i style="--clr:#7adaa5;"></i>
<i style="--clr:#b153d7;"></i>

<div class="login">
<h2>Đăng nhập</h2>

<div class="error">{error}</div>

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
<a href="/register">Đăng ký tài khoản</a>
</div>

</div>
</div>

</body>
</html>
"""

    return html.replace("{error}", error)   
