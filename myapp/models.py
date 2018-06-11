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
class RunSteps(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    NUMBER = db.Column(db.String(2), primary_key=True)
    NAME = db.Column(db.String(50), primary_key=True)
    STATUS = db.Column(db.String(1), primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<RunStatus {RUN_ID}>'.format(name=self.RUN_ID)


# Defining the Model class that maps to the database schema
class ProcessVariables(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    PV_NAME = db.Column(db.String, primary_key=True)
    PV_CONTENT = db.Column(db.String, primary_key=True)
    PV_REASON = db.Column(db.String, primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<Process_Variables {RUN_ID}>'.format(name=self.RUN_ID)


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
        return '<ShiftData {RUN_ID}>'.format(name=self.RUN_ID)


# Defining the Model class that maps to the database schema
class TrafficData(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    YEAR = db.Column(db.String(50), primary_key=True)
    MONTH = db.Column(db.String(50), primary_key=True)
    DATASOURCE = db.Column(db.String(50), primary_key=True)
    PORTROUTE = db.Column(db.String(50), primary_key=True)
    ARRIVEDEPART = db.Column(db.String(50), primary_key=True)
    TRAFFICTOTAL = db.Column(db.String(50), primary_key=True)
    PERIODSTART = db.Column(db.String(50), primary_key=True)
    PERIODEND = db.Column(db.String(50), primary_key=True)
    AM_PM_NIGHT = db.Column(db.String(50), primary_key=True)
    HAUL = db.Column(db.String(50), primary_key=True)
    VEHICLE = db.Column(db.String(50), primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<TrafficData {RUN_ID}>'.format(name=self.RUN_ID)


# Defining the Model class that maps to the database schema
class NonResponseData(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    YEAR = db.Column(db.String(50), primary_key=True)
    MONTH = db.Column(db.String(50), primary_key=True)
    DATA_SOURCE_ID = db.Column(db.String(50), primary_key=True)
    PORTROUTE = db.Column(db.String(50), primary_key=True)
    WEEKDAY = db.Column(db.String(50), primary_key=True)
    ARRIVEDEPART = db.Column(db.String(50), primary_key=True)
    AM_PM_NIGHT = db.Column(db.String(50), primary_key=True)
    SAMPINTERVAL = db.Column(db.String(50), primary_key=True)
    MIGTOTAL = db.Column(db.String(50), primary_key=True)
    ORDTOTAL = db.Column(db.String(50), primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<NonResponseData {RUN_ID}>'.format(name=self.RUN_ID)


# Defining the Model class that maps to the database schema
class UnsampledOOHData(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    YEAR = db.Column(db.String(50), primary_key=True)
    MONTH = db.Column(db.String(50), primary_key=True)
    DATA_SOURCE_ID = db.Column(db.String(50), primary_key=True)
    PORTROUTE = db.Column(db.String(50), primary_key=True)
    REGION = db.Column(db.String(50), primary_key=True)
    ARRIVEDEPART = db.Column(db.String(50), primary_key=True)
    UNSAMP_TOTAL = db.Column(db.String(50), primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<UnsampledOOHData {RUN_ID}>'.format(name=self.RUN_ID)


# Defining the Model class that maps to the database schema
class ImbalanceWeight(db.Model):

    RUN_ID = db.Column(db.String, primary_key=True)
    FLOW = db.Column(db.String, primary_key=True)
    SUM_PRIOR_WT = db.Column(db.String, primary_key=True)
    SUM_IMBAL_WT = db.Column(db.String, primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<ImbalanceWeight {RUN_ID}>'.format(name=self.RUN_ID)