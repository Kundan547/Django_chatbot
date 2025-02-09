from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches
import os

app = Flask(__name__)

learning_state = {"is_learning": False, "last_question": None}

# Load the knowledge base
def load_knowledge_base():
    if not os.path.exists('knowledge_base.json'):
        return {"questions": []}
    with open('knowledge_base.json', 'r') as file:
        return json.load(file)

# Save the new question-answer pair to the knowledge base
def save_to_knowledge_base(new_question, new_answer):
    knowledge_base = load_knowledge_base()
    knowledge_base["questions"].append({"question": new_question, "answer": new_answer})
    with open('knowledge_base.json', 'w') as file:
        json.dump(knowledge_base, file, indent=4)

# Normalize for matching
def normalize(text):
    return text.lower().strip()

# Find the best match
def find_best_match(user_question, questions):
    normalized_questions = [normalize(q) for q in questions]
    matches = get_close_matches(normalize(user_question), normalized_questions, n=1, cutoff=0.5)
    return matches[0] if matches else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    global learning_state
    user_input = request.json.get('message')
    knowledge_base = load_knowledge_base()

    if learning_state["is_learning"]:
        # Save the user response as the answer to the previous question
        save_to_knowledge_base(learning_state["last_question"], user_input)
        learning_state = {"is_learning": False, "last_question": None}
        return jsonify({"response": "Thank you! I've learned something new."})

    # Find the best match for the user input
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

    if best_match:
        # Return the answer for the best match
        answer = next(q["answer"] for q in knowledge_base["questions"] if normalize(q["question"]) == best_match)
        return jsonify({"response": answer})
    else:
        # Ask the user to teach the bot
        learning_state = {"is_learning": True, "last_question": user_input}
        return jsonify({"response": "I don't know the answer. Can you teach me the correct response?"})

if __name__ == "__main__":
    app.run(debug=True)
