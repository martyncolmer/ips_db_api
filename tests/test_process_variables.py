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


def test_create_process_variables(client):

    json_data = []
    rec1 = {'PV_NAME': 'AutomatedTest_PV_1', 'PV_CONTENT': 'AutomatedTest_PV_Content_1', 'PV_REASON': 'AutomatedTest_PV_Reason_1'}

    rec2 = {'PV_NAME': 'AutomatedTest_PV_2', 'PV_CONTENT': 'AutomatedTest_PV_Content_2', 'PV_REASON': 'AutomatedTest_PV_Reason_2'}

    json_data.append(rec1)
    json_data.append(rec2)

    rv = client.post('/process_variables/Test-Run-ID', json=json_data, content_type='application/json')
    assert rv.status_code == 201


def test_get_process_variable(client):
    rv = client.get('/process_variables')
    assert rv.status_code == 200

    json_data = json.loads(rv.data)
    for x in json_data:
        assert x['RUN_ID']
        assert x['PV_NAME']
        assert x['PV_CONTENT']
        assert x['PV_REASON']

    rv = client.get('/process_variables/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert rv.status_code == 200

    json_data = json.loads(rv.data)
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']


def test_update_process_variable(client):

    json_data = {'RUN_ID': '9e5c1872-3f8e-4ae5-85dc-c67a602d011e',
                 'PV_NAME': 'PV_1',
                 'PV_CONTENT': 'if(test is True): PV_1 content = test',
                 'PV_REASON': 'Updated by automated test'}

    rv = client.put('/process_variables', json=json_data, content_type='application/json')

    assert rv.status_code == 200

    rv = client.get('/process_variables/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    json_data = json.loads(rv.data)

    for x in json_data:
        if x['PV_NAME'] == 'PV_1':
            assert x['PV_CONTENT'] == 'if(test is True): PV_1 content = test'
            assert x['PV_REASON'] == 'Updated by automated test'
