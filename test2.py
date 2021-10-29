from SignaturesECDSA import SignaturesECDSA
import ecdsa
import hashlib
import binascii



myPrivateSigning, myVerifyingKey = SignaturesECDSA().loadKey()

data = '1'

publicHex = myVerifyingKey.to_string().hex()

print(publicHex)


sig = SignaturesECDSA().sign(data, myPrivateSigning)

print(sig)


publicKeyVerifyObject = ecdsa.VerifyingKey.from_string(bytes.fromhex(publicHex), curve=ecdsa.SECP256k1)


# (self, message, sig, verifyingKey):

print(SignaturesECDSA().verify(data.encode('utf-8'), sig, publicKeyVerifyObject))



