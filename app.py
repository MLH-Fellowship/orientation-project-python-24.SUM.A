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
        return jsonify(data.get("experience", []))

    if request.method == "POST":
        post_data: dict[str, str] = request.get_json()
        experiences = data.get("experience", [])
        experiences.append(
            Experience(
                post_data["title"],
                post_data["company"],
                post_data["start_date"],
                post_data["end_date"],
                post_data["description"],
                post_data["logo"],
            )
        )

        return jsonify({"id": len(data.get("experience", [])) - 1})

    return jsonify({})

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
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

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
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

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