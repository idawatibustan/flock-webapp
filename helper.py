from fuzzywuzzy import fuzz
import json

def get_questions(params=None):
    # takes in asker_id, q_id, and is_answered as param keys
    questions = json.loads(open('json/questions.json').read())
    if params:
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

    def _reload_questions(self):
        self.questions = json.loads(open('json/questions.json').read())

    def _reinitialize(self):
        self.scores = {}
        self.num_words = 0

    def _enrich(self, obj):
        _id, score = obj.items()
        d = {
            "title": self.questions[_id]['question_title'],
            "url": "/questions/{}".format(_id),
            "description": ', '.join(self.questions[_id]['assigned_to'])
        }
        return d

    def update(self, query):
        if not self.questions:
            self._reload_questions()
            if query == '':
                self._reinitialize()
            else:
                self.num_words = len(query.split(' '))
                for _id, q in self.questions.iteritems():
                    self.scores[_id] = fuzz.token_sort_ratio(query, q['question_title'])

    def get_results(self, top=3):
        answered, unanswered = [], []
        threshold = self.num_words * 5
        for _id, q in self.questions.iteritems():
            score = self.scores[_id]
            if score > threshold:
                if q['is_answered']:
                    answered.append((_id, score))
                else:
                    unanswered.append((_id, score))
        answered = sorted(answered, key=lambda x: x[1], reverse=True)[:top]
        answered = [self._enrich(i) for i in answered]
        unanswered = sorted(unanswered, key=lambda x: x[1], reverse=True)[:top]
        unanswered = [self._enrich(i) for i in unanswered]
        result = {
            "results": {
                "answered": {
                    "name": "Answered",
                    "results": answered
                },
                "unanswered": {
                    "name": "Unanswered",
                    "results": unanswered
                }
            }
        }
