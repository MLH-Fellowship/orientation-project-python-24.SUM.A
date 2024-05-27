'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill
from utils import load_data, save_data, generate_id, correct_spelling

data = load_data('data/data.json')

app = Flask(__name__)

@app.route('/test')
def hello_world():
    '''
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''

    if request.method == "GET":
        return jsonify([edu.__dict__ for edu in data['experience']])

    if request.method == "POST":
        required_fields = ['title', 'company', 'start_date', 'end_date', 'description', 'logo']
        
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400
        
        missing_fields = [field for field in required_fields if field not in request.json]
        if missing_fields:
            return jsonify({'error': 'Missing required fields'}), 400
        
        new_id = generate_id(data, 'experience')
        new_experience_data = request.json
        new_experience_data['id'] = new_id
        new_experience = Experience(**new_experience_data)
        
        data['experience'].append(new_experience)
        save_data('data/data.json', data)
        
        return jsonify({'id': new_id}), 201
    
    return jsonify({'error': 'Method not allowed'}), 405


@app.route('/resume/experience/<int:index>', methods = ['GET'])
def get_experience(index):
    '''
    Handle get request for single experience by index
    '''
    total_length = len(data['experience'])
    if 0 <= index < total_length:
        return jsonify(data["experience"][index])
    return jsonify({'error': 'Invalid Index'}), 400


@app.route('/resume/experience/<int:index>', methods=['DELETE'])
def delete_experience(index):
    '''
    Handles experience delete requests by index
    '''
    total_length = len(data['experience'])
    if 0 <= index < total_length:
        data['experience'].pop(index)
        return jsonify({"message": "Successfully deleted"}), 200

    return jsonify({"error": 'Invalid Index'}), 400


@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    """
    Handle education requests
    """
    if request.method == 'GET':
        # convert education data to dictionary and return as JSON
        return jsonify([edu.__dict__ for edu in data['education']])

    if request.method == 'POST':
        required_fields = ['course', 'school', 'start_date', 'end_date', 'grade', 'logo']
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        missing_fields = [field for field in required_fields if field not in request.json]
        if missing_fields:
            return jsonify({'error': 'Missing required fields'}), 400

        # If we used database, it will generate the id for us
        new_id = generate_id(data, 'education')

        new_education_data = request.json
        new_education_data['id'] = new_id
        new_education = Education(**new_education_data)

        data['education'].append(new_education)
        save_data('data/data.json', data)

        return jsonify({'id': new_id}), 201
    
    return jsonify({'error': 'Method not allowed'}), 405 



@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handles Skill requests
    '''
    if request.method == 'GET':
        index = request.args.get("index")
        if index is not None: #check if requesting a specific index
            if not index.isnumeric(): #is index a number
                return jsonify("Incorrect index"), 400
            
            #check if index is inside the bounds of the list
            if int(index) < 0 or int(index) >= len(data.get("skill")): 
                return jsonify("Incorrect request, index out of bounds"), 400
            return jsonify(data.get("skill")[int(index)]), 200
        
        return jsonify(data.get("skill")), 200 #return the whole list

    if request.method == 'POST':
        required_fields = ['name', 'proficiency', 'logo']
        if not request.json:
            return jsonify({'error': 'No data provided'}), 400

        missing_fields = [field for field in required_fields if field not in request.json]
        if missing_fields:
            return jsonify({'error': 'Missing required fields'}), 400

        data.get("skill").append(Skill(**request.json))
        save_data('data/data.json', data)

        return jsonify({'id': len(data.get("skill")) - 1}), 200

    return jsonify({})


@app.route('/spelling/correct-spelling', methods=['GET', 'POST'])
def spelling_check():
    '''
    Handles spelling check requests
    '''
    data = request.get_json()
    text = data.get('text', '')
    corrected_text = correct_spelling(text)

    # return the original and corrected text
    return jsonify({"before": text, "after": corrected_text})