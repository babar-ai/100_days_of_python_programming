from sqlmodel import create_engine, SQLModel      #engine holds the connections to the database.


# step : 3
# Database configuration
# creating a SQLite engine in SQLMode
#  sqlite:///... is the standard URI for SQLite file-based DBs.

sqlite_file_name = "Database.db"
DATABASE_URL = f"sqlite:///{sqlite_file_name}"

# Think of engine like the bridge between your Python code and your database.engine is your connection to the database.
# connect_args={"check_same_thread": False} lets multiple threads (like FastAPI's background processes) talk to the database.

engine = create_engine(
    DATABASE_URL,
    # echo=True,                                  # Log SQL queries (optional)
    connect_args={"check_same_thread": False} #optional  # Allow multi-threaded access
)
'''This function creates all the tables defined using SQLModel (like Hero, etc.).
It’s typically called once when the app starts (you did that in main.py under @app.on_event("startup")).
'''
#to create the tables for all the table models.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    