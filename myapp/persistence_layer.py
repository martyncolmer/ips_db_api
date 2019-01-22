from myapp.app_methods import get_connection
import pandas


def get(table_name):
    conn = get_connection()

    # Create SQL statement
    sql = "SELECT * from " + table_name

    # Execute the sql statement using the pandas.read_sql function and return
    # the result.
    return pandas.read_sql(sql, conn)


def get_pvs():
    conn = get_connection()

    # Create a cursor object from the connection
    cur = conn.cursor()

    # Specify the sql query for retrieving the process variable statements from the database
    sql = """SELECT 
                RUN_ID, PROCESS_VARIABLE_ID, PV_NAME, PV_DESC, PV_DEF
             FROM 
                PROCESS_VARIABLE_PY
             ORDER BY 
                PROCESS_VARIABLE_ID"""

    # Execute the sql query
    cur.execute(sql)

    data = cur.fetchall()

    # Return the pv statements obtained from the sql query
    return data


    sql = "select * from PROCESS_VARIABLE_PY"

    cur.execute(sql)

    data = cur.fetchall()
    vals = data.values
    columns = ['RUN_ID', 'PROCESS_VARIABLE_ID', 'PV_NAME', 'PV_DESC', 'PV_DEF']
    df = pandas.DataFrame(data)

    return df



def delete_from_table(table_name, condition1=None, operator=None
                      , condition2=None, condition3=None):
    """
    Author         : Elinor Thorne
    Date           : 7 Dec 2017
    Purpose        : Generic SQL query to delete contents of table
    Parameters     : table_name - name of table
                     condition1 - first condition / value
                     operator - comparison operator i.e
                     '=' Equal
                     '!=' Not Equal
                     '>' Greater than
                     '>=' Greater than or equal, etc
                     https://www.techonthenet.com/oracle/comparison_operators.php
                     condition2 - second condition / value
                     condition3 - third condition / value used for BETWEEN
                     ranges, i.e: "DELETE FROM table_name WHERE condition1
                     BETWEEN condition2 AND condition3"
    Returns         : True/False (bool)
    Requirements    : None
    Dependencies    : check_table(),
                      get_sql_connection,
    """

    # Oracle connection variables
    conn = get_connection()
    cur = conn.cursor()

    # Create and execute SQL query
    if condition1 == None:
        # DELETE FROM table_name
        sql = ("DELETE FROM " + table_name)
    elif condition3 == None:
        # DELETE FROM table_name WHERE condition1 <operator> condition2
        sql = ("DELETE FROM " + table_name
               + " WHERE " + condition1
               + " " + operator
               + " '" + condition2 + "'")
    else:
        # DELETE FROM table_name WHERE condition1 BETWEEN condition2 AND condition3
        sql = ("DELETE FROM " + table_name
               + " WHERE " + condition1
               + " " + operator
               + " '" + condition2 + "'"
               + " AND " + condition3)

    try:
        cur.execute(sql)
    except Exception as err:
        print("bla!")
        print(err)
        # database_logger().error(err, exc_info = True)
        return False
    else:
        return sql


def select_data(column_name, table_name, condition1, condition2):
    """
    Author        : Elinor Thorne
    Date          : 21 Dec 2017
    Purpose       : Uses SQL query to retrieve values from database
    Parameters    : column_name, table_name, condition1, condition2, i.e:
                  : "SELECT column_name FROM table_name WHERE condition1 = condition2" (no 'AND'/'OR' clause)
    Returns       : Data Frame for multiple values, scalar/string for single values
    Requirements  : None
    """

    # Connection variables
    conn = get_connection()
    # cur = conn.cursor()

    # Create SQL statement
    sql = """
        SELECT {} 
        FROM {}
        WHERE {} = '{}'
        """.format(column_name, table_name, condition1, condition2)

    try:
        result = pandas.read_sql(sql, conn)
        # print("Result: {}".format(result))
    except Exception as err:
        print(err)
        # Return False to indicate error
        # database_logger().error(err, exc_info = True)
        return pandas.DataFrame(pandas.DataFrame())

    # if an empty data frame is returned
    if len(result) == 0:
        # err_msg = "ERROR: SQL query failed to return result."
        return pandas.DataFrame(pandas.DataFrame())
    elif len(result) == 1:
        # if a single value is returned we don't want it to be a data frame
        result = result.loc[0, column_name]

    return result

