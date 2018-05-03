
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

    # A helper function that defines how a record will be displayed
    # in the console
    def __repr__(self):
        return '<Run {name}>'.format(name=self.name)
