from flask import Flask, render_template, url_for, request, session, redirect
from gevent.wsgi import WSGIServer
from settings import *
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")

@app.route("/", methods=["GET", "POST"])
def home():
    return redirect(url_for("ask"))

@app.route("/ask")
def ask():
    session["data"] = dict(request.args)
    print json.dumps(session["data"], indent=4)
    return render_template("ask.html", data={})

@app.route("/answer")
def answer():
    return render_template("answer.html", data={})

@app.route("/question")
def question():
    #args = dict(request.args)
    #question_obj = get_question(id) #TODO
    #return render_template('question.html', obj=question_obj)
    return "This is the question details page"

@app.route("/answer_modal")
def answer_modal():
	return render_template("answer_modal.html", data={})

@app.route("/search")
def search():
    result = {
      "results": {
        "category1": {
          "name": "Category 1",
          "results": [
            {
              "title": "Result Title",
              "url": "/optional/url/on/click",
              "image": "optional-image.jpg",
              "price": "Optional Price",
              "description": "Optional Description"
            },
            {
              "title": "Result Title",
              "url": "/optional/url/on/click",
              "image": "optional-image.jpg",
              "price": "Optional Price",
              "description": "Optional Description"
            }
          ]
        },
        "category2": {
          "name": "Category 2",
          "results": [
            {
              "title": "Result Title",
              "url": "/optional/url/on/click",
              "image": "optional-image.jpg",
              "price": "Optional Price",
              "description": "Optional Description"
            }
          ]
        }
      }
    }
    return json.dumps(result)

if __name__ == "__main__":
    http_server = WSGIServer(("", PORT), app)
    http_server.serve_forever()
