import mysql.connector
import os
from rich.console import Console
from os.path import join, dirname
from dotenv import load_dotenv

console = Console()
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
print("getting env vars")
db_host = os.getenv("DATABASE_HOST_NAME")
db_user = os.getenv("DATABASE_USER")
db_pwd = os.getenv("DATABASE_USER_PASSWORD")
db_port = os.getenv("DATABASE_PORT")

# Retrieve the SQL database connection object 
def databaseconfig():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pwd,
            port=db_port,
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )

    except Exception as e:
        console.print_exception(show_locals=True)

    return conn