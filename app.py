'''
Flask Application
'''
from flask import Flask, jsonify, request
from models import Experience, Education, Skill

app = Flask(__name__)

data = {
    "experience": [
        Experience("Software Developer",
                   "A Cool Company",
                   "October 2022",
                   "Present",
                   "Writing Python Code",
                   "example-logo.png")
    ],
    "education": [
        Education("Computer Science",
                  "University of Tech",
                  "September 2019",
                  "July 2022",
                  "80%",
                  "example-logo.png")
    ],
    "skill": [
        Skill("Python",
              "1-2 Years",
              "example-logo.png")
    ]
}


@app.route('/test')
def hello_world():
    '''
    Endpoint to return a JSON test message.

    Returns:
        dict: A JSON response containing a test message.
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Endpoint to handle experience request 
    
    GET: Retrieves an experience based on its unique identifier (ID)
    POST: Adds a new experience
    
    Returns:
        dict: A JSON response containing an experience.
    '''
    if request.method == 'GET':
        return jsonify()

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})

@app.route('/resume/education', methods=['GET', 'POST'])
def education():
    '''
    Handle requests related to education information.
    
    GET: Retrieves an education based on its unique identifier (ID) 
    POST: Adds a new education

    Returns:
        dict: A JSON response containing an education.
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


@app.route('/resume/skill', methods=['GET', 'POST'])
def skill():
    '''
    Handle requests related to skill information.
    
    GET: Retrieves a skill based on its unique identifier (ID)    
    POST: Adds a new skill

    Returns:
        dict: A JSON response containing a skill.
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})
