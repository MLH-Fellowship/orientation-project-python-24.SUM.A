'''
Tests in Pytest
'''
from app import app

from models import Skill
from utils import load_data, correct_spelling

data = load_data('data/data.json')

def test_client():
    '''
    Makes a request and checks the message received is the same
    '''
    response = app.test_client().get('/test')
    assert response.status_code == 200
    assert response.json['message'] == "Hello, World!"


def test_experience():
    '''
    Add a new experience and then get all experiences. 
    
    Check that it returns the new experience in that list
    '''
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }

    post_response = app.test_client().post('/resume/experience', json=example_experience)
    assert post_response.status_code == 201
    new_experience_id = post_response.json['id']
    
    get_response = app.test_client().get('/resume/experience')
    assert get_response.status_code == 200
    
    found = False
    for experience in get_response.json:
        if experience['id'] == new_experience_id:
            for key, value in example_experience.items():
                assert experience[key] == value
            found = True
            break
        
    assert found, "New experience was not found in the returned list"

def test_delete_experience():
    '''
    Add a new experience and then delete experience by index. 
    
    '''
    prior_experience = app.test_client().get('resume/experience').json
    example_experience = {
        "title": "Software Developer",
        "company": "A Cooler Company",
        "start_date": "October 2022",
        "end_date": "Present",
        "description": "Writing JavaScript Code",
        "logo": "example-logo.png"
    }
    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']

    response = app.test_client().delete(f'/resume/experience?index={item_id}')
    assert response.json['message'] == "Successfully deleted"
    assert prior_experience == app.test_client().get('resume/experience').json


def test_education():
    '''
    Add a new education and then get all educations.
    
    Check that the new education is correctly added to the list.
    '''
    example_education = {
        "course": "Engineering",
        "school": "NYU",
        "start_date": "October 2022",
        "end_date": "August 2024",
        "grade": "86%",
        "logo": "example-logo.png"
    }
    post_response = app.test_client().post('/resume/education', json=example_education)
    assert post_response.status_code == 201
    new_education_id = post_response.json['id']

    get_response = app.test_client().get('/resume/education')
    assert get_response.status_code == 200

    found = False
    for education in get_response.json:
        if education['id'] == new_education_id:
            for key, value in example_education.items():
                assert education[key] == value
            found = True
            break
        
    assert found, "New education was not found in the returned list"

def test_post_education_missing_fields():
    """Test POST request to /resume/education with missing fields.
    POST request with missing 'end_date' and 'grade' fields.
    """
    incomplete_education = {
        "course": "Engineering",
        "school": "UBC",
        "start_date": "October 2024",
        "logo": "example-logo.png"
    }
    response = app.test_client().post('/resume/education', json=incomplete_education)
    assert response.status_code == 400
    assert 'Missing required fields' in response.json['error']
    assert 'end_date' in response.json['error']
    assert 'grade' in response.json['error']

def test_skill_indexed_get():
    '''
    Load skill data from data.json
    Check that we can get all skills through indexes
    '''
    index = 0
    for skill in data.get("skill"):
        new_skill = Skill(**app.test_client().get(f'/resume/skill?index={index}').json)
        assert new_skill == skill, f"No skill or incorrect skill found at the index {index}"
        index += 1

def test_skill_get_all():
    '''
    Load skills data from data.json
    Check that the list we get from server is the same as the local list
    '''
    local_skills = data.get("skill")
    skills = app.test_client().get('/resume/skill').json
    for i, skill in enumerate(skills):
        assert local_skills[i] == Skill(**skill)

def test_post_experience_missing_fields():
    """Test POST request to /resume/experience with missing fields.
    POST request with missing 'company' and 'start_date' fields.
    """
    incomplete_experience = {
        "title": "Software Developer",  
        "description": "Writes code",
    }
    response = app.test_client().post('/resume/experience', json=incomplete_experience)
    assert response.status_code == 400
    assert 'Missing required fields' in response.json['error']
    assert 'company' in response.json['error']
    assert 'start_date' in response.json['error']

def test_skill():
    '''
    Add a new skill and then get all skills. 
    
    Check that it returns the new skill in that list
    '''
    example_skill = {
        "name": "JavaScript",
        "proficiency": "2-4 years",
        "logo": "example-logo.png"
    }

    item_id = app.test_client().post('/resume/skill',
                                     json=example_skill).json['id']

    response = app.test_client().get('/resume/skill')
    assert response.json[item_id] == example_skill


def test_correct_spelling():
    '''
    Test the correct_spelling function
    '''
    text = "speling"
    expected_output = "spelling"
    assert correct_spelling(text) == expected_output
