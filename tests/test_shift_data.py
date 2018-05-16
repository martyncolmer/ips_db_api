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


def test_get_shift_data(client):
    rv = client.get('/SHIFT_DATA')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 1000
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_get_shift_data_run_id(client):

    # Invalid run_id
    rv = client.get('/SHIFT_DATA/0000')
    assert rv.status_code == 400

    # Valid run_id
    rv = client.get('/SHIFT_DATA/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 1000
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_get_shift_data_data_source(client):

    # Invalid run_id, valid data_source
    rv = client.get('/SHIFT_DATA/0000/4')
    assert rv.status_code == 400

    # Valid run_id, invalid data_source
    rv = client.get('/SHIFT_DATA/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/1')
    assert rv.status_code == 400

    # Valid run_id, valid data_source
    rv = client.get('/SHIFT_DATA/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/4')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 1000
    for x in json_data:
        assert '4' == x['DATA_SOURCE_ID']

