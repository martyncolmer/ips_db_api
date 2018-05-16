from flask_sqlalchemy import SQLAlchemy

# This class provided by flask-sqlalchemy can be used to access all other
# SQLAlchemy building blocks when defining the database model class
# More details at http://flask-sqlalchemy.pocoo.org/2.3/
db = SQLAlchemy()


# Defining the Model class that maps to the database schema
class Run(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(50))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    status = db.Column(db.String(50))
    type = db.Column(db.String(50))

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<Run {name}>'.format(name=self.name)


# Defining the Model class that maps to the database schema
class ShiftData(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    YEAR = db.Column(db.String(50), primary_key=True)
    MONTH = db.Column(db.String(50), primary_key=True)
    DATA_SOURCE_ID = db.Column(db.String(50), primary_key=True)
    PORTROUTE = db.Column(db.String(50), primary_key=True)
    WEEKDAY = db.Column(db.String(50), primary_key=True)
    ARRIVEDEPART = db.Column(db.String(50), primary_key=True)
    TOTAL = db.Column(db.String(50), primary_key=True)
    AM_PM_NIGHT = db.Column(db.String(50), primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<Shift_data {run_id}>'.format(name=self.run_id)
