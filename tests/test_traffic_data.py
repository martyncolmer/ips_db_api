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


def test_get_traffic_data(client):
    rv = client.get('/TRAFFIC_DATA')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 546
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_get_traffic_data_run_id(client):

    # Invalid run_id
    rv = client.get('/TRAFFIC_DATA/0000')
    assert rv.status_code == 400

    # Valid run_id
    rv = client.get('/TRAFFIC_DATA/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 546
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_get_traffic_data_data_source(client):

    # Invalid run_id, valid data_source
    rv = client.get('/TRAFFIC_DATA/0000/4')
    assert rv.status_code == 400

    # Valid run_id, invalid data_source
    rv = client.get('/TRAFFIC_DATA/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/1')
    assert rv.status_code == 400


def test_import_traffic_data(client):

    json_data = []
    rec1 = {'YEAR': '2017', 'MONTH': '1',
            'DATASOURCE': 'Sea', 'PORTROUTE': '611', 'ARRIVEDEPART': '1',
            'TRAFFICTOTAL': 'TRAFFICTOTAL', 'PERIODSTART': 'PERIODSTART', 'PERIODEND': 'PERIODEND',
            'AM_PM_NIGHT': 'AM_PM_NIGHT', 'HAUL': 'HAUL', 'VEHICLE': 'VEHICLE'}

    rec2 = {'RUN_ID': 'Automated-Run_ID', 'YEAR': 'YEAR2', 'MONTH': 'MONTH2',
            'DATASOURCE': 'DATASOURCE2', 'PORTROUTE': 'PORTROUTE2', 'ARRIVEDEPART': 'ARRIVEDEPART2',
            'TRAFFICTOTAL': 'TRAFFICTOTAL2', 'PERIODSTART': 'PERIODSTART2', 'PERIODEND': 'PERIODEND2',
            'AM_PM_NIGHT': 'AM_PM_NIGHT2', 'HAUL': 'HAUL2', 'VEHICLE': 'VEHICLE2'}

    json_data.append(rec1)
    json_data.append(rec2)

    rv = client.post('/traffic_data/Automated-Run_ID', json=json_data, content_type='application/json')
    assert rv.status_code == 200

    rv = client.get('/traffic_data/Automated-Run_ID')

    records = rv.json
    assert len(records) == 2
