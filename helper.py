def get_questions(params=None):
    # takes in asker_id, q_id, and is_answered as param keys
    questions = json.loads(open('json/questions.json').read())
    if params:
        for param, val in params.iteritems():
            questions = [question for question in questions if question[param] == val]
        sophisticated_sort(res)
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

def save_question(q_obj, q_id = None):
    # TODO: andre
    questions = json.loads(open('json/questions.json').read())
    if not q_id:
        q_id = create_id() # can just use unix timestamp converted to string
    questions[q_id] = q_obj
    open('json/questions.json', 'w').write(json.dumps(questions, indent=4))
