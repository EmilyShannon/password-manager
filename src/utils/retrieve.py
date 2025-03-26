from utils.databaseconfig import databaseconfig
from rich import print as rprint
from rich.table import Table
from utils.add import computeMasterKey
import utils.encrypt_decrypt as aes
import pyperclip

def retrieveEntries(master_pass, device_secret, search, decrypt_pass = False):
    data_base = databaseconfig()
    cursor = data_base.cursor()
    
    #Empty string passed as search query will return all entries
    if len(search) == 0:
        query = "SELECT * FROM password_manager.entries"
    else:
        query = "SELECT * FROM password_manager.entries WHERE "
        for i in search:
            query += f"{i} = '{search[i]}' AND "
        # Remove the last ' AND '
        query = query[:-5]

    try:
        cursor.execute(query)
    except Exception as e:
        rprint("[red][!] An error occurred while retrieving the entries")
        rprint(e)
        data_base.rollback()
        return None

    results = cursor.fetchall()
    if len(results) == 0:
        rprint("[yellow][!] No entries found")
        return None
        
    data_base.close()
    return results
    
def display_retrieval_results(master_pass, device_secret, results, decrypt_pass=False):
    # If there are multiple results, display a table
    if (decrypt_pass and len(results) > 1) or (not decrypt_pass):
        table = Table(title="Results for password retrieval")
        table.add_column("Site Name")
        table.add_column("Site URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for result in results:
            table.add_row(result[0], result[1], result[2], result[3],"{Hidden}")

    if (decrypt_pass and len(results) == 1):
        masterkey = computeMasterKey(master_pass, device_secret)
        decrypted_pass = aes.decrypt(key=masterkey, source=results[0][4])
        # Copy decrypted password to the clipboard 
        pyperclip.copy(decrypted_pass.decode()) 
        rprint("[green][+][/green] Password copied to clipboard")

    return table