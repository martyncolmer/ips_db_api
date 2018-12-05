import pandas
import json
from flask import request, abort
import myapp.persistence_layer as p_layer
from myapp.app_methods import get_engine


# RUNS

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


# RUN_STEPS

def get_run_steps(run_id=None):

    data = p_layer.get('RUN_STEPS')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if data.empty:
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

    # Deletes run_steps records for the active run before inserting updated step data
    p_layer.delete_from_table('RUN_STEPS', 'RUN_ID', '=', str(df['RUN_ID'][0]))

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RUN_STEPS', eng, if_exists='append', index=False)

    return "", 201


def edit_run_steps(run_id, value, step_number=None):

    if not run_id:
        abort(400)

    if not value:
        abort(400)

    df = p_layer.get('RUN_STEPS')

    df = df.loc[df['RUN_ID'] == run_id]

    if step_number:
        df.loc[df['STEP_NUMBER'] == float(step_number), 'STEP_STATUS'] = float(value)
    else:
        df.STEP_STATUS = value

    df.index = range(0, len(df))

    # Deletes run_steps records for the active run before inserting updated step data
    p_layer.delete_from_table('RUN_STEPS', 'RUN_ID', '=', str(df['RUN_ID'][0]))

    # Writes new data to sql
    eng = get_engine()
    df.to_sql('RUN_STEPS', eng, if_exists='append', index=False)

    return "", 200


# RESPONSE - These need testing as we couldn't connect to each other properly

def get_response(run_id):

    data = p_layer.get('RESPONSE')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if data.empty:
            abort(400)

    output = data.to_json(orient='records')

    return output


def create_response():
    if not request.json or 'RUN_ID' not in request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('RESPONSE', eng, if_exists='append', index=False)

    return "", 201


# PROCESS VARIABLE

def get_process_variables(run_id=None):

    data = p_layer.get('PROCESS_VARIABLE_PY')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if data.empty:
            abort(400)
    data.sort_values('PROCESS_VARIABLE_ID', inplace=True)
    data.index = range(0, len(data))
    output = data.to_json(orient='records')

    return output


def create_process_variables(run_id):

    # Check if the request contains json data and an id (these must be present)
    if not request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data)

    df.index = range(0, len(df))

    if df.empty:
        abort(400)

    df['RUN_ID'] = run_id

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('PROCESS_VARIABLE_PY', eng, if_exists='append', index=False)

    return "", 201


def delete_process_variables(run_id=None):
    p_layer.delete_from_table('PROCESS_VARIABLE_PY', 'RUN_ID', '=', run_id)

    return "", 200


# PROCESS VARIABLE SETS

def create_pv_set():
    # Check if the request contains json data and an id (these must be present)
    if not request.json or 'RUN_ID' not in request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data, index=[0])

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('PROCESS_VARIABLE_SET', eng, if_exists='append', index=False)

    return "", 201


def get_pv_sets():

    data = p_layer.get('PROCESS_VARIABLE_SET')

    output = data.to_json(orient='records')

    return output


def delete_pv_set(run_id=None):
    p_layer.delete_from_table('PROCESS_VARIABLE_SET', 'RUN_ID', '=', run_id)

    return "", 200


# EXPORT DATA DOWNLOAD

def create_export_data_download():
    if not request.data:
        abort(400)

    # Get json dictionary and values
    json_data = json.loads(request.data)

    data = []

    rec = {'RUN_ID': json_data['RUN_ID'],
           'DOWNLOADABLE_DATA': json_data['DOWNLOADABLE_DATA'],
           'FILENAME': json_data['FILENAME'],
           'SOURCE_TABLE': json_data['SOURCE_TABLE'],
           'DATE_CREATED': json_data['DATE_CREATED']}

    data.append(rec)

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data)

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql('EXPORT_DATA_DOWNLOAD', eng, if_exists='append', index=False)

    return "", 201


def get_export_data_download(run_id, file_name, source_table):
    data = p_layer.get('EXPORT_DATA_DOWNLOAD')

    if data.empty:
        abort(400)

    if run_id:
        data = data.loc[data['RUN_ID'] == run_id]

        if data.empty:
            abort(400)

    if file_name:
        data = data.loc[data['FILENAME'] == file_name]

    if source_table:
        data = data.loc[data['SOURCE_TABLE'] == source_table]

    output = data.to_json(orient='records')

    return output


# DATA

def get_data(run_id, table_name):
    data = p_layer.select_data('*', table_name, 'RUN_ID', run_id)

    if data.empty:
        abort(400)

    data.sort_values('RUN_ID', inplace=True)
    data.index = range(0, len(data))

    output = data.to_json(orient='records')

    return output


# IMPORT DATA

# @TODO: This doesn't work due to errors with the data being converted through the FileStorage object (needs investigation)

def import_data(run_id, table_name, filepath):

    # Check if the request contains json data and an id (these must be present)
    if not request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data)

    df.index = range(0, len(df))

    if df.empty:
        abort(400)

    p_layer.delete_from_table(table_name, 'RUN_ID', '=', run_id)

    df['RUN_ID'] = run_id

    p_layer.insert_dataframe_into_table(table_name=table_name, dataframe=df)

    # Writes data frame to sql
    # eng = get_engine()
    # df.to_sql(table_name, eng, if_exists='append', index=False)

    return "", 201


def import_data_OLD(run_id, table_name):

    # Check if the request contains json data and an id (these must be present)
    if not request.json:
        abort(400)

    # Get data dictionary from the json request
    data = request.json

    # Convert the dictionary into data frame format
    df = pandas.DataFrame(data)

    df.index = range(0, len(df))

    if df.empty:
        abort(400)

    p_layer.delete_from_table(table_name, 'RUN_ID', '=', run_id)

    df['RUN_ID'] = run_id

    # Writes data frame to sql
    eng = get_engine()
    df.to_sql(table_name, eng, if_exists='append', index=False)

    return "", 201
