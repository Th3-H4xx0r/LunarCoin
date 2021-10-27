from SignaturesECDSA import SignaturesECDSA
import ecdsa
from hashlib import sha256
import socket
import json
import hashlib
import pickle

#pk = ecdsa.SigningKey.from_string(bytes.fromhex('c4d2c2a1cdeb1e3bb5746172f468268b94a9c892a106402435a1371800311121'), curve=ecdsa.SECP256k1)

#verifying = pk.get_verifying_key()

#print("VERIFYING KEY: " + str(verifying.to_string().hex()))

#print(hashlib.sha256(b"hello").hexdigest())


vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(
    'a757df5e261c3e2c1378a3b4b7bc755619183d3a19dea5063915ad5b30a4f7b9368fc0c2f7827e3913ed7759f299ba60529b2dc646d83307cc4b9f2d40fb849c'
    ), curve=ecdsa.SECP256k1, hashfunc=sha256)




signature = '228febac04aa2aa4f88288a20d17bfae128b209d1d25ede0b255023307f7342007bbdbe97f05bef231161d9c397113a1f2f23c5415466677c6db0b187c14dcd0'
message = b'asdf'
           #LC123410.01634019.5576489998045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd86440xfuitUDWmLkyQwK8ooZb3aTRQgAQPDHd3d1sgd2pvAZRo66VGHhbLpEu1IRWFN52a2BO5nlCwGg010DN7FV3h03oTqyfLcrp8

#verified = vk.verify(bytes.fromhex(signature), message)
#print(verified) # True

#print("VERIFYING HEX: " + str(vk.to_string().hex()))

#signature = pk.sign(bytes('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 'utf-8'))

#print(signature.hex())

x = pickle.dumps({"key": pickle.dumps(vk)})

y = pickle.loads(x)
print(y)
print(pickle.loads(y['key']))
