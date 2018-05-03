from flask import Flask, jsonify, request, abort

from myapp.models import db, Run

app = Flask(__name__)

# Configuration needed by SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ips_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instead of using db = SQLAlchemy(app)
db.init_app(app)


@app.route('/runs', methods=['GET'])
@app.route('/runs/<id>', methods=['GET'])
def get_runs(run_id=None):

    column_names = ['id', 'name', 'desc', 'start_date', 'end_date', 'status']

    if run_id:
        # Get a single record
        data = Run.query.get(run_id)
        output = {}
        for name in column_names:
            output[name] = getattr(data, name)
    else:
        # Get all records
        data = Run.query.all()

        output = []
        for rec in data:
            output_record = {}
            for name in column_names:
                output_record[name] = getattr(rec, name)
            output.append(output_record)

    return jsonify(output)


@app.route('/runs', methods=['POST'])
def create_run():
    if not request.json or 'id' not in request.json:
        abort(400)

    run = Run(id=request.json['id'],
              name=request.json['name'],
              desc=request.json.get('desc', ""),
              start_date=request.json.get('start_date', ""),
              end_date=request.json.get('end_date', ""))
    db.session.add(run)
    db.session.commit()

    return "", 201


