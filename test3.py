import ecdsa
from SignaturesECDSA import SignaturesECDSA
import pickle

myPrivateSigning, myVerifyingKey = SignaturesECDSA().loadKey()
walletAddress, wif = SignaturesECDSA().make_address(myVerifyingKey.to_string())

import base64

with open("t.png", "rb") as imageFile:
    x = pickle.dumps(imageFile.read())

    print(x.hex())

    #print(SignaturesECDSA().sign(x, myPrivateSigning).hex())




data = ''

for i in range(100000):
    data += str(i)

print(SignaturesECDSA().sign(data, myPrivateSigning).hex())