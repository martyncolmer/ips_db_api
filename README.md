# Example Flask Application with Database

This is a minimal flask application demostrating how to integrate a database backend using the sqlalchemay and flask-sqlalchemy libraries

The application provides a simple REST endpoint to access the data as follows:

|HTTP Method | URL | Description |
|------------|-----|-------------|
| GET | `/respondents`| Get a list of records for all respondents |
| GET | `/respondents/<id>` | Get a single records for respondent with `id = <id>` |

# Quick Start

1. Clone and navigate to the root directory of this repository.

2. Install the dependencies with `pip install -r requirements.txt`

3. Initialise the database by running `python init_db.py`

4. Set the following environment variables:
```
FLASK_APP=myapp/app.py
```

5. Run the application with `flask run`


## Using a `env.bat` File

In windows to make step 4 above easier you can create a `env.bat` file that sets these variables for the current active
terminal session:

```
@ECHO OFF
set FLASK_APP=myapp/app.py
set FLASK_DEBUG=1
```

This can be executed simply by running `env.bat`.

Following the 12 factor app, we will be storing configuration in environment variables, which later will include secret
information. So *make sure that this file is never submitted to version control*
