from SignaturesECDSA import SignaturesECDSA
import ecdsa
from hashlib import sha256
import socket
import json
import hashlib

#pk = ecdsa.SigningKey.from_string(bytes.fromhex('c4d2c2a1cdeb1e3bb5746172f468268b94a9c892a106402435a1371800311121'), curve=ecdsa.SECP256k1)

#verifying = pk.get_verifying_key()

#print("VERIFYING KEY: " + str(verifying.to_string().hex()))

#print(hashlib.sha256(b"hello").hexdigest())


vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(
    '045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd8644'
    ), curve=ecdsa.SECP256k1, hashfunc=sha256)




signature = 'fbafe56cf44efea628617237877d73e65d3e50075e272ff57d12dd2c1c0862ed5ed8dde4eed52f1be551cac5c2b758372ad8d70835cc0a2471c24ef1134cad75'
message = b'LC123410.01634019557.649045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd86440xfuitUDWmLkyQwK8ooZb3aTRQgAQPDHd3d1sgd2pvAZRo66VGHhbLpEu1IRWFN52a2BO5nlCwGg010DN7FV3h03oTqyfLcrp8'
           #LC123410.01634019.5576489998045feff91e0171e2fa0c96863e0b4054747e10e295854b91a5af274c0d2bde908f4f3f9f5a74f6b232b42c1ac3f9d4cb628420fb518bddbe0a7cb8b8a869cd86440xfuitUDWmLkyQwK8ooZb3aTRQgAQPDHd3d1sgd2pvAZRo66VGHhbLpEu1IRWFN52a2BO5nlCwGg010DN7FV3h03oTqyfLcrp8

verified = vk.verify(bytes.fromhex(signature), message)
print(verified) # True

#print("VERIFYING HEX: " + str(vk.to_string().hex()))

#signature = pk.sign(bytes('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 'utf-8'))

#print(signature.hex())



print(SignaturesECDSA().verify(message,
bytes.fromhex(signature), 
 vk))


#verify(self, message, sig, verifyingKey):

'''
print(SignaturesECDSA().verify(b'2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824',
bytes.fromhex('450723c5df627fa68a3d66f49ef9756bbdc1eb5eab536f8fa010557557a59951a4425b2db86d32105f596244069a772ad50136fbd4138a41a8a32c82fb187f5d'), 
 vk))

'''


'''
PRIVATE: 3866a6e7197f300fe8901ea06a2cf34fe8c67c18d7766cb9456755672d214fc4
PRIVATE HEX: 3866a6e7197f300fe8901ea06a2cf34fe8c67c18d7766cb9456755672d214fc4
PUBLIC: 04a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e69c8a42402b8fa9158f0708b0bd18ba7a87601be25b617c85513b15d663093750
PUBLIC HEX: 04a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e69c8a42402b8fa9158f0708b0bd18ba7a87601be25b617c85513b15d663093750
PUBLIC COMPRESSED: 02a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e6
SIGNATURE: f207975756018d5e6eaa714bd2239e1a9cb228c187bb7b55ec19140ee8cdab0225fc7c1881d8e4fcafd72aef7b3b1e395dc3bd01e46dd894899033238e4c89d9
'''