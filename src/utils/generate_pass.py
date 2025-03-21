import random
import string

def generatePass(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))