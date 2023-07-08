import psycopg2
from fastapi import HTTPException
from config import *


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=HOST,
    database=DB,
    user=USER,
    password=PASSWORD
)

# Connect to the PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DB,
            user=USER,
            password=PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Error connecting to the database.") from e



# Creating the source_data table
# Since in /add_data endpoint request body doe not contains source_id. 
# so I thought it should be auto generated so used SERIAL datatype for source_id

def create_table():
    conn = connect_to_database()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS source_data (
                source_id SERIAL PRIMARY KEY,
                source VARCHAR(200) NOT NULL,
                source_type VARCHAR(10) NOT NULL,
                source_tag VARCHAR(10) NOT NULL,
                last_update_date TIMESTAMP NOT NULL,
                from_date TIMESTAMP NOT NULL,
                to_date TIMESTAMP NOT NULL,
                frequency VARCHAR(5) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Error creating the table.") from e
    finally:
        conn.close()