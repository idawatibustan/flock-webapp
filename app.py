from flask import Flask, render_template, url_for, request, session, redirect
from gevent.wsgi import WSGIServer
from settings import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")

@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("ask"))

@app.route("/ask")
def ask():
    return render_template("ask.html", data={})

@app.route("/answer")
def answer():
    return render_template("answer.html", data={})

if __name__ == "__main__":
    http_server = WSGIServer(("", PORT), app)
    http_server.serve_forever()
