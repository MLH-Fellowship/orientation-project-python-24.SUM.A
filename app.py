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
    Returns a JSON test message
    '''
    return jsonify({"message": "Hello, World!"})


@app.route('/resume/experience', methods=['GET', 'POST'])
def experience():
    '''
    Handle experience requests
    '''

    if request.method == "GET":
        experiences: list[Experience] = data.get("experience", [])
        if index := request.args.get("index") is not None:
            try:
                return jsonify(experiences[index])
            except ValueError:
                return jsonify({"error": "Invalid experience index"})
        else:
            return jsonify(experiences)

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
    '''
    Handles education requests
    '''
    if request.method == 'GET':
        return jsonify({})

    if request.method == 'POST':
        return jsonify({})

    return jsonify({})


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
