from SignaturesECDSA import SignaturesECDSA
import ecdsa
from hashlib import sha256
import socket
import json

priv = SignaturesECDSA().generateKeys()

print(priv.to_string())

vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(
    '04a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e69c8a42402b8fa9158f0708b0bd18ba7a87601be25b617c85513b15d663093750'
    ), curve=ecdsa.SECP256k1, hashfunc=sha256)


print(SignaturesECDSA().verify(b'hello world', bytes.fromhex(
    'f207975756018d5e6eaa714bd2239e1a9cb228c187bb7b55ec19140ee8cdab0225fc7c1881d8e4fcafd72aef7b3b1e395dc3bd01e46dd894899033238e4c89d9'
    ), vk))
#print(vk.verify(bytes.fromhex('f207975756018d5e6eaa714bd2239e1a9cb228c187bb7b55ec19140ee8cdab0225fc7c1881d8e4fcafd72aef7b3b1e395dc3bd01e46dd894899033238e4c89d9'), b'hello world'))
#print(sendPublic)

#verify(self, message, sig, verifyingKey):

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('2.tcp.ngrok.io', 11984))

jsonData = json.dumps({'data': 'f207975756018d5e6eaa714bd2239e1a9cb228c187bb7b55ec19140ee8cdab0225fc7c1881d8e4fcafd72aef7b3b1e395dc3bd01e46dd894899033238e4c89d9'})


s.sendall(bytes(jsonData,encoding="utf-8"))
'''
PRIVATE: 3866a6e7197f300fe8901ea06a2cf34fe8c67c18d7766cb9456755672d214fc4
PRIVATE HEX: 3866a6e7197f300fe8901ea06a2cf34fe8c67c18d7766cb9456755672d214fc4
PUBLIC: 04a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e69c8a42402b8fa9158f0708b0bd18ba7a87601be25b617c85513b15d663093750
PUBLIC HEX: 04a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e69c8a42402b8fa9158f0708b0bd18ba7a87601be25b617c85513b15d663093750
PUBLIC COMPRESSED: 02a83b77fad17144e5f86bc7d672035dc967d78981836ae37f40a5b73db311d1e6
SIGNATURE: f207975756018d5e6eaa714bd2239e1a9cb228c187bb7b55ec19140ee8cdab0225fc7c1881d8e4fcafd72aef7b3b1e395dc3bd01e46dd894899033238e4c89d9
'''