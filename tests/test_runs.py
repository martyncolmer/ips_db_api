import pytest
import tempfile
import os
import json
import init_db

from myapp import app as my_app


@pytest.fixture
def client():
    file_handle, file_name = tempfile.mkstemp()
    my_app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_name
    my_app.app.config['TESTING'] = True

    init_db.main()
    client = my_app.app.test_client()
    with my_app.app.app_context():
        my_app.db.init_app(my_app.app)

    yield client

    os.close(file_handle)
    os.unlink(file_name)


def test_get_all_runs(client):
    rv = client.get('/runs')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 5
    assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == json_data[0]['id']
    assert 'fcd39e00-6769-4d12-9915-0c9330aee408' == json_data[1]['id']
    assert 'f144ec22-921f-43ff-a93c-189695336580' == json_data[2]['id']
    assert '1f451a03-02a2-4597-8a95-70961b1a9c29' == json_data[3]['id']
    assert 'a97e0960-6a49-402b-a784-ec5c3c2d74ef' == json_data[4]['id']


def test_get_one_run(client):
    # non-existing id should fail
    rv = client.get('runs/0')
    assert rv.status_code == 400

    rv = client.get('/runs/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 7
    assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == json_data['id']
    assert 'Test run that has actual data' == json_data['desc']
    assert '10022018' == json_data['start_date']
    assert '10022018' == json_data['end_date']
    assert '0' == json_data['type']
    assert '0' == json_data['status']
    assert 'TestRun' == json_data['name']


def test_create_run(client):
    # sending no data should fail
    rv = client.post('/runs')
    assert rv.status_code == 400

    # sending incorrect data should fail
    rv = client.post('/runs', data="not json")
    assert rv.status_code == 400

    # sending json data without the id should fail
    json_data = {'name': 'Test', 'desc': 'desc', 'start_date': 'test',
                 'end_date': 'test', 'status': '0', 'type': '1'}
    rv = client.post('/runs', data=json.dumps(json_data), content_type='application/json')
    assert rv.status_code == 400

    # sending correct data should succeed
    json_data['id'] = '0'
    rv = client.post('/runs', data=json.dumps(json_data), content_type='application/json')
    assert rv.status_code == 201
    # check if run was created
    rv = client.get('/runs')
    json_data = json.loads(rv.data)
    assert len(json_data) == 6


def test_update_run(client):
    # sending no data should fail
    rv = client.put('/runs/0')
    assert rv.status_code == 400

    # sending non-json data should fail
    rv = client.put('runs/0', data="not json")
    assert rv.status_code == 400

    # updating non-existent id should fail
    json_data = {'name': 'Test', 'desc': 'desc', 'start_date': 'test',
                 'end_date': 'test', 'status': '0', 'type': '1'}
    rv = client.put('/runs/0', data=json.dumps(json_data), content_type='application/json')
    assert rv.status_code == 400

    # updating correct run with correct data should succeed
    rv = client.put('/runs/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=json.dumps(json_data),
                     content_type='application/json')
    assert rv.status_code == 200

    # check update succeeded
    rv = client.get('/runs/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert 'desc' == json_data['desc']
