from flask import Flask, request, jsonify
from flask_cors import CORS
from gv_llmquery import *
import json
import time
from random import sample
app = Flask(__name__)
CORS(app)

chat_histories = {}
user_id = 1
name_ontology = 'VIPRIME'
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    start_time = time.time()
    
    relation = find_relation(onto)
    # # Phương pháp 0
    entities = find_entities_from_question_PP0(relation,user_message)
    print(entities)
    # # Phương pháp 1:
    # # entities_with_annotation_sumarry = get_entities_with_annotation(onto, 'tom_tat')
    # # explication = create_explication(entities_with_annotation_sumarry)
    # # entities = find_entities_from_question_PP1(relation,explication,question)
    # # print(entities)

    # # Phương pháp 2:
    # k_entity_names = find_entities_from_question_PP2(onto, model_embedding)
    # print(k_entity_names)
    # entities = classify_entities(onto, k_entity_names)
    # print(entities)
    # entities = json.dumps(entities)
    list_query = create_query(name_ontology, json.loads(entities) )
    list_url = find_url(name_ontology, json.loads(entities))
    if len(list_url) > 0:
        list_url = sample(list_url, 3)

    result_from_ontology = find_question_info(name_ontology, list_query)
    raw_informations_from_ontology = []
    for result in result_from_ontology:
      if str(result[1]) not in ["all_info_embeddings", "summary_embeddings"]:
        print(result)
        raw_informations_from_ontology.append(result)
    k_similar_info = find_similar_info_from_raw_informations(user_message, raw_informations_from_ontology)
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    bot_response = generate_response(relation , k_similar_info, user_message, chat_histories[user_id])
    end_time = time.time()
    print("Thời gian thực thi:", end_time - start_time, "giây")

    

    chat_histories[user_id].append({"sender": "user", "text": user_message})
    chat_histories[user_id].append({"sender": "bot", "text": bot_response})

    # Thay bằng xử lý thực tế
    return jsonify({"response": bot_response,
                    "link": list_url
                    })

if __name__ == "__main__":
    app.run(debug=True)
