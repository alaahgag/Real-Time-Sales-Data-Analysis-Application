import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """
    - Connects to the default database.
    - Creates the 'sales' database if it doesn't exist.
    - Returns the connection and cursor to 'sales'.
    """

    # Connect to the default database
    conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=your_password")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Check if 'sales' database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname='sales'")
    exists = cur.fetchone()

    if not exists:
        # Create 'sales' database with UTF8 encoding if it doesn't exist
        cur.execute("CREATE DATABASE sales WITH ENCODING 'utf8' TEMPLATE template0")

    # Close the connection to the default database
    conn.close()

    # Connect to 'sales' database
    conn = psycopg2.connect("host=localhost dbname=sales user=postgres password=your_password")
    cur = conn.cursor()

    return cur, conn

tables_name = ['sales', 'stocks']

def drop_tables(cur, conn):
    """
    Drops each table.
    """
    for i in tables_name:
        cur.execute('DROP TABLE IF EXISTS {}'.format(i))
        conn.commit()

def create_tables(cur, conn):
    """
    Creates each table using predefined queries.
    """
    
    sales_table = """CREATE TABLE IF NOT EXISTS sales(
Sale_ID int,
Product varchar(40),
Quantity_Sold int,
Each_Price float,
Sales float,
Date date,
Day int,
Month int,
Year int)"""

    stock_table = """
    CREATE TABLE IF NOT EXISTS stocks(
    Product VARCHAR(40),
    Stock_Quantity INT,
    Total_Quantity_Sold INT)"""

    tables = [sales_table, stock_table]

    for i in tables:
        cur.execute(i)
        conn.commit()

def sales_DB_Schema():
    """
    - Creates the 'sales' database if it doesn't exist.
    - Establishes connection with the 'sales' database and gets
      a cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    sales_DB_Schema()