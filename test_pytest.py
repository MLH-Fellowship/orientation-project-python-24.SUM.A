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

    item_id = app.test_client().post('/resume/experience',
                                     json=example_experience).json['id']
    response = app.test_client().get('/resume/experience')
    assert response.json[item_id] == example_experience


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

def test_skill_indexed_get(): #goes through the data and checks if it can get all the skills through indexes
    index = 0
    for skill in data.get("skill"):
        assert Skill(**app.test_client().get('/resume/skill?index=%d' % index).json) == skill, "No skill or incorrect skill found at the index %d" % index
        index += 1

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
