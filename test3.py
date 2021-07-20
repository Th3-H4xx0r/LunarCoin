from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import time
import os.path
from os import path

secret_message = b'ATTACK AT DAWN' * 30

key = None
loadReq = False
if(path.exists('testKEY.pem') != True):
    tic = time.perf_counter()


    ### First, make a key and save it
    key = RSA.generate(4096)
    with open( 'testKEY.pem', 'wb' ) as f:
        f.write( key.exportKey( 'PEM' ))
    
    ### Then use key to encrypt and save our message

    print("Key generation done")

    toc = time.perf_counter()

else:
    loadReq = True
    with open('testKEY.pem', 'rb') as f:
        key = RSA.importKey(f.read())

tic1 = time.perf_counter()

public_crypter = PKCS1_OAEP.new( key )
enc_data = public_crypter.encrypt( secret_message )

print(enc_data)

toc1 = time.perf_counter()
#with open( 'encrypted.txt', 'wb' ) as f:
#    f.write( enc_data )

### And later on load and decode
#with open( 'mykey.pem', 'r' ) as f:
#    key = RSA.importKey( f.read() )

#with open( 'encrypted.txt', 'rb' ) as f:
#    encrypted_data = f.read()

tic2 = time.perf_counter()
public_crypter =  PKCS1_OAEP.new( key )
decrypted_data = public_crypter.decrypt( enc_data )

#print(decrypted_data)

toc2 = time.perf_counter()

if(loadReq == False):    
    print(f"Created key in {toc - tic:0.4f} seconds")
print(f"Encrypted in {toc1 - tic1:0.4f} seconds")
print(f"Decrypted in {toc2 - tic2:0.4f} seconds")