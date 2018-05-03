"""
The Script to initialise the database and load in the data
"""

from myapp.app import app
from myapp.models import Run, db
import csv


# An application context needs to be created when performing database operations
# More details at http://flask.pocoo.org/docs/1.0/appcontext/
with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Load in the data
    reader = csv.DictReader(open('resources/runs.csv'))
    for record in reader:
        # Make use of Pythons dictionary unpacking
        # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
        r = Run(**record)
        db.session.add(r)

    db.session.commit()


