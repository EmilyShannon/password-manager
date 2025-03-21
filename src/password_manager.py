import argparse
import string
from getpass import getpass
import hashlib
import sys
import pyperclip
from rich import print as rprint
from utils.databaseconfig import databaseconfig
from utils.add import addEntry
import utils.retrieve
import utils.generate_pass

# TODO: Add description
parser = argparse.ArgumentParser(description="")

# TODO: add a delete option
parser.add_argument("option", help="Options: (a) - add, (r) - retrieve, (g) - generate password")
parser.add_argument("-L", "--length", type=int, default=16, help="Length of the password to generate")
parser.add_argument("-s", "--site", help="Site Name")
parser.add_argument("-l", "--login", help="Username")
parser.add_argument("-e", "--email", help="Email Address")
parser.add_argument("-u", "--url", help="Site URL")
parser.add_argument("-c", "--copy", action="store_true", help="Copy password to the clipboard")

args = parser.parse_args()

def getAndValidateMasterPass():
    master_pass = getpass("Enter your master password: ")
    hashed_masterpass = hashlib.sha256(master_pass.encode()).hexdigest()

    try:
        data_base = databaseconfig()
        cursor = data_base.cursor()
        cursor.execute("SELECT * FROM password_manager.secrets ORDER BY created_at DESC") # Select all rows from the secrets table, in descending order of their timestamp
    except Exception as e:
        rprint("[red][!] An error occurred while retrieving the master password")
        rprint(e)
        sys.exit(1)

    result = cursor.fetchone() # Get most recent hash masterkey 
    
    if result[0] != hashed_masterpass:
        rprint("[red][!] Master password is incorrect")
        sys.exit(1)

    return [master_pass, result[1]]

def main():
    if args.option in ["a", "add"]:
        # TODO: Allow them to enter fields instead of exiting
        if args.site == None:
            rprint("[red][!] Site Name (-s) is required")
            sys.exit(1)
        if args.login == None:
            rprint("[red][!] Username (-l) is required")
            sys.exit(1)
        if args.url == None:
            rprint("[red][!] Site URL (-u) is required")
            sys.exit(1)
        # Email not required but we need to void NoneType error 
        if args.email == None:
            args.email = "" 

        result = getAndValidateMasterPass()

        if result is not None:
            master_pass, device_secret = result[0], result[1]
            addEntry(master_pass, device_secret, args.site, args.url, args.email, args.login)

    if args.option in ["r", "retrieve"]:
        result = getAndValidateMasterPass()

        search = {}

        if args.site is not None:
            search["sitename"] = args.site
        if args.login is not None:
            search["username"] = args.login
        if args.email is not None:
            search["email"] = args.email
        if args.url is not None:
            search["siteurl"] = args.url
        

        if result is not None:
            utils.retrieve.retrieveEntries(result[0], result[1], search, decrypt_pass=args.copy)


    if args.option in ["g", "generate"]:
        if args.length == None:
            rprint("[red][!] Password length is required (-l) or (--length)")
            sys.exit(1)
        else:
            password = utils.generate_pass.generatePass(args.length)
            pyperclip.copy(password)
            rprint("[green][+][/green] Password generated and copied to clipboard")

main()