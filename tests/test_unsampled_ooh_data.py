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


def test_get_unsampled_ooh_data(client):
    rv = client.get('/unsampled_ooh_data')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 789
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_get_unsampled_ooh_data_run_id(client):

    # Invalid run_id
    rv = client.get('/unsampled_ooh_data/0000')
    assert rv.status_code == 400

    # Valid run_id
    rv = client.get('/unsampled_ooh_data/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 789
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_get_unsampled_ooh_data_data_source(client):

    # Invalid run_id, valid data_source
    rv = client.get('/unsampled_ooh_data/0000/4')
    assert rv.status_code == 400

    # Valid run_id, invalid data_source
    rv = client.get('/unsampled_ooh_data/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/1')
    assert rv.status_code == 400

    # Valid run_id, invalid data_source
    rv = client.get('/unsampled_ooh_data/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/0')
    assert rv.status_code == 200


def test_import_unsampled_ooh_data(client):

    json_data = []
    rec1 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR', 'MONTH': 'MONTH',
            'DATASOURCE': 'DATASOURCE', 'PORTROUTE': 'PORTROUTE', 'REGION': 'REGION',
            'ARRIVEDEPART': 'ARRIVEDEPART', 'UNSAMP_TOTAL': 'UNSAMP_TOTAL'}

    rec2 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR2', 'MONTH': 'MONTH2',
            'DATASOURCE': 'DATASOURCE2', 'PORTROUTE': 'PORTROUTE2', 'REGION': 'REGION2',
            'ARRIVEDEPART': 'ARRIVEDEPART2', 'UNSAMP_TOTAL': 'UNSAMP_TOTAL2'}

    json_data.append(rec1)
    json_data.append(rec2)

    rv = client.post('/unsampled_ooh_data/Automated-Run_ID', json=json_data)
    assert rv.status_code == 200

    rv = client.get('/unsampled_ooh_data/Automated-Run_ID')

    records = rv.json
    assert len(records) == 2
