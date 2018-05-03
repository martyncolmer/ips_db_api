# IPS Data API

This is a minimal flask application integrating a database backend using the sqlalchemay and flask-sqlalchemy libraries

The application provides a simple REST endpoint to access the data as follows:

|HTTP Method | URL | Description |
|------------|-----|-------------|
| GET | `/runs`| Get a list of all runs |
| GET | `/runs/<id>` | Get a single record for run with `id = <id>` |
| POST | `/runs` | Create a new run (associated data must be passed on through JSON) |

# Quick Start

1. Clone and navigate to the root directory of this repository.

2. Install the dependencies with `pip install -r requirements.txt`

3. Initialise the database by running `python init_db.py`

4. Set the following environment variables:
```
FLASK_APP=myapp/app.py
```

5. Run the application with `flask run`


# Making API requests

You can access the data by making API requests. The `requests` library provides this functionality, see it's documentation (http://www.python-requests.org/en/latest/) for more information.

Below is some sample code to retrieve all runs (we assume the app is running on host 127.0.0.1).

```
import requests
import json
response = requests.get('127.0.0.1/runs')
content = json.loads(response.content)
print(content[0])
```

All data to and from the API is in JSON.