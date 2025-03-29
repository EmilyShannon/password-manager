import utils.retrieve 
def update_pass(master_pass, device_secret, search, decrypt_pass = False):
    results = retrieve.retrieveEntries(master_pass, device_secret, search, decrypt_pass = False)

    if results == None:
        return 
    
    if len(results) == 1:
        # TODO ask the user to enter and confirm their new password for the account
        pass

    else:
        # TODO ask the user which entry they change the password for then get the new one.
        pass