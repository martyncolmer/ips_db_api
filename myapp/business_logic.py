from flask import request, Blueprint
from myapp.app_methods import get_connection, get_engine
from flask import Flask, jsonify, request, abort
from myapp.models import db, Run
import pandas
import myapp.persistence_layer as p_layer


def get_run(run_id=False):
    data = p_layer.get('RUN')

    column_names = data.columns
    output = None

    # if a run id is provided search for this specific run
    if run_id:
        # This is not and may not need to be implemented as it is dealt with user side
        pass
    else:

        output = data.to_json(orient='records')

    return output


def create_run():
    # Check if the request contains json data and an id (these must be present)
    if not request.json or 'RUN_ID' not in request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN', eng, if_exists='append', index=False)

    return "", 201


def edit_run(run_id):
    # Check if the request contains json data and an id (these must be present)
    if not request.json or not run_id:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    # Deletes old run instance from database before inserting updated version
    p_layer.delete_from_table('RUN', 'RUN_ID', '=', str(df['RUN_ID'][0]))

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN', eng, if_exists='append', index=False)

    return "", 200
