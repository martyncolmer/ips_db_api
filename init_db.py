"""
The Script to initialise the database and load in the data
"""

from myapp.app import app
from myapp.models import Run, db, RunSteps, ProcessVariables, ShiftData, TrafficData, UnsampledOOHData, NonResponseData
import csv

def main():
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

        # Load in the data
        reader2 = csv.DictReader(open('resources/run_steps.csv'))
        for record in reader2:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = RunSteps(**record)
            db.session.add(r)

        db.session.commit()

        # Load in the data
        reader3 = csv.DictReader(open('resources/PROCESS_VARIABLES.csv'))
        for record in reader3:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = ProcessVariables(**record)
            db.session.add(r)

        db.session.commit()

        # Load in the data
        reader4 = csv.DictReader(open('resources/SHIFT_DATA.csv'))
        for record in reader4:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = ShiftData(**record)
            db.session.add(r)

        db.session.commit()

        # Load in the data
        reader5 = csv.DictReader(open('resources/TRAFFIC_DATA.csv'))
        for record in reader5:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = TrafficData(**record)
            db.session.add(r)

        db.session.commit()

        # Load in the data
        reader6 = csv.DictReader(open('resources/NON_RESPONSE_DATA.csv'))
        for record in reader6:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = NonResponseData(**record)
            db.session.add(r)

        db.session.commit()

        # Load in the data
        reader7 = csv.DictReader(open('resources/UNSAMPLED_OOH_DATA.csv'))
        for record in reader7:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = UnsampledOOHData(**record)
            db.session.add(r)

        db.session.commit()


if __name__ == '__main__':
    main()

