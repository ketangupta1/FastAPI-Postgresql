# FastAPI-Postgresql
Designed the python FastAPI Rest service to store and retrieve data from a PostgreSQL table.

##Install project dependencies: 
In the terminal or command prompt, ensure that you are in the project directory and run the following command to install the required dependencies:

    pip install fastapi pydantic psycopg2 uvicorn
    
This command will install the FastAPI, Pydantic, psycopg2, and uvicorn packages.


##Update the code: 
Open your preferred text editor or IDE and update the code with your PostgreSQL database connection details. Modify the connect_to_database() function to include the correct host, database name, username, and password.


##Run the application: 
In the terminal or command prompt, navigate to the directory containing the main Python file (main.py). Run the following command to start the FastAPI application:

    uvicorn main:app --reload
    
This command will start the FastAPI application and enable automatic reloading on code changes.


##Access the API endpoints: 
Once the application is running, you can access the API endpoints using a tool like Postman or fastApi Swagger UI (http://localhost:8000/docs) or a web browser. 
By default, the application will be available at http://localhost:8000 .
