from flask import Flask, render_template, url_for, request, session, redirect
from gevent.wsgi import WSGIServer
from pprint import pprint
from settings import *
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")

@app.route("/", methods=["GET", "POST"])
def home():
    # TODO: kyle - check if redirect is still a problem, if so shift to /ask
    session['data'] = dict(request.args)
    print json.dumps(session['data'], indent=4)
    return redirect(url_for("questions"))

@app.route("/questions")
def questions():
    # TODO: kyle
    #questions = get_questions(user_id, is_answered = False)
    return render_template("questions.html", data={})

@app.route("/answers")
def answers():
    # TODO: lily
    #questions = get_questions(user_id, is_answered=True)
    return render_template("answers.html", data={})

@app.route("/question_detail", methods=['GET', 'POST'])
def question_detail():
    # TODO: kyle
    if request.method == 'GET':
        # get means that you are viewing a question that has been posted but
        # not answered
        pass
        #args = dict(request.args)
        #question_obj = get_question(id)
        #return render_template('question.html', obj=question_obj)
        return render_template('question_detail.html', data={})
    elif request.method == 'POST':
        data = json.loads(request.data)
        pprint(data)
        question_title = data['title']
        assigned_to = data['assigned_to']
        new_question = {
            'question_title': question_title,
            'assigned_to': [],
            'is_answered': False,
            'answers': []
        }
        save_question(new_question)
        return "This is the question details page"

@app.route("/answer_detail", methods=['GET', 'POST'])
def answer_detail():
    # TODO: andre
    if request.method == 'GET':
        # q_id = request.args['id']
        #question = get_questions(q_id)
        return render_template("answer_detail.html", data={})
    elif request.method == 'POST':
        data = json.loads(request.data)
        q_id, body = data['id'], data['body']
        #question = get_questions(q_id)
        if len(question['answers']) == 0:
            question['answers'] = [question]
        else:
            question['answers'].append(question)
        question['is_answered'] = True
        save_question(question, q_id)
        return 'ok'

@app.route("/search")
def search():
    # TODO: ida
    # TODO: flock.js
    query = dict(request.args)['q']
    result = process_query(query)
    return json.dumps(result)

if __name__ == "__main__":
    http_server = WSGIServer(("", PORT), app)
    http_server.serve_forever()
