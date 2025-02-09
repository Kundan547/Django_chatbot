import json
from difflib import get_close_matches

# Load the knowledge base from a JSON file.
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

#Save the knowledge base from a json file.

def save_knowledge_base(file_path: str, data:dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
        
        
# Find the best match for user from knowledge based from json file.

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None