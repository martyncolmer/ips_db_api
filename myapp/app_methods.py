import pyodbc
import os
from sqlalchemy import create_engine
import pandas


def get_connection():
    """
    Author       : Thomas Mahoney
    Date         : 03 / 04 / 2018
    Purpose      : Establishes a connection to the SQL Server database and returns the connection object.
    Parameters   : in_table_name - the IPS survey records for the period.
                   credentials_file  - file containing the server and login credentials used for connection.
    Returns      : pyodbc connection object
    Requirements : NA
    Dependencies : NA
    """

    # Get credentials and decrypt
    username = os.getenv("DB_USER_NAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    server = os.getenv("DB_SERVER")

    if not username or not password or not database or not server:
        return "No Credentials"

    # Attempt to connect to the database
    try:
        conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=username, pwd=password, autocommit=True)
        #conn = #pytds.connect(dsn=server, database=database, user=username, password=password, autocommit=True)
        #conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=username, pwd=password, autocommit=True)
    except Exception as err:
        # database_logger().error(err, exc_info = True)
        print(err)
        return 'ERROR GETTING CONNECTION'
        return False
    else:
        return conn


def get_engine():
    username = os.getenv("DB_USER_NAME")
    password = os.getenv("DB_PASSWORD")
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")

    connection_string = r'mssql+pyodbc://' + username + \
                        r':' + password + \
                        r'@' + server + \
                        r'/' + database + \
                        r'?driver=SQL+Server+Native+Client+11.0'

    eng = create_engine(connection_string)
    return eng


def extract_data(df):
    """
    Author       : Thomas Mahoney
    Date         : 26 / 04 / 2018
    Purpose      : Extracts the required columns from the import data.
    Parameters   : df - the dataframe containing all of the import data.
    Returns      : The extracted dataframe.
    Requirements : NA
    Dependencies : NA
    """

    # Generate a list of the required columns
    columns = ['SERIAL', 'AM_PM_NIGHT', 'AGE', 'ANYUNDER16', 'APORTLATDEG',
               'APORTLATMIN', 'APORTLATSEC', 'APORTLATNS', 'APORTLONDEG',
               'APORTLONMIN', 'APORTLONDSEC', 'APORTLONEW', 'ARRIVEDEPART',
               'BABYFARE', 'BEFAF','CHILDFARE', 'CHANGECODE', 'COUNTRYVISIT',
               'CPORTLATDEG', 'CPORTLATMIN', 'CPORTLATSEC', 'CPORTLATNS',
               'CPORTLONDEG', 'CPORTLONMIN', 'CPORTLONDSEC', 'CPORTLONEW',
               'INTDATE', 'DAYTYPE', 'DIRECTLEG', 'DVEXPEND', 'DVFARE',
               'DVLINECODE', 'DVPACKAGE', 'DVPACKCOST', 'DVPERSONS', 'DVPORTCODE',
               'EXPENDCODE', 'EXPENDITURE', 'FARE','FAREK', 'FLOW', 'HAULKEY',
               'INTENDLOS', 'INTMONTH', 'KIDAGE', 'LOSKEY', 'MAINCONTRA', 'MIGSI',
               'NATIONALITY', 'NATIONNAME', 'NIGHTS1', 'NIGHTS2', 'NIGHTS3', 'NIGHTS4',
               'NIGHTS5', 'NIGHTS6', 'NIGHTS7', 'NIGHTS8', 'NUMADULTS', 'NUMDAYS',
               'NUMNIGHTS', 'NUMPEOPLE', 'PACKAGEHOL', 'PACKAGEHOLUK', 'PERSONS',
               'PORTROUTE', 'PACKAGE', 'PROUTELATDEG', 'PROUTELATMIN', 'PROUTELATSEC',
               'PROUTELATNS', 'PROUTELONDEG', 'PROUTELONMIN', 'PROUTELONSEC',
               'PROUTELONEW', 'PURPOSE', 'QUARTER', 'RESIDENCE', 'RESPNSE',
               'SEX', 'SHIFTNO','SHUTTLE', 'SINGLERETURN', 'TANDTSI', 'TICKETCOST',
               'TOWNCODE1', 'TOWNCODE2', 'TOWNCODE3', 'TOWNCODE4', 'TOWNCODE5',
               'TOWNCODE6', 'TOWNCODE7', 'TOWNCODE8', 'TRANSFER', 'UKFOREIGN',
               'VEHICLE', 'VISITBEGAN', 'WELSHNIGHTS', 'WELSHTOWN', 'FAREKEY',
               'TYPEINTERVIEW', 'SHIFT_WT']#TODO: remove shift_wt here this is required for non-response step

    # Set the imported columns to be uppercase
    df.columns = df.columns.str.upper()

    # Sort the data by serial number
    df_new = df.sort_values(by='SERIAL')

    # Recreate the dataframe using only the specified columns
    df_new = df_new.filter(columns, axis=1)

    return df_new

#
# def import_survey_data(survey_data_path, run_id):
#     """
#     Author       : Thomas Mahoney
#     Date         : 26 / 04 / 2018
#     Purpose      : Loads the import data into a dataframe then appends the data to the 'SURVEY_SUBSAMPLE'
#                    table on the connected database.
#     Parameters   : survey_data_path - the dataframe containing all of the import data.
#                    run_id - the generated run_id for the current run.
#                    version_id - ID indicating the current version
#     Returns      : NA
#     Requirements : Datafile is of type '.csv', '.pkl' or '.sas7bdat'
#     Dependencies : NA
#     """
#
#     # Check the survey_data_path's suffix to see what it matches then extract using the appropriate method.
#     if survey_data_path[-3:] == "csv":
#         df = pd.read_csv(survey_data_path, engine='python')
#
#     # Fill left side of INTDATE column with an additional 0 if length less than 8 characters
#     df.columns = df.columns.str.upper()
#     if 'INTDATE' in df.columns:
#         df['INTDATE'] = df['INTDATE'].astype(str).str.rjust(8, '0')
#
#     # Call the extract data function to select only the needed columns.
#     df_survey_data = extract_data(df)
#
#     # Add the generated run id to the dataset.
#     df_survey_data['RUN_ID'] = pandas.Series(run_id, index=df_survey_data.index)
#
#     # Insert the imported data into the survey_subsample table on the database.
#     p_layer.insert_dataframe_into_table('SURVEY_SUBSAMPLE', df_survey_data)
#
#
# def import_traffic_data(run_id, filename):
#     """
#     Author        : Elinor Thorne
#     Date          : 27 Nov 2017
#     Purpose       : Imports CSV (Sea, CAA, Tunnel Traffic, Possible Shifts,
#                     Non Response or Unsampled) and inserts to Oracle
#     Parameters    : filename - full directory path to CSV
#     Returns       : True or False
#     Requirements  : pip install pandas
#     Dependencies  : CommonFunctions.import_csv()
#                     CommonFunctions.validate_csv()
#                     CommonFunctions.get_sql_connection()
#                     CommonFunctions.select_data()
#     """
#
#     # Connection variables
#     conn = p_layer.get_connection()
#     cur = conn.cursor()
#
#     # Convert CSV to dataframe and stage
#     dataframe = pandas.read_csv(filename)
#     dataframe.columns = dataframe.columns.str.upper()
#     dataframe.columns = dataframe.columns.str.replace(' ', '')
#     dataframe["RUN_ID"] = run_id
#     dataframe.rename(columns={"DATASOURCE": "DATA_SOURCE_ID"}, inplace=True)
#     dataframe = dataframe.fillna('')
#
#     # replace "REGION" values with 0 if not an expected value
#     if "REGION" in dataframe.columns:
#         dataframe['REGION'].replace(['None', "", ".", 'nan'], 0, inplace=True)
#
#     # Get datasource values and replace with new datasource_id
#     datasource = dataframe.at[1, 'DATA_SOURCE_ID']
#     datasource_id = p_layer.select_data("DATA_SOURCE_ID"
#                                        , "DATA_SOURCE"
#                                        , "DATA_SOURCE_NAME"
#                                        , datasource)
#     dataframe['DATA_SOURCE_ID'].replace([datasource], datasource_id, inplace=True)
#
#     # Select appropriate table name (value) based on data source (key)
#     table_name_dict = {"Sea": "TRAFFIC_DATA",
#                        "Air": "TRAFFIC_DATA",
#                        "Tunnel": "TRAFFIC_DATA",
#                        "Shift": "SHIFT_DATA",
#                        "Non Response": "NON_RESPONSE_DATA",
#                        "Unsampled": "UNSAMPLED_OOH_DATA"}
#     table_name = table_name_dict[datasource]
#
#     # Cleansing
#     if table_name == 'TRAFFIC_DATA':
#         dataframe["VEHICLE"] = 0
#         dataframe['AM_PM_NIGHT'] = dataframe[['AM_PM_NIGHT']].convert_objects(convert_numeric=True).replace("", float('nan'))
#
#         sql = """
#         DELETE FROM [TRAFFIC_DATA]
#         WHERE RUN_ID = '{}'
#         AND DATA_SOURCE_ID = '{}'
#         """.format(run_id, datasource_id)
#     else:
#         sql = """
#         DELETE FROM [{}]
#         WHERE RUN_ID = '{}'
#         """.format(table_name, run_id)
#
#     cur.execute(sql)
#
#     # Insert dataframe to table
#     p_layer.insert_dataframe_into_table(table_name, dataframe)
