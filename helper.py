from fuzzywuzzy import fuzz
import time
import json

def get_questions(params=None):
    # takes in asker_id, q_id, and is_answered as param keys
    questions = json.loads(open('json/questions.json').read())
    if params and type(params) == dict:
        for param, val in params.iteritems():
            questions = { q_id: obj for q_id, obj in questions.iteritems() if obj[param] == val }
    questions = [v for v in questions.values()]
    questions = sorted(questions, key=lambda x: x['rank'], reverse=True)
    return questions

def process_query(query):
    all_questions = get_questions()
    result = []
    for question in all_questions:
        if search_condition_fulfilled:
            result.append(question)

    sorted(result, key=lambda x: compare_key)

    # the below is the desired format for the results
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
    return results

def save_question(q_obj):
    questions = json.loads(open('json/questions.json').read())
    q_id = q_obj['q_id']
    assert set(['is_answered', 'rank', 'q_id', 'question_title', 'answers', 'asker_id', 'assigned_to']) == set(q_obj.keys())
    questions[q_id] = q_obj
    open('json/questions.json', 'w').write(json.dumps(questions, indent=4))

class Powersearch:
    def __init__(self):
        self.questions = {}
        self.scores = {}
        self.num_words = 0
        self.query = ''

    def _reload_questions(self):
        self.questions = json.loads(open('json/questions.json').read())

    def _set_score(self, _id, score):
        self.scores[_id] = score

    def _enrich(self, obj, to_answer):
        _id, score = obj
        base_url = 'answer_detail' if to_answer else 'question_detail'
        d = {
            "title": self.questions[_id]['question_title'],
            "url": "/{}?id={}".format(base_url, _id),
            "description": ', '.join(self.questions[_id]['assigned_to'])
        }
        return d

    def update(self, query):
        self.query = query
        if not self.questions:
            self._reload_questions()
        self.num_words = len(query[0].split(' '))
        for _id, q in self.questions.iteritems():
            score = fuzz.token_sort_ratio(query, q['question_title'])
            self._set_score(_id, score)

    def get_results(self, top=3):
        answered, unanswered = [], []
        threshold = self.num_words * 5
        for _id, q in self.questions.iteritems():
            score = self.scores[_id]
            print score, threshold, q['question_title']
            if score > threshold:
                if q['is_answered']:
                    answered.append((_id, score))
                else:
                    unanswered.append((_id, score))
        answered = sorted(answered, key=lambda x: x[1], reverse=True)[:top]
        answered = [self._enrich(i, False) for i in answered]
        unanswered = sorted(unanswered, key=lambda x: x[1], reverse=True)[:top]
        unanswered = [self._enrich(i, True) for i in unanswered]
        result = {
            "results": {
                "answered": {
                    "name": "Answered",
                    "results": answered
                },
                "unanswered": {
                    "name": "Unanswered",
                    "results": unanswered
                },
                "submit": {
                    "name": "New Question",
                    "results": [
                        {
                          "title": self.query,
                          "url": "/question_detail?id=0000&title="+str(self.query),
                          "description": "Click to submit"
                        }
                    ]
                },
            }
        }
        return result
