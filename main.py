from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
from db import *
import uvicorn


# Define the FastAPI application
app = FastAPI()

# Define a Pydantic model for the data
class SourceData(BaseModel):
    source: str
    source_tag: str
    source_type: str
    from_date: str
    to_date: str
    last_update_date: str
    frequency: str



class UpdateSourceData(BaseModel):
    source_id: int
    from_date: str
    to_date: str
    last_update_date: str 


# API endpoint to get data for a given source
@app.get("/get_data")
def get_data(source_id: int) -> dict:
    conn = connect_to_database()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM source_data WHERE source_id = %s", (source_id,))
        rows = cur.fetchall()
        if rows == []:
            return {"Output":"Source Id does not exist"}
        row = rows[0]
        data = {"source_id":row[0],
                "source":row[1],
                "source_type":row[2],
                "source_tag":row[3],
                "last_update_date":row[4].strftime("%Y-%m-%d %H:%M:%S"),
                "from_date":row[5].strftime("%Y-%m-%d %H:%M:%S"),
                "to_date":row[6].strftime("%Y-%m-%d %H:%M:%S"),
                "frequency":row[7]
        }
        return data
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Error fetching data from the database.") from e
    finally:
        conn.close()



# API endpoint to get data for a given source with updated from_date and to_date
@app.get("/get_data_trigger")
def get_data_trigger(source_id: int) -> dict:
    conn = connect_to_database()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM source_data WHERE source_id = %s", (source_id,))
        rows = cur.fetchall()
        if rows == []:
            return {"Output":"Source Id does not exist"}
        row = rows[0]
        frequency = int(row[7][:-1])
        data = {"source_id":row[0],
                "source":row[1],
                "source_type":row[2],
                "source_tag":row[3],
                "last_update_date":row[4].strftime("%Y-%m-%d %H:%M:%S"),
                "from_date":(row[5] + timedelta(minutes=frequency)).strftime("%Y-%m-%d %H:%M:%S"),
                "to_date":(row[6] + timedelta(minutes=frequency)).strftime("%Y-%m-%d %H:%M:%S"),
                "frequency":row[7]
        }
        return data
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Error Fetching data from the database.") from e
    finally:
        conn.close()



# API endpoint to update from_date, to_date, and last_update_date
@app.put("/update_data")
def update_data(update_source_data: UpdateSourceData) -> dict:
    try:
        # Convert date strings to datetime objects
        from_date = datetime.strptime(update_source_data.from_date, "%Y-%m-%d %H:%M:%S")
        to_date = datetime.strptime(update_source_data.to_date, "%Y-%m-%d %H:%M:%S")
        last_update_date = datetime.strptime(update_source_data.last_update_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect date format. Date format should be 'YYYY-MM-DD HH:MM:SS'.")

    conn = connect_to_database()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM source_data WHERE source_id = %s", (update_source_data.source_id,))
        rows = cur.fetchall()
        if rows == []:
            return {"Output":"Source Id does not exist"}
        cur.execute(
            "UPDATE source_data SET from_date = %s, to_date = %s, last_update_date = %s WHERE source_id = %s",
            (from_date, to_date, last_update_date, update_source_data.source_id)
        )
        conn.commit()
        return {"status": "success"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Error updating data in the database.") from e
    finally:
        conn.close()


# API endpoint to add a new record
@app.post("/add_data")
def add_data(source_data: SourceData) -> dict:
    try:
        # Convert date strings to datetime objects
        from_date = datetime.strptime(source_data.from_date, "%Y-%m-%d %H:%M:%S")
        to_date = datetime.strptime(source_data.to_date, "%Y-%m-%d %H:%M:%S")
        last_update_date = datetime.strptime(source_data.last_update_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail="Incorrect date format. Date format should be 'YYYY-MM-DD HH:MM:SS'.")

    if not source_data.frequency[:-1].isdigit():
        raise HTTPException(status_code=400, detail="Incorrect frequency format. Frequency format should be a integer followed by M.")
    if not source_data.frequency[-1]=="M":
        raise HTTPException(status_code=400, detail="Incorrect frequency format. Frequency format should be a integer followed by M.")

    conn = connect_to_database()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO source_data (source, source_tag, source_type, from_date, to_date, last_update_date, frequency) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (source_data.source, source_data.source_tag, source_data.source_type, from_date, to_date, last_update_date, source_data.frequency)
        )
        conn.commit()
        return {"status": "success"}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail="Error adding data to the database.") from e
    finally:
        conn.close()

# Create the table on startup
create_table()




# Close the database connection when the application stops
@app.on_event("shutdown")
def shutdown_event():
    cur.close()
    conn.close()

# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
