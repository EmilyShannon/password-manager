
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys
 
def encrypt(key, source, encode=True, keyType = 'hex'):
	assert keyType == "hex", "Key type must be hex"
	source = source.encode()
    # Convert key from hex to bytes 
	key = bytes(bytearray.fromhex(key))
    # Create the random initialization vector to ensure uniqueness of encrypted data
	initialization_vec = Random.new().read(AES.block_size)
	# Using AES 
	encryptor = AES.new(key, AES.MODE_CBC, initialization_vec)
	padding = AES.block_size - len(source) % AES.block_size 
	source += bytes([padding]) * padding 
	data = initialization_vec + encryptor.encrypt(source) 
	return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True, keyType = "hex"):
	assert keyType == "hex", "Key type must be hex"
	source = source.encode()
	if decode:
		source = base64.b64decode(source)
	key = bytes(bytearray.fromhex(key))
	initialization_vec = source[:AES.block_size]  
	decryptor = AES.new(key, AES.MODE_CBC, initialization_vec)
	data = decryptor.decrypt(source[AES.block_size:])  # decrypt
	padding = data[-1]  
	if data[-padding:] != bytes([padding]) * padding: 
		raise ValueError("Invalid padding...")
	return data[:-padding]  # remove the padding