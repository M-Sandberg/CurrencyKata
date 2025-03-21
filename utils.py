import pandas as pd
import sqlite3


def list_select(sql: str) -> list:
    """
    Executes a given SQL query and returns the result as a list of dictionaries.

    Args:
        sql (str): The SQL query to be executed.

    Returns:
        list: A list of dictionaries where each dictionary represents a row from the query result.
              The keys of the dictionary are the column names and the values are the corresponding
              row values.
    """
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [{col: row[i] for i, col in enumerate(columns)} for row in rows]


def pd_select(sql: str) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a pandas DataFrame.

    Parameters:
    sql (str): The SQL query to be executed.

    Returns:
    pd.DataFrame: The result of the SQL query as a pandas DataFrame.
    """
    with sqlite3.connect("db.sqlite3") as conn:
        return pd.read_sql_query(sql, conn)


def list_insert(table: str, data: list, if_exists: str = "fail") -> int:
    """
    Inserts a list of dictionaries into a specified SQLite table.

    Args:
        table (str): The name of the table to insert data into.
        data (list): A list of dictionaries where each dictionary represents a row to be inserted.
        if_exists (str, optional): Specifies the behavior when a row with the same primary key already exists.
                                   Options are "fail" (default) to raise an error, or "replace" to replace the existing row.

    Returns:
        int: The row ID of the last inserted row.

    Raises:
        sqlite3.IntegrityError: If `if_exists` is set to "fail" and a row with the same primary key already exists.
    """
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(data[0]))
        columns = ", ".join(data[0].keys())
        if if_exists == "replace":
            sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        else:
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.executemany(sql, [tuple(d.values()) for d in data])
        conn.commit()
        return cursor.lastrowid


def pd_insert(table: str, df: pd.DataFrame, if_exists: str = "fail") -> int:
    """
    Inserts data from a pandas DataFrame into a SQLite database table.

    Parameters:
    table (str): The name of the table to insert data into.
    df (pd.DataFrame): The DataFrame containing the data to be inserted.
    if_exists (str, optional): Specifies the behavior when the table already contains data.
                               Options are "fail" (default) or "replace".

    Returns:
    int: The row ID of the last inserted row.

    Raises:
    sqlite3.DatabaseError: If an error occurs while interacting with the database.
    """
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(df.columns))
        columns = ", ".join(df.columns)
        if if_exists == "replace":
            sql = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        else:
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor.executemany(sql, df.values.tolist())
        conn.commit()
        return cursor.lastrowid
