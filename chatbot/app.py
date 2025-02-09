from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

# Load the knowledge base
def load_knowledge_base():
    with open('knowledge_base.json', 'r') as file:
        return json.load(file)

# Find the best match with case-insensitive comparison
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question.lower(), [q.lower() for q in questions], n=1, cutoff=0.6)
    return matches[0] if matches else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.json.get('message')
    knowledge_base = load_knowledge_base()

    # Ensure user input is normalized
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
    
    if best_match:
        # Return the answer corresponding to the best match
        answer = next(q["answer"] for q in knowledge_base["questions"] if q["question"].lower() == best_match.lower())
        return jsonify({"response": answer})
    else:
        return jsonify({"response": "I don't know the answer. Can you teach me?"})

if __name__ == "__main__":
    app.run(debug=True)
