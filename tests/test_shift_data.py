import pytest
import tempfile
import os
import json
import init_db
from flask import jsonify

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


def test_import_shift_data(client):

    json_data = []
    rec1 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR', 'MONTH': 'MONTH',
                 'DATA_SOURCE_ID': 'DATA_SOURCE_ID', 'PORTROUTE': 'PORTROUTE', 'WEEKDAY': 'WEEKDAY',
                 'ARRIVEDEPART': 'ARRIVEDEPART', 'TOTAL': 'TOTAL', 'AM_PM_NIGHT': 'AM_PM_NIGHT'}
    rec2 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR-2', 'MONTH': 'MONTH-2',
                 'DATA_SOURCE_ID': 'DATA_SOURCE_ID-2', 'PORTROUTE': 'PORTROUTE-2', 'WEEKDAY': 'WEEKDAY-2',
                 'ARRIVEDEPART': 'ARRIVEDEPART-2', 'TOTAL': 'TOTAL-2', 'AM_PM_NIGHT': 'AM_PM_NIGHT-2'}

    json_data.append(rec1)
    json_data.append(rec2)

    rv = client.post('/shift_data/Automated-Run_ID', json=json_data, content_type='application/json')
    assert rv.status_code == 200

    rv = client.get('/SHIFT_DATA/Automated-Run_ID')

    records = rv.json
    assert len(records) == 2
