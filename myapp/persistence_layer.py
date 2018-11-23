from myapp.app_methods import get_connection
import pandas


def get(table_name):
    conn = get_connection()

    # Create SQL statement
    sql = "SELECT * from " + table_name

    # Execute the sql statement using the pandas.read_sql function and return
    # the result.
    return pandas.read_sql(sql, conn)
