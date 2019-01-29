# IPS Data API

This is a minimal flask application integrating a database backend using the sqlalchemay and flask-sqlalchemy libraries

The application provides a simple REST endpoint to access the data as follows:

|HTTP Method | URL | Description |
|------------|-----|-------------|
| GET | `/runs`| Get a list of all runs |
| GET | `/runs/<run_id>` | Get a single record for run with `id = <run_id>` |
| POST | `/runs` | Create a new run (associated data must be passed on through JSON) |
| PUT | `/runs/<run_id>` | Update the run with `<run_id>` (associated data must be passed on through JSON) |

# Quick Start

1. Clone and navigate to the root directory of this repository.

2. Install the dependencies with `pip install -r requirements.txt`

3. Initialise the database by running `python init_db.py`

4. Set the following environment variables:
```
FLASK_APP=myapp/app.py
```

5. Run the application with `flask run`

# Setting up the database

There is a docker-compose file in the project root that can be used to pull 
over the latest sql server instance and configure the database in a docker container.

in the project root:

```bash
docker-compose up -d
```

to stop the service and delete the container:

```bash
docker-compose down
```

```

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


# Making changes to the app

Changes to the app should be made on a separate branch and submitted through a merge request.

All data used to initialise the database resides in `resources`.

All the database tables are specified in `models.py`.

All api endpoints are specified in `app.py`.

Should you need additional packages other than the ones listed in `requirements.txt` make sure to include them in the `vendor` folder.


# Pushing to CloudFoundry

Follow these steps to upload the app to CloudFoundry:

* Make sure you have the CloudFoundry Command Line Interface (CLI) installed (service desk or artifactory)
* Make sure you have CloudFoundry login credentials (service desk request?)
* Open a command line window (cmd from Start menu)
* Change directory to where the app is located on your local pc (e.g. D:/ips_db_api)
* Log in to CloudFoundry with `cf login -u <username> -p <password>`
* Push the app to CloudFoundry with `cf push`
* If the command `cf` does not work you may have to use the full path to the CLI executble (e.g. C:/Applications/CloudFoundry/cf.exe)