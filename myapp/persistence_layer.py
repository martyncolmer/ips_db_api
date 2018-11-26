from myapp.app_methods import get_connection, get_engine
import pandas


def get(table_name):
    conn = get_connection()

    # Create SQL statement
    sql = "SELECT * from " + table_name

    # Execute the sql statement using the pandas.read_sql function and return
    # the result.
    return pandas.read_sql(sql, conn)


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
