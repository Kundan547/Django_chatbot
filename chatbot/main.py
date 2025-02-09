import json
from difflib import get_close_matches
from typing import List, Optional, Dict  # For type hints

# Load the knowledge base from a JSON file.
def load_knowledge_base(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Save the knowledge base to a JSON file.
def save_knowledge_base(file_path: str, data: Dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the best match for user input from the knowledge base.
def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None

# Get the answer for a question from the knowledge base.
def get_answer_for_question(question: str, knowledge_base: Dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# The main chatbot function.
def chatbot():
    knowledge_base = load_knowledge_base('knowledge_base.json')
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == "quit":
            print("Bot: Goodbye!")
            break
        
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer = input('Type the answer or "skip" to skip: ')
            
            if new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you! I learned a new response!")

if __name__ == "__main__":
    chatbot()
