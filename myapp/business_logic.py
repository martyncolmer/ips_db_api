import pandas
from flask import request, abort
import myapp.persistence_layer as p_layer
from myapp.app_methods import get_engine


def get_run(run_id=False):
    data = p_layer.get('RUN')

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


# Run_Steps

def get_run_steps(run_id=None):

    data = p_layer.get('RUN_STEPS')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if len(data) == 0:
            abort(400)

    output = data.to_json(orient='records')

    return output


def create_run_steps(run_id):

    steps = {1: 'Calculate Shift Weight',
             2: 'Calculate Non-Response Weight',
             3: 'Calculate Minimums Weight',
             4: 'Calculate Traffic Weight',
             5: 'Calculate Unsampled Weight',
             6: 'Calculate Imbalance Weight',
             7: 'Calculate Final Weight',
             8: 'Stay Imputation',
             9: 'Fares Imputation',
             10: 'Spend Imputation',
             11: 'Rail Imputation',
             12: 'Regional Weight',
             13: 'Town Stay and Expenditure Imputation',
             14: 'Air Miles',
             }

    if not run_id:
        abort(400)

    data = []

    for key, value in steps.items():
        rec = {'RUN_ID': run_id,
               'STEP_NUMBER': key,
               'STEP_NAME': value,
               'STEP_STATUS': 0}
        data.append(rec)

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data)

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN_STEPS', eng, if_exists='append', index=False)

    return "", 201

