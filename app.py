from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Xin chào! Web Python của tôi đây!</h1>"

if __name__ == "__main__":
    app.run()
