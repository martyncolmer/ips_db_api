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
class ProcessVariableSet(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    NAME = db.Column(db.String)
    USER = db.Column(db.String)
    START_DATE = db.Column(db.String)
    END_DATE = db.Column(db.String)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<Process_Variable Set {RUN_ID}>'.format(name=self.RUN_ID)


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
    DATA_SOURCE_ID = db.Column(db.String(50), primary_key=True)
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


# Defining the Model class that maps to the database schema
class ExportDataDownload(db.Model):

    RUN_ID = db.Column(db.String, primary_key=True)
    DOWNLOADABLE_DATA = db.Column(db.String, primary_key=True)
    FILENAME = db.Column(db.String, primary_key=True)
    SOURCE_TABLE = db.Column(db.String, primary_key=True)
    DATE_CREATED = db.Column(db.String, primary_key=True)

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<ExportDataDownload {'+self.RUN_ID+'}>'


class SurveySubsample(db.Model):
    RUN_ID = db.Column(db.String, primary_key=True)
    SERIAL = db.Column(db.String, primary_key=True)
    AGE = db.Column(db.String, primary_key=True)
    AM_PM_NIGHT = db.Column(db.String, primary_key=True)
    ANYUNDER16 = db.Column(db.String, primary_key=True)
    APORTLATDEG = db.Column(db.String, primary_key=True)
    APORTLATMIN = db.Column(db.String, primary_key=True)
    APORTLATSEC = db.Column(db.String, primary_key=True)
    APORTLATNS = db.Column(db.String, primary_key=True)
    APORTLONDEG = db.Column(db.String, primary_key=True)
    APORTLONMIN = db.Column(db.String, primary_key=True)
    APORTLONSEC = db.Column(db.String, primary_key=True)
    APORTLONEW = db.Column(db.String, primary_key=True)
    ARRIVEDEPART = db.Column(db.String, primary_key=True)
    BABYFARE = db.Column(db.String, primary_key=True)
    BEFAF = db.Column(db.String, primary_key=True)
    CHANGECODE = db.Column(db.String, primary_key=True)
    CHILDFARE = db.Column(db.String, primary_key=True)
    COUNTRYVISIT = db.Column(db.String, primary_key=True)
    CPORTLATDEG = db.Column(db.String, primary_key=True)
    CPORTLATMIN = db.Column(db.String, primary_key=True)
    CPORTLATSEC = db.Column(db.String, primary_key=True)
    CPORTLATNS = db.Column(db.String, primary_key=True)
    CPORTLONDEG = db.Column(db.String, primary_key=True)
    CPORTLONMIN = db.Column(db.String, primary_key=True)
    CPORTLONSEC = db.Column(db.String, primary_key=True)
    CPORTLONEW = db.Column(db.String, primary_key=True)
    INTDATE = db.Column(db.String, primary_key=True)
    DAYTYPE = db.Column(db.String, primary_key=True)
    DIRECTLEG = db.Column(db.String, primary_key=True)
    DVEXPEND = db.Column(db.String, primary_key=True)
    DVFARE = db.Column(db.String, primary_key=True)
    DVLINECODE = db.Column(db.String, primary_key=True)
    DVPACKAGE = db.Column(db.String, primary_key=True)
    DVPACKCOST = db.Column(db.String, primary_key=True)
    DVPERSONS = db.Column(db.String, primary_key=True)
    DVPORTCODE = db.Column(db.String, primary_key=True)
    EXPENDCODE = db.Column(db.String, primary_key=True)
    EXPENDITURE = db.Column(db.String, primary_key=True)
    FARE = db.Column(db.String, primary_key=True)
    FAREK = db.Column(db.String, primary_key=True)
    FLOW = db.Column(db.String, primary_key=True)
    HAULKEY = db.Column(db.String, primary_key=True)
    INTENDLOS = db.Column(db.String, primary_key=True)
    KIDAGE = db.Column(db.String, primary_key=True)
    LOSKEY = db.Column(db.String, primary_key=True)
    MAINCONTRA = db.Column(db.String, primary_key=True)
    MIGSI = db.Column(db.String, primary_key=True)
    INTMONTH = db.Column(db.String, primary_key=True)
    NATIONALITY = db.Column(db.String, primary_key=True)
    NATIONNAME = db.Column(db.String, primary_key=True)
    NIGHTS1 = db.Column(db.String, primary_key=True)
    NIGHTS2 = db.Column(db.String, primary_key=True)
    NIGHTS3 = db.Column(db.String, primary_key=True)
    NIGHTS4 = db.Column(db.String, primary_key=True)
    NIGHTS5 = db.Column(db.String, primary_key=True)
    NIGHTS6 = db.Column(db.String, primary_key=True)
    NIGHTS7 = db.Column(db.String, primary_key=True)
    NIGHTS8 = db.Column(db.String, primary_key=True)
    NUMADULTS = db.Column(db.String, primary_key=True)
    NUMDAYS = db.Column(db.String, primary_key=True)
    NUMNIGHTS = db.Column(db.String, primary_key=True)
    NUMPEOPLE = db.Column(db.String, primary_key=True)
    PACKAGEHOL = db.Column(db.String, primary_key=True)
    PACKAGEHOLUK = db.Column(db.String, primary_key=True)
    PERSONS = db.Column(db.String, primary_key=True)
    PORTROUTE = db.Column(db.String, primary_key=True)
    PACKAGE = db.Column(db.String, primary_key=True)
    PROUTELATDEG = db.Column(db.String, primary_key=True)
    PROUTELATMIN = db.Column(db.String, primary_key=True)
    PROUTELATSEC = db.Column(db.String, primary_key=True)
    PROUTELATNS = db.Column(db.String, primary_key=True)
    PROUTELONDEG = db.Column(db.String, primary_key=True)
    PROUTELONMIN = db.Column(db.String, primary_key=True)
    PROUTELONSEC = db.Column(db.String, primary_key=True)
    PROUTELONEW = db.Column(db.String, primary_key=True)
    PURPOSE = db.Column(db.String, primary_key=True)
    QUARTER = db.Column(db.String, primary_key=True)
    RESIDENCE = db.Column(db.String, primary_key=True)
    RESPNSE = db.Column(db.String, primary_key=True)
    SEX = db.Column(db.String, primary_key=True)
    SHIFTNO = db.Column(db.String, primary_key=True)
    SHUTTLE = db.Column(db.String, primary_key=True)
    SINGLERETURN = db.Column(db.String, primary_key=True)
    TANDTSI = db.Column(db.String, primary_key=True)
    TICKETCOST = db.Column(db.String, primary_key=True)
    TOWNCODE1 = db.Column(db.String, primary_key=True)
    TOWNCODE2 = db.Column(db.String, primary_key=True)
    TOWNCODE3 = db.Column(db.String, primary_key=True)
    TOWNCODE4 = db.Column(db.String, primary_key=True)
    TOWNCODE5 = db.Column(db.String, primary_key=True)
    TOWNCODE6 = db.Column(db.String, primary_key=True)
    TOWNCODE7 = db.Column(db.String, primary_key=True)
    TOWNCODE8 = db.Column(db.String, primary_key=True)
    TRANSFER = db.Column(db.String, primary_key=True)
    UKFOREIGN = db.Column(db.String, primary_key=True)
    VEHICLE = db.Column(db.String, primary_key=True)
    VISITBEGAN = db.Column(db.String, primary_key=True)
    WELSHNIGHTS = db.Column(db.String, primary_key=True)
    WELSHTOWN = db.Column(db.String, primary_key=True)
    AM_PM_NIGHT_PV = db.Column(db.String, primary_key=True)
    APD_PV = db.Column(db.String, primary_key=True)
    ARRIVEDEPART_PV = db.Column(db.String, primary_key=True)
    CROSSINGS_FLAG_PV = db.Column(db.String, primary_key=True)
    STAYIMPCTRYLEVEL1_PV = db.Column(db.String, primary_key=True)
    STAYIMPCTRYLEVEL2_PV = db.Column(db.String, primary_key=True)
    STAYIMPCTRYLEVEL3_PV = db.Column(db.String, primary_key=True)
    STAYIMPCTRYLEVEL4_PV = db.Column(db.String, primary_key=True)
    DAY_PV = db.Column(db.String, primary_key=True)
    DISCNT_F1_PV = db.Column(db.String, primary_key=True)
    DISCNT_F2_PV = db.Column(db.String, primary_key=True)
    DISCNT_PACKAGE_COST_PV = db.Column(db.String, primary_key=True)
    DUR1_PV = db.Column(db.String, primary_key=True)
    DUR2_PV = db.Column(db.String, primary_key=True)
    DUTY_FREE_PV = db.Column(db.String, primary_key=True)
    FAGE_PV = db.Column(db.String, primary_key=True)
    FARES_IMP_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    FARES_IMP_FLAG_PV = db.Column(db.String, primary_key=True)
    FLOW_PV = db.Column(db.String, primary_key=True)
    FOOT_OR_VEHICLE_PV = db.Column(db.String, primary_key=True)
    HAUL_PV = db.Column(db.String, primary_key=True)
    IMBAL_CTRY_FACT_PV = db.Column(db.String, primary_key=True)
    IMBAL_CTRY_GRP_PV = db.Column(db.String, primary_key=True)
    IMBAL_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    IMBAL_PORT_FACT_PV = db.Column(db.String, primary_key=True)
    IMBAL_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    IMBAL_PORT_SUBGRP_PV = db.Column(db.String, primary_key=True)
    LOS_PV = db.Column(db.String, primary_key=True)
    LOSDAYS_PV = db.Column(db.String, primary_key=True)
    MIG_FLAG_PV = db.Column(db.String, primary_key=True)
    MINS_CTRY_GRP_PV = db.Column(db.String, primary_key=True)
    MINS_CTRY_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    MINS_FLAG_PV = db.Column(db.String, primary_key=True)
    MINS_NAT_GRP_PV = db.Column(db.String, primary_key=True)
    MINS_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    MINS_QUALITY_PV = db.Column(db.String, primary_key=True)
    NR_FLAG_PV = db.Column(db.String, primary_key=True)
    NR_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    OPERA_PV = db.Column(db.String, primary_key=True)
    OSPORT1_PV = db.Column(db.String, primary_key=True)
    OSPORT2_PV = db.Column(db.String, primary_key=True)
    OSPORT3_PV = db.Column(db.String, primary_key=True)
    OSPORT4_PV = db.Column(db.String, primary_key=True)
    PUR1_PV = db.Column(db.String, primary_key=True)
    PUR2_PV = db.Column(db.String, primary_key=True)
    PUR3_PV = db.Column(db.String, primary_key=True)
    PURPOSE_PV = db.Column(db.String, primary_key=True)
    QMFARE_PV = db.Column(db.String, primary_key=True)
    RAIL_CNTRY_GRP_PV = db.Column(db.String, primary_key=True)
    RAIL_EXERCISE_PV = db.Column(db.String, primary_key=True)
    RAIL_IMP_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    REG_IMP_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    SAMP_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    SHIFT_FLAG_PV = db.Column(db.String, primary_key=True)
    SHIFT_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    SPEND_IMP_FLAG_PV = db.Column(db.String, primary_key=True)
    SPEND_IMP_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    STAY_IMP_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    STAY_IMP_FLAG_PV = db.Column(db.String, primary_key=True)
    STAY_PURPOSE_GRP_PV = db.Column(db.String, primary_key=True)
    TOWNCODE_PV = db.Column(db.String, primary_key=True)
    TOWN_IMP_ELIGIBLE_PV = db.Column(db.String, primary_key=True)
    TYPE_PV = db.Column(db.String, primary_key=True)
    UK_OS_PV = db.Column(db.String, primary_key=True)
    UKPORT1_PV = db.Column(db.String, primary_key=True)
    UKPORT2_PV = db.Column(db.String, primary_key=True)
    UKPORT3_PV = db.Column(db.String, primary_key=True)
    UKPORT4_PV = db.Column(db.String, primary_key=True)
    UNSAMP_PORT_GRP_PV = db.Column(db.String, primary_key=True)
    UNSAMP_REGION_GRP_PV = db.Column(db.String, primary_key=True)
    WEEKDAY_END_PV = db.Column(db.String, primary_key=True)
    DIRECT = db.Column(db.String, primary_key=True)
    EXPENDITURE_WT = db.Column(db.String, primary_key=True)
    EXPENDITURE_WTK = db.Column(db.String, primary_key=True)
    FAREKEY = db.Column(db.String, primary_key=True)
    OVLEG = db.Column(db.String, primary_key=True)
    SPEND = db.Column(db.String, primary_key=True)
    SPEND1 = db.Column(db.String, primary_key=True)
    SPEND2 = db.Column(db.String, primary_key=True)
    SPEND3 = db.Column(db.String, primary_key=True)
    SPEND4 = db.Column(db.String, primary_key=True)
    SPEND5 = db.Column(db.String, primary_key=True)
    SPEND6 = db.Column(db.String, primary_key=True)
    SPEND7 = db.Column(db.String, primary_key=True)
    SPEND8 = db.Column(db.String, primary_key=True)
    SPEND9 = db.Column(db.String, primary_key=True)
    SPENDIMPREASON = db.Column(db.String, primary_key=True)
    SPENDK = db.Column(db.String, primary_key=True)
    STAY = db.Column(db.String, primary_key=True)
    STAYK = db.Column(db.String, primary_key=True)
    STAY1K = db.Column(db.String, primary_key=True)
    STAY2K = db.Column(db.String, primary_key=True)
    STAY3K = db.Column(db.String, primary_key=True)
    STAY4K = db.Column(db.String, primary_key=True)
    STAY5K = db.Column(db.String, primary_key=True)
    STAY6K = db.Column(db.String, primary_key=True)
    STAY7K = db.Column(db.String, primary_key=True)
    STAY8K = db.Column(db.String, primary_key=True)
    STAY9K = db.Column(db.String, primary_key=True)
    STAYTLY = db.Column(db.String, primary_key=True)
    STAY_WT = db.Column(db.String, primary_key=True)
    STAY_WTK = db.Column(db.String, primary_key=True)
    TYPEINTERVIEW = db.Column(db.String, primary_key=True)
    UKLEG = db.Column(db.String, primary_key=True)
    VISIT_WT = db.Column(db.String, primary_key=True)
    VISIT_WTK = db.Column(db.String, primary_key=True)
    SHIFT_WT = db.Column(db.String, primary_key=True)
    NON_RESPONSE_WT = db.Column(db.String, primary_key=True)
    MINS_WT = db.Column(db.String, primary_key=True)
    TRAFFIC_WT = db.Column(db.String, primary_key=True)
    UNSAMP_TRAFFIC_WT = db.Column(db.String, primary_key=True)
    IMBAL_WT = db.Column(db.String, primary_key=True)
    FINAL_WT = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '<SurveySubsample {RUN_ID}>'.format(name=self.RUN_ID)
