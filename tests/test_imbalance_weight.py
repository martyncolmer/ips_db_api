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


def test_get_imbalance_weight(client):
    rv = client.get('/IMBALANCE_WEIGHT')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert len(json_data) == 3
    for x in json_data:
        assert '9e5c1872-3f8e-4ae5-85dc-c67a602d011e' == x['RUN_ID']