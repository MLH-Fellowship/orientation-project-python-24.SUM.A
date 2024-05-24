'''
Tests in Pytest
'''
from app import app


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


def test_delete_experience():
    '''
    Add a new experience and then delete experience by index. 
    
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

    response = app.test_client().delete('/resume/experience/' + item_id)
    assert response.json["message"] == "Successfully deleted"


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
