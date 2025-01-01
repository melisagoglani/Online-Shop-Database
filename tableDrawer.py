from prettytable import PrettyTable
import sqlite3

def printTable(data, columns=None):
    if isinstance(data, str):
        # If data is a table name, fetch data from the database
        with sqlite3.connect('OnlineShop.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM " + data)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
    else:
        # If data is a list of rows, use it directly
        rows = data
        if not rows:
            print("No data available.")
            return
        if columns is None:
            raise ValueError("Columns must be provided when data is a list of rows")

    table = PrettyTable(columns)
    for row in rows:
        table.add_row(row)
    print(table)