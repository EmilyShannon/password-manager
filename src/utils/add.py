from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from utils.databaseconfig import databaseconfig
from rich import print as rprint
import utils.encrypt_decrypt as aes

def computeMasterKey(master_pass, device_secret):
    password = master_pass.encode()
    salt = device_secret.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key.hex()

def addEntry(master_pass, device_secret, sitename, siteurl, email, username):
    # Ask for user password
    password = getpass("Your password: ")
    master_key = computeMasterKey(master_pass, device_secret)
    encrypted_pass = aes.encrypt(key=master_key, source=password) 
                                 #keyType='bytes')

    #Add the entry 
    data_base = databaseconfig()
    cursor = data_base.cursor()
    query = "SELECT * FROM password_manager.entries"
    cursor.execute(query)
    results = cursor.fetchall()
    id = len(results)
    query = "INSERT INTO password_manager.entries (id, sitename, siteurl, email, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
    val=(id, sitename, siteurl, email, username, encrypted_pass)
    
    try:
        cursor.execute(query, val)
        data_base.commit()
        rprint("[green][+][/green] Entry added successfully")
    except Exception as e:
        rprint("[red][!] An error occurred while adding the entry")
        rprint(e)
        # Undo any part of the transaction that has been executed
        data_base.rollback()
