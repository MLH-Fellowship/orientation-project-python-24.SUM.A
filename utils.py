import json
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
