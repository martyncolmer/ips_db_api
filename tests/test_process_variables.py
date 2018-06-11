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


def test_update_process_variable(client):
    # updating non-existent id should fail
    json_data = {'RUN_ID': '9e5c1872-3f8e-4ae5-85dc-c67a602d011e', 'PV_NAME': 'SHIFT_WT_PV', 'PV_CONTENT': 'Shift wt pv content = test',
                 'PV_REASON': 'Updated by automated test'}
    rv = client.put('/process_variables/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_WT_PV',
                    data=json.dumps(json_data), content_type='application/json')
    assert rv.status_code == 200

