
from flask_sqlalchemy import SQLAlchemy

# This class provided by flask-sqlalchemy can be used to access all other
# SQLAlchemy building blocks when defining the database model class
# More details at http://flask-sqlalchemy.pocoo.org/2.3/
db = SQLAlchemy()

# Defining the Model class that maps to the database schema
class Respondent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    blood_type = db.Column(db.String(3))

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<Respondent {name}>'.format(name=self.name)
