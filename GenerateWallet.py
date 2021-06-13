# Imports
from SignaturesECDSA import SignaturesECDSA
import os.path
from os import path



try:
    exists = path.exists("key.pem")

    if(exists):
        print("Wallet already exists. Cannot create new one unless old one is deleted. Delete privateKey.pem if you want to create a new wallet.")
    else:
        myPrivate = SignaturesECDSA().generateKeys()

        SignaturesECDSA().saveKey(myPrivate)

        print("New wallet created")

except Exception as e:
    print("An error has occured: " + str(e))
