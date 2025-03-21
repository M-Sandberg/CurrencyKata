import pandas as pd
import sqlite3


def select(sql: str, params: tuple = (), return_as_pandas: bool = False):
    """
    Executes a SQL query with parameters and returns the result as either a list of dictionaries
    or a pandas DataFrame based on the return_as_pandas flag.

    Parameters:
        sql (str): The SQL query to be executed.
        params (tuple, optional): Parameters to be used in the SQL query.
        return_as_pandas (bool, optional): If True, return a pandas DataFrame; otherwise, return a list of dicts.

    Returns:
        Union[list[dict], pd.DataFrame]: Query result in the specified format.
    """
    with sqlite3.connect("db.sqlite3") as conn:
        if return_as_pandas:
            return pd.read_sql_query(sql, conn, params=params)
        else:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [{col: row[i] for i, col in enumerate(columns)} for row in rows]


def insert(table: str, df: pd.DataFrame, if_exists: str = "append") -> int:
    """
    Inserts a pandas DataFrame into a specified SQLite table.

    Args:
        table (str): The name of the table to insert data into.
        df (pd.DataFrame): The DataFrame containing the data to be inserted.
        if_exists (str, optional): The behavior when the table already exists.
            Defaults to "append". Options are:
            - 'fail': Raise a ValueError.
            - 'replace': Drop the table before inserting new values.
            - 'append': Insert new values to the existing table.

    Returns:
        int: The number of rows inserted into the table.
    """
    with sqlite3.connect("db.sqlite3") as conn:
        return df.to_sql(table, conn, if_exists=if_exists, index=False)
