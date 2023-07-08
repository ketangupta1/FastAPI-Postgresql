import psycopg2
from config import *


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=HOST,
    database=DB,
    user=USER,
    password=PASSWORD
)


# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Creating the source_data table
# Since in /add_data endpoint request body doe not contains source_id. 
# so I thought it should be auto generated so used SERIAL datatype for source_id
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS source_data (
            source_id SERIAL PRIMARY KEY,
            source VARCHAR(200),
            source_type VARCHAR(10),
            source_tag VARCHAR(10),
            last_update_date TIMESTAMP,
            from_date TIMESTAMP ,
            to_date TIMESTAMP,
            frequency VARCHAR(5)
        );
    """)
    conn.commit()