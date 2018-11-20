#import pyodbc
import os
import pytds

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
        conn = 0 #pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=username, pwd=password, autocommit=True)
        conn = pytds.connect(dsn=server, database=database, user=username, password=password, autocommit=True)
        #conn = pyodbc.connect(driver="{SQL Server}", server=server, database=database, uid=username, pwd=password, autocommit=True)
    except Exception as err:
        # database_logger().error(err, exc_info = True)
        print(err)
        return 'ERROR GETTING CONNECTION'
        return False
    else:
        return conn
