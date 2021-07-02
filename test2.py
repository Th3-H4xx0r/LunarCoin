import sys
import math
from progress.bar import Bar
import pickle

from ecdsa import SigningKey, SECP256k1
from ecdsa import VerifyingKey

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

#x = b'0' * 1024 * 1024 * 1024


'''
bar = Bar('Loading', max=byteSize)

for i in range(byteSize):
    x.append(b"0")
    bar.next()

bar.finish()
'''
#print(sys.getsizeof(x))

#print(convert_size(sys.getsizeof(x)))

'''
print("Writing")
with open('test.dat', 'wb') as fileW:
    pickle.dump(x, fileW)
'''
print("reading")

'''
with open('test.dat', 'rb') as fileR:
    dat = pickle.load(fileR)

    print("size: " + str(convert_size(sys.getsizeof(dat))))
'''

#signing_key = SigningKey.generate(curve=SECP256k1)
#signature = signing_key.sign(x)

#print(signature)

#print(convert_size(sys.getsizeof(signature)))
'''

keyPair = RSA.generate(3072)

pubKey = keyPair.publickey()
#print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
#print(pubKeyPEM.decode('ascii'))

#print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
#print(privKeyPEM.decode('ascii'))

msg = b'0' * 102

print(sys.getsizeof(msg))
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(msg)
print("Encrypted:", binascii.hexlify(encrypted))

#print(encrypted)

print(sys.getsizeof(binascii.hexlify(encrypted)))

decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted)
print('Decrypted:', decrypted)

'''

from Crypto.Cipher import AES

for i in range(5):
    obj = AES.new(b'This is a key123' * 2, AES.MODE_CBC, b'This is an IV456')
    message = b"The answer is no"
    ciphertext = obj.encrypt(message)
    #print(ciphertext)
    # '\xd6\x83\x8dd!VT\x92\xaa`A\x05\xe0\x9b\x8b\xf1'
    #obj2 = AES.new(b'This is a key123', AES.MODE_CBC, b'This is an IV456')
    #print(obj2.decrypt(ciphertext))
    # 'The answer is no'

    print(sys.getsizeof(message))

    #print(ciphertext)
    print(sys.getsizeof(ciphertext))

y = input(">")
