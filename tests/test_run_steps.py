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


def test_get_all_run_steps(client):
    rv = client.get('/run_steps')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) >= 14

    number_of_runs = (len(json_data)/14)
    left_over = number_of_runs % 1
    assert left_over == 0


def test_get_single_run_steps_incorrect_run_id(client):

    # Invalid run_id
    rv = client.get('/run_steps/0000')
    assert rv.status_code == 400


def test_get_run_steps(client):

    # Valid run_id
    rv = client.get('/run_steps/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 14
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_set_run_step_no_value(client):

    rv = client.put('/run_steps/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 405


def test_set_run_step_value_and_step(client):

    rv = client.put('/run_steps/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/1/1')
    assert rv.status_code == 200


def test_set_run_step_value_only(client):

    rv = client.put('/run_steps/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/0')
    assert rv.status_code == 200
