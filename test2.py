import pickle
import sys
import uuid
import base64
import basehash
import zlib
import ecdsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

'''
private_key = ec.generate_private_key(
    ec.SECP384R1()
)
chosen_hash = hashes.SHA256()
hasher = hashes.Hash(chosen_hash)
hasher.update(b"data & ")
hasher.update(b"more data")
digest = hasher.finalize()
sig = private_key.sign(
    digest,
    ec.ECDSA(utils.Prehashed(chosen_hash))
)
public_key = private_key.public_key()

publicBytes = public_key.public_bytes(encoding=serialization.Encoding.PEM,
     format=serialization.PublicFormat.SubjectPublicKeyInfo
)

#print(publicBytes)
'''
def base58KEY(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    # Get the number of leading zeros
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    # Convert hex to decimal
    address_int = int(address_hex, 16)
    # Append digits to the start of string
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    # Add ‘1’ for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string

private_key_bytes = codecs.decode(private_key, 'hex')
# Get ECDSA public key
key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
key_bytes = key.to_string()
key_hex = codecs.encode(key_bytes, 'hex')


'''
sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1) #this is your sign (private key)
private_key = sk.to_string().hex() #convert your private key to hex
vk = sk.get_verifying_key() #this is your verification key (public key)
public_key = vk.to_string().hex()

print("KEY:" + str(base58KEY(public_key)))

#print(public_key)
#we are going to encode the public key to make it shorter
public_key = base64.b64encode(bytes.fromhex(public_key))

#print(public_key)
'''
'''
key = b'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANN/zgMTrkYsV5Lc+ZrXJlWmt1GM+mue\nNupg/CPYQIBoXUi5ftB1kmz85u+7e9iH6lrurwtAGCu7bHTsjD4WGosCAwEAAQ=='

print ("size of original: " + str(len(key)))

compressed = zlib.compress(key)

print("size of compressed: " + str(len(compressed)))

print(compressed)

print(zlib.decompress(compressed))
'''


#id = uuid.UUID(key)

#print(id.int)

#short = base64.b32encode(key)

#print(short)