from getpass import getpass
import hashlib
import random
import string
import sys
from utils.databaseconfig import databaseconfig
from rich.console import Console
from rich import print as rprint

console = Console() 

def genDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def config():
    db = databaseconfig()

    # Cursor to execute queries on the database
    cursor = db.cursor()

    rprint("[green] Database connection established successfully - creating new configuration [/green]")

    # Create a new database named 'password_manager', if it does not exist.
    try:    
        cursor.execute("CREATE DATABASE IF NOT EXISTS password_manager")
    except Exception as e:
        rprint(f"[red][!] An error occurred while creating the database")
        console.print_exception(show_locals=True)
        sys.exit(1)

    rprint("[green][+][/green] database 'password_manager' created successfully")

    # Create tables to contain masterkey hash + device secret and user entries

    # TODO - Add a check for the existence of the tables before creating them, print different message if they already exist
    query = "CREATE TABLE password_manager.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    response = cursor.execute(query)
    rprint("[green][+][/green] table 'secrets' created successfully")

    # Next, create a table named 'entries' in the database, which stores the user's entries in its columns
    # TODO - Add a check for the existence of the tables before creating them, print different message if they already existmysql -u username -pmysqld --skip-grant-tables
    query = "CREATE TABLE password_manager.entries (id INT NOT NULL, sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    response = cursor.execute(query)
    rprint("[green][+][/green] table 'entries' created successfully")

    # Get the master password from the user
    masterkey = ""
    while True:
        #TODO - Add a check for password strength
        masterkey = getpass("Enter a master password: ")
        confirm = getpass("Confirm the master password: ")

        if masterkey == confirm and len(masterkey) > 0:
            break
        else:
            rprint("[red][!] Passwords do not match. Please try again") 

    # Hash the master password
    masterkey_hashed = hashlib.sha256(masterkey.encode()).hexdigest()
    rprint("[green][+][/green] Master password hashed successfully")

    # Generate a device secret
    device_secret = genDeviceSecret()

    # Insert hashed master password and device secret into the 'secrets' table
    # TODO: should there be more than one?
    query = "INSERT INTO password_manager.secrets (masterkey_hash, device_secret) VALUES (%s, %s)"
    val = (masterkey_hashed, device_secret)
    cursor.execute(query, val)
    db.commit()

    rprint("[green][+][/green] Master password and device secret inserted successfully")
    rprint("[green] Configuration completed successfully [/green]")
    db.close()

if __name__ == "__main__":
    config()