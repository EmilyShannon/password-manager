from  utils.retrieve import retrieve_entries
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from utils.add import computeMasterKey
import utils.encrypt_decrypt as aes
import pyperclip

def delete_entry(master_pass, device_secret, search, decrypt_pass = False):
    results, data_base = retrieve_entries(master_pass, device_secret, search, decrypt_pass)
    display_delete_results(master_pass, device_secret, results, data_base, decrypt_pass)

def display_delete_results(master_pass, device_secret, results, data_base, decrypt_pass=False):
    
    if not results:
        return
    
    finished_deleting = False
    cursor = data_base.cursor()
    entry_to_delete = None

    # If there are multiple results, display a table
    table = Table(title="Results for password retrieval")
    table.add_column("ID")
    table.add_column("Site Name")
    table.add_column("Site URL")
    table.add_column("Email")
    table.add_column("Username")
    table.add_column("Password")

    for result in results:
        table.add_row(str(result[0]), result[1], result[2], result[3], result[4], "{Hidden}")


    console = Console()
    console.print(table)

    while not finished_deleting:

        if not results:
            finished_deleting = True

        elif len(results) == 1:
            rprint("[yellow][+][/yellow] Would you like to delete this entry? y/(n)")
            delete = input().lower() 
            
            if delete in ['y', 'yes']:
                entry_to_delete = results[0]
                entry_to_delete_id = int(entry_to_delete[0])
                query = f"DELETE FROM password_manager.entries WHERE id = {entry_to_delete_id}"
            
                try:
                    cursor.execute(query)
                    data_base.commit()
                    rprint("[green][+][/green] Entry deleted successfully")
                except Exception as e:
                    rprint("[red][!] An error occurred while deleting the entry")
                    rprint(e)
                    data_base.rollback()
                    return None
                finished_deleting = True

            elif delete in ['n', 'no']:
                finished_deleting = True
            
            else: 
                rprint("[orange][+][/orange] Please input 'yes' or 'y', or 'no' or 'n'")

        else: # more than one result
            delete= True
            while delete:
                rprint("[yellow][+][/yellow] Would you like to delete any of these entries? y/(n)")
                delete_answer = input().lower() 
                
                if delete_answer in ['y', 'yes']:
                    rprint(f"[yellow][+][/yellow] Which entry would you like to delete? (0-{len(results)-1})")
                    index = int(input())
                
                    if index in range(0, len(results)+1):
                        entry_to_delete = results[index]
                        entry_to_delete_id = int(entry_to_delete[0])
                        query = f"DELETE FROM password_manager.entries WHERE id = {entry_to_delete_id}"
                    
                        try:
                            cursor.execute(query)
                            data_base.commit()
                            rprint("[green][+][/green] Entry deleted successfully")
                        except Exception as e:
                            rprint("[red][!] An error occurred while deleting the entry")
                            rprint(e)
                            data_base.rollback()
                            return None
                        del results[index]
                    
                    else:
                        rprint("[orange][+][/orange] The index you entered is out of range. Remember, the indices start at 0.")

                elif delete_answer in ['n', 'no']:
                    delete = False
                    finished_deleting = True
                
                else: 
                    rprint("[orange][+][/orange] Please input 'yes' or 'y', or 'no' or 'n'")


    return table