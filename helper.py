def get_questions(q_id=None):
    # TODO: andre - get from database
    # TODO: find all filter conditions, question_id, user_id, is_answered
    questions = json.loads(open('json/questions.json').read())
    if q_id:
        return questions[q_id]
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
