import json

from spellchecker import SpellChecker

from models import Experience, Education, Skill

def load_data(filename):
    """
    Using dataclasses to serialize and deserialize JSON data, this forms a "layer" between the data and the application.
    Saving and loading data from a JSON file
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return {
            "experience": [Experience(**exp) for exp in data.get('experience', [])], 
            "education": [Education(**edu) for edu in data.get('education', [])],
            "skill": [Skill(**skl) for skl in data.get('skill', [])]
        }
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {"experience": [], "education": [], "skill": []}  
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return {"experience": [], "education": [], "skill": []}

def save_data(filename, data):
    """
    This function writes the data to a JSON file. First it converts the data to a dictionary, then writes it to the file.
    """
    try:
        with open(filename, 'w') as file:
            json_data = {
                "experience": [exp.__dict__ for exp in data['experience']],
                "education": [edu.__dict__ for edu in data['education']],
                "skill": [skl.__dict__ for skl in data['skill']]
            }
            json.dump(json_data, file, indent=4)
    except IOError as e:
        print(f"An error occurred while writing to {filename}: {e}")

def generate_id(data, model):
    """
    Generate a new ID for a model
    """
    if data[model]:
        return max(item.id for item in data[model] if item.id is not None) + 1
    return 1

def correct_spelling(text):
    '''Corrects the spelling of the given text'''
    spell = SpellChecker()
    words = text.split()
    corrected_words = []
    for word in words:
        if word not in spell:
            correct_word = spell.correction(word)
            corrected_words.append(correct_word)
        else:
            corrected_words.append(word)
    return ' '.join(corrected_words)