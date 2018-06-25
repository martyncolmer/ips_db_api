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


def test_get_export_data_download(client):
    rv = client.get('/EXPORT_DATA_DOWNLOAD')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 6
    for x in json_data:
        assert x["SOURCE_TABLE"] == 'PS_IMBALANCE'


def test_get_export_data_download_run_id(client):

    # Invalid run_id
    rv = client.get('/EXPORT_DATA_DOWNLOAD/0000')
    assert rv.status_code == 400

    # Valid run_id
    rv = client.get('/EXPORT_DATA_DOWNLOAD/f144ec22-921f-43ff-a93c-189695336580')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 1
    for x in json_data:
        assert 'f144ec22-921f-43ff-a93c-189695336580' == x['RUN_ID']


def test_post_export_data_download(client):

    json_data = {'DATE_CREATED': "2018-01-24 12:00:06",
            'DOWNLOADABLE_DATA': "RUN_ID,FLOW,SUM_PRIOER_WT,SUM_IMNAL_WT",
            'FILENAME': 'TestGet',
            'RUN_ID': 'el_24_01_1988',
            'SOURCE_TABLE': 'get_test_source_table'}

    print(type(json_data))

    rv = client.post('/export_data_download', json=json_data, content_type='application/json')
    assert rv.status_code == 201

    rv = client.get('/export_data_download')

    records = rv.json
    assert len(records) == 7



