from flask import Flask, render_template, url_for, request, session, redirect
from gevent.wsgi import WSGIServer
from pprint import pprint
from settings import *
from helper import *
from fuzzywuzzy import fuzz
import requests
import os
import uuid
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).encode("hex")
powersearch = Powersearch()

@app.route("/", methods=["GET", "POST"])
def home():
    # TODO: check why redirect urls don't fucking work
    session['data'] = dict(request.args)
    print json.dumps(session['data'], indent=4)
    return redirect(url_for("questions"))

@app.route("/questions")
def questions():
    try:
        data = dict(request.args)
        data["flockEvent"] = json.loads(data['flockEvent'][0])
        session['data'] = data
    except:
        pass
    params = { 'is_answered': True }
    questions = get_questions(params)
    return render_template("questions.html", data=questions)

@app.route("/answers")
def answers():
    params = { 'is_answered': False }
    questions = get_questions(params)
    return render_template("answers.html", data=questions)

@app.route("/question_detail", methods=['GET', 'POST'])
def question_detail():
    if request.method == 'GET':
        q_id = dict(request.args)['id'][0]
        if q_id == "0000":
            question_title = dict(request.args)['title'][0]
            assigned_to = ['Engineering','Marketing','Human Resources']
            q_id = str(uuid.uuid4())
            new_question = {
                'question_title': question_title,
                'assigned_to': assigned_to,
                'is_answered': False,
                'answers': [],
                'rank': 0,
                'q_id': q_id,
                'asker_id': session["data"]["flockEvent"]["userId"]
            }
            save_question(new_question)
            new_question['event_name'] = 'question.assign'
            r = requests.post('http://45.55.9.70:8080/{}'.format('floqdoc'), data=json.dumps(new_question))
            return questions()
        else:
            params = { 'q_id': q_id }
            question = get_questions(params)[0]
            return render_template('question_detail.html', data=question)
    elif request.method == 'POST':
        data = json.loads(request.data)
        pprint(data)
        question_title = data['title']
        assigned_to = data['assigned_to']
        # session_data = json.loads(session['data']['flockEvent'][0])
        q_id = str(uuid.uuid4())
        new_question = {
            'question_title': question_title,
            'assigned_to': assigned_to,
            'is_answered': False,
            'answers': [],
            'rank': 0,
            'q_id': q_id,
            'asker_id': session["data"]["flockEvent"]["userId"]
        }
        save_question(new_question)
        # return redirect(url_for('questions'))
        I#return redirect(url_for("questions"))
        return questions()
        #return redirect(url_for("questions"))


@app.route("/answer_detail", methods=['GET', 'POST'])
def answer_detail():
    if request.method == 'GET':
        params = { 'q_id': request.args['id'] }
        question = get_questions(params)
        return render_template("answer_detail.html", data=question)
    elif request.method == 'POST':
        answer = request.form['answer']
        q_id, body = request.args['id'], answer
        params = { 'q_id': q_id }
        question = get_questions(params)[0]
        question['answers'] += [body]
        question['is_answered'] = True
        save_question(question)
        question['event_name'] = 'question.answered'
        r = requests.post('http://45.55.9.70:8080/{}'.format('floqdoc'), data=json.dumps(question))
        return answers()
        # return render_template("answers.html")

@app.route("/search")
def search():
    query = dict(request.args)['q'][0]
    powersearch.update(query)
    result = powersearch.get_results()
    print "hello" , result
    return json.dumps(result)

if __name__ == "__main__":
    http_server = WSGIServer(("", PORT), app)
    print 'Listening on port', PORT
    http_server.serve_forever()
