from flask import Flask, jsonify

from myapp.models import db, Respondent

app = Flask(__name__)

# Configuration needed by SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instead of using db = SQLAlchemy(app)
db.init_app(app)


@app.route('/respondents')
@app.route('/respondents/<int:id>')
def get_respondents(id=None):

    column_names = ['name', 'email', 'age']

    if id:
        # Get a single record
        data = Respondent.query.get(id)
        output = {}
        for name in column_names:
            output[name] = getattr(data, name)
    else:
        # Get all records
        data = Respondent.query.all()

        output = []
        for rec in data:
            output_record = {}
            for name in column_names:
                output_record[name] = getattr(rec, name)
                output.append(output_record)

    return jsonify(output)

