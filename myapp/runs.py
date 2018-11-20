from flask import request, Blueprint
from myapp.app_methods import get_connection
from flask import Flask, jsonify, request, abort
from myapp.models import db, Run

bp = Blueprint('runs', __name__, url_prefix='/runs', static_folder='static')

# RUNS


@bp.route('', methods=['POST'])
def create_run():
    # the request should be json and an id must be present
    if not request.json or 'id' not in request.json:
        abort(400)

    run = Run(id=request.json['id'],
              name=request.json['name'],
              desc=request.json.get('desc', ""),
              start_date=request.json.get('start_date', ""),
              end_date=request.json.get('end_date', ""),
              status=request.json.get('status', ""),
              type=request.json.get('type', ""))
    db.session.add(run)
    db.session.commit()

    return "", 201


# @bp.route('', methods=['GET'])
# @bp.route('/<run_id>', methods=['GET'])
# def get_runs(run_id=None):
#     column_names = ['id', 'name', 'desc', 'start_date', 'end_date', 'status', 'type']
#     # if a run id is provided search for this specific run
#     if run_id:
#         # Get a single record
#         data = Run.query.get(run_id)
#         if not data:
#             abort(400)
#         output = {}
#         for name in column_names:
#             output[name] = getattr(data, name)
#     else:
#         # Get all records
#         data = Run.query.all()
#         output = []
#         for rec in data:
#             output_record = {}
#             for name in column_names:
#                 output_record[name] = getattr(rec, name)
#             output.append(output_record)
#
#     return jsonify(output)


@bp.route('/<run_id>', methods=['PUT'])
def update_run(run_id):
    # the request should be json and an id must be present
    if not request.json or not run_id:
        abort(400)

    data = Run.query.get(run_id)

    if not data:
        abort(400)

    data.name = request.json['name']
    data.desc = request.json.get('desc', "")
    data.start_date = request.json.get('start_date', "")
    data.end_date = request.json.get('end_date', "")
    data.status = request.json.get('status', "")
    data.type = request.json.get('type', "")

    db.session.commit()

    return "", 200






@bp.route('', methods=['GET'])
@bp.route('/<run_id>', methods=['GET'])
def get_runs(run_id=None):
    output = b_logic_get_run()

    return output

# Logic


def b_logic_get_run(run_id=False):

    data = p_layer_get('RUN')

    column_names = data.columns
    output = None
    # if a run id is provided search for this specific run
    if run_id:
        pass
        # Get a single record
        # data = Run.query.get(run_id)
        # if not data:
        #     abort(400)
        # output = {}
        # for name in column_names:
        #     output[name] = getattr(data, name)
    else:

        output = data.to_json(orient='records')

    return output


def p_layer_get(table_name):
    conn = get_connection()

    # Create SQL statement
    sql = "SELECT * from " + table_name

    # Execute the sql statement using the pandas.read_sql function and return
    # the result.
    import pandas
    return pandas.read_sql(sql, conn)
