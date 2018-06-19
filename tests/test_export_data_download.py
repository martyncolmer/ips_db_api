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
    assert len(json_data) == 1
    for x in json_data:
        assert 'f144ec22-921f-43ff-a93c-189695336580' == x['RUN_ID']
        # assert 'RUN_ID,FLOW,SUM_PRIOR_WT,SUM_IMBAL_WT' == x['FILENAME']


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
