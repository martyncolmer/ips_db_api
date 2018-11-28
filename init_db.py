"""
The Script to initialise the database and load in the data
"""

from myapp.app import app
from myapp.models import Run, db, RunSteps, ProcessVariables, \
    ShiftData, TrafficData, UnsampledOOHData, NonResponseData, \
    ProcessVariableSet, ImbalanceWeight, ExportDataDownload
import csv


def main():
    # An application context needs to be created when performing database operations
    # More details at http://flask.pocoo.org/docs/1.0/appcontext/
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Load in run data
        reader = csv.DictReader(open('resources/runs.csv'))
        for record in reader:
            # Make use of Pythons dictionary unpacking
            # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
            r = Run(**record)
            db.session.add(r)
        db.session.commit()

        # Load in run step data
        reader2 = csv.DictReader(open('resources/run_steps.csv'))
        for record in reader2:
            # r = RunSteps(**record)
            db.session.add(r)
        db.session.commit()

        # Load in process variable set data
        pv_set_reader = csv.DictReader(open('resources/PV_SETS.csv'))
        for record in pv_set_reader:
            r = ProcessVariableSet(**record)
            db.session.add(r)
        db.session.commit()

        # Load in process variable data
        reader3 = csv.DictReader(open('resources/PROCESS_VARIABLES.csv'))
        for record in reader3:
            r = ProcessVariables(**record)
            db.session.add(r)
        db.session.commit()

        # DATA SETS

        # Load in shift data
        reader4 = csv.DictReader(open('resources/SHIFT_DATA.csv'))
        for record in reader4:
            r = ShiftData(**record)
            db.session.add(r)
        db.session.commit()

        # Load in traffic data
        reader5 = csv.DictReader(open('resources/TRAFFIC_DATA.csv'))
        for record in reader5:
            r = TrafficData(**record)
            db.session.add(r)
        db.session.commit()

        # Load in non response data
        reader6 = csv.DictReader(open('resources/NON_RESPONSE_DATA.csv'))
        for record in reader6:
            r = NonResponseData(**record)
            db.session.add(r)
        db.session.commit()

        # Load in unsampled data
        reader7 = csv.DictReader(open('resources/UNSAMPLED_OOH_DATA.csv'))
        for record in reader7:
            r = UnsampledOOHData(**record)
            db.session.add(r)
        db.session.commit()

        # Load in the data
        reader8 = csv.DictReader(open('resources/IMBALANCE_WEIGHT.csv'))
        for record in reader8:
            r = ImbalanceWeight(**record)
            db.session.add(r)
        db.session.commit()

        # Load EXPORT_DATA_DOWNLOAD data
        reader9 = csv.DictReader(open('resources/EXPORT_DATA_DOWNLOAD.csv'))
        for record in reader9:
            r = ExportDataDownload(**record)
            db.session.add(r)
        db.session.commit()

        # # Load SURVEY_SUBSAMPLE data
        # reader10 = csv.DictReader(open('resources/SURVEY_SUBSAMPLE.csv'))
        # for record in reader10:
        #     r = ExportDataDownload(**record)
        #     db.session.add(r)
        # db.session.commit()


if __name__ == '__main__':
    main()

